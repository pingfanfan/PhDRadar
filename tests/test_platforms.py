"""新平台适配器（scripts/platforms_*.py）的离线测试（构造的详情页样例）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import collect_postings as cp  # noqa: E402,F401

TODAY = "2026-10-18"


def test_egu_ellis_fens_uibk_detail():
    import platforms_at as at
    import platforms_boards as b
    egu = ('<div class="col-md-3 mb-2 mb-md-0 strong text-md-right">Position</div>\n<div class="col-md-9">Postdoctoral researcher in '
           'aerosols</div><div class="col-md-3 mb-2 mb-md-0 strong text-md-right">Employer</div>\n<div class="col-md-9"><p>SLU</p>'
           '<p>About us</p></div><div class="col-md-3 mb-2 mb-md-0 strong text-md-right">Location</div>\n<div class="col-md-9">Umeå, '
           'Sweden</div><div class="col-md-3 mb-2 mb-md-0 strong text-md-right">Salary</div>\n<div class="col-md-9">ca. 39 000 SEK / '
           'month</div><div class="col-md-3 mb-2 mb-md-0 strong text-md-right">Application deadline</div>\n<div class="col-md-9">16 '
           'November 2026</div>')
    row, why = b.egu_detail("8661", "u", egu, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-16" and row["org"] == "SLU" and row["country"] == "SE"
    assert b.egu_detail("1", "u", egu.replace("16 \nNovember 2026".replace("\n", ""), "Open until the position is filled")
                        .replace("16 November 2026", "Open until the position is filled"), TODAY) == (None, "页面无截止日期")
    ellis = ("<h1>PhD Position in Deep Learning at TU Darmstadt</h1><body>Apply by 22/10/26 Career Stage: PhD The position is "
             "fully funded (TV-L E13).</body>")
    row, why = b.ellis_detail("2026-10-22-phd", "u", ellis, TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-22" and row["org"] == "TU Darmstadt" and row["level"] == "phd"
    fens = ("<body>Job ID: 128531 Postdoctoral Position – Sleep Position: Post-doctoral Position Deadline: 15 January 2027 "
            "Contract Length: 2 City: Strasbourg Country: France Institution: CNRS Department: LNCA Description: Join us.</body>")
    row, why = b.fens_detail("128531", "u", fens, TODAY)
    assert why == "收录" and row["deadline"] == "2027-01-15" and row["country"] == "FR" and row["org"] == "CNRS"
    assert b.fens_detail("1", "u", fens.replace("Join us.", "There is no deadline for the application."), TODAY) == \
        (None, "页面无截止日期")
    uibk = ("<h1>Universitätsassistent:in \x96 Postdoc</h1><body>Organisationseinheit: Geographie, Standort Innsbruck "
            "mindestens brutto € 5.014 / Monat (14 mal) Wir freuen uns auf Ihre Onlinebewerbung bis 21.10.2026 unter Angabe der Chiffre"
            "</body>")
    row, why = at.uibk_detail("15963", "u", uibk, TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-21" and row["title"] == "Universitätsassistent:in – Postdoc"
    assert row["amount"] == "mindestens brutto € 5.014 / Monat (14 mal)" and row["org"] == "Universität Innsbruck – Geographie"


CRICK_TERMS = """<body>We offer successful applicants a place on the Crick PhD programme, and a PhD studentship that covers:
<li>£27,715 tax-free student stipend (living allowance) per year for four years</li>
<li>Tuition fees (including for international students) and research costs</li>
Candidates of all nationalities can apply for the Crick PhD programme and studentship.</body>"""
CRICK_POS = """<h1><span><span>Sateriale Lab | Host-pathogen interactions of the Cryptosporidium parasite</span></span></h1>
<div class="o-meta__block "><div class="o-meta__label">Application close date</div>
<div class="o-meta__value"><span class="c-date"> 03 November 2026, 12:00</span>
<span class="c-timezone o-small">GMT</span></div></div><p>A 2027 Crick PhD project with Adam Sateriale.</p>"""


def test_crick_detail():
    import platforms_uk as uk
    uk._CRICK.clear()
    uk._CRICK.update(uk.crick_terms(CRICK_TERMS))
    row, why = uk.crick_detail("x", "https://www.crick.ac.uk/careers-study/vacancies/x", CRICK_POS, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-03" and row["cn"] == "yes" and row["level"] == "phd"
    assert row["title"] == "Host-pathogen interactions of the Cryptosporidium parasite" and row["quote"] == "Application close date 03 November 2026, 12:00 GMT"
    assert "£27,715" in row["amount"] and "international students" in row["funding_for"]
    assert uk.crick_detail("x", "u", CRICK_POS, "2026-11-04") == (None, "已截止")
    # 少数课题因资助来源另有资格限制（写在课题页顶部）→ 按课题页判断
    uk_only = CRICK_POS + "<p>This position is restricted to applicants who are eligible for home fee status.</p>"
    assert uk.crick_detail("x", "u", uk_only, TODAY)[0]["cn"] == "no"
    # 招生总页没读到资助原句 → 不收
    uk._CRICK.clear()
    assert uk.crick_detail("x", "u", CRICK_POS, TODAY) == (None, "未写资助")


def test_crick_urls_reads_every_page_twice():
    # 列表排序不固定：第 1 页与第 0 页重复，不能因此提前停；第二遍能补上第一遍没轮到的课题
    import platforms_uk as uk

    class R:
        def __init__(self, text): self.text = text

    calls = {"n": 0}
    pages = {0: ["a", "b"], 1: ["a", "b"], 2: ["c"]}

    class F:
        def get(self, url):
            if "recruitment" in url:
                return R(CRICK_TERMS)
            calls["n"] += 1
            p = int(url.split("page=")[1])
            slugs = pages[p] + (["d"] if calls["n"] > 3 and p == 1 else [])  # 第二遍时第 1 页才轮到 d
            pager = "".join(f'<a href="?page={i}">' for i in range(3))
            return R(pager + "".join(f'<a href="/careers-study/vacancies/{s}">' for s in slugs))

    assert sorted(slug for slug, _ in uk.crick_urls(F(), 1)) == ["a", "b", "c", "d"]


def test_egu_urls_stops_at_missing_page():
    # 总数正好 100 条：第 1、2 页各 50 条，第 3 页 404 —— 保留前两页，不整份丢掉
    import platforms_boards as b

    class R:
        def __init__(self, text): self.text = text

    class F:
        def get(self, url):
            page = int(url.split("page=")[1])
            if page > 2:
                raise RuntimeError("404 Client Error")
            return R("".join(f'<a href="/jobs/{page * 100 + i}/phd-position-{i}/">' for i in range(50)))

    assert len(b.egu_urls(F(), 10)) == 100


LMS_PAGE = """<p>Successful applicants are awarded a PhD studentship that includes: A generous, tax-free stipend of £26,500 per year,
for four years</p><li>Full coverage of student tuition fees</li><li>Visa costs for overseas students</li>
<p>PhD positions available</p><a href="https://lms.mrc.ac.uk/wp-content/uploads/Brown-Project.docx">Engineered proteins to protect
plants and animals from parasites</a><a href="https://lms.mrc.ac.uk/wp-content/uploads/Russell-Project-1.docx">Reading tissue
history and exposures using spatial single-cell genomics</a>
<p>Our PhD programmes are open to applicants of all nationalities.</p>
<p>Application deadline: Wednesday 18 th November 2026 (9:00) Remote Panel Interviews: Wednesday 6th January 2027</p>"""


def test_lms_urls_and_detail():
    import platforms_uk as uk

    class R:
        text = LMS_PAGE

    class F:
        def get(self, url): return R()

    urls = uk.lms_urls(F(), 1)
    assert [j for j, _ in urls] == ["brown", "russell"] and urls[1][1].endswith("#russell")
    row, why = uk.lms_detail("russell", urls[1][1], LMS_PAGE, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-18" and row["cn"] == "yes"
    assert row["title"].startswith("Reading tissue history") and "£26,500" in row["amount"]
    assert row["quote"] == "Application deadline: Wednesday 18 th November 2026 (9:00)"
    assert uk.lms_detail("russell", "u", LMS_PAGE, "2026-11-19") == (None, "已截止")
    assert uk.lms_detail("nobody", "u", LMS_PAGE, TODAY)[0] is None


SOTON_LIST_PAGE = """<header><span>238 Results</span></header>
<li><a href="/study/postgraduate-research/projects/realising-upconversion" class="card-link"><h3 class="card__title"> Realising upconversion </h3>
<span class="label field-label-above">Closing date:</span> <span>2027-01-31</span>
<span class="label field-label-above">Funding:</span> <span>Fully funded (UK and international)</span></a></li>
<li><a href="/study/postgraduate-research/projects/lanthanide-complexes" class="card-link"><h3 class="card__title"> Lanthanide </h3>
<span class="label field-label-above">Closing date:</span> <span>2027-07-31</span>
<span class="label field-label-above">Funding:</span> <span>Competition funded</span></a></li>
<li><a href="/study/postgraduate-research/projects/macroevolution-of-seastars" class="card-link"><h3 class="card__title"> Seastars </h3>
<span class="label field-label-above">Closing date:</span> <span>2026-11-15</span>
<span class="label field-label-above">Funding:</span> <span>Fully funded (UK only)</span></a></li>"""


def soton_page(funding: str, closing: str, body: str = "") -> str:
    return (f"<h1>Realising upconversion luminescence in supramolecular [d-f] complexes</h1>"
            f"<div>Funding</div><div>{funding}</div><div>Type of degree</div><div>Doctor of Philosophy</div>"
            f"<div>Closing date</div><div>{closing}</div><p>{body}</p>")


def test_soton_urls_keep_only_fully_funded():
    import platforms_uk

    class F:
        def get(self, url):
            return type("R", (), {"text": SOTON_LIST_PAGE if url.endswith("page=0") else "<p>no cards</p>"})()

    urls = platforms_uk.soton_urls(F(), 30)
    assert [j for j, _ in urls] == ["realising-upconversion", "macroevolution-of-seastars"]  # 竞争性资助不读
    assert urls[0][1] == "https://www.southampton.ac.uk/study/postgraduate-research/projects/realising-upconversion"


def test_soton_detail():
    import platforms_uk

    row, why = platforms_uk.soton_detail("x", "https://u", soton_page("Fully funded (UK and international)", "31 Jan 2027"), "2026-11-04")
    assert why == "收录" and row["deadline"] == "2027-01-31" and row["cn"] == "yes"
    assert row["quote"] == "Closing date 31 Jan 2027" and row["funding_for"] == "Funding: Fully funded (UK and international)"
    assert row["amount"] == "" and row["title"].startswith("Realising upconversion") and row["via"] == "Southampton"
    row, _ = platforms_uk.soton_detail("x", "https://u", soton_page("Fully funded (UK only)", "15 November 2026"), "2026-11-04")
    assert row["cn"] == "no" and row["deadline"] == "2026-11-15"
    assert platforms_uk.soton_detail("x", "u", soton_page("Competition funded", "31 Jan 2027"), "2026-11-04")[1] == "自费或竞争性资助"
    assert platforms_uk.soton_detail("x", "u", soton_page("Fully funded (UK and international)", "31 Aug 2024"), "2026-11-04")[1] == "已截止"


COV_LIST_PAGE = """<h3><a href="https://www.coventry.ac.uk/research/research-opportunities/research-students/research-studentships/ai-twin/">AI twin</a></h3>
<a href="https://www.coventry.ac.uk/research/research-opportunities/research-students/research-studentships/non-funded-studentships/">Non-funded</a>
<a href="https://www.coventry.ac.uk/research/research-opportunities/research-students/research-studentships/?var1=1208">filter</a>
<h3><a href="/research/research-opportunities/research-students/research-studentships/battery-aging/">Battery</a></h3>"""


def cov_page(eligibility: str, deadline: str, funding: str | None) -> str:
    fund = f"<h3>Funding</h3> <p>{funding}</p>" if funding is not None else ""
    return (f"<h1>AI-Enhanced EMC Digital Twin for Automotive WBG Converters</h1>"
            f"<p><strong>Eligibility:</strong> {eligibility}</p>"
            f"<p><strong>Application deadline:</strong> <span>{deadline}</span></p>"
            f"<p><strong>Start date:</strong> <span>May 2027</span></p><h3>Introduction</h3><p>x</p>{fund}")


def test_coventry_urls_skip_non_funded_and_filters():
    import platforms_uk

    class F:
        def get(self, url):
            return type("R", (), {"text": COV_LIST_PAGE})()

    assert [j for j, _ in platforms_uk.cov_urls(F(), 1)] == ["ai-twin", "battery-aging"]


def test_coventry_detail():
    import platforms_uk

    ok = cov_page("UK/International (including EU) graduates with the required entry requirements", "15 November 2026",
                  "Tuition fees and bursary")
    row, why = platforms_uk.cov_detail("ai-twin", "https://u", ok, "2026-11-06")
    assert why == "收录" and row["deadline"] == "2026-11-15" and row["cn"] == "yes"
    assert row["quote"] == "Application deadline: 15 November 2026" and row["funding_for"] == "Funding: Tuition fees and bursary"
    assert row["amount"] == "" and row["id"] == "coventry:ai-twin" and row["via"] == "Coventry"
    row, _ = platforms_uk.cov_detail("x", "u", cov_page("UK only", "15 November 2026", "Tuition fees and stipend"), "2026-11-06")
    assert row["cn"] == "no"
    assert platforms_uk.cov_detail("x", "u", cov_page("UK/International", "15 November 2026", None), "2026-11-06")[1] == "自费或竞争性资助"
    assert platforms_uk.cov_detail("x", "u", cov_page("UK/International", "15 November 2026", "Self-funded"), "2026-11-06")[1] == "自费或竞争性资助"
    assert platforms_uk.cov_detail("x", "u", cov_page("UK/International", "1 May 2026", "Tuition fees"), "2026-11-06")[1] == "已截止"


def test_uibk_english_pages():
    # 2026-11 起门户默认返回英文页：职位名、截止与薪资写法都变了
    import platforms_at as at

    phd = ("<h1>\n\t\tUniversity Assistant (PhD position)</h1><h2>Administrative unit:</h2> Department of Ecology "
           "Extent of employment: 20 hours per week. The minimum gross salary (stipulated by collective agreement) for 20 hours per "
           "week amounts to € 1.888 per month (14 times)*. Application: We are looking forward to receiving your online application "
           "by 11.11.2026 stating the code BIO-15884")
    row, why = at.uibk_detail("15884", "u", phd, "2026-11-07")
    assert why == "收录" and row["level"] == "phd" and row["deadline"] == "2026-11-11"
    assert row["amount"] == "€ 1.888 per month (14 times)" and row["org"] == "Universität Innsbruck – Department of Ecology"
    assert row["quote"] == "application by 11.11.2026"
    lecturer = phd.replace("University Assistant (PhD position)", "Senior Lecturer (Doctorate/PhD)")
    assert at.uibk_detail("16013", "u", lecturer, "2026-11-07")[1] == "非博士/博后岗位"
    postdoc = phd.replace("(PhD position)", "(postdoc)")
    assert at.uibk_detail("15913", "u", postdoc, "2026-11-07")[0]["level"] == "postdoc"


LBORO_LIST_PAGE = "".join(
    f'<li class="list__item js-degree uk lboro studentship" data-keywords="x">'
    f'<a class="list__link" href="/study/postgraduate/research-degrees/phd-opportunities/{slug}/"><h3>PhD</h3>'
    f'<p><span class="list__text"><span class="visually-hidden">Funding status</span>\n\n        {status}\n      </span></p></a></li>'
    for slug, status in [("flow-boiling", "Funded"), ("self-paid", "Self-funded"), ("garden-ponds", "Funded")])


def lboro_page(intl: str, deadline: str, body: str) -> str:
    return (f'<span class="degree-info__heading-title">\n  Stochastic analysis of flow boiling\n</span>'
            f"<p>Qualification(s) available: PhD Entry requirements 2:1 Fees for 2027-28 (per academic year) (Funded) "
            f"UK: Fully funded International: {intl} Full-time 3 years Start date October 2027 Application deadline {deadline} "
            f"Project reference FP-HZ-2026R</p><p>{body}</p>")


def test_lboro_urls_keep_only_funded():
    import platforms_uk

    class F:
        def get(self, url):
            return type("R", (), {"text": LBORO_LIST_PAGE})()

    assert [j for j, _ in platforms_uk.lboro_urls(F(), 1)] == ["flow-boiling", "garden-ponds"]


def test_lboro_detail():
    import platforms_uk as uk

    body = "The studentship provides an enhanced tax-free stipend of £22,437 per year, for a minimum of 3 years."
    row, why = uk.lboro_detail("flow-boiling", "https://u", lboro_page("Fully funded", "10 December 2026", body), "2026-11-08")
    assert why == "收录" and row["cn"] == "yes" and row["deadline"] == "2026-12-10"
    assert row["title"] == "Stochastic analysis of flow boiling" and row["quote"] == "Application deadline 10 December 2026"
    assert row["funding_for"] == "UK: Fully funded; International: Fully funded"
    assert row["amount"] == "stipend of £22,437 per year" and row["id"] == "lboro:flow-boiling" and row["via"] == "Loughborough"
    # 国际生只给本土学费（需自付差额）或不适用 → 按规则算限本土
    assert uk.lboro_detail("x", "u", lboro_page("Part funded", "15 January 2027", body), "2026-11-08")[0]["cn"] == "no"
    assert uk.lboro_detail("x", "u", lboro_page("Not applicable", "15 January 2027", body), "2026-11-08")[0]["cn"] == "no"
    # CENTA 等培训项目的课题（课题多于名额）不逐条收
    centa = lboro_page("Fully funded", "6 January 2027", "The studentship is offered on a competitive basis. " + body)
    assert uk.lboro_detail("x", "u", centa, "2026-11-08")[1].startswith("培训项目课题")
    assert uk.lboro_detail("x", "u", lboro_page("Fully funded", "1 May 2026", body), "2026-11-08")[1] == "已截止"
    self_funded = lboro_page("Fully funded", "1 May 2027", body).replace("(Funded) ", "(Self-funded) ")
    assert uk.lboro_detail("x", "u", self_funded, "2026-11-08")[1] == "自费或竞争性资助"


HW_P = "/about/our-schools/energy-geoscience-infrastructure-and-society/study-with-us/postgraduate-research/funded-research-opportunities"
HW_LIST_PAGE = ('<table><caption>Current PhD opportunities</caption><tbody>'
                f'<tr><td>EGIS2026-KS</td><td><a class="link" href="{HW_P}/multiphase-flow">Multiphase Flow</a></td><td>17-01-27</td></tr>'
                f'<tr><td>EGIS2026DLA-NW</td><td><a class="link" href="{HW_P}/geological-ai">Geological AI</a></td><td>31-01-27</td></tr>'
                '</tbody></table>')


def hw_page(who: str, closing: str, stipend: str = "provide an annual stipend (£21,685 in 2026-27) for up to 42 months") -> str:
    return (f'<h1 class="heading">PhD Multiscale X-ray Imaging of Multiphase Flow</h1>'
            f"<p>Code EGIS2026-KS Funding {who} School Energy, Geoscience, Infrastructure and Society Location Edinburgh "
            f"Award PhD Supervisor Kamaljit Singh Start date May, January Closing date {closing} Duration 48 months</p>"
            f"<h2>Funding information</h2><p>The studentship will cover tuition fees and {stipend}.</p>")


def test_hw_urls_read_table():
    import platforms_uk

    class F:
        def get(self, url):
            return type("R", (), {"text": HW_LIST_PAGE})()

    got = platforms_uk.hw_urls(F(), 1)
    assert [j for j, _ in got] == ["multiphase-flow", "geological-ai"]
    assert got[0][1] == "https://www.hw.ac.uk" + HW_P + "/multiphase-flow"


def test_hw_detail():
    import platforms_uk as uk

    row, why = uk.hw_detail("multiphase-flow", "https://u", hw_page("Fully funded (Students worldwide)", "Sunday, 17 January 2027"), "2026-11-11")
    assert why == "收录" and row["cn"] == "yes" and row["deadline"] == "2027-01-17"
    assert row["title"] == "Multiscale X-ray Imaging of Multiphase Flow" and row["quote"] == "Closing date 17 January 2027"
    assert row["funding_for"] == "Funding: Fully funded (Students worldwide)"
    assert row["amount"] == "stipend (£21,685 in 2026-27) for up to 42 months"
    assert row["id"] == "hw:multiphase-flow" and row["via"] == "Heriot-Watt" and row["place"] == "Edinburgh"
    assert uk.hw_detail("x", "u", hw_page("Fully funded (UK students only)", "Sunday, 31 January 2027"), "2026-11-11")[0]["cn"] == "no"
    assert uk.hw_detail("x", "u", hw_page("Fully funded (UK students only)", "Friday, 30 October 2026"), "2026-11-11") == (None, "已截止")
    assert uk.hw_detail("x", "u", hw_page("Self-funded", "Sunday, 31 January 2027"), "2026-11-11") == (None, "自费或竞争性资助")
    assert uk.hw_detail("x", "u", hw_page("Fully funded (Students worldwide)", "TBC"), "2026-11-11") == (None, "页面无截止日期")
