import json
import xml.etree.ElementTree as ET

from scripts.build_feeds import write_feeds

ROWS = [
    {"id": "a", "n": "PhD in AI", "u": "https://example.org/a", "r": ["UK"], "d": ["ai"], "l": ["phd"], "c": "full",
     "e": "yes", "o": {"st": "open", "dl": "2026-10-25", "q": "Deadline 25 October 2026"}},
    {"id": "b", "n": "Postdoc <Bio>", "u": "https://example.org/b?x=1&y=2", "r": ["DE"], "l": ["postdoc"],
     "e": "check", "o": {"st": "open", "dl": "2027-01-10"}},
    {"id": "c", "n": "Closed", "u": "https://example.org/c", "e": "yes"},  # 不在“现在可申请”里
    {"id": "d", "n": "Not for CN", "u": "https://example.org/d", "e": "no", "o": {"st": "open", "dl": "2026-11-01"}},
]


def items(path):
    return ET.parse(path).getroot().findall(".//item")


def test_feeds_only_open_and_eligible(tmp_path):
    write_feeds(ROWS, tmp_path, today="2026-10-20")
    ids = [i.find("guid").text for i in items(tmp_path / "feeds" / "all.xml")]
    assert ids == ["phdradar:a", "phdradar:b"]  # 同一天出现：先截止的在前；已截止与“不可申”不收
    assert [i.find("guid").text for i in items(tmp_path / "feeds" / "cn.xml")] == ["phdradar:a"]
    assert [i.find("guid").text for i in items(tmp_path / "feeds" / "soon.xml")] == ["phdradar:a"]
    assert [i.find("guid").text for i in items(tmp_path / "feeds" / "postdoc.xml")] == ["phdradar:b"]
    assert (tmp_path / "feeds" / "index.html").exists()


def test_first_seen_is_kept(tmp_path):
    write_feeds(ROWS[:1], tmp_path, today="2026-10-20")
    write_feeds(ROWS, tmp_path, today="2026-10-21")
    seen = json.loads((tmp_path / "assets" / "first-seen.json").read_text())
    assert seen == {"a": "2026-10-20", "b": "2026-10-21"}
    first = items(tmp_path / "feeds" / "all.xml")[0]
    assert first.find("guid").text == "phdradar:b"  # 新出现的排最前
    assert "21 Oct 2026" in first.find("pubDate").text
