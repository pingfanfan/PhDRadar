"""学科招聘板的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

- MathJobs.org（美国数学会，与 Academic Jobs Online 同一套系统）：一个 RSS 列出全部在招广告，岗位页上有 “Appl Deadline”。
  robots.txt 要求 Crawl-delay 5（Fetcher 自动遵守）。
- Texas A&M 自然资源招聘板（jobs.rwfm.tamu.edu）：生态 / 野生动物 / 林学的研究生助研与博后；岗位页有 “Application Deadline” 字段。
  无 robots.txt（404）。
- H-Net Job Guide（人文社科）：岗位页有 “Closing Date” 字段；robots.txt 要求 Crawl-delay 5，首次访问需要保存 cookie（Session 自动处理）。
"""
from __future__ import annotations

import gzip
import html as htmllib
import re

import collect_postings as cp
from collect_postings import Fetcher, _any, _FUNDED, _RESTRICTED, _SCREENING, _SELF_FUNDED, level_of, page_text, parse_day, \
    place_country

# ───────────────────────── MathJobs.org ─────────────────────────

MJ_RSS = "https://www.mathjobs.org/jobs?joblst------rss"


def mj_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    raw = f.get(MJ_RSS).content
    xml = (gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw).decode("utf-8", "replace")  # 未声明编码的 gzip 也能读
    out = []
    for item in re.findall(r"<item\b(.*?)</item>", xml, re.S):
        def tag(name: str) -> str:
            m = re.search(rf"<{name}>(.*?)</{name}>", item, re.S)
            return htmllib.unescape(m.group(1).strip()) if m else ""
        jid, title = tag("ads:ID"), tag("title")
        if not jid or not level_of(title) or not tag("ads:Deadline"):  # RSS 里没写截止的广告页面上也没有，不读
            continue
        cp._AJO["mj" + jid] = {"univ": tag("ads:Univ"), "dept": tag("ads:Dept"), "country": tag("ads:Country"),
                               "city": tag("ads:City"), "desc": tag("description")}
        out.append(("mj" + jid, f"https://www.mathjobs.org/jobs/list/{jid}"))
    return out


def mj_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    row, why = cp.ajo_detail(jid, url, raw, today)  # 页面结构与 AJO 相同
    if row:
        row.update(id=f"mathjobs:{jid[2:]}", via="MathJobs")
    return row, why


# ───────────────────────── Texas A&M Natural Resources Job Board ─────────────────────────

TAMU = "https://jobs.rwfm.tamu.edu"
TAMU_LISTS = [TAMU + "/search/?Graduate=yes&PageNum={page}", TAMU + "/search/?Faculty_PostDoc=yes&PageNum={page}"]


def tamu_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for tpl in TAMU_LISTS:
        for page in range(1, max_pages + 1):
            ids = re.findall(r"/view-job/\?id=(\d+)", f.get(tpl.format(page=page)).text)
            new = [i for i in dict.fromkeys(ids) if i not in seen]
            for i in new:
                seen[i] = f"{TAMU}/view-job/?id={i}"
            if not new:
                break
    return list(seen.items())


def tamu_field(text: str, name: str, nxt: str) -> str:
    m = re.search(rf"{name}:\s*(.*?)\s+(?:{nxt}):", text)
    return m.group(1).strip() if m else ""


def tamu_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    head = page_text((re.search(r"<title>(.*?)</title>", raw, re.S) or [None, ""])[1]).split(" | ")[0]
    title, _, org = head.partition(" at ")  # 标题形如 “PhD Positions: Fish Ecology at Purdue University”
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"Application Deadline:\s*(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if not m:
        return None, "页面无截止日期"
    deadline = f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    if deadline < today:
        return None, "已截止"
    salary = tamu_field(text, "Salary", "Education Required|Experience Required|Location")
    d = text.find(" Description ", m.end())
    body = text[d:d + 8000] if d >= 0 else ""
    if _any(_SELF_FUNDED, body) or not (re.search(r"\d", salary) or _any(_FUNDED, body)):
        return None, "未写资助或自费"
    place = tamu_field(text, "Location", "Tags")
    return {
        "id": f"tamu-rwfm:{jid}", "title": title[:200], "url": url, "org": org[:120],
        "country": place_country(place) or ("US" if re.search(r",\s*[A-Z][a-z]+", place) else ""), "place": place[:80],
        "level": level, "deadline": deadline, "quote": m.group(0), "funding_for": "", "amount": salary[:200],
        "cn": "no" if _any(_RESTRICTED, body) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, body) else [], "via": "TAMU Natural Resources Job Board",
    }, "收录"


# ───────────────────────── H-Net Job Guide ─────────────────────────

HNET = "https://networks.h-net.org"


def hnet_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for page in range(max_pages):
        raw = f.get(f"{HNET}/jobs/browse?page={page}").text
        new = 0
        for jid, slug in re.findall(r'href="(?:https://networks\.h-net\.org)?/jobs/(\d+)/([a-z0-9-]+)"', raw):
            if jid not in seen and re.search(r"post-?doc|postdoctoral|doctoral|ph-?d|fellow", slug):
                seen[jid] = f"{HNET}/jobs/{jid}/{slug}"
                new += 1
        if not re.search(r"/jobs/\d+/", raw):
            break
    return list(seen.items())


def hnet_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    full = page_text(h1.group(1)) if h1 else ""
    org, _, title = full.partition(" - ")
    title = title or full
    text = page_text(raw)
    pos = re.search(r"\bPosition\s+(Post-Doctoral Fellow|Graduate Student|Fellowship|[A-Z][\w /-]{2,40}?)\s+[A-Z]", text)
    level = level_of(title) or ("postdoc" if pos and "Post-Doctoral" in pos.group(1) else None)
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"Closing Date\s+([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    if not m:
        return None, "页面无截止日期"
    deadline = parse_day(m.group(1))
    if not deadline or deadline < today:
        return None, "已截止"
    body = text[:m.start()]
    if _any(_SELF_FUNDED, body) or not _any(_FUNDED, body):
        return None, "未写资助或自费"
    cur = r"(?:[$€£]|USD|EUR|GBP|CHF|CAD|AUD|ILS)"
    pay = re.search(rf"(?:salary|stipend)[^.]{{0,80}}?{cur}\s?[\d,]+[^.]{{0,40}}|{cur}\s?[\d,]{{5,}}[^.]{{0,40}}(?:salary|stipend)", body, re.I)
    loc = re.search(r"\bLocation\s+(.{3,80}?)\s+(?:Subject Fields|Posting Date|Institution Type|Position)\b", text)
    place = loc.group(1) if loc else ""
    return {
        "id": f"hnet:{jid}", "title": title[:200], "url": url, "org": org[:120], "country": place_country(place),
        "place": place[:80], "level": level, "deadline": deadline, "quote": m.group(0), "funding_for": "",
        "amount": (pay.group(0).strip() if pay else "")[:200], "cn": "no" if _any(_RESTRICTED, body) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, body) else [], "via": "H-Net Job Guide",
    }, "收录"


ADAPTERS = {"mathjobs": (mj_urls, mj_detail), "tamu-rwfm": (tamu_urls, tamu_detail), "hnet": (hnet_urls, hnet_detail)}
VIA_RANK = {"MathJobs": 2, "TAMU Natural Resources Job Board": 2, "H-Net Job Guide": 2}
