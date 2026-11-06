"""英国研究所 / 学校自己的博士招聘页适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。
用来替代被 Cloudflare 拦截的 FindAPhD（路线图第 5 项“原始出处”）。

- Francis Crick Institute：“PhD student positions” 列表（?page=N 翻页）列出当年每个博士课题，课题页有
  “Application close date 03 November 2026, 12:00 GMT”。资助与资格写在招生总页（PhD student recruitment）上，
  对全部课题适用：“Candidates of all nationalities can apply”、学费（含国际生）与免税生活费；少数课题另有资格限制时
  写在课题页顶部（按课题页正文判断限本土）。robots.txt 只禁止 /admin/、/search/、/user/ 等后台路径。
- MRC Laboratory of Medical Sciences（LMS）：“LMS 4-year PhD studentships” 招生页列出当年每个资助课题（课题介绍是 .docx 附件），
  截止日期、资助与资格对全部课题适用，都写在同一页上，所以列表与详情都读这一页（每个课题读一次，同页带 #锚点区分）。
  robots.txt 只禁止 /wp-admin/。
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
    # 列表每次打开的排序不固定（同一课题会出现在不同页、有的页轮不到），所以按翻页栏的最后一页把每页都读一遍，
    # 再读第二遍补上第一遍漏掉的；不能在“某页没有新课题”时提前停
    seen: dict[str, str] = {}
    first = f.get(CRICK_LIST.format(page=0)).text
    last = min(max([int(n) for n in re.findall(r"[?&]page=(\d+)", first)] or [0]), 30)
    for rnd in range(2):
        for page in range(last + 1):
            raw = first if rnd == 0 and page == 0 else f.get(CRICK_LIST.format(page=page)).text
            for path, slug in re.findall(r'href="(/careers-study/vacancies/([a-z0-9-]+))"', raw):
                seen.setdefault(slug, CRICK + path)
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


# ───────────────────────── MRC Laboratory of Medical Sciences ─────────────────────────

LMS_PAGE = "https://lms.mrc.ac.uk/work-and-study/studentships/lms-4-year-phd-studentships/"
LMS_PROJECT = re.compile(r'href="https://lms\.mrc\.ac\.uk/wp-content/uploads/([A-Za-z0-9-]+)-Project[^"]*\.docx"[^>]*>([^<]{5,200})<')


def lms_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    raw = f.get(LMS_PAGE).text
    return [(slug.lower(), f"{LMS_PAGE}#{slug.lower()}") for slug, _ in dict(LMS_PROJECT.findall(raw)).items()]


def lms_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    title = next((page_text(t) for slug, t in LMS_PROJECT.findall(raw) if slug.lower() == jid), "")
    if not title:
        return None, "非博士/博后岗位"
    text = page_text(raw)
    m = re.search(r"Application deadline:?\s*(?:\w+day\s+)?(\d{1,2})\s*(?:st|nd|rd|th)?\s+([A-Z][a-z]+\s+\d{4})(?:\s*\(([\d:]+)\))?", text)
    deadline = parse_day(f"{m.group(1)} {m.group(2)}") if m else None
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    stipend = re.search(r"tax-free stipend of £[\d,]+ per year, for \w+ years", text)
    fees = re.search(r"Full coverage of student tuition fees", text)
    if not (stipend or fees):
        return None, "未写资助"
    cn = "no" if cp.cn_of(text) == "no" else "yes" if re.search(r"open to applicants of all nationalities", text) else "check"
    return {
        "id": f"lms:{jid}", "title": title[:200], "url": url, "org": "MRC Laboratory of Medical Sciences (LMS)",
        "country": "UK", "place": "London", "level": "phd", "deadline": deadline, "quote": m.group(0).strip(),
        "funding_for": fees.group(0) if fees else "", "amount": stipend.group(0) if stipend else "",
        "cn": cn, "flags": cp.flags_of(text), "via": "MRC LMS",
    }, "收录"


# ───────────────────────── University of Southampton ─────────────────────────
# 学校自己的“当前在招博士课题”列表（/study/postgraduate-research/projects?page=N，约 24 页），每张卡片写明
# Closing date 与 Funding（Competition funded / Fully funded (UK only) / Fully funded (UK and international)）。
# 竞争性资助按本库规则不收，所以列表阶段只挑“Fully funded”的课题去读详情页；详情页顶部同样写着 Funding 与 Closing date，
# 以详情页为准。robots.txt 只禁止 /research/search/、/profileview/ 等，不禁止 /study/postgraduate-research/projects。
# 详情页“Fees and funding”一节多是学校通用说明，没有写具体金额 → amount 留空，不猜。

SOTON = "https://www.southampton.ac.uk"
SOTON_LIST = SOTON + "/study/postgraduate-research/projects?page={page}"
SOTON_CARD = re.compile(r'<a href="(/study/postgraduate-research/projects/([a-z0-9-]+))" class="card-link">.*?'
                        r'Funding:</span>\s*<span>([^<]*)</span>', re.S)
_MON3 = {m[:3]: i + 1 for i, m in enumerate(cp.MONTHS)}


def soton_day(s: str) -> str | None:
    """'31 Jan 2027' / '31 January 2027' → ISO。"""
    from datetime import date
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{4})", s)
    if not m or m.group(2).lower() not in _MON3:
        return parse_day(s)
    try:
        return date(int(m.group(3)), _MON3[m.group(2).lower()], int(m.group(1))).isoformat()
    except ValueError:
        return None


def soton_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for page in range(min(max_pages, 40)):
        cards = SOTON_CARD.findall(f.get(SOTON_LIST.format(page=page)).text)
        if not cards:
            break
        for path, slug, funding in cards:
            if funding.strip().lower().startswith("fully funded"):
                seen.setdefault(slug, SOTON + path)
    return list(seen.items())


def soton_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = page_text(h1.group(1)) if h1 else ""
    fund = re.search(r"Funding\s+(Fully funded \([^)]*\)|Competition funded|Self[- ]funded[^.]{0,40}?)\s+Type of degree", text)
    if not fund or not fund.group(1).lower().startswith("fully funded"):
        return None, "自费或竞争性资助"
    m = re.search(r"Closing date\s+(\d{1,2}\s+[A-Za-z]{3,9}\.?\s+\d{4})", text)
    deadline = soton_day(m.group(1)) if m else None
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    who = fund.group(1)
    cn = "yes" if re.search(r"international", who, re.I) else "no" if re.search(r"UK only", who, re.I) else "check"
    if cn == "yes" and cp.cn_of(text) == "no":
        cn = "check"  # 页面正文另写了限本土：不凭标签判断
    level = "postdoc" if cp.POSTDOC.search(title) and not cp.PHD.search(title) else "phd"
    return {
        "id": f"soton:{jid}", "title": title[:200], "url": url, "org": "University of Southampton",
        "country": "UK", "place": "Southampton", "level": level, "deadline": deadline,
        "quote": "Closing date " + m.group(1), "funding_for": "Funding: " + who, "amount": "",
        "cn": cn, "flags": cp.flags_of(text), "via": "Southampton",
    }, "收录"


# ───────────────────────── Coventry University ─────────────────────────
# 学校自己的“Research studentships”列表（一页，列出当前在招的带资助课题；无资助的课题另放在 non-funded-studentships 页，不读）。
# 课题页顶部是固定字段：Eligibility / Duration / Application deadline / Start date；资助写在“Funding”小节
# （如 “Tuition fees and bursary”，多不写金额 → amount 留空，不猜）。robots.txt 只禁 /episerver、/shared-content、站内搜索等。

COV = "https://www.coventry.ac.uk"
COV_LIST = COV + "/research/research-opportunities/research-students/research-studentships/"
COV_LINK = re.compile(r'href="(?:https://www\.coventry\.ac\.uk)?(/research/research-opportunities/research-students/'
                      r'research-studentships/([a-z0-9-]+)/)"')


def cov_field(raw: str, label: str) -> str:
    m = re.search(rf"<strong>\s*{label}:?\s*</strong>(.*?)</p>", raw, re.S | re.I)
    return page_text(m.group(1)) if m else ""


def cov_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for path, slug in COV_LINK.findall(f.get(COV_LIST).text):
        if "non-funded" not in slug:
            seen.setdefault(slug, COV + path)
    return list(seen.items())


def cov_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = page_text(h1.group(1)) if h1 else ""
    fund = re.search(r"<h3>\s*Funding\s*</h3>\s*<p>(.*?)</p>", raw, re.S | re.I)
    fund_text = page_text(fund.group(1)) if fund else ""
    if not fund_text or re.search(r"self[- ]fund|non[- ]funded|no funding", fund_text, re.I):
        return None, "自费或竞争性资助"
    when = cov_field(raw, "Application deadline")
    deadline = soton_day(when) if when else None
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    who = cov_field(raw, "Eligibility")
    cn = ("yes" if re.search(r"international", who, re.I) else
          "no" if re.search(r"\bUK only\b|home (fee|student)s? only", who, re.I) else "check")
    text = page_text(raw)
    if cn == "yes" and cp.cn_of(text) == "no":
        cn = "check"  # 正文另写了限本土：不凭顶部字段判断
    return {
        "id": f"coventry:{jid}", "title": title[:200], "url": url, "org": "Coventry University",
        "country": "UK", "place": "Coventry", "level": "phd", "deadline": deadline,
        "quote": "Application deadline: " + when, "funding_for": "Funding: " + fund_text, "amount": "",
        "cn": cn, "flags": cp.flags_of(text), "via": "Coventry",
    }, "收录"


ADAPTERS = {"crick": (crick_urls, crick_detail), "lms": (lms_urls, lms_detail), "soton": (soton_urls, soton_detail),
            "coventry": (cov_urls, cov_detail)}
VIA_RANK = {"Crick": 3, "MRC LMS": 3, "Southampton": 3, "Coventry": 3}
