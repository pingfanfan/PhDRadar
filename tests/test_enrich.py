"""岗位结构化字段提取的离线测试（构造的详情页样例）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import enrich_postings as ep  # noqa: E402
from collect_postings import page_text  # noqa: E402

DAAD_PAGE = """<html><body><nav>Study and Research in Germany PhD Studies &amp; Research</nav>
PhD Detail Back to Overview <h1>PhD Student (f/m/d) Mineral systems</h1> Full PhD Working Language English Location Freiberg
Application Deadline 30. Nov 2026 Starting Date 01. Jan 2027 Overview Description Required Documents Application Overview
Open Positions 1 Time Span 01. Jan 2027 for 36 months Application Deadline 30. Nov 2026 Financing yes Type of Position Full PhD
Working Language English Required Degree Diplom Master Areas of study Geology Description Description The PhD student will ...
Required Documents Required Documents Motivation letter CV Certificates References Application Application
https://www.example.de/apply Contact HZDR Opens chatbot Address Deutscher Akademischer Austauschdienst</body></html>"""

JAC_PAGE = """<html><body>Find a Job Back to search results <h1>PhD Studentship: Monte Carlo Methods</h1>
University of Birmingham Qualification Type: PhD Location: Birmingham Funding for: UK Students, EU Students, International Students
Funding amount: £20,780 Hours: Full Time Placed On: 13th October 2026 Closes: 10th January 2027
Applicants should hold a first or upper second class degree in Mathematics. Applicants whose first language is not English
must have IELTS 6.5 with no less than 6.0 in any band. Share on social media More PhDs from University of Birmingham</body></html>"""


def body(via, raw):
    return ep.body_of(via, page_text(raw))


def test_body_trims_navigation_and_footer():
    b = body("DAAD PhDGermany", DAAD_PAGE)
    assert b.startswith("PhD Detail Back to Overview")
    assert "Deutscher Akademischer" not in b and "Study and Research" not in b
    b = body("jobs.ac.uk", JAC_PAGE)
    assert b.startswith("Back to search results") and "More PhDs" not in b


def test_daad_rules():
    b = body("DAAD PhDGermany", DAAD_PAGE)
    r = ep.rule_daad(b)
    assert r["degree"]["value"].startswith("硕士") and "Diplom" in r["degree"]["value"]
    assert r["language"] == {"value": "工作语言：英语", "quote": "Working Language English"}
    assert r["duration"]["value"] == "36 个月"
    assert r["start"]["value"] == "2027 年 1 月 1 日"
    assert r["documents"]["value"] == "动机信、学历证书、推荐信、简历"
    bn = ep.norm(b)
    assert all(ep.check_field(k, v, bn) is None for k, v in r.items())


def test_daad_unknown_document_left_to_subagent():
    page = DAAD_PAGE.replace("Motivation letter CV", "Motivation letter Portfolio of artworks CV")
    assert "documents" not in ep.rule_daad(body("DAAD PhDGermany", page))


def test_jac_funding_for_rule():
    r = ep.rule_jac(body("jobs.ac.uk", JAC_PAGE))
    assert r["nationality"]["value"] == "资助对象：英国学生、欧盟学生、国际学生"
    assert ep.rule_jac("Funding for: Self-funded applicants Hours: Full Time") == {}  # 不认识的不写


def test_quote_must_be_in_page():
    bn = ep.norm(body("jobs.ac.uk", JAC_PAGE))
    ok = {"value": "英语非母语需 IELTS 6.5，单项不低于 6.0",
          "quote": "must have IELTS 6.5 with no less than 6.0 in any band"}
    assert ep.check_field("language", ok, bn) is None
    # 改写过的原句不通过
    bad = {"value": "需 IELTS 6.5", "quote": "IELTS 6.5 is required"}
    assert ep.check_field("language", bad, bn) == "原句不在正文"
    # 用省略号拼接两处也不通过
    bad = {"value": "需 IELTS 6.5", "quote": "Applicants should hold ... IELTS 6.5"}
    assert ep.check_field("language", bad, bn) == "原句不在正文"


def test_numbers_only_from_quote():
    bn = ep.norm(body("jobs.ac.uk", JAC_PAGE))
    bad = {"value": "需 IELTS 7.0", "quote": "must have IELTS 6.5 with no less than 6.0 in any band"}
    assert ep.check_field("language", bad, bn).startswith("数字不在原句")
    text = ep.norm("The employment will be for a period of four years, starting in September 2027.")
    assert ep.check_field("duration", {"value": "4 年", "quote": "for a period of four years"}, text) is None
    assert ep.check_field("duration", {"value": "四年", "quote": "for a period of four years"}, text) is None
    assert ep.check_field("duration", {"value": "三年", "quote": "for a period of four years"}, text).startswith("数字")
    assert ep.check_field("start", {"value": "2027 年 9 月", "quote": "starting in September 2027"}, text) is None
    assert ep.numbers("€3,204 and 01") == {"3204", "1"}


def test_quote_normalisation():
    text = ep.norm("A Master’s degree (or comparable) in physics; ob\xadtai\xadning – soon")
    assert ep.check_field("degree", {"value": "物理硕士", "quote": "A Master's degree (or comparable) in physics"}, text) is None
    assert ep.norm("obtaining - soon") in text


def test_field_format_checks():
    text = ep.norm("Please send your application by email to jobs@example.org before the deadline.")
    q = "Please send your application by email to jobs@example.org"
    assert ep.check_field("apply_via", {"value": "邮件：jobs@example.org", "quote": q}, text) is None
    assert ep.check_field("apply_via", {"value": "通过邮箱", "quote": q}, text) == "申请方式格式"
    assert ep.check_field("degree", {"value": "未写明", "quote": q}, text) == "空话"
    assert ep.check_field("salary", {"value": "x", "quote": q}, text) == "未知字段"
    assert ep.check_field("degree", "硕士", text) == "格式不对"


def test_apply_rows_keeps_rules_and_drops_bad_fields():
    b = body("jobs.ac.uk", JAC_PAGE)
    data = {"jobs-ac-uk:X": {"checked": "2026-10-19", "nationality": {"value": "规则", "quote": "Funding for: UK Students"}}}
    rows = [{"id": "jobs-ac-uk:X", "fields": {
        "nationality": {"value": "子代理", "quote": "International Students"},
        "degree": {"value": "数学一等或二等一学位", "quote": "Applicants should hold a first or upper second class degree in Mathematics"},
        "language": {"value": "IELTS 7", "quote": "IELTS 7 overall"},
        "documents": None}},
        {"id": "not-in-bundle", "fields": {}}]
    stats = ep.apply_rows(data, rows, {"jobs-ac-uk:X": b}, "2026-10-19")
    rec = data["jobs-ac-uk:X"]
    assert rec["nationality"]["value"] == "规则"  # 规则结果不被覆盖
    assert "degree" in rec and "language" not in rec and "documents" not in rec
    assert rec["llm"] == "2026-10-19"
    assert stats["原句不在正文"] == 1 and stats["id 不在输入"] == 1


def test_parse_out_tolerates_fences(tmp_path):
    p = tmp_path / "out-001.yml"
    p.write_text("```yaml\n- id: a\n  fields: {}\n```\n", encoding="utf-8")
    assert ep.parse_out(p) == [{"id": "a", "fields": {}}]


def test_numbers_dates_ordinals_and_nordic_words():
    q = "Startdate: 01.12.2026"
    assert ep.check_field("start", {"value": "2026 年 12 月 1 日", "quote": q}, ep.norm(q)) is None
    q = "two-year appointment, with the possibility of renewal for a third year"
    assert ep.check_field("duration", {"value": "两年，可续第三年", "quote": q}, ep.norm(q)) is None
    q = "dock minst två år och max 3 år"
    assert ep.check_field("duration", {"value": "至少两年、最长 3 年", "quote": q}, ep.norm(q)) is None
    q = "Tillträde januari 2027 eller enligt överenskommelse."
    assert ep.check_field("start", {"value": "2027 年 1 月或协商", "quote": q}, ep.norm(q)) is None
    q = "The employment duration is 3 years."  # 原句没有 1.5，简述写了就丢弃
    assert ep.check_field("duration", {"value": "3 年（先签 1.5 年）", "quote": q}, ep.norm(q)).startswith("数字")


def test_inria_rules():
    b = ("Inria job offers > Offer #2026-10502 Contract type : Fixed-term contract Level of qualifications required : "
         "PhD or equivalent Fonction : Post-Doctoral Research Visit General Information Starting date : 2027-01-01 "
         "Duration of contract : 1 year, 6 months Deadline to apply : 2026-11-30 Warning : you must enter your e-mail "
         "address in order to save your application to Inria. Applications must be submitted online on the Inria website.")
    r = ep.rule_inria(b)
    assert r["degree"]["value"] == "博士或同等学历"
    assert r["duration"]["value"] == "1 年 6 个月"
    assert r["apply_via"]["value"].startswith("在线系统")
    assert "start" not in r  # 开始日期栏目常过期，不用规则
    assert all(ep.check_field(k, v, ep.norm(b)) is None for k, v in r.items())


def test_french_and_german_number_words():
    q = "Contrat de trois ans à partir de janvier 2027"
    assert ep.check_field("duration", {"value": "3 年，2027 年 1 月起", "quote": q}, ep.norm(q)) is None
    q = "Die Stelle ist auf drei Jahre befristet"
    assert ep.check_field("duration", {"value": "3 年", "quote": q}, ep.norm(q)) is None


def test_portuguese_spanish_italian_words():
    q = "Inicio: novembro de 2026"
    assert ep.check_field("start", {"value": "2026 年 11 月", "quote": q}, ep.norm(q)) is None
    q = "dois nomes de referência com email"
    assert ep.check_field("documents", {"value": "两位推荐人", "quote": q}, ep.norm(q)) is None
    q = "contratto di tre anni a partire da gennaio 2027"
    assert ep.check_field("duration", {"value": "3 年，2027 年 1 月起", "quote": q}, ep.norm(q)) is None


def test_jobbnorge_body_from_listing_json():
    d = {"activeLanguages": [1, 2], "components": [
        {"typeId": 0, "heading": "PhD Fellowship in railway systems", "text": ""},
        {"typeId": 4, "heading": "Qualification requirements",
         "text": "<ul><li>A master's degree in civil engineering</li><li>Very good English skills</li></ul>"},
        {"typeId": 3, "image": {}},
        {"typeId": 1, "heading": "About us", "column1": "<p>OsloMet is ...</p>"},
    ], "contacts": [{"name": "Mahdi Kioumarsi", "title": "Professor", "email": "x@oslomet.no"}]}
    body = ep.jobbnorge_body(d)
    assert body.startswith("PhD Fellowship in railway systems Qualification requirements")
    assert "master's degree in civil engineering" in body and "Very good English skills" in body
    assert "About us" not in body and "OsloMet is" not in body
    assert body.endswith("Contact: Mahdi Kioumarsi, Professor")
    assert "Jobbnorge" not in ep.SKIP_VIA and "Jobbnorge" not in ep.NO_FETCH


def test_findaphd_body_and_import(tmp_path, monkeypatch):
    import collect_postings as cp
    raw = ("<html><nav>PhDs Events Funding</nav><h1>Flexible thermoelectrics</h1><p>About the Project</p>"
           "<p>Supervisory team: Professor Iris Nandhakumar. " + "Project text. " * 30 + "</p>"
           "<p>Entry requirements A UK 2:1 honours degree, or its international equivalent.</p>"
           "<p>Funding Notes Full stipend.</p><p>Register your interest for this project</p><form>Dialling code</form></html>")
    cp.save_text(tmp_path / "texts", "findaphd:200322", raw)
    body = (tmp_path / "texts" / "findaphd_200322.txt").read_text(encoding="utf-8")
    assert body.startswith("About the Project") and "Entry requirements A UK 2:1" in body
    assert "Funding Notes Full stipend." in body and "Register your interest" not in body and "Dialling" not in body
    monkeypatch.setattr(ep, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(ep, "live_postings", lambda today: [{"id": "findaphd:200322", "via": "FindAPhD"}])
    assert ep.cmd_import_texts(type("A", (), {"dir": str(tmp_path / "texts"), "today": "2026-10-22"})()) == 0
    assert (tmp_path / "cache" / "findaphd_200322.txt").read_text(encoding="utf-8") == body
    assert "FindAPhD" in ep.NO_FETCH
