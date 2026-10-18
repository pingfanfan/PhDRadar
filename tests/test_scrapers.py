"""离线测试：用固定样例验证解析逻辑、资格识别和注册表，不访问网络。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scrapers.common import Job, classify, is_phd_posting, looks_like_phd, matches_keywords, parse_date, posting_level  # noqa: E402
from scrapers.sources import ADAPTERS, academictransfer, euraxess, jobs_ac_uk, varbi  # noqa: E402
from scrapers.sources.feeds import make_feed_adapter, parse_feed  # noqa: E402


class FakeResponse:
    def __init__(self, text="", data=None):
        self.text = text
        self.content = text.encode("utf-8")
        self._data = data

    def json(self):
        return self._data


class FakeFetcher:
    """按 URL 子串返回预设响应。"""

    def __init__(self, routes: dict[str, FakeResponse]):
        self.routes = routes
        self.requested: list[str] = []

    def get(self, url, **_):
        self.requested.append(url)
        for key, resp in self.routes.items():
            if key in url:
                return resp
        return FakeResponse("<html></html>")


def job(title="", summary=""):
    return Job(source="t", id="t:1", title=title, url="https://x", summary=summary)


# ───────── 识别规则 ─────────

@pytest.mark.parametrize("text,expected", [
    ("Fully funded PhD studentship. UK students only.", "restricted"),
    ("This position is only open to home students", "restricted"),
    ("Applicants must be a UK national", "restricted"),
    ("US citizens or permanent residents only", "restricted"),
    ("Funded PhD Project (Students Worldwide)", "international"),
    ("The position is open to all nationalities", "international"),
    ("International applicants are welcome to apply", "international"),
    ("PhD in robotics at TU Delft", "unknown"),
])
def test_eligibility(text, expected):
    assert classify(job(summary=text)).eligibility == expected


def test_funding_and_screening_flags():
    j = classify(job("PhD position", "Fully funded; candidates require ATAS clearance"))
    assert j.funding == "funded"
    assert "security-screening" in j.flags
    assert classify(job("PhD", "This is a self-funded project")).funding == "self-funded"


@pytest.mark.parametrize("raw,iso", [
    ("2026-11-30T23:59:00Z", "2026-11-30"),
    ("30.11.2026", "2026-11-30"),
    ("Deadline: 30 November 2026", "2026-11-30"),
    ("Nov 30, 2026", "2026-11-30"),
    ("Mon, 05 Oct 2026 10:00:00 +0000", "2026-10-05"),
    ("not a date", None),
])
def test_parse_date(raw, iso):
    assert parse_date(raw) == iso


def test_phd_and_keywords():
    assert looks_like_phd("Doctoral student in machine learning")
    assert looks_like_phd("PhD Research Fellow (stipendiat)")
    assert not looks_like_phd("Professor of Chemistry")
    assert matches_keywords(job("PhD in Machine Learning"), ["machine learning"])
    assert not matches_keywords(job("PhD in Ecology"), ["robotics"])
    assert matches_keywords(job("anything"), [])


@pytest.mark.parametrize("title,summary,expected", [
    ("PhD position in Quantum Optics", "", True),
    ("Doctoral researcher in Food Science, MSCA Doctoral Network", "", True),
    ("Tenure-track Assistant Professor", "Candidates must hold a PhD", False),
    ("Postdoc in Electron Optics", "", False),
    ("Postdoctoral PhD-level researcher", "", False),
    ("Penn State: Graduate Research Assistantship", "Fully funded PhD studentship in soils", True),
    ("Research Engineer", "PhD students in the group", False),
])
def test_is_phd_posting(title, summary, expected):
    assert is_phd_posting(title, summary) is expected


@pytest.mark.parametrize("title,summary,level", [
    ("PhD position in Quantum Optics", "", "phd"),
    ("PhD Research Fellow in Informatics (stipendiat)", "", "phd"),
    ("Postdoctoral Researcher in Ecology", "", "postdoc"),
    ("Postdoc or PhD student in robotics", "", "postdoc"),
    ("Research Fellow in Machine Learning", "", "postdoc"),
    ("Research Associate (fixed term)", "", "postdoc"),
    ("Tenure-track Assistant Professor", "PhD required", None),
    ("Lab Manager", "postdoc position available", None),
    ("Graduate Research Assistantship", "Two postdoctoral positions are open", "postdoc"),
])
def test_posting_level(title, summary, level):
    assert posting_level(title, summary) == level


def test_euraxess_levels():
    html = EURAXESS_HTML.replace("</ul>", '<li><article><a href="/jobs/999">Postdoc in Chemistry</a></article></li>'
                                 '<li><article><a href="/jobs/998">Full Professor of Law</a></article></li></ul>')
    jobs = euraxess.fetch(FakeFetcher({"page=0": FakeResponse(html)}), keywords=[], limit=5)
    assert [(j.id, j.level) for j in jobs] == [("euraxess:123456", "phd"), ("euraxess:999", "postdoc")]


# ───────── 解析器 ─────────

RSS = """<?xml version="1.0"?><rss version="2.0"><channel>
<item><title>PhD position in Quantum Optics</title><link>https://ex.org/job/1</link>
<description>Fully funded, open to all nationalities</description><pubDate>Mon, 05 Oct 2026 10:00:00 +0000</pubDate>
<guid>https://ex.org/job/1</guid></item>
<item><title>Professor of Physics</title><link>https://ex.org/job/2</link><description>Senior role</description></item>
</channel></rss>"""

ATOM = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Doctoral researcher</title><link rel="alternate" href="https://ex.org/a"/><id>tag:a</id>
<updated>2026-10-01T00:00:00Z</updated><summary>Stipend provided</summary></entry></feed>"""


def test_parse_feed_rss_and_atom():
    items = parse_feed(RSS)
    assert [i["title"] for i in items][:1] == ["PhD position in Quantum Optics"]
    atom = parse_feed(ATOM)
    assert atom[0]["link"] == "https://ex.org/a" and atom[0]["guid"] == "tag:a"


def test_feed_adapter_filters_non_phd():
    fetch = make_feed_adapter("demo", "https://ex.org/rss?q={q}")
    jobs = fetch(FakeFetcher({"ex.org/rss": FakeResponse(RSS)}), keywords=[], limit=10)
    assert len(jobs) == 1 and jobs[0].posted == "2026-10-05"


EURAXESS_HTML = """<html><body><ul>
<li><article><a href="/jobs/123456">PhD position in Computational Biology</a>
<a href="/partnering/organisations/profile/42">Ghent University</a>
<span>Belgium</span><span>Posted on: 1 October 2026</span><span>Application Deadline: 30 November 2026</span></article></li>
</ul></body></html>"""


def test_euraxess_parser():
    jobs = euraxess.fetch(FakeFetcher({"page=0": FakeResponse(EURAXESS_HTML)}), keywords=[], limit=5)
    assert len(jobs) == 1
    j = jobs[0]
    assert j.id == "euraxess:123456" and j.institution == "Ghent University"
    assert j.country == "Belgium" and j.deadline == "2026-11-30" and j.posted == "2026-10-01"


JOBSAC_HTML = """<div class="j-search-result__text">
<a href="/job/DMX123/phd-studentship-in-ai?ref=x">Fully Funded PhD Studentship in AI</a>
<div class="j-search-result__employer">University of Bristol</div>
<div>Date Placed: 3 Oct 2026</div></div>"""


def test_jobs_ac_uk_parser():
    jobs = jobs_ac_uk.fetch(FakeFetcher({"startIndex=1": FakeResponse(JOBSAC_HTML)}), keywords=[], limit=5)
    assert jobs[0].url == "https://www.jobs.ac.uk/job/DMX123/phd-studentship-in-ai"
    assert jobs[0].institution == "University of Bristol" and jobs[0].posted == "2026-10-03"


SITEMAP = """<urlset><url><loc>https://www.academictransfer.com/en/jobs/351234/phd-candidate-in-robotics/</loc></url>
<url><loc>https://www.academictransfer.com/en/jobs/351235/assistant-professor-in-law/</loc></url></urlset>"""
AT_DETAIL = """<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"JobPosting",
"title":"PhD Candidate in Robotics","hiringOrganization":{"name":"TU Delft"},
"jobLocation":{"address":{"addressLocality":"Delft"}},"validThrough":"2026-12-01T00:00:00+01:00",
"datePosted":"2026-10-02","description":"<p>Open to all nationalities</p>"}]}</script>"""


def test_academictransfer_parser():
    f = FakeFetcher({"sitemap": FakeResponse(SITEMAP), "/jobs/351234/": FakeResponse(AT_DETAIL)})
    jobs = academictransfer.fetch(f, keywords=[], limit=5)
    assert len(jobs) == 1
    j = jobs[0]
    assert (j.title, j.institution, j.city, j.deadline) == ("PhD Candidate in Robotics", "TU Delft", "Delft", "2026-12-01")
    assert not any("351235" in u for u in f.requested)


VARBI_HTML = """<table><tr><td class="pos-title"><a href="https://lu.varbi.com/en/what:job/jobID:777/">Doctoral student in Physics</a></td>
<td class="pos-town">Lund</td><td class="pos-ends">2026-11-15</td></tr>
<tr><td class="pos-title"><a href="https://lu.varbi.com/en/what:job/jobID:778/">Lecturer</a></td></tr></table>"""


def test_varbi_parser():
    f = FakeFetcher({"lu.varbi.com": FakeResponse(VARBI_HTML)})
    jobs = varbi.fetch(f, keywords=[], limit=5)
    assert [j.id for j in jobs] == ["varbi:lu-777"] and jobs[0].deadline == "2026-11-15"


# ───────── 注册表与数据一致性 ─────────

def test_every_adapter_maps_to_a_source():
    from catalog import load_sources

    ids = {s["id"] for s in load_sources()}
    missing = sorted(set(ADAPTERS) - ids)
    assert not missing, f"抓取器 id 不在 sources.yml 中：{missing}"


def test_fetcher_timeout_override(monkeypatch):
    from scrapers.common import Fetcher

    f = Fetcher(respect_robots=False, delay=0)
    seen = {}

    class R:
        status_code = 200

        def raise_for_status(self):
            pass

    def fake_get(url, **kw):
        seen.update(kw)
        return R()

    monkeypatch.setattr(f.session, "get", fake_get)
    f.get("https://example.org", timeout=60)
    assert seen["timeout"] == 60
