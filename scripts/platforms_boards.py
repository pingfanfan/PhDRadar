"""学科招聘板的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

- MathJobs.org（美国数学会，与 Academic Jobs Online 同一套系统）：一个 RSS 列出全部在招广告，岗位页上有 “Appl Deadline”。
  robots.txt 要求 Crawl-delay 5（Fetcher 自动遵守）。
- Texas A&M 自然资源招聘板（jobs.rwfm.tamu.edu）：生态 / 野生动物 / 林学的研究生助研与博后；岗位页有 “Application Deadline” 字段。
  无 robots.txt（404）。
- EconJobMarket（经济学）：只收 “Postdoctoral Scholar” 类型（博士生 / RA 市场需登录，不收）；岗位页有 “Application deadline: 10 Nov 2026”。
  robots.txt 全部允许。
- LINGUIST List（语言学）：“Support”（博士奖学金）与 “Jobs” 两个 RSS；公告页有 “Application Deadline: 15-Jan-2027” 字段。
  robots.txt 只禁止 AdsBot-Google 与 HTTrack。
- EGU Jobs（欧洲地球科学联合会招聘板）：岗位页有结构化字段 “Application deadline 3 November 2026” 与 “Salary”；
  robots.txt 只禁止 /admin/ 等后台路径。写 “Open until the position is filled” 的不收。
- ELLIS Jobs（欧洲 AI 研究网络）：岗位卡与详情页写 “Apply by 22/10/26” 和 “Career Stage: PhD|Postdoc”；robots.txt 全部允许。
- FENS Job Market（欧洲神经科学学会）：详情页有 “Position: … Deadline: 29 October 2026”；robots.txt 只禁止 /wp-admin/。
  正文写明没有截止日期（“no deadline”）的不收。
- H-Net Job Guide（人文社科）：岗位页有 “Closing Date” 字段；robots.txt 要求 Crawl-delay 5，首次访问需要保存 cookie（Session 自动处理）。
"""
from __future__ import annotations

import gzip
import html as htmllib
import re

import collect_postings as cp
from collect_postings import Fetcher, _any, _FUNDED, _SELF_FUNDED, level_of, page_text, parse_day, \
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
            v = htmllib.unescape(m.group(1).strip()) if m else ""
            try:  # 部分字段是双重编码的 UTF-8（“MÃ¼nster”）
                return v.encode("latin-1").decode("utf-8") if "Ã" in v else v
            except UnicodeError:
                return v
        jid, title = tag("ads:ID"), tag("title")
        if not jid or not level_of(title) or re.search(r"\bsummer\b", title, re.I) or not tag("ads:Deadline"):  # RSS 里没写截止的广告页面上也没有，不读
            continue
        cp._AJO["mj" + jid] = {"univ": tag("ads:Univ"), "dept": tag("ads:Dept"), "country": tag("ads:Country"),
                               "city": tag("ads:City"), "desc": tag("description")}
        out.append(("mj" + jid, f"https://www.mathjobs.org/jobs/list/{jid}"))
    return out


def mj_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    row, why = cp.ajo_detail(jid, url, raw, today)  # 页面结构与 AJO 相同
    if row:
        row.update(id=f"mathjobs:{jid[2:]}", via="MathJobs")
        if "Hong Kong" in row["org"] + row["place"]:
            row["country"] = "HK"
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
    title = head.partition(" at ")[0] if " at " in head else head  # 标题常写成 “… at 某大学”
    # 正文里标题后紧跟雇主名和单位类型括注：“… Purdue University Department of Forestry (State) Details”
    o = re.search(re.escape(head) + r"\s+([^|]{3,150}?)\s+\([A-Za-z /-]{2,25}\)\s+Details", text)
    org = o.group(1) if o else ""
    if not org:  # 雇主名在标题下的 <em> 里：“Texas A&M - Kingsville (State)”
        em = re.search(r"</h3>\s*<p>\s*<em>(.*?)</em>", raw, re.S)
        org = re.sub(r"\s*\([A-Za-z /-]{2,25}\)\s*$", "", page_text(em.group(1))) if em else ""
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
        "cn": cp.cn_of(body), "flags": cp.flags_of(body), "via": "TAMU Natural Resources Job Board",
    }, "收录"


# ───────────────────────── H-Net Job Guide ─────────────────────────

HNET = "https://networks.h-net.org"


def hnet_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    # robots.txt 写 Crawl-delay 5，但翻页稍快仍会回 429：放慢到 20 秒一次；中途被拒就停在已拿到的页
    f.host_delay["networks.h-net.org"] = 20
    seen: dict[str, str] = {}
    for page in range(max_pages):
        try:
            raw = f.get(f"{HNET}/jobs/browse?page={page}").text
        except Exception as e:  # noqa: BLE001
            print(f"[hnet] 第 {page + 1} 页被拒（{type(e).__name__}），保留已拿到的 {len(seen)} 条")
            break
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
        "amount": (pay.group(0).strip() if pay else "")[:200], "cn": cp.cn_of(body),
        "flags": cp.flags_of(body), "via": "H-Net Job Guide",
    }, "收录"


# ───────────────────────── EconJobMarket ─────────────────────────

EJM = "https://econjobmarket.org"
EJM_LIST = EJM + "/positions?position_type_id=6&excludePastDeadline=1&sortBy=ca"  # 6 = Postdoctoral Scholar，一页列全


def ejm_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    ids = dict.fromkeys(re.findall(r'name="position(\d+)"', f.get(EJM_LIST).text))
    return [(i, f"{EJM}/positions/{i}") for i in ids]


def ejm_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    head = re.search(r"Login/Register Translate this website (.{5,250}?) Advertiser:\s*(.{2,150}?) Field\(s\)", text)
    if not head or not re.search(r"Position type\(s\):[^:]{0,60}Postdoctoral Scholar", text):
        return None, "非博士/博后岗位"
    title, org = head.group(1), head.group(2)
    if not level_of(title) and not re.search(r"fellow|researcher|scholar", title, re.I):
        return None, "非博士/博后岗位"
    m = re.search(r"Application deadline:\s*(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})", text)
    if not m or m.group(2).lower() not in cp.MONTH3:
        return None, "页面无截止日期"
    deadline = parse_day(f"{m.group(1)} {cp.MONTH3[m.group(2).lower()]} {m.group(3)}")
    if not deadline or deadline < today:
        return None, "已截止"
    salary = re.search(r"Salary:\s*(.{2,80}?)\s+(?:Letters of reference|Application deadline)", text)
    loc = re.search(r"Location of job:\s*(.{2,150}?)\s+Degree required", text)
    place = loc.group(1) if loc else ""
    ad = text[m.end():m.end() + 8000]
    return {
        "id": f"econjobmarket:{jid}", "title": title[:200], "url": url, "org": org[:120],
        "country": cp.country_code(place.rsplit(",", 1)[-1]) if place else "", "place": place[:80], "level": "postdoc",
        "deadline": deadline, "quote": m.group(0), "funding_for": "", "amount": (salary.group(1) if salary else "")[:200],
        "cn": cp.cn_of(ad),
        "flags": cp.flags_of(ad), "via": "EconJobMarket",
    }, "收录"


# ───────────────────────── LINGUIST List ─────────────────────────

LL_FEEDS = ["https://linguistlist.org/issues/rss/support", "https://linguistlist.org/issues/rss/jobs"]


def ll_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for feed in LL_FEEDS:
        for title, link, vol, num in re.findall(r"<item>\s*<title>(.*?)</title>\s*<link>(https://linguistlist\.org/issues/(\d+)/(\d+)/)</link>",
                                                f.get(feed).text, re.S):
            if re.search(r"\bph\.?d\b|post-?doc|doctoral", htmllib.unescape(title), re.I):
                out.setdefault(f"{vol}-{num}", link)
    return list(out.items())


def ll_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    subj = re.search(r"Subject:\s*(.{5,250}?)\s+E-mail this message", text)
    title = subj.group(1) if subj else ""
    level = "postdoc" if re.search(r"post-?doc", title, re.I) else "phd" if re.search(r"\bph\.?d\b|doctoral", title, re.I) else None
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"Application Deadline:\s*(\d{1,2})-([A-Za-z]{3})-(\d{4})", text)
    if not m or m.group(2).lower() not in cp.MONTH3:
        return None, "页面无截止日期"
    deadline = parse_day(f"{m.group(1)} {cp.MONTH3[m.group(2).lower()]} {m.group(3)}")
    if not deadline or deadline < today:
        return None, "已截止"
    body = text[:m.start()]
    if _any(_SELF_FUNDED, body) or _any(cp.NOT_FUNDED, body) or \
            not (_any(_FUNDED, body) or re.search(r"stipends|funding|[$€£]\s?\d", body, re.I)):
        return None, "未写资助或自费"
    org = re.search(r"Institution/Organization:\s*(.{2,150}?)\s+(?:Department|Web Address|Level|Duties):", text)
    cur = r"(?:[$€£]|USD|EUR|GBP|CHF|CAD|AUD)"
    pay = re.search(rf"(?:salary|stipends?)[^.]{{0,80}}?{cur}\s?[\d,.]+[^.]{{0,40}}|{cur}\s?[\d,]{{5,}}[^.]{{0,40}}", body, re.I)
    return {
        "id": f"linguistlist:{jid}", "title": title[:200], "url": url, "org": (org.group(1) if org else "")[:120],
        "country": "", "place": "", "level": level, "deadline": deadline, "quote": m.group(0), "funding_for": "",
        "amount": (pay.group(0).strip() if pay else "")[:200], "cn": cp.cn_of(body),
        "flags": cp.flags_of(body), "via": "LINGUIST List",
    }, "收录"


# ───────────────────────── EGU Jobs ─────────────────────────

EGU = "https://www.egu.eu"


def egu_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for page in range(1, max_pages + 1):
        found = re.findall(r'href="(/jobs/(\d+)/([a-z0-9-]+)/)"', f.get(f"{EGU}/jobs/?limit=50&page={page}").text)
        for path, jid, slug in found:
            if jid not in seen and re.search(r"ph-?d|doctoral|doctorate|post-?doc|studentship", slug):
                seen[jid] = EGU + path
        if len({j for _, j, _ in found}) < 50:  # 每页 50 条，不满一页就是最后一页
            break
    return list(seen.items())


def egu_field(raw: str, label: str) -> str:
    m = re.search(rf'text-md-right">{label}</div>\s*<div class="col-md-9">(.*?)</div>', raw, re.S)
    return re.sub(r"\s+", " ", page_text(m.group(1))).strip() if m else ""


def egu_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    title = egu_field(raw, "Position")
    level = level_of(title) or ("postdoc" if re.search(r"post-?doc", title, re.I) else None)
    if not level:
        return None, "非博士/博后岗位"
    when = egu_field(raw, "Application deadline")
    deadline = parse_day(when)
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    salary = egu_field(raw, "Salary")
    text = page_text(raw)
    if _any(_SELF_FUNDED, text) or _any(cp.NOT_FUNDED, text) or not (re.search(r"\d", salary) or _any(_FUNDED, text)):
        return None, "未写资助或自费"
    emp = re.search(r'text-md-right">Employer</div>.*?<p>(.*?)</p>', raw, re.S)
    place = egu_field(raw, "Location")
    return {
        "id": f"egu:{jid}", "title": title[:200], "url": url, "org": (page_text(emp.group(1)) if emp else "")[:120],
        "country": place_country(place), "place": place[:80], "level": level, "deadline": deadline,
        "quote": f"Application deadline {when}", "funding_for": "", "amount": salary[:200],
        "cn": cp.cn_of(text), "flags": cp.flags_of(text), "via": "EGU Jobs",
    }, "收录"


# ───────────────────────── ELLIS Jobs ─────────────────────────

ELLIS = "https://ellis.eu"


def ellis_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for page in range(1, max_pages + 1):
        found = re.findall(r'href="(?:https://ellis\.eu)?(/research/jobs/(\d{4}-\d{2}-\d{2}-[a-z0-9-]+))"',
                           f.get(f"{ELLIS}/research/jobs?page={page}").text)
        new = [(p, slug) for p, slug in dict.fromkeys(found) if slug not in seen]
        for path, slug in new:
            if re.search(r"ph-?d|doctoral|post-?doc", slug):
                seen[slug] = ELLIS + path
        if not new:
            break
    return list(seen.items())


def ellis_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"\s+", " ", page_text(h1.group(1))).strip() if h1 else ""
    text = page_text(raw)
    stage = re.search(r"Career Stage:\s*(PhD|Postdoc)\b", text)
    if not stage:
        return None, "非博士/博后岗位"
    m = re.search(r"Apply by (\d{2})/(\d{2})/(\d{2})\b", text)
    if not m:
        return None, "页面无截止日期"
    deadline = f"20{m.group(3)}-{m.group(2)}-{m.group(1)}"
    if deadline < today:
        return None, "已截止"
    body = text[stage.end():]
    if _any(_SELF_FUNDED, body) or _any(cp.NOT_FUNDED, body) or not (_any(_FUNDED, body) or re.search(r"fully funded|funded position", body, re.I)):
        return None, "未写资助或自费"
    org = re.search(r"\bat (?:the )?(.{3,100})$", title)
    return {
        "id": f"ellis:{jid[:60]}", "title": title[:200], "url": url, "org": (org.group(1) if org else "")[:120], "country": "",
        "place": "", "level": "postdoc" if stage.group(1) == "Postdoc" else "phd", "deadline": deadline, "quote": m.group(0),
        "funding_for": "", "amount": "", "cn": cp.cn_of(body), "flags": cp.flags_of(body), "via": "ELLIS Jobs",
    }, "收录"


# ───────────────────────── FENS Job Market ─────────────────────────

FENS = "https://www.fens.org/careers/job-market"


def fens_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for page in range(1, max_pages + 1):
        ids = dict.fromkeys(re.findall(r"/careers/job-market/job/(\d+)", f.get(FENS if page == 1 else f"{FENS}/page/{page}").text))
        new = [i for i in ids if i not in seen]
        for i in new:
            seen[i] = f"{FENS}/job/{i}"
        if not new:
            break
    return list(seen.items())


def fens_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    head = re.search(r"Job ID: \d+ (.{5,250}?) Position: (.{3,60}?) Deadline: ([A-Za-z0-9 ,]{6,30}?) (?=[A-Z][a-z]+(?: [A-Z][a-z]+)*:)", text)
    if not head:
        return None, "页面无截止日期"
    title, position, when = head.group(1), head.group(2), head.group(3)
    level = "postdoc" if re.search(r"post-?doc", position, re.I) else "phd" if re.search(r"ph\.?\s?d", position, re.I) else None
    if not level:
        return None, "非博士/博后岗位"
    body = text[head.end():]
    if re.search(r"\bno (?:application )?deadline\b", body, re.I):  # 字段写了日期、正文却说没有截止：不收
        return None, "页面无截止日期"
    deadline = parse_day(when)
    if not deadline:
        return None, "页面无截止日期"
    if deadline < today:
        return None, "已截止"
    if _any(_SELF_FUNDED, body) or _any(cp.NOT_FUNDED, body) or (level == "phd" and not _any(_FUNDED, body)):  # 博后是雇佣岗位
        return None, "未写资助或自费"
    inst = re.search(r"Institution:\s*(.{2,120}?)\s+Department:", text)
    country = re.search(r"Country:\s*([A-Z][A-Za-z ]{2,40}?)\s+Institution:", text)
    city = re.search(r"City:\s*(.{2,60}?)\s+Country:", text)
    return {
        "id": f"fens:{jid}", "title": title[:200], "url": url, "org": (inst.group(1) if inst else "")[:120],
        "country": cp.country_code(country.group(1)) if country else "", "place": (city.group(1) if city else "")[:80],
        "level": level, "deadline": deadline, "quote": f"Deadline: {when}", "funding_for": "", "amount": "",
        "cn": cp.cn_of(body), "flags": cp.flags_of(body), "via": "FENS Job Market",
    }, "收录"


ADAPTERS = {"mathjobs": (mj_urls, mj_detail), "tamu-rwfm": (tamu_urls, tamu_detail), "hnet": (hnet_urls, hnet_detail),
            "econjobmarket": (ejm_urls, ejm_detail), "linguistlist": (ll_urls, ll_detail),
            "egu": (egu_urls, egu_detail), "ellis": (ellis_urls, ellis_detail), "fens": (fens_urls, fens_detail)}
VIA_RANK = {"MathJobs": 2, "TAMU Natural Resources Job Board": 2, "H-Net Job Guide": 2, "EconJobMarket": 2, "LINGUIST List": 2, "EGU Jobs": 2, "ELLIS Jobs": 1, "FENS Job Market": 2}
