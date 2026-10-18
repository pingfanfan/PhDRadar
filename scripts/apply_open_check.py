#!/usr/bin/env python3
"""把“现在能否申请”的核实结论写入 _data/open_now.yml，并用程序检查引文确实出现在页面正文里。

    python scripts/apply_open_check.py --pages /tmp/pages/open --verdicts '/tmp/pages/open/verdicts-*.yml' [--dry-run]

规则（宁严勿宽）：
- open：引文在正文里，且 deadline 为 rolling 或 ≥ 今天 → 列入“现在可申请”。
- upcoming：引文在正文里，且给出 opens → 列入“即将开放”。
- closed：引文在正文里 → 从清单移除，并把信源 status 改为 closed。
- note 里写了“推断 / TBC / 待定”、或人工 --exclude 的 → 不列入。
- unclear / 引文对不上 / 日期不合理 → 从清单移除（不能保证可申请就不列）。
本次核查过的 id 会整体替换旧记录；没核查到的旧记录保持不变（由 build_open.py 按截止日自动过期）。
"""
from __future__ import annotations

import argparse
import glob
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from apply_page_verdicts import in_text, norm  # noqa: E402

OPEN_FILE = ROOT / "_data" / "open_now.yml"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# 核实员自己承认年份是推断的、或页面标注“待定”的，不能算“保证可申请”
HEDGE = re.compile(r"推断|推算|推定|据此|inferr|TBC|待定|待确认|to be confirmed|tentative", re.I)


def load_open() -> dict[str, dict]:
    if not OPEN_FILE.exists():
        return {}
    return {r["id"]: r for r in yaml.safe_load(OPEN_FILE.read_text(encoding="utf-8")) or []}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True)
    ap.add_argument("--verdicts", nargs="+", required=True)
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--exclude", nargs="*", default=[], help="人工复核后不列入清单的 id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pages = Path(args.pages)
    texts: dict[str, str] = {}
    for b in sorted(pages.glob("bundle-*.yml")):
        for row in yaml.safe_load(b.read_text(encoding="utf-8")) or []:
            texts[row["fetch"]["id"]] = norm(row["fetch"]["text"])

    verdicts = []
    for pattern in args.verdicts:
        for f in sorted(glob.glob(pattern)):
            verdicts += yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []

    current = load_open()
    closed, stats = [], {"open": 0, "upcoming": 0, "closed": 0, "unclear": 0, "rejected": 0}
    seen = set()
    for r in verdicts:
        sid = r.get("id")
        if sid in seen or sid not in texts:
            continue
        seen.add(sid)
        current.pop(sid, None)
        verdict, quote = r.get("verdict"), str(r.get("quote") or "")
        if verdict in ("open", "upcoming", "closed") and not in_text(quote, texts[sid]):
            stats["rejected"] += 1
            continue
        quote = " ".join(quote.split())[:200]
        deadline, opens = str(r.get("deadline") or ""), str(r.get("opens") or "")
        if sid in args.exclude or (verdict in ("open", "upcoming") and HEDGE.search(str(r.get("note") or ""))):
            stats["rejected"] += 1
            continue
        if verdict == "open":
            if deadline != "rolling" and not (DATE.match(deadline) and deadline >= args.today):
                stats["rejected"] += 1
                continue
            current[sid] = {"id": sid, "state": "open", "deadline": deadline, "quote": quote,
                            "note": r.get("note") or "", "checked": args.today}
            stats["open"] += 1
        elif verdict == "upcoming":
            if not re.match(r"^\d{4}-\d{2}", opens):
                stats["rejected"] += 1
                continue
            row = {"id": sid, "state": "upcoming", "opens": opens, "quote": quote, "note": r.get("note") or "",
                   "checked": args.today}
            if DATE.match(deadline):
                row["deadline"] = deadline
            current[sid] = row
            stats["upcoming"] += 1
        elif verdict == "closed":
            closed.append({"id": sid, "action": "update", "fields": {"status": "closed"},
                           "evidence": "页面正文：" + quote})
            stats["closed"] += 1
        else:
            stats["unclear"] += 1

    rows = sorted(current.values(), key=lambda x: (x["state"] != "open", x.get("deadline") or "9999", x["id"]))
    print(stats, f"→ 清单共 {len(rows)} 条")
    if args.dry_run:
        return 0
    OPEN_FILE.write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    if closed:
        res = pages / "closed.yml"
        res.write_text(yaml.safe_dump(closed, allow_unicode=True, sort_keys=False), encoding="utf-8")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "apply_verification.py"), str(res)], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
