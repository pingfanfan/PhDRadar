"""/rank 排序的离线测试：构造画像 + 构造岗位，验证硬性筛选、打分顺序，以及 Python（rank.py）与浏览器（assets/rank.js）结果一致。"""
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import rank  # noqa: E402
from rank_rules import rules  # noqa: E402

TODAY = date(2026, 10, 19)


def job(id, n, dl="2026-11-28", **kw):
    """构造一条 catalog.json 里的“现在可申请”岗位。"""
    x = {"id": id, "n": n, "u": f"https://example.org/{id}", "r": ["UK"], "l": ["phd"], "c": "full", "e": "yes",
         "d": [], "v": True, "o": {"st": "open", "dl": dl}}
    x.update(kw)
    return x


PROFILE = {
    "nationality": "CN",
    "education": [{"degree": "bachelor", "status": "completed"}, {"degree": "master", "status": "ongoing", "end": "2027-06"}],
    "research": {"keywords": ["机器学习", "医学影像", "MRI"]},
    "target": {"levels": ["phd"], "start": "2027-09"},
    "languages": {"ielts": 6.5},
    "countries": {"accept": ["UK", "NL"], "prefer": ["NL"]},
    "funding": {"min_coverage": "full", "min_monthly_eur": 1800},
    "deadline": {"min_prep_days": 14},
}

ROWS = [
    job("ml-uk", "Machine Learning for Medical Imaging", d=["ai", "med"]),
    job("ml-nl", "Machine learning for MRI reconstruction", r=["NL"], d=["ai", "med"]),
    job("ml-soon", "Machine learning PhD", dl="2026-10-25", d=["ai"]),
    job("pd", "Postdoc in machine learning", l=["postdoc"], c="salary", d=["ai"]),
    job("no-cn", "Machine learning studentship", e="no", d=["ai"]),
    job("home-only", "Machine learning studentship", rq="资助对象（公告原文）：Funded PhD Project (UK Students Only)", d=["ai"]),
    job("ielts", "Machine learning in health", rq="IELTS overall 7.5 required", d=["ai"]),
    job("german", "Doktorand/in (m/w/d) Maschinelles Lernen", r=["DE"], d=["ai"]),
    job("france", "Machine learning PhD in Paris", r=["FR"], d=["ai"]),
    job("eu-wide", "Machine learning doctoral network", r=["EU"], d=["ai"]),
    job("history", "Medieval history of trade", d=["humanities"]),
    job("partial", "Machine learning partial scholarship", c="partial", d=["ai"]),
    job("master", "Machine learning for imaging", r=["NL"], rq="学位要求：Master；工作语言：English", d=["ai"]),
    job("start-early", "Machine learning for imaging", r=["NL"], rq="开始时间：01. Jan 2027", d=["ai"]),
    job("poor", "Machine learning with small stipend", s="€1,200/月", d=["ai"]),
    job("expired", "Machine learning PhD", dl="2026-10-01", d=["ai"]),
    {"id": "no-open", "n": "Machine learning programme", "u": "https://example.org/x", "l": ["phd"], "e": "yes", "v": True},
]


def by_id(res):
    return {a["id"]: a for a in res["ranked"] + res["excluded"]}


def test_hard_filters_with_reasons():
    res = rank.rank(ROWS, PROFILE, TODAY)
    ex = {a["id"]: " ".join(a["excluded"]) for a in res["excluded"]}
    assert "截止太近" in ex["ml-soon"]
    assert "层次不符" in ex["pd"]
    assert "不可申请" in ex["no-cn"]
    assert "限本国" in ex["home-only"]
    assert "雅思要求 7.5" in ex["ielts"]
    assert "要求德语" in ex["german"]
    assert "不在你可接受的国家" in ex["france"] and "不在你可接受的国家" in ex["german"]
    assert "资助低于你的底线" in ex["partial"]
    assert "要求硕士学位" not in ex.get("master", "")  # 入学前会拿到硕士
    assert "开始时间 2027-01" in ex["start-early"]
    assert "低于你的底线 €1800" in ex["poor"]
    ranked = [a["id"] for a in res["ranked"]]
    assert "eu-wide" in ranked and "master" in ranked  # EU 范围的项目对接受荷兰的人开放
    assert "history" not in ranked and "history" not in ex and res["unrelated"] == 1
    assert "expired" not in by_id(res) and "no-open" not in by_id(res)
    assert res["considered"] == len(ROWS) - 2


def test_bachelor_only_excluded_from_master_required():
    p = {**PROFILE, "education": [{"degree": "bachelor", "status": "completed"}]}
    ex = {a["id"]: a["excluded"] for a in rank.rank(ROWS, p, TODAY)["excluded"]}
    assert "要求硕士学位" in ex["master"]
    p = {**PROFILE, "target": {"levels": ["postdoc"]}, "education": [{"degree": "master"}]}
    ex = {a["id"]: a["excluded"] for a in rank.rank(ROWS, p, TODAY)["excluded"]}
    assert "博后岗位要求博士学位" in ex["pd"]


def test_ranking_order_and_reasons():
    res = rank.rank(ROWS, PROFILE, TODAY)
    ranked = [a["id"] for a in res["ranked"]]
    # 标题同时命中两个方向且在偏好国家的排第一；只命中一个方向的在后
    assert ranked[0] == "ml-nl"
    assert ranked.index("ml-uk") < ranked.index("eu-wide")
    top = res["ranked"][0]
    assert len(top["reasons"]) == 3
    assert "「机器学习」（标题）" in top["reasons"][0] and "「医学影像」（标题）" in top["reasons"][0]
    assert "（你的偏好）" in top["reasons"][2]
    assert "中国学生可申" in top["reasons"][1]


def test_synonyms_counted_once():
    # “医学影像”和“MRI”属于同一组同义词，同一个标题只加一次分
    one = rank.rank([job("a", "MRI of the brain", d=["med"])], {"research": {"keywords": ["医学影像"]}}, TODAY)
    two = rank.rank([job("a", "MRI of the brain", d=["med"])], {"research": {"keywords": ["医学影像", "MRI"]}}, TODAY)
    assert one["ranked"][0]["score"] == two["ranked"][0]["score"]


def test_longest_match_wins():
    # “神经网络”不能被当成“神经（科学）”，否则神经科学岗位会被误推给做深度学习的人
    res = rank.rank([job("neuro", "Cellular neuroscience of memory", d=["neuro"])],
                    {"research": {"keywords": ["神经网络"]}}, TODAY)
    assert res["ranked"] == [] and res["unrelated"] == 1


def test_security_screening_penalty():
    rows = [job("a", "Quantum materials PhD", d=["physics"]),
            job("b", "Quantum materials PhD", d=["physics"], fl=["security-screening"])]
    res = rank.rank(rows, {"research": {"keywords": ["quantum"]}, "sensitive_field": True}, TODAY)
    s = {a["id"]: a for a in res["ranked"]}
    assert s["a"]["score"] > s["b"]["score"]
    assert "安全审查" in s["b"]["reasons"][2]
    assert "ATAS" in s["a"]["reasons"][2]


def test_cn_only_and_non_cn_nationality():
    rows = [job("chk", "Machine learning PhD", e="check", d=["ai"]), job("no", "Machine learning PhD", e="no", d=["ai"])]
    p = {"research": {"keywords": ["machine learning"]}, "eligibility": {"cn_only": True}}
    assert [a["id"] for a in rank.rank(rows, p, TODAY)["ranked"]] == []
    p = {"research": {"keywords": ["machine learning"]}, "nationality": "DE"}
    assert sorted(a["id"] for a in rank.rank(rows, p, TODAY)["ranked"]) == ["chk", "no"]


@pytest.mark.parametrize("text,eur", [
    ("€2,100/月（税后）", 2100), ("£20,780/年", 20780 * 1.17 / 12), ("The basic salary of EUR 3.776,10 (on a full-time basis)", 3776.1),
    ("4000-4400 €/month", 4000), ("$50,000 or more", 50000 * 0.92 / 12), ("Competitive", None), ("SEK 34 000 per month", 34000 * 0.087),
])
def test_monthly_eur(text, eur):
    got = rank.monthly_eur(text)
    assert (got is None) if eur is None else abs(got - eur) < 1


def test_rules_json_in_sync():
    built = ROOT / "assets" / "rank-rules.json"
    from build_site import DISC_WORDS
    assert json.loads(built.read_text(encoding="utf-8")) == json.loads(json.dumps(rules(DISC_WORDS))), \
        "assets/rank-rules.json 过期：运行 python scripts/build_site.py"


def run_js(rows, profiles, today):
    script = """
const r = require(process.argv[1]); const fs = require('fs');
const inp = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = inp.profiles.map(p => { const res = r.rank(inp.rows, p, inp.rules, inp.today);
  return {ranked: res.ranked.map(a => [a.id, a.score, a.reasons]), excluded: res.excluded.map(a => [a.id, a.excluded]),
          unrelated: res.unrelated, considered: res.considered, disc: res.disc}; });
process.stdout.write(JSON.stringify(out));
"""
    inp = json.dumps({"rows": rows, "profiles": profiles, "rules": rules(), "today": today.isoformat()}, ensure_ascii=False)
    p = subprocess.run(["node", "-e", script, str(ROOT / "assets" / "rank.js")], input=inp, capture_output=True, text=True, check=True)
    return json.loads(p.stdout)


def run_py(rows, profiles, today):
    out = []
    for p in profiles:
        res = rank.rank(rows, p, today)
        out.append({"ranked": [[a["id"], a["score"], a["reasons"]] for a in res["ranked"]],
                    "excluded": [[a["id"], a["excluded"]] for a in res["excluded"]],
                    "unrelated": res["unrelated"], "considered": res["considered"], "disc": res["disc"]})
    return out


PROFILES = [
    PROFILE,
    {**PROFILE, "education": [{"degree": "bachelor"}], "languages": {"toefl": 95}, "sensitive_field": True},
    {"research": {"keywords": ["神经网络", "quantum", "生态"]}, "countries": {"exclude": ["UK"]}, "eligibility": {"cn_only": True}},
    {"research": {"keywords": ["climate", "海洋"]}, "target": {"levels": ["phd", "postdoc"]}, "education": [{"degree": "phd"}],
     "languages": {"german": "C1"}, "funding": {"min_coverage": "confirmed"}, "deadline": {"min_prep_days": 0}},
]


@pytest.mark.skipif(not shutil.which("node"), reason="需要 node")
def test_js_matches_python_on_fixtures():
    assert run_js(ROWS, PROFILES, TODAY) == run_py(ROWS, PROFILES, TODAY)


@pytest.mark.skipif(not shutil.which("node"), reason="需要 node")
def test_js_matches_python_on_catalog():
    path = ROOT / "assets" / "catalog.json"
    if not path.exists():
        pytest.skip("没有 catalog.json")
    rows = json.loads(path.read_text(encoding="utf-8"))
    rows = [x for x in rows if x.get("o")][:1500]
    assert run_js(rows, PROFILES, TODAY) == run_py(rows, PROFILES, TODAY)
