"""AcademicTransfer：荷兰学术招聘平台。读站点地图筛出博士/博后岗，再读详情页 JSON-LD。"""
from __future__ import annotations

import json
import re

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

SOURCE_ID = "academictransfer"
SITEMAP = "https://www.academictransfer.com/sitemap-vacancies.xml"
LOC_RE = re.compile(r"<loc>([^<]+/jobs/(\d+)/[^<]+?)</loc>")
PHD_SLUG = re.compile(r"(phd|doctoral|promovend|doctorate|postdoc|post-doc|postdoctoral)", re.I)
LD_RE = re.compile(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def find_job_posting(node):
    if isinstance(node, dict):
        if node.get("@type") == "JobPosting":
            return node
        node = list(node.values())
    if isinstance(node, list):
        for v in node:
            hit = find_job_posting(v)
            if hit:
                return hit
    return None


def parse_detail(html: str) -> dict | None:
    for block in LD_RE.findall(html):
        try:
            hit = find_job_posting(json.loads(block))
        except json.JSONDecodeError:
            continue
        if hit:
            return hit
    return None


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    urls = [(u, jid) for u, jid in LOC_RE.findall(f.get(SITEMAP).text) if PHD_SLUG.search(u.rsplit("/", 1)[-1] or u)]
    if keywords:  # 先用 URL slug 粗筛，减少详情页请求
        slugged = [(u, j) for u, j in urls if any(k.lower().replace(" ", "-") in u.lower() for k in keywords)]
        urls = slugged or urls
    jobs = []
    for url, jid in urls[: limit * 2]:
        posting = parse_detail(f.get(url).text) or {}
        org = posting.get("hiringOrganization") or {}
        loc = posting.get("jobLocation") or {}
        loc = loc[0] if isinstance(loc, list) and loc else loc
        jobs.append(Job(
            source=SOURCE_ID,
            id=f"{SOURCE_ID}:{jid}",
            title=clean_text(posting.get("title") or url.rsplit("/", 1)[-1].replace("-", " "), 300),
            url=url,
            institution=org.get("name", "") if isinstance(org, dict) else "",
            country="NL",
            city=((loc.get("address") or {}).get("addressLocality", "") if isinstance(loc, dict) else ""),
            posted=parse_date(posting.get("datePosted")),
            deadline=parse_date(posting.get("validThrough")),
            summary=clean_text(posting.get("description")),
            level=posting_level(posting.get("title") or url.rsplit("/", 1)[-1].replace("-", " ")) or "phd",
        ))
    return jobs
