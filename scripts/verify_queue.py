#!/usr/bin/env python3
"""生成待核实的信源队列（供研究员每轮核实一批“不确定”的信息）。

    python scripts/verify_queue.py --worker 2 --of 3 --n 25 > research/inbox/verify-queue.yml
    # 专职核实员：在全部信源中按序号分片，只取 2026-10-14 之前未核实过的，分成 4 份给 4 个子代理
    python scripts/verify_queue.py --scope all --worker 1 --of 3 --before 2026-10-14 --n 80 --chunks 4 --out research/inbox/verify-v1

优先级：① 链接核查报告中 ❌ 失效的条目 → ② cn_eligible 为 'check'（需核实）→ ③ verified 日期最旧的条目。
研究员 k 负责自己的 worker-k.yml，以及主文件 _data/sources.yml 中序号 index % n == k-1 的条目。
"""
from __future__ import annotations

import argparse
import json
import zlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import EXTRA_DIR, MAIN  # noqa: E402

FIELDS = ["id", "name", "url", "category", "levels", "regions", "funding", "cn_eligible", "coverage", "stipend", "deadline",
          "deadline_note", "status", "requirements", "notes", "verified"]


def owned(k: int, n: int) -> list[dict]:
    main = yaml.safe_load(MAIN.read_text(encoding="utf-8"))["sources"]
    mine = [s for i, s in enumerate(main) if i % n == k - 1]
    extra = EXTRA_DIR / f"worker-{k}.yml"
    if extra.exists():
        mine += yaml.safe_load(extra.read_text(encoding="utf-8")) or []
    return mine


def all_sources(k: int, n: int) -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from catalog import load_sources

    # 按 id 的哈希分片：条目被新增/删除后分片归属不变（按序号分片会随库的增减漂移，导致已完成的核实员留下尾巴）
    return [s for s in load_sources() if zlib.crc32(s["id"].encode()) % n == k - 1]


def dead_ids() -> dict[str, str]:
    report = ROOT / "reports" / "source-health.md"
    dead = {} if not report.exists() else {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"\| `([^`]+)`[^|]*\| ❌ \| ([^|]*)\|", report.read_text(encoding="utf-8"))}
    access = ROOT / "reports" / "access.json"  # 每日可访问性检查（access_report.py）的结果更新，以它为准
    if access.exists():
        for sid, v in (json.loads(access.read_text(encoding="utf-8")).get("sources") or {}).items():
            if v.get("status") == "dead":
                dead[sid] = v.get("detail", "")
            else:
                dead.pop(sid, None)
    full = ROOT / "reports" / "access-all.csv"  # 全部信源的检查（access_report.py --all），补上未逐页核对的条目
    if full.exists():
        import csv
        with full.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r["能否打开"] == "失效":
                    dead.setdefault(r["id"], r["详情"])
    return dead


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", type=int, required=True)
    ap.add_argument("--of", type=int, default=3)
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--scope", choices=["owned", "all"], default="owned",
                    help="owned：研究员自己的条目；all：全部信源按序号分片（专职核实员用）")
    ap.add_argument("--before", help="只取 verified 早于该日期（YYYY-MM-DD）的条目，用于完成一遍全量核实")
    ap.add_argument("--need-fields", action="store_true",
                    help="与 --before 合用：已核实但还没有 coverage 字段的条目也排进队列")
    ap.add_argument("--chunks", type=int, default=1, help="把队列分成几份（每个子代理一份）")
    ap.add_argument("--out", help="与 --chunks 合用：写入 <out>-1.yml … 而不是打印")
    args = ap.parse_args()
    dead = dead_ids()

    def priority(s):
        missing = not s.get("coverage")
        return (0 if s["id"] in dead else 1 if s.get("cn_eligible") == "check" else 2 if missing else 3,
                str(s.get("verified") or ""))

    pool = all_sources(args.worker, args.of) if args.scope == "all" else owned(args.worker, args.of)
    if args.before:
        sprint = ROOT / "research" / "verify-sprint.txt"  # 冲刺开始日：当天已核实的条目不再排队，否则队列永远清不空
        if sprint.exists():
            args.before = min(args.before, sprint.read_text().strip())
        pool = [s for s in pool if str(s.get("verified") or "") < args.before
                or (args.need_fields and not s.get("coverage"))]
    queue = sorted(pool, key=priority)[: args.n]
    out = []
    for s in queue:
        item = {k: s.get(k) for k in FIELDS if s.get(k) not in (None, "", [])}
        if s["id"] in dead:
            item["link_status"] = f"失效：{dead[s['id']]}"
        out.append(item)
    if args.out:
        size = -(-len(out) // max(args.chunks, 1)) or 1
        for i in range(0, len(out), size):
            Path(f"{args.out}-{i // size + 1}.yml").write_text(
                yaml.safe_dump(out[i:i + size], allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
        print(f"待核实：本分片剩余 {len(pool)} 条，本轮取 {len(out)} 条，分成 {-(-len(out) // size) if out else 0} 份")
    else:
        print(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=200))
    return 0


if __name__ == "__main__":
    sys.exit(main())
