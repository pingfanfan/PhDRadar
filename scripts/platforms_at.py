"""奥地利平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

Universität Innsbruck 招聘门户（lfuonline.uibk.ac.at/public/karriereportal）：学校自建、服务器渲染；
  robots.txt 只允许 /public/karriereportal*（我们只读这部分）。只收标题写明 “Dissertationsstelle”（博士职位）或 “Postdoc” 的岗位；
  截止日期取 “Wir freuen uns auf Ihre Onlinebewerbung bis 19.10.2026”，薪资取 “brutto € 1.888 / Monat (14 mal)”。
"""
from __future__ import annotations

import re

import collect_postings as cp
from collect_postings import Fetcher, page_text

UIBK = "https://lfuonline.uibk.ac.at/public/"
UIBK_LIST = UIBK + "karriereportal.home?rubrik_in=PSP"  # 加 &lang=en 会返回空表
UIBK_DEADLINE = re.compile(r"(?:Online)?[Bb]ewerbung\s+bis\s+(?:zum\s+)?(\d{1,2})\.(\d{1,2})\.(\d{4})")


def uibk_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    ids = dict.fromkeys(re.findall(r"karriereportal\.details\?asg_id_in=(\d+)", f.get(UIBK_LIST).text))
    return [(i, f"{UIBK}karriereportal.details?asg_id_in={i}") for i in ids]


def uibk_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    raw = raw.replace("\x96", "–")  # 页面按 ISO-8859-1 声明，实为 Windows-1252 的破折号
    h = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"\s+", " ", page_text(h.group(1))).strip() if h else ""
    if re.search(r"post-?doc", title, re.I):
        level = "postdoc"
    elif re.search(r"dissertation|doktorand|prae-?doc|pre-?doc", title, re.I):
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
    pay = re.search(r"(?:mindestens\s+)?brutto\s+€\s?[\d.,]+\s*/\s*Monat(?:\s*\(14\s*mal\))?", text)
    unit = re.search(r"Organisationseinheit:\s*(.{2,120}?)(?:,\s*Standort|\s+Beschäftigungsausmaß:)", text)
    return {
        "id": f"uibk:{jid}", "title": title[:200], "url": url,
        "org": ("Universität Innsbruck – " + unit.group(1) if unit else "Universität Innsbruck")[:120],
        "country": "AT", "place": "Innsbruck", "level": level, "deadline": deadline, "quote": m.group(0),
        "funding_for": "", "amount": (pay.group(0) if pay else "")[:200], "cn": cp.cn_of(text), "flags": cp.flags_of(text),
        "via": "Universität Innsbruck",
    }, "收录"


ADAPTERS = {"uibk": (uibk_urls, uibk_detail)}
VIA_RANK = {"Universität Innsbruck": 3}
