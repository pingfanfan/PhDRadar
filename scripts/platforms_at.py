"""奥地利平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

Universität Innsbruck 招聘门户（lfuonline.uibk.ac.at/public/karriereportal）：学校自建、服务器渲染；
  robots.txt 只允许 /public/karriereportal*（我们只读这部分）。只收标题写明博士职位（“Dissertationsstelle” / “PhD position”）
  或 “Postdoc” 的岗位；“Senior Lecturer (Doctorate/PhD)” 是要求已有博士的教职，不算。
  2026-11 起门户默认返回英文页：截止日期写 “online application by 11.11.2026”，薪资写 “€ 1.888 per month (14 times)”，
  单位写 “Administrative unit:”；德文页仍是 “Onlinebewerbung bis 19.10.2026”“brutto € 1.888 / Monat (14 mal)”“Organisationseinheit:”，两种都认。
"""
from __future__ import annotations

import re

import collect_postings as cp
from collect_postings import Fetcher, page_text

UIBK = "https://lfuonline.uibk.ac.at/public/"
UIBK_LIST = UIBK + "karriereportal.home?rubrik_in=PSP"  # 加 &lang=en 会返回空表
UIBK_DEADLINE = re.compile(r"(?:(?:Online)?[Bb]ewerbung\s+bis\s+(?:zum\s+)?|application\s+by\s+)(\d{1,2})\.(\d{1,2})\.(\d{4})")


def uibk_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    ids = dict.fromkeys(re.findall(r"karriereportal\.details\?asg_id_in=(\d+)", f.get(UIBK_LIST).text))
    return [(i, f"{UIBK}karriereportal.details?asg_id_in={i}") for i in ids]


def uibk_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    raw = raw.replace("\x96", "–")  # 页面按 ISO-8859-1 声明，实为 Windows-1252 的破折号
    h = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"\s+", " ", page_text(h.group(1))).strip() if h else ""
    if re.search(r"post-?doc", title, re.I):
        level = "postdoc"
    elif re.search(r"lecturer|lektor", title, re.I):
        return None, "非博士/博后岗位"  # 要求已有博士的教职（标题里的 Doctorate/PhD 是资格要求）
    elif re.search(r"dissertation|doktorand|prae-?doc|pre-?doc|\bph\.?d\b", title, re.I):
        level = "phd"
    else:
        return None, "非博士/博后岗位"
    text = page_text(raw)
    m = UIBK_DEADLINE.search(text)
    if not m:
        return None, "页面无截止日期"
    deadline = f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    if deadline < today:
        return None, "已截止"
    pay = re.search(r"(?:mindestens\s+)?brutto\s+€\s?[\d.,]+\s*/\s*Monat(?:\s*\(14\s*mal\))?"
                    r"|€\s?[\d.,]+\s*per\s+month(?:\s*\(14\s*times\))?", text)
    unit = re.search(r"(?:Organisationseinheit|Administrative unit):\s*(.{2,120}?)"
                     r"(?:,\s*(?:Standort|Location)|\s+(?:Beschäftigungsausmaß|Extent of employment):)", text)
    return {
        "id": f"uibk:{jid}", "title": title[:200], "url": url,
        "org": ("Universität Innsbruck – " + unit.group(1) if unit else "Universität Innsbruck")[:120],
        "country": "AT", "place": "Innsbruck", "level": level, "deadline": deadline, "quote": m.group(0),
        "funding_for": "", "amount": (pay.group(0) if pay else "")[:200], "cn": cp.cn_of(text), "flags": cp.flags_of(text),
        "via": "Universität Innsbruck",
    }, "收录"


ADAPTERS = {"uibk": (uibk_urls, uibk_detail)}
VIA_RANK = {"Universität Innsbruck": 3}
