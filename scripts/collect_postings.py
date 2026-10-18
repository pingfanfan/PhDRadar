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
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scrapers.common import Disallowed, Fetcher, _FUNDED, _RESTRICTED, _SCREENING, _SELF_FUNDED, _any  # noqa: E402

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
                        r"clinical training|teaching fellow|director|coordinator", re.I)


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
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s*,?\s+(\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    m = re.search(r"([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))).isoformat()
    return None


def level_of(title: str) -> str | None:
    if NOT_TARGET.search(title):
        return None
    if POSTDOC.search(title):
        return "postdoc"
    if PHD.search(title):
        return "phd"
    return None


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
           "TAIWAN": "TW", "ISRAEL": "IL", "QATAR": "QA", "SAUDI ARABIA": "SA", "UNITED ARAB EMIRATES": "AE"}


def country_code(raw: str) -> str:
    """JSON-LD 国家（ISO 代码或英文名）→ 本库地区代码；认不出就留空，不猜。"""
    raw = str(raw or "").strip().upper()
    if raw in COUNTRY:
        return COUNTRY[raw]
    return raw if len(raw) == 2 and raw.isalpha() else ""


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
    if _any(_SELF_FUNDED, title + " " + amount + " " + body[:3000]) or re.search(r"competition[\s-]funded", title + amount, re.I):
        return None, "自费或竞争性资助"
    if level == "phd" and not (funding_for or amount):
        return None, "未写资助"
    if level == "postdoc" and not salary:
        return None, "未写薪资"
    if level == "phd":
        cn = "yes" if re.search(r"International Students", funding_for) else "no" if funding_for else "check"
    else:
        cn = "no" if _any(_RESTRICTED, body[:6000]) else "check"
    if cn == "check" and _any(_RESTRICTED, body[:6000]):
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
        "flags": ["security-screening"] if _any(_SCREENING, body[:8000]) else [],
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
    org = ld.get("hiringOrganization") or {}
    return {
        "id": f"academictransfer:{jid}",
        "title": re.sub(r"\s+", " ", title)[:200],
        "url": url,
        "org": (org.get("name") if isinstance(org, dict) else "") or "",
        "country": "NL", "place": "",
        "level": level,
        "deadline": deadline,
        "quote": m.group(0),
        "funding_for": "",
        "amount": sm.group(1).strip()[:200],
        "cn": "no" if _any(_RESTRICTED, text) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, text) else [],
        "via": "AcademicTransfer",
    }, "收录"


# ───────────────────────── Nature Careers ─────────────────────────

NC_INDEX = "https://www.nature.com/naturecareers/sitemapindex.xml"
NC_JOB = re.compile(r"<loc>\s*(https://www\.nature\.com/naturecareers/job/(\d+)/([^<\s]*))\s*</loc>")
NC_SLUG = re.compile(r"phd|doctoral|doctorate|postdoc|post-doc|postdoctoral|studentship", re.I)


def nc_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for sm in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", f.get(NC_INDEX).text)[:max_pages]:
        for url, jid, slug in NC_JOB.findall(f.get(sm).text):
            if NC_SLUG.search(slug):
                out.setdefault(jid, url)
    return sorted(out.items(), key=lambda kv: -int(kv[0]))


def nc_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = page_text(h1.group(1)) if h1 else ""
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    m = re.search(r"Closing date\s+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})", text)
    if not m:
        return None, "页面无截止日期"
    deadline = parse_day(m.group(1).replace(m.group(1).split()[1], MONTH3.get(m.group(1).split()[1].lower()[:3], m.group(1).split()[1])))
    if not deadline or deadline < today:
        return None, "已截止"
    emp = re.search(r"Employer\s+(.{2,120}?)\s+Location\s", text)
    loc = re.search(r"Location\s+(.{2,120}?)\s+(?:Salary|Closing date)\s", text)
    sal = re.search(r"Salary\s+(.{1,120}?)\s+Closing date\s", text)
    body = text[m.end():m.end() + 8000]
    if _any(_SELF_FUNDED, title + " " + body) or (level == "phd" and not (sal or _any(_FUNDED, body))):
        return None, "未写资助或自费"
    return {
        "id": f"naturecareers:{jid}",
        "title": re.sub(r"\s+", " ", title)[:200],
        "url": url,
        "org": emp.group(1).strip() if emp else "",
        "country": "", "place": (loc.group(1).strip() if loc else "")[:80],
        "level": level,
        "deadline": deadline,
        "quote": m.group(0),
        "funding_for": "",
        "amount": (sal.group(1).strip() if sal else "")[:200],
        "cn": "no" if _any(_RESTRICTED, body) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, body) else [],
        "via": "Nature Careers",
    }, "收录"


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
        "amount": (notes.group(1).strip() if notes else "")[:300],
        "cn": cn,
        "flags": ["security-screening"] if _any(_SCREENING, text) else [],
        "via": "FindAPhD",
    }, "收录"


ADAPTERS = {"jobs-ac-uk": (jac_urls, jac_detail), "academictransfer": (at_urls, at_detail),
            "findaphd": (fap_urls, fap_detail), "naturecareers": (nc_urls, nc_detail)}
DEFAULT = "jobs-ac-uk,academictransfer,naturecareers"  # findaphd 需在本地电脑运行，不放进默认


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sources", default=DEFAULT)
    ap.add_argument("--save-samples", type=int, default=0, help="把前 N 个详情页原文存到 research/inbox/samples/，便于调整解析规则")
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--max-pages", type=int, default=80)
    ap.add_argument("--max-details", type=int, default=3000)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    f = Fetcher(delay=1.0)
    old = {r["id"]: r for r in (yaml.safe_load(OUT.read_text(encoding="utf-8")) or [])} if OUT.exists() else {}
    rows: dict[str, dict] = {k: v for k, v in old.items() if v["deadline"] == "rolling" or v["deadline"] >= args.today}
    for name in args.sources.split(","):
        list_fn, detail_fn = ADAPTERS[name]
        try:
            urls = list_fn(f, args.max_pages)
        except Exception as e:  # noqa: BLE001
            print(f"[{name}] 列表失败：{e}")
            continue
        stats: dict[str, int] = {}
        for i, (jid, url) in enumerate(urls[: args.max_details]):
            try:
                raw = f.get(url).text
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
        print(f"[{name}] 列表 {len(urls)} 个：{stats}")
    out = sorted(rows.values(), key=lambda r: (r["deadline"], r["id"]))
    print(f"岗位清单共 {len(out)} 条（中国学生可申 {sum(r['cn'] == 'yes' for r in out)} · 待确认 "
          f"{sum(r['cn'] == 'check' for r in out)} · 限本土 {sum(r['cn'] == 'no' for r in out)}）")
    if not args.dry_run:
        OUT.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
