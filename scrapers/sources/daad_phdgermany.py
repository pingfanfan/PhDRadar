"""DAAD PhDGermany：德国面向国际生的博士岗位库。"""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from ..common import Fetcher, Job, clean_text, parse_date

SOURCE_ID = "daad-phdgermany"
BASE = "https://www.daad.de"
LIST_URL = BASE + "/en/studying-in-germany/phd-studies-research/phd-germany/?phd-p={page}"
DETAIL_RE = re.compile(r"/phd-germany/detail/[^\s\"'?]+-(\d{3,7})/")
STOP = {"type of promotion", "application deadline", "working language", "beginning", "required degree", "location", "more"}


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    jobs: dict[str, Job] = {}
    for page in range(1, 11):
        soup = BeautifulSoup(f.get(LIST_URL.format(page=page)).text, "html.parser")
        new = 0
        for a in soup.find_all("a", href=DETAIL_RE):
            jid = DETAIL_RE.search(a["href"]).group(1)
            if jid in jobs:
                continue
            card = a.find_parent("article") or a.parent.parent
            parts = [p.strip() for p in card.get_text("|", strip=True).split("|") if p.strip()]
            title = next((p for p in parts[2:] if p.lower().rstrip(":") not in STOP), a.get_text(" ", strip=True))
            text = " | ".join(parts)
            dl = re.search(r"Application deadline\s*:?\s*\|?\s*([^|]+)", text, re.I)
            loc = re.search(r"Location\s*:?\s*\|\s*([^|]+)", text, re.I)
            href = a["href"].split("?")[0]
            jobs[jid] = Job(
                source=SOURCE_ID,
                id=f"{SOURCE_ID}:{jid}",
                title=title,
                url=href if href.startswith("http") else BASE + href,
                institution=parts[0] if parts else "",
                country="DE",
                city=loc.group(1).strip() if loc else "",
                deadline=parse_date(dl.group(1)) if dl else None,
                summary=clean_text(text),
            )
            new += 1
        if not new or len(jobs) >= limit * 3:
            break
    return list(jobs.values())
