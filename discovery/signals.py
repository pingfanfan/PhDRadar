"""识别网页/帖子中的“导师在招博士生/博士后”信号。

打分是启发式的：强信号（明确说在招 PhD）+3，弱信号（招生相关措辞）+1，
明确“不招”直接判 0。结果仅用于排序和人工复核，不代表岗位一定存在或带奖。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

STRONG = [
    r"\b(i\s+am|i'm|we\s+are|we're|my\s+(lab|group)\s+is|our\s+(lab|group|team)\s+is)\s+(actively\s+|currently\s+|now\s+)?"
    r"(looking\s+for|recruiting|seeking|hiring|accepting)\s+(\w+\s+){0,3}(ph\.?\s?d|doctoral|graduate)\s+(students?|candidates?|researchers?)",
    r"\b(ph\.?\s?d|doctoral)\s+(positions?|openings?|studentships?|vacanc(y|ies))\s+(are\s+|is\s+)?(now\s+)?(available|open)\b",
    r"\b(open|funded|available)\s+(ph\.?\s?d|doctoral)\s+(positions?|openings?|studentships?)\b",
    r"\bfully[\s-]+funded\s+(ph\.?\s?d|doctoral)\b",
    r"\b(recruiting|looking\s+for|seeking|hiring)\s+(\w+\s+){0,3}(ph\.?\s?d|doctoral)\s+students?\b",
    r"\b(ph\.?\s?d|doctoral)\s+students?\s+(wanted|needed)\b",
    r"招收.{0,10}(博士|PhD)", r"(全奖|全额奖学金).{0,10}(博士|PhD)", r"(博士|PhD).{0,6}(招生|名额)",
    # 博士后
    r"\b(i\s+am|i'm|we\s+are|we're|my\s+(lab|group)\s+is|our\s+(lab|group|team)\s+is)\s+(actively\s+|currently\s+|now\s+)?"
    r"(looking\s+for|recruiting|seeking|hiring)\s+(\w+\s+){0,3}(post[-\s]?docs?|postdoctoral\s+(researchers?|fellows?|scholars?))",
    r"\b(post[-\s]?doc(toral)?)\s+(positions?|openings?|fellowships?)\s+(are\s+|is\s+)?(now\s+)?(available|open)\b",
    r"\b(open|funded|available)\s+(post[-\s]?doc(toral)?)\s+(positions?|openings?)\b",
    r"招收.{0,10}博士后", r"博士后.{0,6}(招聘|招生|名额)",
]
WEAK = [
    r"\bprospective\s+(ph\.?\s?d\s+)?students?\b",
    r"\bjoin\s+(my|our|the)\s+(lab|group|team)\b",
    r"\b(openings|vacancies|open\s+positions)\b",
    r"\bapply\s+to\s+(work\s+with\s+me|my\s+group|our\s+lab)\b",
    r"\bfall\s+20(2[6-9]|3\d)\b", r"\b(spring|autumn)\s+20(2[6-9]|3\d)\b",
    r"\bfunded\b", r"\bstipend\b", r"\bscholarship\b",
]
NEGATIVE = [
    r"\b(not|no\s+longer)\s+(currently\s+)?(accepting|recruiting|taking|looking\s+for)\s+(any\s+)?(new\s+)?(ph\.?\s?d\s+)?students?\b",
    r"\bno\s+(open\s+)?(ph\.?\s?d\s+)?(positions?|openings?)\s+(are\s+)?(currently\s+)?available\b",
    r"\bnot\s+(be\s+)?(recruiting|accepting)\b",
    r"(暂不|不再)招收",
]
_STRONG = [re.compile(p, re.I) for p in STRONG]
_WEAK = [re.compile(p, re.I) for p in WEAK]
_NEG = [re.compile(p, re.I) for p in NEGATIVE]
_YEAR = re.compile(r"\b(?:fall|spring|autumn|winter|summer)?\s*(20(?:2[6-9]|3\d))\b", re.I)


@dataclass
class Signal:
    score: int = 0
    snippets: list[str] = field(default_factory=list)
    years: list[str] = field(default_factory=list)
    levels: list[str] = field(default_factory=list)  # 片段中提到的层级：phd / postdoc
    negative: bool = False

    @property
    def recruiting(self) -> bool:
        return self.score >= 3 and not self.negative


def _snippet(text: str, m: re.Match, width: int = 110) -> str:
    start, end = max(0, m.start() - width), min(len(text), m.end() + width)
    return re.sub(r"[\s\ufffd]+", " ", text[start:end]).strip()


def detect(text: str, max_snippets: int = 3) -> Signal:
    sig = Signal()
    if any(p.search(text) for p in _NEG):
        sig.negative = True
    for p in _STRONG:
        for m in p.finditer(text):
            sig.score += 3
            if len(sig.snippets) < max_snippets:
                sig.snippets.append(_snippet(text, m))
            break
    if sig.score:  # 弱信号只在已有强信号时加分，避免泛泛的“funded”误报
        sig.score += sum(1 for p in _WEAK if p.search(text))
    sig.years = sorted({y for y in _YEAR.findall(text)})
    joined = " ".join(sig.snippets)
    if re.search(r"ph\.?\s?d|doctoral|博士(?!后)", joined, re.I):
        sig.levels.append("phd")
    if re.search(r"post[-\s]?doc|postdoctoral|博士后", joined, re.I):
        sig.levels.append("postdoc")
    if sig.negative:
        sig.score = 0
    return sig


def page_text(html: str) -> str:
    """把 HTML 转为纯文本（去掉脚本、样式、导航）。"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        tag.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" ")).strip()
