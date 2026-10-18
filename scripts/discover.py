#!/usr/bin/env python3
"""长期“发现”流程：寻找在招博士生的导师和新的信源，生成 reports/discovery.md。

    python scripts/discover.py                       # 运行全部渠道
    python scripts/discover.py -c bluesky,github_lists
    python scripts/discover.py --budget 800          # CSRankings 每次扫描的主页数

结果累积在 data/discovery/：
    faculty.json   疑似在招导师（主页 + 证据片段），status: new/reviewed/promoted/rejected
    sources.json   候选信源（如新出现的 GitHub 汇总仓库）
    watch.json     _data/faculty.yml 中关注导师主页的监控状态
需要外网，通常由 GitHub Actions 每周运行。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from discovery.channels import CHANNELS, Context  # noqa: E402
from discovery.store import Store  # noqa: E402
from scrapers.common import Fetcher, now_iso  # noqa: E402

REPORT = ROOT / "reports" / "discovery.md"


EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


def cell(s) -> str:
    return EMAIL.sub("[邮箱已隐去]", str(s or "")).replace("|", "/").replace("\n", " ")[:160]


def render(ctx: Context) -> str:
    fac = ctx.faculty.items
    new_fac = sorted((fac[k] for k in ctx.faculty.added), key=lambda r: -r.get("score", 0))
    pending = [r for r in fac.values() if r.get("status") == "new"]
    lines = [
        "# 发现报告", "",
        f"生成时间：{now_iso()}（`scripts/discover.py`）", "",
        *[f"- {line}" for line in ctx.log], "",
        f"累计疑似在招导师 **{len(fac)}** 位（待审核 {len(pending)}），候选信源 **{len(ctx.sources.items)}** 个。"
        "用 Claude Code 的 `/review-discoveries` 审核后，可加入 `_data/faculty.yml` 或 `_data/sources.yml`。", "",
        f"## 本次新发现的在招导师（{len(new_fac)}）", "",
        "| 导师 | 机构 | 国家 | 渠道 | 招生层次 / 年份 |", "| --- | --- | --- | --- | --- |",
    ]
    for r in new_fac[:150]:
        lines.append(f"| [{cell(r.get('name'))}]({r.get('homepage')}) | {cell(r.get('affiliation'))} | {cell(r.get('country'))} "
                     f"| {', '.join(r.get('channels', []))} | {cell(' '.join(r.get('levels') or []) + ' ' + ' '.join(r.get('years') or []))} |")
    changed = [r for r in ctx.watch.items.values() if r.get("changed_on") == now_iso()[:10]]
    lines += ["", f"## 关注导师主页变化（{len(changed)}）", ""]
    lines += [f"- [{cell(r['name'])}]({r['url']})：{'在招 ✅' if r.get('recruiting') else '内容有更新'}"
              for r in changed] or ["- 无"]
    new_src = [ctx.sources.items[k] for k in ctx.sources.added]
    lines += ["", f"## 新的候选信源（{len(new_src)}）", "", "| 名称 | 说明 | 渠道 |", "| --- | --- | --- |"]
    lines += [f"| [{cell(r['name'])}]({r['url']}) | {cell(r.get('description'))} | {', '.join(r['channels'])} |" for r in new_src[:100]]
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-c", "--channels", help="逗号分隔，默认全部：" + ",".join(CHANNELS))
    p.add_argument("--budget", type=int, default=400, help="CSRankings 每次扫描的主页数")
    args = p.parse_args()
    names = args.channels.split(",") if args.channels else list(CHANNELS)
    ctx = Context(fetcher=Fetcher(delay=0.5, timeout=20), faculty=Store("faculty"), sources=Store("sources"),
                  watch=Store("watch"), budget=args.budget)
    for name in names:
        print(f"[{name}] …", file=sys.stderr)
        try:
            CHANNELS[name](ctx)
        except Exception as e:  # noqa: BLE001 单个渠道失败不影响其他渠道
            ctx.log.append(f"{name}: 失败 {type(e).__name__}: {str(e)[:160]}")
        print(f"  {ctx.log[-1] if ctx.log else ''}", file=sys.stderr)
    for s in (ctx.faculty, ctx.sources, ctx.watch):
        s.save()
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(render(ctx), encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8")[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
