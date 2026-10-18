#!/usr/bin/env python3
"""导出机器可读的数据集到 data/export/，供数据中台、表格软件和其他工具使用。

    data/export/sources.json / sources.csv     全部信源
    data/export/faculty.csv                    自动发现的在招导师线索
    data/export/jobs.csv                       最近一次抓取的岗位
    data/export/stats.json                     当前统计
    data/export/stats_history.json             每日统计历史（按日期覆盖当天记录）
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import load_catalog  # noqa: E402

OUT = ROOT / "data" / "export"
SOURCE_FIELDS = ["id", "name", "url", "category", "levels", "regions", "disciplines", "funding", "cn_eligible",
                 "access", "language", "coverage", "stipend", "deadline", "deadline_note", "status", "requirements",
                 "notes", "verified", "verify_method", "page_evidence", "feed"]


def _flat(v):
    return "; ".join(map(str, v)) if isinstance(v, list) else ("" if v is None else str(v))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:  # utf-8-sig：Excel 直接打开不乱码
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: _flat(r.get(k)) for k in fields})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    data = load_catalog()
    sources = [{**s, "levels": s.get("levels") or ["phd"]} for s in data["sources"]]
    cats = {c["id"]: c["title"] for c in data["categories"]}
    (OUT / "sources.json").write_text(json.dumps({"categories": data["categories"], "sources": sources},
                                                 ensure_ascii=False, indent=0), encoding="utf-8")
    write_csv(OUT / "sources.csv", [{**s, "category": cats.get(s["category"], s["category"])} for s in sources], SOURCE_FIELDS)

    fac_path = ROOT / "data" / "discovery" / "faculty.json"
    faculty = list(json.loads(fac_path.read_text(encoding="utf-8")).values()) if fac_path.exists() else []
    faculty.sort(key=lambda r: -r.get("score", 0))
    write_csv(OUT / "faculty.csv", faculty, ["name", "affiliation", "country", "homepage", "channels", "levels", "score",
                                             "years", "openings", "areas", "status", "first_seen", "last_seen"])

    jobs_path = ROOT / "data" / "jobs.json"
    jobs = json.loads(jobs_path.read_text(encoding="utf-8")).get("jobs", []) if jobs_path.exists() else []
    write_csv(OUT / "jobs.csv", jobs, ["level", "eligibility", "funding", "title", "institution", "country", "city",
                                       "deadline", "posted", "source", "url", "flags", "fetched_at"])

    today = datetime.now(timezone.utc).date().isoformat()
    stats = {
        "date": today,
        "sources": len(sources),
        "by_category": dict(Counter(s["category"] for s in sources)),
        "by_level": dict(Counter("both" if len(set(s["levels"])) == 2 else s["levels"][0] for s in sources)),
        "by_eligible": dict(Counter(s["cn_eligible"] for s in sources)),
        "regions": len({r for s in sources for r in s["regions"]}),
        "faculty_leads": len(faculty),
        "jobs": len(jobs),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    hist_path = OUT / "stats_history.json"
    hist = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else {}
    hist[today] = {k: stats[k] for k in ("sources", "faculty_leads", "jobs", "regions")}
    hist_path.write_text(json.dumps(dict(sorted(hist.items())), indent=1), encoding="utf-8")
    print(f"导出：信源 {len(sources)} · 导师线索 {len(faculty)} · 岗位 {len(jobs)} → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
