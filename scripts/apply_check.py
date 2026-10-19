#!/usr/bin/env python3
"""/apply 的程序部分：准备申请目录、从岗位原文摘申请清单、逐句校验文书里的事实。

    python scripts/apply_check.py prepare findaphd:195793          # 建 applications/<id>/，取岗位原文，生成申请清单
    python scripts/apply_check.py prepare https://... --text-file 原文.txt   # 网页打不开时用自己复制的原文
    python scripts/apply_check.py papers "Jane Smith" --affil Loughborough   # 查导师近期论文（OpenAlex），写进 lab.yml 前人工挑选
    python scripts/apply_check.py check applications/findaphd-195793          # 校验 drafts/*.md，写 check-report.md
    python scripts/apply_check.py clean applications/findaphd-195793          # 校验通过后去掉出处标记，写 final/*.md
    python scripts/apply_check.py edit-ratio applications/findaphd-195793     # 本人改稿后：final/ 与 sent/ 的修改比例

事实约束（文书里写到申请者的经历，每条都必须能在 cv-facts.yml 里找到）：
- 起草时每句涉及经历的话都标出处：[cv:pub1]、[cv:edu1,proj2]；引用导师论文标 [lab:p1]；引用岗位原文标 [post]。
- 程序逐句检查：
  · 出处 id 必须存在；
  · 句中的数字、机构 / 人名等专有名词（连续大写词、缩写）、引号或书名号里的标题、奖项名、网址，
    都必须出现在该句所引出处的原文里（未标出处的句子只能用申请者姓名联系方式、岗位标题机构、导师姓名）；
  · “我做过 / I developed / my thesis …” 这类经历句没有 [cv:…] 出处直接判错；
  · 未填的占位符（TODO、XXX、<…>）判错；空话套话只给提醒，交给审稿子代理判断。
- 程序只能保证“没有凭空出现的事实”，不能保证语义对应正确；所以之后还要跑审稿子代理（research/apply-review-prompt.md）。

申请目录在 applications/（已在 .gitignore），申请者的材料绝不提交。
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
APPS = ROOT / "applications"
DRAFTS = ["email.md", "cover-letter.md", "research-plan.md", "cv-advice.md"]
FACT_PATHS = ["cv-facts.yml", "applications/cv-facts.yml"]  # 与 docs/profile-schema.md 一致，都在 .gitignore

# ───────────────────────── 找岗位 ─────────────────────────


def safe_id(pid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", pid).strip("-")[:80]


def load_postings() -> list[dict]:
    path = ROOT / "_data" / "postings.yml"
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or []) if path.exists() else []


def load_fields() -> dict:
    """工程 A 的岗位结构化字段（_data/posting_fields.yml，按 id 索引；文件不存在就是空）。"""
    path = ROOT / "_data" / "posting_fields.yml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if isinstance(data, list):
        return {d["id"]: d for d in data if isinstance(d, dict) and d.get("id")}
    return data if isinstance(data, dict) else {}


def find_opportunity(key: str, postings: list[dict] | None = None, sources: list[dict] | None = None) -> dict:
    """按 id 或链接在岗位与信源里查找；都查不到时只有链接也能继续（原文由 --text-file 提供）。"""
    postings = load_postings() if postings is None else postings
    for p in postings:
        if key in (p.get("id"), p.get("url")) or key in (p.get("also") or []):
            return {"kind": "posting", **p}
    if sources is None:
        from catalog import load_catalog
        sources = load_catalog()["sources"]
    for s in sources:
        if key in (s.get("id"), s.get("url")):
            return {"kind": "source", "id": s["id"], "title": s.get("name"), "url": s.get("url"),
                    "deadline": s.get("deadline"), "requirements": s.get("requirements"), "org": s.get("org", "")}
    if key.startswith("https://"):
        return {"kind": "url", "id": "url-" + safe_id(re.sub(r"^https://(www\.)?", "", key))[:60], "url": key, "title": ""}
    raise SystemExit(f"找不到 {key}：请给岗位 id（见网站链接 # 后面的部分）或官网链接")


def fetch_text(url: str) -> str:
    """走 Fetcher（robots.txt、限速）取正文；被拒或失败返回空串。"""
    import requests

    from scrapers.common import Disallowed, Fetcher
    from fetch_pages import page_text

    try:
        r = Fetcher(delay=1.0, timeout=25).get(url)
    except (Disallowed, requests.RequestException):
        return ""
    return page_text(r.text) if "html" in r.headers.get("Content-Type", "html") else ""


# ───────────────────────── 申请清单 ─────────────────────────

NUM_WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}
CHECK_ITEMS = [  # (清单项, 原文匹配规则)
    ("简历 CV", r"\b(curriculum vitae|CV|r[ée]sum[ée])\b"),
    ("求职信 / 动机信", r"\b(cover(ing)? letter|motivation(al)? letter|letter of motivation|personal statement|statement of purpose|letter of intent|(short |brief |one-page |supporting )?statement\s*(\([^)]*\)\s*)?(of|saying|explaining|describing|outlining|setting out)|supporting statement)\b"),
    ("研究计划 / 研究陈述", r"\b(research (proposal|statement|plan)|project proposal|statement of research)\b"),
    ("成绩单与学位证明", r"\b(transcripts?|diploma|degree certificates?|academic records?|grades?)\b"),
    ("推荐信 / 推荐人", r"\b(references?|referees?|recommendation letters?|letters? of (recommendation|reference)|reference letters?)\b"),
    ("语言成绩", r"\b(IELTS|TOEFL|Duolingo|PTE|Cambridge English|English (language )?(proficiency|requirements?|test))\b"),
    ("论文 / 写作样本", r"\b(writing sample|publication list|list of publications|master'?s thesis|copy of (your )?thesis)\b"),
    ("GRE", r"\bGRE\b"),
    ("护照 / 身份证明", r"\b(passport|proof of identity)\b"),
    ("作品集", r"\bportfolio\b"),
]
FORMAT_RE = re.compile(r"(max(imum)?\.?|up to|no (more|longer) than|not (to )?exceed(ing)?|limited to|at most|maximum of)\s+"
                       r"(\d[\d,]*|[a-z]+)\s+(words?|pages?|characters?|A4)|\b\d[\d,]*[\s-](words?|pages?)\b|\bsingle (PDF|file|document)\b|\bin English\b", re.I)
REF_RE = re.compile(r"\b(\d|one|two|three|four|five)\s+(academic\s+|professional\s+)?(references?|referees?|letters? of (recommendation|reference)|recommendation letters?|reference letters?)\b", re.I)
DEADLINE_RE = re.compile(r"\b(deadline|closing date|closes|apply by|applications? (must|should) be (received|submitted)|close[sd]? on|no later than)\b", re.I)
TIME_RE = re.compile(r"\b(\d{1,2}[:.]\d{2}\s*(am|pm)?|midnight|noon|\d{1,2}\s*(am|pm))\b|\b(CET|CEST|GMT|BST|UTC|AEST|AEDT|EST|EDT|PST|PDT|JST|KST|SGT|HKT|NZST|NZDT)\b", re.I)
HOW_RE = re.compile(r"\b(apply (online|via|through|using|here)|application (portal|form|system)|submit (your|an|the) application|send (your|an|the) application|via e-?mail|by e-?mail)\b|[\w.+-]+@[\w-]+\.[\w.-]+", re.I)
START_RE = re.compile(r"\b(start(ing)? date|expected to start|commenc(e|ing|ement)|start in|starting (in|on|from))\b", re.I)
INTERVIEW_RE = re.compile(r"\binterviews?\b.*\b(held|expected|take place|scheduled|will be)\b", re.I)
REQ_RE = re.compile(r"\b(acceptable (first )?degree|entry requirements?|eligibility|we (seek|are looking for) (a )?candidates?|candidates? (should|must|will) (have|hold|possess)|"
                    r"applicants? (should|must|will) (have|hold|possess)|(2:1|upper second|first[- ]class)|master'?s degree|bachelor'?s degree|person specification|essential|desirable)\b", re.I)
FUND_RE = re.compile(r"\b(stipend|funding (amount|for)|salary|maintenance|tuition fees?|(home|international) fees?|fee waiver|fully[- ]funded|studentships? (covers?|includes?)|per annum|p\.a\.)\b|[£€$]\s?\d", re.I)
CONTACT_RE = re.compile(r"\b(informal enquiries|for (further|more) information|contact (person|details)|questions? (about|regarding))\b", re.I)


BOILER = re.compile(r"^(jobs by email|skip to main content|back to search results|apply|share|save|print)$", re.I)


def sentences_of(text: str) -> list[str]:
    """网页正文常把一句话断成几行（标签与取值、括号、邮箱各占一行）：先并行再切句。"""
    lines: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or BOILER.match(line):
            continue
        prev = lines[-1] if lines else ""
        if prev and (prev.endswith(":") and len(prev) < 60 or re.match(r"^[)\],.;:a-z(]", line)
                     or re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+\)?\.?", line) or re.search(r"[(,]$", prev)):
            lines[-1] = f"{prev} {line}"
        else:
            lines.append(line)
    out = []
    for line in lines:
        out += [s.strip() for s in re.split(r"(?<=[.;!?])\s+(?=[A-Z0-9•\-–(])", line) if s.strip()]
    return out


def extract_checklist(text: str) -> dict:
    """从岗位原文按规则摘句子；只摘原句，摘不到就是空（不猜）。"""
    sents = sentences_of(text)
    hits = lambda rx: list(dict.fromkeys(s for s in sents if re.search(rx, s)))[:4]  # noqa: E731
    items = {name: hits(rx) for name, rx in CHECK_ITEMS}
    refs = []
    for s in sents:
        for m in REF_RE.finditer(s):
            refs.append(NUM_WORDS.get(m.group(1).lower(), m.group(1)))
    deadline = [s for s in sents if DEADLINE_RE.search(s)][:4]
    return {
        "materials": {k: v for k, v in items.items() if v},
        "references": sorted(set(refs)),
        "format": hits(FORMAT_RE),
        "deadline": deadline,
        "deadline_time": [s for s in deadline if TIME_RE.search(s)],
        "requirements": hits(REQ_RE),
        "funding": hits(FUND_RE),
        "how": hits(HOW_RE),
        "start": hits(START_RE),
        "interview": hits(INTERVIEW_RE),
        "contact": hits(CONTACT_RE),
    }


def checklist_md(opp: dict, cl: dict, fields: dict | None, has_text: bool) -> str:
    q = lambda xs: "\n".join(f"  > {x}" for x in xs)  # noqa: E731
    L = [f"# 申请清单：{opp.get('title') or opp['url']}", "",
         f"- 机构：{opp.get('org') or '（见原文）'}", f"- 官网：{opp['url']}",
         f"- 截止：{opp.get('deadline') or '（见原文）'}" + (f"（原句：{opp['quote']}）" if opp.get("quote") else ""), ""]
    if not has_text:
        L += ["> ⚠️ 没取到岗位原文（网站拒绝程序访问）。请打开官网，把正文复制到同目录的 `posting.txt`，再运行一次 prepare。", ""]
    rows = [(FIELD_NAMES[k], v) for k, v in (fields or {}).items() if k in FIELD_NAMES and isinstance(v, dict) and v.get("value")]
    if rows:
        cell = lambda t: str(t or "").replace("|", "／").replace("\n", " ")  # noqa: E731
        L += ["## 申请须知（岗位库已摘出的字段）", "", "| 项 | 简述 | 公告原句 |", "| --- | --- | --- |"]
        L += [f"| {name} | {cell(v['value'])} | {cell(v.get('quote'))} |" for name, v in rows] + [""]
    L += ["## 需要准备的材料", "", "以下每项都摘自岗位原文；原文没提到的材料不代表不需要，提交前请再读一遍官网。", ""]
    for name, quotes in cl["materials"].items():
        L += [f"- [ ] **{name}**", q(quotes)]
    if not cl["materials"]:
        L.append("- 原文里没找到材料清单（请在官网的 How to apply 部分确认）")
    L += ["", "## 推荐信", "", f"- 原文提到的推荐信 / 推荐人数量：{'、'.join(cl['references']) + ' 封' if cl['references'] else '原文未写明数量'}"]
    for title, key in [("资格与背景要求", "requirements"), ("资助与费用（注意国际生学费差额）", "funding"), ("格式与字数", "format"), ("截止时间与时区", "deadline_time"), ("截止相关原句", "deadline"),
                       ("申请方式", "how"), ("开始时间", "start"), ("面试安排", "interview"), ("联系人", "contact")]:
        if key == "deadline" and cl["deadline_time"]:
            continue
        L += ["", f"## {title}", "", q(cl[key]) if cl[key] else "- 原文未写明"]
    if not cl["deadline_time"]:
        L += ["", "> 截止时刻和时区原文没写：按当地时间当天 00:00 前提交最稳妥，或发邮件确认。"]
    L += ["", "## 提交前自查", "", "- [ ] 文书里每条经历都能在 cv-facts.yml 找到（`apply_check.py check` 通过）",
          "- [ ] 审稿意见已处理（review.md）", "- [ ] 推荐人已提前两周以上联系，并告知截止日期",
          "- [ ] 文件命名、格式（PDF）与字数符合要求", "- [ ] 在 `python scripts/track.py` 看板里把状态改为“已投”", ""]
    return "\n".join(L)


FIELD_NAMES = {"degree": "学位与专业", "language": "语言要求", "start": "开始时间", "duration": "资助 / 合同年限",
               "documents": "材料清单", "apply_via": "申请方式", "supervisor": "导师", "nationality": "国籍 / 学费身份限制"}
LAB_TEMPLATE = """# 导师与课题组信息（起草套磁信只许引用这里的内容；每篇论文必须有可打开的链接）
supervisor:
  name: ''          # 岗位原文里的导师姓名
  homepage: ''      # 官方主页
  group: ''
papers:             # 近 3 年、与岗位课题相关的 2–4 篇；summary 只写摘要里的原话或忠实转述
  # - id: p1
  #   title: ''
  #   year: 2025
  #   venue: ''
  #   url: https://doi.org/...
  #   summary: ''
"""


def cmd_prepare(args) -> int:
    opp = find_opportunity(args.key)
    d = Path(args.out_root) / safe_id(opp["id"])
    (d / "drafts").mkdir(parents=True, exist_ok=True)
    txt = d / "posting.txt"
    if args.text_file:
        txt.write_text(Path(args.text_file).read_text(encoding="utf-8"), encoding="utf-8")
    elif not txt.exists() and not args.no_fetch:
        text = fetch_text(opp["url"])
        if text:
            txt.write_text(text, encoding="utf-8")
    text = txt.read_text(encoding="utf-8") if txt.exists() else ""
    fields = load_fields().get(opp["id"])
    (d / "posting.yml").write_text(yaml.safe_dump({k: v for k, v in opp.items() if v not in (None, "", [])},
                                                  allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    (d / "checklist.md").write_text(checklist_md(opp, extract_checklist(text), fields, bool(text)), encoding="utf-8")
    if not (d / "lab.yml").exists():
        sup = ((fields or {}).get("supervisor") or {}).get("value", "")
        (d / "lab.yml").write_text(LAB_TEMPLATE.replace("name: ''", "name: " + json.dumps(sup, ensure_ascii=False), 1), encoding="utf-8")
    print(f"{d}：posting.yml、checklist.md、lab.yml" + ("、posting.txt" if text else "（缺 posting.txt：网页没取到，请复制原文）"))
    return 0


# ───────────────────────── 导师论文 ─────────────────────────


def cmd_papers(args) -> int:
    """OpenAlex 查作者近期论文。只是候选：写进 lab.yml 前要打开链接确认是同一个人。"""
    import requests

    from scrapers.common import Fetcher

    f = Fetcher(delay=1.0, timeout=25)
    key = os.environ.get("OPENALEX_API_KEY")
    auth = f"&api_key={key}" if key else ""
    try:
        authors = f.get(f"https://api.openalex.org/authors?search={requests.utils.quote(args.name)}&per-page=10{auth}").json()["results"]
    except requests.RequestException as e:
        print(f"OpenAlex 访问失败（{e}）：请改用网页搜索导师主页 / Google Scholar / DBLP，手动填写 lab.yml。")
        return 1
    if args.affil:
        authors = [a for a in authors if args.affil.lower() in str(a.get("last_known_institutions") or a.get("affiliations")).lower()]
    if not authors:
        print("没找到匹配的作者：换个写法或去掉 --affil，或手动填写 lab.yml。")
        return 1
    a = authors[0]
    inst = ", ".join(i.get("display_name", "") for i in a.get("last_known_institutions") or [])
    print(f"# 候选作者：{a['display_name']}（{inst}；{a.get('works_count')} 篇）{a['id']}")
    works = f.get(f"https://api.openalex.org/works?filter=author.id:{a['id'].rsplit('/', 1)[-1]},from_publication_date:{date.today().year - 3}-01-01"
                  f"&sort=publication_date:desc&per-page={args.n}{auth}").json()["results"]
    papers = [{"id": f"p{i}", "title": w.get("title"), "year": w.get("publication_year"),
               "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
               "url": w.get("doi") or w.get("id")} for i, w in enumerate(works, 1)]
    print(yaml.safe_dump({"papers": papers}, allow_unicode=True, sort_keys=False, width=200))
    return 0


# ───────────────────────── 事实校验 ─────────────────────────

META_KEYS = {"source", "extracted", "updated", "version", "schema"}  # cv-facts 的元数据，不是事实
IDENTITY_KEYS = {"name", "name_en", "name_zh", "email", "phone", "homepage", "github", "linkedin", "orcid", "address"}
ALWAYS_OK = {  # 不需要出处的常用词（小写）
    "i", "dear", "prof", "professor", "dr", "phd", "ph.d", "msc", "bsc", "ba", "ma", "mphil", "meng", "beng", "cv", "pdf",
    "sincerely", "regards", "best", "kind", "yours", "faithfully", "thank", "thanks", "english", "chinese", "mandarin",
    "china", "ai", "ml", "nlp", "re", "subject", "gpa", "ects", "wam", "ps", "phdradar", "github", "email", "university", "lab", "group",
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "mr", "ms", "mrs", "ii", "iii", "iv",
}
LEADING = {"the", "a", "an", "in", "during", "at", "as", "this", "these", "my", "our", "your", "since", "after", "before",
           "while", "when", "with", "through", "for", "from", "on", "dear", "best", "kind", "if", "although", "both", "also",
           "furthermore", "moreover", "however", "therefore", "building", "having", "given", "specifically", "recently",
           "currently", "previously", "overall", "finally", "first", "second", "third", "beyond", "under", "to", "and", "of", "re",
           "subject", "would", "could", "please", "thank", "regarding", "about", "following", "looking", "prospective",
           "application", "applicant", "enquiry", "inquiry", "interest", "question", "request", "proposed", "potential",
           "current", "future", "related", "relevant", "possible", "several", "many", "some", "each", "every", "all",
           "most", "here", "there", "what", "which", "how", "why", "it", "its", "that", "those", "then", "now", "today",
           "sincerely", "yours", "warm", "warmest", "warmly", "one", "two", "three", "key", "main", "next", "new", "other"}
CONNECT = {"of", "and", "for", "&", "de", "von", "van", "der", "la", "du"}
ABBR = re.compile(r"\b(Prof|Dr|Mr|Ms|Mrs|e\.g|i\.e|et al|vs|No|Fig|Dept|Univ|approx|cf|St)\.", re.I)
CITE = re.compile(r"\[(cv|lab):\s*([^\]]+)\]|\[post\]")
URL_RE = re.compile(r"https?://[^\s)\]>，。]+")
# 经历句：第一人称 + 非“意向 / 礼貌”类动词，或“my … experience / thesis …”，或“我…过 / 我的硕士…”
NOT_CLAIM = (r"(am|'m) (writing|interested|applying|excited|keen|glad|happy|grateful|eager|available|willing|able|confident|aware|"
             r"looking|hoping|curious|attaching|enclosing|reaching|contacting|sure|not sure|passionate|fascinated|motivated|drawn|delighted|"
             r"honou?red|pleased|particularly|very|really|truly|deeply|most)|would|will|'d|'ll|hope|look|believe|think|wish|want|"
             r"plan|intend|can|could|should|may|might|read|noticed|came across|saw|learned of|understand|see|note|wonder|appreciate|"
             r"apply|(have )?(a |one |two |three |some |a few |several )(specific |short |brief |quick )?(questions?|quer(y|ies))|"
             r"(have |had |do |did |am )?(not|never|no|little|limited)\b|haven't|hadn't|didn't|don't|lack|am name\b|name\b|am also|also (hope|would|wish)|welcome|thank|attach|enclose|apologi[sz]e|feel|find|found your|was (glad|excited|pleased) to")
EXP_EN_NOSUBJ = re.compile(r"^\s*(having|after|since|while|as an?|as the)\s+(served|worked|been|led|completed|studied|interned|taught|published|won|received|developed|built|conducted)\b", re.I)
EXP_EN = re.compile(r"\b(I|I've|I'd|I'm)\s+(?:(?:also|recently|previously|then|further|additionally|currently|have|had|already|personally)\s+)*(?!(?:also|recently|previously|then|further|additionally|currently|have|had|already|personally|" + NOT_CLAIM + r")\b)[a-z0-9]"
                    r"|\bmy\s+(?!(?:background|interests?|motivation|application|cv|questions?|enquiry|inquiry|email|letter|name|availability|plans?|goals?)\b)(?:[\w'-]+\s+){0,2}?(thesis|dissertation|papers?|publications?|projects?|internships?|research|experience|degree|master'?s|bachelor'?s|msc|bsc|gpa|grades?|ranking|"
                    r"supervisor|advisor|award|skills?|first-author|training|expertise|synthesis|testing|experiments?|measurements?|results?|analys[ie]s|stud(y|ies)|code|models?|data|work on|work with)\b", re.I)
EXP_ZH = re.compile(r"(我|本人)(曾|在|参与|负责|主导|发表|获得|获|完成|开发|设计|实现|带领|担任|本科|硕士|毕业|就读|研究了|做过|有.{0,6}(经验|基础|积累))|^曾(担任|在|经|参与|获|负责|主持)|(?<![\w])曾(担任|任|参与|主持)"
                    r"|(我|本人)[^，。,；;！？\s]{0,6}过|我的(硕士|本科|博士|毕业|课题|论文|项目|研究|经历|经验|成绩|排名|技能|背景)"
                    r"|^(已有|我已有|现有)?(方法)?积累[：:]|^已有(方法|技术|经验)")
HYPE = re.compile(r"\b(passionate|world[- ]class|cutting[- ]edge|groundbreaking|ground-breaking|outstanding|exceptional|excellent|perfect (fit|match)|dream|"
                  r"unique opportunity|extremely|highly motivated|hard[- ]?working|truly|deeply|incredibly|amazing|revolutionary|state-of-the-art|"
                  r"always been fascinated|ever since i was)\b|顶尖|极其|非常|卓越|杰出|完美|梦想|热爱|深深|无比|最优秀", re.I)
PLACEHOLDER = re.compile(r"\b(TODO|TBD|XXX|FIXME)\b|\{\{|<[^<>\n]{1,30}>|\[(\?|待补|填写)[^\]]*\]|【[^】]*】")
NAME_ZH = re.compile(r"[一-鿿]{2,15}(大学|学院|研究所|研究院|实验室|公司|医院|中心|奖学金|奖|竞赛|大赛|基金)")
QUOTED = re.compile(r"“([^”]{3,})”|\"([^\"]{3,})\"|《([^》]{2,})》|‘([^’]{3,})’")
YEAR_RANGE = re.compile(r"(?<!\d)((?:19|20)\d\d)\s*(?:[–—-]|to|至|到)\s*((?:19|20)\d\d)(?!\d)")
DURATION_RE = re.compile(r"(?<![\w.])\d+(?:\s*[–—~-]\s*\d+)?\s*(?:个月|月|周|天|年|months?|weeks?|days?|years?)(?![\w])|第\s*\d+\s*(?:年|学期|个月|阶段)|\b(?:year|month|phase|stage)\s+\d+\b", re.I)
RATIO_RE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?\s*[/:]\s*\d+(?:\.\d+)?(?![\w])")
NUM_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
ZH_NUM = {"两": "2", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9", "十": "10"}


# 身份 / 状态 / 角色类说法：句中出现了，所引出处里就必须有同义说法（防止“在审”写成“已接收”、二作写成一作、参与写成主导）
CLAIMS = [
    ("第一作者", r"\bfirst[- ]author(ed)?\b|\blead author\b|第一作者|一作", r"first[- ]author|lead author|第一作者|一作|共同一作"),
    ("共同第一作者", r"\bco-?first\b|\bequal contribution\b|共同一作|共同第一", r"co-?first|equal contribution|共同一作|共同第一"),
    ("通讯作者", r"\bcorresponding author\b|通讯作者", r"corresponding author|通讯作者"),
    ("已接收", r"\baccepted\b|\bin press\b|已接收|被接收|已被.{0,40}接受|录用", r"accepted|in press|接收|录用|published|发表"),
    ("已发表", r"\bpublished\b|\bappeared in\b|已发表|发表于|发表在", r"published|appeared|发表|\b(19|20)\d\d\b.*(journal|proceedings|conference)|accepted"),
    ("口头报告 / 亮点", r"\b(oral|spotlight)( presentation| talk)?\b|口头报告", r"oral|spotlight|口头报告"),
    ("最佳论文", r"\bbest (paper|poster|student paper)\b|最佳论文", r"best (paper|poster|student paper)|最佳论文"),
    ("专利", r"\bpatents?\b|专利", r"patent|专利"),
    ("主导 / 带领", r"\bI (led|headed|directed|supervised|managed)\b|\bas (the )?(team |project |course project )?lead(er)?\b|\bwas (the )?(\w+ ){0,3}(lead|leader|head|coordinator)\b|主导|主持|带领|领导了|负责人|组长|带头", r"\blead\b|\bled\b|leader|\bheaded\b|\bsupervised\b|\bmanaged\b|主导|主持|带领|负责人|组长"),
    ("独立完成", r"\bindependently\b|\bsingle-handedly\b|\bon my own\b|\bby myself\b|\b(built|designed|wrote|developed|did|ran|implemented|made|created)\b[^.]{0,60}\bmyself\b|\bfrom scratch\b|\b(mostly|largely|entirely) my own\b|\bmy own work\b|\bmain contribution\b|\bsole\b|独立(完成|设计|运行|开展|搭建|负责|操作)|独自|一人完成|主要贡献|均由我|全部由我|都由我",
     r"independent|sole|from scratch|main contribution|独立|独自|主要贡献"),
    ("排名", r"\b(top|ranked|ranking)\b|排名|前\s*\d+\s*%", r"top|rank|排名|前\s*\d"),
    ("奖项 / 奖学金", r"\b(award(ed)?|prize|scholarship|fellowship|medal|honou?r)s?\b|奖学金|获奖|奖项|荣誉", r"award|prize|scholarship|fellowship|medal|honou?r|奖"),
    ("设计 / 开发 / 搭建", r"\b(designed|developed|built|invented|created|devised|founded|constructed|engineered)\b|设计了|开发了|搭建|研制|发明",
     r"design|develop|built|build|implement|creat|propos|construct|wrote|invent|设计|开发|搭建|实现|编写|构建|研制"),
    ("影响 / 被采用", r"\b(widely |highly |well )?cited\b|\bcitations?\b|\b(adopted|deployed|used) by\b|\bnow (used|in use)\b|\bfeatured\b|\bcover\b|\bmedia\b|被引|被采用|封面|报道",
     r"cit(ed|ation)|adopted|deployed|used by|featured|cover|media|被引|采用|封面|报道"),
    ("首次 / 新颖", r"\bnovel\b|\bnever (been )?(reported|done|seen)\b|\bfor the first time\b|\bfirst to\b|\bpioneer|首次|首创|开创|填补.{0,4}空白",
     r"novel|first time|never|首次|首创"),
    ("结论强度", r"\b(completely|entirely|fully) (eliminat|solv|prevent|remov|suppress)|\bproved?\b|\bguarantee|\boutperform|\bstate-of-the-art\b|\bsignificantly\b|\bsuperior\b|彻底|完全(消除|解决)|证明了|显著|明显(提|改|延|降|增)|大幅|极大|优于|翻倍|\bdoubled\b|\bhalved\b|\b\w+fold\b",
     r"complete|entire|eliminat|prov(ed|e)|guarantee|outperform|state-of-the-art|significant|superior|彻底|完全|证明|显著|优于"),
    ("责任范围", r"\b(responsible for|in charge of|oversaw|oversee)\b|全权|负责全部|负责整个", r"responsib|in charge|oversaw|lead|led|manag|负责"),
    ("全称量词", r"\b(all of (them|which|these|the)|all \d+|every one|each of (them|the)|in each (section|case|of)|without exception|in every case|consistently)\b|全部|所有|均达到|均不低于|均(在|为|达)|每项|各项|无一例外|每一",
     r"\ball\b|every|each|consistent|全部|所有|均"),
    ("成果物", r"\b(posters?|open[- ]source|packages?|software|librar(y|ies)|datasets?|patents?|talks?|preprints?|app|website|tool ?kit)\b|海报|口头报告|软件|代码库|开源|数据集|专利|小程序",
     None),
    ("熟练程度", r"\b(extensive|extensively|proficien\w*|expert\w*|advanced|strong command|fluent\w*|mastery|in-depth|deep (knowledge|expertise)|routinely|regularly|frequently|years of)\b|长期|丰富|深厚|娴熟|精通|熟练|扎实|深入",
     None),
    ("独占", r"\b(the only|the sole|sole operator|exclusively)\b|唯一", None),
    ("职位身份", r"\b(teaching assistants?|TA|intern(ship)?s?|staff|employee|technician|engineer|manager|lecturer|tutor|instructor|postdoc)\b|助教|实习|员工|职员|技术员|工程师|讲师|正式",
     None),
    ("指导培训他人", r"\b(mentor(ed|ing)?|train(ed|ing)? (new|junior|other|students|colleagues|volunteers)|taught|supervis(ed|ing) (students|juniors|undergraduates))\b|培训了?|指导了?(新|学弟|学妹|本科)|带(过|了)?(新同学|学生)",
     r"mentor|train|taught|teach|supervis|培训|指导|带教"),
    ("名次", r"\branked (first|second|third|top|\d+(st|nd|rd|th))\b|\b\d+(st|nd|rd|th) (out )?of \d+|第[一二三四五六七八九十\d]+名|排名第", None),
    ("论文用途", r"用于(发表|论文)|数据已(发表|用于)|\b(data|results) (were|was|have been) (published|used in)\b", None),
    ("频率", r"\b(every (day|week|month)|daily|weekly|monthly|twice a (day|week|month)|once a (day|week|month)|three times a (day|week))\b|每天|每周|每月|每日",
     None),  # 频率说法原样出现在出处里才行
    ("研究结论", r"\b(showed|shows|demonstrated|revealed|found|established|concluded|confirmed) that\b|结果表明|发现了?|结论(是|为)|证实|揭示|得出", r"show|demonstrat|reveal|found|result|kept|reduced|improv|表明|发现|结果"),
]


# 学位层次：句子说“硕士 / 本科 / 博士”，所引出处必须是同一层次（防止把本科的事写到硕士名下）
DEGREES = [
    ("硕士", r"硕士|研究生阶段|\bmaster'?s\b|\bM\.?Sc\b|\bM\.?Eng\b|\bMPhil\b|\bMRes\b|\bM\.?A\.?\b(?= (in|degree))"),
    ("本科", r"本科|学士|\bbachelor'?s\b|\bundergraduate\b|\bB\.?Sc\b|\bB\.?Eng\b|\bB\.?A\.?\b(?= (in|degree))"),
    ("博士", r"博士(?!后|生岗位|项目|奖学金)|\bdoctoral (thesis|research|studies)\b|\bmy PhD\b"),
]


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    s = re.sub(r"'s\b", "", s.lower())
    s = re.sub(r"[^\w&+#.\-/ 一-鿿]", " ", s)
    return re.sub(r"\s+", " ", s).strip(" .")


def num_norm(n: str) -> str:
    n = n.replace(",", "")
    if "." in n:
        n = n.rstrip("0").rstrip(".")
    return n.lstrip("0") or "0"


def numbers_in(text: str) -> set[str]:
    out = {num_norm(n) for n in NUM_RE.findall(text)}  # 不收“L8 R8.5”里贴着字母的分项分：否则总分写成 8.0 也能通过
    for m in re.finditer(r"\b(" + "|".join(list(NUM_WORDS)[2:]) + r")\b", text, re.I):
        out.add(NUM_WORDS[m.group(1).lower()])
    for m in re.finditer(r"(?<!第)([两二三四五六七八九十])(篇|项|个|次|年|门|份|位|届|名)", text):
        out.add(ZH_NUM[m.group(1)])
    return out


def flatten(v) -> str:
    if isinstance(v, dict):
        return " ".join(flatten(x) for x in v.values())  # 只取值：键名（supervisor、award…）不能当出处
    if isinstance(v, list):
        return " ".join(flatten(x) for x in v)
    return "" if v is None else str(v)


def fact_index(data, prefix: str = "") -> dict[str, str]:
    """把 cv-facts / lab.yml 拆成 {出处 id: 原文}：带 id 的条目用 id，列表项无 id 用“节名.序号”，其余整节用节名。"""
    out: dict[str, str] = {}
    if not isinstance(data, dict):
        return out
    for key, val in data.items():
        if key in IDENTITY_KEYS or key in META_KEYS:
            continue
        if isinstance(val, list) and any(isinstance(x, dict) for x in val):
            for i, it in enumerate(val, 1):
                fid = str(it.get("id")) if isinstance(it, dict) and it.get("id") else f"{key}.{i}"
                out[fid] = flatten(it)
        elif isinstance(val, dict) and val and all(isinstance(x, (dict, list)) for x in val.values()) and key not in ("supervisor",):
            out.update({f"{key}.{k}" if not k.startswith(key) else k: v for k, v in fact_index(val).items()})
            out[key] = flatten(val)
        else:
            out[key] = flatten(val)
    return out


def identity_text(facts: dict, profile: dict | None = None) -> str:
    """申请者姓名与联系方式：cv-facts.yml 顶层的 name / email 等，或 profile.yml 里的同名字段。"""
    vals = [flatten(d.get(k)) for d in (facts, profile or {}) for k in IDENTITY_KEYS if isinstance(d, dict) and d.get(k)]
    for k in ("profile", "basics", "person"):  # 兼容把身份信息放在子节的写法
        if isinstance(facts.get(k), dict):
            vals += [flatten(v) for kk, v in facts[k].items() if kk in IDENTITY_KEYS]
    return " ".join(vals)


def split_sentences(text: str) -> list[tuple[int, str]]:
    """逐行切句（保留行号）；缩写里的点不切；只有出处标记的片段并回前一句。"""
    out: list[tuple[int, str]] = []
    in_code = False
    for ln, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip() or line.strip().startswith("<!--"):
            continue
        line = re.sub(r"^\s*(#+|[-*+]|\d+[.)]|>)\s+", "", line)
        safe = ABBR.sub(lambda m: m.group(0).replace(".", "\x00"), line)
        for part in re.split(r"(?<=[.!?])\s+(?=\S)|(?<=[。！？])\s*(?=\S)", safe):
            part = part.replace("\x00", ".").strip()
            if not part:
                continue
            if out and out[-1][0] == ln and not CITE.sub("", part).strip(" .。"):
                out[-1] = (ln, out[-1][1] + " " + part)
            else:
                out.append((ln, part))
    return out


def proper_names(s: str) -> list[str]:
    """连续的大写开头词（中间允许 of/and 等）、缩写与驼峰词（NeurIPS、MIT、PyTorch）。
    句首的常用词（LEADING）去掉；句首的其他大写词照样算，所以“Northbridge University awarded …”也会被查。"""
    toks = re.findall(r"[A-Za-z][A-Za-z0-9&'’+.\-]*[A-Za-z0-9+]|[A-Za-z]|&|[,;:()]", s)
    runs, cur = [], []
    for t in toks + ["."]:
        if (t[0].isupper() and t not in ("I", "I'm", "I've", "I'd")) or (cur and t.lower() in CONNECT):
            cur.append(t)
            continue
        while cur and cur[-1].lower() in CONNECT:
            cur.pop()
        if cur:
            runs.append(cur)
        cur = []
    out = []
    for run in runs:
        while run and run[0].lower() in LEADING:
            run = run[1:]
        while run and run[-1].lower() in CONNECT:
            run = run[:-1]
        if not run:
            continue
        caps = [t for t in run if t[0].isupper()]
        acronym = len(run) == 1 and len(re.findall(r"[A-Z]", run[0])) >= 2
        if len(caps) >= 2 or acronym:
            name = re.sub(r"['’]s$", "", " ".join(run))
            if norm(name) not in ALWAYS_OK and not all(norm(t) in ALWAYS_OK for t in run):
                out.append(name)
    return out


def is_initialism(acr: str, allowed_n: str) -> bool:
    """OCT ← optical coherence tomography、MALA ← Metropolis-adjusted Langevin algorithm：缩写由出处里连续几个词的首字母组成。"""
    acr = acr.lower()
    if not 2 <= len(acr) <= 6 or not acr.isalpha():
        return False
    ws = [w for w in re.split(r"[\s\-/]+", allowed_n) if w]
    return any("".join(w[0] for w in ws[i:i + len(acr)]) == acr for i in range(len(ws) - len(acr) + 1))


def covered(name: str, allowed_n: str, words: set[str]) -> bool:
    """名称能否被出处原文拼出来：从左到右取出处里出现过的最长连续片段；单个词必须在出处里单独出现过（或是常用词）。"""
    if " " not in name.strip() and is_initialism(name.strip(), allowed_n):
        return True
    toks = norm(name).split()
    i = 0
    while i < len(toks):
        for j in range(len(toks), i, -1):
            seg = " ".join(toks[i:j])
            if (j - i > 1 and re.search(r"(?<![\w])" + re.escape(seg) + r"(?![\w])", allowed_n)) or (j - i == 1 and (seg in words or seg in ALWAYS_OK or seg in CONNECT)):
                i = j
                break
        else:
            return False
    return True


STOP = set("""about above after again also among because been before being below between both could does doing during each
from further have having here into just more most other over same should some such than that their them then there these they
this those through under until very were what when where which while will with would your yours ours mine, the and for are was
using used based work worked project projects research thesis paper papers experience including include within""".split())


def content(text: str) -> set[str]:
    """内容词：英文 ≥4 个字母的非停用词（去掉复数 s），中文按两字一组。"""
    words = {w.rstrip("s") for w in re.findall(r"[a-z][a-z\-]{3,}", text.lower()) if w not in STOP}
    zh = "".join(re.findall(r"[一-鿿]+", text))
    return words | {zh[i:i + 2] for i in range(len(zh) - 1)}


def misattributed(body: str, cited: list[str], facts: dict[str, str]) -> str | None:
    """句子内容和所引出处几乎不重合、却和另一条事实高度重合 → 出处可能张冠李戴。"""
    S = content(body)
    if len(S) < 3 or not cited:
        return None
    own = len(S & content(" ".join(facts.get(i, "") for i in cited))) / len(S)
    best, bid = max(((len(S & content(t)) / len(S), i) for i, t in facts.items() if i not in cited), default=(0, None))
    if own < 0.2 and best >= own + 0.25:
        return f"句子内容与 [cv:{','.join(cited)}] 对不上，更像 [cv:{bid}]"
    english = len(re.findall(r"[一-鿿]", body)) < 4
    if english and len(S) >= 4 and own < 0.15:
        return f"句子内容在 [cv:{','.join(cited)}] 里几乎找不到依据"
    return None


# —— 白名单：带 [cv:…] 的句子里，实词（动词、名词、形容词）的词干必须在所引出处里（同义词组互通）——
# 黑名单（CLAIMS）挡不住同义改写（ran / coordinated / mentored / set up…），所以经历句反过来要求“出处里有才许写”。
SYNONYMS = [
    "implement build built develop code coded program wrote write creat construct set setup install configur establish",
    "run ran conduct perform carri complet undertak did do done",
    "measur quantif record monitor track assess",
    "analy process evaluat comput",
    "synthe prepar made make fabric",
    "assist help support contribut",
    "operat maintain handl",
    "studi study investig research examin explor",
    "use used using appli employ utili",
    "obtain earn receiv award won win achiev score scored hold held gain",
    "author wrote write draft",
    "lead led leader coordinat manag supervis direct head",
    "cycle cycled test tested assembl",
    "estimat infer",
    "reduc lower decreas cut",
    "improv increas boost",
    "survey transect",
    "characteri",
    "rank ranking ranked top placed",
    "publish published appear appeared",
]
SYN = {}
for _g in SYNONYMS:
    _ws = set(_g.split())
    for _w in _ws:
        SYN.setdefault(_w, set()).update(_ws)
GENERIC = set("""also about across after alongside another around based before between both closely
directly during especially final focus focused focusing further including interest interested itself least main mainly
more most other overall particularly previous previously recent recently related relevant second similar specifically such
their there these thing those through together toward towards using very well where which while with within would years
months weeks project projects research work worked experience experiences thesis dissertation degree paper papers study course
team group school university department cohort student students studentship position advert area areas topic topics
approach method methods results result background skills skill programme program master masters bachelor bachelors msc bsc
phd doctoral member aspects aspect part parts kind kinds level levels basic basics hands involved involving include includes
gave give given role took take taken this that what them they from have been being into onto upon over under than then
each every some many much several various same different able ability help reading writing listening speaking
sub-scores subscores band bands section sections overall certificate certification qualification qualifications data use uses
like start starting date dates close closest only applicant applicants limited learning learn statement technical separately
score scored scores author authors studies studied among interests enquiry regarding could should might
january february march april june july august september october november december""".split())
# 出处常是中文转述 + 英文原句：常见词的中英对应，英文句子里的词在中文出处里出现也算有依据
BILINGUAL = {"analys": "分析", "analyz": "分析", "coral": "珊瑚", "exper": "实验|经历|经验", "data": "数据", "batter": "电池",
             "cell": "电池|细胞", "model": "模型", "sampl": "样品|样本|采样", "surve": "调查|调研", "measu": "测|测量", "synth": "合成",
             "struc": "结构", "simul": "模拟|仿真", "fluor": "荧光", "photo": "光", "therm": "热", "heat": "热", "aquar": "水族|养殖",
             "volun": "志愿", "maint": "维护", "opera": "操作", "field": "野外|实地", "certi": "证书", "divin": "潜水", "diver": "潜水",
             "stati": "统计", "first-author": "第一作者|一作|first author", "second-author": "第二作者|二作|second author", "appea": "发表|publish", "ranki": "排名|top", "gpa": "绩点|均分", "stude": "学生", "thesi": "论文", "paper": "论文", "publi": "发表", "schol": "奖学金", "award": "奖",
             "assis": "协助|助理", "resea": "研究", "super": "导师|prof\\.|dr\\.|supervisor", "proje": "项目|课题", "cours": "课程", "teamw": "团队", "team": "团队|小组"}
DEGREE_VERBS = {"completed", "complete", "hold", "holding", "obtained", "earned", "graduated", "awarded", "finished", "studied"}


def stem_ok(word: str, own_words: set[str], own_text: str) -> bool:
    w = word.lower()
    if w in GENERIC or w in STOP or len(w) < 4 and w not in SYN:
        return True
    zh = next((v for k, v in BILINGUAL.items() if w.startswith(k)), None)
    if zh and re.search(zh, own_text):
        return True
    if w in DEGREE_VERBS and re.search(r"\b(msc|bsc|ba|ma|meng|beng|mphil|mres|phd|degree|master|bachelor|certificate|diver|licen[cs]e)|学士|硕士|博士|学位|证书", own_text):
        return True  # “I completed my MSc …”：学位条目本身就是完成 / 获得
    cands = {w[:5]} | {x[:5] for x in SYN.get(w, ())} | {x[:5] for k, v in SYN.items() if w.startswith(k) for x in v}
    return any(c in own_words for c in cands)  # 只按词首比：子串会让 simplex 里的 imple、cycled 里的 led 冒充依据


def unsupported_words(seg: str, own: str) -> list[str]:
    """英文实词：出处里（按前 5 个字母的词干或同义词组）找不到的词。"""
    own_l = own.lower()
    own_words = {t[:5] for t in re.findall(r"[a-z]{3,}", own_l)}
    words = [w for t in re.findall(r"(?<![\w-])[A-Za-z][a-z\-]{2,}(?![\w-])", seg) for w in t.split("-") if len(w) >= 3]  # 连字符词拆开比
    return list(dict.fromkeys(w for w in words if not stem_ok(w, own_words, own_l)))


def segments(s: str) -> tuple[list[tuple[str, list[str]]], str]:
    """按出处标记把句子切成片段：每段文字归它后面紧跟的那个标记；最后一个标记之后的尾巴单独返回（当作没有出处的话检查）。"""
    out, last, cites = [], 0, list(CITE.finditer(s))
    for m in cites:
        out.append((s[last:m.start()], [m.group(0)]))
        last = m.end()
    return out, (s[last:] if cites else "")


UNIT_ZH = {"week": "周", "month": "月", "day": "天|日", "year": "年", "tank": "缸", "cell": "电池|个", "cycle": "圈|次|循环",
           "cluster": "团簇|种", "paper": "篇", "student": "名|位|人", "member": "名|位|人", "people": "名|位|人", "sample": "个|份"}
SECTIONS = {"l": "listening|听力", "r": "reading|阅读", "w": "writing|写作", "s": "speaking|口语"}


def digits(text: str) -> str:
    return re.sub(r"\b(" + "|".join(list(NUM_WORDS)[2:]) + r")\b", lambda m: NUM_WORDS[m.group(1).lower()], text, flags=re.I)


def unit_mismatch(text: str, own: str) -> list[str]:
    """数字要带着出处里的单位：出处是“6-week … 12-tank”，句子写“12 weeks”就不对（只比英文单位；出处是中文时查对应字）。"""
    own_d = digits(own).lower()
    out = []
    for m in re.finditer(r"(?<![\w./])(\d+(?:\.\d+)?)(?:\s*-\s*|\s+)(?:(?:more|than|of|the|my|our)\s+)?([a-z]{3,})", digits(text).lower()):
        n, unit = m.group(1), m.group(2)
        if unit in STOP or unit in GENERIC and unit not in ("years", "months", "weeks"):
            continue
        hits = [o for o in re.finditer(r"(?<![\w./])" + re.escape(n) + r"(?![\w.]|\.\d)", own_d)]
        if not hits:
            continue  # 数字本身不在出处里，另有规则报错
        u4, zh = unit[:4], next((v for k, v in UNIT_ZH.items() if unit.startswith(k)), None)
        ok = False
        for o in hits:
            after = own_d[o.end():o.end() + 40]
            before = own_d[max(0, o.start() - 30):o.start()]
            nxt = re.findall(r"[a-z]{3,}", after)[:3]
            if any(w.startswith(u4) for w in nxt) or u4 in before.split()[-2:] or any(w.startswith(u4) for w in before.split()[-2:]):
                ok = True
            elif zh and re.match(r"\s*(" + zh + ")", after):
                ok = True
            elif not re.match(r"\s*-?\s*[a-z]", after) and not (zh is None and re.match(r"\s*[一-鿿]", after)):
                ok = ok or not nxt[:1] and not re.match(r"\s*[一-鿿]", after)
        if not ok:
            out.append(f"{n} {unit}")
    for m in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(%|percent|个百分点)", text):  # 百分数要和出处里的百分数一致
        if not re.search(r"(?<![\w.])" + re.escape(m.group(1)) + r"\s*(%|percent)", own_d):
            out.append(m.group(1) + "%")
    return out


def tense_error(text: str, own: str, today: date | None = None) -> bool:
    """句子说“正在 / currently”，所引条目却已经结束（结束日期早于今天，且没写在读 / expected）。"""
    if not re.search(r"\b(currently|now|ongoing|at present|presently|still)\b|正在|目前(在|正)|至今", text, re.I):
        return False
    if re.search(r"ongoing|expected|present|至今|在读|预计", own, re.I):
        return False
    ends = re.findall(r"((?:19|20)\d\d)-(\d\d)", own)
    if not ends:
        return False
    y, m = max((int(a), int(b)) for a, b in ends)
    t = today or date.today()
    return (y, m) < (t.year, t.month)


def check_sentence(s: str, facts: dict[str, str], lab: dict[str, str], post: str | None, base: str) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    cited_cv, cited_lab, cited_post = [], [], False
    for m in CITE.finditer(s):
        if m.group(0) == "[post]":
            cited_post = True
            continue
        ids = [i.strip() for i in m.group(2).split(",") if i.strip()]
        (cited_cv if m.group(1) == "cv" else cited_lab).extend(ids)
    for i in cited_cv:
        if i not in facts:
            errs.append(f"出处 [cv:{i}] 在 cv-facts.yml 里不存在")
    for i in cited_lab:
        if i not in lab:
            errs.append(f"出处 [lab:{i}] 在 lab.yml 里不存在")
    if cited_post and post is None:
        errs.append("引用了 [post] 但没有 posting.txt")
    body = CITE.sub("", s)
    allowed = " ".join([base] + [facts.get(i, "") for i in cited_cv] + [lab.get(i, "") for i in cited_lab] + ([post or ""] if cited_post else []))
    allowed_n = norm(allowed)
    n_cited = len(cited_cv) + len(cited_lab)
    nums = numbers_in(allowed) | ({str(n_cited)} if n_cited >= 2 else set())  # “两个项目 [cv:proj1,proj2]”
    urls = URL_RE.findall(body)
    text = URL_RE.sub(" ", body)
    for u in urls:
        if u.rstrip("/.") not in allowed:
            errs.append(f"网址不在出处里：{u}")
    compact = re.sub(r"\s+", "", allowed)
    for r in RATIO_RE.findall(text):  # 3.82/4.0、3/62、8:1 这类比值整体核对
        if re.sub(r"\s+", "", r) not in compact:
            errs.append(f"比值 {r} 不在所引出处里")
    for a, b in YEAR_RANGE.findall(text):  # 2023–2024：两个年份要在出处里按顺序挨着出现
        if not re.search(a + r"\D{1,12}" + b, allowed) and a != b or a == b and not re.search(a + r"\D{1,12}" + a, allowed):
            errs.append(f"年份区间 {a}–{b} 与所引出处不符")
    plan_nums: set[str] = set()
    if not (cited_cv or EXP_EN.search(text) or EXP_ZH.search(text)):  # 不讲经历的句子里，计划用的时长（前 6 个月、Year 1）不算事实
        for m in list(DURATION_RE.finditer(text)) + list(re.finditer(r"\b(\d+|two|three|four)\s+(\w+\s+)?(questions?|quer(y|ies))\b", text, re.I)):
            plan_nums |= numbers_in(m.group(0))
    for m in re.finditer(r"(?<![A-Za-z])([LRWS])\s?(\d+(?:\.\d+)?)", allowed):  # 雅思分项“L8 R8.5”：句子提到对应分项才算
        if re.search(SECTIONS[m.group(1).lower()], text, re.I):
            nums.add(num_norm(m.group(2)))
    if cited_cv:  # 雅思 / 托福分项分：句子讲某一分项的分数，出处里要有这一分项（“L8 R8.5”）
        for m in re.finditer(r"\b(listening|reading|writing|speaking)\b[^.;,，。]{0,25}?(\d+(?:\.\d+)?)|(听力|阅读|写作|口语)[^.;,，。]{0,10}?(\d+(?:\.\d+)?)", text, re.I):
            sec, val = (m.group(1) or m.group(3)), (m.group(2) or m.group(4))
            letter = {"listening": "L", "reading": "R", "writing": "W", "speaking": "S", "听力": "L", "阅读": "R", "写作": "W", "口语": "S"}[sec.lower()]
            if not re.search(r"(?<![A-Za-z])" + letter + r"\s?" + re.escape(val) + r"(?![\d.])", allowed):
                errs.append(f"分项成绩 {sec} {val} 在所引出处里找不到")
    for n in sorted(numbers_in(text) - nums - plan_nums):
        errs.append(f"数字 {n} 不在所引出处里")
    for groups in QUOTED.findall(text):
        t = next(g for g in groups if g)
        if norm(t) and norm(t) not in allowed_n:
            errs.append(f"标题 / 引语不在所引出处里：“{t}”")
    words = set(allowed_n.split())
    for name in proper_names(text):
        if not covered(name, allowed_n, words):
            errs.append(f"专有名词不在所引出处里：{name}")
    for m in NAME_ZH.finditer(text):
        if norm(m.group(0)) not in allowed_n:
            errs.append(f"专有名词不在所引出处里：{m.group(0)}")
    if cited_cv and not cited_post and not cited_lab:
        own = " ".join(facts.get(i, "") for i in cited_cv)
        for label, rx in DEGREES:
            if re.search(rx, text, re.I) and not re.search(rx, own, re.I):
                errs.append(f"句子说的是{label}阶段，所引出处里没有{label}")
    if cited_cv:  # 只查申请者自己的经历句；讲导师论文或岗位的句子不受此限
        own = " ".join(facts.get(i, "") for i in cited_cv)
        counted = len(cited_cv) >= 2 and re.search(r"\b(two|three|four|both|\d+)\s+(\w+[- ])?\w+|[两二三四]\s*[篇项个]", text, re.I)
        plain = text
        for nm in proper_names(text):  # “PADI Advanced Open Water Diver”里的 Advanced 不是熟练程度
            plain = plain.replace(nm, " ")
        for label, said, need in CLAIMS:
            m = re.search(said, plain, re.I)
            if not m:
                continue
            rx = need or re.escape(m.group(0))
            if not re.search(rx, own, re.I):
                errs.append(f"“{label}”的说法在所引出处里找不到" + (f"：{m.group(0)}" if need is None else ""))
            elif counted and not all(re.search(rx, facts.get(i, ""), re.I) for i in cited_cv):
                errs.append(f"“{label}”的说法不是每条所引出处都有（“两篇一作”要求两条出处都是一作）")
    segs, tail = segments(s)
    for seg, marks in segs:  # 标 [post] / [lab] 的那段只能讲岗位或论文，不能夹带自己的经历
        if not marks[0].startswith("[cv:") and (EXP_EN.search(seg) or re.search(r"(我|本人)(曾|有|做过|用过|操作过|参与|负责|完成|掌握)", seg)):
            errs.append(f"{marks[0]} 那一段写了自己的经历：经历要标 [cv:…] 出处")
    if cited_cv:
        own_all = " ".join(facts.get(i, "") for i in cited_cv)
        for m in re.finditer(r"\b(graduated|completed|finished|obtained|received|awarded|earned)\b[^.;]{0,80}?\b(?:in|by)\s+((?:19|20)\d\d)\b|((?:19|20)\d\d)\s*年?毕业", text, re.I):
            y = m.group(2) or m.group(3)
            ends = [int(a) for a, _ in re.findall(r"((?:19|20)\d\d)-(\d\d)", own_all)] or [int(a) for a in re.findall(r"(?<!\d)((?:19|20)\d\d)(?!\d)", own_all)]
            if ends and int(y) != max(ends):
                errs.append(f"毕业 / 获得年份 {y} 与所引条目的结束年份 {max(ends)} 不符")
    if tail.strip(" .。,，;；?？!！") and (EXP_EN.search(tail) or EXP_ZH.search(tail)):
        errs.append("出处标记后面又写了经历：请把这部分也标上出处，或把标记移到句末")
    for seg, marks in segs:  # 每段只能用它自己那个出处
        m = CITE.match(marks[0])
        if m and m.group(1) == "cv":
            ids = [i.strip() for i in m.group(2).split(",") if i.strip() in facts]
            if not ids:
                continue
            seg_text = re.sub(r"\b(" + "|".join(list(NUM_WORDS)[2:]) + r")\b", lambda m: NUM_WORDS[m.group(1).lower()], URL_RE.sub(" ", seg), flags=re.I)
            for nm in proper_names(seg_text):
                seg_text = seg_text.replace(nm, " ")
            bad = [w for w in unsupported_words(seg_text, " ".join(facts[i] for i in ids) + " " + base) if not re.search(r"[一-鿿]", w)]
            if bad:  # 词表层面的检查惩罚改写多于拦住编造（第二轮红队），降为“需核对”，交给证据核对（review.yml）
                warns.append(f"需核对：这些词在 [cv:{','.join(ids)}] 里没出现：{'、'.join(bad[:6])}")
    if cited_cv:
        own = " ".join(facts.get(i, "") for i in cited_cv)
        cv_text = " ".join(seg for seg, marks in segments(s)[0] if marks[0].startswith("[cv:"))
        for um in unit_mismatch(cv_text, own):
            errs.append(f"数字与单位和出处对不上：{um}")
        if tense_error(text, own):
            errs.append("句子说“正在 / currently”，但所引条目已经结束")
        if re.search(r"\bmy (own )?(\w+ ){0,2}(paper|publication|article|study|discovery|finding|work)s?\b|\bis my (own )?work\b|\bI (discovered|found|showed|demonstrated|wrote the paper)\b|我的(论文|文章|发现|工作|成果)", text, re.I) \
                and re.search(r"second[- ]author|third[- ]author|co-?author|第[二三四]作者|二作|三作", own, re.I) and not re.search(r"first[- ]author|第一作者|一作", own, re.I):
            errs.append("出处不是第一作者论文：要写明作者位次，不能说成“我的论文 / 我发现”")
    if cited_cv and all(i in facts for i in cited_cv):
        why = misattributed(re.sub(r"\[(lab|post)[^\]]*\]", "", body), cited_cv, facts) if not (cited_lab or cited_post) else None
        if why:
            errs.append(why)
    if not cited_cv and not cited_lab and not cited_post:
        for label, said, _ in CLAIMS[:9]:  # 一作、已接收、最佳论文、主导等强说法，没有出处不许写
            if re.search(said, text, re.I):
                errs.append(f"“{label}”的说法没有标注出处")
    named = text
    for nm in proper_names(text):  # “I am Lin Xiaozhou”：申请者 / 导师姓名不算经历
        if covered(nm, norm(base), set(norm(base).split())):
            named = named.replace(nm, "name")
    if not cited_cv and (EXP_EN.search(named) or EXP_ZH.search(text) or EXP_EN_NOSUBJ.search(text)):
        errs.append("经历句没有标注 [cv:…] 出处")
    if PLACEHOLDER.search(text):
        errs.append(f"有未填的占位符：{PLACEHOLDER.search(text).group(0)}")
    for m in HYPE.finditer(text):
        warns.append(f"空话 / 夸张用词：{m.group(0)}")
    return errs, warns


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None


def find_facts(arg: str | None) -> Path:
    for p in [arg, os.environ.get("PHDRADAR_FACTS")] + FACT_PATHS:
        if p and (ROOT / p if not Path(p).is_absolute() else Path(p)).exists():
            return ROOT / p if not Path(p).is_absolute() else Path(p)
    raise SystemExit("找不到 cv-facts.yml：先运行 /setup 生成，或用 --facts 指定路径")


def check_dir(d: Path, facts_data: dict, profile: dict | None = None) -> dict:
    """校验 d/drafts/*.md；返回 {文件: {"errors": [(行, 句, 问题)], "warnings": [...]}}。"""
    facts = fact_index(facts_data)
    lab_data = load_yaml(d / "lab.yml") or {}
    lab = fact_index(lab_data)
    opp = load_yaml(d / "posting.yml") or {}
    post = (d / "posting.txt").read_text(encoding="utf-8") if (d / "posting.txt").exists() else None
    sup = lab_data.get("supervisor") or {}
    base = " ".join([identity_text(facts_data, profile), str(opp.get("title", "")), str(opp.get("org", "")), str(opp.get("url", "")),
                     flatten(sup) if isinstance(sup, dict) else str(sup)])
    date_line = re.compile(r"^\s*(\d{1,2} \w+ \d{4}|\w+ \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2}|\d{4}年\d{1,2}月\d{1,2}日)\s*$")
    out = {}
    files = sorted((d / "drafts").glob("*.md")) if (d / "drafts").exists() else []
    for f in files:
        res = {"errors": [], "warnings": []}
        for ln, s in split_sentences(f.read_text(encoding="utf-8")):
            if date_line.match(s):
                continue
            errs, warns = check_sentence(s, facts, lab, post, base)
            res["errors"] += [(ln, s, e) for e in errs]
            res["warnings"] += [(ln, s, w) for w in warns]
        out[f.name] = res
    return out


# —— 证据核对（第二层）：审稿子代理为每句经历摘出 cv-facts 里的原文作证据，程序核对证据真的在所引出处里 ——
def sentence_key(s: str) -> str:
    import hashlib
    return hashlib.sha1(norm(CITE.sub("", s)).encode()).hexdigest()[:10]


def cv_sentences(d: Path, facts: dict[str, str]):
    """drafts 里所有带 [cv:…] 的句子：(文件, 行, 句子, 所引 id)。"""
    for f in sorted((d / "drafts").glob("*.md")) if (d / "drafts").exists() else []:
        for ln, s in split_sentences(f.read_text(encoding="utf-8")):
            ids = [i.strip() for m in CITE.finditer(s) if m.group(1) == "cv" for i in m.group(2).split(",") if i.strip()]
            if ids:
                yield f.name, ln, s, ids


def evidence_template(d: Path, facts_data: dict, profile: dict | None = None) -> list[dict]:
    """生成 / 更新 evidence.yml：保留已填的条目，新句子追加空条目；附上程序的“需核对”提醒给审稿参考。"""
    facts = fact_index(facts_data)
    old = {e.get("key"): e for e in (load_yaml(d / "evidence.yml") or []) if isinstance(e, dict)}
    res = check_dir(d, facts_data, profile)
    risk = {(name, ln): [w for _, _, w in r["warnings"] if w.startswith("需核对")] for name, r in res.items() for ln, _, _ in r["warnings"]}
    out = []
    for name, ln, s, ids in cv_sentences(d, facts):
        k = sentence_key(s)
        e = old.get(k) or {"key": k, "verdict": "", "evidence": [], "note": ""}
        e.update({"file": name, "line": ln, "sentence": CITE.sub("", s).strip(), "cites": ids,
                  "risks": risk.get((name, ln), [])})
        out.append({k2: e[k2] for k2 in ("key", "file", "line", "sentence", "cites", "risks", "verdict", "evidence", "note")})
    return out


def evidence_errors(d: Path, facts_data: dict) -> list[tuple[str, int, str, str]]:
    """每句经历都要有审稿给出的 supported 结论，证据原文逐字出现在所引出处里，并包含句中的数字。"""
    facts = fact_index(facts_data)
    got = {e.get("key"): e for e in (load_yaml(d / "evidence.yml") or []) if isinstance(e, dict)}
    errs = []
    for name, ln, s, ids in cv_sentences(d, facts):
        e = got.get(sentence_key(s))
        if not e:
            errs.append((name, ln, s, "evidence.yml 里没有这句：先运行 evidence 并让审稿子代理填写"))
            continue
        if e.get("verdict") != "supported":
            errs.append((name, ln, s, f"审稿结论不是 supported（{e.get('verdict') or '未填'}）：{e.get('note', '')}"))
            continue
        quotes = [q for q in e.get("evidence") or [] if isinstance(q, str) and q.strip()]
        own = norm(" ".join(facts.get(i, "") for i in ids))
        if not quotes:
            errs.append((name, ln, s, "supported 但没有给出证据原文"))
        for q in quotes:
            if len(q) > 200:
                errs.append((name, ln, s, f"证据太长（{len(q)} 字）：只摘支持这句的那一小段，不要整条粘贴"))
            elif norm(q) not in own:
                errs.append((name, ln, s, f"证据不在所引出处 [cv:{','.join(ids)}] 里：“{q[:80]}”"))
        cv_text = " ".join(seg for seg, marks in segments(s)[0] if marks[0].startswith("[cv:"))
        missing = numbers_in(cv_text) - numbers_in(" ".join(quotes)) - ({str(len(ids))} if len(ids) >= 2 else set())
        if quotes and missing:
            errs.append((name, ln, s, f"句中的数字 {sorted(missing)} 没有出现在证据里"))
    return errs


def report_md(res: dict) -> str:
    n_err = sum(len(r["errors"]) for r in res.values())
    L = [f"# 事实校验：{'通过' if not n_err else f'{n_err} 处问题'}", "",
         "规则：经历句必须标 [cv:…] 出处；数字、专有名词、标题、网址必须出现在所引出处里。提醒只供参考。", ""]
    for name, r in res.items():
        L += [f"## {name}：{len(r['errors'])} 错误 · {len(r['warnings'])} 提醒", ""]
        for ln, s, e in r["errors"]:
            L.append(f"- ❌ 第 {ln} 行：{e}\n  > {s[:220]}")
        for ln, s, w in r["warnings"]:
            L.append(f"- ⚠️ 第 {ln} 行：{w}")
        L.append("")
    if not res:
        L.append("drafts/ 里没有文书。")
    return "\n".join(L)


def with_evidence(res: dict, d: Path, facts_data: dict) -> dict:
    for name, ln, s, why in evidence_errors(d, facts_data):
        res.setdefault(name, {"errors": [], "warnings": []})["errors"].append((ln, s, "证据核对：" + why))
    return res


def cmd_evidence(args) -> int:
    d = Path(args.dir)
    rows = evidence_template(d, load_yaml(find_facts(args.facts)) or {}, load_yaml(ROOT / "profile.yml"))
    (d / "evidence.yml").write_text("# 审稿子代理填写：verdict 写 supported / unsupported；evidence 逐字摘录 cv-facts 里支持这句的原文（每个数字都要在证据里）\n"
                                    + yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    todo = sum(1 for r in rows if r["verdict"] != "supported")
    print(f"→ {d / 'evidence.yml'}：{len(rows)} 句经历，{todo} 句待审稿填写证据")
    return 0


def cmd_check(args) -> int:
    d = Path(args.dir)
    facts_data = load_yaml(find_facts(args.facts)) or {}
    res = check_dir(d, facts_data, load_yaml(ROOT / "profile.yml"))
    if args.require_evidence:
        res = with_evidence(res, d, facts_data)
    (d / "check-report.md").write_text(report_md(res), encoding="utf-8")
    n_err = sum(len(r["errors"]) for r in res.values())
    for name, r in res.items():
        print(f"{name}: {len(r['errors'])} 错误 · {len(r['warnings'])} 提醒")
    print(f"→ {d / 'check-report.md'}" + ("" if not n_err else "（有错误：改稿后重跑，直到 0 错误）"))
    return 1 if n_err else 0


def strip_cites(text: str) -> str:
    text = re.sub(r"\s*" + CITE.pattern, "", text)
    return re.sub(r"[ \t]+([.,;:!?。，；：！？])", r"\1", text)


def cmd_clean(args) -> int:
    d = Path(args.dir)
    facts_data = load_yaml(find_facts(args.facts)) or {}
    res = with_evidence(check_dir(d, facts_data, load_yaml(ROOT / "profile.yml")), d, facts_data)  # 定稿必须过证据核对
    if any(r["errors"] for r in res.values()):  # 没有绕过选项：定稿草稿一定是校验和证据都通过的
        print("校验没通过，先改稿（见 check-report.md）")
        (d / "check-report.md").write_text(report_md(res), encoding="utf-8")
        return 1
    (d / "final").mkdir(exist_ok=True)
    for f in sorted((d / "drafts").glob("*.md")):
        (d / "final" / f.name).write_text(strip_cites(f.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"→ {d / 'final'}：去掉出处标记的定稿草稿。改好后放到 sent/ 同名文件，可用 edit-ratio 统计修改量。")
    return 0


def edit_ratio(a: str, b: str) -> float:
    wa, wb = re.findall(r"\w+|[^\w\s]", a), re.findall(r"\w+|[^\w\s]", b)
    return 1 - difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio() if wa or wb else 0.0


def cmd_edit_ratio(args) -> int:
    d = Path(args.dir)
    for f in sorted((d / "final").glob("*.md")):
        g = d / "sent" / f.name
        if g.exists():
            print(f"{f.name}: 修改 {edit_ratio(f.read_text(encoding='utf-8'), g.read_text(encoding='utf-8')):.0%}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("key", help="岗位 / 信源 id 或官网链接")
    p.add_argument("--text-file", help="岗位原文（网页打不开时手动复制）")
    p.add_argument("--out-root", default=str(APPS))
    p.add_argument("--no-fetch", action="store_true")
    p.set_defaults(fn=cmd_prepare)
    p = sub.add_parser("papers")
    p.add_argument("name")
    p.add_argument("--affil")
    p.add_argument("--n", type=int, default=8)
    p.set_defaults(fn=cmd_papers)
    for name, fn in [("check", cmd_check), ("evidence", cmd_evidence), ("clean", cmd_clean), ("edit-ratio", cmd_edit_ratio)]:
        p = sub.add_parser(name)
        p.add_argument("dir")
        p.add_argument("--facts")
        p.add_argument("--require-evidence", action="store_true", help="同时核对 evidence.yml（clean 总是核对）")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
