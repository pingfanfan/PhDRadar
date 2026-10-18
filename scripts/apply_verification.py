#!/usr/bin/env python3
"""把核实结果写回信源数据。输入是 YAML 列表，每项：

    - id: some-source
      action: keep | update | delete
      fields: {url: ..., notes: ..., cn_eligible: 'yes', levels: [phd], funding: ..., name: ...}  # 仅 update 时
      evidence: "<核实依据：搜索结果标题 — URL>"

keep：信息无误，只把 verified 更新为今天；update：修改给出的字段并更新 verified；delete：删除该条目。
条目可以在 _data/sources.yml 或 _data/sources_extra/*.yml 中。

    python scripts/apply_verification.py research/inbox/<日期>-verify-worker-k.yml
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import COVERAGE, DEADLINE_WORDS, MAIN, STATUS, extra_files  # noqa: E402
from merge_sources import FIELDS, dump, scalar  # noqa: E402

EDITABLE = {"name", "url", "notes", "cn_eligible", "levels", "funding", "regions", "disciplines", "category",
            "coverage", "stipend", "deadline", "deadline_note", "status", "requirements", "verify_method", "page_evidence"}


def _value(v) -> str:
    return "[" + ", ".join(scalar(x) for x in v) + "]" if isinstance(v, list) else scalar(v)


def apply_main(text: str, sid: str, action: str, fields: dict, today: str, defaults: dict | None = None) -> tuple[str, bool]:
    start = text.find("\nsources:\n")  # 只在 sources 段里找，避免与分类 id 重名
    m = re.compile(rf"^  - id: {re.escape(sid)}\n(?:    .*\n)*", re.M).search(text, max(start, 0))
    if not m:
        return text, False
    block = m.group(0)
    if action == "delete":
        return text[:m.start()] + text[m.end():], True
    new = block
    for k, v in (defaults or {}).items():  # 仅在该字段尚不存在时补默认值
        if not re.search(rf"^    {k}: ", new, re.M):
            new = new.rstrip("\n") + f"\n    {k}: {_value(v)}\n"
    for k, v in {**fields, "verified": today}.items():
        line = f"    {k}: {_value(v)}"
        if re.search(rf"^    {k}: ", new, re.M):
            new = re.sub(rf"^    {k}: .*$", lambda _: line, new, count=1, flags=re.M)
        else:
            new = new.rstrip("\n") + "\n" + line + "\n"
    return text[:m.start()] + new + text[m.end():], True


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    results = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8")) or []
    today = date.today().isoformat()
    main_text = MAIN.read_text(encoding="utf-8")
    extras = {f: yaml.safe_load(f.read_text(encoding="utf-8")) or [] for f in extra_files()}
    changed_extras = set()
    stats = {"keep": 0, "update": 0, "delete": 0, "missing": 0}
    for r in results:
        sid, action = r.get("id"), r.get("action", "keep")
        fields = {k: v for k, v in (r.get("fields") or {}).items() if k in EDITABLE}
        if fields.get("cn_eligible") in (True, False):
            fields["cn_eligible"] = "yes" if fields["cn_eligible"] else "no"
        if "deadline" in fields:
            fields["deadline"] = str(fields["deadline"])
            if not (re.match(r"^\d{4}-\d{2}-\d{2}$", fields["deadline"]) or fields["deadline"] in DEADLINE_WORDS):
                fields.pop("deadline")
        for key, allowed in (("coverage", COVERAGE), ("status", STATUS)):  # 不合法的取值直接丢弃
            if key in fields and fields[key] not in allowed:
                fields.pop(key)
        defaults = {"coverage": "unknown"} if action in ("keep", "update") and "coverage" not in fields else {}
        main_text, found = apply_main(main_text, sid, action, fields if action == "update" else {}, today, defaults)
        if not found:
            for f, entries in extras.items():
                for i, e in enumerate(entries):
                    if e.get("id") == sid:
                        found = True
                        changed_extras.add(f)
                        if action == "delete":
                            entries.pop(i)
                        else:
                            for k, v in defaults.items():
                                e.setdefault(k, v)
                            e.update(fields if action == "update" else {})
                            e["verified"] = today
                        break
                if found:
                    break
        stats[action if found else "missing"] = stats.get(action if found else "missing", 0) + 1
    MAIN.write_text(main_text, encoding="utf-8")
    for f in changed_extras:
        body = "\n".join(dump(e) for e in extras[f]) + "\n" if extras[f] else ""
        f.write_text(re.sub(r"^  ", "", body, flags=re.M), encoding="utf-8")
    print(f"核实结果：保留 {stats['keep']} · 更新 {stats['update']} · 删除 {stats['delete']} · 未找到 {stats['missing']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
