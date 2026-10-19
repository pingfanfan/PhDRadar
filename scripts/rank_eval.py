#!/usr/bin/env python3
"""/rank 评测：用 tests/rank_eval_profiles.yml 的虚构画像排序，对照人工标注 tests/rank_eval_labels.yml 算前 10 准确率。

    python scripts/rank_eval.py                 # 打印每个画像的前 10 与准确率；未标注的条目标 “?”
    python scripts/rank_eval.py --today 2026-10-19 --only p03-medimg

标注规则（docs/rank-eval.md）：1 = 按这个画像，这条值得出现在前 10；0 = 不该推荐（方向不对口、明显不合适）。
标注按机会 id 记录，换一天的数据重跑时只需补标新出现的条目。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import rank  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default="2026-10-19")
    ap.add_argument("--only", default="")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    profiles = yaml.safe_load((ROOT / "tests" / "rank_eval_profiles.yml").read_text(encoding="utf-8"))
    lf = ROOT / "tests" / "rank_eval_labels.yml"
    labels = (yaml.safe_load(lf.read_text(encoding="utf-8")) if lf.exists() else None) or {}
    rows = json.loads((ROOT / "assets" / "catalog.json").read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in rows}
    today = date.fromisoformat(a.today)
    stats = {False: [0, 0, 0], True: [0, 0, 0]}  # 调规则用的画像 / 留出画像：命中、总数、未标注
    for p in profiles:
        if a.only and p["id"] != a.only:
            continue
        res = rank.rank(rows, p, today)
        lab = labels.get(p["id"]) or {}
        top = res["ranked"][:a.top]
        g = sum(1 for r in top if lab.get(r["id"]) == 1)
        u = sum(1 for r in top if r["id"] not in lab)
        st = stats[bool(p.get("heldout"))]
        st[0], st[1], st[2] = st[0] + g, st[1] + len(top), st[2] + u
        print(f"\n## {p['id']}（{p.get('note', '')}）推荐 {len(res['ranked'])} · 排除 {len(res['excluded'])} · 不相关 {res['unrelated']}"
              f" · 前 {len(top)} 条命中 {g}" + (f"，未标注 {u}" if u else ""))
        for r in top:
            x = by_id[r["id"]]
            mark = {1: "✓", 0: "✗"}.get(lab.get(r["id"]), "?")
            print(f"  {mark} {r['score']:>3} {r['id']} | {x['n'][:110]} | {x.get('org', '')[:40]} | {','.join(x.get('r', []))} | {','.join(r['hits'])}")
    for held, (good, total, unlabeled) in stats.items():
        if total:
            print(f"\n{'留出画像' if held else '调规则用的画像'}前 {a.top} 准确率：{good}/{total} = {good / total:.0%}"
                  + (f"（另有 {unlabeled} 条未标注）" if unlabeled else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
