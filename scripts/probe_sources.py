#!/usr/bin/env python3
"""信源可用性核查：真实访问每个信源链接，并试跑每个抓取器，生成 reports/source-health.md。

用于“确认信源”：哪些链接可以打开、哪些被拦截或失效、哪些抓取器能拿到岗位。
需要外网，通常在 GitHub Actions 中运行。
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from check_links import check_all, load_sources  # noqa: E402
from scrape import run_source  # noqa: E402

from scrapers.common import Fetcher, now_iso  # noqa: E402
from scrapers.sources import ADAPTERS  # noqa: E402

REPORT = ROOT / "reports" / "source-health.md"
ICON = {"ok": "✅", "warn": "⚠️", "dead": "❌"}


def main() -> int:
    sources = load_sources()
    names = {s["id"]: s["name"] for s in sources}
    print("检查链接…", file=sys.stderr)
    links = check_all(sources)

    print("试跑抓取器…", file=sys.stderr)
    fetcher = Fetcher(delay=1.0)
    scrapers = {}
    for sid in sorted(ADAPTERS):
        t0 = time.monotonic()
        jobs, err = run_source(sid, fetcher, [], 5)
        scrapers[sid] = {
            "count": len(jobs), "error": err, "seconds": round(time.monotonic() - t0, 1),
            "sample": jobs[0].title[:80] if jobs else "",
            "sample_eligibility": jobs[0].eligibility if jobs else "",
        }
        print(f"[{sid}] {len(jobs)} {err}", file=sys.stderr)

    ok = sum(1 for v in links.values() if v[0] == "ok")
    working = sum(1 for v in scrapers.values() if v["count"])
    lines = [
        "# 信源可用性报告", "",
        f"生成时间：{now_iso()}（由 `scripts/probe_sources.py` 在 GitHub Actions 中真实访问生成）", "",
        f"- 链接：{len(links)} 个，✅ 可访问 {ok}，⚠️ 被拦截/需登录 "
        f"{sum(1 for v in links.values() if v[0] == 'warn')}，❌ 失效 {sum(1 for v in links.values() if v[0] == 'dead')}",
        f"- 抓取器：{len(scrapers)} 个，能拿到岗位 {working} 个", "",
        "## 抓取器", "", "| 信源 | 状态 | 样例岗位 | 耗时 | 错误 |", "| --- | :-: | --- | --- | --- |",
    ]
    for sid, r in scrapers.items():
        status = "✅" if r["count"] else ("❌" if r["error"] else "⚠️ 0 条")
        lines.append(f"| `{sid}` | {status} {r['count'] or ''} | {r['sample'].replace('|', '/')} "
                     f"| {r['seconds']}s | {r['error'].replace('|', '/')} |")
    lines += ["", "## 需要关注的链接", "", "⚠️ 多为网站拦截脚本访问（403/429）或需要登录，浏览器中通常可正常打开；❌ 需修复。", "",
              "| 信源 | 状态 | 详情 |", "| --- | :-: | --- |"]
    for sid, (status, detail) in sorted(links.items(), key=lambda kv: (kv[1][0] != "dead", kv[0])):
        if status != "ok":
            lines.append(f"| `{sid}` {names[sid]} | {ICON[status]} | {detail} |")
    redirected = [(sid, d) for sid, (s, d) in links.items() if s == "ok" and "→" in d]
    if redirected:
        lines += ["", "## 发生跳转的链接（可考虑更新为最终地址）", "", "| 信源 | 详情 |", "| --- | --- |"]
        lines += [f"| `{sid}` | {d} |" for sid, d in redirected]

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (REPORT.with_suffix(".json")).write_text(json.dumps(
        {"generated_at": now_iso(), "links": {k: list(v) for k, v in links.items()}, "scrapers": scrapers},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
