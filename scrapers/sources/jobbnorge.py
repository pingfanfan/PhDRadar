"""Jobbnorge：挪威高校职位，使用其公开 API，按标题筛出博士（stipendiat）与博后（postdoktor）岗位。"""
from __future__ import annotations

import re

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

SOURCE_ID = "jobbnorge"
LIST_URL = "https://publicapi.jobbnorge.no/v1/jobs?lang=2"


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    data = f.get(LIST_URL).json()
    items = data if isinstance(data, list) else data.get("jobs") or data.get("items") or []
    jobs = []
    for it in items:
        level = posting_level(it.get("title") or "", it.get("summary") or "")
        if level is None:
            continue
        jid = it.get("id")
        jobs.append(Job(
            source=SOURCE_ID,
            id=f"{SOURCE_ID}:{jid}",
            title=clean_text(it.get("title"), 300),
            url=it.get("link") or f"https://www.jobbnorge.no/ledige-stillinger/stilling/{jid}",
            institution=it.get("employer") or "",
            country="NO",
            city=it.get("location") or "",
            deadline=parse_date(it.get("deadline")),
            summary=clean_text(it.get("summary")),
            level=level,
        ))
    return jobs
