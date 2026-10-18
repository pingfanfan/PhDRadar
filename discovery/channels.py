"""发现渠道。每个渠道是一个函数：run(ctx) -> None，把结果写入 ctx.faculty / ctx.sources / ctx.watch。

- faculty_watch   监控 _data/faculty.yml 中的导师主页，发现变化与招生信号
- csrankings      轮换扫描 CSRankings 中的教授主页，找“在招博士生”的表述
- bluesky         从 Bluesky 招生帖反查发帖导师及其主页
- github_lists    在 GitHub 搜索新出现的 PhD 岗位/导师招生汇总仓库
- aiopenings      读取教授自填的 AIOpenings 招生表
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import yaml

from scrapers.common import Disallowed, Fetcher

from .signals import detect, page_text
from .store import DIR, ROOT, Store, known_source_urls, norm_url


@dataclass
class Context:
    fetcher: Fetcher
    faculty: Store  # 疑似在招导师（key = 主页）
    sources: Store  # 候选信源（key = URL）
    watch: Store  # 关注导师主页的状态（key = 主页）
    budget: int = 400  # csrankings 每次扫描的主页数
    log: list[str] = field(default_factory=list)


def _fetch_text(f: Fetcher, url: str, timeout: int = 15) -> str | None:
    try:
        r = f.session.get(url, timeout=timeout)  # 主页扫描：单次请求、不重试（已在调用前检查 robots.txt）
        if r.status_code >= 400 or "html" not in r.headers.get("Content-Type", "html"):
            return None
        return page_text(r.text)[:200_000]
    except Exception:  # noqa: BLE001
        return None


def _allowed(f: Fetcher, url: str) -> bool:
    try:
        return f.allowed(url)
    except Exception:  # noqa: BLE001
        return True


# ───────────────────────── 关注列表 ─────────────────────────

def faculty_watch(ctx: Context) -> None:
    path = ROOT / "_data" / "faculty.yml"
    people = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("faculty") or [] if path.exists() else []
    changed = 0
    for p in people:
        url = p.get("openings_url") or p["homepage"]
        if not _allowed(ctx.fetcher, url):
            continue
        text = _fetch_text(ctx.fetcher, url)
        if text is None:
            ctx.watch.upsert(norm_url(url), {"name": p["name"], "url": url, "error": "unreachable"}, "faculty_watch")
            continue
        sig = detect(text)
        digest = hashlib.sha256(" ".join(sig.snippets).encode() + text[:20000].encode()).hexdigest()[:16]
        prev = ctx.watch.items.get(norm_url(url), {})
        rec = {"name": p["name"], "url": url, "hash": digest, "score": sig.score, "snippets": sig.snippets,
               "years": sig.years, "recruiting": sig.recruiting, "error": ""}
        if prev and prev.get("hash") != digest:
            rec["changed_on"] = date.today().isoformat()
            changed += 1
        ctx.watch.upsert(norm_url(url), rec, "faculty_watch")
    ctx.log.append(f"faculty_watch: 关注 {len(people)} 位导师，{changed} 个主页有变化")


# ───────────────────────── CSRankings 主页扫描 ─────────────────────────

CSR_FILES = "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv"
CSR_COUNTRIES = "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/institutions.csv"


def csrankings(ctx: Context) -> None:
    rows = list(csv.DictReader(io.StringIO(ctx.fetcher.get(CSR_FILES, timeout=60).text)))
    country = {}
    try:  # 机构 → 国家（institution,region,countryabbrv,homepage）
        for r in csv.DictReader(io.StringIO(ctx.fetcher.get(CSR_COUNTRIES, timeout=60).text)):
            country[r.get("institution", "")] = (r.get("countryabbrv") or "").upper()
    except Exception:  # noqa: BLE001
        pass
    people = {}
    for r in rows:
        hp = (r.get("homepage") or "").strip()
        if hp.startswith("http") and "scholar.google" not in hp and "dblp.org" not in hp:
            people.setdefault(norm_url(hp), (r.get("name", ""), r.get("affiliation", ""), hp))
    keys = sorted(people, key=lambda k: hashlib.md5(k.encode()).hexdigest())  # 固定的伪随机顺序
    state_path = DIR / "csrankings_cursor.json"
    cursor = json.loads(state_path.read_text())["offset"] if state_path.exists() else 0
    batch = [keys[(cursor + i) % len(keys)] for i in range(min(ctx.budget, len(keys)))]

    def scan(key):
        name, aff, hp = people[key]
        if not _allowed(ctx.fetcher, hp):
            return None
        text = _fetch_text(ctx.fetcher, hp)
        return (key, name, aff, hp, detect(text)) if text else None

    hits = 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        for res in pool.map(scan, batch):
            if not res or not res[4].recruiting:
                continue
            key, name, aff, hp, sig = res
            ctx.faculty.upsert(key, {"name": name, "affiliation": aff, "homepage": hp,
                                     "country": country.get(aff, ""),
                                     "discipline": "cs", "score": sig.score, "snippets": sig.snippets,
                                     "years": sig.years, "levels": sig.levels}, "csrankings")
            hits += 1
    DIR.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps({"offset": (cursor + len(batch)) % len(keys), "total": len(keys)}))
    ctx.log.append(f"csrankings: 扫描 {len(batch)}/{len(keys)} 个主页（进度 {cursor}→{(cursor + len(batch)) % len(keys)}），{hits} 个在招信号")


# ───────────────────────── Bluesky 招生帖 → 导师 ─────────────────────────

BSKY = "https://api.bsky.app/xrpc"
BSKY_QUERIES = ['"looking for PhD students"', '"recruiting PhD students"', '"PhD positions available"',
                '"fully funded PhD"', '"open PhD position"', '"hiring PhD students"',
                '"looking for a postdoc"', '"hiring a postdoc"', '"postdoc position available"', '"postdoctoral position"']
URL_RE = re.compile(r"https?://[^\s)>\]]+")


def bluesky(ctx: Context) -> None:
    authors: dict[str, dict] = {}
    for q in BSKY_QUERIES:
        try:
            data = ctx.fetcher.get(f"{BSKY}/app.bsky.feed.searchPosts?q={quote(q)}&sort=latest&limit=100").json()
        except Exception as e:  # noqa: BLE001
            ctx.log.append(f"bluesky: 查询 {q} 失败 {type(e).__name__}")
            continue
        for post in data.get("posts", []):
            text = (post.get("record") or {}).get("text", "")
            sig = detect(text)
            if sig.score < 3:
                continue
            a = post.get("author") or {}
            handle = a.get("handle", "")
            rkey = post.get("uri", "").rsplit("/", 1)[-1]
            entry = authors.setdefault(a.get("did", handle), {"handle": handle, "name": a.get("displayName") or handle,
                                                              "posts": [], "links": [], "score": 0})
            entry["posts"].append(f"https://bsky.app/profile/{handle}/post/{rkey}")
            entry["links"] += [u for u in URL_RE.findall(text) if "bsky.app" not in u]
            entry["score"] = max(entry["score"], sig.score)
            entry.setdefault("snippets", []).append(text[:280])
    dids = list(authors)
    for i in range(0, len(dids), 25):  # 批量读取个人简介中的主页链接
        try:
            params = "&".join(f"actors={quote(d)}" for d in dids[i:i + 25])
            for prof in ctx.fetcher.get(f"{BSKY}/app.bsky.actor.getProfiles?{params}").json().get("profiles", []):
                if prof.get("did") in authors:
                    authors[prof["did"]]["bio"] = prof.get("description", "")
                    authors[prof["did"]]["links"] += URL_RE.findall(prof.get("description", ""))
        except Exception:  # noqa: BLE001
            pass
    for a in authors.values():
        homepage = next((u for u in a["links"] if not re.search(r"(x\.com|twitter\.com|linkedin|forms\.gle|doi\.org)", u)), "")
        key = norm_url(homepage) if homepage else f"bsky:{a['handle']}"
        ctx.faculty.upsert(key, {"name": a["name"], "homepage": homepage or f"https://bsky.app/profile/{a['handle']}",
                                 "bio": a.get("bio", "")[:300], "evidence": a["posts"][:3], "score": a["score"],
                                 "snippets": a["snippets"][:2]}, "bluesky")
    ctx.log.append(f"bluesky: {len(authors)} 位发帖招生的作者")


# ───────────────────────── GitHub 上的新汇总仓库 ─────────────────────────

GH_QUERIES = ["phd positions", "phd openings", "phd recruitment", "fully funded phd", "phd opportunities",
              "faculty recruiting phd", "博士招生", "全奖博士", "phd application"]


def github_lists(ctx: Context) -> None:
    headers = {"Accept": "application/vnd.github+json"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    since = (date.today() - timedelta(days=120)).isoformat()
    known = known_source_urls()
    found = 0
    for q in GH_QUERIES:
        url = f"https://api.github.com/search/repositories?q={quote(q)}+pushed:>{since}&sort=stars&order=desc&per_page=30"
        try:
            items = ctx.fetcher.session.get(url, headers=headers, timeout=30).json().get("items", [])
        except Exception:  # noqa: BLE001
            continue
        for it in items:
            if it.get("stargazers_count", 0) < 5 or it.get("fork"):
                continue
            key = norm_url(it["html_url"])
            if key in known:
                continue
            ctx.sources.upsert(key, {"name": it["full_name"], "url": it["html_url"],
                                     "description": (it.get("description") or "")[:300],
                                     "stars": it.get("stargazers_count", 0), "pushed_at": it.get("pushed_at", "")[:10],
                                     "suggested_category": "github-resources", "query": q}, "github_lists")
            found += 1
    ctx.log.append(f"github_lists: {found} 个候选仓库（已排除信源库中已有的）")


# ───────────────────────── AIOpenings 招生表 ─────────────────────────

AIO_BASE = "https://raw.githubusercontent.com/yzhao062/AIOpenings/main/"


def aiopenings(ctx: Context) -> None:
    """读取 AIOpenings 仓库中按学校拆分的 JSON（教授自填：方向、主页、招生名额、联系方式）。"""
    index = ctx.fetcher.get(AIO_BASE + "universities_json/0_index.json", timeout=60).json()
    n = 0
    for item in index:
        path = str(item.get("file", "")).replace("\\", "/")
        try:
            rows = ctx.fetcher.get(AIO_BASE + path, timeout=60).json()
        except Exception:  # noqa: BLE001
            continue
        for row in rows if isinstance(rows, list) else []:
            hp = str(row.get("Homepage") or "").strip()
            name = str(row.get("Faculty") or "").strip()
            if not name or not hp.startswith("http"):
                continue
            ctx.faculty.upsert(norm_url(hp), {
                "name": name, "homepage": hp, "affiliation": row.get("University") or item.get("University", ""),
                "areas": str(row.get("Research Interests") or "")[:200], "openings": str(row.get("Positions") or "")[:160],
                "requirements": str(row.get("Requirements") or "")[:200], "contact": str(row.get("How to Reach out") or "")[:200],
                "season": str(row.get("Notes") or "")[:40], "discipline": "cs", "score": 6,
            }, "aiopenings")
            n += 1
    ctx.log.append(f"aiopenings: {len(index)} 所学校，{n} 位教授自填在招")


CHANNELS = {
    "faculty_watch": faculty_watch,
    "csrankings": csrankings,
    "bluesky": bluesky,
    "github_lists": github_lists,
    "aiopenings": aiopenings,
}
