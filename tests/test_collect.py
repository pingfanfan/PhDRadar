

def test_merge_platforms_keeps_other_platforms_from_latest():
    import collect_postings as cp
    old = [{"id": "findaphd:1", "v": "old"}, {"id": "findaphd:2", "v": "old"}, {"id": "jobs-ac-uk:A", "v": "latest"}]
    new = [{"id": "findaphd:1", "v": "new"}, {"id": "findaphd:3", "v": "new"}, {"id": "jobs-ac-uk:A", "v": "stale"}]
    rows = cp.merge_platforms(old, new, {"findaphd"})
    assert {k: r["v"] for k, r in rows.items()} == {"findaphd:1": "new", "findaphd:3": "new", "jobs-ac-uk:A": "latest"}
