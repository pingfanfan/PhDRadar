#!/usr/bin/env python3
"""生成 GitHub Pages 首页：可搜索、可筛选的信源查询页（默认只显示核实员确认“现在可申请”的条目）。

    python scripts/build_site.py

写入：
    index.html            首页（静态 HTML，模板见 scripts/site_template.html）
    assets/catalog.json   首页加载的精简数据（全部信源，已核对条目带官网原句）
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import load_catalog  # noqa: E402
from build_sources import DISCIPLINE_NAMES, REGION_NAMES  # noqa: E402

REPO = "https://github.com/pingfanfan/PhDRadar"
LABELS = {
    "region": REGION_NAMES,
    "discipline": DISCIPLINE_NAMES,
    "level": {"phd": "博士", "postdoc": "博后"},
    "coverage": {"full": "全奖（学费＋生活费）", "salary": "带薪岗位", "partial": "半奖 / 部分资助", "tuition": "仅免学费",
                 "stipend": "仅生活费", "varies": "视项目而定", "none": "不提供资助", "unknown": "官网未写明"},
    "status": {"open": ["开放申请", "p-ok"], "upcoming": ["即将开放", "p-warn"], "closed": ["本轮已截止", "p-mute"],
               "rolling": ["随时可申", "p-ok"], "ongoing": ["持续更新", "p-ok"]},
    "cn": {"yes": ["中国学生可申请", "p-ok"], "partial": ["部分可申请", "p-warn"], "check": ["资格待核实", "p-warn"],
           "no": ["中国学生不可申请", "p-bad"]},
    "deadline": {"rolling": "滚动截止", "varies": "各项目不同", "unknown": "官网未写明"},
}


def row(s: dict) -> dict:
    """首页用的精简字段；未核对条目不带要求和原句，避免把未经核对的细节当成事实展示。"""
    verified = s.get("verify_method") == "page"
    r = {"n": s["name"], "u": s["url"], "r": s.get("regions") or [], "d": s.get("disciplines") or [],
         "l": s.get("levels") or ["phd"], "c": s.get("coverage"), "s": s.get("stipend"), "dl": s.get("deadline"),
         "st": s.get("status"), "e": s.get("cn_eligible"), "v": verified}
    if verified:
        r.update({"dn": s.get("deadline_note"), "rq": s.get("requirements"), "pq": s.get("page_evidence"),
                  "vd": s.get("verified")})
    return {k: v for k, v in r.items() if v not in (None, "", [])}


def main() -> int:
    from build_open import live_rows  # 延迟导入：build_open 依赖本模块的 LABELS
    data = load_catalog()
    live = {r["id"]: r for r in live_rows()}
    rows = []
    for s in data["sources"]:
        r = row(s)
        o = live.get(s["id"])
        if o and s.get("cn_eligible") != "no":
            r["o"] = {k: v for k, v in {"st": o["state"], "dl": o.get("deadline"), "op": o.get("opens"),
                                        "q": o.get("quote"), "ck": o.get("checked")}.items() if v}
        rows.append(r)
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "catalog.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    verified = [r for r in rows if r.get("v")]
    page = (ROOT / "scripts" / "site_template.html").read_text(encoding="utf-8")
    for key, val in {
        "__OPEN__": f"{sum(1 for r in rows if r.get('o')):,}",
        "__VERIFIED__": f"{len(verified):,}",
        "__VERIFIED_YES__": f"{sum(1 for r in verified if r.get('e') == 'yes'):,}",
        "__TOTAL__": f"{len(rows):,}",
        "__DATE__": datetime.now(timezone.utc).date().isoformat(),
        "__REPO__": REPO,
        "__LABELS__": json.dumps(LABELS, ensure_ascii=False),
    }.items():
        page = page.replace(key, val)
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"首页：现在可申请 {sum(1 for r in rows if r.get('o'))} · 已核对 {len(verified)} / 全部 {len(rows)} 条 → index.html, assets/catalog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
