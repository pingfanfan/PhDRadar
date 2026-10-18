"""jobs.ac.uk：英国高校招聘平台的 PhD 分类。"""
from __future__ import annotations

import re
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

SOURCE_ID = "jobs-ac-uk"
BASE = "https://www.jobs.ac.uk"
LIST_URLS = [  # (列表地址, 默认层级)
    (BASE + "/search/?jobTypeFacet%5B%5D=phds&pageSize=25&startIndex={start}{kw}", "phd"),
    (BASE + "/search/?jobTypeFacet%5B%5D=research-related&keywords=postdoc{kw2}&pageSize=25&startIndex={start}", "postdoc"),
]
JOB_HREF = re.compile(r"^/job/([A-Z0-9]+)/")


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    kw = f"&keywords={quote_plus(' '.join(keywords))}" if len(keywords) == 1 else ""
    kw2 = f"+{quote_plus(' '.join(keywords))}" if len(keywords) == 1 else ""
    jobs: dict[str, Job] = {}
    for url_tpl, default_level in LIST_URLS:
        _fetch_list(f, url_tpl, default_level, kw, kw2, jobs, limit)
    return list(jobs.values())


def _fetch_list(f: Fetcher, url_tpl: str, default_level: str, kw: str, kw2: str, jobs: dict, limit: int) -> None:
    start_count = len(jobs)
    for page in range(10):
        soup = BeautifulSoup(f.get(url_tpl.format(start=1 + 25 * page, kw=kw, kw2=kw2)).text, "html.parser")
        new = 0
        for a in soup.find_all("a", href=JOB_HREF):
            jid = JOB_HREF.match(a["href"]).group(1)
            if jid in jobs:
                continue
            card = a.find_parent("div", class_=re.compile(r"j-search-result__text")) or a.parent
            text = card.get_text(" ", strip=True)
            emp = card.find("div", class_=re.compile(r"j-search-result__employer"))
            level = posting_level(a.get_text(" ", strip=True), text) or default_level
            if default_level == "postdoc" and level != "postdoc":
                continue
            placed = re.search(r"Date\s+Placed:\s*(\d{1,2}\s+[A-Za-z]{3,9}(?:\s+\d{4})?)", text)
            jobs[jid] = Job(
                source=SOURCE_ID,
                id=f"{SOURCE_ID}:{jid}",
                title=a.get_text(" ", strip=True),
                url=BASE + a["href"].split("?")[0],
                institution=emp.get_text(" ", strip=True) if emp else "",
                country="GB",
                posted=parse_date(placed.group(1)) if placed and re.search(r"\d{4}", placed.group(1)) else None,
                summary=clean_text(text),
                level=level,
            )
            new += 1
        if not new or len(jobs) - start_count >= limit * 3:
            break
