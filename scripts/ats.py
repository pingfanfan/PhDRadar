#!/usr/bin/env python3
"""大学自己的招聘系统（ATS）：通用适配器 + 学校清单。

EURAXESS、Academic Positions 等聚合站上的岗位，大多转自大学自己的招聘系统；直接读源头，信息是第一手的。
只用网站允许的方式：所有请求走 Fetcher（robots.txt、Crawl-delay、真实 User-Agent），被拦就跳过该校，不做任何绕过。

每个系统是 (urls, detail) 两个函数，输出与 collect_postings.py 相同的岗位行；由 collect_postings.py 注册：

    python scripts/collect_postings.py -s workday,successfactors --dry-run

收录规则沿用 collect_postings.py：标题判定博士 / 博后（level_of），正文里找得到截止日期原句（find_deadline），
写明有资助（_FUNDED 或薪资），没有自费字样（_SELF_FUNDED）；明确限本土（_RESTRICTED）标 cn: no，否则 'check'。
"""
from __future__ import annotations

import html as htmllib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scrapers.common import Fetcher, _FUNDED, _RESTRICTED, _SCREENING, _SELF_FUNDED, _any

# ───────────────────────── 学校清单 ─────────────────────────
# 每所学校都先确认过：入口能访问、robots.txt 允许读取（2026-10-19 实测）。
# Workday：入口是 robots.txt 里列出的对外招聘站点地图（不收学生兼职、临时工、内部保密等站点）。
WORKDAY = [  # (学校, 站点地图, 国家)
    ("Aalto University", "https://aalto.wd3.myworkdayjobs.com/aalto/siteMap.xml", "FI"),
    ("Nanyang Technological University", "https://ntu.wd3.myworkdayjobs.com/Careers/siteMap.xml", "SG"),
    ("National University of Singapore", "https://nus.wd1.myworkdayjobs.com/Careers/siteMap.xml", "SG"),
    ("The University of Sydney", "https://usyd.wd105.myworkdayjobs.com/USYD_EXTERNAL_CAREER_SITE/siteMap.xml", "AU"),
    ("The University of Melbourne", "https://unimelb.wd105.myworkdayjobs.com/UoM_External_Career/siteMap.xml", "AU"),
    ("Monash University", "https://monash.wd105.myworkdayjobs.com/Monash/siteMap.xml", "AU"),
    ("The University of Queensland", "https://uq.wd3.myworkdayjobs.com/uqcareers/siteMap.xml", "AU"),
    ("Macquarie University", "https://mq.wd3.myworkdayjobs.com/CareersatMQ/siteMap.xml", "AU"),
    ("RMIT University", "https://rmit.wd3.myworkdayjobs.com/RMIT_Careers/siteMap.xml", "AU"),
    ("Flinders University", "https://flinders.wd3.myworkdayjobs.com/flinders_employment/siteMap.xml", "AU"),
    ("McGill University", "https://mcgill.wd3.myworkdayjobs.com/McGill_Careers/siteMap.xml", "CA"),
    ("University of Waterloo", "https://uwaterloo.wd3.myworkdayjobs.com/uw_careers/siteMap.xml", "CA"),
    ("University of Ottawa", "https://uottawa.wd3.myworkdayjobs.com/uOttawa_External_Career_Site/siteMap.xml", "CA"),
    ("The University of British Columbia", "https://ubc.wd10.myworkdayjobs.com/ubcfacultyjobs/siteMap.xml", "CA"),
    ("The University of British Columbia", "https://ubc.wd10.myworkdayjobs.com/ubcstaffjobs/siteMap.xml", "CA"),
    ("The University of Chicago", "https://uchicago.wd5.myworkdayjobs.com/External/siteMap.xml", "US"),
    ("University of Pennsylvania", "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/siteMap.xml", "US"),
    ("Washington University in St. Louis", "https://wustl.wd1.myworkdayjobs.com/External/siteMap.xml", "US"),
    ("University of Southern California", "https://usc.wd5.myworkdayjobs.com/ExternalUSCCareers/siteMap.xml", "US"),
    ("Penn State University", "https://psu.wd1.myworkdayjobs.com/PSU_Academic/siteMap.xml", "US"),
    ("University of Washington", "https://wd5.myworkdaysite.com/recruiting/uw/UWHires/siteMap.xml", "US"),
]
# SAP SuccessFactors 招聘站（Career Site Builder）：入口是站点根，岗位清单读 /sitemap.xml。
SUCCESSFACTORS = [  # (学校, 站点, 国家)
    ("EPFL", "https://careers.epfl.ch", "CH"),
    ("Ghent University", "https://jobs.ugent.be", "BE"),
    ("University of Helsinki", "https://jobs.helsinki.fi", "FI"),
    ("Delft University of Technology", "https://careers.tudelft.nl", "NL"),
]

# Oracle Recruiting Cloud：候选人站点的公开接口（站点本身无 robots.txt）。
ORACLE = [  # (学校, 主机, 站点编号, 国家)
    ("Technical University of Denmark (DTU)", "https://efzu.fa.em2.oraclecloud.com", "CX_1", "DK"),
    ("University of Southern Denmark (SDU)", "https://fa-eosd-saasfaprod1.fa.ocs.oraclecloud.com", "CX_1001", "DK"),
]
# PageUp：列表页 /en/listing/ 分页 + 岗位页 /en/job/<编号>/（microdata）。
PAGEUP = [  # (学校, 列表页, 国家)
    ("The University of Hong Kong", "https://jobs.hku.hk/en/listing/", "HK"),
    ("La Trobe University", "https://jobs.latrobe.edu.au/en/listing/", "AU"),
]

# 标题 / 链接里的博士、博后关键词（含芬兰语、荷兰语、法语、德语常见写法）
SLUG = re.compile(r"ph\.?d|doctoral|doctorate|doctorand|promovend|post-?doc|postdoctoral|post-doctoral|research-?fellow|"
                  r"research-?associate|väitöskirja|tohtori|doktorand|doctorant|studentship|scholarship", re.I)
SENIOR = re.compile(r"\b(senior|principal|lead|chief)\b", re.I)  # 高级研究员不是博后
# 除 _FUNDED 外，大学雇佣合同常见的薪资写法
PAY = _FUNDED + [r"\bremuneration\b", r"\bpay\s+(scale|grade|range|band|level)\b", r"\bsalary\s+(scale|range|band|grade)\b",
                 r"\b(gehalt|vergütung|entgelt|palkka|salaire|lohn)\b", r"\b(AUD|HKD|SGD|CHF|EUR|CAD|USD|DKK|SEK|NOK)\s?\$?\d",
                 r"[€$£]\s?\d{1,3}(?:[,.\s]\d{3})+", r"\b\d{1,3}(?:[,.\s]\d{3})+\s?(€|EUR|CHF|DKK|SEK|NOK)\b"]
AMOUNT = re.compile(r"(?:salary|stipend|remuneration|pay)[^.]{0,100}?(?:[€$£]|AUD|HKD|SGD|CHF|EUR|CAD|USD|DKK|SEK|NOK)\s?\$?"
                    r"\d[\d,.\s]*[^.]{0,40}", re.I)


# find_deadline 之外，大学招聘页常见的截止写法（如 DTU “must be submitted no later than 4 November 2026”）
EXTRA_KW = (r"(?:(?:submitted|received|apply|applications?)\s+(?:\w+\s+){0,3}?(?:no later than|by|before|on or before|until)|"
            r"(?:accepted|considered)\s+until|due date|last (?:application|closing) date|application period ends|"
            r"ansøgningsfrist|sista ansökningsdag|søknadsfrist|hakuaika päättyy|viimeinen hakupäivä)")
GAP = r"([^.\d]{0,60}?)"  # 关键词与日期之间的文字；含 start / begin 的是开始日期，不是截止
NOT_DEADLINE = re.compile(r"start|begin|commenc|from\b", re.I)
DATE_OF = r"(\d{1,2}(?:st|nd|rd|th)?\s+of\s+[A-Za-z]{3,9},?\s+\d{4})"  # “25th of October 2026”
NUM_DATE = r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})"  # “30/10/2026”“30-10-2026”：按 日/月/年 读，美国、加拿大的写法有歧义
DAY_MONTH = r"(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([A-Za-z]{3,9})\b(?!,?\s+\d{4})"  # 没写年份的 “1 November”


def deadline(text: str, end_date: str = "", country: str = "") -> tuple[str | None, str]:
    """截止日期 + 原句（正文里最先出现的那处）。end_date 是招聘系统里的结构化下架日期：原句只写日月时，与它相差 3 天内才借用它的年份。"""
    kw = rf"(?:{cp.DEADLINE_KW}|{EXTRA_KW})"
    found: list[tuple[int, str, str]] = []
    for m in re.finditer(kw + GAP + "(?:" + cp.ANY_DATE + "|" + DATE_OF + ")", text, re.I):
        if NOT_DEADLINE.search(m.group(1)):
            continue
        iso, _ = cp.find_deadline("deadline " + (m.group(2) or m.group(3).replace(" of ", " ").replace(",", "")))
        if iso:
            found.append((m.start(), iso, m.group(0).strip()))
    for m in re.finditer(kw + GAP + NUM_DATE, text, re.I):
        d, mo, y = (int(x) for x in m.groups()[-3:])
        if NOT_DEADLINE.search(m.group(1)) or mo > 12 or (d <= 12 and country in ("US", "CA")):  # 日月可互换且该国常用 月/日/年
            continue
        found.append((m.start(), f"{y}-{mo:02d}-{d:02d}", m.group(0).strip()))
    if found:
        return min(found)[1:]
    # UBC：“Posting End Date October 30, 2026 Note: Applications will be accepted until 11:59 PM on the Posting End Date.”
    if re.search(r"accepted until[^.]{0,30}posting end date", text, re.I):
        m = re.search(r"Posting End Date\s+" + cp.ANY_DATE, text)
        if m:
            return cp.find_deadline("deadline " + m.group(1))[0], m.group(0)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", end_date[:10]):
        from datetime import date
        end = date.fromisoformat(end_date[:10])
        for m in re.finditer(kw + r"[^.\d]{0,40}?" + DAY_MONTH, text, re.I):
            month = cp.MONTHS.get(cp.MONTH3.get(m.group(2).lower()[:3], m.group(2)).lower())
            if not month:
                continue
            for y in (end.year - 1, end.year, end.year + 1):
                try:
                    day = date(y, month, int(m.group(1)))
                except ValueError:
                    continue
                if abs((day - end).days) <= 3:
                    return day.isoformat(), m.group(0).strip()
    return None, ""


_SEEN: dict[tuple, str] = {}


def row(adapter: str, jid: str, url: str, title: str, org: str, country: str, place: str, text: str, via: str,
        today: str, end_date: str = "") -> tuple[dict | None, str]:
    """通用收录判断：博士 / 博后 + 截止原句 + 写明资助。text 是岗位正文（纯文本）。"""
    title = re.sub(r"\s+", " ", title).strip()
    level = None if SENIOR.search(title) else cp.level_of(title)
    # 只写 Research Associate / Research Fellow 的标题，正文要求博士学位才算博后（否则多是研究助理类职位）
    if level == "postdoc" and not re.search(r"post[\s-]?doc", title, re.I) and \
            not re.search(r"\bph\.?\s?d\b|doctoral degree|doctorate", text, re.I):
        level = None
    if not level:
        return None, "非博士/博后岗位"
    day, quote = deadline(text, end_date, country)
    if not day:
        return None, "页面无截止日期"
    if day < today:
        return None, "已截止"
    if _any(_SELF_FUNDED, title + " " + text):
        return None, "自费或竞争性资助"
    if not _any(PAY, text):
        return None, "未写资助"
    key = (adapter, org, title.lower(), day)
    if key in _SEEN and _SEEN[key] != jid:  # 同一岗位的另一语言版本（如赫尔辛基大学的芬兰语 / 英语页）
        return None, "重复（另一语言版本）"
    _SEEN[key] = jid
    amount = AMOUNT.search(text)
    return {
        "id": f"{adapter}:{jid}", "title": title[:200], "url": url, "org": org, "country": country,
        "place": place[:80], "level": level, "deadline": day, "quote": quote[:160], "funding_for": "",
        "amount": (amount.group(0).strip() if amount else "")[:200],
        "cn": "no" if _any(_RESTRICTED, text) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, text) else [], "via": via,
    }, "收录"


# ───────────────────────── Workday（*.myworkdayjobs.com） ─────────────────────────
# 站点地图列出全部在招岗位；岗位页是脚本渲染的，正文取自同一站点的公开岗位接口 /wday/cxs/<租户>/<站点>/job/...（robots 未禁止）。
# 截止日期只认正文里的原句；接口里的下架日期（endDate / validThrough）不当截止日期。

WD_LOC = re.compile(r"<loc>\s*([^<\s]+/job/[^<\s]+?_(R?[A-Za-z]*-?\d+)(?:-\d+)?)\s*</loc>")
_WD_SCHOOL: dict[str, tuple[str, str, str]] = {}  # 岗位 id → (学校, 国家, 公开岗位页)


def wd_api(url: str) -> str:
    """公开岗位页 → 岗位接口：https://t.wd3.myworkdayjobs.com/site/job/... → .../wday/cxs/t/site/job/..."""
    m = re.match(r"(https://([\w-]+)\.wd\d+\.myworkdayjobs\.com)/(?:[a-z]{2}-[A-Z]{2}/)?([\w-]+)(/job/.+)", url)
    if m:
        return f"{m.group(1)}/wday/cxs/{m.group(2)}/{m.group(3)}{m.group(4)}"
    m = re.match(r"(https://wd\d+\.myworkdaysite\.com)/recruiting/([\w-]+)/([\w-]+)(/job/.+)", url)
    return f"{m.group(1)}/wday/cxs/{m.group(2)}/{m.group(3)}{m.group(4)}" if m else url


def wd_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, sitemap, country in WORKDAY:
        try:
            xml = htmllib.unescape(f.get(sitemap).text)
        except Exception as e:  # noqa: BLE001 某校被拦或下线：跳过该校
            print(f"[workday] {school} 站点地图失败：{type(e).__name__}")
            continue
        tenant = re.search(r"//(?:([\w-]+)\.wd\d+\.myworkdayjobs\.com|wd\d+\.myworkdaysite\.com/recruiting/([\w-]+))", sitemap)
        tenant = (tenant.group(1) or tenant.group(2)) if tenant else "wd"
        for url, req in WD_LOC.findall(xml):
            if SLUG.search(url.rsplit("/", 1)[-1]):
                jid = f"{tenant}-{req}"
                if jid not in out:
                    out[jid] = wd_api(url)
                    _WD_SCHOOL[jid] = (school, country, url)
    return list(out.items())


def wd_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    import json
    try:
        info = json.loads(raw).get("jobPostingInfo") or {}
    except json.JSONDecodeError:
        info = {}
    if not info:
        return None, "页面无岗位数据"
    school, country, public = _WD_SCHOOL.get(jid, ("", "", url))
    return row("workday", jid, info.get("externalUrl") or public, info.get("title") or "", school,
               cp.country_code((info.get("country") or {}).get("descriptor")) or country, info.get("location") or "",
               cp.page_text(info.get("jobDescription") or ""), "Workday", today, info.get("endDate") or "")


# ───────────────────────── SAP SuccessFactors 招聘站（Career Site Builder） ─────────────────────────
# /sitemap.xml 列出在招岗位 /job/<地点-标题>/<编号>/；岗位页用 microdata（itemprop="title" / "description"）。

SF_LOC = re.compile(r"<loc>\s*(https://[^<\s]+/job/([^<\s/]+)/(\d+)/)\s*</loc>")
_SF_SCHOOL: dict[str, tuple[str, str]] = {}


def sf_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, base, country in SUCCESSFACTORS:
        try:
            xml = htmllib.unescape(f.get(base + "/sitemap.xml").text)
        except Exception as e:  # noqa: BLE001
            print(f"[successfactors] {school} 站点地图失败：{type(e).__name__}")
            continue
        host = base.split("//")[1].split(".")[-2]
        for url, slug, num in SF_LOC.findall(xml):
            if SLUG.search(slug):
                jid = f"{host}-{num}"
                out.setdefault(jid, url)
                _SF_SCHOOL[jid] = (school, country)
    return list(out.items())


def _itemprop(raw: str, name: str) -> str:
    m = re.search(rf'<(\w+)[^>]*itemprop="{name}"[^>]*>(.*?)</\1>', raw, re.S)
    if not m:
        m = re.search(rf'itemprop="{name}"[^>]*content="([^"]*)"', raw)
        return htmllib.unescape(m.group(1)) if m else ""
    return m.group(2)


def sf_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    school, country = _SF_SCHOOL.get(jid, ("", ""))
    title = cp.page_text(_itemprop(raw, "title"))
    d = raw.find('itemprop="description"')
    d = raw.find(">", d) + 1 if d >= 0 else -1
    text = cp.page_text(raw[d:d + 120000]) if d > 0 else cp.page_text(raw)
    place = cp.page_text(_itemprop(raw, "addressLocality") or _itemprop(raw, "streetAddress"))
    return row("successfactors", jid, url, title, school, country, place, text, "SuccessFactors", today)


# ───────────────────────── Oracle Recruiting Cloud（*.oraclecloud.com 候选人站点） ─────────────────────────
# 列表接口 recruitingCEJobRequisitions 按发布时间分页；详情接口 recruitingCEJobRequisitionDetails 给出完整正文。

ORC_LIST = "{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList" \
           "&finder=findReqs;siteNumber={site},limit=100,offset={offset},sortBy=POSTING_DATES_DESC"
ORC_DETAIL = "{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?expand=all&onlyData=true" \
             "&finder=ById;Id=%22{id}%22,siteNumber={site}"
_ORC: dict[str, tuple[str, str, str]] = {}  # 岗位 id → (学校, 国家, 公开岗位页)


def orc_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, host, site, country in ORACLE:
        try:
            for page in range(max_pages):
                items = f.get(ORC_LIST.format(host=host, site=site, offset=100 * page)).json()["items"]
                reqs = items[0].get("requisitionList") or [] if items else []
                for r in reqs:
                    if SLUG.search(r.get("Title") or ""):
                        jid = f"{site}-{host.split('//')[1].split('.')[0]}-{r['Id']}"
                        out[jid] = ORC_DETAIL.format(host=host, site=site, id=r["Id"])
                        _ORC[jid] = (school, country, f"{host}/hcmUI/CandidateExperience/en/sites/{site}/job/{r['Id']}")
                if len(reqs) < 100:
                    break
        except Exception as e:  # noqa: BLE001
            print(f"[oracle] {school} 列表失败：{type(e).__name__}")
    return list(out.items())


def orc_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    import json
    items = json.loads(raw).get("items") or []
    if not items:
        return None, "页面无岗位数据"
    d = items[0]
    school, country, public = _ORC.get(jid, ("", "", url))
    text = cp.page_text(" ".join(d.get(k) or "" for k in (
        "ExternalDescriptionStr", "ExternalResponsibilitiesStr", "ExternalQualificationsStr", "ShortDescriptionStr")))
    return row("oracle", jid, public, d.get("Title") or "", school, country, d.get("PrimaryLocation") or "", text,
               "Oracle Recruiting", today, d.get("ExternalPostedEndDate") or "")


# ───────────────────────── PageUp（*.pageuppeople.com 及学校自有域名） ─────────────────────────

PU_LINK = re.compile(r'href="((?:https://[^"/]+)?/en/job/(\d+)/([^"?#]*))"')
_PU: dict[str, tuple[str, str]] = {}


def pu_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, listing, country in PAGEUP:
        origin = "/".join(listing.split("/")[:3])
        f.host_delay[origin.split("//")[1]] = 4  # 访问稍快就会弹 AWS WAF 验证
        seen: set[str] = set()
        try:
            for page in range(1, max_pages + 1):
                found = PU_LINK.findall(f.get(f"{listing}?page={page}&page-items=200").text)
                if not {num for _, num, _ in found} - seen:  # 翻到底了（没有新岗位）
                    break
                for href, num, slug in found:
                    seen.add(num)
                    jid = f"{origin.split('//')[1]}-{num}"
                    if SLUG.search(slug):
                        out.setdefault(jid, href if href.startswith("http") else origin + href)
                        _PU[jid] = (school, country)
        except Exception as e:  # noqa: BLE001
            print(f"[pageup] {school} 列表失败：{type(e).__name__}")
    return list(out.items())


def pu_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    if "awsWafCookie" in raw[:3000]:
        return None, "被拦截（WAF 验证）"
    school, country = _PU.get(jid, ("", ""))
    title = cp.page_text(_itemprop(raw, "title"))
    d = raw.find('id="job-content"')
    e = raw.find('id="search-results"', d)
    text = cp.page_text(raw[d:e if e > d else d + 120000]) if d >= 0 else cp.page_text(raw)
    return row("pageup", jid, url, title, school, country, "", text, "PageUp", today)


ADAPTERS = {"workday": (wd_urls, wd_detail), "successfactors": (sf_urls, sf_detail), "oracle": (orc_urls, orc_detail),
            "pageup": (pu_urls, pu_detail)}
VIA_RANK = {"Workday": 3, "SuccessFactors": 3, "Oracle Recruiting": 3, "PageUp": 3}

import collect_postings as cp  # noqa: E402 放在末尾：collect_postings 末尾经 platforms_ats.py 导入本模块时，要先看到 ADAPTERS
