"""EURAXESS：欧盟研究岗位库，筛选 First Stage Researcher (R1) = 博士岗。"""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

SOURCE_ID = "euraxess"
BASE = "https://euraxess.ec.europa.eu"
# 447 = R1（博士）、448 = R2（博后）。2026-10 实测服务端渲染页面会忽略该筛选，
# 因此抓取全部岗位后在本地按标题判断层级，排除教职/行政岗位。
LIST_URL = BASE + "/jobs/search?f%5B0%5D=offer_type%3Ajob_offer&page={page}"
JOB_HREF = re.compile(r"^(?:https://euraxess\.ec\.europa\.eu)?/jobs/(\d+)$")
COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Czechia", "Denmark",
    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Norway", "Poland", "Portugal",
    "Romania", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "Israel",
    "Türkiye", "Turkey", "Serbia", "China", "United States", "Canada", "Japan",
]


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    jobs: dict[str, Job] = {}
    for page in range(30):
        soup = BeautifulSoup(f.get(LIST_URL.format(page=page)).text, "html.parser")
        new = 0
        for a in soup.find_all("a", href=JOB_HREF):
            jid = JOB_HREF.match(a["href"]).group(1)
            title = a.get_text(" ", strip=True)
            if jid in jobs or not title:
                continue
            card = a.find_parent(["article", "li"]) or a.parent.parent
            text = card.get_text(" ", strip=True)
            level = posting_level(title, text) or ("phd" if "R1" in text else "postdoc" if "R2" in text else None)
            if level is None:
                jobs[jid] = None  # 教职/行政等，记录已见
                new += 1
                continue
            org = card.find("a", href=re.compile(r"/partnering/|/organisation"))
            deadline = re.search(r"Deadline\s*:?\s*([^|]{6,40}?\d{4})", text, re.I)
            posted = re.search(r"Posted\s*(?:on)?\s*:?\s*([^|]{6,30}?\d{4})", text, re.I)
            jobs[jid] = Job(
                source=SOURCE_ID,
                id=f"{SOURCE_ID}:{jid}",
                title=title,
                url=f"{BASE}/jobs/{jid}",
                institution=org.get_text(" ", strip=True) if org else "",
                country=next((c for c in COUNTRIES if re.search(rf"\b{c}\b", text)), ""),
                deadline=parse_date(deadline.group(1)) if deadline else None,
                posted=parse_date(posted.group(1)) if posted else None,
                summary=clean_text(text),
                level=level,
            )
            new += 1
        if not new or sum(1 for j in jobs.values() if j) >= limit * 3:
            break
    return [j for j in jobs.values() if j]
