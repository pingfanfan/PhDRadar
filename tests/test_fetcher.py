"""Fetcher 的礼貌访问：robots.txt 的 Crawl-delay 从第一个请求就生效；429 时退避更久。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scrapers import common  # noqa: E402


class Resp:
    def __init__(self, status=200, text="", headers=None):
        self.status_code, self.text, self.headers = status, text, headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise common.requests.HTTPError(str(self.status_code))


class Clock:
    def __init__(self):
        self.now, self.slept = 1000.0, []

    def monotonic(self):
        return self.now

    def sleep(self, s):
        self.slept.append(round(s, 2))
        self.now += s


def make(monkeypatch, responses):
    clock = Clock()
    monkeypatch.setattr(common.time, "monotonic", clock.monotonic)
    monkeypatch.setattr(common.time, "sleep", clock.sleep)
    f = common.Fetcher(delay=1.0)
    calls = []

    def get(url, **kw):
        calls.append(url)
        return responses[url].pop(0) if isinstance(responses[url], list) else responses[url]
    monkeypatch.setattr(f.session, "get", get)
    return f, clock, calls


def test_first_request_waits_crawl_delay_after_robots(monkeypatch):
    f, clock, calls = make(monkeypatch, {
        "https://ex.org/robots.txt": Resp(text="User-agent: *\nCrawl-delay: 5\n"),
        "https://ex.org/jobs": Resp(text="ok"),
    })
    assert f.get("https://ex.org/jobs").text == "ok"
    assert calls == ["https://ex.org/robots.txt", "https://ex.org/jobs"]
    assert clock.slept == [5.0]  # 取完 robots.txt 后等满 5 秒再发第一个请求


def test_429_without_retry_after_backs_off_longer(monkeypatch):
    f, clock, _ = make(monkeypatch, {
        "https://ex.org/robots.txt": Resp(status=404),
        "https://ex.org/jobs": [Resp(status=429), Resp(text="ok")],
    })
    assert f.get("https://ex.org/jobs").text == "ok"
    assert 30 in clock.slept
