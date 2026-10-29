"""英国研究所 / 学校自己的博士招聘页适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。
用来替代被 Cloudflare 拦截的 FindAPhD（路线图第 5 项“原始出处”）。

- Francis Crick Institute：“PhD student positions” 列表（?page=N 翻页）列出当年每个博士课题，课题页有
  “Application close date 03 November 2026, 12:00 GMT”。资助与资格写在招生总页（PhD student recruitment）上，
  对全部课题适用：“Candidates of all nationalities can apply”、学费（含国际生）与免税生活费；少数课题另有资格限制时
  写在课题页顶部（按课题页正文判断限本土）。robots.txt 只禁止 /admin/、/search/、/user/ 等后台路径。
"""
from __future__ import annotations

import re

import collect_postings as cp
from collect_postings import Fetcher, page_text, parse_day

# ───────────────────────── Francis Crick Institute ─────────────────────────

CRICK = "https://www.crick.ac.uk"
CRICK_LIST = CRICK + "/careers-and-study/students/phd-students/phd-student-positions?page={page}"
CRICK_TERMS = CRICK + "/careers-study/students/phd-student-recruitment"
_CRICK: dict[str, str] = {}  # 招生总页上对全部课题适用的资助与资格原句


def crick_terms(raw: str) -> dict[str, str]:
    """从招生总页摘出资助金额、学费与国籍原句；页面上没写的就留空（不猜）。"""
    text = page_text(raw)
    stipend = re.search(r"£[\d,]+ tax-free student stipend[^.]{0,80}?per year for \w+ years", text)
    fees = re.search(r"Tuition fees \(including for international students\)", text)
    who = re.search(r"Candidates of all nationalities can apply[^.]{0,80}", text)
    return {"amount": stipend.group(0) if stipend else "", "fees": fees.group(0) if fees else "",
            "who": who.group(0).strip() if who else ""}


def crick_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    _CRICK.clear()
    _CRICK.update(crick_terms(f.get(CRICK_TERMS).text))
    seen: dict[str, str] = {}
    for page in range(max(max_pages, 20)):  # 每页约 3 个课题，一年二三十个
        found = re.findall(r'href="(/careers-study/vacancies/([a-z0-9-]+))"', f.get(CRICK_LIST.format(page=page)).text)
        new = [(path, slug) for path, slug in dict.fromkeys(found) if slug not in seen]
        if not new:
            break
        seen.update({slug: CRICK + path for path, slug in new})
    return list(seen.items())


def crick_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    # 标题形如“Sateriale Lab | Host-pathogen interactions …”：去掉课题组前缀，与其他平台上的同一课题能去重
    title = re.sub(r"^.{0,80}?\bLabs?\s*\|\s*", "", page_text(h1.group(1)) if h1 else "")
    m = re.search(r"Application close date</div>\s*<div[^>]*>\s*<span[^>]*>\s*([^<]+?)\s*</span>\s*"
                  r"(?:<span[^>]*>\s*([A-Z]{2,4})\s*</span>)?", raw)
    if not m:
        return None, "页面无截止日期"
    deadline = parse_day(m.group(1).split(",")[0])
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    if not (_CRICK.get("amount") or _CRICK.get("fees")):
        return None, "未写资助"  # 招生总页没读到资助原句：不收，不猜
    text = page_text(raw)
    cn = "no" if cp.cn_of(text) == "no" else "yes" if _CRICK.get("who") else "check"
    return {
        "id": f"crick:{jid}", "title": title[:200], "url": url, "org": "The Francis Crick Institute",
        "country": "UK", "place": "London", "level": "phd", "deadline": deadline,
        "quote": "Application close date " + " ".join(g for g in m.groups() if g),
        "funding_for": _CRICK.get("fees", ""), "amount": _CRICK.get("amount", ""),
        "cn": cn, "flags": cp.flags_of(text), "via": "Crick",
    }, "收录"


ADAPTERS = {"crick": (crick_urls, crick_detail)}
VIA_RANK = {"Crick": 3}
