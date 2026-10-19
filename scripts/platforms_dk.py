"""丹麦平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

Aarhus University（international.au.dk）：全校空缺列表页把全部岗位以内嵌 JSON（Emply 数据）给出，一次请求即可；
  岗位页写有 “Apply Deadline: Tuesday 10 Nov 2026 at 23:59 CET”，截止日期只从这句原文取。无 robots.txt（404）。
  丹麦博士是带薪雇员，工资按国家学术人员集体协议发放；博后页面写有年薪区间。
"""
from __future__ import annotations

import json
import re

from collect_postings import MONTH3, Fetcher, _any, _FUNDED, _RESTRICTED, _SCREENING, _SELF_FUNDED, level_of, page_text, \
    parse_day

AU = "https://international.au.dk"
AU_LIST = AU + "/about/profile/vacant-positions/"
AU_DEADLINE = re.compile(r"Apply\s+Deadline:\s*(?:[A-Za-z]+day\s+)?(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})(?:\s+at\s+\d{1,2}:\d{2}\s*[A-Z]{3,4})?")


def au_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    m = re.search(r"vacancies\s*=\s*(\[.*?\]);\s*\n", f.get(AU_LIST).text, re.S)
    rows = json.loads(m.group(1)) if m else []
    return [(str(v["id"]), AU + v["link"]) for v in rows if v.get("link") and level_of(v.get("title") or "")]


def au_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"\s+", " ", page_text(h1.group(1)) if h1 else "")
    level = level_of(title)
    if not level:
        return None, "非博士/博后岗位"
    text = page_text(raw)
    m = AU_DEADLINE.search(text)
    if not m or m.group(2).lower() not in MONTH3:
        return None, "页面无截止日期"
    deadline = parse_day(f"{m.group(1)} {MONTH3[m.group(2).lower()]} {m.group(3)}")
    if not deadline or deadline < today:
        return None, "已截止"
    body = text[:m.start()]
    if _any(_SELF_FUNDED, body) or not (_any(_FUNDED, body) or re.search(r"collective agreement", body, re.I)):
        return None, "未写资助或自费"
    sal = re.search(r"(?:yearly|monthly|annual) base salary[^.]{0,160}?DKK\s?[\d.,]+(?:\s+and\s+DKK\s?[\d.,]+)?", body, re.I)
    return {
        "id": f"aarhus:{jid}", "title": title[:200], "url": url, "org": "Aarhus University", "country": "DK", "place": "",
        "level": level, "deadline": deadline, "quote": m.group(0), "funding_for": "", "amount": (sal.group(0) if sal else "")[:200],
        "cn": "no" if _any(_RESTRICTED, body) else "check",
        "flags": ["security-screening"] if _any(_SCREENING, body) else [], "via": "Aarhus University",
    }, "收录"


ADAPTERS = {"aarhus": (au_urls, au_detail)}
VIA_RANK = {"Aarhus University": 3}
