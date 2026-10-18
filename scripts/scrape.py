#!/usr/bin/env python3
"""抓取带奖博士（PhD）与博士后岗位，去重后输出 JSON 和 Markdown 摘要。

示例：
    python scripts/scrape.py                                   # 抓取全部已启用信源
    python scripts/scrape.py -s euraxess,jobbnorge -k "machine learning" -k robotics
    python scripts/scrape.py --new-only                        # 只输出上次之后的新岗位
    python scripts/scrape.py --level postdoc                   # 只看博士后岗位
    python scripts/scrape.py --list                            # 列出所有抓取器
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scrapers.common import Disallowed, Fetcher, classify, matches_keywords, now_iso  # noqa: E402
from scrapers.sources import ADAPTERS  # noqa: E402

DATA = ROOT / "data"
SEEN = DATA / "seen.json"
LEVEL_LABEL = {"phd": "博士", "postdoc": "博后"}
ELIG_LABEL = {"international": "✅ 国际生可申", "restricted": "⛔ 有国籍/学费限制", "unknown": "❔ 未注明"}


def run_source(sid: str, fetcher: Fetcher, keywords: list[str], limit: int,
               levels: tuple[str, ...] = ("phd", "postdoc")) -> tuple[list, str]:
    try:
        jobs = ADAPTERS[sid](fetcher, keywords=keywords, limit=limit)
    except Disallowed as e:
        return [], f"robots.txt 不允许抓取：{e}"
    except Exception as e:  # noqa: BLE001 单个信源失败不影响整体
        return [], f"{type(e).__name__}: {str(e)[:200]}"
    stamp = now_iso()
    out = []
    for j in jobs:
        j.fetched_at = stamp
        classify(j)
        if j.level in levels and matches_keywords(j, keywords):
            out.append(j)
    return out[:limit], ""


def to_markdown(jobs: list[dict], errors: dict[str, str], title: str) -> str:
    lines = [f"# {title}", "", f"生成时间：{now_iso()}　共 {len(jobs)} 个岗位", ""]
    order = {"international": 0, "unknown": 1, "restricted": 2}
    jobs = sorted(jobs, key=lambda j: (order[j["eligibility"]], j["deadline"] or "9999", j["source"]))
    lines += ["| 层级 | 资格 | 岗位 | 机构 | 国家 | 截止 | 信源 | 标记 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for j in jobs:
        flags = ", ".join(([] if j["funding"] == "unknown" else [j["funding"]]) + j["flags"])
        title = j["title"].replace("|", "\\|")
        inst = j["institution"].replace("|", "\\|")[:60]
        lines.append(f"| {LEVEL_LABEL.get(j.get('level', 'phd'), '博士')} | {ELIG_LABEL[j['eligibility']]} | [{title}]({j['url']}) | {inst} | {j['country']} "
                     f"| {j['deadline'] or ''} | {j['source']} | {flags} |")
    if errors:
        lines += ["", "## 抓取失败的信源", ""] + [f"- `{k}`：{v}" for k, v in errors.items()]
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-s", "--sources", help="逗号分隔的信源 id，默认全部")
    p.add_argument("-k", "--keyword", action="append", default=[], help="关键词（可多次），任一命中即保留")
    p.add_argument("--limit", type=int, default=60, help="每个信源最多保留的岗位数")
    p.add_argument("--level", default="phd,postdoc", help="岗位层级：phd、postdoc 或 phd,postdoc（默认两者）")
    p.add_argument("--new-only", action="store_true", help="只输出 data/seen.json 中没有的新岗位")
    p.add_argument("--no-robots", action="store_true", help="不检查 robots.txt（不建议）")
    p.add_argument("--out", default=str(DATA / "jobs.json"))
    p.add_argument("--md", default=str(DATA / "jobs.md"))
    p.add_argument("--list", action="store_true", help="列出所有抓取器")
    args = p.parse_args()

    if args.list:
        print("\n".join(sorted(ADAPTERS)))
        return 0
    sids = args.sources.split(",") if args.sources else sorted(ADAPTERS)
    unknown = [s for s in sids if s not in ADAPTERS]
    if unknown:
        p.error(f"未知信源：{unknown}；用 --list 查看")

    fetcher = Fetcher(respect_robots=not args.no_robots)
    seen = json.loads(SEEN.read_text(encoding="utf-8")) if SEEN.exists() else {}
    all_jobs, errors = [], {}
    for sid in sids:
        t0 = time.monotonic()
        jobs, err = run_source(sid, fetcher, args.keyword, args.limit, tuple(args.level.split(",")))
        print(f"[{sid}] {len(jobs)} 个岗位 ({time.monotonic() - t0:.1f}s){'  ✗ ' + err if err else ''}", file=sys.stderr)
        if err:
            errors[sid] = err
        all_jobs += jobs

    unique = {j.id: j.to_dict() for j in all_jobs}
    if args.new_only:
        unique = {k: v for k, v in unique.items() if k not in seen}
    for k, v in unique.items():
        seen.setdefault(k, v["fetched_at"])

    DATA.mkdir(exist_ok=True)
    jobs = list(unique.values())
    Path(args.out).write_text(json.dumps({"updated_at": now_iso(), "total": len(jobs), "errors": errors,
                                          "jobs": jobs}, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.md).write_text(to_markdown(jobs, errors, "最新带奖博士/博后岗位" + ("（新增）" if args.new_only else "")),
                             encoding="utf-8")
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    print(f"共 {len(jobs)} 个岗位 → {args.out} / {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
