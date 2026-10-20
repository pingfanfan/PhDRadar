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
    try:
        ats.pu_detail("x", "u", waf, TODAY)
        raise AssertionError("WAF 验证页应当让适配器停下")
    except RuntimeError:
        pass


class _Page:
    def __init__(self, text):
        self.text = text


class _Fetch:
    def __init__(self, text):
        self.page = _Page(text)

    def get(self, url):
        return self.page


def test_reachmee():
    listing = """<tr><td>20260357</td><td><a href='https://web103.reachmee.com/ext/I003/304/job?site=5&lang=UK&validator=x&job_id=15133'
class='btn btn-link'>Doctoral student in Material Science</a></td><td><span class='show-mobile'>Application deadline:</span>
<span data-order="1" style="display:none">2026-11-20</span> 20/11/2026</td></tr><tr><td>20260495</td>
<td><a href='https://web103.reachmee.com/ext/I003/304/job?site=5&lang=UK&validator=x&job_id=15131' class='btn btn-link'>
Avdelningsadministratör</a></td></tr>"""
    saved = ats.REACHMEE[:]
    ats.REACHMEE[:] = [("Chalmers University of Technology", "https://web103.reachmee.com/ext/I003/304", "site=5", "SE")]
    try:
        out = ats.rm_urls(_Fetch(listing), 1)
    finally:
        ats.REACHMEE[:] = saved
    assert [jid for jid, _ in out] == ["I003-304-15133"]
    page = """<h1>Doctoral student in Material Science</h1><p>A starting salary of 35,725 SEK per month.</p>
<p>We welcome your application no later than November 20 For questions, please contact</p>"""
    row, why = ats.rm_detail("I003-304-15133", out[0][1], page, TODAY)
    # 原句没写年份：与列表上的结构化截止日期一致才借用年份
    assert why == "收录" and row["deadline"] == "2026-11-20" and row["quote"] == "application no later than November 20"
    assert row["org"] == "Chalmers University of Technology" and row["country"] == "SE" and row["level"] == "phd"


def test_university_list_page():
    listing = """<a href="/all-vacancies/?show=170609">PhD fellowship in Plant Nutrition</a>
<a href="/all-vacancies/?show=170610">Head of Section, Finance</a>"""
    out = ats.ls_urls(_Fetch(listing), 1)
    assert out == [("ku-170609", "https://employment.ku.dk/all-vacancies/?show=170609")]
    page = """<h1>PhD fellowship in Plant Nutrition</h1><p>The salary is in accordance with the collective agreement.</p>
<p>Application deadline: The deadline for applications is 23 October 2026, 23:59 CET.</p>"""
    row, why = ats.ls_detail("ku-170609", out[0][1], page, TODAY)
    assert why == "收录" and row["deadline"] == "2026-10-23" and row["via"] == "University of Copenhagen"


def test_deadline_long_apply_sentence_and_spaced_ordinal():
    text = ("You can apply for this vacancy through the University of Antwerp’s online job application platform until "
            "November 12 th 2026 . Click on the 'Apply' button")
    assert ats.deadline(text)[0] == "2026-11-12"


def test_german_wimi_level():
    phd = "<h1>Wissenschaftliche/r Mitarbeiter/in (w/m/d)</h1><p>Die Möglichkeit zur Promotion ist gegeben. Vergütung nach " \
          "TV-L E 13.</p><p>Bewerbungsfrist: 03.11.2026</p>"
    ats._LS["rwth-V000011469"] = ("RWTH Aachen University", "DE", r"<h1[^>]*>(.*?)</h1>")
    row, why = ats.ls_detail("rwth-V000011469", "u", phd, TODAY)
    assert why == "收录" and row["level"] == "phd" and row["deadline"] == "2026-11-03"
    postdoc = phd.replace("Die Möglichkeit zur Promotion ist gegeben.", "Voraussetzung ist eine abgeschlossene Promotion.") \
        .replace("03.11.2026", "04.11.2026")
    ats._LS["rwth-V2"] = ats._LS["rwth-V000011469"]
    assert ats.ls_detail("rwth-V2", "u", postdoc, TODAY)[0]["level"] == "postdoc"


def test_hash_sitemap_reads_every_link():
    xml = "<urlset><url><loc>https://job-portal.lmu.de/jobposting/dc5b4c16a1</loc></url></urlset>"
    saved = ats.LISTS[:]
    ats.LISTS[:] = [("LMU Munich", "https://job-portal.lmu.de/sitemap.xml.gz",
                     r"(?#全部)<loc>https://job-portal\.lmu\.de(/jobposting/([0-9a-f]+))</loc>", "https://job-portal.lmu.de", "DE")]
    try:
        out = ats.ls_urls(_Fetch(xml), 1)
    finally:
        ats.LISTS[:] = saved
    assert out == [("lmu-dc5b4c16a1", "https://job-portal.lmu.de/jobposting/dc5b4c16a1")]


def test_romance_language_deadlines():
    assert ats.deadline("scadenza: 30 ottobre 2026, 12:00")[0] == "2026-10-30"
    assert ats.deadline("Publié le 16 oct. 2026 - Ouvert jusqu'au 13 nov. 2026")[0] == "2026-11-13"
    # 学校自己的页面（非美加）默认 日/月/年；没有提示时日月可互换就不收
    assert ats.deadline("Date limite : 07/10/2026") == (None, "")
    assert ats.deadline("Date limite : 07/10/2026", order_hint="DMY")[0] == "2026-10-07"
