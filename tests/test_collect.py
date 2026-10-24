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
