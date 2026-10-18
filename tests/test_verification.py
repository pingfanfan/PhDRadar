"""核实写回逻辑的离线测试。"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from apply_verification import apply_main  # noqa: E402

MAIN = """categories:
  - id: dup
    title: 分类
sources:
  - id: a
    name: A
    url: https://a.example/
    cn_eligible: 'check'
    verified: 2026-10
  - id: dup
    name: D
    url: https://d.example/
"""


def test_update_only_touches_sources_section():
    text, found = apply_main(MAIN, "dup", "update", {"cn_eligible": "yes"}, "2026-10-12")
    assert found
    data = yaml.safe_load(text)
    assert data["categories"][0] == {"id": "dup", "title": "分类"}
    assert data["sources"][1]["cn_eligible"] == "yes"
    assert str(data["sources"][1]["verified"]) == "2026-10-12"


def test_update_replaces_fields_and_quotes():
    text, _ = apply_main(MAIN, "a", "update", {"cn_eligible": "no", "levels": ["phd", "postdoc"]}, "2026-10-12")
    src = yaml.safe_load(text)["sources"][0]
    assert src["cn_eligible"] == "no" and src["levels"] == ["phd", "postdoc"]
    assert text.count("cn_eligible") == 1


def test_keep_and_delete():
    text, _ = apply_main(MAIN, "a", "keep", {}, "2026-10-12")
    assert str(yaml.safe_load(text)["sources"][0]["verified"]) == "2026-10-12"
    text, found = apply_main(MAIN, "a", "delete", {}, "2026-10-12")
    assert found and [s["id"] for s in yaml.safe_load(text)["sources"]] == ["dup"]
    assert apply_main(MAIN, "missing", "keep", {}, "2026-10-12") == (MAIN, False)


def test_update_writes_opportunity_fields():
    text, _ = apply_main(MAIN, "a", "update", {"coverage": "full", "deadline": "2026-12-01", "status": "open",
                                               "requirements": "需硕士；IELTS 6.5"}, "2026-10-13")
    src = yaml.safe_load(text)["sources"][0]
    assert src["coverage"] == "full" and str(src["deadline"]) == "2026-12-01" and src["status"] == "open"
    assert src["requirements"] == "需硕士；IELTS 6.5"


def test_keep_defaults_coverage_to_unknown_once():
    text, _ = apply_main(MAIN, "a", "keep", {}, "2026-10-13", {"coverage": "unknown"})
    assert yaml.safe_load(text)["sources"][0]["coverage"] == "unknown"
    text2, _ = apply_main(text, "a", "update", {"coverage": "full"}, "2026-10-13", {"coverage": "unknown"})
    assert yaml.safe_load(text2)["sources"][0]["coverage"] == "full"
    text3, _ = apply_main(text2, "a", "keep", {}, "2026-10-13", {"coverage": "unknown"})
    assert yaml.safe_load(text3)["sources"][0]["coverage"] == "full"  # 已有值不被默认值覆盖


def test_merge_rejects_entries_without_evidence(tmp_path, monkeypatch):
    import subprocess
    f = tmp_path / "in.yml"
    f.write_text("- {id: zz-noevidence-test, name: x, url: 'https://zz-noevidence.example/', category: aggregators, regions: [US], "
                 "disciplines: [all], funding: info, cn_eligible: 'check', access: [web], language: en, notes: n}\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "merge_sources.py"), str(f), "--dry-run"],
                         capture_output=True, text=True).stdout
    assert "无 evidence" in out
