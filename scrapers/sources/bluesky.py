"""Bluesky：搜索学者发布的博士/博后招聘帖。

默认使用 api.bsky.app 匿名搜索（2026-10 实测可用；public.api.bsky.app 会返回 403）。
如匿名接口失效，可设置环境变量 BSKY_HANDLE / BSKY_APP_PASSWORD（应用专用密码）改用登录搜索。
"""
from __future__ import annotations

import os
import re
from urllib.parse import quote

from ..common import Fetcher, Job, clean_text, parse_date, posting_level

SOURCE_ID = "bluesky-phd-position"
PUBLIC = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
AUTHED = "https://bsky.social/xrpc/app.bsky.feed.searchPosts"
RECRUIT_RE = re.compile(r"\b(hiring|recruiting|looking for|open(ing)?s?|position|apply|funded|studentship)\b", re.I)


def _token(f: Fetcher) -> str | None:
    handle, pw = os.getenv("BSKY_HANDLE"), os.getenv("BSKY_APP_PASSWORD")
    if not (handle and pw):
        return None
    r = f.session.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                       json={"identifier": handle, "password": pw}, timeout=f.timeout)
    r.raise_for_status()
    return r.json()["accessJwt"]


def fetch(f: Fetcher, *, keywords: list[str], limit: int) -> list[Job]:
    token = _token(f)
    posts = []
    for base in ('"PhD position"', '"postdoc position"'):
        query = base + (f" {keywords[0]}" if keywords else "")
        params = f"?q={quote(query)}&sort=latest&limit=100"
        try:
            if token:
                data = f.get(AUTHED + params, headers={"Authorization": f"Bearer {token}"}).json()
            else:
                data = f.get(PUBLIC + params).json()
        except Exception as e:  # noqa: BLE001
            raise RuntimeError("Bluesky 匿名搜索失败，可设置 BSKY_HANDLE 和 BSKY_APP_PASSWORD 改用登录搜索") from e
        posts += data.get("posts", [])
    jobs = []
    seen = set()
    for post in posts:
        if post.get("uri") in seen:
            continue
        seen.add(post.get("uri"))
        text = (post.get("record") or {}).get("text", "")
        if not RECRUIT_RE.search(text):
            continue
        handle = (post.get("author") or {}).get("handle", "")
        rkey = post.get("uri", "").rsplit("/", 1)[-1]
        jobs.append(Job(
            source=SOURCE_ID,
            id=f"{SOURCE_ID}:{post.get('uri')}",
            title=clean_text(text, 140),
            url=f"https://bsky.app/profile/{handle}/post/{rkey}",
            institution=(post.get("author") or {}).get("displayName", "") or handle,
            posted=parse_date((post.get("record") or {}).get("createdAt")),
            summary=clean_text(text),
            level="postdoc" if posting_level("", text) == "postdoc" or "postdoc" in text.lower() else "phd",
        ))
    return jobs
