import json

from scripts.build_api import write_api

ROWS = [
    {"id": "ajo:1", "n": "Postdoc in QIS", "org": "UNM", "u": "https://example.org/1", "r": ["US"], "l": ["postdoc"], "c": "salary",
     "e": "check", "v": True, "via": "Academic Jobs Online", "o": {"st": "open", "dl": "2026-11-01", "q": "Appl Deadline: 2026/11/01", "ck": "2026-10-19"},
     "af": {"dg": ["需博士学位", "Ph.D. required"]}, "fl": ["security-screening"]},
    {"id": "prog", "n": "某奖学金", "u": "https://example.org/p", "r": ["UK"], "l": ["phd"], "d": ["all", "bio"], "c": "full", "e": "yes",
     "v": True, "pq": "Fully funded", "vd": "2026-10-18", "o": {"st": "open", "dl": "2026-10-30"}},
    {"id": "closed", "n": "已截止", "u": "https://example.org/c", "e": "yes", "v": True, "pq": "x", "vd": "2026-10-01"},
    {"id": "unverified", "n": "未核对", "u": "https://example.org/u", "e": "check", "v": False},
    {"id": "no", "n": "不可申", "u": "https://example.org/n", "e": "no", "v": True, "o": {"st": "open", "dl": "2026-11-05"}},
]


def test_api_files(tmp_path):
    counts = write_api(ROWS, tmp_path, today="2026-10-20")
    assert counts == {"opportunities": 2, "sources": 3}
    opps = json.loads((tmp_path / "api/v1/opportunities.json").read_text())
    assert [x["id"] for x in opps["items"]] == ["prog", "ajo:1"]  # 按截止排序；已截止、不可申不收
    post = opps["items"][1]
    assert post["kind"] == "posting" and post["requirements"]["degree"]["quote"] == "Ph.D. required"
    assert post["evidence_quote"] == "Appl Deadline: 2026/11/01" and post["flags"] == ["security-screening"]
    assert opps["items"][0]["disciplines"] == ["bio"] and opps["items"][0]["evidence_quote"] == "Fully funded"
    srcs = json.loads((tmp_path / "api/v1/sources.json").read_text())
    assert "unverified" not in [x["id"] for x in srcs["items"]]  # 只公开核对过的
    spec = json.loads((tmp_path / "api/openapi.json").read_text())
    assert set(spec["paths"]) == {"/api/v1/index.json", "/api/v1/opportunities.json", "/api/v1/changes.json", "/api/v1/sources.json"}
    assert "opportunities.json" in (tmp_path / "llms.txt").read_text()


def test_changes_log(tmp_path):
    write_api(ROWS, tmp_path, today="2026-10-20")  # 第一次：没有上一版，不记变更
    assert json.loads((tmp_path / "api/v1/changes.json").read_text())["days"] == []
    later = [r for r in ROWS if r["id"] != "ajo:1"] + [
        {"id": "new", "n": "新岗位", "u": "https://example.org/x", "e": "yes", "v": True, "o": {"st": "open", "dl": "2026-12-01"}}]
    write_api(later, tmp_path, today="2026-10-21")
    write_api(later, tmp_path, today="2026-10-21")  # 同一天再生成一次：合并，不重复
    days = json.loads((tmp_path / "api/v1/changes.json").read_text())["days"]
    assert days == [{"date": "2026-10-21", "added": ["new"], "removed": ["ajo:1"]}]
    write_api(ROWS, tmp_path, today="2026-10-21")  # 当天又回来：既不算新增也不算下架
    days = json.loads((tmp_path / "api/v1/changes.json").read_text())["days"]
    assert days == [{"date": "2026-10-21", "added": [], "removed": []}]
