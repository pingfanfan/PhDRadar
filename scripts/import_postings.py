#!/usr/bin/env python3
"""把公开仓库 Actions 采集到的岗位并回主库（FindAPhD 等平台只有 GitHub Actions 能访问）。

    python scripts/import_postings.py                       # 默认并回 collect_postings.ACTIONS 里的全部平台
    python scripts/import_postings.py --via FindAPhD,Varbi --url <postings.yml 地址>

逐个平台：用远端该平台的全部岗位替换本地同平台岗位（远端比本地旧、或远端没有该平台岗位时不替换），
去掉已截止的，最后跨平台去重一次。
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
from collect_postings import ACTIONS, OUT, dedupe  # noqa: E402

URL = "https://raw.githubusercontent.com/pingfanfan/PhDRadar/main/_data/postings.yml"


def newest(rows: list[dict]) -> str:
    return max((str(r.get("checked") or "") for r in rows), default="")


def merge(local: list[dict], remote: list[dict], vias: list[str], today: str) -> tuple[list[dict], list[str]]:
    """返回 (合并去重后的岗位, 每个平台一行说明)。"""
    rows, notes = list(local), []
    for via in vias:
        theirs = [r for r in remote if r.get("via") == via]
        mine = [r for r in rows if r.get("via") == via]
        if not theirs or newest(theirs) < newest(mine):
            notes.append(f"{via}：远端 {len(theirs)} 条，最近采集 {newest(theirs) or '无'}，不比本地新（{newest(mine) or '无'}），不替换")
            continue
        live = [r for r in theirs if r["deadline"] == "rolling" or r["deadline"] >= today]
        rows = [r for r in rows if r.get("via") != via] + live
        notes.append(f"{via}：本地 {len(mine)} 条 → 远端 {len(live)} 条（最近采集 {newest(theirs)}）")
    rows, dropped = dedupe(rows)
    notes.append(f"去重合并 {dropped} 条，共 {len(rows)} 条")
    return sorted(rows, key=lambda r: (r["deadline"], r["id"])), notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--via", default=",".join(ACTIONS.values()), help="逗号分隔的平台名（岗位的 via 字段）")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    remote = yaml.safe_load(requests.get(args.url, timeout=60).text) or []
    local = yaml.safe_load(OUT.read_text(encoding="utf-8")) or []
    rows, notes = merge(local, remote, [v.strip() for v in args.via.split(",") if v.strip()], args.today)
    print("\n".join(notes))
    if rows != sorted(local, key=lambda r: (r["deadline"], r["id"])):
        OUT.write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
