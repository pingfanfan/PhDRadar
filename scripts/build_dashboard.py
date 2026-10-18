#!/usr/bin/env python3
"""把 data/export/ 中的数据嵌入 dashboard/template.html，生成数据中台页面 dashboard/dist/index.html。

先运行 scripts/export_data.py 更新数据；生成的页面是单个自包含 HTML（发布为 claude.ai 私密 Artifact）。
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "data" / "export"
TEMPLATE = ROOT / "dashboard" / "template.html"
OUT = ROOT / "dashboard" / "dist" / "index.html"


def read_csv(name: str) -> list[dict]:
    path = EXPORT / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> int:
    src = json.loads((EXPORT / "sources.json").read_text(encoding="utf-8"))
    cats = [{"id": c["id"], "t": c["title"]} for c in src["categories"]]
    cat_index = {c["id"]: i for i, c in enumerate(cats)}
    sources = [[s["name"], s["url"], cat_index.get(s["category"], 0), s.get("levels") or ["phd"], s["regions"],
                s["disciplines"], s["cn_eligible"], s["notes"], s.get("coverage") or "", s.get("stipend") or "",
                s.get("deadline") or "", s.get("deadline_note") or "", s.get("status") or "", s.get("requirements") or ""]
               for s in src["sources"]]
    faculty = [[r["name"], r["homepage"], r["affiliation"], r["country"], r["channels"], r["levels"],
                int(float(r["score"] or 0)), (r["areas"] or "")[:260], r["openings"], r["first_seen"]]
               for r in read_csv("faculty.csv") if r.get("homepage")]
    jobs = [[j["title"], j["url"], j["institution"], j["country"], j["level"], j["eligibility"], j["funding"],
             j["deadline"], j["posted"], j["source"]] for j in read_csv("jobs.csv")]
    stats = json.loads((EXPORT / "stats.json").read_text(encoding="utf-8"))
    history = json.loads((EXPORT / "stats_history.json").read_text(encoding="utf-8"))
    payload = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "cats": cats,
               "sources": sources, "faculty": faculty, "jobs": jobs, "stats": stats, "history": history}
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\ufffd", " ")  # 去掉抓取页面编码损坏留下的替换字符
    html = TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", blob)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"数据中台：信源 {len(sources)} · 导师线索 {len(faculty)} · 岗位 {len(jobs)} → {OUT.relative_to(ROOT)}"
          f"（{OUT.stat().st_size // 1024} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
