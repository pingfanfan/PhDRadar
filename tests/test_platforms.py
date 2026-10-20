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
