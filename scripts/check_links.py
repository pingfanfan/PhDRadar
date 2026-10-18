#!/usr/bin/env python3
"""检查 _data/sources.yml 中所有链接是否可访问。

很多学术网站会拦截脚本（403/429）或需要登录，这类结果记为“warn”而非失效；
只有 404/410、DNS/连接失败才算“dead”，并让脚本以非零状态退出。
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
import yaml

DATA = Path(__file__).resolve().parent.parent / "_data" / "sources.yml"
BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
DEAD = {404, 410}


def check_url(url: str) -> tuple[str, str]:
    """返回 (status, detail)，status ∈ ok / warn / dead。"""
    headers = {"User-Agent": BROWSER_UA, "Accept-Language": "en-US,en;q=0.9"}
    try:
        r = requests.get(url, headers=headers, timeout=25, allow_redirects=True, stream=True)
        r.close()
    except requests.ConnectionError as e:
        if "Name or service not known" in str(e) or "NameResolutionError" in str(e):
            return "dead", "DNS 解析失败"
        if isinstance(e, (requests.ConnectTimeout, requests.exceptions.SSLError)):
            return "warn", f"{type(e).__name__}（境外服务器访问受限或证书问题，浏览器中通常可打开）"
        return "warn", f"{type(e).__name__}（连接失败，可能限制境外访问）"
    except requests.RequestException as e:
        return "warn", f"{type(e).__name__}（超时）"
    final = r.url if r.url.rstrip("/") != url.rstrip("/") else ""
    detail = f"HTTP {r.status_code}" + (f" → {final}" if final else "")
    if r.status_code < 400:
        return "ok", detail
    return ("dead" if r.status_code in DEAD else "warn"), detail


def load_sources() -> list[dict]:
    sys.path.insert(0, str(DATA.parent.parent))
    from catalog import load_sources as _load

    return _load()


def check_all(sources: list[dict]) -> dict[str, tuple[str, str]]:
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = pool.map(lambda s: check_url(s["url"]), sources)
    return {s["id"]: res for s, res in zip(sources, results)}


def main() -> int:
    sources = load_sources()
    results = check_all(sources)
    bad = {k: v for k, v in results.items() if v[0] != "ok"}
    for sid, (status, detail) in sorted(bad.items(), key=lambda kv: kv[1][0]):
        print(f"[{status.upper()}] {sid}: {detail}")
    dead = sum(1 for v in results.values() if v[0] == "dead")
    print(f"\n{len(results)} checked · {dead} dead · {len(bad) - dead} warnings")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
