#!/usr/bin/env python3
"""探测一个招聘平台能否按规矩抓取：读 robots.txt 允许的站点地图，列出匹配的岗位链接，存几个样例页。

    python scripts/probe_portal.py --sitemap https://www.findapostdoc.com/sitemap.xml --pattern '/postdoc/' -n 8

所有请求都走 Fetcher（遵守 robots.txt、限速）；遇到人机验证就停，不做任何绕过。
样例页存到 research/inbox/samples/probe-*.html，用来写正式的解析规则。
"""
from __future__ import annotations

import argparse
import gzip
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scrapers.common import Disallowed, Fetcher  # noqa: E402

LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def load(f: Fetcher, url: str) -> str:
    r = f.get(url)
    if "Just a moment" in r.text[:3000]:
        raise SystemExit(f"被人机验证拦截：{url}（停止，不做绕过）")
    body = r.content
    return gzip.decompress(body).decode("utf-8", "replace") if body[:2] == b"\x1f\x8b" else r.text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitemap", action="append", required=True, help="站点地图或索引（可多次）")
    ap.add_argument("--pattern", required=True, help="岗位链接需匹配的正则")
    ap.add_argument("-n", type=int, default=8, help="保存几个样例页")
    ap.add_argument("--max-sitemaps", type=int, default=30)
    args = ap.parse_args()
    f = Fetcher(delay=1.5)
    pat = re.compile(args.pattern, re.I)
    queue, seen, jobs = list(args.sitemap), set(), []
    while queue and len(seen) < args.max_sitemaps:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            xml = load(f, url)
        except Disallowed:
            print(f"robots.txt 不允许：{url}")
            continue
        except Exception as e:  # noqa: BLE001
            print(f"读取失败：{url} {e}")
            continue
        locs = LOC.findall(xml)
        if "<sitemapindex" in xml:
            queue += locs
        else:
            jobs += [u for u in locs if pat.search(u)]
        print(f"{url}：{len(locs)} 个链接")
    jobs = list(dict.fromkeys(jobs))
    print(f"匹配 {args.pattern!r} 的岗位链接：{len(jobs)} 个；示例：{jobs[:3]}")
    out = ROOT / "research" / "inbox" / "samples"
    out.mkdir(parents=True, exist_ok=True)
    for i, u in enumerate(jobs[: args.n]):
        try:
            (out / f"probe-{i}.html").write_text(load(f, u), encoding="utf-8")
            print(f"已存样例 {i}: {u}")
        except (Disallowed, Exception) as e:  # noqa: BLE001
            print(f"样例失败 {u}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
