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
