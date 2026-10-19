"""意大利平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

INFN（意大利国家核物理研究院）招聘站 jobs.dsi.infn.it：首页列出全部在招公告；无 robots.txt（404）。
  只收类型为 “Incarico Post-Doc” 或标题写明 post-doctoral 的公告（研究院的博后合同，薪资写在公告 PDF 里）；
  截止日期取详情页结构化字段 “Data scadenza 15-11-2026”。
"""
from __future__ import annotations

import re

from collect_postings import Fetcher, _any, _SCREENING, page_text

INFN = "https://jobs.dsi.infn.it/"
INFN_FIELDS = re.compile(r"Numero (\d+) Anno \d{4} Titolo (.+?) Numero posti (\d+) Tipo (.+?) Data bando [\d-]+ "
                         r"(Data scadenza (\d{2})-(\d{2})-(\d{4}))")


def infn_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    ids = dict.fromkeys(re.findall(r'href="dettagli_job\.php\?id=(\d+)"', f.get(INFN).text))
    return [(i, f"{INFN}dettagli_job.php?id={i}") for i in ids]


def infn_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    m = INFN_FIELDS.search(text)
    if not m:
        return None, "页面无截止日期"
    num, title, seats, kind = m.group(1), m.group(2).strip(), m.group(3), m.group(4).strip()
    if kind != "Incarico Post-Doc" and not re.search(r"post-?doc", title, re.I):
        return None, "非博士/博后岗位"
    deadline = f"{m.group(8)}-{m.group(7)}-{m.group(6)}"
    if deadline < today:
        return None, "已截止"
    return {
        "id": f"infn:{num}", "title": title[:200], "url": url, "org": "INFN – Istituto Nazionale di Fisica Nucleare",
        "country": "IT", "place": "", "level": "postdoc", "deadline": deadline, "quote": m.group(5),
        "funding_for": "", "amount": "", "cn": "check",
        "flags": ["security-screening"] if _any(_SCREENING, text) else [], "via": "INFN Jobs",
    }, "收录"


ADAPTERS = {"infn": (infn_urls, infn_detail)}
VIA_RANK = {"INFN Jobs": 3}
