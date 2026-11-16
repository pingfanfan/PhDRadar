"""瑞士平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

Swiss Nanoscience Institute（SNI，巴塞尔大学）博士学院：每年一轮课题，官网 PhD program 页有一张课题表
  （Ref. Nr. / Project / Principal Investigator / Co-PI(s)），多数课题附 PDF 说明，统一经 biped.sni.unibas.ch 在线申请。
  robots.txt 只列站点地图、不设限制。FindAPhD 上转载的巴塞尔纳米课题就来自这张表；
  表里写了 “Please don't apply anymore” 或 “A candidate has been selected” 的课题不收（FindAPhD 上仍挂着）。
  页面没有统一截止日期：写的是 “Positions will be filled as suitable candidates are found”，按 rolling 收录；
  过了页面时间线里的 “Latest project start” 就视为本轮结束。资助金额页面未写，留空。
"""
from __future__ import annotations

import re

import collect_postings as cp
from collect_postings import Fetcher, page_text

SNI = "https://nanoscience.unibas.ch/en/forschung/phd-programm/"
SNI_ROW = re.compile(r"<tr>\s*<td>\s*(P\d{4})\s*</td>(.*?)</tr>", re.S)
SNI_ROLLING = re.compile(r"Positions will be filled as suitable candidates are found[^.]{0,80}\.?")
SNI_LATEST = re.compile(r"(\d{1,2})\s+([A-Z][a-z]+)\s+(\d{4})\s+Latest project start")
SNI_CLOSED = re.compile(r"don.t apply|candidate has been selected|position (?:has been )?filled", re.I)
MONTHS = {m: i for i, m in enumerate(("January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"), 1)}


def sni_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    raw = f.get(SNI).text
    return [(ref.lower(), f"{SNI}#{ref}") for ref, _ in SNI_ROW.findall(raw)]


def sni_detail(jid: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    text = page_text(raw)
    roll = SNI_ROLLING.search(text)
    if not roll or "Apply now" not in text:
        return None, "申请未开放"
    m = SNI_LATEST.search(text)
    if m and m.group(2) in MONTHS and f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}" < today:
        return None, "已截止"
    row = next((cells for ref, cells in SNI_ROW.findall(raw) if ref.lower() == jid), None)
    if row is None:
        return None, "课题表无此课题"
    cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
    if len(cells) < 3:
        return None, "课题信息不全"
    project = re.sub(r"\s+", " ", page_text(cells[0])).strip()
    if SNI_CLOSED.search(project):
        return None, "已停止招收"
    title = re.sub(r"\s*\(\s*pdf\s*\)\s*", " ", project).strip()
    if not title:
        return None, "课题信息不全"
    return {
        "id": f"sni:{jid}", "title": title[:200], "url": url,
        "org": "University of Basel – Swiss Nanoscience Institute", "country": "CH", "place": "Basel", "level": "phd",
        "deadline": "rolling", "quote": roll.group(0), "funding_for": "", "amount": "",
        "cn": cp.cn_of(text), "flags": cp.flags_of(text), "via": "SNI PhD School",
    }, "收录"


ADAPTERS = {"sni": (sni_urls, sni_detail)}
VIA_RANK = {"SNI PhD School": 3}
