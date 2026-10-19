"""/apply 的离线测试：申请清单摘句、事实校验（编造的经历一条都不能通过）、去标记。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import apply_check as ac  # noqa: E402

FIX = ROOT / "tests" / "fixtures" / "apply"
LIN = yaml.safe_load((FIX / "lin-xiaozhou.yml").read_text(encoding="utf-8"))

POSTING = """PhD Studentship: Monte Carlo Methods for Constrained and Aggregated Data
Funding for:
UK Students, EU Students, International Students
Closes:
10th January 2027
Optimal scaling theory, such as the well-known 0.234 acceptance rule, tells practitioners how to tune MCMC algorithms in high dimensions.
The project will derive optimal tuning rules for samplers such as random-walk Metropolis and MALA on constrained domains, starting with the probability simplex.
Applicants should hold a first-class or upper second-class degree in mathematics or statistics.
Please email Dr Hu (
s.hu@example.ac.uk
) with a CV, your transcripts and a short statement (no more than one page) saying which strand interests you.
Two references are required. Applications must be submitted by 23:59 GMT on 10 January 2027.
Formal applications should be made through the University online application system.
The intended start date is September 2027.
Jobs by Email
"""
LAB = {"supervisor": {"name": "Dr Shan Hu", "homepage": "https://www.example.ac.uk/staff/hu"},
       "papers": [{"id": "p1", "title": "Exact fusion of posterior inferences under aggregate constraints", "year": 2025,
                   "venue": "Journal of Computational and Graphical Statistics", "url": "https://doi.org/10.0000/example"}]}
OPP = {"id": "test:1", "title": "PhD Studentship: Monte Carlo Methods for Constrained and Aggregated Data",
       "org": "University of Birmingham", "url": "https://www.example.ac.uk/job/1"}

GOOD = """Subject: Prospective PhD applicant – Monte Carlo Methods for Constrained and Aggregated Data

Dear Dr Hu,

My name is Lin Xiaozhou, and I am writing about the PhD Studentship: Monte Carlo Methods for Constrained and Aggregated Data at the University of Birmingham.

Your plan to derive optimal tuning rules for MALA on the probability simplex [post] is close to my MSc thesis on adaptive tuning of Metropolis-adjusted Langevin algorithms on the probability simplex [cv:edu1].
I also read your paper "Exact fusion of posterior inferences under aggregate constraints" [lab:p1].
As a research assistant, I implemented a data-augmentation Gibbs sampler in R and C++ for regional disease counts with exact row and column totals [cv:proj1].
On synthetic tables it reduced the effective-sample-size cost per second by about 40% compared with the baseline sampler [cv:proj1].
A paper from my thesis is under review at Statistics and Computing [cv:pub1].
I completed my MSc at Northbridge University with a GPA of 3.82/4.0, ranking 3/62 [cv:edu1].
Two of my projects used sequential and Gibbs sampling [cv:proj1,proj2].
我在 Northbridge University 完成了统计学硕士学习 [cv:edu1]。

Would you be open to a short call about whether my background fits the project?

Best regards,
Lin Xiaozhou
lin.xz@example.com
"""

# 每一句都是编造或与出处不符的经历：必须被程序拦下
FABRICATED = [
    "I completed my MSc at Northbridge University with a GPA of 3.92/4.0 [cv:edu1].",            # 改了数字
    "I ranked 1/62 in my cohort [cv:edu1].",                                                       # 改了排名
    "I received the Outstanding Graduate Award of Northbridge University [cv:award1].",           # 编造奖项
    "I was a visiting student at Imperial College London [cv:edu1].",                             # 编造机构
    "I interned at DeepMind on probabilistic programming [cv:proj1].",                            # 编造公司
    'My paper "Fast MCMC on the simplex" was accepted [cv:pub1].',                                # 编造论文题目
    "My paper was published in the Annals of Statistics [cv:pub1].",                              # 编造期刊
    "I published three first-author papers [cv:pub1].",                                           # 编造数量
    "I implemented a Gibbs sampler that was 10 times faster than the baseline.",                  # 经历句无出处 + 数字
    "I developed a new variational inference library.",                                           # 经历句无出处
    "I led a team of 5 students in the traffic project [cv:proj2].",                              # 改了人数
    "My IELTS score is 8.0 [cv:ielts].",                                                          # 改了成绩
    "I hold a PhD scholarship from the China Scholarship Council [cv:award1].",                   # 编造资助
    "My code is available at https://github.com/linxz/simplex-mala [cv:proj1].",                  # 编造网址
    "I worked on this during my MSc [cv:edu9].",                                                  # 出处 id 不存在
    "I also read your 2023 paper on exact fusion [lab:p1].",                                      # 导师论文年份不符
    "I applied the 0.5 acceptance rule in my thesis [cv:edu1].",                                  # 数字不在出处
    "我曾获得国家奖学金和优秀毕业生奖 [cv:award1]。",                                                # 中文：编造“优秀毕业生奖”
    "我在南湖大学做过两年研究助理 [cv:proj1]。",                                                     # 中文：编造机构与年限
    "我发表了两篇论文。",                                                                           # 中文：经历句无出处
    "I studied at Northbridge University from 2022 [cv:edu1].",                                   # 改了年份
    "TODO: add one sentence about my teaching experience.",                                       # 占位符
    "My paper on tuning MALA on the simplex has been accepted [cv:pub1].",                       # 在审写成已接收
    "I am the first author of a paper on tuning MALA [cv:pub1].",                                # 出处没写一作
    "I led the small-area disease mapping project [cv:proj1].",                                  # 研究助理写成主导
    "I independently implemented a data-augmentation Gibbs sampler [cv:proj1].",                 # 夸大为独立完成
    "My work on traffic estimation received a best paper award [cv:proj2].",                     # 编造最佳论文
]


def make_dir(tmp_path: Path, draft: str) -> Path:
    d = tmp_path / "app"
    (d / "drafts").mkdir(parents=True)
    (d / "posting.txt").write_text(POSTING, encoding="utf-8")
    (d / "posting.yml").write_text(yaml.safe_dump(OPP, allow_unicode=True), encoding="utf-8")
    (d / "lab.yml").write_text(yaml.safe_dump(LAB, allow_unicode=True), encoding="utf-8")
    (d / "drafts" / "email.md").write_text(draft, encoding="utf-8")
    return d


def errors(res: dict) -> list:
    return [e for r in res.values() for e in r["errors"]]


def test_good_draft_passes(tmp_path):
    res = ac.check_dir(make_dir(tmp_path, GOOD), LIN)
    assert errors(res) == []


@pytest.mark.parametrize("sentence", FABRICATED)
def test_fabricated_claim_is_caught(tmp_path, sentence):
    res = ac.check_dir(make_dir(tmp_path, GOOD + "\n" + sentence + "\n"), LIN)
    assert errors(res), f"编造的句子通过了校验：{sentence}"


def test_hype_is_warning_not_error(tmp_path):
    res = ac.check_dir(make_dir(tmp_path, GOOD + "\nI am passionate about this cutting-edge project.\n"), LIN)
    assert not errors(res)
    assert any("空话" in w for r in res.values() for _, _, w in r["warnings"])


def test_fact_index_ids_and_sections():
    idx = ac.fact_index(LIN)
    assert {"edu1", "edu2", "pub1", "proj1", "proj2", "award1", "ielts", "skills"} <= set(idx)
    assert "3.82/4.0" in idx["edu1"]
    assert "name" not in idx  # 身份信息不当出处，但在 identity_text 里
    assert "Lin Xiaozhou" in ac.identity_text(LIN)


def test_checklist_quotes_original(tmp_path):
    cl = ac.extract_checklist(POSTING)
    assert "简历 CV" in cl["materials"] and "成绩单与学位证明" in cl["materials"] and "求职信 / 动机信" in cl["materials"]  # short statement saying …
    assert cl["references"] == ["2"]
    assert any("no more than one page" in s for s in cl["format"])
    assert any("23:59 GMT" in s for s in cl["deadline_time"])
    assert any("s.hu@example.ac.uk" in s for s in cl["how"])  # 断行的邮箱并回原句
    assert any("September 2027" in s for s in cl["start"])
    assert any("upper second-class" in s for s in cl["requirements"])
    assert any("International Students" in s for s in cl["funding"])
    assert not any("Jobs by Email" in s for v in cl.values() if isinstance(v, list) for s in v)
    md = ac.checklist_md(OPP, cl, None, True)
    assert "23:59 GMT" in md and "推荐信" in md


def test_checklist_without_text_says_so():
    md = ac.checklist_md(OPP, ac.extract_checklist(""), None, False)
    assert "posting.txt" in md and "原文未写明" in md


def test_strip_cites_and_clean(tmp_path):
    assert ac.strip_cites("I did X [cv:proj1].") == "I did X."
    assert ac.strip_cites("见原文 [post]。") == "见原文。"
    d = make_dir(tmp_path, GOOD)
    facts = tmp_path / "facts.yml"
    facts.write_text(yaml.safe_dump(LIN, allow_unicode=True), encoding="utf-8")
    args = type("A", (), {"dir": str(d), "facts": str(facts), "force": False})
    assert ac.cmd_clean(args) == 0
    out = (d / "final" / "email.md").read_text(encoding="utf-8")
    assert "[cv:" not in out and "[lab:" not in out and "Lin Xiaozhou" in out


def test_find_opportunity_from_postings():
    postings = [{"id": "jobs-ac-uk:X1", "title": "T", "url": "https://a.example/x1", "deadline": "2027-01-01"}]
    assert ac.find_opportunity("https://a.example/x1", postings, [])["id"] == "jobs-ac-uk:X1"
    assert ac.find_opportunity("https://b.example/y", [], [])["kind"] == "url"
    with pytest.raises(SystemExit):
        ac.find_opportunity("nope", [], [])


def test_edit_ratio():
    assert ac.edit_ratio("a b c d", "a b c d") == 0
    assert 0 < ac.edit_ratio("a b c d", "a b x d") < 0.5


def test_profile_schema_facts_format(tmp_path):
    """docs/profile-schema.md 的 facts 列表格式（产品 C）同样适用。"""
    zhou = yaml.safe_load((FIX / "zhou-muyang.yml").read_text(encoding="utf-8"))
    idx = ac.fact_index(zhou)
    assert {"edu-1", "pub-1", "proj-1", "lang-1"} <= set(idx)
    good = ("Dear Dr Hu,\n\nI synthesised five polyoxometalate clusters and cycled more than 200 coin cells [cv:proj-1].\n"
            "My first-author paper appeared in the Journal of Energy Chemistry in 2025 [cv:pub-1].\n\nBest regards,\nZhou Muyang\n")
    assert errors(ac.check_dir(make_dir(tmp_path, good), zhou)) == []
    bad = good + "My best cell kept 85% capacity after 500 cycles [cv:proj-1].\n"
    (tmp_path / "app" / "drafts" / "email.md").write_text(bad, encoding="utf-8")
    assert errors(ac.check_dir(tmp_path / "app", zhou))


def test_identity_from_profile(tmp_path):
    facts = {"facts": [{"id": "edu-1", "text": "MSc Statistics"}]}
    draft = "Best regards,\nWang Lan\n"
    assert errors(ac.check_dir(make_dir(tmp_path, draft), facts))
    assert errors(ac.check_dir(tmp_path / "app", facts, {"name": "Wang Lan"})) == []


@pytest.mark.parametrize("sentence", [
    "Southlake University awarded me a full scholarship [cv:edu1].",
    "Imperial College London hosted my summer internship.",
])
def test_sentence_initial_names_are_checked(tmp_path, sentence):
    assert errors(ac.check_dir(make_dir(tmp_path, GOOD + "\n" + sentence + "\n"), LIN))


def test_checklist_shows_posting_fields_and_prefills_supervisor(tmp_path, monkeypatch):
    fields = {"documents": {"value": "动机信、简历", "quote": "Required Documents Motivation letter CV"},
              "supervisor": {"value": "Dr Shan Hu", "quote": "Supervisor: Dr Shan Hu"}, "checked": "2026-10-19"}
    md = ac.checklist_md(OPP, ac.extract_checklist(POSTING), fields, True)
    assert "| 材料清单 | 动机信、简历 | Required Documents Motivation letter CV |" in md
    monkeypatch.setattr(ac, "find_opportunity", lambda key: dict(OPP))
    monkeypatch.setattr(ac, "load_fields", lambda: {"test:1": fields})
    txt = tmp_path / "p.txt"
    txt.write_text(POSTING, encoding="utf-8")
    args = type("A", (), {"key": "test:1", "out_root": str(tmp_path), "text_file": str(txt), "no_fetch": True})
    assert ac.cmd_prepare(args) == 0
    lab = yaml.safe_load((tmp_path / "test-1" / "lab.yml").read_text(encoding="utf-8"))
    assert lab["supervisor"]["name"] == "Dr Shan Hu"
    assert (tmp_path / "test-1" / "posting.txt").read_text(encoding="utf-8") == POSTING


def test_red_team_eval_catches_all_fabrications(tmp_path, monkeypatch, capsys):
    """apply_eval.py 对合格文书逐句造编造变体：除“出处张冠李戴”外必须全部拦下。"""
    import apply_eval

    d = make_dir(tmp_path, GOOD)
    facts = tmp_path / "facts.yml"
    facts.write_text(yaml.safe_dump(LIN, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["apply_eval.py", str(d), "--facts", str(facts)])
    assert apply_eval.main() == 0, capsys.readouterr().out
    assert "漏网 0 条" in capsys.readouterr().out


@pytest.mark.parametrize("sentence", [
    "I maintained the lab's server and analysed survey data [cv:proj1].",          # 张冠李戴：proj1 不是这个内容（且无出处支持）
    "I also gained experience with solid-state electrodes.",                     # 经历句无出处（非常见动词）
    "My imaging experience covers confocal microscopy.",                          # my … experience
    "我操作过原位拉曼池。",                                                         # 我…过
    "I studied at Northbridge University in 2025–2025 [cv:edu1].",               # 年份区间不符
    "My first-author paper was published in 2026.",                              # 无出处的一作 / 已发表
])
def test_more_fabrications_are_caught(tmp_path, sentence):
    assert errors(ac.check_dir(make_dir(tmp_path, GOOD + "\n" + sentence + "\n"), LIN))


def test_misattributed_citation():
    idx = ac.fact_index(LIN)
    body = "I built a particle filter in Python estimating route flows from link counts"
    assert ac.misattributed(body, ["proj2"], idx) is None
    assert "proj2" in ac.misattributed(body, ["award1"], idx)


# 只换说法、不换事实词的编造（针对三个虚构申请者）：程序必须全部拦下
SUBTLE = [
    ("lin-xiaozhou", "My paper on tuning MALA on the simplex via online acceptance-rate control has been widely cited [cv:pub1]."),
    ("lin-xiaozhou", "I designed the data-augmentation Gibbs sampler for regional disease counts with exact row and column totals myself, from scratch [cv:proj1]."),
    ("lin-xiaozhou", "The particle filter I built in Python estimating route flows from link counts is now used by a city traffic department [cv:proj2]."),
    ("lin-xiaozhou", "My MSc thesis on adaptive tuning of Metropolis-adjusted Langevin algorithms on the probability simplex proved convergence guarantees [cv:edu1]."),
    ("lin-xiaozhou", "In the disease mapping project, my Gibbs sampler for regional disease counts was the main contribution of the group [cv:proj1]."),
    ("zhou-muyang", "I developed the in situ Raman cell for solid-state electrodes that the group now uses [cv:proj-2]."),
    ("zhou-muyang", "In my Journal of Energy Chemistry paper, the polyoxometalate anchoring layers completely eliminated polysulfide shuttling in Li-S cells [cv:pub-1]."),
    ("zhou-muyang", "I synthesised five polyoxometalate clusters that had never been reported before [cv:proj-1]."),
    ("zhou-muyang", "My cyclic voltammetry, XRD and XPS results were featured on the journal cover [cv:proj-1]."),
    ("zhou-muyang", "My second-author ChemElectroChem paper on in situ Raman tracking of sulfur speciation was mostly my own work [cv:pub-2]."),
    ("chen-ruoxi", "My 6-week heat-stress experiment on Acropora and Pocillopora fragments showed that Pocillopora recovered faster after bleaching [cv:proj-1]."),
    ("chen-ruoxi", "I designed and built the 12-tank recirculating aquarium system for the heat-stress experiment [cv:proj-1]."),
    ("chen-ruoxi", "As a volunteer at Southbay Public Aquarium I was responsible for the entire coral collection [cv:work-1]."),
    ("chen-ruoxi", "I measured photosynthetic efficiency of Acropora and Pocillopora fragments with PAM fluorometry every day [cv:proj-1]."),
]


@pytest.mark.parametrize("who,sentence", SUBTLE)
def test_subtle_fabrications_are_caught(who, sentence):
    facts = ac.fact_index(yaml.safe_load((FIX / f"{who}.yml").read_text(encoding="utf-8")))
    errs, _ = ac.check_sentence(sentence, facts, {}, None, "")
    assert errs, sentence


@pytest.mark.parametrize("who,sentence", [
    ("chen-ruoxi", "I measured photosynthetic efficiency with PAM fluorometry twice a week [cv:proj-1]."),
    ("zhou-muyang", "I synthesised five polyoxometalate clusters and characterised them by XRD, XPS and cyclic voltammetry [cv:proj-1]."),
    ("lin-xiaozhou", "In a course project which I led, I built a particle filter in Python estimating route flows from link counts [cv:proj2]."),
])
def test_faithful_sentences_pass(who, sentence):
    facts = ac.fact_index(yaml.safe_load((FIX / f"{who}.yml").read_text(encoding="utf-8")))
    errs, _ = ac.check_sentence(sentence, facts, {}, None, "")
    assert errs == [], errs


def test_known_false_positives_now_pass(tmp_path):
    """演示中起草子代理报告的误报：缩写、计划时长、中文序数。"""
    post = "The project uses optical coherence tomography and sequential Monte Carlo."
    facts = ac.fact_index(LIN)
    for s in ["The project uses OCT to image coral tissue [post].",
              "前 6–12 个月：先复现岗位提到的 SMC 方法 [post]。",
              "Year 1: reproduce the baseline samplers.",
              "紧随其后的第二位作者是我导师。".replace("我导师", "导师")]:
        errs, _ = ac.check_sentence(s, facts, {}, post, "")
        assert errs == [], (s, errs)
    errs, _ = ac.check_sentence("I have 6 years of experience with Stan.", facts, {}, post, "")
    assert errs  # 经历句里的时长仍要出处


def test_quantifier_overclaim():
    facts = ac.fact_index(yaml.safe_load((FIX / "zhou-muyang.yml").read_text(encoding="utf-8")))
    bad = "I assembled and cycled more than 200 coin cells, all of which kept 78% capacity after 500 cycles at 1C [cv:proj-1]."
    good = "I assembled and cycled more than 200 coin cells; the best cell kept 78% capacity after 500 cycles at 1C [cv:proj-1]."
    assert ac.check_sentence(bad, facts, {}, None, "")[0]
    assert ac.check_sentence(good, facts, {}, None, "")[0] == []


@pytest.mark.parametrize("sentence,ok", [
    ("I have two specific questions.", True),
    ("I am Lin Xiaozhou.", True),
    ("I have not worked on diffusion limits.", True),       # 如实说明缺口
    ("I have no experience with Stan, but I hope to learn.", True),
    ("I completed my MSc at Northbridge University in June 2026 [cv:edu1].", True),
    ("I have two papers.", False),
    ("I am a final-year student.", False),
])
def test_identity_gaps_and_questions(sentence, ok):
    errs, _ = ac.check_sentence(sentence, ac.fact_index(LIN), {}, None, "Lin Xiaozhou lin.xz@example.com")
    assert (errs == []) == ok, errs


def test_degree_level_must_match_citation():
    facts = ac.fact_index(yaml.safe_load((FIX / "zhou-muyang.yml").read_text(encoding="utf-8")))
    assert ac.check_sentence("我的硕士课题是多金属氧酸盐修饰的碳载体 [cv:edu-2]。", facts, {}, None, "")[0]
    assert ac.check_sentence("我的硕士课题是多金属氧酸盐修饰的碳载体 [cv:edu-1]。", facts, {}, None, "")[0] == []
    assert ac.check_sentence("During my BSc I studied chemistry [cv:edu-1].", facts, {}, None, "")[0]
