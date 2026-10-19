"""岗位采集脚本的离线测试（构造的详情页样例）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import collect_postings as cp  # noqa: E402

TODAY = "2026-10-18"

JAC_PAGE = """<html><script type="application/ld+json">{"@type":"JobPosting","title":"PhD Studentship: Tandem Catalysts",
"hiringOrganization":{"name":"University of Exeter"}}</script><body>
Qualification Type: PhD Location: Exeter Funding for: UK Students, EU Students, International Students
Funding amount: International tuition fees and an annual stipend of £21,805 Hours: Full Time
Placed On: 16th October 2026 Closes: 20th December 2026 Reference: 6024 Both UK and international applicants are eligible.
</body></html>"""

FAP_PAGE = """<html><h1>Machine learning for climate PhD</h1><body>
University of X Dr Y Application Deadline: 15 January 2027 Funded PhD Project (Students Worldwide) Visit institution website
</body></html>"""
FAP_ROLLING = """<html><script type="application/ld+json">{"@type":"JobPosting","title":"Quantum PhD","datePosted":"01/10/2026 10:00:00",
"jobLocation":{"@type":"Place","address":{"addressCountry":"GB"}}}</script><body>Heriot-Watt Dr Z Applications accepted all year round
Funded PhD Project (Students Worldwide) Visit institution website Funding Notes Full stipend and international fees are covered. References</body></html>"""


def test_parse_day():
    assert cp.parse_day("20th December 2026") == "2026-12-20"
    assert cp.parse_day("January 15, 2027") == "2027-01-15"
    assert cp.parse_day("15 January") is None  # 没有年份不猜


def test_jobs_ac_uk_detail():
    row, why = cp.jac_detail("DTH797", "https://www.jobs.ac.uk/job/DTH797/x", JAC_PAGE, TODAY)
    assert why == "收录"
    assert row["deadline"] == "2026-12-20" and row["cn"] == "yes" and row["level"] == "phd"
    assert row["quote"] in cp.page_text(JAC_PAGE)
    past, why = cp.jac_detail("A", "u", JAC_PAGE.replace("2026 Reference", "2025 Reference"), TODAY)
    assert past is None and why == "已截止"
    uk, _ = cp.jac_detail("B", "u", JAC_PAGE.replace(", EU Students, International Students", ""), TODAY)
    assert uk["cn"] == "no"


def test_findaphd_detail():
    row, why = cp.fap_detail("123", "https://www.findaphd.com/phds/project/x/?p123", FAP_PAGE, TODAY)
    assert why == "收录" and row["deadline"] == "2027-01-15" and row["cn"] == "yes"
    self_funded = FAP_PAGE.replace("Funded PhD Project (Students Worldwide)", "Self-Funded PhD Students Only (UK Students Only)")
    assert cp.fap_detail("1", "u", self_funded, TODAY)[0] is None
    uk_only = FAP_PAGE.replace("Students Worldwide", "UK Students Only")
    assert cp.fap_detail("2", "u", uk_only, TODAY)[0]["cn"] == "no"


def test_findaphd_rolling_needs_recent_post():
    row, why = cp.fap_detail("9", "u", FAP_ROLLING, TODAY)
    assert why == "收录" and row["deadline"] == "rolling" and row["country"] == "UK" and "international fees" in row["amount"]
    old = FAP_ROLLING.replace("01/10/2026", "19/10/2025")
    assert cp.fap_detail("9", "u", old, TODAY) == (None, "全年招生但发布超过 90 天")


def test_findaphd_weekday_deadline():
    page = FAP_PAGE.replace("Application Deadline: 15 January 2027", "Tuesday, February 02, 2027")
    row, why = cp.fap_detail("7", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2027-02-02" and row["quote"] == "Tuesday, February 02, 2027"


def test_academictransfer_detail():
    page = """<html><script type="application/ld+json">{"@type":"JobPosting","title":"PhD: Lensless 3D optical imaging",
"hiringOrganization":{"name":"ARCNL"}}</script><body>PhD: Lensless 3D optical imaging Deadline 17 Nov ’26 Published 21 May ’26
Salary indication max. €3115 per month Location Amsterdam</body></html>"""
    row, why = cp.at_detail("361214", "https://www.academictransfer.com/en/jobs/361214/phd-x/", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-17" and row["amount"] == "max. €3115 per month"


def test_naturecareers_detail():
    page = """<html><h1>Postdoctoral Fellow Position – Cancer Immunotherapies</h1><body>Employer University of Maryland School of Medicine
Location 21201, Baltimore Salary 65,000 Closing date 15 Jan 2027 Website https://x</body></html>"""
    row, why = cp.nc_detail("12865818", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2027-01-15" and row["level"] == "postdoc"
    assert row["org"] == "University of Maryland School of Medicine" and row["amount"] == "65,000"


def test_dedupe_across_platforms():
    a = {"id": "jobs-ac-uk:1", "title": "PhD Studentship: Tandem Catalysts for CO2 Electrolysis", "org": "University of Exeter",
         "deadline": "2026-12-20", "url": "u1", "via": "jobs.ac.uk", "cn": "check", "amount": "£21,805"}
    b = {"id": "findaphd:2", "title": "Tandem catalysts for CO2 electrolysis (Fully Funded)", "org": "University of Exeter",
         "deadline": "2026-12-20", "url": "u2", "via": "FindAPhD", "cn": "yes", "amount": ""}
    c = dict(a, id="jobs-ac-uk:3", title="Postdoc in Optics", url="u3")
    out, dropped = cp.dedupe([a, b, c])
    assert dropped == 1 and len(out) == 2
    merged = next(r for r in out if r["id"] == "jobs-ac-uk:1")
    assert merged["cn"] == "yes" and merged["also"] == ["u2"]


def test_dedupe_keeps_same_platform_namesakes():
    a = {"id": "jobs-ac-uk:1", "title": "Postdoctoral Research Associate", "org": "University of Edinburgh",
         "deadline": "2026-10-19", "url": "u1", "via": "jobs.ac.uk", "cn": "check"}
    b = dict(a, id="jobs-ac-uk:2", url="u2")
    out, dropped = cp.dedupe([a, b])
    assert dropped == 0 and len(out) == 2


def test_madgex_us_date_format():
    page = """<html><h1>Michelson Postdoctoral Prize Lectureship</h1><body>Employer Case Western Reserve University Location Ohio
Salary 0 Posted Oct 16, 2026 Closes Dec 15, 2026 Discipline Physics</body></html>"""
    urls, detail = cp.madgex("physicstoday")
    row, why = detail("42020982", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-12-15" and row["amount"] == "" and row["via"] == "Physics Today Jobs"


def test_varbi_detail_english_date():
    page = """<html><title>PhD student in physics at Lund University</title><h1>PhD student in physics</h1><body>
Published 16.Oct.2026 Last application date 08.Nov.2026 Login and apply</body></html>"""
    row, why = cp.vb_detail("977396", "https://lu.varbi.com/en/what:job/jobID:977396/", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-08" and row["org"] == "Lund University"


def test_find_deadline_formats():
    assert cp.find_deadline("The deadline for applications is October 27, 2026 (16:00 CET).")[0] == "2026-10-27"
    assert cp.find_deadline("Duration of contract : 12 months Deadline to apply : 2026-10-31 Warning")[0] == "2026-10-31"
    assert cp.find_deadline("Bewerbungsfrist: 15.11.2026")[0] == "2026-11-15"
    assert cp.find_deadline("Bewerbungsschluss ist der 3. Dezember 2026.")[0] == "2026-12-03"
    assert cp.find_deadline("Application deadline: 15 January")[0] is None  # 没有年份不猜


def test_level_phd_research_fellow():
    assert cp.level_of("PhD Research Fellow in Marine Biology") == "phd"
    assert cp.level_of("Postdoctoral Research Fellow in Optics") == "postdoc"
    assert cp.level_of("Research Fellow in Electrochemistry") == "postdoc"


def test_the_unijobs_detail():
    page = """<html><h1 class="mds-font-s6">University Assistant Postdoctoral 1, Psychology</h1><body>Employer UNIVERSITY OF VIENNA
Location Vienna (Landbezirke) (AT) Salary The basic salary of EUR 5.079,50 (14 times a year) Closing date 24 Oct 2026 View more</body></html>"""
    _, detail = cp.madgex("the-unijobs")
    row, why = detail("416677", "https://www.timeshighereducation.com/unijobs/listing/416677/x/", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-24" and row["level"] == "postdoc" and row["via"] == "THE Unijobs"


def test_place_country():
    assert cp.place_country("Vienna (Landbezirke) (AT)") == "AT"
    assert cp.place_country("Canberra, ACT, Australian Capital Territory, Australia") == "AU"
    assert cp.place_country("21201, Baltimore") == ""
    assert cp.place_country("Memphis, Tennessee") == "US" and cp.place_country("Wien, Österreich") == "AT"
    assert cp.place_country("Benguerir, Morocco (MA)") == "MA"


def test_inspire_detail():
    rec = {"metadata": {"position": "Postdoctoral Fellowship in Theoretical Physics", "ranks": ["POSTDOC"], "status": "open",
                        "deadline_date": "2026-11-12", "regions": ["Europe"], "description": "<div>two-year fellowship</div>",
                        "institutions": [{"value": "INFN, Genoa", "record": {"$ref": "https://inspirehep.net/api/institutions/902881"}}]}}
    cp._INSPIRE_COUNTRY["https://inspirehep.net/api/institutions/902881"] = "IT"
    import json
    row, why = cp.inspire_detail("3070001", "u", json.dumps(rec), TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-12" and row["country"] == "IT" and row["url"].endswith("/jobs/3070001")
    rec["metadata"]["ranks"] = ["SENIOR"]
    assert cp.inspire_detail("1", "u", json.dumps(rec), TODAY)[0] is None


def test_ajo_detail():
    cp._AJO["33125"] = {"univ": "Ghent University", "dept": "Mechanics of Materials and Structures", "country": "BE", "city": "Gent",
                        "desc": "[Net salary (after taxes) starting from 2900 EUR/month] Belgium has been"}
    page = """<html><body>Position Title: Postdoc (3 years) on numerical simulation of composite hydrogen tanks (Belgium)
Position Type: Postdoctoral Position Appl Deadline: 2027/01/31 12:00:00 (posted 2026/10/17 , listed until 2027/04/17)
Position Description: Apply Position Description research</body></html>"""
    row, why = cp.ajo_detail("33125", "https://academicjobsonline.org/ajo/jobs/33125", page, TODAY)
    assert why == "收录" and row["deadline"] == "2027-01-31" and row["country"] == "BE"
    assert row["amount"] == "Net salary (after taxes) starting from 2900 EUR/month"
    no_dl = page.replace("2027/01/31 12:00:00 ", "")
    assert cp.ajo_detail("33125", "u", no_dl, TODAY) == (None, "页面无截止日期")


def test_daad_detail():
    page = """<html><head><title>&quot;PhD position on Digital Twins of Magnesium Alloys&quot; -  Helmholtz-Zentrum Hereon - DAAD</title></head>
<body>Location Geesthacht Application Deadline 12. Nov 2026 Starting Date as soon as possible Overview Financing yes
Type of Position Full PhD Working Language English Required Degree Master Areas of study Physics Description x</body></html>"""
    url = "https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/detail/x-10489/?phd-id=10489"
    row, why = cp.daad_detail("10489", url, page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-12" and row["org"] == "Helmholtz-Zentrum Hereon"
    assert "Master" in row["requirements"]
    stay = page.replace("Full PhD", "1-2 Year Research Stay")
    assert cp.daad_detail("1", url, stay, TODAY) == (None, "非博士/博后岗位")
    assert cp.daad_detail("1", url, page.replace("Financing yes", "Financing no"), TODAY)[0] is None
