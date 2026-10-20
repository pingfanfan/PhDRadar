#!/usr/bin/env python3
"""生成 GitHub Pages 首页：可搜索、可筛选的信源查询页（默认只显示核实员确认“现在可申请”的条目）。

    python scripts/build_site.py

写入：
    index.html            首页（静态 HTML，模板见 scripts/site_template.html）
    assets/catalog.json   首页加载的精简数据（全部信源，已核对条目带官网原句）
    assets/rank-rules.json “为我推荐”的排序规则（来自 scripts/rank_rules.py，浏览器端 assets/rank.js 使用）
    feeds/                RSS 订阅源与订阅说明页（scripts/build_feeds.py）
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
    r = {"id": s["id"], "n": s["name"], "u": s["url"], "r": s.get("regions") or [], "d": s.get("disciplines") or [],
         "l": s.get("levels") or ["phd"], "c": s.get("coverage"), "s": s.get("stipend"), "dl": s.get("deadline"),
         "st": s.get("status"), "e": s.get("cn_eligible"), "v": verified}
    if verified:
        r.update({"dn": s.get("deadline_note"), "rq": s.get("requirements"), "pq": s.get("page_evidence"),
                  "vd": s.get("verified")})
    return {k: v for k, v in r.items() if v not in (None, "", [])}


# 招聘平台岗位没有学科字段：只按标题里的明确词归类，归不上就不标（不猜）
DISC_WORDS = {
    "ai": r"machine learning|deep learning|artificial intelligence|\bAI\b|neural network|computer vision|natural language|\bLLMs?\b|reinforcement learning",
    "cs": r"computer science|computing|software|cyber|informatics|data science|algorithm|distributed systems",
    "math": r"mathemati|statistic|probabilit|\bmaths?\b",
    "physics": r"physics|quantum|astro|cosmolog|optic|photonic|plasma|particle|laser",
    "chem": r"chemi|material|catalys|polymer|electrochem|batter(y|ies)",
    "bio": r"biolog|molecular|genom|genetic|protein|microb|biochem|immun|bioinformatic|(?<!fuel )\bcells?\b|\b[DR]NA\b|mitochond|vir(us|al|olog)|agricult|\bcrops?\b|\bplants?\b(?! engineering)",
    "eco": r"ecolog|evolution|biodiversit",
    "neuro": r"neuro|cognitive|brain",
    "geo": r"climate|geolog|geophys|ocean|marine|\bearth\b|environment|hydrolog|atmospher|glacio|\bsoil",
    "engineering": r"engineer|mechanical|electrical|civil|robot|aerospace|manufactur|structural",
    "social": r"sociolog|psycholog|political|politics|education|anthropolog|social",
    "humanities": r"histor|philosoph|linguist|literature|theolog|music|classics|archaeolog",
    "econ": r"econom|financ",
    "business": r"business|management|marketing|accounting",
    "med": r"medic|clinic|health|cancer|epidemiolog|pharma|surgery|nursing|disease|patholog|cardio|oncolog",
}


def disciplines_of(title: str) -> list[str]:
    import re

    return [k for k, w in DISC_WORDS.items() if re.search(w, title, re.I)]


# 申请须知字段（_data/posting_fields.yml，enrich_postings.py 校验过原句）→ 首页的短键
FIELD_KEYS = {"degree": "dg", "language": "lg", "start": "sd", "duration": "du", "documents": "dc", "apply_via": "av",
              "supervisor": "sv", "nationality": "na"}
LANG_NAMES = "英语|德语|法语|荷兰语|瑞典语|挪威语|丹麦语|芬兰语|西班牙语|意大利语|葡萄牙语|日语|韩语|冰岛语"


def lang_tag(value: str) -> str:
    """卡片上的语言标签：写了考试分数就显示分数，否则显示提到的语言。"""
    import re

    tests = re.findall(r"(?:IELTS|TOEFL(?: iBT)?|PTE)\s*(?:\([^)]*\)\s*)?\d+(?:\.\d)?", value)
    cefr = [f"{lang} {lv}" for lang, lv in re.findall(rf"({LANG_NAMES})[^；;，,。]{{0,15}}?(?<![A-Za-z])([ABC][12])(?![0-9])", value)]
    tags = list(dict.fromkeys(re.sub(r"\s+", " ", t) for t in tests + cefr))
    if tags:
        return " / ".join(tags[:2])
    return "、".join(list(dict.fromkeys(re.findall(LANG_NAMES, value)))[:2])


def posting_fields() -> dict:
    path = ROOT / "_data" / "posting_fields.yml"
    if not path.exists():
        return {}
    import yaml

    out = {}
    for pid, rec in (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).items():
        af = {short: [rec[k]["value"], rec[k]["quote"]] for k, short in FIELD_KEYS.items() if isinstance(rec.get(k), dict)}
        if af:
            out[pid] = af
    return out


def posting_rows() -> list[dict]:
    """招聘平台上的具体岗位（_data/postings.yml，由 collect_postings.py 采集）：截止 ≥ 今天、不限本土的才上首页。"""
    path = ROOT / "_data" / "postings.yml"
    if not path.exists():
        return []
    import yaml

    fields = posting_fields()

    today = datetime.now(timezone.utc).date().isoformat()
    out = []
    for p in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
        if p.get("cn") == "no":
            continue
        if p["deadline"] == "rolling":  # 全年招生：两周内复查过才展示
            if (datetime.fromisoformat(today) - datetime.fromisoformat(p["checked"])).days > 14:
                continue
        elif p["deadline"] < today:
            continue
        r = {"id": p["id"], "n": p["title"], "org": p.get("org"), "u": p["url"], "r": [p["country"]] if p.get("country") else [],
             "l": [p["level"]], "c": "salary" if p["level"] == "postdoc" else ("full" if p.get("funding_for") else None),
             "s": p.get("amount"), "dl": p["deadline"], "e": p.get("cn") or "check", "v": True, "via": p.get("via"),
             "o": {"st": "open", "dl": p["deadline"], "q": p.get("quote"), "ck": p.get("checked")},
             "d": disciplines_of(p["title"]), "fl": p.get("flags")}
        if p.get("also"):
            r["al"] = p["also"]
        af = fields.get(p["id"])
        if af:
            r["af"] = af
            if af.get("lg") and lang_tag(af["lg"][0]):
                r["lt"] = lang_tag(af["lg"][0])
        notes = ([f"资助对象（公告原文）：{p['funding_for']}"] if p.get("funding_for") else []) + \
            ([p["requirements"]] if p.get("requirements") else [])  # rank.py 的硬性筛选读这段文字，保留；页面上与申请须知重复的部分由模板去掉
        if notes:
            r["rq"] = "；".join(notes)
        out.append({k: v for k, v in r.items() if v not in (None, "", [])})
    return out


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
    rows += posting_rows()
    intros_file = ROOT / "_data" / "intros.yml"  # 申请者简介（apply_intros.py 校验后写入）
    if intros_file.exists():
        import yaml

        intros = yaml.safe_load(intros_file.read_text(encoding="utf-8")) or {}
        for r in rows:
            if r["id"] in intros:
                r["in"] = intros[r["id"]]
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "catalog.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    from build_feeds import write_feeds
    n_feeds = write_feeds(rows, ROOT)
    from rank_rules import rules as rank_rules
    (ROOT / "assets" / "rank-rules.json").write_text(json.dumps(rank_rules(DISC_WORDS), ensure_ascii=False, separators=(",", ":")),
                                                     encoding="utf-8")
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
    print(f"首页：现在可申请 {sum(1 for r in rows if r.get('o'))} · 已核对 {len(verified)} / 全部 {len(rows)} 条 → index.html, assets/catalog.json；订阅源 {n_feeds} 个 → feeds/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
