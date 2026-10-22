import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify_queue as vq  # noqa: E402


def test_dead_ids_carry_check_date(tmp_path, monkeypatch):
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "access-all.csv").write_text(
        "﻿id,名称,链接,分类,地区,逐页核对过,能否打开,详情,检查时间（UTC）\n"
        "a,A,https://a,x,UK,否,失效,HTTP 404,2026-10-20 20:01\n"
        "b,B,https://b,x,UK,否,能打开,HTTP 200,2026-10-20 20:01\n", encoding="utf-8")
    monkeypatch.setattr(vq, "ROOT", tmp_path)
    assert vq.dead_ids() == {"a": ("HTTP 404", "2026-10-20")}
