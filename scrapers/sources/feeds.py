"""通用 RSS / Atom 适配器，覆盖 Madgex 职位站（Nature Careers 等）和 WordPress 职位板。"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

ATOM = "{http://www.w3.org/2005/Atom}"


def parse_feed(xml_text: str) -> list[dict]:
    """把 RSS 2.0 或 Atom 解析成 [{title, link, summary, published, guid}]。"""
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)  # noqa: S314 公开职位 feed
    items = []
    for it in root.iter("item"):
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "summary": it.findtext("description") or "",
            "published": it.findtext("pubDate") or "",
            "guid": (it.findtext("guid") or it.findtext("link") or "").strip(),
        })
    for e in root.iter(f"{ATOM}entry"):
        link = e.find(f"{ATOM}link[@rel='alternate']")
        if link is None:
            link = e.find(f"{ATOM}link")
        items.append({
            "title": (e.findtext(f"{ATOM}title") or "").strip(),
            "link": link.get("href", "") if link is not None else "",
            "summary": e.findtext(f"{ATOM}summary") or e.findtext(f"{ATOM}content") or "",
            "published": e.findtext(f"{ATOM}published") or e.findtext(f"{ATOM}updated") or "",
            "guid": (e.findtext(f"{ATOM}id") or "").strip(),
        })
    return items


def make_feed_adapter(source_id: str, url: str, *, phd_only: bool = True, country: str = ""):  # phd_only：只收博士/博后岗
    """生成一个读取单个 feed 的 fetch 函数。url 中的 {q} 会替换为搜索词。"""

    def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
        q = "+".join((keywords[0] if keywords else "phd").split())
        resp = f.get(url.format(q=q))
        jobs = []
        for it in parse_feed(resp.content):
            level = posting_level(it["title"], clean_text(it["summary"], 3000))
            if phd_only and level is None:
                continue
            jobs.append(Job(
                source=source_id,
                id=f"{source_id}:{it['guid'] or it['link']}",
                title=clean_text(it["title"], 300),
                url=it["link"],
                country=country,
                posted=parse_date(it["published"]),
                summary=clean_text(it["summary"]),
                level=level or "phd",
            ))
            if len(jobs) >= limit:
                break
        return jobs

    fetch.__doc__ = f"RSS/Atom: {url}"
    return fetch
