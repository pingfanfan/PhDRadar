"""抓取器公共工具：统一的岗位结构、礼貌的 HTTP 客户端、资格/资助识别。"""
from __future__ import annotations

import re
import time
import urllib.robotparser
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from urllib.parse import urlparse

import requests

USER_AGENT = (
    "Mozilla/5.0 (compatible; PhDRadar/0.1; "
    "+https://github.com/pingfanfan/PhDRadar)"
)


@dataclass
class Job:
    """所有适配器的统一输出格式。"""

    source: str  # 对应 _data/sources.yml 中的 id
    id: str  # 全局唯一：<source>:<站内 id 或 URL>
    title: str
    url: str
    institution: str = ""
    country: str = ""
    city: str = ""
    posted: str | None = None  # YYYY-MM-DD
    deadline: str | None = None  # YYYY-MM-DD
    summary: str = ""
    eligibility: str = "unknown"  # international / restricted / unknown
    funding: str = "unknown"  # funded / self-funded / unknown
    flags: list[str] = field(default_factory=list)  # 如 security-screening
    level: str = "phd"  # phd / postdoc
    fetched_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class Disallowed(Exception):
    """robots.txt 不允许抓取。"""


class Fetcher:
    """带 robots.txt 检查、按站点限速和简单重试的 HTTP 客户端。"""

    def __init__(self, delay: float = 1.0, timeout: int = 30, respect_robots: bool = True):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        self.delay = delay
        self.timeout = timeout
        self.respect_robots = respect_robots
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self._last_hit: dict[str, float] = {}

    def allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        parts = urlparse(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                r = self.session.get(origin + "/robots.txt", timeout=self.timeout)
                if r.status_code >= 400:
                    rp = None  # 没有 robots.txt 视为允许
                else:
                    rp.parse(r.text.splitlines())
            except requests.RequestException:
                rp = None
            self._robots[origin] = rp
        rp = self._robots[origin]
        return rp is None or rp.can_fetch(USER_AGENT, url)

    def get(self, url: str, **kwargs) -> requests.Response:
        if not self.allowed(url):
            raise Disallowed(url)
        parts = urlparse(url)
        host = parts.netloc
        rp = self._robots.get(f"{parts.scheme}://{host}")
        crawl_delay = (rp.crawl_delay(USER_AGENT) if rp else None) or 0  # robots.txt 的 Crawl-delay 优先
        wait = max(self.delay, float(crawl_delay)) - (time.monotonic() - self._last_hit.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        for attempt in range(3):
            self._last_hit[host] = time.monotonic()
            try:
                r = self.session.get(url, **{"timeout": self.timeout, **kwargs})
            except requests.ConnectionError:  # 对方断开连接：稍等后重试
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))
                continue
            if r.status_code in (429, 502, 503, 504) and attempt < 2:
                retry_after = r.headers.get("Retry-After", "")
                time.sleep(min(int(retry_after), 60) if retry_after.isdigit() else 5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        return r  # pragma: no cover


# ───────────────────────── 文本识别 ─────────────────────────

_RESTRICTED = [
    r"\b(uk|home)[\s/-]*(fee[\s-]*(status|rate)?\s+)?(students?|applicants?|candidates?)\s+only\b",
    r"\bonly\s+(open|available|eligible)\s+(to|for)\s+(uk|home|eu|eea|u\.?s\.?|domestic|swiss|dutch|german)\b",
    r"\bopen\s+to\s+(uk|home|domestic)\s+(students?|applicants?)\s+only\b",
    r"\b(must|need to)\s+(be|have)\s+(a\s+)?(uk|u\.?s\.?|eu|australian|canadian)\s+(citizen|national|resident)",
    r"\b(u\.?s\.?|australian|canadian)\s+citizens?\s+(and|or)\s+permanent\s+residents?\s+only\b",
    r"\bdomestic\s+(students?|applicants?|candidates?)\s+only\b",
    r"\bnot\s+(open|available)\s+to\s+international\b",
    r"\bhome\s+fees?\s+only\b",
]
_INTERNATIONAL = [
    r"\bstudents\s+worldwide\b",
    r"\bopen\s+to\s+(all|international)\s+(students|applicants|candidates|nationalities)\b",
    r"\binternational\s+(students|applicants|candidates)\s+(are\s+)?(also\s+)?(eligible|welcome|encouraged)\b",
    r"\bregardless\s+of\s+(nationality|citizenship)\b",
    r"\b(all|any)\s+nationalit(y|ies)\b",
    r"\bno\s+nationality\s+restrictions?\b",
    r"\bincluding\s+international\s+(students|fees)\b",
    r"\binternational\s+fees?\s+(are\s+)?(covered|waived|included)\b",
]
_FUNDED = [
    r"\bfully[\s-]+funded\b", r"\bfunded\s+(phd|position|studentship|project)\b", r"\bstipend\b",
    r"\bsalary\b", r"\bstudentship\b", r"\bscholarship\b", r"\btuition\s+(fees?\s+)?waiver\b",
    r"\bemployment\s+contract\b", r"\bgross\s+(monthly|annual)\b", r"\b(tv-l|e\s?13)\b", r"\bstipendiat\b",
]
_SELF_FUNDED = [r"\bself[\s-]+funded\b", r"\bno\s+funding\b", r"\bunfunded\b", r"\bcompetition\s+funded\b"]
_SCREENING = [
    r"\batas\b", r"\bexport\s+control", r"\bsecurity\s+(screening|clearance|vetting)\b",
    r"\bknowledge\s+security\b", r"\bdual[\s-]use\b",
]


def _any(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, re.I) for p in patterns)


def classify(job: Job) -> Job:
    """根据标题和摘要推断国际生资格、资助情况和审查风险（启发式，需人工复核）。"""
    text = f"{job.title}\n{job.summary}"
    if _any(_RESTRICTED, text):
        job.eligibility = "restricted"
    elif _any(_INTERNATIONAL, text):
        job.eligibility = "international"
    if _any(_SELF_FUNDED, text):
        job.funding = "self-funded"
    elif _any(_FUNDED, text):
        job.funding = "funded"
    if _any(_SCREENING, text) and "security-screening" not in job.flags:
        job.flags.append("security-screening")
    return job


PHD_TITLE_RE = re.compile(
    r"\b(ph\.?\s?d|doctoral|doctorate|doktorand\w*|promovend\w*|stipendiat|"
    r"studentship|dphil|research\s+fellow\s+\(phd\)|thèse|these|dottorato)\b",
    re.I,
)


POSTDOC_TITLE_RE = re.compile(
    r"\b(post[-\s]?doc\w*|postdoctoral|postdoktor\w*|post-doctoral|research\s+associate|"
    r"(?<!ph\.d\.\s)(?<!phd\s)research\s+fellow(ship)?)\b",
    re.I,
)
NON_ACADEMIC_TITLE_RE = re.compile(
    r"\b(professor|lecturer|faculty|tenure|chair|head\s+of|director|engineer|technician|manager|officer|"
    r"coordinator|administrator|instructor|group\s+leader|senior\s+researcher|research\s+scientist)\b",
    re.I,
)
# 兼容旧代码：既非 PhD 也非博后的岗位，以及博后岗位
NON_PHD_TITLE_RE = re.compile(NON_ACADEMIC_TITLE_RE.pattern + "|" + POSTDOC_TITLE_RE.pattern, re.I)
PHD_SUMMARY_RE = re.compile(
    r"\b(ph\.?\s?d\.?\s+(position|student|candidate|studentship|project|fellowship)s?|"
    r"doctoral\s+(student|candidate|researcher|position|network)s?|studentships?|fully[\s-]funded\s+ph\.?d)\b",
    re.I,
)
POSTDOC_SUMMARY_RE = re.compile(
    r"\b(post[-\s]?doc(toral)?\s+(position|fellow|fellowship|researcher|scholar|opening)s?|postdocs?\s+wanted)\b",
    re.I,
)


def looks_like_phd(text: str) -> bool:
    return bool(PHD_TITLE_RE.search(text))


def posting_level(title: str, summary: str = "") -> str | None:
    """判断岗位层级：'phd'、'postdoc'，或 None（教职、行政、工程师等不收录）。

    注意：教职广告常写 “PhD required”，所以摘要里只出现 “PhD” 不算博士岗。
    """
    t = title or ""
    if re.search(r"\bph\.?\s?d\s+research\s+fellow|\bstipendiat\b", t, re.I):  # 挪威 “PhD Research Fellow” 是博士岗
        return "phd"
    if POSTDOC_TITLE_RE.search(t):
        return "postdoc"
    if PHD_TITLE_RE.search(t):
        return "phd"
    if NON_ACADEMIC_TITLE_RE.search(t):
        return None
    if POSTDOC_SUMMARY_RE.search(summary or ""):
        return "postdoc"
    if PHD_SUMMARY_RE.search(summary or ""):
        return "phd"
    return None


def is_phd_posting(title: str, summary: str = "") -> bool:
    return posting_level(title, summary) == "phd"


def matches_keywords(job: Job, keywords: list[str]) -> bool:
    if not keywords:
        return True
    text = f"{job.title} {job.summary} {job.institution}".lower()
    return any(k.lower() in text for k in keywords)


# ───────────────────────── 日期 ─────────────────────────

_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def parse_date(text: str | None) -> str | None:
    """尽量把常见日期格式转成 YYYY-MM-DD，失败返回 None。"""
    if not text:
        return None
    text = text.strip()
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        y, mo, d = map(int, m.groups())
        return _safe(y, mo, d)
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
    if m:
        d, mo, y = map(int, m.groups())
        return _safe(y, mo, d)
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\.?,?\s+(\d{4})", text)
    if m and m.group(2)[:3].lower() in _MONTHS:
        return _safe(int(m.group(3)), _MONTHS[m.group(2)[:3].lower()], int(m.group(1)))
    m = re.search(r"([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", text)
    if m and m.group(1)[:3].lower() in _MONTHS:
        return _safe(int(m.group(3)), _MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
    try:  # RFC 2822（RSS pubDate）
        from email.utils import parsedate_to_datetime

        return parsedate_to_datetime(text).date().isoformat()
    except (TypeError, ValueError, IndexError):
        return None


def _safe(y: int, mo: int, d: int) -> str | None:
    try:
        return date(y, mo, d).isoformat()
    except ValueError:
        return None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_text(text: str | None, limit: int = 600) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]
