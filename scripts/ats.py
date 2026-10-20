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
from scrapers.common import Fetcher, _FUNDED, _SELF_FUNDED, _any

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
    ("Murdoch University", "https://murdoch.wd3.myworkdayjobs.com/MurdochCareers/siteMap.xml", "AU"),
    ("Australian Catholic University", "https://acu.wd108.myworkdayjobs.com/ACUCareers/siteMap.xml", "AU"),
    ("Carleton University", "https://carleton.wd1.myworkdayjobs.com/CarletonCareers/siteMap.xml", "CA"),
    ("EMBL", "https://embl.wd103.myworkdayjobs.com/EMBL/siteMap.xml", "DE"),
]
# SAP SuccessFactors 招聘站（Career Site Builder）：入口是站点根，岗位清单读 /sitemap.xml。
SUCCESSFACTORS = [  # (学校, 站点, 国家)
    ("EPFL", "https://careers.epfl.ch", "CH"),
    ("Ghent University", "https://jobs.ugent.be", "BE"),
    ("University of Helsinki", "https://jobs.helsinki.fi", "FI"),
    ("Delft University of Technology", "https://careers.tudelft.nl", "NL"),
    ("University of Basel", "https://careers.unibas.ch", "CH"),
    ("University of Vienna", "https://jobs.univie.ac.at", "AT"),
    ("Freie Universität Berlin", "https://jobs.fu-berlin.de", "DE"),
    ("University of Stuttgart", "https://careers.uni-stuttgart.de", "DE"),
    ("Vrije Universiteit Brussel", "https://jobs.vub.be", "BE"),
    ("UCLouvain", "https://jobs.uclouvain.be", "BE"),
    ("National University of Singapore", "https://careers.nus.edu.sg", "SG"),
    ("Singapore University of Technology and Design", "https://careers.sutd.edu.sg", "SG"),
    ("A*STAR", "https://careers.a-star.edu.sg", "SG"),
    ("CSIRO", "https://jobs.csiro.au", "AU"),
    ("University of Toronto", "https://jobs.utoronto.ca", "CA"),
    ("Fraunhofer-Gesellschaft", "https://jobs.fraunhofer.de", "DE"),
]

# Oracle Recruiting Cloud：候选人站点的公开接口（站点本身无 robots.txt）。
ORACLE = [  # (学校, 主机, 站点编号, 国家)
    ("Technical University of Denmark (DTU)", "https://efzu.fa.em2.oraclecloud.com", "CX_1", "DK"),
    ("University of Southern Denmark (SDU)", "https://fa-eosd-saasfaprod1.fa.ocs.oraclecloud.com", "CX_1001", "DK"),
    ("The University of Edinburgh", "https://elxw.fa.em3.oraclecloud.com", "CX_1001", "UK"),
    ("University of Alberta", "https://iaejup.fa.ocs.oraclecloud.com", "UOA-Careers", "CA"),
]
# PageUp：列表页 /en/listing/ 分页 + 岗位页 /en/job/<编号>/（microdata）。
PAGEUP = [  # (学校, 列表页, 国家)
    ("The University of Hong Kong", "https://jobs.hku.hk/en/listing/", "HK"),
    ("La Trobe University", "https://jobs.latrobe.edu.au/en/listing/", "AU"),
]

# ReachMee：学校页面里嵌入的外部招聘站（参数取自学校页面引用的 customerjs 脚本）。
REACHMEE = [  # (学校, 站点, 查询参数, 国家)
    ("Chalmers University of Technology", "https://web103.reachmee.com/ext/I003/304",
     "site=5&lang=UK&validator=a72aeedd63ec10de71e46f8d91d0d57c", "SE"),
]

# 学校自建的招聘页：列表页上的岗位链接 + 岗位页（标题取 <h1>）。
LISTS = [  # (学校, 列表页或站点地图, 岗位链接正则：(路径, 编号), 链接前缀, 国家[, 标题正则（默认取 <h1>）])
    ("University of Copenhagen", "https://employment.ku.dk/all-vacancies/", r'href="(/all-vacancies/\?show=(\d+))"',
     "https://employment.ku.dk", "DK"),
    # 理大研究岗位表格：整行可点（data-href），岗位页的 <h1> 是“Post Specification”，标题在 <title>
    ("The Hong Kong Polytechnic University", "https://jobs.polyu.edu.hk/research.php",
     r'data-href="(job_detail\.php\?job=(\d+))"', "https://jobs.polyu.edu.hk/", "HK",
     r"<title>\s*Job Application - (.*?)</title>"),
    ("University of Cambridge", "https://www.cam.ac.uk/jobs/search", r'href="(/jobs/[a-z0-9-]+-([a-z]{2}\d{5}))"',
     "https://www.cam.ac.uk", "UK"),
    # ANU 新版 PageUp 招聘页：robots.txt 允许岗位页（Crawl-delay 5），清单读站点地图
    ("Australian National University", "https://jobs.anu.edu.au/sitemap.xml",
     r"<loc>https://jobs\.anu\.edu\.au(/jobs/([a-z0-9-]+))</loc>", "https://jobs.anu.edu.au", "AU"),
    ("University of Antwerp", "https://www.uantwerpen.be/en/jobs/vacancies/academic-staff/",
     r'href="(\?q=(\d+)&(?:amp;)?descr=[^"]+)"', "https://www.uantwerpen.be/en/jobs/vacancies/academic-staff/", "BE"),
    ("Copenhagen Business School", "https://www.cbs.dk/en/about-cbs/job-and-career/vacant-positions",
     r'href="(/en/about-cbs/job-and-career/vacant-positions/([a-z0-9-]+))"', "https://www.cbs.dk", "DK"),
    ("University of Tartu", "https://ut.ee/en/academic-job-offers", r'href="(/en/job-offer/([a-z0-9-]+))"', "https://ut.ee", "EE"),
    ("SISSA", "https://www.sissa.it/recruitment", r'href="(/bandi/([a-z0-9-]+))"', "https://www.sissa.it", "IT"),
    ("Institut Pasteur", "https://research.pasteur.fr/en/wp-sitemap-posts-job-1.xml",
     r"<loc>https://research\.pasteur\.fr(/en/job/([a-z0-9-]+)/)</loc>", "https://research.pasteur.fr", "FR"),
    # Teamtailor 招聘站：robots.txt 只禁 /app/ 等后台路径
    ("IRB Barcelona", "https://recruitment.irbbarcelona.org/sitemap.xml",
     r"<loc>https://recruitment\.irbbarcelona\.org(/jobs/(\d+)-[a-z0-9-]+)</loc>", "https://recruitment.irbbarcelona.org", "ES"),
    # nCore：robots.txt 禁止 / 但允许 /jobposition/ 与 /sitemap
    ("Istituto Italiano di Tecnologia", "https://app.ncoreplat.com/sitemap.xml",
     r"<loc>https://app\.ncoreplat\.com(/jobposition/(\d+)/[a-z0-9-]+/istituto-italiano-di-tecnologia)</loc>",
     "https://app.ncoreplat.com", "IT"),
    # b-ite 招聘站：站点地图只有哈希链接，(?#全部) 表示不按链接文字筛选，逐个读岗位页
    ("LMU Munich", "https://job-portal.lmu.de/sitemap.xml.gz",
     r"(?#全部)<loc>https://job-portal\.lmu\.de(/jobposting/([0-9a-f]+))</loc>", "https://job-portal.lmu.de", "DE"),
    ("Universität Hamburg", "https://stellen.uni-hamburg.de/sitemap.xml.gz",
     r"(?#全部)<loc>https://stellen\.uni-hamburg\.de(/jobposting/([0-9a-f]+))</loc>", "https://stellen.uni-hamburg.de", "DE"),
    ("Forschungszentrum Jülich", "https://recruiting.fz-juelich.de/sitemap.xml.gz",
     r"(?#全部)<loc>https://recruiting\.fz-juelich\.de(/jobposting/([0-9a-f]+))</loc>", "https://recruiting.fz-juelich.de", "DE"),
    # d.vinci 招聘站
    ("Karlsruhe Institute of Technology (KIT)", "https://jobs.pse.kit.edu/sitemap.xml",
     r"<loc>https://jobs\.pse\.kit\.edu(/en/jobs/(\d+)/[a-z0-9-]+)</loc>", "https://jobs.pse.kit.edu", "DE"),
    ("German Cancer Research Center (DKFZ)", "https://jobs.dkfz.de/sitemap.xml",
     r"<loc>https://jobs\.dkfz\.de(/en/jobs/(\d+)/[a-z0-9-]+)</loc>", "https://jobs.dkfz.de", "DE"),
    # Refline（ETH 领域研究所）：robots.txt 允许
    *[(name, f"https://apply.refline.ch/{cid}/search.html?form.buttons.listAll=1&lang=en",
       rf'href="https://apply\.refline\.ch(/({cid}/\d+)/pub/\d+/index\.html)"', "https://apply.refline.ch", "CH")
      for name, cid in (("Paul Scherrer Institute (PSI)", 673278), ("Eawag", 673277), ("Empa", 673276), ("WSL", 273855))],
    ("Technical University of Munich (TUM)", "https://portal.mytum.de/jobs/asRss",
     r"<link>https://portal\.mytum\.de(/jobs/wissenschaftler/(NewsArticle_\d+_\d+))</link>", "https://portal.mytum.de", "DE"),
    ("RWTH Aachen University", [f"https://www.rwth-aachen.de/cms/root/wir/Karriere/~buym/RWTH-Jobportal/?page={n}" for n in range(1, 5)],
     r'href="(/go/id/kbag/file/(V\d+)/)"', "https://www.rwth-aachen.de", "DE"),
    ("Leibniz Association", "https://www.leibniz-gemeinschaft.de/en/careers/jobs",
     r'href="(/en/careers/jobs/detail/job/show/Job/([a-z0-9-]+))"', "https://www.leibniz-gemeinschaft.de", "DE"),
    ("Helmholtz-Zentrum Dresden-Rossendorf (HZDR)", ["https://www.hzdr.de/db/!JobList?pNid=490&pSelCat=6",
                                                     "https://www.hzdr.de/db/!JobList?pNid=490&pSelCat=14"],
     r'href="(Cms\?pNid=490&(?:amp;)?pOid=(\d+)&(?:amp;)?pContLang=en)"', "https://www.hzdr.de/db/", "DE", r"<title>(.*?)</title>"),
    ("Medical University of Vienna", "https://www.meduniwien.ac.at/web/karriere/offene-stellen/",
     r'href="(/web/karriere/offene-stellen/personalmitteilungsblatt-[^"]*kennzahl-(\d+)/\d+/)"', "https://www.meduniwien.ac.at", "AT",
     r"<h2[^>]*>(.*?)</h2>"),
    ("University of Innsbruck", "https://lfuonline.uibk.ac.at/public/karriereportal.home?lang=de",
     r'href="https://lfuonline\.uibk\.ac\.at(/public/karriereportal\.details\?asg_id_in=(\d+))"', "https://lfuonline.uibk.ac.at", "AT",
     r"<title>(.*?)</title>"),
    ("WU Vienna", "https://jobs.wu.ac.at/job-offers.html", r'href="https://jobs\.wu\.ac\.at(/[A-Za-z0-9-]+-j(\d+)\.html)"',
     "https://jobs.wu.ac.at", "AT"),
    ("GFZ Helmholtz Centre for Geosciences", "https://www.gfz.de/en/career/job-offers",
     r'href="(/en/career/job-offers/details/(\d+))"', "https://www.gfz.de", "DE", r"<title>(.*?)(?::\s*GFZ)?</title>"),
    # INRAE：站点地图只有编号链接（/ot-<n>），多数是实习，按岗位页标题筛
    ("INRAE", "https://jobs.inrae.fr/sitemap.xml", r"(?#全部)<loc>https://jobs\.inrae\.fr(/(ot-\d+))</loc>", "https://jobs.inrae.fr", "FR"),
    ("University of Bologna", "https://bandi.unibo.it/ricerca/incarichi-post-doc/RSS",
     r'rdf:about="https://bandi\.unibo\.it(/s/apos7/([a-z0-9-]+))"', "https://bandi.unibo.it", "IT"),
    # prospective.ch 公开接口（JSON 里的 directlink 指向学校招聘页）
    ("University of Zurich", "https://ohws.prospective.ch/public/v1/medium/1002007/jobs?lang=en&offset=0&limit=500",
     r'"directlink"\s*:\s*"https://jobs\.uzh\.ch(/job-vacancies/([a-z0-9-]+/[0-9a-f-]+))"', "https://jobs.uzh.ch", "CH"),
]

# 标题 / 链接里的博士、博后关键词（含芬兰语、荷兰语、法语、德语常见写法）
SLUG = re.compile(r"ph\.?d|doctoral|doctorate|doctorand|promovend|post-?doc|postdoctoral|post-doctoral|research-?fellow|"
                  r"research-?associate|väitöskirja|tohtori|doktorand|doctorant|doctorat|studentship|scholarship|"
                  r"pr(?:a|ä|ae)-?doc|pre-?doc|promotion|wissenschaftliche", re.I)
# level_of 认不出的其他语言写法：奥地利的 prae doc（博士生职位）、德语 Doktorand / Promotion、法语 doctorant
LEVEL_PHD = re.compile(r"pr(?:a|ä|ae|e)[\s-]?doc|doktorand|promotion|doctorant|doctorat|väitöskirjatutkija", re.I)
LEVEL_POSTDOC = re.compile(r"postdoktorand|post[\s-]?doc", re.I)
WIMI = re.compile(r"wiss(?:\.|enschaftlich\w*)\s*(?:/r|\*r|:r)?\s*Mitarbeiter", re.I)
SENIOR = re.compile(r"\b(senior|principal|lead|chief)\b|part[\s-]time", re.I)  # 高级研究员不是博后；兼职岗位不收
# 除 _FUNDED 外，大学雇佣合同常见的薪资写法
PAY = _FUNDED + [r"\b(full[\s-]time|temporary|fixed[\s-]term)\s+(employment|contract)\b", r"\bremuneration\b", r"\bpay\s+(scale|grade|range|band|level)\b", r"\bsalary\s+(scale|range|band|grade)\b",
                 r"\b(gehalt|vergütung|entgelt|palkka|salaire|lohn|rémunération|compenso|importo|retribuzione|salario|retribución)\b", r"\b(AUD|HKD|SGD|CHF|EUR|CAD|USD|DKK|SEK|NOK)\s?\$?\d",
                 r"[€$£]\s?\d{1,3}(?:[,.\s]\d{3})+", r"\b\d{1,3}(?:[,.\s]\d{3})+\s?(€|EUR|CHF|DKK|SEK|NOK)\b"]
AMOUNT = re.compile(r"(?:salary|stipend|remuneration|pay)[^.]{0,100}?(?:[€$£]|AUD|HKD|SGD|CHF|EUR|CAD|USD|DKK|SEK|NOK)\s?\$?"
                    r"\d[\d,.\s]*[^.]{0,40}", re.I)


# find_deadline 之外，大学招聘页常见的截止写法（如 DTU “must be submitted no later than 4 November 2026”）
EXTRA_KW = (r"(?:(?:submitted|received|apply|applications?)\s+(?:\w+\s+){0,3}?(?:no later than|by|before|on or before|until)|"
            r"apply for this (?:vacancy|position)[^.]{0,100}?(?:until|up to and including|before|by)|(?:accepted|considered)\s+until|due date|bewerbungsende|closing at|closes on|last (?:application|closing) date|application period ends|"
            r"ansøgningsfrist|sista ansökningsdag|søknadsfrist|hakuaika päättyy|viimeinen hakupäivä|"
            r"scadenza|date limite|ouvert jusqu'au|fecha l[ií]mite|plazo de (?:solicitud|presentaci[oó]n))")
# 法语、意大利语、西班牙语月份 → 英文（德语月份 find_deadline 自己会换）
ROMANCE_MONTHS = {"janvier": "January", "février": "February", "fevrier": "February", "mars": "March", "avril": "April",
                  "mai": "May", "juin": "June", "juillet": "July", "août": "August", "aout": "August", "septembre": "September",
                  "octobre": "October", "novembre": "November", "décembre": "December", "decembre": "December",
                  "gennaio": "January", "febbraio": "February", "marzo": "March", "aprile": "April", "maggio": "May",
                  "giugno": "June", "luglio": "July", "agosto": "August", "settembre": "September", "ottobre": "October",
                  "dicembre": "December", "enero": "January", "febrero": "February", "abril": "April", "mayo": "May",
                  "junio": "June", "julio": "July", "septiembre": "September", "octubre": "October", "noviembre": "November",
                  "diciembre": "December"}
GAP = r"([^.\d]{0,60}?)"  # 关键词与日期之间的文字；含 start / begin 的是开始日期，不是截止
NOT_DEADLINE = re.compile(r"start|begin|commenc|from\b", re.I)
DATE_OF = r"(\d{1,2}(?:st|nd|rd|th)?\s+of\s+[A-Za-z]{3,9},?\s+\d{4})"  # “25th of October 2026”
NUM_DATE = r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})"  # “30/10/2026”“11/30/2026”：日月顺序看同页其他日期，判断不了就不收


def num_order(text: str) -> str:
    """页面上数字日期的顺序：有一处首位 > 12 → 'MDY'（如 SuccessFactors 英文界面 “12/15/2026”），次位 > 12 → 'DMY'；矛盾或看不出 → ''。"""
    orders = {"DMY" if int(a) > 12 else "MDY" for a, b in re.findall(r"\b(\d{1,2})[/-](\d{1,2})[/-]\d{4}\b", text)
              if int(a) > 12 or int(b) > 12} - {""}
    return orders.pop() if len(orders) == 1 else ""
DAY_MONTH = r"(?:(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([A-Za-z]{3,9})|([A-Za-z]{3,9})\s+(\d{1,2})(?:st|nd|rd|th)?)\b(?!,?\s+\d{4})"  # 没写年份的 “1 November”“November 20”


def deadline(text: str, end_date: str = "", order_hint: str = "") -> tuple[str | None, str]:
    """截止日期 + 原句（正文里最先出现的那处）。end_date 是招聘系统里的结构化下架日期：原句只写日月时，与它相差 3 天内才借用它的年份。"""
    text = re.sub(r"(\d)\s+(st|nd|rd|th)\b", r"\1\2", text)  # “November 12 th 2026”
    kw = rf"(?:{cp.DEADLINE_KW}|{EXTRA_KW})"
    found: list[tuple[int, str, str]] = []
    for m in re.finditer(kw + GAP + "(?:" + cp.ANY_DATE + "|" + DATE_OF + ")", text, re.I):
        if NOT_DEADLINE.search(m.group(1)):
            continue
        day = m.group(2) or m.group(3).replace(" of ", " ").replace(",", "")
        day = re.sub(r"[A-Za-zÀ-ÿ]+", lambda w: ROMANCE_MONTHS.get(w.group(0).lower().rstrip("."), w.group(0)), day)
        iso, _ = cp.find_deadline("deadline " + day)
        if iso:
            found.append((m.start(), iso, m.group(0).strip()))
    order = num_order(text) or order_hint
    for m in re.finditer(kw + GAP + NUM_DATE, text, re.I):
        d, mo, y = (int(x) for x in m.groups()[-3:])
        if order == "MDY":
            d, mo = mo, d
        if NOT_DEADLINE.search(m.group(1)) or not order or mo > 12 or d > 31:
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
            dd, mon = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
            month = cp.MONTHS.get(cp.MONTH3.get(mon.lower()[:3], mon).lower())
            if not month:
                continue
            for y in (end.year - 1, end.year, end.year + 1):
                try:
                    day = date(y, month, int(dd))
                except ValueError:
                    continue
                if abs((day - end).days) <= 3:
                    return day.isoformat(), m.group(0).strip()
    return None, ""


_SEEN: dict[tuple, str] = {}
REF = re.compile(r"\b(?:Job ID|Stellen ID|Reference(?: number)?|Referenz|Anf\.-Kennung|Kennziffer)\s*:?\s*([A-Z]{0,4}-?\d{3,})")


def row(adapter: str, jid: str, url: str, title: str, org: str, country: str, place: str, text: str, via: str,
        today: str, end_date: str = "", order_hint: str = "") -> tuple[dict | None, str]:
    """通用收录判断：博士 / 博后 + 截止原句 + 写明资助。text 是岗位正文（纯文本）。"""
    title, text = re.sub(r"\s+", " ", title.replace("\xad", "")).strip(), text.replace("\xad", "")  # 去掉软连字符
    level = None if SENIOR.search(title) else cp.level_of(title) or \
        (None if cp.NOT_TARGET.search(title) else "postdoc" if LEVEL_POSTDOC.search(title) else
         "phd" if LEVEL_PHD.search(title) else None)
    # 德国常见的“Wissenschaftliche/r Mitarbeiter/in”：正文要求已完成博士 → 博后；写明可以读博（Promotion）→ 博士
    if not level and WIMI.search(title) and not cp.NOT_TARGET.search(title):
        level = "postdoc" if re.search(r"abgeschlossene[nr]?\s+Promotion|\bpromoviert|Doktortitel|completed\s+(?:a\s+)?(?:PhD|doctorate)|"
                                       r"PhD\s+(?:degree\s+)?(?:is\s+)?required", text, re.I) else \
            "phd" if re.search(r"(?:Möglichkeit|Gelegenheit)\s+zur\s+(?:Promotion|Weiterqualifikation)|zur\s+Promotion|Promotionsstelle|"
                               r"Promotionsvorhaben|Promotionsabsicht|Promotion\s+(?:ist|wird)|promovieren|Dissertation|"
                               r"pursue\s+a\s+(?:PhD|doctorate)|"
                               r"PhD\s+(?:project|student|position|thesis)|doctoral\s+(?:studies|thesis|candidate)", text, re.I) else None
    # 只写 Research Associate / Research Fellow 的标题，正文要求博士学位才算博后（否则多是研究助理类职位）
    if level == "postdoc" and not re.search(r"post[\s-]?doc", title, re.I) and not WIMI.search(title) and \
            not re.search(r"\bph\.?\s?d\b|doctoral degree|doctorate", text, re.I):
        level = None
    if not level:
        return None, "非博士/博后岗位"
    day, quote = deadline(text, end_date, order_hint)
    if not day:
        return None, "页面无截止日期"
    if day < today:
        return None, "已截止"
    if _any(_SELF_FUNDED, title + " " + text):
        return None, "自费或竞争性资助"
    if not _any(PAY, text):
        return None, "未写资助"
    # 同一岗位的另一语言版本（如赫尔辛基大学的芬兰语 / 英语页）：标题相同，或站内编号相同（维也纳大学德 / 英文标题不同）
    ref = REF.search(text)
    keys = [(adapter, org, title.lower(), day)] + ([(adapter, org, ref.group(1), day)] if ref else [])
    if any(_SEEN.get(k, jid) != jid for k in keys):
        return None, "重复（另一语言版本）"
    _SEEN.update({k: jid for k in keys})
    amount = AMOUNT.search(text)
    from collect_postings import cn_of, flags_of  # 资格 / 安全审查用岗位采集的共用规则（限本土、写明国际生可申、ZRR 等）
    return {
        "id": f"{adapter}:{jid}", "title": title[:200], "url": url, "org": org, "country": country,
        "place": place[:80], "level": level, "deadline": day, "quote": quote[:160], "funding_for": "",
        "amount": (amount.group(0).strip() if amount else "")[:200],
        "cn": cn_of(text), "flags": flags_of(text), "via": via,
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

SF_LOC = re.compile(r"<(?:loc|link)>\s*(https://[^<\s]+/job/([^<\s/]+)/(\d+)/)\s*</(?:loc|link)>")  # 个别站点（CSIRO）的 sitemap.xml 实为 RSS
_SF_SCHOOL: dict[str, tuple[str, str]] = {}


def sf_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, base, country in SUCCESSFACTORS:
        try:
            xml = htmllib.unescape(f.get(base + "/sitemap.xml").text)
        except Exception as e:  # noqa: BLE001
            print(f"[successfactors] {school} 站点地图失败：{type(e).__name__}")
            continue
        host = base.split("//")[1].split(".")[1]  # careers.unibas.ch → unibas
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


SF_END = re.compile(r"Find similar jobs|Ähnliche Stellen|Similar jobs|Trouver des offres similaires|Vergelijkbare vacatures", re.I)


def sf_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    school, country = _SF_SCHOOL.get(jid, ("", ""))
    title = cp.page_text(_itemprop(raw, "title"))
    if not title:  # 有的站点标题由脚本填入，<title> 里是 “岗位名 Job Details | 学校”
        m = re.search(r"<title>\s*(.*?)\s+(?:Job Details|Stellendetails|Détails de l'offre)", raw, re.S)
        title = cp.page_text(m.group(1)) if m else ""
    # 正文 + 自定义字段（截止日期常在描述之外，如 FU Berlin “Bewerbungsende: 09.11.2026”）；到“相似岗位”为止
    # 从页面里的岗位标题元素开始读（不从 <title> 和搜索栏开始，搜索栏里有“Promotionsabsicht”之类的筛选项）
    i = max(raw.find('itemprop="title"'), raw.find('id="main-job-title-heading"'))
    text = cp.page_text(raw[i if i >= 0 else 0:])
    end = SF_END.search(text)
    text = text[:end.start()] if end else text
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
    if "awsWafCookie" in raw[:3000]:  # 被 AWS WAF 验证拦截：整个适配器停下，不做绕过
        raise RuntimeError("被 AWS WAF 人机验证拦截，停止")
    school, country = _PU.get(jid, ("", ""))
    title = cp.page_text(_itemprop(raw, "title"))
    d = raw.find('id="job-content"')
    e = raw.find('id="search-results"', d)
    text = cp.page_text(raw[d:e if e > d else d + 120000]) if d >= 0 else cp.page_text(raw)
    return row("pageup", jid, url, title, school, country, "", text, "PageUp", today)


# ───────────────────────── ReachMee（*.reachmee.com/ext） ─────────────────────────

# 链接后面的表格单元里有隐藏的结构化截止日期（<span data-order="1" style="display:none">2026-11-14</span>）
RM_LINK = re.compile(r"<a href='([^']+/job\?[^']*job_id=(\d+))'[^>]*>(.*?)</a>(.{0,400}?display:none\">(\d{4}-\d{2}-\d{2}))?", re.S)
_RM: dict[str, tuple[str, str, str]] = {}  # 岗位 id → (学校, 国家, 列表上的截止日期)


def rm_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for school, base, query, country in REACHMEE:
        try:
            raw = f.get(f"{base}/main?{query}").text
        except Exception as e:  # noqa: BLE001
            print(f"[reachmee] {school} 列表失败：{type(e).__name__}")
            continue
        for href, num, label, _, listed in RM_LINK.findall(raw):
            if SLUG.search(cp.page_text(label)):
                jid = f"{base.rsplit('/', 2)[-2]}-{base.rsplit('/', 1)[-1]}-{num}"
                out.setdefault(jid, htmllib.unescape(href))
                _RM[jid] = (school, country, listed)
    return list(out.items())


def rm_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    school, country, listed = _RM.get(jid, ("", "", ""))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    return row("reachmee", jid, url, cp.page_text(h1.group(1)) if h1 else "", school, country, "", cp.page_text(raw),
               "ReachMee", today, listed)


# ───────────────────────── 学校自建招聘页（列表页 + 岗位页） ─────────────────────────

_LS: dict[str, tuple[str, str, str]] = {}  # 岗位 id → (学校, 国家, 标题正则)


def ls_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    import gzip
    out: dict[str, str] = {}
    for school, listing, link_re, prefix, country, *title_re in LISTS:
        for page in [listing] if isinstance(listing, str) else listing:  # 可以是多页列表
            try:
                r = f.get(page)
                body = getattr(r, "content", b"")
                raw = gzip.decompress(body).decode("utf-8", "replace") if body[:2] == b"\x1f\x8b" else r.text
            except Exception as e:  # noqa: BLE001
                print(f"[university] {school} 列表失败：{type(e).__name__}")
                continue
            # 站点地图 / RSS / Atom（链接正则以 < 开头）：看链接本身；列表页：只读链接文字（或整行可点的表格行）像博士 / 博后岗位的
            feed = link_re.lstrip("(?#全部)").startswith(("<", '"'))
            blocks = [raw] if feed else [b.group(0) for b in re.finditer(r"<(a|tr|li)\b[^>]*>.*?</\1>", raw, re.S)]
            for block in blocks:
                for m in re.finditer(link_re, block):
                    label = m.group(0) if feed else cp.page_text(block)
                    if feed and "<item" in raw:  # RSS：看所在条目的标题
                        item = raw.rfind("<item", 0, m.start())
                        label = raw[item:m.end()] if item >= 0 else label
                    if "(?#全部)" in link_re or SLUG.search(label):
                        host = (prefix + m.group(1)).split("//")[1].split("/")[0].split(".")
                        jid = f"{host[1] if len(host) > 2 else host[0]}-{m.group(2)}"
                        out.setdefault(jid, prefix + htmllib.unescape(m.group(1)))
                        _LS[jid] = (school, country, title_re[0] if title_re else r"<h1[^>]*>(.*?)</h1>")
    return list(out.items())


GENERIC_TITLE = re.compile(r"^(contact|kontakt|job offers?|jobs?|stellenangebote?|vacanc(?:y|ies)|careers?)$", re.I)


def ls_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    school, country, title_re = _LS.get(jid, ("", "", r"<h1[^>]*>(.*?)</h1>"))
    # 第一个非空、不是“Contact / Job offer”这类栏目名的标题
    # 优先像岗位名的（如 TUM 页面的第一个 <h1> 是校名）
    cands = [m for m in re.finditer(title_re, raw, re.S)
             if cp.page_text(m.group(1)) and not GENERIC_TITLE.match(cp.page_text(m.group(1)))]
    t = next((m for m in cands if SLUG.search(cp.page_text(m.group(1))) or WIMI.search(cp.page_text(m.group(1)))),
             cands[0] if cands else None)
    title = cp.page_text(t.group(1)) if t else ""
    if re.search(r"JavaScript is (disabled|required)", title, re.I):
        return None, "页面要脚本才显示（可能被拦）"
    # 正文从页面里的标题开始读，避开导航菜单（如 RWTH 菜单里的“Promotion von A bis Z”）；标题取自 <title> 时从 <body> 读
    start = t.start() if t and "<title" not in title_re else max(raw.find("<body"), 0)
    # 学校自己的页面（非美加）：同页看不出日月顺序时按 日/月/年 读（招聘系统的英文界面才会用 月/日/年）
    return row("university", jid, url, title, school, country, "", cp.page_text(raw[start:]),
               school, today, order_hint="" if country in ("US", "CA") else "DMY")


ADAPTERS = {"workday": (wd_urls, wd_detail), "successfactors": (sf_urls, sf_detail), "oracle": (orc_urls, orc_detail),
            "pageup": (pu_urls, pu_detail), "reachmee": (rm_urls, rm_detail), "university": (ls_urls, ls_detail)}
VIA_RANK = {"Workday": 3, "SuccessFactors": 3, "Oracle Recruiting": 3, "PageUp": 3, "ReachMee": 3, **{s[0]: 3 for s in LISTS}}

import collect_postings as cp  # noqa: E402 放在末尾：collect_postings 末尾经 platforms_ats.py 导入本模块时，要先看到 ADAPTERS
