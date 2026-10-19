"""法国平台的岗位适配器，由 collect_postings.py 注册（ADAPTERS / VIA_RANK）。

CNRS emploi（emploi.cnrs.fr）：法国国家科研中心的官方招聘站。
  robots.txt 只禁止 /Administration/、/Candidat/、/Gestion/；岗位清单取自站点地图 /Sitemaps/OffresSiteMapProviderResult.ashx。
  只收两类：“CDD Doctorant”（三年博士合同）与 “Chercheur en contrat CDD”（要求博士学位的研究员短期合同，即博后）。
  截止日期取页面上的 “Date limite de candidature : lundi 9 novembre 2026 23:59”；薪资取 “Rémuneration” 一栏原文。
"""
from __future__ import annotations

import re

import collect_postings as cp
from collect_postings import Fetcher, page_text

CNRS_SITEMAP = "https://emploi.cnrs.fr/Sitemaps/OffresSiteMapProviderResult.ashx"
CNRS_LOC = re.compile(r"<loc>\s*(?:https://)?(emploi\.cnrs\.fr/Offres/(?:Doctorant|CDD)/([A-Z0-9]+-[A-Z0-9]+-\d+)/Default\.aspx)\s*</loc>")
FR_MONTHS = {m: i + 1 for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                                             "septembre", "octobre", "novembre", "décembre"])}
CNRS_DEADLINE = re.compile(r"Date limite de candidature\s*:\s*(?:[a-zé]+\s+)?(\d{1,2})(?:er)?\s+([a-zéû]+)\s+(\d{4})(?:\s+\d{1,2}:\d{2})?",
                           re.I)
# 法国公共机构岗位要求国籍、或涉及国防保密（ZRR）的会写明；ZRR 需要安全审查
CNRS_ZRR = re.compile(r"zone à régime restrictif|\bZRR\b", re.I)


def cnrs_urls(f: Fetcher, max_pages: int) -> list[tuple[str, str]]:
    return [(ref, "https://" + u) for u, ref in dict.fromkeys(CNRS_LOC.findall(f.get(CNRS_SITEMAP).text))]


def cnrs_field(text: str, name: str, nxt: str) -> str:
    m = re.search(rf"{name}\s+(.*?)\s+(?:{nxt})\b", text)
    return m.group(1).strip() if m else ""


def cnrs_detail(ref: str, url: str, raw: str, today: str) -> tuple[dict | None, str]:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"\s+", " ", page_text(h1.group(1)) if h1 else "")
    text = page_text(raw)
    kind = cnrs_field(text, "Type de Contrat", "Temps de Travail")
    if kind == "CDD Doctorant":
        level = "phd"
    elif kind == "Chercheur en contrat CDD":
        level = "postdoc"
    else:
        return None, "非博士/博后岗位"
    m = CNRS_DEADLINE.search(text)
    if not m or m.group(2).lower() not in FR_MONTHS:
        return None, "页面无截止日期"
    deadline = f"{m.group(3)}-{FR_MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    if deadline < today:
        return None, "已截止"
    pay = cnrs_field(text, "Rémuneration", "Postuler|Date limite")
    if not re.search(r"\d", pay):
        return None, "未写资助或自费"
    unit = cnrs_field(text, "L'unité", "Type de Contrat")
    place = re.sub(r"^\d{5}\s+", "", cnrs_field(text, "Lieu de Travail", "Durée du contrat|Date d'Embauche"))
    return {
        "id": f"cnrs:{ref}", "title": title[:200], "url": url, "org": ("CNRS – " + unit if unit else "CNRS")[:120],
        "country": "FR", "place": place.title()[:80], "level": level, "deadline": deadline, "quote": m.group(0),
        "funding_for": "", "amount": pay[:200], "cn": "check",
        "flags": ["security-screening"] if CNRS_ZRR.search(text) else cp.flags_of(text), "via": "CNRS Emploi",
    }, "收录"


ADAPTERS = {"cnrs": (cnrs_urls, cnrs_detail)}
VIA_RANK = {"CNRS Emploi": 3}
