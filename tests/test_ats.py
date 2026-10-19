"""大学招聘系统适配器（scripts/ats.py）的离线测试：样例按各系统真实页面的结构精简而来。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ats  # noqa: E402
import collect_postings as cp  # noqa: E402

TODAY = "2026-10-19"


def test_registered_in_collect_postings():
    for name in ats.ADAPTERS:
        assert name in cp.ADAPTERS and name in cp.DEFAULT.split(",")


def test_deadline_phrasings():
    assert ats.deadline("Your complete online application must be submitted no later than 4 November 2026 (23:59).") == \
        ("2026-11-04", "application must be submitted no later than 4 November 2026")
    assert ats.deadline("The deadline for applications is 25th of October 2026 , but")[0] == "2026-10-25"
    assert ats.deadline("Open position Due Date: 21.10.2026 (23.59 Europe/Helsinki time)")[0] == "2026-10-21"
    assert ats.deadline("→ Apply before 30/10/2026 (DD/MM/YYYY) 23:59")[0] == "2026-10-30"
    assert ats.deadline("Applications Close Sunday 25 October 2026")[0] == "2026-10-25"
    # 开始日期不是截止日期
    assert ats.deadline("Deadline for the application for position starting on 1st January 2027") == (None, "")
    # 数字日期的日月顺序看同页其他日期：看不出就不收
    assert ats.deadline("Apply by 10/11/2026") == (None, "")
    assert ats.deadline("Job vacancy starting: 12/15/2026 | Application deadline: 02/01/2027")[0] == "2027-02-01"
    assert ats.deadline("Contract start 1/11/2026. Apply until 27/10/2026")[0] == "2026-10-27"
    # 只写日月：与系统里的下架日期相差 3 天内才借用其年份
    assert ats.deadline("Applications close: 1 November, 11:55 PM", end_date="2026-11-02") == \
        ("2026-11-01", "Applications close: 1 November")
    assert ats.deadline("Applications close: 1 November, 11:55 PM", end_date="2026-12-20") == (None, "")
    assert ats.deadline("Applications close: 1 November, 11:55 PM") == (None, "")
    ubc = "Posting End Date October 30, 2026 Note: Applications will be accepted until 11:59 PM on the Posting End Date."
    assert ats.deadline(ubc) == ("2026-10-30", "Posting End Date October 30, 2026")


WD_JOB = {"jobPostingInfo": {
    "title": "Doctoral Researcher in Trustworthy Machine Learning", "location": "Otaniemi", "country": {"descriptor": "Finland"},
    "endDate": "2026-11-01", "externalUrl": "https://aalto.wd3.myworkdayjobs.com/aalto/job/Otaniemi/Doctoral-Researcher_R48273",
    "jobDescription": "<p>We are looking for a doctoral researcher (PhD student).</p><p>The starting salary is 2900 € per month."
                      "</p><p>The deadline for applications is 31.10.2026 (23:59 EET).</p>"}}


def test_workday():
    url = "https://aalto.wd3.myworkdayjobs.com/aalto/job/Otaniemi/Doctoral-Researcher_R48273"
    assert ats.wd_api(url) == "https://aalto.wd3.myworkdayjobs.com/wday/cxs/aalto/aalto/job/Otaniemi/Doctoral-Researcher_R48273"
    assert ats.wd_api("https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/job/Philadelphia/Postdoc_JR1") == \
        "https://wd1.myworkdaysite.com/wday/cxs/upenn/careers-at-penn/job/Philadelphia/Postdoc_JR1"
    ats._WD_SCHOOL["aalto-R48273"] = ("Aalto University", "FI", url)
    row, why = ats.wd_detail("aalto-R48273", ats.wd_api(url), json.dumps(WD_JOB), TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-31" and row["level"] == "phd" and row["country"] == "FI"
    assert row["url"] == url and row["org"] == "Aalto University" and row["via"] == "Workday" and row["cn"] == "check"
    assert row["quote"] == "deadline for applications is 31.10.2026"
    senior = json.loads(json.dumps(WD_JOB))
    senior["jobPostingInfo"]["title"] = "Senior Research Fellow"
    assert ats.wd_detail("aalto-R1", "u", json.dumps(senior), TODAY) == (None, "非博士/博后岗位")
    nopay = json.loads(json.dumps(WD_JOB))
    nopay["jobPostingInfo"]["jobDescription"] = "<p>PhD student wanted. The deadline for applications is 31.10.2026.</p>"
    assert ats.wd_detail("aalto-R2", "u", json.dumps(nopay), TODAY) == (None, "未写资助")
    assert ats.wd_detail("aalto-R3", "u", '{"widget":"redirect"}', TODAY) == (None, "页面无岗位数据")


def test_workday_sitemap_listing():
    xml = """<urlset><url><loc>https://ntu.wd3.myworkdayjobs.com/Careers/job/Singapore/Research-Fellow--AI-_R00012345-1</loc></url>
<url><loc>https://ntu.wd3.myworkdayjobs.com/Careers/job/Singapore/Research-Fellow--AI-_R00012345-2</loc></url>
<url><loc>https://ntu.wd3.myworkdayjobs.com/Careers/job/Singapore/Finance-Manager_R00099999</loc></url></urlset>"""

    class F:
        def get(self, url):
            return type("R", (), {"text": xml})()

    saved = ats.WORKDAY[:]
    ats.WORKDAY[:] = [("Nanyang Technological University", "https://ntu.wd3.myworkdayjobs.com/Careers/siteMap.xml", "SG")]
    try:
        out = ats.wd_urls(F(), 1)
    finally:
        ats.WORKDAY[:] = saved
    assert [jid for jid, _ in out] == ["ntu-R00012345"]  # 同一职位的多个发布只读一次，非学术岗不读
    assert out[0][1].startswith("https://ntu.wd3.myworkdayjobs.com/wday/cxs/ntu/Careers/job/")


SF_PAGE = """<html><body><span itemprop="title">PhD Position Chaotic Sampling for Secure Systems</span>
<span itemprop="description" class="jobdescription"><p>Doctoral candidate in cryptography.</p>
<p>Salary range: €3204 - €4051 per month. Are you interested? Please apply no later than 23 October 2026 via the button.</p>
</span><span itemprop="jobLocation"><meta itemprop="addressLocality" content="Delft"></span>
<div class="similar">Postdoc in X. Apply no later than 1 January 2026</div></body></html>"""


def test_successfactors():
    ats._SF_SCHOOL["tudelft-1373201357"] = ("Delft University of Technology", "NL")
    row, why = ats.sf_detail("tudelft-1373201357", "https://careers.tudelft.nl/job/Delft-PhD/1373201357/", SF_PAGE, TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-23" and row["level"] == "phd" and row["place"] == "Delft"
    assert row["quote"] == "apply no later than 23 October 2026" and row["amount"].startswith("Salary range: €3204")
    # 同一岗位的另一语言版本（不同编号、同标题同截止）只收一次
    ats._SF_SCHOOL["tudelft-999"] = ("Delft University of Technology", "NL")
    assert ats.sf_detail("tudelft-999", "u", SF_PAGE, TODAY) == (None, "重复（另一语言版本）")


def test_oracle():
    ats._ORC["CX_1-efzu-8420"] = ("Technical University of Denmark (DTU)", "DK",
                                  "https://efzu.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/8420")
    detail = {"items": [{"Title": "PhD scholarship in Resilient Distribution Grids - DTU Wind",
                         "PrimaryLocation": "Kgs. Lyngby, Denmark", "ExternalPostedEndDate": "2026-11-04T22:59:00+00:00",
                         "ExternalDescriptionStr": "<p>Salary and appointment terms: the salary is based on the collective "
                                                   "agreement.</p><p>Your complete online application must be submitted no "
                                                   "later than 4 November 2026 (23:59 Danish time).</p>"}]}
    row, why = ats.orc_detail("CX_1-efzu-8420", "api", json.dumps(detail), TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-04" and row["url"].endswith("/sites/CX_1/job/8420")
    assert row["org"] == "Technical University of Denmark (DTU)" and row["via"] == "Oracle Recruiting"


def test_pageup():
    page = """<div id="job-content"><h2 itemprop="title">Post-doctoral Fellow (several posts)</h2>
<p>Applicants should have a PhD degree. A highly competitive salary commensurate with qualifications will be offered.</p>
<p>Advertised: Oct 16, 2026 (HK Time) Applications close: Nov 30, 2026 (HK Time)</p></div>
<div id="search-results">Postdoctoral Fellow Dec 31, 2025</div>"""
    ats._PU["jobs.hku.hk-537680"] = ("The University of Hong Kong", "HK")
    row, why = ats.pu_detail("jobs.hku.hk-537680", "https://jobs.hku.hk/en/job/537680/postdoctoral-fellow", page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-11-30" and row["level"] == "postdoc" and row["country"] == "HK"
    waf = '<html><script>window.awsWafCookieDomainList = [];</script></html>'
    assert ats.pu_detail("x", "u", waf, TODAY) == (None, "被拦截（WAF 验证）")
