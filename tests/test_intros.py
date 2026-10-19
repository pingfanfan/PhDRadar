"""简介校验（apply_intros.check）的离线测试。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import apply_intros as ai  # noqa: E402

SRC = {"id": "jobs-ac-uk:X", "title": "PhD Studentship in Pure Mathematics", "org": "University of Birmingham", "level": "phd",
       "amount": "Home fees and a stipend at standard rates for 3-3.5 years", "cn": "no"}


def test_numbers_and_length():
    assert ai.check(SRC, "伯明翰大学纯数学方向博士奖学金，覆盖 Home 学费并提供标准生活费，资助 3-3.5 年。") is None
    assert ai.check(SRC, "伯明翰大学纯数学方向博士奖学金，覆盖 Home 学费并提供生活费 £21,000，资助 3-3.5 年。").startswith("数字不在原文")


def test_eligibility_must_match_data():
    assert ai.check(SRC, "伯明翰大学纯数学方向博士奖学金，面向国际学生招收，覆盖学费并提供标准生活费。").startswith("资格与数据不符")
    assert ai.check(dict(SRC, cn="check"), "伯明翰大学纯数学方向博士奖学金，仅限英国学生申请，覆盖学费并提供标准生活费。").startswith("资格与数据不符")
    assert ai.check(dict(SRC, cn="no"), "伯明翰大学纯数学方向博士奖学金，仅限英国学生申请，覆盖学费并提供标准生活费。") is None


def test_postdoc_full_scholarship_and_placeholders():
    post = dict(SRC, level="postdoc", cn="check", amount="£38,000")
    assert ai.check(post, "伯明翰大学数学系博士后岗位，全奖资助，年薪 £38,000，研究纯数学。") == "博后写成全奖"
    assert ai.check(SRC, "Quadram 研究所的 CASE 博士奖学金，与 INSERT 合作，研究海藻健康产品。") == "含禁用词"
    assert ai.check(post, "伯明翰大学数学系博士后岗位，薪资面议，研究纯数学方向的问题。") == "面议无依据"
