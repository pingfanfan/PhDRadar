#!/usr/bin/env python3
"""把研究得到的候选信源（YAML 列表）合并进 _data/sources.yml：校验字段、按 id/URL 去重，追加到文件末尾。

    python scripts/merge_sources.py candidates.yml [more.yml ...] [--target worker-1] [--dry-run]

--target 指定写入 _data/sources_extra/<target>.yml（并行研究员各用各的文件）；不指定则追加到 _data/sources.yml。

候选条目可带 evidence（来源证据，不写入）和 feed（机器可读地址，会保留）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import COVERAGE, DEADLINE_WORDS, EXTRA_DIR, STATUS, load_catalog  # noqa: E402
from discovery.store import norm_url  # noqa: E402

DATA = ROOT / "_data" / "sources.yml"
FIELDS = ["id", "name", "url", "category", "regions", "disciplines", "funding", "levels", "cn_eligible", "access",
          "language", "coverage", "stipend", "deadline", "deadline_note", "status", "requirements", "notes", "verify_method", "page_evidence", "verified", "feed"]
REQUIRED = ["id", "name", "url", "category", "regions", "disciplines", "funding", "cn_eligible", "access", "language", "notes"]
QUOTE = {"yes", "no", "on", "off", "true", "false", "y", "n"}


def scalar(v) -> str:
    s = str(v)
    if s.lower() in QUOTE or re.search(r"^[\[\]{}&*!|>'\"%@`#-]|: | #|:$|^\s|\s$", s) or s == "":
        return "'" + s.replace("'", "''") + "'"
    return s


def dump(entry: dict) -> str:
    out = []
    for i, k in enumerate(f for f in FIELDS if entry.get(f) not in (None, "", [])):
        v = entry[k]
        val = "[" + ", ".join(scalar(x) for x in v) + "]" if isinstance(v, list) else scalar(v)
        out.append(("  - " if i == 0 else "    ") + f"{k}: {val}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--target", help="写入 _data/sources_extra/<target>.yml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-no-evidence", action="store_true", help="允许没有 evidence 的条目入库（默认拒绝：质量优先）")
    args = ap.parse_args()

    data = load_catalog()
    cats = {c["id"] for c in data["categories"]}
    ids = {s["id"] for s in data["sources"]}
    urls = {norm_url(s["url"]) for s in data["sources"]}
    added, skipped = [], []
    for f in args.files:
        for e in yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []:
            if not args.allow_no_evidence and not str(e.get("evidence") or "").strip():
                skipped.append((e.get("id"), "无 evidence（必须给出搜索结果中的标题与链接作为依据）"))
                continue
            e = {k: v for k, v in e.items() if k in FIELDS}
            e["cn_eligible"] = {True: "yes", False: "no"}.get(e.get("cn_eligible"), e.get("cn_eligible"))
            e["regions"] = ["NO" if r is False else str(r) for r in e.get("regions") or ["GLOBAL"]]
            e["verified"] = str(e.get("verified") or "2026-10")
            if e.get("deadline") is not None:
                e["deadline"] = str(e["deadline"])
            for key, allowed in (("coverage", COVERAGE), ("status", STATUS)):  # 结构化字段取值不合法就丢弃该字段，不影响入库
                if e.get(key) not in allowed:
                    e.pop(key, None)
            if e.get("deadline") and not (re.match(r"^\d{4}-\d{2}-\d{2}$", e["deadline"]) or e["deadline"] in DEADLINE_WORDS):
                e.pop("deadline")
            problems = [k for k in REQUIRED if not e.get(k)]
            if e.get("levels") and any(lv not in ("phd", "postdoc") for lv in e["levels"]):
                problems.append(f"levels={e['levels']}")
            if e.get("category") not in cats:
                problems.append(f"category={e.get('category')}")
            if not str(e.get("url", "")).startswith("https://"):
                problems.append("url 非 https")
            key = norm_url(str(e.get("url", "")))
            if problems or e.get("id") in ids or key in urls:
                skipped.append((e.get("id"), "重复" if not problems else ",".join(problems)))
                continue
            ids.add(e["id"])
            urls.add(key)
            added.append(e)
    print(f"新增 {len(added)}，跳过 {len(skipped)}")
    for sid, why in skipped:
        print(f"  跳过 {sid}: {why}")
    if added and not args.dry_run:
        if args.target:
            if not re.fullmatch(r"[a-z0-9-]+", args.target):
                ap.error("--target 只能包含小写字母、数字和连字符")
            path = EXTRA_DIR / f"{args.target}.yml"
            EXTRA_DIR.mkdir(parents=True, exist_ok=True)
            text = path.read_text(encoding="utf-8").rstrip("\n") + "\n" if path.exists() else ""
            body = "\n".join(dump(e) for e in added) + "\n"
            # extra 文件是顶层列表：去掉两格缩进
            text += re.sub(r"^  ", "", body, flags=re.M)
            path.write_text(text, encoding="utf-8")
        else:
            text = DATA.read_text(encoding="utf-8").rstrip("\n")
            text += "\n\n  # ───────────────────────── 批量研究补充（待链接核查） ─────────────────────────\n"
            text += "\n".join(dump(e) for e in added) + "\n"
            DATA.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
