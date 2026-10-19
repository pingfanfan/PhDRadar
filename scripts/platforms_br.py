"""巴西平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

FAPESP Oportunidades（圣保罗州研究基金会，fapesp.br/oportunidades/）：基金会官方的奖学金岗位公告板，一页列出全部在招公告；
  robots.txt 全部允许。只收博后（Post-Doctoral）、博士（Doctorate）与直博（Direct Doctorate）三类；
  截止日期取详情页英文栏 “Deadline for submissions: 2026-10-23”，资助额取 “Value: R$ 12.570,00”（FAPESP 月度奖学金）。
"""
from __future__ import annotations

import html as htmllib
import re

from collect_postings import Fetcher, cn_of, flags_of, page_text

FAPESP = "https://fapesp.br"
FAPESP_ITEM = re.compile(r'<li class="box_col aberta [^"]*tipo_(1|2|12)\b[^"]* en">\s*<a href="/oportunidades/(?:Control/\.\./)?([^"]+?/(\d+)/)"')


def fapesp_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    out: dict[str, str] = {}
    for _, path, jid in FAPESP_ITEM.findall(f.get(FAPESP + "/oportunidades/").text):
        out.setdefault(jid, f"{FAPESP}/oportunidades/{htmllib.unescape(path)}")
    return list(out.items())


def fapesp_field(raw: str, label: str) -> str:
    m = re.search(rf'<p class="linha(?: en)?(?: [a-z_]+)?">\s*<strong>{label}:\s*</strong>(.*?)</p>', raw, re.S)
    return re.sub(r"\s+", " ", page_text(m.group(1))).strip() if m else ""


def fapesp_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    t = re.search(r'<h3 class="detalhe en">(.*?)</h3>', raw, re.S)
    title = re.sub(r"\s+", " ", page_text(t.group(1))).strip() if t else ""
    if re.search(r"post-?doc", title, re.I):
        level = "postdoc"
    elif re.search(r"doctorate|doctoral|ph\.?d", title, re.I):
        level = "phd"
    else:
        return None, "非博士/博后岗位"
    raw_deadline = fapesp_field(raw, "Deadline for submissions")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_deadline):
        return None, "页面无截止日期"
    if raw_deadline < today:
        return None, "已截止"
    value = re.sub(r"\s*\(consulte.*$", "", fapesp_field(raw, "Value"))
    if not re.search(r"\d", value):
        return None, "未写资助或自费"
    text = page_text(raw)
    return {
        "id": f"fapesp:{jid}", "title": title[:200], "url": url, "org": fapesp_field(raw, "Unit/Instituition")[:120],
        "country": "BR", "place": fapesp_field(raw, "Locale")[:80], "level": level, "deadline": raw_deadline,
        "quote": f"Deadline for submissions: {raw_deadline}", "funding_for": "", "amount": value[:200],
        "cn": cn_of(text), "flags": flags_of(text), "via": "FAPESP Oportunidades",
    }, "收录"


ADAPTERS = {"fapesp": (fapesp_urls, fapesp_detail)}
VIA_RANK = {"FAPESP Oportunidades": 3}
