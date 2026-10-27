import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))


def test_merge_platforms_keeps_other_platforms_from_latest():
    import collect_postings as cp
    old = [{"id": "findaphd:1", "v": "old"}, {"id": "findaphd:2", "v": "old"}, {"id": "jobs-ac-uk:A", "v": "latest"}]
    new = [{"id": "findaphd:1", "v": "new"}, {"id": "findaphd:3", "v": "new"}, {"id": "jobs-ac-uk:A", "v": "stale"}]
    rows = cp.merge_platforms(old, new, {"findaphd"})
    assert {k: r["v"] for k, r in rows.items()} == {"findaphd:1": "new", "findaphd:3": "new", "jobs-ac-uk:A": "latest"}


def test_make_public_keeps_newer_actions_rows():
    import make_public as mp
    mine = [{"id": "findaphd:1", "checked": "2026-10-21", "deadline": "2026-11-01"},
            {"id": "jobs-ac-uk:A", "checked": "2026-10-24", "deadline": "2026-11-01"}]
    public = [{"id": "findaphd:2", "checked": "2026-10-24", "deadline": "2026-11-02"},
              {"id": "jobs-ac-uk:B", "checked": "2026-10-20", "deadline": "2026-11-01"}]
    out = mp.newer_platform_rows(mine, public, {"findaphd"})
    assert [r["id"] for r in out] == ["jobs-ac-uk:A", "findaphd:2"]
    assert mp.newer_platform_rows(public, mine, {"findaphd"}) == sorted(public, key=lambda r: (r["deadline"], r["id"]))


def _run_main(monkeypatch, tmp_path, adapters, extra=()):
    import collect_postings as cp
    monkeypatch.setattr(cp, "OUT", tmp_path / "postings.yml")
    monkeypatch.setattr(cp, "ADAPTERS", adapters)
    monkeypatch.setattr(cp, "expand", lambda s: s.split(","))
    monkeypatch.setattr(cp.Fetcher, "get", lambda self, url, **kw: type("R", (), {"text": "<html>x</html>"})())
    monkeypatch.setattr(sys, "argv", ["collect_postings.py", "-s", ",".join(adapters), "--dry-run", "--today", "2026-10-27", *extra])
    return cp.main()


def test_fail_if_none_when_every_platform_is_blocked(monkeypatch, tmp_path, capsys):
    def blocked(f, pages):
        raise RuntimeError("403 Client Error: Forbidden")
    code = _run_main(monkeypatch, tmp_path, {"findaphd": (blocked, None)}, ["--fail-if-none"])
    assert code == 3 and "一条岗位都没读到" in capsys.readouterr().out


def test_fail_if_none_passes_when_something_was_read(monkeypatch, tmp_path):
    adapters = {"demo": (lambda f, pages: [("1", "https://ex.org/1")], lambda jid, url, raw, today: (None, "已截止"))}
    assert _run_main(monkeypatch, tmp_path, adapters, ["--fail-if-none"]) == 0
    def blocked(f, pages):
        raise RuntimeError("403")
    assert _run_main(monkeypatch, tmp_path, {"findaphd": (blocked, None)}) == 0  # 不加选项时照旧返回 0
