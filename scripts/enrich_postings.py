#!/usr/bin/env python3
"""给在招岗位补上申请要用的结构化字段（学位、语言、开始时间、年限、材料、申请方式、导师、国籍限制），每个字段附官网原句。

    python scripts/enrich_postings.py fetch [--limit 200] [--via Varbi]   # 读详情页 → 规则提取，正文缓存在 .cache/posting_text/
    python scripts/enrich_postings.py bundle --dir /tmp/enrich --size 15   # 规则没取全的岗位分批写成子代理输入
    python scripts/enrich_postings.py apply --dir /tmp/enrich              # 校验子代理输出（out-*.yml）并写回
    python scripts/enrich_postings.py stats                                # 覆盖率与各字段命中率

子代理（model: sonnet）按 research/enrich-prompt.md 从正文抽取。写入前程序校验：
- 原句（quote）必须一字不差地出现在该岗位的页面正文里（只统一空白、引号、连字符和大小写）；
- 中文简述（value）里的每个数字都必须出现在原句里（英文数字词与月份按数字算）；
- 申请方式只能是“在线系统 / 邮件 / 其他”开头；不合格的字段整项丢弃，宁缺毋滥。
结果写入 _data/posting_fields.yml（按岗位 id）；已处理的 id 记下日期，增量运行。FindAPhD 本机被拦，不处理；Jobbnorge 详情页靠脚本渲染，暂不处理。
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import threading
from datetime import date
from urllib.parse import urlparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from scrapers.common import Disallowed, Fetcher  # noqa: E402
from collect_postings import page_text  # noqa: E402

POSTINGS = ROOT / "_data" / "postings.yml"
OUT = ROOT / "_data" / "posting_fields.yml"
CACHE = ROOT / ".cache" / "posting_text"
FIELDS = ["degree", "language", "start", "duration", "documents", "apply_via", "supervisor", "nationality"]
KEY3 = ["degree", "language", "documents"]  # 路线图“做完的标准”看的三项
MAX_TEXT = 15000
QUOTE_LEN = {"documents": 900}  # 材料清单常是一整段列表，允许长一些
SKIP_VIA = {"FindAPhD", "Jobbnorge"}
RETRY_DAYS = 7  # 读取失败的岗位隔几天再试

# 各平台正文的起止标记：只把岗位本身交给子代理，去掉导航、推荐岗位、页脚
BODY = {
    "jobs.ac.uk": (r"Back to search results", r"Share on social media|We value your feedback|Advert information"),
    "AcademicTransfer": (r"Research fields|Job description", r"Employer information|Interesting for you"),
    "Varbi": (r"Login and apply .*?Login and apply", r"Share links Return to job vacancies|Login and apply Share links"),
    "DAAD PhDGermany": (r"PhD Detail Back to Overview", r"Opens chatbot|All addresses in the DAAD Network"),
    "Nature Careers": (r"More Results", r"Share this job|Similar jobs"),
    "Science Careers": (r"More Results", r"Share this job|Similar jobs"),
    "Physics Today Jobs": (r"Visit Physics Today \(This link will open in a new window\) Employers", r"Share Facebook Twitter|Similar jobs"),
    "THE Unijobs": (r"More Results", r"Share this job|Similar jobs"),
    "Inria Jobs": (r"Inria job offers >", r"I create my account|Share on"),
    "Academic Jobs Online": (r"", r"Further Info|Apply Online|Previous Job"),
    "ETH Zurich Jobs": (r"", r"About ETH|Apply online"),
}


# ───────────────────────── 文本与校验 ─────────────────────────

def norm(s: str) -> str:
    s = s.replace("\xad", "").replace("​", "").replace("\xa0", " ")
    s = re.sub(r"[‘’‛′`´]", "'", s)
    s = re.sub(r"[“”„″]", '"', s)
    s = re.sub(r"[‐‑‒–—―−]", "-", s)
    return re.sub(r"\s+", " ", s).strip().lower()


WORD_NUM = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
WORD_NUM.update({"half": "0.5", "thirteen": "13", "fifteen": "15", "twenty": "20", "thirty": "30",
                 "forty": "40", "fifty": "50", "sixty": "60", "hundred": "100", "thousand": "1000"})
WORD_NUM.update(dict(zip("first second third fourth fifth sixth seventh eighth ninth tenth".split(), map(str, range(1, 11)))))
# 瑞典语 / 挪威语 / 丹麦语 / 德语 / 荷兰语 / 法语公告里的 2–10（1 的写法与冠词同形，不收）
for words in ("två tre fyra fem sex sju åtta nio tio", "to tre fire fem seks sju åtte ni ti",
              "zwei drei vier fünf sechs sieben acht neun zehn", "twee drie vier vijf zes zeven acht negen tien",
              "deux trois quatre cinq six sept huit neuf dix", "dois três quatro cinco seis sete oito nove dez",
              "dos tres cuatro cinco seis siete ocho nueve diez", "due tre quattro cinque sei sette otto nove dieci"):
    WORD_NUM.update({w: str(i) for i, w in enumerate(words.split(), start=2) if w not in ("to", "ni", "sex")})
WORD_NUM.update({"duas": "2", "segundo": "2", "terceiro": "3", "två": "2", "andra": "2", "tredje": "3", "fjärde": "4", "zweite": "2", "dritte": "3",
                 "deuxième": "2", "troisième": "3", "six": "6"})
MONTH_NUM = {m: str(i + 1) for i, m in enumerate(
    "january february march april may june july august september october november december".split())}
MONTH_NUM.update({m[:3]: n for m, n in MONTH_NUM.items()} | {"sept": "9"})
for i, names in enumerate(["januari januar janvier", "februari februar février", "mars märz maart", "april avril",
                           "maj mai mei", "juni juin", "juli juillet", "augusti august augustus août",
                           "september septembre", "oktober octobre", "november novembre", "december dezember desember décembre"], 1):
    MONTH_NUM.update({n: str(i) for n in names.split()})
for i, names in enumerate(["janeiro enero gennaio", "fevereiro febrero febbraio", "março marzo", "abril aprile", "maio mayo maggio",
                           "junho junio giugno", "julho julio luglio", "agosto", "setembro septiembre settembre",
                           "outubro octubre ottobre", "novembro noviembre", "dezembro diciembre dicembre"], 1):
    MONTH_NUM.update({n: str(i) for n in names.split()})
CN_NUM = dict(zip("一二两三四五六七八九十", ["1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))


def numbers(text: str) -> set[str]:
    """数字集合：去掉千分位与前导零；'4,000' → '4000'，'01' → '1'。"""
    out = set()
    text = re.sub(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b", r"\1 \2 \3", text)  # 日期“01.12.2026”拆成日、月、年
    for n in re.findall(r"\d[\d,.]*\d|\d", text):
        n = n.replace(",", "").rstrip(".")
        if "." in n:
            n = n.rstrip("0").rstrip(".") if re.fullmatch(r"\d+\.\d+", n) else n
        out.add(n.lstrip("0") or "0")
    return out


def quote_numbers(quote: str) -> set[str]:
    out = numbers(quote)
    for w in re.findall(r"[a-zäöåüéèûàçãõêíóúâ]+", quote.lower()):
        if w in WORD_NUM:
            out.add(WORD_NUM[w])
        if w in MONTH_NUM:
            out.add(MONTH_NUM[w])
    return out


def value_numbers(value: str) -> set[str]:
    """简述里的数字：阿拉伯数字 + 单个汉字数字（“四年”“两封推荐信”）；“十二月”等组合按单字检查已足够严格。"""
    out = numbers(value)
    for ch in re.findall(r"[一二两三四五六七八九十](?=[年个封份月周页位名])", value):
        out.add(CN_NUM[ch])
    return out


BANNED = re.compile(r"未写明|未提及|未说明|未知|不详|待确认|未提供|无相关|(?-i:\bN/A\b)|unknown|not (?:specified|mentioned)", re.I)
APPLY_VIA = re.compile(r"^(在线系统|邮件|其他)")


def check_field(name: str, f, body_norm: str) -> str | None:
    """返回不通过的原因；None 表示通过。"""
    if name not in FIELDS:
        return "未知字段"
    if not isinstance(f, dict) or not isinstance(f.get("value"), str) or not isinstance(f.get("quote"), str):
        return "格式不对"
    value, quote = f["value"].strip(), f["quote"].strip()
    if not value or not quote:
        return "空值"
    if BANNED.search(value):
        return "空话"
    if len(value) > 160:
        return "简述过长"
    if not 6 <= len(quote) <= QUOTE_LEN.get(name, 400):
        return "原句长度不符"
    if norm(quote) not in body_norm:
        return "原句不在正文"
    extra = value_numbers(value) - quote_numbers(quote)
    if extra:
        return f"数字不在原句：{sorted(extra)}"
    if name == "apply_via" and not APPLY_VIA.match(value):
        return "申请方式格式"
    if name == "supervisor" and not re.search(r"[A-Za-z]", value + quote):
        return "导师无姓名"
    return None


def body_of(via: str, text: str) -> str:
    start, end = BODY.get(via, ("", ""))
    if start:
        m = re.search(start, text, re.S)
        if m:
            text = text[m.start():] if via != "Varbi" else text[m.end():]
    if end:
        m = re.search(end, text[200:])
        if m:
            text = text[:200 + m.start()]
    return text.strip()[:MAX_TEXT]


# ───────────────────────── 规则提取（平台固定栏目） ─────────────────────────

DEGREE_CN = {"master": "硕士", "magister": "硕士", "diplom": "德国 Diplom（相当于硕士）", "bachelor": "学士", "phd": "博士",
             "doctorate": "博士", "state examination": "国家考试（Staatsexamen）"}
LANG_CN = {"english": "英语", "german": "德语", "french": "法语", "spanish": "西班牙语", "italian": "意大利语"}
DOC_CN = {"motivation letter": "动机信", "cover letter": "求职信", "cv": "简历", "certificates": "学历证书",
          "references": "推荐信", "reference letters": "推荐信", "letters of recommendation": "推荐信",
          "transcript of records": "成绩单", "transcripts": "成绩单", "research proposal": "研究计划",
          "proof of language proficiency": "语言能力证明", "publications": "发表论文", "copy of passport": "护照复印件",
          "abstract of master thesis": "硕士论文摘要", "letter of motivation": "动机信", "diploma": "学位证书"}
FUNDING_FOR_CN = {"uk students": "英国学生", "eu students": "欧盟学生", "international students": "国际学生"}


def F(value: str, quote: str) -> dict:
    return {"value": value, "quote": quote}


def rule_daad(body: str) -> dict:
    out = {}
    m = re.search(r"Required Degree\s+(.{2,120}?)\s+(?=Areas of study|Description)", body)
    if m:
        kinds = []
        for k, v in DEGREE_CN.items():
            if re.search(rf"\b{k}", m.group(1), re.I) and v not in kinds:
                kinds.append(v)
        if kinds:
            out["degree"] = F(" 或 ".join(kinds), m.group(0).strip())
    m = re.search(r"Working Language\s+([A-Za-z ,/&]+?)\s+(?=Location|Required|Areas|Application)", body)
    if m:
        langs = [LANG_CN[w.lower()] for w in re.findall(r"[A-Za-z]+", m.group(1)) if w.lower() in LANG_CN]
        if langs:
            out["language"] = F("工作语言：" + "、".join(dict.fromkeys(langs)), m.group(0).strip())
    m = re.search(r"Time Span\s+(.{2,80}?)\s+(?=Application Deadline|Financing)", body)
    if m:
        y = re.search(r"\bfor\s+(\d+(?:\.\d+)?)\s+years?\b", m.group(1))
        mo = re.search(r"\bfor\s+(\d+)\s+months?\b", m.group(1))
        if y or mo:
            out["duration"] = F(f"{y.group(1)} 年" if y else f"{mo.group(1)} 个月", m.group(0).strip())
    m = re.search(r"Starting Date\s+(as soon as possible|\d{1,2}\.\s*[A-Za-z]{3}\s+\d{4})\s+(?=Overview|Description)", body)
    if m:
        v = m.group(1)
        if v.startswith("as soon"):
            v = "尽快"
        else:
            d, mon, y = re.match(r"(\d{1,2})\.\s*([A-Za-z]{3})\s+(\d{4})", v).groups()
            v = f"{y} 年 {MONTH_NUM.get(mon.lower(), '?')} 月 {int(d)} 日"
        if "?" not in v:
            out["start"] = F(v, m.group(0).strip())
    m = re.search(r"Required Documents Required Documents\s+(.{3,400}?)\s+(?=Application Application|Application\b)", body)
    if m:
        items, rest = [], m.group(1)
        for k in sorted(DOC_CN, key=len, reverse=True):
            if re.search(rf"\b{re.escape(k)}\b", rest, re.I):
                rest = re.sub(rf"\b{re.escape(k)}\b", " ", rest, flags=re.I)
                items.append(DOC_CN[k])
        if items and not re.sub(r"[\s,;/&.-]|and", "", rest, flags=re.I):  # 每一项都认得才用规则，否则交给子代理
            out["documents"] = F("、".join(dict.fromkeys(items)), m.group(0).strip())
    return out


def rule_jac(body: str) -> dict:
    m = re.search(r"Funding for:\s*(.{3,120}?)\s+(?=Funding amount:|Hours:|Placed On:|Salary:)", body)
    if not m:
        return {}
    parts = [FUNDING_FOR_CN.get(p.strip().lower()) for p in m.group(1).split(",")]
    if not parts or None in parts:
        return {}
    return {"nationality": F("资助对象：" + "、".join(parts), m.group(0).strip())}


def rule_inria(body: str) -> dict:
    """Inria 招聘页的固定栏目（开始日期栏目常是过期的旧值，交给子代理从正文取）。"""
    out = {}
    m = re.search(r"Level of qualifications required : (PhD or equivalent|Graduate degree or equivalent)", body)
    if m:
        out["degree"] = F("博士或同等学历" if m.group(1).startswith("PhD") else "研究生学位（硕士）或同等学历", m.group(0))
    m = re.search(r"Duration of contract : ((?:\d+ years?)?(?:, )?(?:\d+ months?)?)(?= Deadline)", body)
    if m and m.group(1):
        y = re.search(r"(\d+) years?", m.group(1))
        mo = re.search(r"(\d+) months?", m.group(1))
        out["duration"] = F(" ".join(x for x in (f"{y.group(1)} 年" if y else "", f"{mo.group(1)} 个月" if mo else "") if x), m.group(0))
    m = re.search(r"Applications must be submitted online on the Inria website\.", body)
    if m:
        out["apply_via"] = F("在线系统：Inria 招聘网站", m.group(0))
    return out


RULES = {"DAAD PhDGermany": rule_daad, "jobs.ac.uk": rule_jac, "Inria Jobs": rule_inria}


# ───────────────────────── 读取 ─────────────────────────

def load_yaml(p: Path, default):
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or default) if p.exists() else default


def save(data: dict) -> None:
    tmp = OUT.with_suffix(".yml.tmp")  # 先写临时文件再改名：读取方不会读到写了一半的文件
    tmp.write_text(yaml.safe_dump(dict(sorted(data.items())), allow_unicode=True, width=200, sort_keys=False),
                   encoding="utf-8")
    tmp.replace(OUT)


def cache_path(pid: str) -> Path:
    return CACHE / (re.sub(r"[^\w.-]", "_", pid) + ".txt")


def live_postings(today: str) -> list[dict]:
    out = []
    for p in load_yaml(POSTINGS, []):
        if p.get("cn") == "no" or p.get("via") in SKIP_VIA:
            continue
        if p["deadline"] != "rolling" and p["deadline"] < today:
            continue
        out.append(p)
    return out


def inspire_text(f: Fetcher, url: str) -> str:
    """INSPIRE 详情页靠脚本渲染：读它公开的 REST 接口记录（collect_postings.py 也用这个接口）。"""
    jid = re.search(r"/jobs/(\d+)", url).group(1)
    md = f.get(f"https://inspirehep.net/api/jobs/{jid}").json().get("metadata", {})
    parts = [md.get("position", ""), page_text(md.get("description", "")),
             " ".join(r.get("value", "") if isinstance(r, dict) else str(r) for r in md.get("reference_letters", {}).get("urls", []))]
    return " ".join(p for p in parts if p)


def ats_text(f: Fetcher, p: dict) -> str | None:
    """详情页靠脚本渲染的招聘系统：读采集器用的同一个公开岗位接口（见 scripts/ats.py、platforms_de.py）。"""
    import base64
    import ats

    url = p["url"]
    if p["via"] == "Workday":
        info = f.get(ats.wd_api(url)).json().get("jobPostingInfo") or {}
        return " ".join(x for x in (info.get("title"), page_text(info.get("jobDescription") or "")) if x)
    if p["via"] == "Oracle Recruiting":
        m = re.match(r"(https://[^/]+)/hcmUI/CandidateExperience/[a-z]{2}/sites/([\w-]+)/job/(\w+)", url)
        if not m:
            return None
        items = f.get(ats.ORC_DETAIL.format(host=m.group(1), site=m.group(2), id=m.group(3))).json().get("items") or []
        d = items[0] if items else {}
        return page_text(" ".join(d.get(k) or "" for k in ("Title", "ExternalDescriptionStr", "ExternalResponsibilitiesStr",
                                                             "ExternalQualificationsStr", "ShortDescriptionStr")))
    if p["via"] == "Bundesagentur für Arbeit":
        from platforms_de import BA, BA_KEY
        ref = url.rstrip("/").rsplit("/", 1)[-1]
        j = f.get(f"{BA}/pc/v4/jobdetails/{base64.b64encode(ref.encode()).decode()}", headers=BA_KEY).json()
        desc = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", j.get("stellenangebotsBeschreibung") or "")
        return " ".join(x for x in (j.get("stellenangebotsTitel"), page_text(re.sub(r"[*_#\\]+", " ", desc))) if x)
    return None


def page_body(f: Fetcher, p: dict) -> str:
    if p["via"] == "INSPIRE-HEP Jobs":
        return inspire_text(f, p["url"])[:MAX_TEXT]
    if p["via"] in ("Workday", "Oracle Recruiting", "Bundesagentur für Arbeit"):
        return (ats_text(f, p) or "")[:MAX_TEXT]
    text = page_text(f.get(p["url"]).text)
    if p["via"] not in BODY:  # 没配起止标记的平台：从标题第二次出现处开始（第一次多在 <title> 或导航里）
        key = (p.get("title") or "")[:40]
        first = text.find(key) if key else -1
        second = text.find(key, first + 1) if first >= 0 else -1
        if second > 0:
            text = text[second:]
    return body_of(p["via"], text)


def cmd_fetch(args) -> int:
    today = args.today or date.today().isoformat()
    data = load_yaml(OUT, {})
    CACHE.mkdir(parents=True, exist_ok=True)
    todo = []
    for p in live_postings(today):
        if args.via and p["via"] != args.via:
            continue
        rec = data.get(p["id"]) or {}
        if rec.get("checked") and not rec.get("error") and (cache_path(p["id"]).exists() or rec.get("llm")):
            continue
        if rec.get("error") and (date.fromisoformat(today) - date.fromisoformat(rec["checked"])).days < RETRY_DAYS:
            continue
        todo.append(p)
    todo = todo[: args.limit] if args.limit else todo
    print(f"待读取 {len(todo)} 个岗位")
    stats: dict[str, int] = {}
    lock = threading.Lock()
    done = [0]

    def one(f: Fetcher, p: dict) -> None:
        rec = {k: v for k, v in (data.get(p["id"]) or {}).items() if k in FIELDS or k == "llm"}
        try:
            cached = cache_path(p["id"])
            body = cached.read_text(encoding="utf-8") if cached.exists() else page_body(f, p)  # 上次中断前已读过的不再访问
        except Disallowed:
            rec.update(checked=today, error="robots.txt 不允许")
        except Exception as e:  # noqa: BLE001
            rec.update(checked=today, error=f"读取失败 {type(e).__name__}"[:80])
        else:
            if len(body) < 200:
                rec.update(checked=today, error="正文太短")
            else:
                cache_path(p["id"]).write_text(body, encoding="utf-8")
                rec["checked"] = today
                rec.pop("error", None)
                bn = norm(body)
                for k, v in (RULES.get(p["via"], lambda b: {})(body)).items():
                    if check_field(k, v, bn) is None:  # 规则结果也走同一套校验
                        rec[k] = v
        with lock:
            data[p["id"]] = rec
            key = rec.get("error") or "成功"
            stats[key] = stats.get(key, 0) + 1
            done[0] += 1
            if done[0] % 100 == 0:
                save(data)
                print(f"  {done[0]}/{len(todo)} {stats}", flush=True)

    def worker(items: list[dict]) -> None:
        f = Fetcher(delay=args.delay)  # 每个站点一个线程、一个客户端：站内仍按间隔逐个访问
        for p in items:
            one(f, p)

    by_host: dict[str, list[dict]] = {}
    for p in todo:
        by_host.setdefault(urlparse(p["url"]).netloc.split(".", 1)[-1], []).append(p)
    threads = [threading.Thread(target=worker, args=(items,)) for items in by_host.values()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    save(data)
    print(stats)
    return 0


# ───────────────────────── 子代理批次 ─────────────────────────

SECOND_DOC = r"curriculum vitae|\bCV\b|cover letter|motivation letter|letter of motivation|transcripts?|referees|lettre de motivation|Lebenslauf|Anschreiben|Zeugnisse"
SECOND_LANG = r"IELTS|TOEFL|fluent|proficien|command of (the )?English|English (language )?skills|Englischkenntnisse|Deutschkenntnisse|anglais"


def cmd_bundle(args) -> int:
    today = args.today or date.today().isoformat()
    data = load_yaml(OUT, {})
    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in live_postings(today):
        rec = data.get(p["id"]) or {}
        if rec.get("error") or not cache_path(p["id"]).exists():
            continue
        if args.second_pass:  # 第二遍：已抽过、但正文明显写了材料或语言却没取到的岗位
            text = cache_path(p["id"]).read_text(encoding="utf-8")
            if not rec.get("llm") or rec.get("llm2") or sum(k in rec for k in KEY3) >= 2 or not (
                    ("documents" not in rec and re.search(SECOND_DOC, text, re.I))
                    or ("language" not in rec and re.search(SECOND_LANG, text, re.I))):
                continue
        elif rec.get("llm"):
            continue
        if all(k in rec for k in FIELDS):
            continue
        rows.append({"id": p["id"], "title": p["title"], "org": p.get("org", ""), "level": p["level"],
                     "have": [k for k in FIELDS if k in rec], "text": cache_path(p["id"]).read_text(encoding="utf-8")})
    rows = rows[: args.limit] if args.limit else rows
    n = 0
    for i in range(0, len(rows), args.size):
        n += 1
        (d / f"bundle-{n:03d}.yml").write_text(
            yaml.safe_dump(rows[i:i + args.size], allow_unicode=True, width=10**6, sort_keys=False), encoding="utf-8")
    print(f"{len(rows)} 个岗位 → {n} 个批次（{d}/bundle-*.yml）；子代理输出写到 {d}/out-<同编号>.yml")
    return 0


def parse_out(path: Path) -> list:
    raw = path.read_text(encoding="utf-8").strip()
    raw = re.sub(r"^```\w*\n|\n```$", "", raw)
    try:
        return yaml.safe_load(raw) or []
    except yaml.YAMLError:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []


def apply_rows(data: dict, rows: list, bodies: dict[str, str], today: str, verbose: bool = False,
               mark: str = "llm") -> dict[str, int]:
    stats: dict[str, int] = {}

    def bump(k):
        stats[k] = stats.get(k, 0) + 1

    for r in rows if isinstance(rows, list) else []:
        pid = r.get("id") if isinstance(r, dict) else None
        if pid not in bodies:
            bump("id 不在输入")
            continue
        rec = data.setdefault(pid, {"checked": today})
        bn = norm(bodies[pid])
        for name, f in (r.get("fields") or {}).items():
            if name in rec:  # 规则已取到的不覆盖
                continue
            if f in (None, "", {}):
                continue
            why = check_field(name, f, bn)
            if why:
                bump(why.split("：")[0])
                if verbose:
                    print(f"  ✗ {pid} {name}: {why} | {f}")
                continue
            rec[name] = {"value": f["value"].strip(), "quote": f["quote"].strip()}
            bump(f"通过·{name}")
        rec[mark] = today
    return stats


def cmd_apply(args) -> int:
    today = args.today or date.today().isoformat()
    data = load_yaml(OUT, {})
    d = Path(args.dir)
    total: dict[str, int] = {}
    for b in sorted(d.glob("bundle-*.yml")):
        o = d / b.name.replace("bundle-", "out-")
        if not o.exists():
            print(f"{o.name} 不存在，跳过")
            continue
        bodies = {it["id"]: it["text"] for it in yaml.safe_load(b.read_text(encoding="utf-8")) or []}
        rows = parse_out(o)
        if not rows:
            print(f"{o.name} 解析失败或为空")
            continue
        for k, v in apply_rows(data, rows, bodies, today, args.verbose, "llm2" if args.second_pass else "llm").items():
            total[k] = total.get(k, 0) + v
    print(dict(sorted(total.items())))
    if not args.dry_run:
        save(data)
    return 0


def cmd_rules(args) -> int:
    data = load_yaml(OUT, {})
    via = {p["id"]: p["via"] for p in load_yaml(POSTINGS, [])}
    n = 0
    for pid, rec in data.items():
        rule = RULES.get(via.get(pid, ""))
        if not rule or not cache_path(pid).exists():
            continue
        body = cache_path(pid).read_text(encoding="utf-8")
        for k, v in rule(body).items():
            if check_field(k, v, norm(body)) is None and rec.get(k) != v:
                rec[k] = v
                n += 1
    save(data)
    print(f"规则更新 {n} 个字段")
    return 0


def cmd_recheck(args) -> int:
    """校验规则收紧后，对已写入的字段按缓存正文重新校验，不通过的删除。"""
    data = load_yaml(OUT, {})
    stats: dict[str, int] = {}
    for pid, rec in data.items():
        if not cache_path(pid).exists():
            continue
        bn = norm(cache_path(pid).read_text(encoding="utf-8"))
        for k in [k for k in FIELDS if k in rec]:
            why = check_field(k, rec[k], bn)
            if why:
                stats[why.split("：")[0]] = stats.get(why.split("：")[0], 0) + 1
                if args.verbose:
                    print(f"  ✗ {pid} {k}: {why} | {rec[k]}")
                del rec[k]
    save(data)
    print(f"删除 {sum(stats.values())} 个字段 {stats}")
    return 0


def cmd_stats(args) -> int:
    today = args.today or date.today().isoformat()
    data = load_yaml(OUT, {})
    allp = [p for p in load_yaml(POSTINGS, []) if p.get("cn") != "no" and (p["deadline"] == "rolling" or p["deadline"] >= today)]
    reach = [p for p in allp if p["via"] not in SKIP_VIA]
    two = [p for p in allp if sum(k in (data.get(p["id"]) or {}) for k in KEY3) >= 2]
    print(f"在招岗位 {len(allp)}（可读取 {len(reach)}）；学位/语言/材料至少两项：{len(two)} = "
          f"{len(two) / max(len(allp), 1):.0%}（占可读取 {len(two) / max(len(reach), 1):.0%}）")
    for k in FIELDS:
        n = sum(k in (data.get(p["id"]) or {}) for p in reach)
        print(f"  {k:12s} {n:5d}  {n / max(len(reach), 1):.0%}")
    by: dict[str, list[int]] = {}
    for p in reach:
        s = by.setdefault(p["via"], [0, 0])
        s[0] += 1
        s[1] += sum(k in (data.get(p["id"]) or {}) for k in KEY3) >= 2
    for v, (n, ok) in sorted(by.items(), key=lambda x: -x[1][0]):
        print(f"  {v:22s} {ok:4d}/{n:<4d} {ok / n:.0%}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("fetch")
    a.add_argument("--limit", type=int, default=0)
    a.add_argument("--via")
    a.add_argument("--delay", type=float, default=2.0)
    a = sub.add_parser("bundle")
    a.add_argument("--dir", required=True)
    a.add_argument("--size", type=int, default=15)
    a.add_argument("--second-pass", action="store_true", help="对已抽过但漏了材料/语言的岗位再抽一遍")
    a.add_argument("--limit", type=int, default=0)
    a = sub.add_parser("apply")
    a.add_argument("--dir", required=True)
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("-v", "--verbose", action="store_true")
    a.add_argument("--second-pass", action="store_true", help="第二遍的输出：记 llm2，避免重复抽")
    sub.add_parser("rules")
    a = sub.add_parser("recheck")
    a.add_argument("-v", "--verbose", action="store_true")
    sub.add_parser("stats")
    args = ap.parse_args()
    return {"fetch": cmd_fetch, "bundle": cmd_bundle, "apply": cmd_apply, "rules": cmd_rules, "recheck": cmd_recheck, "stats": cmd_stats}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
