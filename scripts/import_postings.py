#!/usr/bin/env python3
"""把公开仓库 Actions 采集到的某个平台的岗位并回主库（FindAPhD 只能在 GitHub Actions 上采集）。

    python scripts/import_postings.py                 # 默认取 PhDRadar 的 FindAPhD 岗位
    python scripts/import_postings.py --via FindAPhD --url <postings.yml 地址>

用远端该平台的全部岗位替换本地同平台岗位（远端比本地旧时不替换），去掉已截止的，再跨平台去重。
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from collect_postings import OUT, dedupe  # noqa: E402

URL = "https://raw.githubusercontent.com/pingfanfan/PhDRadar/main/_data/postings.yml"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--via", default="FindAPhD")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    remote = [r for r in yaml.safe_load(requests.get(args.url, timeout=60).text) or [] if r.get("via") == args.via]
    local = yaml.safe_load(OUT.read_text(encoding="utf-8")) or []
    mine = [r for r in local if r.get("via") == args.via]
    newest = lambda rows: max((str(r.get("checked") or "") for r in rows), default="")  # noqa: E731
    if not remote or newest(remote) < newest(mine):
        print(f"远端 {args.via} 岗位 {len(remote)} 条，最近采集 {newest(remote) or '无'}，不比本地新（{newest(mine) or '无'}），不替换")
        return 0
    live = [r for r in remote if r["deadline"] == "rolling" or r["deadline"] >= args.today]
    rows, dropped = dedupe([r for r in local if r.get("via") != args.via] + live)
    OUT.write_text(yaml.safe_dump(sorted(rows, key=lambda r: (r["deadline"], r["id"])), allow_unicode=True, sort_keys=False,
                                  width=200), encoding="utf-8")
    print(f"{args.via}：本地 {len(mine)} 条 → 远端 {len(live)} 条（最近采集 {newest(remote)}）；去重合并 {dropped} 条，共 {len(rows)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
