#!/usr/bin/env python3
"""把“基于页面正文”的核实结论写回数据，并用程序检查每一句引文确实出现在页面正文里。

    python scripts/apply_page_verdicts.py --pages /tmp/pages/pilot --verdicts /tmp/pages/pilot/verdicts-*.yml [--dry-run]

规则：
- 抓取结局 dead（404/410/域名不存在）→ 删除该条目（链接已不存在；若有新地址需人工补，不留死链）。
- blocked / thin（403、被断开、没有正文）→ 不改，不算页面核实；条目保持“未页面核实”。
- verdict=pass 且 evidence_quote 能在正文里找到 → 写入 verify_method: page、page_evidence、字段修正。
- verdict=fail 且 fail_quote 能在正文里找到 → 删除。
- 引文对不上、或 cn_eligible 改 'yes' 却没有可验证的 eligibility_quote → 该修正按 unclear 处理，不写入。
"""
from __future__ import annotations

import argparse
import glob
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

OK_FIELDS = {"coverage", "stipend", "deadline", "deadline_note", "status", "requirements", "notes", "cn_eligible", "levels"}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower().replace("’", "'").replace("“", '"').replace("”", '"')


def in_text(quote: str, text_norm: str) -> bool:
    q = norm(quote).strip(" .…\"'")
    return len(q) >= 12 and q in text_norm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True)
    ap.add_argument("--verdicts", nargs="+", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delete", nargs="*", default=[], help="人工复核后批准删除的 id；其余删除建议只写入 review.yml，不自动执行")
    args = ap.parse_args()

    pages = Path(args.pages)
    index = yaml.safe_load((pages / "index.yml").read_text(encoding="utf-8"))
    texts: dict[str, str] = {}
    for b in sorted(pages.glob("bundle-*.yml")):
        for row in yaml.safe_load(b.read_text(encoding="utf-8")) or []:
            texts[row["fetch"]["id"]] = norm(row["fetch"]["text"])

    out, stats = [], {"pass": 0, "fail": 0, "dead": 0, "unclear": 0, "quote_mismatch": 0, "blocked": 0}
    for sid, v in index.items():
        if v["outcome"] == "dead":
            out.append({"id": sid, "action": "delete", "evidence": f"页面打不开（{v.get('error')}）"})
            stats["dead"] += 1
        elif v["outcome"] in ("blocked", "thin"):
            stats["blocked"] += 1

    verdicts = []
    for pattern in args.verdicts:
        for f in glob.glob(pattern):
            verdicts += yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []
    seen = set()
    for r in verdicts:
        sid = r.get("id")
        if sid in seen or sid not in texts:
            continue
        seen.add(sid)
        text = texts[sid]
        verdict = r.get("verdict")
        if verdict == "pass":
            if not in_text(r.get("evidence_quote", ""), text):
                stats["quote_mismatch"] += 1
                continue
            fields = {k: v for k, v in (r.get("fields") or {}).items() if k in OK_FIELDS}
            if fields.get("cn_eligible") == "yes" and not in_text(r.get("eligibility_quote", ""), text):
                fields.pop("cn_eligible")
            if fields.get("cn_eligible") == "no" and not in_text(r.get("eligibility_quote", ""), text):
                fields.pop("cn_eligible")
            fields["verify_method"] = "page"
            fields["page_evidence"] = " ".join(str(r["evidence_quote"]).split())[:200]
            out.append({"id": sid, "action": "update", "fields": fields, "evidence": "页面正文：" + fields["page_evidence"]})
            stats["pass"] += 1
        elif verdict == "fail":
            if not in_text(r.get("fail_quote", ""), text):
                stats["quote_mismatch"] += 1
                continue
            out.append({"id": sid, "action": "delete", "evidence": "页面正文：" + " ".join(str(r["fail_quote"]).split())[:200]})
            stats["fail"] += 1
        else:
            stats["unclear"] += 1

    review = [r for r in out if r["action"] == "delete" and r["id"] not in args.delete]
    out = [r for r in out if not (r["action"] == "delete" and r["id"] not in args.delete)]
    (pages / "review.yml").write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False), encoding="utf-8")
    res = pages / "apply.yml"
    res.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(stats, f"→ {res}")
    if not args.dry_run and out:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "apply_verification.py"), str(res)], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
