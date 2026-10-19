"""德国平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / HEADERS / VIA_RANK）。

联邦劳动局职位搜索（Bundesagentur für Arbeit, Jobsuche）：
  接口文档 https://jobsuche.api.bund.dev/（bundesAPI 社区整理，源码 github.com/bundesAPI/jobsuche-api）。
  文档写明所有人用同一个公开 clientId 访问：请求头 X-API-Key: jobboerse-jobsuche（不需要 OAuth 或自己的密钥）。
  搜索 /pc/v6/jobs（v4 已返回 403），详情 /pc/v4/jobdetails/{base64(参考号)}；对外链接用 arbeitsagentur.de 的岗位页。
  截止日期只从岗位描述原文里取（Bewerbungsfrist / bis zum … + 申请语境）；取不到就不收。
"""
from __future__ import annotations

import base64
import json
import re
from datetime import date, timedelta

import collect_postings as cp
from collect_postings import ANY_DATE, DE_MONTHS, MONTH3, Fetcher, _any, _SELF_FUNDED, page_text, \
    parse_day

BA = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
BA_KEY = {"X-API-Key": "jobboerse-jobsuche"}
BA_QUERIES = ["Doktorand", "PhD", "Promotion", "Postdoc", "Doctoral"]
# “Promotion” 也指市场推广：只认学位语境
BA_TITLE = re.compile(r"doktorand|promotionsstelle|(?:zur|der|mit|einer)\s+promotion|ph\.?\s?d\b|promovend|doctoral|"
                      r"post-?doc|postdoktorand", re.I)
BA_SKIP = re.compile(r"berufsbegleitend|werkstudent|praktik|abschlussarbeit|master'?s? thesis|bachelor|"
                     r"professor|lecturer|manager", re.I)
BA_PHD = re.compile(r"doktorand|promotion|ph\.?\s?d\b|promovend|(?<!post)(?<!post-)doctoral", re.I)  # “Postdoctoral” 不算
BA_POSTDOC = re.compile(r"post-?doc|postdoktorand|postdoctoral", re.I)
BA_FUNDED = re.compile(r"tv-?l\b|tvöd|\be\s?13\b|\beg\s?13\b|entgeltgruppe|salary|gehalt|vergütung|vergütet|stipend|"
                       r"bezahl|\bpaid\b|\bpay\b", re.I)
# 截止日期：明确的截止字样，或“bis zum/spätestens 日期”且前后有申请语境（排除“befristet bis zum 31.12.2029”这类合同期）
BA_KW = r"(?:bewerbungsfrist|bewerbungsschluss|einsendeschluss|application deadline|deadline(?: for applications?| is| of)?|" \
        r"closing date|apply by|applications? (?:close|due|until)|bis (?:zum|spätestens(?: zum| am)?)|spätestens (?:zum|am|bis)|\bby)"
BA_CONTEXT = re.compile(r"bewerb|application|apply|kennziffer|ausschreibungs", re.I)


def ba_day(raw: str) -> str | None:
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", raw):
        d, mo, y = raw.split(".")
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    words = raw.replace(".", " ")
    for de, en in DE_MONTHS.items():
        words = re.sub(de, en, words, flags=re.I)
    return parse_day(re.sub(r"\b([A-Za-z]{3})[a-z]*\b", lambda x: MONTH3.get(x.group(1).lower(), x.group(0)), words))


def ba_deadline(text: str, today: str) -> tuple[str | None, str]:
    """描述原文里的申请截止日期 → (ISO, 原文片段)。只认一年内的日期（更远的是合同期限，不是截止）。"""
    horizon = (date.fromisoformat(today) + timedelta(days=365)).isoformat()
    for m in re.finditer(BA_KW + r"[^.\d]{0,40}?" + ANY_DATE, text, re.I):
        kw = m.group(0).lower()
        if kw.startswith(("bis ", "spätestens")):
            if not BA_CONTEXT.search(text[max(0, m.start() - 120):m.end() + 80]):
                continue
        elif kw.startswith("by"):  # “please apply … by 01.11.2026”：前文要有申请字样
            if not re.search(r"apply|application", text[max(0, m.start() - 120):m.start()], re.I):
                continue
        iso = ba_day(m.group(1))
        if iso and iso <= horizon:
            quote = m.group(0).strip()
            if kw.startswith(("bis ", "spätestens", "by")):  # 只有“bis zum 日期”读不出是申请截止：带上同一句前面的话
                head = text[max(0, m.start() - 100):m.start()]
                head = re.split(r"(?<![\d.])[.!?]\s+|\s{2,}", head)[-1].strip()
                quote = f"{head} {quote}".strip()
            return iso, quote
    return None, ""


def ba_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for q in BA_QUERIES:
        for page in range(1, max_pages + 1):
            rows = f.get(f"{BA}/pc/v6/jobs", params={"was": q, "angebotsart": 1, "size": 100, "page": page},
                         headers=BA_KEY).json().get("ergebnisliste") or []
            for r in rows:
                ref, title = r.get("referenznummer") or "", r.get("stellenangebotsTitel") or ""
                if ref and BA_TITLE.search(title) and not BA_SKIP.search(title) and not r.get("externeUrl"):
                    seen.setdefault(ref, f"{BA}/pc/v4/jobdetails/{base64.b64encode(ref.encode()).decode()}")
            if len(rows) < 100:
                break
    return list(seen.items())


def ba_detail(ref: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    j = json.loads(raw)
    title = re.sub(r"\\([*_:])", r"\1", j.get("stellenangebotsTitel") or "").strip()
    if not BA_TITLE.search(title) or BA_SKIP.search(title):
        return None, "非博士/博后岗位"
    level = "postdoc" if BA_POSTDOC.search(title) and not BA_PHD.search(title) else "phd"  # “Doktorand/in / PostDoc” 按博士
    desc = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", j.get("stellenangebotsBeschreibung") or "")  # Markdown 链接只留文字
    text = page_text(re.sub(r"[*_#\\]+", " ", desc))
    if not text:
        return None, "页面无截止日期"
    deadline, quote = ba_deadline(text, today)
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    if _any(_SELF_FUNDED, text) or not (BA_FUNDED.search(text) or j.get("verguetungsangabe") not in (None, "KEINE_ANGABEN")):
        return None, "未写资助或自费"
    sal = re.search(r"(?:TV-?L|TVöD|Entgeltgruppe|E\s?13|EG\s?13)[^.;\n]{0,60}", text)
    if j.get("gehaltsspanneVon"):
        per = {"JAHRESGEHALT": " / Jahr", "MONATSGEHALT": " / Monat"}.get(j.get("verguetungsangabe"), "")
        per = "" if per == " / Jahr" and j["gehaltsspanneVon"] < 10000 else per  # 把月薪填成年薪的，不写周期
        amount = f"{j['gehaltsspanneVon']:,.0f}–{j.get('gehaltsspanneBis') or j['gehaltsspanneVon']:,.0f} €{per}"
    else:
        amount = sal.group(0).strip() if sal else ""
    loc = ((j.get("stellenlokationen") or [{}])[0].get("adresse") or {})
    return {
        "id": f"arbeitsagentur:{ref}", "title": re.sub(r"\s+", " ", title)[:200],
        "url": f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{ref}",
        "org": re.sub(r"\s+", " ", j.get("firma") or "")[:120], "country": "DE", "place": (loc.get("ort") or "")[:80],
        "level": level, "deadline": deadline, "quote": quote[:160], "funding_for": "", "amount": amount[:200],
        "cn": cp.cn_of(text),
        "flags": cp.flags_of(text), "via": "Bundesagentur für Arbeit",
    }, "收录"


ADAPTERS = {"arbeitsagentur": (ba_urls, ba_detail)}
HEADERS = {"arbeitsagentur": BA_KEY}
VIA_RANK = {"Bundesagentur für Arbeit": 1}  # 多是转载机构自己的招聘页：跨平台重复时让位给其他平台
