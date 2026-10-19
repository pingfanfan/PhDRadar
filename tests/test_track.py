"""申请追踪看板（scripts/track.py）的离线测试。"""
import json
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import track  # noqa: E402

TODAY = date(2026, 10, 19)
POSTINGS = [
    {"id": "findaphd:195793", "title": "ML for Climate PhD", "org": "University of X",
     "url": "https://www.findaphd.com/phds/project/x/?p195793", "deadline": "2026-11-02",
     "quote": "2 November 2026 23:59 GMT", "country": "GB", "checked": "2026-10-18"},
    {"id": "jobsac:1", "title": "Old", "org": "Y", "url": "https://jobs.ac.uk/1", "deadline": "2026-10-01", "checked": "2026-10-18"},
    {"id": "jobsac:2", "title": "Fresh", "org": "Z", "url": "https://jobs.ac.uk/2", "deadline": "rolling", "checked": "2026-10-15"},
    {"id": "jobsac:3", "title": "Stale", "org": "Z", "url": "https://jobs.ac.uk/3", "deadline": "2026-12-01", "checked": "2026-09-01"},
]
SOURCES = [{"id": "csc-programme", "name": "国家留学基金委项目", "url": "https://www.csc.edu.cn/", "deadline": "rolling"}]


def run(tmp_path, *args, today="2026-10-19"):
    return track.main(["--file", str(tmp_path / "tracker.yml"), "--today", today, *args])


@pytest.fixture
def fake_data(monkeypatch):
    monkeypatch.setattr(track, "load_postings", lambda: POSTINGS)
    monkeypatch.setattr(track, "load_sources", lambda: SOURCES)


def entry(**kw):
    base = {"id": "x:1", "title": "T", "org": "O", "url": "https://e.org/1", "deadline": "unknown", "stage": "want",
            "result": "", "contacts": [], "notes": "", "history": [], "added": "2026-10-01"}
    return track.normalize({**base, **kw})


def test_add_from_postings_and_no_duplicates():
    entries = []
    e, new = track.cmd_add(entries, "findaphd:195793", TODAY, postings=POSTINGS, sources=[])
    assert new and e["title"] == "ML for Climate PhD" and e["deadline"] == "2026-11-02"
    assert e["deadline_note"] == "2 November 2026 23:59 GMT"
    assert e["history"] == [{"date": "2026-10-19", "stage": "want"}] and e["added"] == "2026-10-19"
    _, new2 = track.cmd_add(entries, "findaphd:195793", TODAY, postings=POSTINGS, sources=[])
    _, new3 = track.cmd_add(entries, POSTINGS[0]["url"], TODAY, postings=POSTINGS, sources=[])
    assert not new2 and not new3 and len(entries) == 1


def test_add_from_catalog_and_custom():
    entries = []
    e, _ = track.cmd_add(entries, "csc-programme", TODAY, postings=[], sources=SOURCES)
    assert e["title"] == "国家留学基金委项目" and e["deadline"] == "rolling"
    with pytest.raises(SystemExit):
        track.cmd_add(entries, "https://lab.example.edu/join", TODAY, postings=[], sources=[])
    e2, new = track.cmd_add(entries, "https://lab.example.edu/join", TODAY, title="Lab PhD",
                            deadline="2026-12-01", postings=[], sources=[])
    assert new and e2["id"].startswith("custom:") and e2["url"] == "https://lab.example.edu/join"
    assert len(entries) == 2


def test_cli_add_writes_ordered_yaml(tmp_path, fake_data):
    assert run(tmp_path, "add", "findaphd:195793") == 0
    assert run(tmp_path, "add", "findaphd:195793") == 0
    data = yaml.safe_load((tmp_path / "tracker.yml").read_text(encoding="utf-8"))
    assert len(data) == 1
    assert list(data[0])[:5] == ["id", "title", "org", "url", "deadline"]


def test_stage_chinese_alias_and_history(tmp_path, fake_data):
    run(tmp_path, "add", "findaphd:195793")
    run(tmp_path, "stage", "findaphd:195793", "准备中")
    run(tmp_path, "stage", "findaphd:195793", "结果", "--result", "offer", "--date", "2026-12-01")
    e = yaml.safe_load((tmp_path / "tracker.yml").read_text(encoding="utf-8"))[0]
    assert e["stage"] == "result" and e["result"] == "offer"
    assert [h["stage"] for h in e["history"]] == ["want", "prep", "result"]
    assert e["history"][-1] == {"date": "2026-12-01", "stage": "result", "result": "offer"}
    with pytest.raises(SystemExit):
        track.cmd_stage(e, "随便", TODAY)


def test_contact_and_reply(tmp_path, fake_data):
    run(tmp_path, "add", "findaphd:195793")
    run(tmp_path, "contact", "findaphd:195793", "--to", "Prof. X", "--date", "2026-10-01")
    assert any("套磁跟进" in x for x in track.remind(track.load_tracker(tmp_path / "tracker.yml"), TODAY))
    run(tmp_path, "reply", "findaphd:195793", "--to", "Prof. X")
    e = track.load_tracker(tmp_path / "tracker.yml")[0]
    assert e["contacts"][0]["replied"] is True
    assert not any("套磁跟进" in x for x in track.remind([e], TODAY))


@pytest.mark.parametrize("days,expect", [(14, "还有 14 天"), (7, "还有 7 天"), (1, "明天截止"), (0, "今天截止"),
                                         (-3, "已过期"), (13, None), (8, None), (2, None)])
def test_remind_deadlines(days, expect):
    d = date.fromordinal(TODAY.toordinal() + days).isoformat()
    out = track.remind([entry(deadline=d, stage="prep")], TODAY)
    if expect is None:
        assert out == []
    else:
        assert len(out) == 1 and expect in out[0]


def test_remind_skips_sent_and_rolling():
    d = date.fromordinal(TODAY.toordinal() + 7).isoformat()
    assert track.remind([entry(deadline=d, stage="sent"), entry(deadline=d, stage="interview"),
                         entry(deadline="rolling")], TODAY) == []


def test_remind_contacts_ten_days_and_interview():
    c = lambda d, r=False: {"to": "Prof. Y", "date": d, "replied": r, "note": ""}  # noqa: E731
    assert len(track.remind([entry(contacts=[c("2026-10-09")])], TODAY)) == 1  # 恰好 10 天
    assert track.remind([entry(contacts=[c("2026-10-10")])], TODAY) == []  # 9 天
    assert track.remind([entry(contacts=[c("2026-10-01", True)])], TODAY) == []
    assert track.remind([entry(stage="interview", contacts=[c("2026-10-01")])], TODAY) == []
    out = track.remind([entry(stage="interview", interview="2026-10-22")], TODAY)
    assert len(out) == 1 and "面试准备" in out[0]
    assert track.remind([entry(stage="interview", interview="2026-10-23")], TODAY) == []


def test_ics_content(tmp_path):
    entries = [
        entry(id="a:1", title="Deep, learning; PhD\\2", deadline="2026-11-30", deadline_note="23:59 GMT\nUK time"),
        entry(id="a:2", deadline="2026-10-01"),  # 已过
        entry(id="a:3", deadline="rolling"),
        entry(id="a:4", deadline="2026-12-01", stage="result", result="reject"),
        entry(id="a:5", deadline="2026-11-15", stage="interview", interview="2026-10-25"),
    ]
    text = track.ics(entries, TODAY)
    assert text.count("BEGIN:VEVENT") == 3  # a:1、a:5 截止、a:5 面试
    assert "UID:a:1@phdradar" in text and "UID:a:5-interview@phdradar" in text
    assert "DTSTART;VALUE=DATE:20261130" in text and "DTEND;VALUE=DATE:20261201" in text
    for n in (14, 7, 1):
        assert f"TRIGGER:-P{n}D" in text
    assert "\r\n" in text and "\n" not in text.replace("\r\n", "")
    unfolded = text.replace("\r\n ", "")
    assert "Deep\\, learning\\; PhD\\\\2" in unfolded
    assert "23:59 GMT\\nUK time" in unfolded
    assert "URL:https://e.org/1" in unfolded
    assert all(len(ln.encode()) <= 75 for ln in text.split("\r\n"))
    run(tmp_path, "ics")  # 空看板也能导出
    assert (tmp_path / "deadlines.ics").read_bytes().startswith(b"BEGIN:VCALENDAR\r\n")


def test_weekly_sections(tmp_path):
    rk = tmp_path / "rankings"
    rk.mkdir()
    (rk / "2026-10-18.md").write_text("# 排序\n" + "\n".join(f"{i}. [P{i}](https://e.org/{i})" for i in range(1, 15)),
                                      encoding="utf-8")
    entries = [entry(id="findaphd:195793", url=POSTINGS[0]["url"], deadline="2026-11-02", stage="prep",
                     contacts=[{"to": "Prof. Z", "date": "2026-10-01", "replied": False, "note": ""}]),
               entry(id="b:1", deadline="2026-12-31", stage="sent")]
    text = track.weekly(entries, TODAY, postings=POSTINGS, ranking_dirs=[rk])
    for head in ("一、新匹配机会", "二、未来 14 天截止", "三、待跟进套磁", "四、各阶段计数"):
        assert head in text
    assert "[P10](https://e.org/10)" in text and "[P11]" not in text
    assert "不在看板里的岗位：1 条" in text  # 只有 jobsac:2
    assert "还剩 14 天" in text and "Prof. Z" in text
    assert "- 准备中：1" in text and "- 已投：1" in text
    assert "先运行 /rank" in track.weekly([], TODAY, postings=[], ranking_dirs=[tmp_path / "none"])


def test_import_site(tmp_path, fake_data):
    run(tmp_path, "add", "csc-programme")
    data = {"saved": {"findaphd:195793": 1, "csc-programme": 1, "mystery:9": 1},
            "status": {"findaphd:195793": {"s": "sent", "t": "2026-10-10"},
                       "csc-programme": {"s": "result", "r": "withdraw", "t": "2026-10-12"}}}
    p = tmp_path / "saved.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    run(tmp_path, "import-site", str(p))
    entries = track.load_tracker(tmp_path / "tracker.yml")
    by = {e["id"]: e for e in entries}
    assert len(entries) == 3
    assert by["findaphd:195793"]["title"] == "ML for Climate PhD" and by["findaphd:195793"]["stage"] == "sent"
    assert by["findaphd:195793"]["history"][-1] == {"date": "2026-10-10", "stage": "sent"}
    assert by["csc-programme"]["stage"] == "result" and by["csc-programme"]["result"] == "withdraw"
    assert by["mystery:9"]["stage"] == "want"
    run(tmp_path, "import-site", str(p))  # 再导一次不重复、不重复记 history
    entries2 = track.load_tracker(tmp_path / "tracker.yml")
    assert len(entries2) == 3 and entries2 == entries


def test_board_columns():
    text = track.board([entry(deadline="2026-10-26"), entry(id="r", stage="result", result="offer")], TODAY)
    for col in ("## 想投（1）", "## 准备中（0）", "## 已投（0）", "## 面试（0）", "## 结果（1）"):
        assert col in text
    assert "还剩 7 天" in text and "录取" in text and "待办：" in text


def test_new_matches_uses_profile_and_skips_known(tmp_path):
    """每周摘要的新匹配：按画像排序（rank.py），跳过看板里已有的和以前列过的。"""
    row = lambda i, n: {"id": i, "n": n, "u": f"https://ex.org/{i}", "l": ["phd"], "r": ["UK"], "c": "full",  # noqa: E731
                        "dl": "2026-12-01", "e": "yes", "v": True, "d": ["ai"],
                        "o": {"st": "open", "dl": "2026-12-01", "q": "Closes 1 Dec 2026", "ck": "2026-10-19"}}
    rows = [row("a", "Deep learning for MRI reconstruction"), row("b", "Machine learning for medical imaging"),
            row("c", "Deep learning for crop yield"), {**row("d", "Medieval history of trade"), "d": ["humanities"]}]
    profile = {"research": {"keywords": ["deep learning", "machine learning"]}, "target": {"levels": ["phd"]}}
    entries = [{"id": "a", "url": "https://ex.org/a", "stage": "want"}]
    got = track.new_matches(entries, date(2026, 10, 19), profile, rows, seen={"c"})
    assert [m["id"] for m in got] == ["b"]
    text = track.weekly(entries, date(2026, 10, 19), postings=[], ranking_dirs=[], matches=got)
    assert "Machine learning for medical imaging" in text and "按你的画像" in text
