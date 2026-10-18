"""INSPIRE HEP Jobs：高能/理论物理职位，官方 REST API，筛选博士与博后级别的开放岗位。"""
from __future__ import annotations

from ..common import Fetcher, Job, clean_text, parse_date

SOURCE_ID = "inspire-jobs"
API = "https://inspirehep.net/api/jobs?sort=mostrecent&size=100&page=1&rank={rank}"
RANKS = {"PHD": "phd", "POSTDOC": "postdoc"}


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    jobs = []
    for rank, level in RANKS.items():
        data = f.get(API.format(rank=rank), headers={"Accept": "application/json"}).json()
        jobs += _parse(data, rank, level)
    return jobs


def _parse(data: dict, rank: str, level: str) -> list[Job]:
    jobs = []
    for hit in data.get("hits", {}).get("hits", []):
        md = hit.get("metadata", {})
        if rank not in (md.get("ranks") or []) or md.get("status", "open") != "open":
            continue
        cn = md.get("control_number") or hit.get("id")
        insts = ", ".join(i.get("value", "") for i in md.get("institutions") or [])
        jobs.append(Job(
            source=SOURCE_ID,
            id=f"{SOURCE_ID}:{cn}",
            title=clean_text(md.get("position"), 300),
            url=f"https://inspirehep.net/jobs/{cn}",
            institution=insts,
            country=", ".join(md.get("regions") or []),
            deadline=parse_date(md.get("deadline_date")),
            posted=parse_date(hit.get("created")),
            summary=clean_text(md.get("description")),
            level=level,
        ))
    return jobs
