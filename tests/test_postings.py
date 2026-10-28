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


def test_expand_sources():
    assert cp.expand("actions") == list(cp.ACTIONS)
    assert "findaphd" not in cp.expand("default")
    assert cp.expand("default,findaphd")[-1] == "findaphd"
    try:
        cp.expand("nope")
    except SystemExit:
        pass
    else:
        raise AssertionError("未知平台应报错")


def test_import_merges_several_platforms():
    import import_postings as ip

    def row(i, via, checked, deadline="2026-12-01"):
        return {"id": f"{via}:{i}", "title": f"PhD {i}", "org": via, "deadline": deadline, "url": f"u{via}{i}", "via": via,
                "checked": checked}

    local = [row(1, "FindAPhD", "2026-10-17"), row(2, "Varbi", "2026-10-18"), row(3, "KU Leuven", "2026-10-19")]
    remote = [row(4, "FindAPhD", "2026-10-18"), row(5, "FindAPhD", "2026-10-18", "2026-10-01"),
              row(6, "KU Leuven", "2026-10-18"), row(7, "Varbi", "2026-10-19")]
    rows, notes = ip.merge(local, remote, ["FindAPhD", "KU Leuven", "Inria Jobs"], TODAY)
    ids = {r["id"] for r in rows}
    assert ids == {"FindAPhD:4", "Varbi:2", "KU Leuven:3"}  # FindAPhD 替换并去掉已截止；KU Leuven 远端更旧不替换；Varbi 不在清单不动
    assert len(notes) == 4


def test_arbeitsagentur_detail():
    import json
    import platforms_de as de
    job = {"stellenangebotsTitel": "Doktorand\\*in (w/m/d)", "firma": "Universität Duisburg-Essen",
           "verguetungsangabe": "JAHRESGEHALT", "gehaltsspanneVon": 38560.0, "gehaltsspanneBis": 54807.0,
           "stellenlokationen": [{"adresse": {"ort": "Essen, Ruhr"}}],
           "stellenangebotsBeschreibung": "## Doktorand\\*in\n\n**(TV-L 13, 65 %)** Die Stelle ist bis zum 31.12.2029 befristet.\n\n"
                                          "**Bewerbungsfrist:** 05.11.2026 [Hier bewerben](https://example.org)"}
    row, why = de.ba_detail("10000-1-S", "u", json.dumps(job), TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-05" and row["quote"] == "Bewerbungsfrist: 05.11.2026"
    assert row["url"].endswith("/jobdetail/10000-1-S") and row["amount"] == "38,560–54,807 € / Jahr" and row["country"] == "DE"
    assert row["title"] == "Doktorand*in (w/m/d)"
    # 合同期限“bis zum 31.12.2029”不是截止日期；“bis zum”要有申请语境
    job["stellenangebotsBeschreibung"] = "TV-L 13. Die Stelle ist bis zum 31.12.2029 befristet."
    assert de.ba_detail("1", "u", json.dumps(job), TODAY) == (None, "页面无截止日期")
    job["stellenangebotsBeschreibung"] = "TV-L 13. Bitte bewerben Sie sich bis zum 9. November 2026 unter der Kennziffer 26-1."
    assert de.ba_detail("1", "u", json.dumps(job), TODAY)[0]["deadline"] == "2026-11-09"
    job["stellenangebotsTitel"] = "Expert Promotion Category Management (m/w/d)"
    assert de.ba_detail("1", "u", json.dumps(job), TODAY) == (None, "非博士/博后岗位")
    assert cp.ADAPTERS["arbeitsagentur"] and cp.HEADERS["arbeitsagentur"] == {"X-API-Key": "jobboerse-jobsuche"}


# ───── 2026-10 抽检 300 条后补的规则 ─────

def test_madgex_body_deadline_overrides_listing_date():
    page = """<html><h1>Postdoctoral Fellowship in Climate Dynamics</h1><body>Employer Harvard University Location Cambridge, MA
Salary $92,000 Closing date 23 Oct 2026 Applications and letters are due November 1, 2026, and should be submitted online.</body></html>"""
    row, why = cp.nc_detail("1", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-01" and "November 1, 2026" in row["quote"] and row["country"] == "US"


def test_madgex_until_filled_is_rolling():
    page = """<html><h1>Postdoctoral Researcher in Bioengineering</h1><body>Employer Rice University Location Houston, TX
Salary 65,000 Closing date 14 Nov 2026 Applications will be reviewed immediately and until the position is filled.</body></html>"""
    row, _ = cp.nc_detail("2", "u", page, TODAY)
    assert row["deadline"] == "rolling" and "until the position is filled" in row["quote"]


def test_madgex_rejects_contract_gigs_and_reads_eligibility():
    gig = """<html><h1>Remote Chemistry Expert (PhD)</h1><body>Employer Turing Location Remote Salary $100 Closes Oct 23, 2026
Remote contract for PhDs in Chemistry. Pay rate: $100+/hour</body></html>"""
    _, detail = cp.madgex("physicstoday")
    assert detail("3", "u", gig, TODAY)[0] is None
    q = """<html><h1>Postdoctoral Fellow in Nuclear Nonproliferation</h1><body>Employer LBNL Location Berkeley, CA Salary 90,000
Closes Nov 26, 2026 Eligibility to obtain and maintain a DOE Q-level security clearance, which requires U.S. citizenship.</body></html>"""
    row, _ = detail("4", "u", q, TODAY)
    assert row["cn"] == "no" and row["flags"] == ["security-screening"]
    ok = q.replace("Eligibility to obtain and maintain a DOE Q-level security clearance, which requires U.S. citizenship.",
                   "We welcome applications from any nationality.")
    assert detail("5", "u", ok, TODAY)[0]["cn"] == "yes"


def test_jobs_ac_uk_home_fee_difference_is_restricted():
    page = JAC_PAGE.replace("Both UK and international applicants are eligible.",
                            "International students must pay the difference between the Home and International tuition fees themselves.")
    row, _ = cp.jac_detail("C", "u", page, TODAY)
    assert row["cn"] == "no"
    uk_fees = JAC_PAGE.replace("International tuition fees and an annual stipend", "UK tuition fees and an annual stipend") \
                      .replace("Both UK and international applicants are eligible.", "")
    assert cp.jac_detail("D", "u", uk_fees, TODAY)[0]["cn"] == "yes"  # 页头写明含国际生、正文没写自付差额：按页面说的算
    label_uk = JAC_PAGE.replace(", EU Students, International Students", "").replace(
        "Both UK and international applicants are eligible.", "Studentships cover fees at home or international rates.")
    assert cp.jac_detail("E", "u", label_uk, TODAY)[0]["cn"] == "check"


def test_inspire_competitive_call_and_until_filled():
    import json
    rec = {"metadata": {"position": "Postdoctoral position", "ranks": ["POSTDOC"], "status": "open", "deadline_date": "2026-11-26",
                        "institutions": [], "description": "The group welcomes expressions of interest from researchers wishing "
                        "to apply through the Juan de la Cierva (JdC) 2026 fellowship program."}}
    assert cp.inspire_detail("1", "u", json.dumps(rec), TODAY) == (None, "未写资助或自费")
    rec["metadata"]["description"] = "Two-year postdoc. This posting will remain open until filled."
    row, _ = cp.inspire_detail("2", "u", json.dumps(rec), TODAY)
    assert row["deadline"] == "rolling"
    rec["metadata"]["description"] = "The deadline is December 20, 2026. TDLI invites candidates of all nationalities."
    row, _ = cp.inspire_detail("3", "u", json.dumps(rec), TODAY)
    assert row["deadline"] == "2026-12-20" and row["cn"] == "yes"


def test_institute_zrr_and_earliest_deadline():
    _, detail = cp.institute("inria")
    page = """<html><h1>Post-Doctoral Research Visit F/M Graph learning</h1><body>Deadline to apply : 2026-11-18
The deadline of application is 15th November, 2026. Defence Security : This position is likely to be situated in a restricted
area (ZRR). Remuneration 2788 euros gross per month</body></html>"""
    row, why = detail("2026-10622", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-15" and row["flags"] == ["security-screening"] and "2788" in row["amount"]
    assert detail("x", "u", page + " Funding for this postdoc position has not yet been secured.", TODAY)[0] is None


def test_daad_org_from_contact_headline():
    page = """<html><head><title>&quot;PhD Position: Active Matter&quot; - Leipzig University Molecular Nanophotonics Group Frank Cichos - DAAD</title></head>
<body>Location Leipzig Application Deadline 22. Oct 2026 Financing yes Type of Position Full PhD
<h3 class="qa-headline u-size-24">Leipzig University<br>Molecular Nanophotonics Group<br>Frank Cichos</h3></body></html>"""
    row, why = cp.daad_detail("10479", "u", page, TODAY)
    assert why == "收录" and row["org"] == "Leipzig University"


def test_varbi_org_full_name():
    page = """<html><h1>PhD in Sociology of Law</h1><body>Last application date 08.Nov.2026</body></html>"""
    row, _ = cp.vb_detail("980150", "https://lu.varbi.com/en/what:job/jobID:980150/", page, TODAY)
    assert row["org"] == "Lund University"


def test_level_excludes_faculty_and_gigs():
    assert cp.level_of("Doctoral Research Faculty - Molecular Oncology") is None
    assert cp.level_of("Faculty - MD, PhD, MD/PhD, equivalent") is None
    assert cp.level_of("Remote Chemistry Expert (PhD)") is None
    assert cp.level_of("Postdoctoral Researcher in Legal History (Faculty of Law)") == "postdoc"
    assert cp.level_of("Future Faculty in the Physical Sciences Postdoctoral Fellowship") == "postdoc"


def test_dedupe_specific_title_different_deadlines():
    a = {"id": "naturecareers:1", "title": "Postdoctoral Associate - Aortic Imaging & Clinical Research", "deadline": "2026-11-11",
         "org": "Baylor College of Medicine (BCM)", "url": "u1", "via": "Nature Careers", "cn": "check"}
    b = dict(a, id="sciencecareers:2", org="Baylor College of Medicine", deadline="2026-10-27", url="u2", via="Science Careers")
    out, dropped = cp.dedupe([a, b])
    assert dropped == 1 and out[0]["id"] == "sciencecareers:2" and out[0]["also"] == ["u1"]  # 留截止更早的那条
    # 标题太泛（只剩“博后研究员”）或机构不同：不合并
    g = dict(a, title="Postdoctoral Research Associate")
    assert cp.dedupe([g, dict(g, id="x", via="Science Careers", url="u3", deadline="2026-12-01")])[1] == 0
    assert cp.dedupe([a, dict(b, org="University of Florida")])[1] == 0

def test_cnrs_detail():
    import platforms_fr as fr
    page = ("<html><h1>Thèse en physique du vivant (H/F)</h1><body>L'offre en un coup d'oeil L'unité Institut Lumière Matière "
            "Type de Contrat CDD Doctorant Temps de Travail Complet Lieu de Travail 69622 VILLEURBANNE Durée du contrat 36 mois "
            "Date d'Embauche 01/01/2027 Rémuneration La rémunération est de 2300 bruts mensuel Postuler "
            "Date limite de candidature : lundi 9 novembre 2026 23:59 Description du Poste</body></html>")
    row, why = fr.cnrs_detail("UMR5306-CLADES-001", "u", page, TODAY)
    assert why == "收录" and row["level"] == "phd" and row["deadline"] == "2026-11-09" and row["place"] == "Villeurbanne"
    assert row["amount"] == "La rémunération est de 2300 bruts mensuel" and row["org"] == "CNRS – Institut Lumière Matière"
    postdoc = page.replace("CDD Doctorant Temps", "Chercheur en contrat CDD Temps")
    assert fr.cnrs_detail("1", "u", postdoc, TODAY)[0]["level"] == "postdoc"
    engineer = page.replace("CDD Doctorant Temps", "Ingénieur en contrat CDD Temps")
    assert fr.cnrs_detail("1", "u", engineer, TODAY) == (None, "非博士/博后岗位")
    assert fr.cnrs_detail("1", "u", page.replace("9 novembre 2026", "9 octobre 2026"), TODAY) == (None, "已截止")
    xml = "<loc>https://emploi.cnrs.fr/Offres.aspx</loc><loc>emploi.cnrs.fr/Offres/Doctorant/UPR3572-HELDUM-001/Default.aspx</loc>"
    assert fr.CNRS_LOC.findall(xml) == [("emploi.cnrs.fr/Offres/Doctorant/UPR3572-HELDUM-001/Default.aspx", "UPR3572-HELDUM-001")]


def test_mathjobs_tamu_hnet_detail():
    import platforms_boards as b
    mj = ("<html><body>Position Title: PhD candidates in geometric analysis Position Type: Other Position Location: Canberra "
          "Appl Deadline: 2026/12/18 23:59:59 (posted 2026/09/29 , listed until 2026/12/18) Position Description: "
          "The candidates will be supported by scholarships funded through an ARC Discovery project.</body></html>")
    row, why = b.mj_detail("mj29069", "https://www.mathjobs.org/jobs/list/29069", mj, TODAY)
    assert why == "收录" and row["id"] == "mathjobs:29069" and row["via"] == "MathJobs" and row["deadline"] == "2026-12-18"
    tamu = ("<html><title>PhD Positions: Fish Ecology at Purdue University | Natural Resources Job Board</title><body>"
            "PhD Positions: Fish Ecology at Purdue University Purdue University (State) Details Application Deadline: 11/20/2026 Published: 10/15/2026 Salary: starting at $30,000 per year "
            "Education Required: Bachelors Experience Required: none Location: West Lafayette, Indiana Tags: Graduate Opportunities "
            "Description Two funded PhD positions.</body></html>")
    row, why = b.tamu_detail("1", "u", tamu, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-20" and row["org"] == "Purdue University" and row["country"] == "US"
    assert row["amount"] == "starting at $30,000 per year"
    assert b.tamu_detail("1", "u", tamu.replace("PhD Positions", "Graduate Assistantship (MS)"), TODAY) == (None, "非博士/博后岗位")
    hnet = ("<html><h1>Yale University - Henry Chauncey Postdoctoral Fellowship</h1><body>Position Post-Doctoral Fellow "
            "Location Connecticut, United States Subject Fields History Salary: $69,000 plus $5,000 for research expenses. "
            "Posting Date October 15, 2026 Closing Date January 8, 2027 Disclaimer</body></html>")
    row, why = b.hnet_detail("70582", "u", hnet, TODAY)
    assert why == "收录" and row["org"] == "Yale University" and row["deadline"] == "2027-01-08" and row["country"] == "US"
    assert row["amount"].startswith("Salary: $69,000")


def test_aarhus_detail():
    import platforms_dk as dk
    page = ("<html><h1>Postdoc in genetics of puberty</h1><body>The yearly base salary for a fulltime postdoc is between "
            "DKK 493.394,35 and DKK 585.322,48 depending on experience. Apply Deadline: Tuesday 10 Nov 2026 at 23:59 CET</body></html>")
    row, why = dk.au_detail("45001", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-10" and row["level"] == "postdoc" and "DKK 493.394,35" in row["amount"]
    assert dk.au_detail("1", "u", page.replace("Apply Deadline: Tuesday 10 Nov 2026 at 23:59 CET", ""), TODAY) == (None, "页面无截止日期")
    assert dk.au_detail("1", "u", page.replace("Postdoc in", "Student Assistant in"), TODAY) == (None, "非博士/博后岗位")


def test_institutes_psi_ibs_eso():
    psi = ("<html><h1 class='heading'>PhD Student in Materials Science</h1><body>Please submit your application online by "
           "<strong>5 November 2026&nbsp;</strong>(including list of publications)</body></html>")
    row, why = cp.ADAPTERS["psi"][1]("75342", "u", psi, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-05" and row["level"] == "phd" and row["country"] == "CH"
    ibs = ("<html><h1 id='t_logo'>IBS</h1><table><thead><tr><th>Title</th>\n<td colspan='5'>2026-6 Recruitment for Postdoctoral "
           "Research Associate Positions</td></tr></thead><tr><th>Closing Date</th><td>2026-11-06 18:00</td></tr></table></html>")
    row, why = cp.ADAPTERS["ibs"][1]("2187", "u", ibs, TODAY)
    assert why == "收录" and row["title"].startswith("2026-6 Recruitment") and row["deadline"] == "2026-11-06"
    eso = ("<html><h1 style='font-size: 40px;'>\nESO Studentship Programme Europe 2026/2027\n</h1><body>"
           "The upcoming deadline for applications is 20 October 2026 (including reference letters).</body></html>")
    row, why = cp.ADAPTERS["eso"][1]("2026_0055", "u", eso, TODAY)
    assert why == "收录" and row["level"] == "phd" and row["deadline"] == "2026-10-20"
    listing = 'href="/prog/recruit/eng/sub04_01/view.do;jsessionid=AB?pageIndex=1&amp;idx=2187"'
    f = type("F", (), {"get": lambda self, u: type("R", (), {"text": listing})()})()
    assert cp.ADAPTERS["ibs"][0](f, 1) == [("2187", "https://www.ibs.re.kr/prog/recruit/eng/sub04_01/view.do?idx=2187")]


def test_econjobmarket_detail():
    import platforms_boards as b
    page = ("<html><body>Login/Register Translate this website Postdoctoral Researcher (f/m/d) Advertiser: Ifo Institute "
            "Field(s) of specialization: International Trade Position type(s): Postdoctoral Scholar Location of job: Munich, "
            "Bavaria, 81679, Germany Degree required: Doctorate Salary: 68,200 EUR Letters of reference required: 3 "
            "Application deadline: 18 Nov 2026 midnight UTC Ad text: We are looking for a postdoc.</body></html>")
    row, why = b.ejm_detail("12844", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-18" and row["org"] == "Ifo Institute" and row["country"] == "DE"
    assert row["amount"] == "68,200 EUR"
    assert b.ejm_detail("1", "u", page.replace("Postdoctoral Scholar", "Assistant Professor"), TODAY)[0] is None


def test_until_date_is_deadline():
    t = "Review of applications will start as soon as possible and continue until January 13, 2027, or until the post is filled."
    assert cp.refine_deadline("2026-12-01", "q", t, TODAY) == ("2027-01-13", "continue until January 13, 2027")
    assert cp.refine_deadline("2026-12-01", "q", "Applications will be considered until the position is filled.", TODAY)[0] == "rolling"


def test_infn_and_pasteur_detail():
    import platforms_it as it
    page = ("<html><body>Dettaglio bando Numero 29226 Anno 2026 Titolo Selezione per il conferimento di n. 1 Incarico Post-Doc "
            "scientifico Numero posti 1 Tipo Incarico Post-Doc Data bando 16-10-2026 Data scadenza 26-10-2026 Bando (PDF)</body></html>")
    row, why = it.infn_detail("4699", "u", page, TODAY)
    assert why == "收录" and row["id"] == "infn:29226" and row["deadline"] == "2026-10-26" and row["quote"] == "Data scadenza 26-10-2026"
    prize = page.replace("Incarico Post-Doc scientifico", "Premio nazionale").replace("Tipo Incarico Post-Doc", "Tipo Borsa")
    assert it.infn_detail("1", "u", prize, TODAY) == (None, "非博士/博后岗位")
    rp = "<html><h1>Postdoc position in aging</h1><body>Application Deadline 30 Nov 2026 Funding is available.</body></html>"
    row, why = cp.ADAPTERS["pasteur"][1]("x", "u", rp, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-30" and row["level"] == "postdoc"
    far = rp.replace("30 Nov 2026", "31 Dec 2027")  # 一年多以后的占位日期不算截止
    assert cp.ADAPTERS["pasteur"][1]("x", "u", far, TODAY) == (None, "页面无截止日期")


def test_soft_dates_and_expired_body_deadline():
    hdr = "2026-11-23"
    soft = "Applicants are encouraged to apply by October 20th, 2026. Late applications may continue to be reviewed."
    assert cp.refine_deadline(hdr, "q", soft, TODAY) == (hdr, "q")
    letters = "Applications by November 1, 2026 and ensure that 3 letters of recommendation are received by November 8, 2026."
    assert cp.refine_deadline("2026-10-31", "q", "Deadline: November 1, 2026. " + letters, TODAY)[0] == "2026-11-01"
    assert cp.refine_deadline(hdr, "q", "Application Deadline: September 6, 2026", TODAY)[0] == "2026-09-06"  # 正文截止已过
    assert cp.refine_deadline(hdr, "q", "applications received before 23 February 2025 will be considered", TODAY) == (hdr, "q")  # 旧模板残留
    assert cp.refine_deadline(hdr, "q", "Applications are open at any time - there are no closing dates.", TODAY)[0] == "rolling"


def test_more_open_eligibility_phrases():
    for t in ["The program is open to U.S. and non-U.S. citizens.", "We seek exceptional graduates from around the globe.",
              "The Broad Institute will offer visa sponsorship for this opportunity.", "available to UK and International students"]:
        assert cp.cn_of(t) == "yes", t
    assert cp.cn_of("Visa sponsorship is not available for this position.") == "check"


def test_tamu_org_from_em_and_citizens_only():
    import platforms_boards as b
    page = ("<html><title>M.S. or Ph.D. Graduate Assistantship | Natural Resources Job Board</title><body>"
            "<h3>M.S. or Ph.D. Graduate Assistantship</h3> <p> <em>Texas A&amp;M - Kingsville (State)</em> | "
            '<a href="https://www.tamuk.edu/">https://www.tamuk.edu/</a> </p> <h6>Details</h6> Application Deadline: 10/31/2026 '
            "Salary: $2,000 to $2,500 per month Education Required: Bachelors Location: Kingsville, Texas Tags: Graduate "
            "Description Funded assistantship. Applicants must be U.S. citizens only.</body></html>")
    row, why = b.tamu_detail("118359", "u", page, TODAY)
    assert why == "收录" and row["org"] == "Texas A&M - Kingsville" and row["cn"] == "no"

def test_fapesp_detail():
    import platforms_br as br
    page = ('<h3 class="detalhe pt">Bolsa de PD</h3><h3 class="detalhe en">Post-Doctoral Fellowship in Genetic endocrinology</h3>'
            '<p class="linha en"><strong>Value:    </strong> R$ 12.570,00 (consulte os valores de Bolsas da FAPESP).</p>'
            '<p class="linha en instituicao"><strong>Unit/Instituition:   </strong> FMUSP/USP</p>'
            '<p class="linha pt"><strong>Data limite para inscrições: </strong> 23/10/2026</p>'
            '<p class="linha en"><strong>Deadline for submissions:    </strong> 2026-10-23</p>'
            '<p class="linha en local"><strong>Locale:      </strong>São Paulo</p>')
    row, why = br.fapesp_detail("9917", "u", page, TODAY)
    assert why == "收录" and row["level"] == "postdoc" and row["deadline"] == "2026-10-23" and row["amount"] == "R$ 12.570,00"
    assert row["org"] == "FMUSP/USP" and row["place"] == "São Paulo" and row["country"] == "BR"
    master = page.replace("Post-Doctoral Fellowship", "Master's Fellowship")
    assert br.fapesp_detail("1", "u", master, TODAY) == (None, "非博士/博后岗位")
    item = '<li class="box_col aberta x tipo_1 en">\n <a href="/oportunidades/Control/../centro-(epic)/9768/">'
    assert br.FAPESP_ITEM.findall(item) == [("1", "centro-(epic)/9768/", "9768")]


def test_linguistlist_detail():
    import platforms_boards as b
    page = ("<html><body>Subject: Psycholinguistics: PhD, University of Alberta E-mail this message to a friend "
            "Institution/Organization: University of Alberta Department: Linguistics Level: PhD Description: Accepted PhD students "
            "are provided four years of funding in the form of TA and RA stipends ($25,000 per year minimum). "
            "Application Deadline: 15-Jan-2027 Mailing Address</body></html>")
    row, why = b.ll_detail("37-3335", "u", page, TODAY)
    assert why == "收录" and row["deadline"] == "2027-01-15" and row["org"] == "University of Alberta" and row["level"] == "phd"
    assert row["amount"].startswith("stipends ($25,000")
    assert b.ll_detail("1", "u", page.replace("Application Deadline: 15-Jan-2027", ""), TODAY) == (None, "页面无截止日期")


def test_export_controlled_and_own_funding():
    assert cp.flags_of("Ability to work with export-controlled technologies is required.") == ["security-screening"]
    assert cp._any(cp.NOT_FUNDED, "Anställningen förutsätter att den sökande medför egen finansiering.")
    assert cp._any(cp.NOT_FUNDED, "Applicants must bring their own funding.")


def test_dedupe_org_spelled_differently():
    a = {"id": "arbeitsagentur:1", "title": "PhD Student: DNA break signature in cancers", "org": "Deutsches Krebsforschungszentrum",
         "deadline": "2026-10-28", "url": "u1", "via": "Bundesagentur für Arbeit", "cn": "check"}
    b = dict(a, id="naturecareers:2", org="German Cancer Research Center in the Helmholtz Association", url="u2", via="Nature Careers")
    assert cp.dedupe([a, b])[1] == 1
    c = {"id": "sciencecareers:3", "title": "Postdoctoral Research in Cancer Immunology and Immune Engineering",
         "org": "UT Southwestern Medical Center - Center for Immunology", "deadline": "2026-11-30", "url": "u3", "via": "Science Careers", "cn": "check"}
    d = dict(c, id="naturecareers:4", org="The University of Texas Southwestern Medical Center", deadline="2026-12-31", url="u4", via="Nature Careers")
    assert cp.dedupe([c, d])[1] == 1
    # 同名课题、不同机构、截止差很多：不合并
    e = {"id": "findaphd:5", "title": "Investigating pathogenic mechanisms and therapeutic targets of mtDNA mutations",
         "org": "Medical Research Council (Cambridge)", "deadline": "2026-12-08", "url": "u5", "via": "FindAPhD", "cn": "yes"}
    f = dict(e, id="jobs-ac-uk:6", org="University of Birmingham", deadline="2027-01-29", url="u6", via="jobs.ac.uk")
    assert cp.dedupe([e, f])[1] == 0


def test_hnet_listing_keeps_pages_before_429():
    import platforms_boards as b

    class Page:
        def __init__(self, text):
            self.text = text

    class F:
        def __init__(self):
            self.host_delay = {}

        def get(self, url):
            if url.endswith("page=0"):
                return Page('<a href="/jobs/70582/yale-university-postdoctoral-fellowship">x</a><a href="/jobs/70590/assistant-professor-history">y</a>')
            raise RuntimeError("429 Client Error: Too Many Requests")

    f = F()
    urls = b.hnet_urls(f, 5)
    assert urls == [("70582", "https://networks.h-net.org/jobs/70582/yale-university-postdoctoral-fellowship")]
    assert f.host_delay["networks.h-net.org"] == 20


def test_findaphd_ukri_training_is_check():
    # UKRI 博士培训项目：平台标“Students Worldwide”也只算待确认（国际生名额有上限、学费差额常需自付）
    dtp = FAP_PAGE.replace("Visit institution website", "Visit institution website This BBSRC DTP project")
    assert cp.fap_detail("8", "u", dtp, TODAY)[0]["cn"] == "check"
    uk_only = dtp.replace("Students Worldwide", "UK Students Only")
    assert cp.fap_detail("8", "u", uk_only, TODAY)[0]["cn"] == "no"  # 写明限本土的保持不变


def test_stale_postings_are_delisted():
    import build_site
    assert not build_site.stale({"checked": "2026-10-21"}, "2026-10-28")  # 7 天内
    assert build_site.stale({"checked": "2026-10-20"}, "2026-10-28")  # 超过 7 天
    assert build_site.stale({}, "2026-10-28")  # 没有核对日期也下架
