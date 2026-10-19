#!/usr/bin/env python3
"""按申请者画像给“现在可申请”的机会排序：先硬性筛选（写明排除原因），再打分（每项给依据）。

    python scripts/rank.py                         # 读 profile.yml，写 rankings/<今天>.md 与 .json
    python scripts/rank.py --profile p.yml --top 30 --today 2026-10-19 --out rankings/

数据来自 assets/catalog.json（build_site.py 生成，与网站同一份）；规则在 scripts/rank_rules.py，
网站“为我推荐”用 assets/rank.js 按同一份规则在浏览器里排序（tests/test_rank.py 保证两边结果一致）。
画像结构见 docs/profile-schema.md。画像与排序结果只留在本地（已写进 .gitignore）。
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import rank_rules  # noqa: E402

CJK = re.compile(r"[㐀-鿿]")
MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
DISC_ZH = {"all": "不限学科", "cs": "计算机", "ai": "人工智能", "math": "数学", "physics": "物理", "chem": "化学与材料",
           "bio": "生物", "eco": "生态与进化", "neuro": "神经科学", "geo": "地球与环境", "engineering": "工程",
           "social": "社会科学", "humanities": "人文", "econ": "经济", "business": "商科", "med": "医学与健康"}
COVERAGE_ZH = {"full": "全奖（学费＋生活费）", "salary": "带薪岗位", "partial": "半奖 / 部分资助", "tuition": "仅免学费",
               "stipend": "仅生活费", "varies": "视项目而定", "none": "不提供资助", "unknown": "资助官网未写明", "": "资助官网未写明"}
ELIG_ZH = {"yes": "中国学生可申", "partial": "部分渠道可申", "check": "资格待核实（申请前请自己确认）", "": "资格待核实（申请前请自己确认）"}


# ---------- 词与文本 ----------

def _esc(s: str) -> str:
    return re.sub(r"([.*+?^${}()|\[\]\\\-])", r"\\\1", s)


def compile_term(t: str):
    """把词表里的一个词变成匹配函数需要的 (kind, pattern)。kind: sub 子串 / re 正则。"""
    if CJK.search(t):
        return ("sub", t)
    prefix = t.endswith("*")
    core = t.rstrip("*")
    cs = core.isupper() and len(core.replace(" ", "")) <= 4
    body = r"[\s\-]+".join(_esc(w) for w in core.split())
    pat = r"(?<![A-Za-z0-9])" + body + ("" if prefix else r"(?![A-Za-z0-9])")
    return ("re", re.compile(pat, 0 if cs else re.I))


def find(term, text: str) -> int:
    """返回命中位置，未命中 -1。"""
    kind, p = term
    if kind == "sub":
        return text.find(p)
    m = p.search(text)
    return m.start() if m else -1


def term_span(term, text: str):
    kind, p = term
    if kind == "sub":
        i = text.find(p)
        return (i, i + len(p)) if i >= 0 else None
    m = p.search(text)
    return (m.start(), m.end()) if m else None


def ymd(s) -> date | None:
    """'2026-10-19' / '2027-09' → date；其它返回 None。"""
    s = str(s or "")
    m = re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$", s)
    if not m:
        return None
    return date(int(m[1]), int(m[2]), int(m[3] or 1))


def parse_start(rq: str) -> date | None:
    """申请须知里结构化的“开始时间：01. Mar 2027”。“as soon as possible” 等返回 None。"""
    m = re.search(r"开始时间：(\d{1,2})\.? ([A-Za-z]{3})[a-z]* (\d{4})", rq or "")
    if not m or m[2].lower() not in MONTHS:
        return None
    return date(int(m[3]), MONTHS[m[2].lower()], int(m[1]))


def parse_number(s: str) -> float | None:
    s = s.replace(" ", "").replace(" ", "")
    if "," in s and "." in s:
        dec = "," if s.rfind(",") > s.rfind(".") else "."
        s = s.replace("." if dec == "," else ",", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", "") if re.search(r",\d{3}$", s) else s.replace(",", ".")
    elif "." in s and re.search(r"\.\d{3}$", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


CUR = {"€": "EUR", "eur": "EUR", "£": "GBP", "gbp": "GBP", "us$": "USD", "$": "USD", "usd": "USD", "chf": "CHF",
       "sek": "SEK", "nok": "NOK", "dkk": "DKK", "hk$": "HKD", "hkd": "HKD", "s$": "SGD", "sgd": "SGD", "a$": "AUD",
       "aud": "AUD", "c$": "CAD", "cad": "CAD", "nzd": "NZD", "jpy": "JPY", "¥": "JPY"}
AMOUNT = re.compile(r"(US\$|HK\$|S\$|A\$|C\$|€|£|\$|¥|EUR|GBP|USD|CHF|SEK|NOK|DKK|HKD|SGD|AUD|CAD|NZD|JPY)\s?(\d[\d.,  ]*\d|\d)"
                    r"|(\d[\d.,  ]*\d|\d)\s?(€|EUR|CHF|SEK|NOK|DKK|kr)", re.I)


def monthly_eur(s: str) -> float | None:
    """金额原文 → 约合欧元/月（取第一个数，范围取下限）；拿不准返回 None。"""
    m = AMOUNT.search(s or "")
    if not m:
        return None
    cur, num = (m[1], m[2]) if m[1] else (m[4], m[3])
    if not m[1]:  # “4000-4400 €/month”：范围取下限
        lo = re.search(r"(\d[\d.,]*)\s?[-–—]\s?$", s[:m.start()])
        if lo:
            num = lo[1]
    cur = cur.lower()
    if cur == "kr":
        cur = "sek"
    v = parse_number(num.strip())
    code = CUR.get(cur)
    if v is None or not code:
        return None
    tail = (s[m.end():m.end() + 30]).lower()
    if re.search(r"月|month", tail):
        per = 1
    elif re.search(r"年|annum|year|annual|p\.?a\b|pa\b", tail):
        per = 12
    else:
        per = 12 if v >= 10000 else 1
    eur = v * rank_rules.FX[code] / per
    return eur if 300 <= eur <= 20000 else None


# ---------- 画像 ----------

def prepare(profile: dict, rules: dict | None = None) -> dict:
    """把 profile.yml（或网站表单）整理成排序用的结构。"""
    R = rules or rank_rules.rules()
    groups = [{"d": g["d"], "m": bool(g.get("m")), "t": [t.lstrip("=") for t in g["t"]], "syn": [compile_term(t.lstrip("=")) for t in g["t"]],
               "all": [(compile_term(t), t.rstrip("*").lower()) for t in g["t"] + g["n"] if not t.startswith("=")]} for g in R["groups"]]
    stop = re.compile(R["stop"], re.I)
    research = profile.get("research") or {}
    seen, kws = set(), []
    for k in research.get("keywords") or []:
        k = str(k).strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            kws.append(k)
    disc = [d for d in research.get("disciplines") or [] if d]
    keywords = []
    for k in kws:
        spans = []
        for gi, g in enumerate(groups):
            for c in g["syn"]:
                sp = term_span(c, k)
                if sp:
                    spans.append((sp[0], sp[1], gi))
        # 只保留最长的命中：“神经网络”不应同时算作“神经”
        kept, cover = [], [False] * len(k)
        for a in spans:
            if any(b[2] != a[2] and b[0] <= a[0] and a[1] <= b[1] and (b[1] - b[0]) > (a[1] - a[0]) for b in spans):
                continue
            for i in range(a[0], a[1]):
                cover[i] = True
            if a[2] not in kept:
                kept.append(a[2])
        rest = stop.sub(" ", "".join(" " if cv else ch for ch, cv in zip(k, cover))).strip()
        own = not any(k.lower() == t.rstrip("*").lower() for gi in kept for t in groups[gi]["t"])
        for gi in kept:
            for d in groups[gi]["d"]:
                if d not in disc:
                    disc.append(d)
        if not kept:
            for d, w in R["disc_words"].items():
                if re.search(w, k, re.I) and d not in disc:
                    disc.append(d)
        keywords.append({"k": k, "lit": (compile_term(k), k.lower()) if own else None,
                         "concepts": [(f"g{gi}", groups[gi]["all"]) for gi in kept], "need_lit": bool(rest) or not kept,
                         "method": bool(kept) and all(groups[gi]["m"] for gi in kept)})
    edu = profile.get("education") or []
    target = profile.get("target") or {}
    start = ymd(target.get("start"))
    deg = 0
    for e in edu:
        lv = R["levels"].get(str(e.get("degree") or "").lower(), 0)
        end = ymd(e.get("end"))
        done = e.get("status", "completed") == "completed" or (start and end and end <= start)
        if done and lv > deg:
            deg = lv
    langs = profile.get("languages") or {}
    countries = profile.get("countries") or {}
    funding = profile.get("funding") or {}
    elig = profile.get("eligibility") or {}
    return {
        "keywords": keywords, "disc": disc, "deg": deg,
        "levels": target.get("levels") or ["phd"], "start": start,
        "ielts": langs.get("ielts"), "toefl": langs.get("toefl"),
        "german": R["cefr"].get(str(langs.get("german") or "").upper().replace("NATIVE", "native"), 0),
        "accept": countries.get("accept") or [], "prefer": countries.get("prefer") or [], "exclude": countries.get("exclude") or [],
        "min_cov": funding.get("min_coverage") or "any", "min_eur": funding.get("min_monthly_eur"),
        "prep": int(prep if (prep := (profile.get("deadline") or {}).get("min_prep_days")) is not None else 14),
        "cn": str(profile.get("nationality") or "CN").upper() == "CN", "cn_only": bool(elig.get("cn_only")),
        "sensitive": bool(profile.get("sensitive_field")), "R": R, "kwf": {},
        "restrict": re.compile(R["restrict"], re.I), "german_re": re.compile(R["german"]),
        "local_re": re.compile(R["local_lang"], re.I), "noise": re.compile(R["noise"], re.I),
        "noise_body": re.compile(R["noise_body"]), "focus": re.compile(R["focus"], re.I),
        "local_ok": any(str((o.get("lang") if isinstance(o, dict) else o) or "").strip().lower() in R["local_langs"]
                        for o in langs.get("other") or []),
    }


# ---------- 单条打分 ----------

def match_texts(x: dict, P: dict) -> tuple[str, str]:
    """用来匹配关键词的标题与简介：去掉资助方 / 机构名；标题写了“focus on”时只用它后面的方向（简介里多半是系名，不用）。"""
    mtitle = P["noise"].sub(" ", x.get("n") or "")
    mbody = P["noise_body"].sub(" ", P["noise"].sub(" ", x.get("in") or ""))
    fm = P["focus"].search(mtitle)
    if fm:
        mtitle, mbody = mtitle[fm.end():], ""
    return mtitle, mbody


def kw_hits_text(kw: dict, text: str) -> bool:
    return bool(text) and bool((kw["lit"] and find(kw["lit"][0], text) >= 0)
                               or any(find(t[0], text) >= 0 for _, concept in kw["concepts"] for t in concept))


def specificity(df: int, W: dict) -> float:
    """关键词越常见，每次命中的分越低（命中上百条的“癌症”不如命中十几条的“immunotherapy”有区分度）。"""
    a, b, lo, hi = W["spec"]
    f = a - b * math.log10(max(df, 1))
    return math.floor(min(hi, max(lo, f)) * 100 + 0.5) / 100


def mmdd(d: str) -> str:
    return f"{int(d[5:7])}/{int(d[8:10])}"


def assess(x: dict, P: dict, today: date) -> dict | None:
    """返回 {score, parts, hits, reasons, excluded}；不在“现在可申请”里的返回 None。"""
    R, W = P["R"], P["R"]["weights"]
    o = x.get("o")
    if not o:
        return None
    dl = o.get("dl") or x.get("dl") or ""
    dd = ymd(dl) if len(str(dl)) == 10 else None
    if dd and dd < today:
        return None
    n_days = (dd - today).days if dd else None
    title, body = x.get("n") or "", x.get("in") or ""  # 不用机构名：“National Institute of Education”不代表教育学
    mtitle, mbody = match_texts(x, P)
    rq = x.get("rq") or ""
    regions, levels, xd = x.get("r") or [], x.get("l") or ["phd"], x.get("d") or []
    c, e = x.get("c") or "", x.get("e") or ""
    out: list[str] = []

    # 硬性筛选
    if P["cn"] and e == "no":
        out.append("中国学生不可申请")
    if P["cn"] and P["cn_only"] and e not in ("yes", "partial"):
        out.append("资格待核实（你选了只看中国学生可申）")
    if P["restrict"].search(title + " " + rq):
        out.append("公告写明限本国 / 本土学生")
    if not any(lv in P["levels"] for lv in levels):
        out.append("层次不符（岗位是" + "、".join("博后" if lv == "postdoc" else "博士" for lv in levels) + "）")
    elif "phd" not in levels and P["deg"] < 3:
        out.append("博后岗位要求博士学位")
    m = re.search(r"学位要求：([^；]*)", rq)
    if m and "phd" in levels and P["deg"] < 2 and re.search(r"Master|Magister|Diplom", m[1]) and "Bachelor" not in m[1]:
        out.append("要求硕士学位")
    m = re.search(r"IELTS[^0-9；]{0,30}(\d(?:\.\d)?)", rq)
    if m and P["ielts"] is not None and float(P["ielts"]) < float(m[1]):
        out.append(f"雅思要求 {m[1]}（你 {P['ielts']}）")
    m = re.search(r"TOEFL[^0-9；]{0,30}(\d{2,3})", rq)
    if m and P["toefl"] is not None and P["ielts"] is None and float(P["toefl"]) < float(m[1]):
        out.append(f"托福要求 {m[1]}（你 {P['toefl']}）")
    if P["german_re"].search(title + " " + rq) and P["german"] < R["cefr"]["B2"]:
        out.append("要求德语")
    if P["local_re"].search(title) and not P["local_ok"]:
        out.append("公告用挪威语 / 瑞典语 / 丹麦语 / 荷兰语发布")
    if n_days is not None and n_days < P["prep"]:
        out.append(f"截止太近（还有 {n_days} 天，少于你设的准备期 {P['prep']} 天）")
    js = parse_start(rq)
    if js and P["start"] and js < P["start"] - timedelta(days=31):
        out.append(f"开始时间 {js.isoformat()[:7]} 早于你能入学的 {P['start'].isoformat()[:7]}")
    ok = R["coverage_ok"].get(P["min_cov"])
    if ok is not None and c not in ok:
        out.append("资助未写明全奖 / 带薪" if P["min_cov"] == "confirmed" else f"资助低于你的底线（{COVERAGE_ZH.get(c, c)}）")
    if P["min_eur"]:
        eur = monthly_eur(x.get("s") or "")
        if eur is not None and eur < float(P["min_eur"]):
            out.append(f"金额约 €{math.floor(eur + 0.5):,}/月，低于你的底线 €{P['min_eur']}")
    if any(r in P["exclude"] for r in regions):
        out.append("在你排除的国家")
    elif P["accept"] and regions and "GLOBAL" not in regions and not any(r in P["accept"] for r in regions) \
            and not ("EU" in regions and any(a in R["eu"] for a in P["accept"])):
        out.append("不在你可接受的国家")

    # 研究匹配
    hits, credited = [], set()
    strict = bool(xd) and "all" not in xd and any(d in P["disc"] for d in xd)  # 学科明确对得上
    near = P["disc"] + [s for d in P["disc"] for s in R["siblings"].get(d, [])]
    elsewhere = any(d != "all" and d not in near for d in xd)  # 岗位还属于你方向以外的学科
    clash = bool(P["disc"]) and bool(xd) and "all" not in xd and not strict  # 学科明确对不上
    for where, text, w in (("标题", mtitle, W["title"]), ("简介", mbody, W["body"])):
        if not text:
            continue
        for kw in P["keywords"]:
            if kw["k"] in [h[1] for h in hits]:
                continue
            # got：命中的记分标签（组号 + 实际命中的词），同一组或同一个词只记一次分
            got = ["k:" + kw["lit"][1], kw["lit"][1]] if kw["lit"] and find(kw["lit"][0], text) >= 0 else []
            full = bool(got)
            if not full:
                n = 0
                for tag, concept in kw["concepts"]:
                    t = next((t for t in concept if find(t[0], text) >= 0), None)
                    if t:
                        got += [tag, t[1]]
                        n += 1
                full = n > 0 and n == len(kw["concepts"]) and not kw["need_lit"]
            if not got or any(t in credited for t in got):
                continue
            # 学科对不上的命中多半是字面巧合（“immune memory”“memory device” 之于认知神经科学）；
            # 弱命中（只命中一部分、只在简介里、词表外的单个词）要求学科明确对得上
            weak = not full or where == "简介" or (not kw["concepts"] and " " not in kw["k"].strip() and not CJK.search(kw["k"]))
            if clash or (weak and P["disc"] and not strict and "all" not in xd):
                continue
            credited.update(got)
            applied = kw["method"] and elsewhere and P["disc"]
            note = ("" if full else "·部分") + ("·用于其他学科" if applied else "")
            hits.append((w * (1 if full else W["partial"]) * (W["applied"] if applied else 1) * P["kwf"].get(kw["k"], 1), kw["k"], where + note))
    hits.sort(key=lambda h: -h[0])
    kw_score = min(W["kw_cap"], sum(W["kw"][i] * h[0] for i, h in enumerate(hits[:3])))
    overlap = [d for d in xd if d != "all" and d in P["disc"]]
    d_score = W["disc"] * len(overlap) / len([d for d in xd if d != "all"]) if overlap else (W["all_disc"] if "all" in xd and hits else 0)
    research = kw_score + d_score

    # 其余各项
    funding = W["funding"].get(c, W["funding"][""])
    WD = W["deadline"]
    if dl == "rolling":
        dscore = WD["rolling"]
    elif o.get("st") == "upcoming":
        dscore = WD["upcoming"]
    elif n_days is None:
        dscore = WD["unknown"]
    else:
        dscore = WD["close"] if n_days < 21 else WD["best"] if n_days <= 75 else WD["far"] if n_days <= 150 else WD["very_far"]
    if P["prefer"]:
        region = W["region_prefer"] if any(r in P["prefer"] for r in regions) else W["region_other"]
    else:
        region = W["region_ok"]
    elig = W["elig"].get(e, W["elig"][""]) if P["cn"] else W["elig"][""]
    penalty = 0
    flags = []
    if "security-screening" in (x.get("fl") or []):
        penalty += W["screen_sensitive"] if P["sensitive"] else W["screen"]
        flags.append("⚠ 公告提到安全审查" + ("，你的方向较敏感" if P["sensitive"] else ""))
    if P["sensitive"] and "UK" in regions and any(d in R["atas_disc"] for d in P["disc"]) and any(d in R["atas_disc"] for d in xd):
        penalty += W["atas"]
        flags.append("⚠ 英国理工科敏感方向可能需要 ATAS 审查")
    total = research + funding + dscore + region + elig + penalty
    score = max(0, min(100, math.floor(total + 0.5)))

    # 三行理由
    names = [DISC_ZH.get(d, d) for d in overlap]
    if hits:
        r1 = "研究匹配：命中" + "、".join(f"「{h[1]}」（{h[2]}）" for h in hits) + (f"；学科：{'、'.join(names)}" if names else "")
    elif names:
        r1 = f"研究匹配：学科相同（{'、'.join(names)}），标题与简介没有直接出现你的关键词"
    else:
        r1 = "研究匹配：未命中你的关键词与学科"
    pay = COVERAGE_ZH.get(c, c)
    r2 = "资助与资格：" + " · ".join(filter(None, [pay, x.get("s") if x.get("s") and len(x["s"]) <= 60 else None,
                                                   ELIG_ZH.get(e, ELIG_ZH[""]) if P["cn"] else None]))
    if dl == "rolling":
        when = "滚动招生"
    elif o.get("st") == "upcoming":
        when = "即将开放" + (f"（{o['op']}）" if o.get("op") else "")
    elif dd:
        when = f"{mmdd(dl)} 截止（还有 {n_days} 天）"
    else:
        when = "截止日期官网未写明"
    where = "、".join(regions) or "地区未写明"
    if P["prefer"] and any(r in P["prefer"] for r in regions):
        where += "（你的偏好）"
    r3 = "时间与地区：" + " · ".join([when, where] + flags)
    return {"id": x["id"], "score": score,
            "parts": {"research": research, "funding": funding, "deadline": dscore, "region": region, "elig": elig, "penalty": penalty},
            "hits": [h[1] for h in hits], "reasons": [r1, r2, r3], "excluded": out, "relevant": bool(hits)}


def rank(rows: list[dict], profile: dict, today: date, rules: dict | None = None) -> dict:
    """返回 {ranked: 命中关键词的（按分数）, related: 只是学科相同的, excluded: 被硬性条件排除的, unrelated: 数量, considered: 数量}。"""
    P = prepare(profile, rules)
    # 先数每个关键词在现在可申请的机会里命中多少条，用来给常见词降权
    df = {kw["k"]: 0 for kw in P["keywords"]}
    for x in rows:
        o = x.get("o")
        dl = (o or {}).get("dl") or x.get("dl") or ""
        if not o or (len(str(dl)) == 10 and ymd(dl) < today):
            continue
        t, b = match_texts(x, P)
        for kw in P["keywords"]:
            if kw_hits_text(kw, t) or kw_hits_text(kw, b):
                df[kw["k"]] += 1
    P["kwf"] = {k: specificity(n, P["R"]["weights"]) for k, n in df.items()}
    ranked, related, excluded, unrelated, considered = [], [], [], 0, 0
    by_id = {x["id"]: x for x in rows}
    for x in rows:
        a = assess(x, P, today)
        if a is None:
            continue
        considered += 1
        if a["excluded"]:
            excluded.append(a)
        elif not a["relevant"]:
            if a["parts"]["research"] > 0:
                related.append(a)
            else:
                unrelated += 1
        else:
            ranked.append(a)

    def key(a):
        x = by_id[a["id"]]
        dl = (x.get("o") or {}).get("dl") or x.get("dl") or ""
        return (-a["score"], dl if len(dl) == 10 else "9999", a["id"])

    ranked.sort(key=key)
    related.sort(key=key)
    excluded.sort(key=lambda a: (-a["parts"]["research"], a["id"]))
    return {"ranked": ranked, "related": related, "excluded": excluded, "unrelated": unrelated, "considered": considered, "disc": P["disc"]}


# ---------- 输出 ----------

def render(res: dict, rows: list[dict], profile: dict, today: date, top: int = 30) -> str:
    by_id = {x["id"]: x for x in rows}
    P = prepare(profile)
    kws = "、".join(k["k"] for k in P["keywords"]) or "（未填）"
    lines = [f"# 为你排序的机会（{today.isoformat()}）", "",
             f"- 画像：关键词 {kws}；学科 {'、'.join(DISC_ZH.get(d, d) for d in P['disc']) or '未识别'}；"
             f"层次 {'、'.join('博后' if l == 'postdoc' else '博士' for l in P['levels'])}",
             f"- 现在可申请的机会 {res['considered']} 条：命中你的关键词 {len(res['ranked'])} 条，只是学科相同 {len(res['related'])} 条，"
             f"硬性条件排除 {len(res['excluded'])} 条，方向不相关 {res['unrelated']} 条。",
             "- 只推荐标题或简介命中你关键词的机会；分数 0–100：研究匹配 70（关键词 50 + 学科 20）、资助 10、截止 8、地区 7、资格 5，安全审查降分。资格写“待核实”的，投递前请自己读官网确认。",
             "- 排序只用标题、简介、学科与硬性条件；`/rank` 会再让 Claude 读前几条的原文做判断。信息以官网为准。", ""]
    for i, a in enumerate(res["ranked"][:top], 1):
        x = by_id[a["id"]]
        head = " — ".join(filter(None, [x["n"], x.get("org")]))
        lines += [f"### {i}. {head} · {a['score']} 分", ""] + [f"- {r}" for r in a["reasons"]] + [f"- 官网：<{x['u']}>", ""]
    if res["related"]:
        lines += ["## 学科相同、但没有命中你的关键词", "",
                  f"共 {len(res['related'])} 条，方向可能对口也可能不对口；关键词换个说法（加英文、同义词）可能会把真正对口的提上来。前 10 条：", ""]
        lines += [f"- {by_id[a['id']]['n']}（{'、'.join(by_id[a['id']].get('r', []))}） <{by_id[a['id']]['u']}>" for a in res["related"][:10]]
        lines.append("")
    if res["excluded"]:
        counts: dict[str, int] = {}
        for a in res["excluded"]:
            for r in a["excluded"]:
                k = re.sub(r"[（(].*$", "", r)
                counts[k] = counts.get(k, 0) + 1
        lines += ["## 被排除的机会", "", "按原因统计（一条可能有多个原因）：", ""]
        lines += [f"- {k}：{v} 条" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])]
        near = [a for a in res["excluded"] if a["parts"]["research"] >= 25][:15]
        if near:
            lines += ["", "方向对口但被排除的（看看条件能否补上）：", ""]
            lines += [f"- {by_id[a['id']]['n']}：{'；'.join(a['excluded'])} <{by_id[a['id']]['u']}>" for a in near]
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", default=str(ROOT / "profile.yml"))
    ap.add_argument("--catalog", default=str(ROOT / "assets" / "catalog.json"))
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--today", default=None)
    ap.add_argument("--out", default=str(ROOT / "rankings"))
    ap.add_argument("--stdout", action="store_true", help="只打印，不写文件")
    a = ap.parse_args()
    import yaml

    pf = Path(a.profile)
    if not pf.exists():
        print(f"找不到画像 {pf}。先运行 /setup，或复制 profile.example.yml 为 profile.yml 再修改。")
        return 2
    profile = yaml.safe_load(pf.read_text(encoding="utf-8")) or {}
    rows = json.loads(Path(a.catalog).read_text(encoding="utf-8"))
    today = date.fromisoformat(a.today) if a.today else datetime.now().date()
    res = rank(rows, profile, today)
    md = render(res, rows, profile, today, a.top)
    if a.stdout:
        print(md)
        return 0
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{today.isoformat()}.md").write_text(md, encoding="utf-8")
    by_id = {x["id"]: x for x in rows}
    top = [{**r, "item": by_id[r["id"]]} for r in res["ranked"][:max(a.top, 50)]]
    (out / f"{today.isoformat()}.json").write_text(json.dumps({"date": today.isoformat(), "top": top}, ensure_ascii=False, indent=1),
                                                   encoding="utf-8")
    print(f"推荐 {len(res['ranked'])} 条（学科相同 {len(res['related'])}，排除 {len(res['excluded'])}，不相关 {res['unrelated']}）→ {out / (today.isoformat() + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
