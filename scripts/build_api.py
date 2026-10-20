#!/usr/bin/env python3
"""生成给 AI agent / 程序读取的静态 JSON 接口（随网站一起发布在 GitHub Pages 上，无需服务器）。

由 build_site.py 在写完 assets/catalog.json 与订阅源之后调用，也可单独运行：

    python scripts/build_api.py

写入（字段名用完整英文单词，不用首页的缩写；说明见 docs/agents.md）：
    api/v1/index.json           接口目录：版本、生成日期、条数、各端点、使用规则
    api/v1/opportunities.json   现在可申请的机会（与首页“现在可申请”同一份）
    api/v1/sources.json         逐页核对过官网的信源（项目页、奖学金、招聘平台等）
    api/v1/schema.json          以上两类记录的 JSON Schema
    api/openapi.json            OpenAPI 3.1 描述（可直接导入为 agent 的工具）
    llms.txt                    给大模型读的站点说明（https://llmstxt.org 约定）
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from build_sources import DISCIPLINE_NAMES, REGION_NAMES  # noqa: E402

SITE = "https://pingfanfan.github.io/PhDRadar/"
REPO = "https://github.com/pingfanfan/PhDRadar"
VERSION = "1.0"
REQ_FIELDS = {"dg": "degree", "lg": "language", "sd": "start_date", "du": "duration", "dc": "documents",
              "av": "how_to_apply", "sv": "supervisor", "na": "nationality_restriction"}
RULES = [
    "Every opportunity was checked against its official page; evidence_quote is the sentence seen there. Cite it, and send users to url to confirm before applying.",
    "Do not infer eligibility: cn_eligible 'check' means the official page does not say whether applicants from mainland China can apply.",
    "Deadlines are as stated on the official page; time zones are not normalised. Items disappear from opportunities.json after their deadline.",
    "Agents may draft materials, but the applicant reviews and submits every application personally. No automated mass submission.",
    "Data licence: CC BY 4.0. Attribute PhDRadar and link to the official page.",
]


def clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in (None, "", [], {})}


def opportunity(r: dict, seen: dict[str, str]) -> dict:
    o = r.get("o") or {}
    req = {REQ_FIELDS[k]: {"summary_zh": v[0], "quote": v[1]} for k, v in (r.get("af") or {}).items() if k in REQ_FIELDS}
    return clean({
        "id": r["id"], "kind": "posting" if r.get("via") else "programme", "title": r["n"], "organization": r.get("org"),
        "url": r["u"], "detail_url": f"{SITE}#{r['id']}",
        "regions": r.get("r"), "region_names_zh": [REGION_NAMES.get(c, c) for c in r.get("r") or []],
        "levels": r.get("l"), "disciplines": [d for d in r.get("d") or [] if d != "all"],
        "funding_coverage": r.get("c"), "amount": r.get("s"),
        "deadline": o.get("dl") or r.get("dl"), "status": o.get("st") or r.get("st"), "opens": o.get("op"),
        "cn_eligible": r.get("e") or "check", "evidence_quote": o.get("q") or r.get("pq"),
        "checked": o.get("ck") or r.get("vd"), "first_seen": seen.get(r["id"]),
        "intro_zh": r.get("in"), "requirements": req, "notes_zh": r.get("rq"), "deadline_note_zh": r.get("dn"),
        "language_tag": r.get("lt"), "flags": r.get("fl"), "platform": r.get("via"), "also_posted_at": r.get("al"),
    })


def source(r: dict) -> dict:
    return clean({
        "id": r["id"], "name_zh": r["n"], "url": r["u"], "detail_url": f"{SITE}#{r['id']}",
        "regions": r.get("r"), "levels": r.get("l"), "disciplines": [d for d in r.get("d") or [] if d != "all"],
        "funding_coverage": r.get("c"), "amount": r.get("s"), "deadline": r.get("dl"), "status": r.get("st"),
        "deadline_note_zh": r.get("dn"), "cn_eligible": r.get("e") or "check", "requirements_zh": r.get("rq"),
        "evidence_quote": r.get("pq"), "checked": r.get("vd"), "intro_zh": r.get("in"), "open_now": bool(r.get("o")),
    })


ENUMS = {
    "levels": ["phd", "postdoc"],
    "funding_coverage": ["full", "salary", "partial", "tuition", "stipend", "varies", "none", "unknown"],
    "cn_eligible": ["yes", "partial", "check", "no"],
    "status": ["open", "upcoming", "closed", "rolling", "ongoing"],
}


def schema() -> dict:
    s = lambda **kw: {"type": "string", **kw}  # noqa: E731
    arr = lambda item: {"type": "array", "items": item}  # noqa: E731
    quoted = {"type": "object", "properties": {"summary_zh": s(), "quote": s(description="Original sentence from the posting")}}
    common = {
        "id": s(description="Stable identifier"), "url": s(format="uri", description="Official page — the source of truth"),
        "detail_url": s(format="uri", description="This item on the PhDRadar site"),
        "regions": arr(s(description="Country/region code, e.g. UK, DE, US, HK")),
        "levels": arr(s(enum=ENUMS["levels"])), "disciplines": arr(s(enum=sorted(set(DISCIPLINE_NAMES) - {"all"}))),
        "funding_coverage": s(enum=ENUMS["funding_coverage"]), "amount": s(description="Amount as written on the official page"),
        "deadline": s(description="YYYY-MM-DD, or rolling / varies / unknown"), "status": s(enum=ENUMS["status"]),
        "cn_eligible": s(enum=ENUMS["cn_eligible"], description="Can applicants from mainland China apply, per the official page; check = not stated"),
        "evidence_quote": s(description="Sentence seen on the official page when it was checked"),
        "checked": s(format="date", description="Date the official page was last checked"), "intro_zh": s(description="Short summary in Chinese"),
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{SITE}api/v1/schema.json",
        "$defs": {
            "Opportunity": {"type": "object", "required": ["id", "kind", "title", "url", "cn_eligible"], "properties": {
                **common, "kind": s(enum=["posting", "programme"]), "title": s(), "organization": s(),
                "region_names_zh": arr(s()), "opens": s(), "first_seen": s(format="date"),
                "requirements": {"type": "object", "properties": {k: quoted for k in REQ_FIELDS.values()}},
                "notes_zh": s(), "deadline_note_zh": s(), "language_tag": s(),
                "flags": arr(s(description="security-screening = posting mentions export control / ATAS / research security")),
                "platform": s(description="Job board the posting came from"), "also_posted_at": arr(s(format="uri"))}},
            "Source": {"type": "object", "required": ["id", "name_zh", "url", "cn_eligible"], "properties": {
                **common, "name_zh": s(), "deadline_note_zh": s(), "requirements_zh": s(), "open_now": {"type": "boolean"}}},
        },
    }


def openapi(counts: dict) -> dict:
    def get(summary: str, ref: str, key: str) -> dict:
        return {"get": {"operationId": key, "summary": summary, "responses": {"200": {"description": "OK", "content": {"application/json": {
            "schema": {"type": "object", "properties": {"generated": {"type": "string"}, "count": {"type": "integer"},
                                                        "items": {"type": "array", "items": {"$ref": f"{SITE}api/v1/schema.json#/$defs/{ref}"}}}}}}}}}}
    return {
        "openapi": "3.1.0",
        "info": {"title": "PhDRadar API", "version": VERSION, "license": {"name": "CC BY 4.0 (data)", "identifier": "CC-BY-4.0"},
                 "description": "Funded PhD and postdoc opportunities for students from mainland China, each checked against its official page. "
                                "Static JSON files regenerated daily; read-only; no authentication. " + " ".join(RULES)},
        "servers": [{"url": SITE.rstrip("/")}],
        "paths": {
            "/api/v1/index.json": {"get": {"operationId": "getIndex", "summary": "API directory, counts and usage rules",
                                           "responses": {"200": {"description": "OK"}}}},
            "/api/v1/opportunities.json": get(f"Opportunities open now ({counts['opportunities']})", "Opportunity", "listOpportunities"),
            "/api/v1/sources.json": get(f"Verified sources ({counts['sources']})", "Source", "listSources"),
        },
    }


def llms_txt(counts: dict, today: str) -> str:
    return f"""# PhDRadar

> Funded PhD and postdoc opportunities abroad, curated for students from mainland China. Every item was checked against its official page and carries the sentence seen there; items are removed after their deadline. Updated daily (last: {today}).

Read the JSON files below rather than scraping the HTML page. All endpoints are static, read-only and need no key.

## Data
- [API directory]({SITE}api/v1/index.json): counts, endpoints, field notes and usage rules
- [Opportunities open now]({SITE}api/v1/opportunities.json): {counts['opportunities']} items — postings and programmes with deadline, funding, eligibility for mainland Chinese applicants, evidence quote, and requirement fields quoted from the posting
- [Verified sources]({SITE}api/v1/sources.json): {counts['sources']} scholarship schemes, doctoral programmes and job boards
- [JSON Schema]({SITE}api/v1/schema.json) and [OpenAPI]({SITE}api/openapi.json)
- [RSS feeds]({SITE}feeds/): new opportunities by discipline and region

## Rules for agents
""" + "\n".join(f"- {r}" for r in RULES) + f"""

## Docs
- [Field reference and agent guide (Chinese)]({REPO}/blob/main/docs/agents.md)
- [Applicant workflow: /setup, /rank, /apply, /track]({REPO}/blob/main/docs/roadmap.md)
"""


def write_api(rows: list[dict], root: Path = ROOT, today: str | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date().isoformat()
    seen_file = root / "assets" / "first-seen.json"
    seen = json.loads(seen_file.read_text(encoding="utf-8")) if seen_file.exists() else {}
    opps = [opportunity(r, seen) for r in rows if r.get("o") and r.get("e") != "no"]
    opps.sort(key=lambda x: (x.get("deadline") or "~", x["id"]))
    srcs = [source(r) for r in rows if r.get("v") and not r.get("via")]
    srcs.sort(key=lambda x: x["id"])
    counts = {"opportunities": len(opps), "sources": len(srcs)}
    out = root / "api" / "v1"
    out.mkdir(parents=True, exist_ok=True)

    def dump(path: Path, data, compact: bool = True) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":") if compact else None,
                                   indent=None if compact else 1) + "\n", encoding="utf-8")

    dump(out / "opportunities.json", {"generated": today, "count": len(opps), "items": opps})
    dump(out / "sources.json", {"generated": today, "count": len(srcs), "items": srcs})
    dump(out / "schema.json", schema(), compact=False)
    dump(out / "index.json", {
        "name": "PhDRadar API", "version": VERSION, "generated": today, "site": SITE, "counts": counts,
        "endpoints": {"opportunities": f"{SITE}api/v1/opportunities.json", "sources": f"{SITE}api/v1/sources.json",
                      "schema": f"{SITE}api/v1/schema.json", "openapi": f"{SITE}api/openapi.json", "feeds": f"{SITE}feeds/"},
        "enums": ENUMS, "region_names_zh": REGION_NAMES, "discipline_names_zh": DISCIPLINE_NAMES,
        "rules": RULES, "docs": f"{REPO}/blob/main/docs/agents.md", "license": "CC BY 4.0",
    }, compact=False)
    dump(root / "api" / "openapi.json", openapi(counts), compact=False)
    (root / "llms.txt").write_text(llms_txt(counts, today), encoding="utf-8")
    return counts


def main() -> int:
    rows = json.loads((ROOT / "assets" / "catalog.json").read_text(encoding="utf-8"))
    print(f"接口：{write_api(rows)} → api/、llms.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
