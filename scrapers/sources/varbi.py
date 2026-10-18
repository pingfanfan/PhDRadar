"""Varbi：瑞典多所大学共用的招聘系统，读取各校职位列表，筛出博士生与博后岗位。"""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from ..common import Disallowed, Fetcher, Job, parse_date, posting_level

SOURCE_ID = "varbi"
UNIVERSITIES = {  # 子域名: (学校, 城市)
    "lu": ("Lund University", "Lund"),
    "kth": ("KTH Royal Institute of Technology", "Stockholm"),
    "uu": ("Uppsala University", "Uppsala"),
    "su": ("Stockholm University", "Stockholm"),
    "ki": ("Karolinska Institutet", "Stockholm"),
    "liu": ("Linköping University", "Linköping"),
    "umu": ("Umeå University", "Umeå"),
    "gu": ("University of Gothenburg", "Gothenburg"),
}


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    jobs = []
    errors = []
    for sub, (name, city) in UNIVERSITIES.items():
        try:
            soup = BeautifulSoup(f.get(f"https://{sub}.varbi.com/en/").text, "html.parser")
        except (Disallowed, Exception) as e:  # noqa: BLE001 单个学校失败不影响其他学校
            errors.append(f"{sub}: {type(e).__name__}")
            continue
        for row in soup.find_all("tr"):
            a = row.select_one("td.pos-title a") or row.find("a", href=re.compile(r"jobID:\d+"))
            level = posting_level(a.get_text(" ", strip=True)) if a else None
            if not a or level is None:
                continue
            jid = re.search(r"jobID:(\d+)", a.get("href", ""))
            ends = row.select_one("td.pos-ends")
            town = row.select_one("td.pos-town")
            dept = row.select_one("td.pos-subcompany")
            jobs.append(Job(
                source=SOURCE_ID,
                id=f"{SOURCE_ID}:{sub}-{jid.group(1) if jid else a['href']}",
                title=a.get_text(" ", strip=True),
                url=a["href"] if a["href"].startswith("http") else f"https://{sub}.varbi.com{a['href']}",
                institution=name + (f" – {dept.get_text(' ', strip=True)}" if dept else ""),
                country="SE",
                city=town.get_text(" ", strip=True) if town else city,
                deadline=parse_date(ends.get_text(" ", strip=True)) if ends else None,
                level=level,
            ))
    if not jobs and errors:
        raise RuntimeError("; ".join(errors))
    return jobs
