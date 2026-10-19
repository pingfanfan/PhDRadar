#!/usr/bin/env python3
"""采集招聘平台上具体的带资助博士/博后岗位，逐个读详情页，由程序提取截止日期原文。

    python scripts/collect_postings.py --today 2026-10-18                  # 全部平台
    python scripts/collect_postings.py -s jobs-ac-uk --max-pages 5 --dry-run

只收：详情页上能读到截止日期原文、截止 ≥ 今天、写明有资助的岗位。
国际生资格只看页面字段（jobs.ac.uk 的 “Funding for”）或明确限制语句；看不出来标 'check'。
结果写入 _data/postings.yml（按截止日期排序；本次未再见到的旧岗位在截止前保留）。
"""
from __future__ import annotations

import argparse
import html as htmllib
import importlib
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.modules.setdefault("collect_postings", sys.modules[__name__])  # 直接运行时，platforms_*.py 导入的也是这一份
from scrapers.common import Disallowed, Fetcher, _FUNDED, _INTERNATIONAL, _RESTRICTED, _SCREENING, _SELF_FUNDED, _any  # noqa: E402

OUT = ROOT / "_data" / "postings.yml"
LD_RE = re.compile(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
MONTH3 = {"jan": "January", "feb": "February", "mar": "March", "apr": "April", "may": "May", "jun": "June", "jul": "July",
          "aug": "August", "sep": "September", "sept": "September", "oct": "October", "nov": "November", "dec": "December"}
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}
POSTDOC = re.compile(r"post[\s-]?doc|postdoctoral|research (associate|fellow)", re.I)
PHD = re.compile(r"\bph\.?d\b|doctoral|doctorate|studentship|promovend|dphil|candidate", re.I)
# 不是学位/博后岗位的常见标题（教职、行政、技术员、实习等）
NOT_TARGET = re.compile(r"lecturer|professor|manager|administrator|technician|officer|assistant \(|internship|"
                        r"clinical training|teaching fellow|director|coordinator|faculty (position|member)|junior faculty|research faculty|^faculty\b|\bexpert\b", re.I)


def page_text(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", " ", raw, flags=re.S | re.I)
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def job_posting(raw: str) -> dict:
    def find(node):
        if isinstance(node, dict):
            if node.get("@type") == "JobPosting":
                return node
            node = list(node.values())
        if isinstance(node, list):
            for v in node:
                hit = find(v)
                if hit:
                    return hit
        return None

    for block in LD_RE.findall(raw):
        try:
            hit = find(json.loads(block))
        except json.JSONDecodeError:
            continue
        if hit:
            return hit
    return {}


def parse_day(s: str) -> str | None:
    """'20th December 2026' / '20 December 2026' / '2026-12-20' → ISO；没有年份返回 None。"""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return m.group(0)
    try:
        m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s*,?\s+(\d{4})", s)
        if m and m.group(2).lower() in MONTHS:
            return date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
        m = re.search(r"([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", s)
        if m and m.group(1).lower() in MONTHS:
            return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))).isoformat()
    except ValueError:  # 31 November 之类的无效日期
        return None
    return None


def level_of(title: str) -> str | None:
    if NOT_TARGET.search(title):
        return None
    if re.search(r"post[\s-]?doc|postdoctoral", title, re.I):
        return "postdoc"
    if PHD.search(title):  # “PhD Research Fellow”（挪威 stipendiat）是博士岗位，先于 research fellow 判断
        return "phd"
    if POSTDOC.search(title):
        return "postdoc"
    return None


# ───────────────────────── 各平台共用的正文判断（2026-10 抽检 300 条后按错误模式补充） ─────────────────────────

# 安全审查：法国 ZRR/PPST、瑞典《保护性安全法》、挪威安全法与出口管制、美国 DOE Q 级许可
SCREENING = _SCREENING + [r"\bZRR\b", r"\bPPST\b", r"protection of (the )?national scientific", r"protective security act",
                          r"\bsikkerhetsloven", r"\beksportkontroll", r"export of strategic goods", r"\bQ[- ]?(level )?clearance\b"]
# 限本土：只付本土学费且国际生自付差额、只限有 Home 学费资格者、需美国公民身份
RESTRICTED = _RESTRICTED + [
    r"\brestricted to (applicants|candidates|students) (who|with)[^.]{0,60}\b(home|uk|eu|eea|citizen|citizenship|resident)",
    r"\brequires? u\.?s\.? citizenship\b", r"\bu\.?s\.? citizenship (is )?required\b", r"\bmust be (a )?u\.?s\.? citizens?\b",
    r"\binternational[^.]{0,120}\b(pay|cover|fund|meet)\b[^.]{0,60}\bdifference\b",
    r"\bdifference between (the )?(home|uk) and international", r"\bextra costs associated with international",
]
INTERNATIONAL = _INTERNATIONAL + [r"\bfrom any country\b"]
# 不是已落实资助的岗位：竞争性奖学金的意向征集、资助尚未落实、按时薪的远程合同工
NOT_FUNDED = [
    r"expressions? of interest[^.]{0,160}\b(fellowships?|programmes?|programs?)\b",
    r"\bwishing to apply (for|to)[^.]{0,100}\b(fellowships?|programmes?|programs?)\b",
    r"\bapplications? to one or more of the following[^.]{0,60}(funding|fellowship)",
    r"\bfunding[^.]{0,40}has not (yet )?been (secured|confirmed)", r"\bsubject to (the )?(successful )?(funding|availability of funding)\b",
    r"\bremote contract\b", r"\bpay rate:?\s*\$\d+", r"\bmore projects than funded (opportunities|places|studentships)\b",
]
ROLLING = re.compile(r"[^.]{0,120}(?:until (?:the |a )?(?:position|post|positions|vacancy|role|job)s? (?:is |are |has been |have been )?filled|"
                     r"on a rolling basis|open until filled|no deadline for (?:the )?application)[^.]{0,60}", re.I)


def cn_of(text: str) -> str:
    """正文写明限本土 → no；写明对国际生 / 所有国籍开放 → yes；都没有 → check（不猜）。"""
    return "no" if _any(RESTRICTED, text) else "yes" if _any(INTERNATIONAL, text) else "check"


def flags_of(text: str) -> list[str]:
    return ["security-screening"] if _any(SCREENING, text) else []


def refine_deadline(deadline: str, quote: str, body: str, today: str) -> tuple[str, str]:
    """平台页头的截止日常是广告下架日：正文另写了（今天以后的）申请截止就以正文为准，取最早的一个；
    正文没写任何截止日期、只说招满为止 / 滚动审核 → rolling；其余保持页头。"""
    found = all_deadlines(body)
    future = sorted(d for d in found if d[0] >= today)
    if future:
        return future[0] if future[0][0] != deadline else (deadline, quote)
    if not found:
        m = ROLLING.search(body)
        if m:
            return "rolling", m.group(0).strip()[:160]
    return deadline, quote


# ───────────────────────── jobs.ac.uk ─────────────────────────

JAC = "https://www.jobs.ac.uk"
JAC_LISTS = [JAC + "/search/?jobTypeFacet%5B%5D=phds&pageSize=25&startIndex={start}",
             JAC + "/search/?keywords=postdoctoral&pageSize=25&startIndex={start}",
             JAC + "/search/?keywords=postdoc&pageSize=25&startIndex={start}"]
JAC_HREF = re.compile(r'href="(/job/([A-Z0-9]+)/[^"?#]+)')


def jac_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for tpl in JAC_LISTS:
        for page in range(max_pages):
            raw = f.get(tpl.format(start=1 + 25 * page)).text
            new = 0
            for href, jid in JAC_HREF.findall(raw):
                if jid not in seen:
                    seen[jid] = JAC + href
                    new += 1
            if not new:
                break
    return list(seen.items())


# JSON-LD 里的国家写法（ISO 代码或英文名）→ 本库地区代码
COUNTRY = {"GB": "UK", "UNITED KINGDOM": "UK", "UK": "UK", "ENGLAND": "UK", "SCOTLAND": "UK", "WALES": "UK",
           "NORTHERN IRELAND": "UK", "HONG KONG": "HK", "HK": "HK", "CHINA": "CN", "IRELAND": "IE", "IE": "IE",
           "NETHERLANDS": "NL", "GERMANY": "DE", "DENMARK": "DK", "SWEDEN": "SE", "NORWAY": "NO", "FINLAND": "FI",
           "BELGIUM": "BE", "FRANCE": "FR", "SPAIN": "ES", "ITALY": "IT", "PORTUGAL": "PT", "SWITZERLAND": "CH",
           "AUSTRIA": "AT", "POLAND": "PL", "CZECH REPUBLIC": "CZ", "CZECHIA": "CZ", "LUXEMBOURG": "LU",
           "SINGAPORE": "SG", "JAPAN": "JP", "SOUTH KOREA": "KR", "KOREA": "KR", "AUSTRALIA": "AU",
           "NEW ZEALAND": "NZ", "CANADA": "CA", "UNITED STATES": "US", "USA": "US", "US": "US", "MACAU": "MO",
           "TAIWAN": "TW", "ISRAEL": "IL", "QATAR": "QA", "SAUDI ARABIA": "SA", "UNITED ARAB EMIRATES": "AE",
           "ÖSTERREICH": "AT", "DEUTSCHLAND": "DE", "SCHWEIZ": "CH", "MOROCCO": "MA"}
US_STATES = ("Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|"
             "Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|"
             "Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|"
             "Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|"
             "West Virginia|Wisconsin|Wyoming|District of Columbia")
US_ABBR = ("AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|"
           "OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC")


def country_code(raw: str) -> str:
    """JSON-LD 国家（ISO 代码或英文名）→ 本库地区代码；认不出就留空，不猜。"""
    raw = str(raw or "").strip().upper()
    if raw in COUNTRY:
        return COUNTRY[raw]
    return raw if len(raw) == 2 and raw.isalpha() else ""


def place_country(place: str) -> str:
    """Madgex 的地点栏 → 地区代码：'Vienna (AT)' 取括号里的代码，否则找完整国名；认不出留空。"""
    m = re.search(r"\(([A-Z]{2})\)", place or "")
    if m:
        return country_code(m.group(1))
    up = (place or "").upper()
    hits = {v for k, v in COUNTRY.items() if len(k) > 2 and re.search(rf"\b{k}\b", up)}
    if not hits and re.search(rf",\s*(?:{US_STATES})\s*$", place or ""):  # 'Memphis, Tennessee'（Georgia 等州名放在逗号后才算）
        hits = {"US"}
    if not hits and re.search(rf",\s*(?:{US_ABBR})\s*$|\s(?:US|USA)\s*$", place or ""):  # 'Houston, TX' / 'Princeton, New Jersey US'
        hits = {"US"}
    return hits.pop() if len(hits) == 1 else ""


def jac_field(text: str, name: str, nxt: str) -> str:
    m = re.search(rf"{name}:\s*(.*?)\s+(?:{nxt}):", text)
    return m.group(1).strip() if m else ""


def jac_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    ld = job_posting(raw)
    title = (ld.get("title") or "").strip()
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    closes = re.search(r"Closes:\s*(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})", text)
    if not closes:
        return None, "页面无截止日期"
    deadline = parse_day(closes.group(1))
    if not deadline or deadline < today:
        return None, "已截止"
    funding_for = jac_field(text, "Funding for", "Funding amount|Hours|Placed On|Salary")
    amount = jac_field(text, "Funding amount", "Hours|Placed On")
    salary = jac_field(text, "Salary", "Hours|Placed On|Contract Type")
    body = text[closes.end():]
    if _any(_SELF_FUNDED, title + " " + amount + " " + body[:3000]) or re.search(r"competition[\s-]funded", title + amount, re.I) \
            or _any(NOT_FUNDED, body[:6000]):
        return None, "自费或竞争性资助"
    if level == "phd" and not (funding_for or amount):
        return None, "未写资助"
    if level == "postdoc" and not salary:
        return None, "未写薪资"
    head = body[:6000]
    if level == "phd":
        cn = "yes" if re.search(r"International Students", funding_for) else "no" if funding_for else "check"
        # 页头标签只写 UK Students，但正文写明国际生也可（按国际学费资助 / 不论居住身份）：标签不可靠，改为待确认
        if cn == "no" and re.search(r"international (rates?|fees?)|regardless of (their )?(residential status|nationality)", head, re.I):
            cn = "check"
        # 标签含国际生但资助只写英国 / Home 学费、没提国际学费：国际生可能要自付差额，改为待确认
        if cn == "yes" and re.search(r"\b(uk|home)\b[^.]{0,30}(tuition )?fees?", amount + " " + head, re.I) \
                and not re.search(r"international[^.]{0,30}fees?|fees?[^.]{0,30}international (rate|level)|overseas fee", amount + " " + head, re.I):
            cn = "check"
    else:
        cn = cn_of(head)
    if _any(RESTRICTED, head):  # 正文写明国际生自付差额 / 限本土
        cn = "no"
    # 只付“英国本土（Home）学费”而没提国际生：国际生要自付学费差额，按限本土处理
    if cn == "check" and level == "phd" and re.search(r"\bhome\b[^.]{0,40}fee|fee[^.]{0,40}\bhome\b", amount, re.I) \
            and not re.search(r"international|overseas", amount + funding_for, re.I):
        cn = "no"
    org = ld.get("hiringOrganization") or {}
    loc = ld.get("jobLocation") or {}
    loc = loc[0] if isinstance(loc, list) and loc else loc
    addr = (loc.get("address") or {}) if isinstance(loc, dict) else {}
    country = addr.get("addressCountry") if isinstance(addr, dict) else ""
    country = (country.get("name") if isinstance(country, dict) else country) or ""
    place = jac_field(text, "Location", "Funding for|Salary|Hours|Placed On|Funding amount")
    amount, salary = [v if not re.match(r"not specified", v, re.I) else "" for v in (amount, salary)]
    return {
        "id": f"jobs-ac-uk:{jid}",
        "title": re.sub(r"\s+", " ", title)[:200],
        "url": url,
        "org": (org.get("name") if isinstance(org, dict) else "") or "",
        "country": country_code(country),
        "place": place[:80],
        "level": level,
        "deadline": deadline,
        "quote": closes.group(0),
        "funding_for": funding_for[:120],
        "amount": (amount or salary)[:200],
        "cn": cn,
        "flags": flags_of(body[:8000]),
        "via": "jobs.ac.uk",
    }, "收录"


# ───────────────────────── AcademicTransfer ─────────────────────────

AT_SITEMAP = "https://www.academictransfer.com/sitemap-vacancies.xml"
AT_LOC = re.compile(r"<loc>([^<]+/jobs/(\d+)/[^<]+?)</loc>")
AT_SLUG = re.compile(r"phd|doctoral|promovend|doctorate|postdoc|post-doc|postdoctoral", re.I)


def at_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    return [(jid, u) for u, jid in AT_LOC.findall(f.get(AT_SITEMAP).text)
            if "/en/jobs/" in u and AT_SLUG.search(u.rstrip("/").rsplit("/", 1)[-1])]


def at_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    ld = job_posting(raw)
    title = (ld.get("title") or "").strip()
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    text = page_text(raw)
    m = re.search(r"Deadline\s+(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+[’']?(\d{2,4})", text)
    if not m:
        return None, "页面无截止日期"
    year = m.group(3) if len(m.group(3)) == 4 else "20" + m.group(3)
    deadline = parse_day(f"{m.group(1)} {MONTH3.get(m.group(2).lower(), m.group(2))} {year}")
    if not deadline or deadline < today:
        return None, "已截止"
    sm = re.search(r"Salary indication\s+(.{3,80}?per (?:month|year))", text, re.I)
    if not sm:
        return None, "未写薪资"
    if _any(NOT_FUNDED, text):
        return None, "未写资助或自费"
    deadline, quote = refine_deadline(deadline, m.group(0), text[m.end():], today)
    org = ld.get("hiringOrganization") or {}
    return {
        "id": f"academictransfer:{jid}",
        "title": re.sub(r"\s+", " ", title)[:200],
        "url": url,
        "org": (org.get("name") if isinstance(org, dict) else "") or "",
        "country": "NL", "place": "",
        "level": level,
        "deadline": deadline,
        "quote": quote,
        "funding_for": "",
        "amount": sm.group(1).strip()[:200],
        "cn": cn_of(text),
        "flags": flags_of(text),
        "via": "AcademicTransfer",
    }, "收录"


# ───────────────────────── Madgex 系招聘站（Nature Careers、Science Careers、Physics Today、THE Unijobs） ─────────────────────────
# 同一套建站系统：站点地图索引 → /job/<编号>/<slug>/；详情页有 Employer / Location / Salary / Closing date（或 Closes）

MADGEX = {  # 适配器名: (站点地图索引, 平台名, 岗位链接前缀)
    "naturecareers": ("https://www.nature.com/naturecareers/sitemapindex.xml", "Nature Careers",
                      "https://www.nature.com/naturecareers/job/"),
    "sciencecareers": ("https://jobs.sciencecareers.org/sitemapindex.xml", "Science Careers", "https://jobs.sciencecareers.org/job/"),
    "physicstoday": ("https://jobs.physicstoday.org/sitemapindex.xml", "Physics Today Jobs", "https://jobs.physicstoday.org/job/"),
    # THE 的索引里前几个是分类列表页，岗位在 sitemap2-*
    "the-unijobs": ("https://www.timeshighereducation.com/unijobs/sitemapindex.xml", "THE Unijobs",
                    "https://www.timeshighereducation.com/unijobs/listing/", r"/sitemap2-"),
}
NC_SLUG = re.compile(r"phd|doctoral|doctorate|postdoc|post-doc|postdoctoral|studentship", re.I)
MG_DATE = r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|[A-Za-z]{3,9}\.?\s+\d{1,2},\s+\d{4})"


def mg_day(s: str) -> str | None:
    """'15 Jan 2027' / 'Nov 15, 2026' → ISO（月份缩写补全后交给 parse_day）。"""
    return parse_day(re.sub(r"[A-Za-z]{3,9}\.?", lambda m: MONTH3.get(m.group(0).rstrip(".").lower()[:3], m.group(0)), s, count=1))


def madgex(name: str):
    index, via, prefix, *only = MADGEX[name]
    job_re = re.compile(r"<loc>\s*(" + re.escape(prefix) + r"(\d+)/([^<\s]*))\s*</loc>")

    def urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
        out: dict[str, str] = {}
        sitemaps = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", f.get(index).text)
        for sm in [u for u in sitemaps if not only or re.search(only[0], u)][:max_pages]:
            for url, jid, slug in job_re.findall(f.get(sm).text):
                if NC_SLUG.search(slug):
                    out.setdefault(jid, url)
        return sorted(out.items(), key=lambda kv: -int(kv[0]))

    def detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
        text = page_text(raw)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
        title = page_text(h1.group(1)) if h1 else ""
        level = level_of(title)
        if not level:
            return None, "非博士/博后岗位"
        m = re.search(r"(?:Closing date|Closes)\s+" + MG_DATE, text)
        if not m:
            return None, "页面无截止日期"
        deadline = mg_day(m.group(1))
        if not deadline or deadline < today:
            return None, "已截止"
        emp = re.search(r"Employer\s+(.{2,120}?)\s+Location\s", text)
        loc = re.search(r"Location\s+(.{2,120}?)\s+(?:Salary|Posted|Closing date|Closes)\s", text)
        sal = re.search(r"Salary\s+(.{1,120}?)\s+(?:Posted|Closing date|Closes)\s", text)
        salary = sal.group(1).strip() if sal and sal.group(1).strip() not in ("0", "-") else ""
        body = text[m.end():m.end() + 8000]
        if _any(_SELF_FUNDED, title + " " + body) or _any(NOT_FUNDED, body) or \
                (level == "phd" and not (salary or _any(_FUNDED, body))):
            return None, "未写资助或自费"
        deadline, quote = refine_deadline(deadline, m.group(0), body, today)
        ld = job_posting(raw)
        lloc = ld.get("jobLocation") or {}
        lloc = lloc[0] if isinstance(lloc, list) and lloc else lloc
        laddr = (lloc.get("address") or {}) if isinstance(lloc, dict) else {}
        lcountry = laddr.get("addressCountry") if isinstance(laddr, dict) else ""
        lcountry = (lcountry.get("name") if isinstance(lcountry, dict) else lcountry) or ""
        return {
            "id": f"{name}:{jid}",
            "title": re.sub(r"\s+", " ", title)[:200],
            "url": url,
            "org": emp.group(1).strip() if emp else "",
            "country": (place_country(loc.group(1)) if loc else "") or country_code(lcountry),
            "place": (loc.group(1).strip() if loc else "")[:80],
            "level": level,
            "deadline": deadline,
            "quote": quote,
            "funding_for": "",
            "amount": salary[:200],
            "cn": cn_of(body),
            "flags": flags_of(body),
            "via": via,
        }, "收录"

    return urls, detail


nc_urls, nc_detail = madgex("naturecareers")


# ───────────────────────── Jobbnorge（挪威高校，官方公开接口） ─────────────────────────

JN_API = "https://publicapi.jobbnorge.no/v1/jobs?lang=2"
JN_TITLE = re.compile(r"stipendiat|ph\.?d|doktorgrad|doctoral|postdoktor|post-?doc", re.I)
_JN: dict[str, dict] = {}  # 接口数据缓存：详情页是脚本渲染的，截止日期以接口字段为准


def jn_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out = []
    for it in f.get(JN_API).json():
        if JN_TITLE.search(it.get("title") or ""):
            _JN[str(it["id"])] = it
            out.append((str(it["id"]), it.get("link") or f"https://www.jobbnorge.no/ledige-stillinger/stilling/{it['id']}"))
    return out


def jn_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    it = _JN.get(jid) or {}
    title = (it.get("title") or "").strip()
    level = level_of(title) or ("phd" if re.search(r"stipendiat|doktorgrad", title, re.I) else
                                "postdoc" if re.search(r"postdoktor", title, re.I) else None)
    if not level:
        return None, "非博士/博后岗位"
    m = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", it.get("deadline") or "")
    if not m:
        return None, "页面无截止日期"
    deadline = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    if deadline < today:
        return None, "已截止"
    return {
        "id": f"jobbnorge:{jid}", "title": title[:200], "url": url, "org": it.get("employer") or "",
        "country": "NO", "place": (it.get("location") or "")[:80], "level": level, "deadline": deadline,
        "quote": f"Søknadsfrist {it['deadline']}", "funding_for": "", "amount": "",
        "cn": "check", "flags": [], "via": "Jobbnorge",
    }, "收录"


# ───────────────────────── INSPIRE-HEP Jobs（高能物理 / 天体物理岗位库，公开 REST 接口） ─────────────────────────

INSPIRE_API = "https://inspirehep.net/api/jobs?size=100&page={page}&sort=mostrecent&q=status:open"
_INSPIRE_COUNTRY: dict[str, str] = {}  # 机构记录 → 国家代码（每个机构只查一次）


def inspire_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    """列出在招的博士 / 博后岗位；详情直接取该岗位的接口记录（JSON），截止日期是机构填写的结构化字段。"""
    out = []
    for page in range(1, max_pages + 1):
        hits = f.get(INSPIRE_API.format(page=page)).json()["hits"]["hits"]
        for h in hits:
            m = h["metadata"]
            if not {"PHD", "POSTDOC"} & set(m.get("ranks") or []):
                continue
            for inst in m.get("institutions") or []:
                ref = (inst.get("record") or {}).get("$ref", "")
                if ref and ref not in _INSPIRE_COUNTRY:
                    try:
                        addr = (f.get(ref).json()["metadata"].get("addresses") or [{}])[0]
                        _INSPIRE_COUNTRY[ref] = country_code(addr.get("country_code"))
                    except Exception:  # noqa: BLE001 机构记录取不到就不写国家
                        _INSPIRE_COUNTRY[ref] = ""
            out.append((str(m["control_number"]), f"https://inspirehep.net/api/jobs/{m['control_number']}"))
        if len(hits) < 100:
            break
    return out


def inspire_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    m = json.loads(raw)["metadata"]
    ranks = set(m.get("ranks") or [])
    level = "postdoc" if "POSTDOC" in ranks else "phd" if "PHD" in ranks else None
    if not level or m.get("status") != "open":
        return None, "非博士/博后岗位"
    deadline = m.get("deadline_date") or ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", deadline):
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    body = page_text(m.get("description") or "")
    if _any(_SELF_FUNDED, body) or _any(NOT_FUNDED, body) or (level == "phd" and not _any(_FUNDED, body)):
        return None, "未写资助或自费"
    deadline, quote = refine_deadline(deadline, f"Deadline: {deadline}", body, today)
    insts = m.get("institutions") or []
    countries = {_INSPIRE_COUNTRY.get((i.get("record") or {}).get("$ref", ""), "") for i in insts} - {""}
    return {
        "id": f"inspire:{jid}", "title": re.sub(r"\s+", " ", m.get("position") or "")[:200],
        "url": f"https://inspirehep.net/jobs/{jid}", "org": " / ".join(i.get("value", "") for i in insts)[:120],
        "country": countries.pop() if len(countries) == 1 else "", "place": ", ".join(m.get("regions") or [])[:80],
        "level": level, "deadline": deadline, "quote": quote, "funding_for": "", "amount": "",
        "cn": cn_of(body), "flags": flags_of(body), "via": "INSPIRE-HEP Jobs",
    }, "收录"


# ───────────────────────── Academic Jobs Online（RSS 列表 + 岗位页上的 Appl Deadline） ─────────────────────────

AJO_RSS = "https://academicjobsonline.org/ajo?joblist-0-0-0-----rss--"
_AJO: dict[str, dict] = {}  # RSS 字段缓存：机构、国家、薪资括注


def ajo_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out = []
    for item in re.findall(r"<item\b(.*?)</item>", f.get(AJO_RSS).text, re.S):
        def tag(name: str) -> str:
            m = re.search(rf"<{name}>(.*?)</{name}>", item, re.S)
            return htmllib.unescape(m.group(1).strip()) if m else ""
        jid, title = tag("ads:ID"), tag("title")
        if not jid or not level_of(title):
            continue
        _AJO[jid] = {"univ": tag("ads:Univ"), "dept": tag("ads:Dept"), "country": tag("ads:Country"),
                     "city": tag("ads:City"), "desc": tag("description")}
        out.append((jid, f"https://academicjobsonline.org/ajo/jobs/{jid}"))
    return out


def ajo_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    it = _AJO.get(jid) or {}
    t = re.search(r"Position Title:\s*(.{3,200}?)\s+Position Type:", text)
    title = t.group(1) if t else ""
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"Appl Deadline:\s*(\d{4})/(\d{2})/(\d{2})", text)  # 只写 listed until 的不算截止日期
    if not m:
        return None, "页面无截止日期"
    deadline = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if deadline < today:
        return None, "已截止"
    d = text.find("Position Description:")
    body = text[d:d + 8000] if d >= 0 else it.get("desc", "")
    if _any(_SELF_FUNDED, body) or _any(NOT_FUNDED, body) or (level == "phd" and not _any(_FUNDED, body)):
        return None, "未写资助或自费"
    deadline, quote = refine_deadline(deadline, m.group(0), body, today)
    pay = re.match(r"\[([^\]]{3,150})\]", it.get("desc", ""))  # 雇主在简介开头括注的薪资
    return {
        "id": f"ajo:{jid}", "title": title[:200], "url": url,
        "org": ", ".join(x for x in (it.get("univ"), it.get("dept")) if x)[:120],
        "country": country_code(it.get("country")), "place": it.get("city", "")[:80], "level": level,
        "deadline": deadline, "quote": quote, "funding_for": "",
        "amount": pay.group(1) if pay and re.search(r"\d", pay.group(1)) else "",
        "cn": cn_of(body), "flags": flags_of(body), "via": "Academic Jobs Online",
    }, "收录"


# ───────────────────────── DAAD PhDGermany（德国博士岗位库；详情链接必须带 phd-id，否则服务器返回别的岗位） ─────────────────────────

DAAD = "https://www.daad.de"
DAAD_LIST = DAAD + "/en/studying-in-germany/phd-studies-research/phd-germany/?phd-p={page}"
DAAD_LINK = re.compile(r'href="(/en/studying-in-germany/phd-studies-research/phd-germany/detail/[^"?#]*-(\d{3,6})/)')
DAAD_PHD = re.compile(r"Type of Position\s+(?:Full PhD|PhD|Structured PhD|Individual PhD|Cotutelle)", re.I)


def daad_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for page in range(1, max_pages + 1):
        found = DAAD_LINK.findall(f.get(DAAD_LIST.format(page=page)).text)
        if not found:
            break
        for path, jid in found:
            out.setdefault(jid, f"{DAAD}{path}?phd-id={jid}")
    return list(out.items())


def daad_field(text: str, name: str, nxt: str) -> str:
    m = re.search(rf"{name}\s+(.{{1,200}}?)\s+(?:{nxt})\b", text)
    return m.group(1).strip() if m else ""


def daad_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    t = re.search(r"<title>\s*\"(.+?)\"\s*-\s*(.*?)\s*-\s*DAAD\s*</title>", htmllib.unescape(re.search(
        r"<title>.*?</title>", raw, re.S).group(0)) if "<title>" in raw else "", re.S)  # "岗位名" - 机构 - DAAD
    if not t:
        return None, "页面无标题"
    title, org = page_text(t.group(1)), page_text(t.group(2))
    # 页面标题里的机构名混着课题组和导师名；联系人栏用 <br> 分开“机构 / 院系 / 联系人”，取第一段
    head = re.search(r'class="qa-headline[^"]*"[^>]*>(.*?)</h3>', raw, re.S)
    if head:
        org = page_text(re.split(r"<br\s*/?>", head.group(1))[0]) or org
    if not DAAD_PHD.search(text):  # 短期访学（Research Stay）等不是博士岗位
        return None, "非博士/博后岗位"
    level = "phd"
    m = re.search(r"Application Deadline\s+(\d{1,2})\.\s*([A-Za-z]{3})[a-z]*\.?\s+(\d{4})", text)
    if not m:
        return None, "页面无截止日期"
    deadline = mg_day(f"{m.group(1)} {m.group(2)} {m.group(3)}")
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    fin = re.search(r"Financing\s+(yes|no)\b", text, re.I)
    if not fin or fin.group(1).lower() != "yes" or _any(_SELF_FUNDED, text):
        return None, "未写资助或自费"
    start = daad_field(text, "Starting Date", "Overview|Description")
    lang = daad_field(text, "Working Language", "Location|Required|Application|Overview")
    degree = daad_field(text, "Required Degree", "Areas of study|Description|Overview")
    req = "；".join(x for x in (f"学位要求：{degree}" if degree else "", f"工作语言：{lang}" if lang else "",
                                f"开始时间：{start}" if start else "") if x)
    return {
        "id": f"daad:{jid}", "title": title[:200], "url": url, "org": org[:120], "country": "DE",
        "place": daad_field(text, "Location", "Application|Starting|Overview")[:80], "level": level, "deadline": deadline,
        "quote": m.group(0), "funding_for": "", "amount": "", "requirements": req,
        "cn": cn_of(text), "flags": flags_of(text), "via": "DAAD PhDGermany",
    }, "收录"


# ───────────────────────── Varbi（瑞典高校共用招聘系统） ─────────────────────────

VARBI = ["lu", "kth", "uu", "su", "ki", "liu", "umu", "gu", "slu", "ltu", "mau", "oru", "kau", "miun", "hh", "his", "mdu",
         "du", "bth", "lnu", "sh", "hb", "hig", "hv"]
VARBI_NAMES = {"lu": "Lund University", "kth": "KTH Royal Institute of Technology", "uu": "Uppsala University",
               "su": "Stockholm University", "ki": "Karolinska Institutet", "liu": "Linköping University", "umu": "Umeå University",
               "gu": "University of Gothenburg", "slu": "Swedish University of Agricultural Sciences",
               "ltu": "Luleå University of Technology", "mau": "Malmö University", "oru": "Örebro University",
               "kau": "Karlstad University", "miun": "Mid Sweden University", "hh": "Halmstad University", "his": "University of Skövde",
               "mdu": "Mälardalen University", "du": "Dalarna University", "bth": "Blekinge Institute of Technology",
               "lnu": "Linnaeus University", "sh": "Södertörn University", "hb": "University of Borås", "hig": "University of Gävle",
               "hv": "University West"}
VB_LINK = re.compile(r'href="(?:https://(\w+)\.varbi\.com)?(/en/what:job/jobID:(\d+)/[^"]*)"[^>]*>(.*?)</a>', re.S)
VB_TITLE = re.compile(r"ph\.?d|doctoral|doktorand|postdoc|post-doc|postdoktor", re.I)


def vb_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for sub in VARBI:
        try:
            html = f.get(f"https://{sub}.varbi.com/en/").text
        except Exception:  # noqa: BLE001 个别学校没有 Varbi 站点
            continue
        for _, path, jid, label in VB_LINK.findall(html):
            if VB_TITLE.search(page_text(label)):
                out.setdefault(jid, f"https://{sub}.varbi.com{path}")
    return list(out.items())


def vb_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = page_text(h1.group(1)) if h1 else ""
    level = level_of(title) or ("phd" if re.search(r"doktorand", title, re.I) else
                                "postdoc" if re.search(r"postdoktor", title, re.I) else None)
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"(?:Last application date|Last day (?:of|for) application|Sista ansökningsdag)\s*:?\s*"
                  r"(\d{4}-\d{2}-\d{2}|\d{1,2}\.[A-Za-z]{3}\.\d{4})", text, re.I)
    if not m:
        return None, "页面无截止日期"
    raw_day = m.group(1)
    deadline = raw_day if "-" in raw_day else mg_day(raw_day.replace(".", " "))  # “08.Nov.2026”
    if not deadline or deadline < today:
        return None, "已截止"
    org = re.search(r"<title>.*?(?:at|vid)\s+([^<|]+)</title>", raw, re.S | re.I)
    sub = url.split("//")[1].split(".")[0]
    if _any(NOT_FUNDED, text):
        return None, "未写资助或自费"
    return {
        "id": f"varbi:{jid}", "title": re.sub(r"\s+", " ", title)[:200], "url": url,
        "org": (org.group(1).strip() if org else VARBI_NAMES.get(sub, sub.upper())),
        "country": "SE", "place": "", "level": level, "deadline": deadline, "quote": m.group(0),
        "funding_for": "", "amount": "", "cn": cn_of(text), "flags": flags_of(text), "via": "Varbi",
    }, "收录"


# ───────────────────────── 机构自己的招聘页（列表页 + 通用截止日期识别） ─────────────────────────

DEADLINE_KW = r"(?:application deadline|submit your application(?: online)? by|deadline for (?:receipt of )?applications?|deadline to apply|closing date|apply by|" \
              r"applications? (?:close|due)|applications?(?: and letters)? (?:are|is) due|full consideration[^.\d]{0,40}?by|" \
              r"(?:submitted|received) (?:no later than|by)|no later than|" \
              r"bewerbungsfrist|bewerbungsschluss|date limite de candidature|deadline)"
ANY_DATE = r"(\d{4}-\d{2}-\d{2}|\d{1,2}(?:st|nd|rd|th)?\.?\s+[A-Za-zäé]{3,9}\.?,?\s+\d{4}|[A-Za-z]{3,9}\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}|\d{1,2}\.\d{1,2}\.\d{4})"
DE_MONTHS = {"januar": "January", "februar": "February", "märz": "March", "april": "April", "mai": "May", "juni": "June",
             "juli": "July", "august": "August", "september": "September", "oktober": "October", "november": "November",
             "dezember": "December"}


def find_deadline(text: str) -> tuple[str | None, str]:
    """在正文里找“截止关键词 + 60 字内的日期”，返回 (ISO 日期, 原文片段)；没有年份或认不出就返回 None。"""
    found = all_deadlines(text)
    return found[0] if found else (None, "")


def all_deadlines(text: str) -> list[tuple[str, str]]:
    """正文里所有“截止关键词 + 日期”，按出现顺序返回 (ISO 日期, 原文片段)。"""
    out = []
    for m in re.finditer(DEADLINE_KW + r"[^.\d]{0,60}?" + ANY_DATE, text, re.I):
        raw = m.group(1)
        if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", raw):
            d, mo, y = raw.split(".")
            iso = f"{y}-{int(mo):02d}-{int(d):02d}"
        else:
            words = raw.replace(".", " ")
            for de, en in DE_MONTHS.items():
                words = re.sub(de, en, words, flags=re.I)
            iso = parse_day(re.sub(r"\b([A-Za-z]{3})[a-z]*\b", lambda x: MONTH3.get(x.group(1).lower(), x.group(0)), words))
        try:
            iso = iso and date.fromisoformat(iso).isoformat()
        except ValueError:
            iso = None
        if iso:
            out.append((iso, m.group(0).strip()[:160]))
    return out


INSTITUTES = {  # 适配器名: (列表页, 岗位链接正则（相对或绝对）, 链接前缀, 平台名, 机构, 国家)
    "ethz": (["https://jobs.ethz.ch/"], r'href="(/job/view/(\d+))"', "https://jobs.ethz.ch", "ETH Zurich Jobs", "ETH Zurich", "CH"),
    "inria": (["https://jobs.inria.fr/public/classic/en/offres"], r'href="(/public/classic/en/offres/(\d{4}-\d{5}))"',
              "https://jobs.inria.fr", "Inria Jobs", "Inria", "FR"),
    "mpg": (["https://www.mpg.de/feeds/stellenangebote.rss"], r"<link>(https://www\.mpg\.de/job-([0-9a-f]{32}))</link>", "",
            "Max-Planck-Gesellschaft", "Max-Planck-Gesellschaft", "DE"),
    # 以下三个：robots.txt 不限制岗位页；截止日期取正文 “Closing Date …” / “Deadline for receipt of applications … is …” 原文
    "psi": (["https://www.psi.ch/en/hr/job-opportunities"], r'href="(/en/hr/job-opportunities/(\d+)-[a-z0-9-]+)"', "https://www.psi.ch",
            "PSI Jobs", "Paul Scherrer Institut", "CH"),
    "eso": (["https://recruitment.eso.org/"], r'href="(/jobs/(20\d{2}_\d{4}))"', "https://recruitment.eso.org", "ESO Recruitment",
            "European Southern Observatory", "", r"<h1 style='font-size: 40px;'>(.*?)</h1>"),
    # 列表链接带 jsessionid，详情页地址按编号重拼；标题在表格的 Title 一栏
    "ibs": (["https://www.ibs.re.kr/prog/recruit/eng/sub04_01/list.do"], r'href="(/prog/recruit/eng/sub04_01/view\.do)[^"]*?idx=(\d+)"',
            "https://www.ibs.re.kr{path}?idx={jid}", "IBS Recruitment", "Institute for Basic Science", "KR",
            r"<th>Title</th>\s*<td[^>]*>(.*?)</td>"),
}
INST_TITLE = re.compile(r"ph\.?d|doctoral|doktorand|promotion|post-?doc|postdoktorand|post-doctoral|studentship", re.I)


def institute(name: str):
    pages, link_re, prefix, via, org, country, *title_re = INSTITUTES[name]
    title_re = title_re[0] if title_re else r"<h1[^>]*>(.*?)</h1>"

    def urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
        out: dict[str, str] = {}
        for page in pages:
            for path, jid in re.findall(link_re, f.get(page).text):
                out.setdefault(jid, prefix.format(path=path, jid=jid) if "{" in prefix else prefix + path)
        return list(out.items())

    def detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
        h1 = re.search(title_re, raw, re.S)
        title = page_text(h1.group(1)) if h1 else ""
        if not INST_TITLE.search(title):
            return None, "非博士/博后岗位"
        level = "postdoc" if re.search(r"post-?doc|postdoktorand|post-doctoral", title, re.I) else "phd"
        text = page_text(raw)
        found = all_deadlines(text)
        if not found:
            return None, "页面无截止日期"
        future = sorted(d for d in found if d[0] >= today)  # 结构化字段与正文写的不同（如 11-18 与 15 Nov）时取最早的
        if not future:
            return None, "已截止"
        deadline, quote = future[0]
        if _any(NOT_FUNDED, text):
            return None, "未写资助或自费"
        sal = re.search(r"(?:monthly gross salary|salary)[^.]{0,80}?(?:€|EUR|CHF)\s?[\d.,]+[^.]{0,30}", text, re.I) or \
            re.search(r"\d[\d.,\s]{2,8}\s?(?:€|euros?|EUR)\s*(?:gross|brut)[^.]{0,30}", text, re.I)
        return {
            "id": f"{name}:{jid}", "title": re.sub(r"\s+", " ", title)[:200], "url": url, "org": org,
            "country": country, "place": "", "level": level, "deadline": deadline, "quote": quote[:160],
            "funding_for": "", "amount": (sal.group(0).strip() if sal else "")[:200],
            "cn": cn_of(text), "flags": flags_of(text), "via": via,
        }, "收录"

    return urls, detail


# ───────────────────────── FindAPhD ─────────────────────────
# 云端机器的 IP 会被 Cloudflare 拦（403）；请在自己电脑上运行：
#   python scripts/collect_postings.py -s findaphd --save-samples 5
# 遵守 robots.txt（只读站点地图和单个项目页，不碰被禁止的搜索页），被拦就停，不做任何绕过。

FAP = "https://www.findaphd.com"
FAP_SITEMAP = FAP + "/sitemap.ashx?sitemap-projects-{n}.xml.gz"
FAP_LOC = re.compile(r"<loc>\s*(https://www\.findaphd\.com/phds/project/[^<\s]+?\?p(\d+))\s*</loc>")
FAP_DEADLINE = re.compile(r"(?:Application\s+)?Deadline:?\s*((?:\w+day,?\s+)?\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4}"
                          r"|[A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})", re.I)
FAP_DAY = re.compile(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})")
FAP_FUNDING = re.compile(r"(Funded PhD Project|Competition Funded PhD Project|Self-Funded PhD Students Only|"
                         r"Funded PhD Programme|PhD Research Project)\s*\(([^)]{3,60})\)", re.I)


def fap_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    import gzip

    def load(url: str) -> str:
        r = f.get(url)
        if "Just a moment" in r.text[:3000]:
            raise RuntimeError("被 Cloudflare 人机验证拦截，停止（不做绕过）")
        body = r.content
        return gzip.decompress(body).decode("utf-8", "replace") if body[:2] == b"\x1f\x8b" else r.text

    out: dict[str, str] = {}
    queue, seen = [FAP_SITEMAP.format(n=0)], set()
    while queue and len(seen) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        xml = load(url)
        if "<sitemapindex" in xml:  # 索引文件：继续读下一层的项目站点地图
            queue += [htmllib.unescape(u) for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml) if "projects" in u]
            continue
        found = FAP_LOC.findall(htmllib.unescape(xml))
        if not found and len(seen) == 1:
            print(f"[findaphd] 站点地图里没有项目链接：{xml[:800]!r}")
        for u, pid in found:
            out.setdefault(pid, u)
    return sorted(out.items(), key=lambda kv: -int(kv[0]))  # 新发布的项目（编号大）优先


def fap_detail(pid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    if "Just a moment" in raw[:3000]:
        raise RuntimeError("被 Cloudflare 人机验证拦截")
    ld = job_posting(raw)
    text = page_text(raw)
    title = page_text(ld.get("title") or "") or page_text((re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S) or [None, ""])[1])
    if re.search(r"Self-Funded PhD Students Only", text[:20000]):
        return None, "自费或竞争性资助"
    fund = FAP_FUNDING.search(text)
    if not fund:
        return None, "未写资助类型"
    kind, who = fund.group(1).lower(), fund.group(2)
    if kind.startswith(("self", "competition", "phd research")):
        return None, "自费或竞争性资助"
    # 截止信息紧挨在资助标签前面：具体日期，或 “Applications accepted all year round”
    head = text[max(0, fund.start() - 200):fund.start()]
    # 项目页在导师名后直接写截止日期，如 “Tuesday, February 02, 2027”
    dl = FAP_DAY.search(head) or FAP_DEADLINE.search(head)
    if dl:
        deadline, quote = parse_day(dl.group(1)), dl.group(0)
        if not deadline or deadline < today:
            return None, "已截止"
    elif "Applications accepted all year round" in head:
        posted = re.match(r"(\d{2})/(\d{2})/(\d{4})", str(ld.get("datePosted") or ""))
        posted = f"{posted.group(3)}-{posted.group(2)}-{posted.group(1)}" if posted else ""
        if not posted or (date.fromisoformat(today) - date.fromisoformat(posted)).days > 90:
            return None, "全年招生但发布超过 90 天"
        deadline, quote = "rolling", "Applications accepted all year round"
    else:
        return None, "页面无截止日期"
    cn = "yes" if re.search(r"worldwide|international", who, re.I) else "no" if re.search(r"only", who, re.I) else "check"
    org = ld.get("hiringOrganization") or {}
    loc = ld.get("jobLocation") or {}
    loc = loc[0] if isinstance(loc, list) and loc else loc
    country = ((loc.get("address") or {}).get("addressCountry") or "") if isinstance(loc, dict) else ""
    notes = re.search(r"Funding Notes?\s+(.{20,400}?)(?:\s+References|\s+How good is research|$)", text)
    return {
        "id": f"findaphd:{pid}",
        "title": re.sub(r"\s+", " ", title)[:200],
        "url": url,
        "org": (org.get("name") if isinstance(org, dict) else "") or "",
        "country": country_code(country),
        "place": "",
        "level": "phd",
        "deadline": deadline,
        "quote": quote,
        "funding_for": fund.group(0)[:120],
        "amount": re.sub(r"\s*\[?\bINSERT\b\]?", "", notes.group(1).strip() if notes else "")[:300],  # 平台模板没填的占位符
        "cn": cn,
        "flags": flags_of(text),
        "via": "FindAPhD",
    }, "收录"


ADAPTERS = {"jobs-ac-uk": (jac_urls, jac_detail), "academictransfer": (at_urls, at_detail),
            "findaphd": (fap_urls, fap_detail), "jobbnorge": (jn_urls, jn_detail), "varbi": (vb_urls, vb_detail),
            "inspire": (inspire_urls, inspire_detail), "ajo": (ajo_urls, ajo_detail), "daad": (daad_urls, daad_detail),
            **{k: madgex(k) for k in MADGEX}, **{k: institute(k) for k in INSTITUTES}}
HEADERS: dict[str, dict] = {}  # 个别接口要求的请求头（适配器名 → 请求头），如联邦劳动局的公开 clientId
_EXTRA_RANK: dict[str, int] = {}
# 新平台写在 scripts/platforms_*.py：各自导出 ADAPTERS，可选 HEADERS、VIA_RANK
for _mod in sorted(p.stem for p in (ROOT / "scripts").glob("platforms_*.py")):
    _mod = importlib.import_module(_mod)
    if not hasattr(_mod, "ADAPTERS"):  # 先导入了 platforms_*.py、它正在导入本模块：跳过（用法是先导入 collect_postings）
        continue
    ADAPTERS.update(_mod.ADAPTERS)
    HEADERS.update(getattr(_mod, "HEADERS", {}))
    _EXTRA_RANK.update(getattr(_mod, "VIA_RANK", {}))
# 只有 GitHub Actions 能访问的平台（适配器名 → 岗位的 via 名）：由公开仓库的 postings 工作流采集（-s actions），
# 每日任务再用 import_postings.py 并回主库；本地默认清单不含它们
ACTIONS = {"findaphd": "FindAPhD"}
DEFAULT = "jobs-ac-uk,academictransfer,naturecareers,sciencecareers,physicstoday,the-unijobs,jobbnorge,inspire,ajo,daad,varbi,ethz,inria,mpg,arbeitsagentur,workday,successfactors,oracle,pageup,cnrs,mathjobs,tamu-rwfm,hnet,aarhus,psi,eso,ibs,econjobmarket,university"


def expand(sources: str) -> list[str]:
    """'-s' 参数 → 适配器名列表：'default' 是本地清单，'actions' 是只能在 Actions 上采集的清单，可以和具体名字混写。"""
    out: list[str] = []
    for name in (n.strip() for n in sources.split(",")):
        names = DEFAULT.split(",") if name == "default" else list(ACTIONS) if name == "actions" else [name] if name else []
        for n in names:
            if n not in ADAPTERS:
                raise SystemExit(f"未知平台：{n}（可选：{', '.join(sorted(ADAPTERS))}，或 default / actions）")
            if n not in out:
                out.append(n)
    return out


# 同一岗位常在多个平台出现：机构 + 标题 + 截止日期相同视为同一个，只留信息最全的那条
VIA_RANK = {"jobs.ac.uk": 3, "AcademicTransfer": 3, "Nature Careers": 2, "Science Careers": 2, "Physics Today Jobs": 2, "THE Unijobs": 2, "Jobbnorge": 3, "INSPIRE-HEP Jobs": 2, "Academic Jobs Online": 2, "DAAD PhDGermany": 2, "Varbi": 3,
            "FindAPhD": 1, **_EXTRA_RANK}
TITLE_NOISE = re.compile(r"\b(phd|ph\.d|studentship|position|project|fully|funded|scholarship|the|a|an|in|on|of|for|and|with)\b|[^a-z0-9]+")


def dup_key(r: dict) -> tuple[str, str, str]:
    title = TITLE_NOISE.sub(" ", r["title"].lower())
    org = re.sub(r"\b(the|university|of|universit[yé]|college)\b|[^a-z]+", " ", r.get("org", "").lower())
    return (" ".join(title.split())[:80], " ".join(org.split())[:30], r["deadline"])


def dedupe(rows: list[dict]) -> tuple[list[dict], int]:
    best: dict[tuple, dict] = {}
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        k = dup_key(r)
        groups.setdefault(k, []).append(r)
    out = []
    for k, g in list(groups.items()):
        # 同一平台不会重复发同一岗位：同平台的同名岗位（如两个 “Postdoctoral Research Associate”）各自保留
        vias = [r.get("via") for r in g]
        if len(set(vias)) < len(vias):
            seen_via: set = set()
            first = []
            for r in g:
                if r.get("via") in seen_via:
                    out.append(r)
                else:
                    seen_via.add(r.get("via"))
                    first.append(r)
            g = first
        keep = max(g, key=lambda r: (VIA_RANK.get(r.get("via"), 0), sum(1 for v in r.values() if v)))
        cns = {r.get("cn") for r in g}
        keep = dict(keep, cn="no" if "no" in cns else "yes" if "yes" in cns else "check")  # 任一平台写明限本土就按限本土
        if len(g) > 1:
            keep["also"] = sorted({r["url"] for r in g if r is not keep and r["url"] != keep["url"]})
        out.append(keep)
    out = merge_across(out)
    return out, len(rows) - len(out)


# 第二遍：不同平台上标题足够具体、机构一致的岗位，截止日期不同也是同一个（平台各自写广告下架日）
GENERIC = re.compile(r"\b(post|doc|postdoc|postdoctoral|doctoral|research|researcher|associate|fellow|fellowship|scientist|scholar|"
                     r"student|candidate|positions?|opportunity|m|f|d|x|w|lab|laboratory|department|division|group)\b")


def specific_title(title: str) -> str:
    t = " ".join(TITLE_NOISE.sub(" ", title.lower()).split())
    return t if len(GENERIC.sub(" ", t).split()) >= 3 else ""


def org_words(org: str) -> set[str]:
    org = re.sub(r"\([^)]*\)", " ", org.lower())
    return set(re.sub(r"\b(the|university|universit[yé]|of|college|inc|e v|gmbh)\b|[^a-z]+", " ", org).split())


def same_org(a: str, b: str) -> bool:
    wa, wb = org_words(a), org_words(b)
    return bool(wa and wb) and (wa <= wb or wb <= wa or len(wa & wb) / len(wa | wb) >= 0.5)


def merge_across(rows: list[dict]) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for r in rows:
        k = specific_title(r["title"])
        by.setdefault(k, []).append(r)
    out = by.pop("", [])
    for g in by.values():
        while g:
            first, rest = g[0], g[1:]
            grp, vias = [first], {first.get("via")}
            for r in rest:
                if r.get("via") not in vias and same_org(first.get("org", ""), r.get("org", "")):
                    grp.append(r)
                    vias.add(r.get("via"))
            g = [r for r in rest if all(r is not x for x in grp)]
            if len(grp) == 1:
                out.append(first)
                continue
            # 留截止最早的那条（原句就在它自己的页面上），平台信息量作次序
            keep = min(grp, key=lambda r: (r["deadline"] == "rolling", r["deadline"], -VIA_RANK.get(r.get("via"), 0)))
            cns = {r.get("cn") for r in grp}
            keep = dict(keep, cn="no" if "no" in cns else "yes" if "yes" in cns else "check")
            urls = {u for r in grp for u in [r["url"], *(r.get("also") or [])]} - {keep["url"]}
            keep["also"] = sorted(urls)
            out.append(keep)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sources", default="default", help="逗号分隔的平台名；default = 本地清单，actions = 只能在 Actions 上采集的清单")
    ap.add_argument("--save-samples", type=int, default=0, help="把前 N 个详情页原文存到 research/inbox/samples/，便于调整解析规则")
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--max-pages", type=int, default=80)
    ap.add_argument("--max-details", type=int, default=3000)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dedupe-only", action="store_true", help="不采集，只对现有 _data/postings.yml 去重")
    args = ap.parse_args()
    if args.dedupe_only:
        rows, dropped = dedupe(yaml.safe_load(OUT.read_text(encoding="utf-8")) or [])
        OUT.write_text(yaml.safe_dump(sorted(rows, key=lambda r: (r["deadline"], r["id"])), allow_unicode=True,
                                      sort_keys=False, width=200), encoding="utf-8")
        print(f"去重：合并 {dropped} 条，剩 {len(rows)} 条")
        return 0
    f = Fetcher(delay=1.0)
    old = {r["id"]: r for r in (yaml.safe_load(OUT.read_text(encoding="utf-8")) or [])} if OUT.exists() else {}
    rows: dict[str, dict] = {k: v for k, v in old.items() if v["deadline"] == "rolling" or v["deadline"] >= args.today}
    for name in expand(args.sources):
        list_fn, detail_fn = ADAPTERS[name]
        try:
            urls = list_fn(f, args.max_pages)
        except Exception as e:  # noqa: BLE001
            print(f"[{name}] 列表失败：{e}")
            continue
        stats: dict[str, int] = {}
        for i, (jid, url) in enumerate(urls[: args.max_details]):
            try:
                raw = f.get(url, headers=HEADERS.get(name)).text
                if i < args.save_samples:
                    d = ROOT / "research" / "inbox" / "samples"
                    d.mkdir(parents=True, exist_ok=True)
                    (d / f"{name}-{jid}.html").write_text(raw, encoding="utf-8")
                row, why = detail_fn(jid, url, raw, args.today)
            except RuntimeError as e:  # 被人机验证拦截：整站停止
                print(f"[{name}] {e}")
                break
            except Disallowed:
                row, why = None, "robots 不允许"
            except Exception:  # noqa: BLE001
                row, why = None, "详情页失败"
            stats[why] = stats.get(why, 0) + 1
            if row:
                row["checked"] = args.today
                rows[row["id"]] = row
            elif why not in ("详情页失败", "robots 不允许"):  # 页面读到了但按现行规则不再收录（已截止、不再写资助等）：去掉旧记录
                rows.pop(f"{name}:{jid}", None)
        print(f"[{name}] 列表 {len(urls)} 个：{stats}")
    deduped, dropped = dedupe(list(rows.values()))
    print(f"去重：合并 {dropped} 条跨平台重复岗位")
    out = sorted(deduped, key=lambda r: (r["deadline"], r["id"]))
    print(f"岗位清单共 {len(out)} 条（中国学生可申 {sum(r['cn'] == 'yes' for r in out)} · 待确认 "
          f"{sum(r['cn'] == 'check' for r in out)} · 限本土 {sum(r['cn'] == 'no' for r in out)}）")
    if not args.dry_run:
        OUT.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
