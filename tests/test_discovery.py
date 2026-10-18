"""发现流程的离线测试。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from discovery import store as store_mod  # noqa: E402
from discovery.signals import detect, page_text  # noqa: E402
from discovery.store import Store, norm_url  # noqa: E402


@pytest.mark.parametrize("text,recruiting", [
    ("I am actively looking for PhD students to join my group in Fall 2027.", True),
    ("We're recruiting two fully funded PhD students in robotics.", True),
    ("PhD positions are available in my lab starting 2027.", True),
    ("本课题组招收2027年秋季入学的全奖博士生", True),
    ("I am not currently accepting new PhD students.", False),
    ("Our lab is funded by NSF. Prospective students should read our papers.", False),
    ("I received my PhD from MIT in 2015.", False),
])
def test_detect(text, recruiting):
    assert detect(text).recruiting is recruiting


def test_detect_years_and_snippets():
    sig = detect("Openings: I am looking for PhD students for Fall 2027 (fully funded).")
    assert "2027" in sig.years and sig.snippets and sig.score >= 4


def test_page_text_strips_scripts():
    assert page_text("<html><script>var x</script><p>Hello <b>world</b></p></html>") == "Hello world"


def test_norm_url():
    assert norm_url("https://www.Example.edu/~alice/index.html?x=1") == "example.edu/~alice"
    assert norm_url("http://example.edu/~alice/") == "example.edu/~alice"


def test_store_upsert_merges(tmp_path, monkeypatch):
    monkeypatch.setattr(store_mod, "DIR", tmp_path)
    s = Store("t")
    s.path = tmp_path / "t.json"
    s.upsert("k", {"name": "A", "score": 3, "snippets": ["x"]}, "csrankings")
    s.upsert("k", {"name": "A", "score": 5, "snippets": ["y"]}, "bluesky")
    rec = s.items["k"]
    assert rec["score"] == 5 and rec["snippets"] == ["x", "y"] and rec["channels"] == ["csrankings", "bluesky"]
    assert s.added == ["k"] and rec["status"] == "new"


def test_merge_sources_dry_run(tmp_path):
    cand = tmp_path / "c.yml"
    cand.write_text(yaml.safe_dump([
        {"id": "new-thing", "name": "New", "url": "https://new.example.org/phd", "category": "aggregators",
         "regions": ["GLOBAL"], "disciplines": ["all"], "funding": "info", "cn_eligible": "check",
         "access": ["web"], "language": "en", "notes": "测试", "evidence": "New — https://new.example.org/phd"},
        {"id": "euraxess-dup", "name": "Dup", "url": "https://euraxess.ec.europa.eu/jobs/search", "category": "aggregators",
         "regions": ["EU"], "disciplines": ["all"], "funding": "info", "cn_eligible": "yes",
         "access": ["web"], "language": "en", "notes": "重复", "evidence": "x — https://euraxess.ec.europa.eu/jobs/search"},
    ], allow_unicode=True), encoding="utf-8")
    out = subprocess.run([sys.executable, str(ROOT / "scripts/merge_sources.py"), str(cand), "--dry-run"],
                         capture_output=True, text=True, check=True).stdout
    assert "新增 1" in out and "euraxess-dup: 重复" in out


def test_faculty_watchlist_schema():
    data = yaml.safe_load((ROOT / "_data/faculty.yml").read_text(encoding="utf-8"))
    for p in data.get("faculty") or []:
        assert p.get("name") and str(p.get("homepage", "")).startswith("http")


def test_merge_to_extra_target(tmp_path, monkeypatch):
    import catalog

    extra = tmp_path / "extra"
    monkeypatch.setattr(catalog, "EXTRA_DIR", extra)
    sys.argv = ["merge_sources.py"]
    import importlib.util

    spec = importlib.util.spec_from_file_location("merge_sources", ROOT / "scripts/merge_sources.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "EXTRA_DIR", extra)
    cand = tmp_path / "c.yml"
    cand.write_text(yaml.safe_dump([{"id": "zz-new", "name": "N", "url": "https://zz.example.org/x", "category": "aggregators",
                                     "regions": ["GLOBAL"], "disciplines": ["all"], "funding": "info", "levels": ["postdoc"],
                                     "cn_eligible": "yes", "access": ["web"], "language": "en", "notes": "测试",
                                     "evidence": "N — https://zz.example.org/x"}],
                                   allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["merge_sources.py", str(cand), "--target", "worker-9"])
    mod.main()
    entries = yaml.safe_load((extra / "worker-9.yml").read_text(encoding="utf-8"))
    assert entries[0]["id"] == "zz-new" and entries[0]["cn_eligible"] == "yes" and entries[0]["levels"] == ["postdoc"]


def test_render_all_pages():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_sources

    data = {
        "categories": [{"id": "aggregators", "title": "综合聚合平台", "description": "d"}],
        "sources": [{"id": "a", "name": "A | B", "url": "https://a.example.org", "category": "aggregators",
                     "regions": ["UK", "EU"], "disciplines": ["cs"], "funding": "info", "cn_eligible": "yes",
                     "access": ["web"], "language": "en", "notes": "n", "levels": ["phd", "postdoc"]}],
    }
    pages = build_sources.render_all(data)
    keys = {str(k) for k in pages}
    assert {"SOURCES.md", "sources/category/aggregators.md", "sources/region/uk.md", "sources/region/eu.md",
            "sources/discipline/cs.md"} <= keys
    assert "A \\| B" in pages[Path("sources/category/aggregators.md")]  # 竖线已转义
    assert "博士+博后" in pages[Path("sources/region/uk.md")]
    assert "sources/category/aggregators.md" in pages[Path("SOURCES.md")]
