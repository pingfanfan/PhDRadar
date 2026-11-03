#!/usr/bin/env python3
"""并入仓库主人本人用浏览器采集的 FindAPhD 岗位（用户 11-03 明确决定的例外，风险由用户承担）。

    python scripts/import_findaphd_refresh.py --file <postings.yml>        # 本地文件
    python scripts/import_findaphd_refresh.py --git-ref origin/findaphd-refresh-2026-11-03   # 某个分支里的 _data/postings.yml

只取 via 为 FindAPhD、带核对日期的记录，按本库岗位规则清洗后并入 _data/postings.yml：
- 竞争性资助（Competition Funded）与自费的不收；已截止、截止不是 YYYY-MM-DD / rolling 的不收；
- 国家代码 GB → UK；flags 只用于安全审查标记，原数据里的学科标签清空；
- quote 必须是截止日期原句，原数据给的是资助类型标签，清空；
- cn 一律写成字符串；UKRI 博士培训项目（DTP / CDT 等）不凭平台标签算可申，改 check；
- 只用 7 天内核对过的记录（与网站“7 天未重新核对即下架”一致），且比库里同一岗位更新（按 checked）。
自动采集仍然不绕过 FindAPhD 的拦截；这里只处理用户自己交来的数据。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import collect_postings as cp  # noqa: E402
from collect_postings import OUT, dedupe  # noqa: E402

COUNTRY = {"GB": "UK"}


def clean(rows: list[dict], today: str) -> tuple[list[dict], dict[str, int]]:
    keep, why = [], {}
    for x in rows:
        if not str(x.get("id", "")).startswith("findaphd:") or not x.get("checked"):
            continue
        ff = str(x.get("funding_for") or "")
        dl = str(x.get("deadline") or "")
        fresh_since = (date.fromisoformat(today) - timedelta(days=7)).isoformat()
        reason = ("核对日期超过 7 天" if str(x["checked"]) < fresh_since else
                  "竞争性资助或自费" if re.match(r"(?i)\s*(competition|self)", ff) else
                  "截止格式不对" if not re.fullmatch(r"\d{4}-\d{2}-\d{2}|rolling", dl) else
                  "已截止" if dl != "rolling" and dl < today else "")
        if reason:
            why[reason] = why.get(reason, 0) + 1
            continue
        y = dict(x, deadline=dl, flags=[], quote="", cn=str(x.get("cn") or "check"), checked=str(x["checked"]))
        y["country"] = COUNTRY.get(str(y.get("country") or ""), str(y.get("country") or ""))
        if y["cn"] not in ("yes", "no", "check"):
            y["cn"] = "check"
        if y["cn"] == "yes" and cp.UKRI_TRAINING.search(f"{y.get('title', '')} {ff}"):
            y["cn"] = "check"
        keep.append(y)
    return keep, why


def merge(local: list[dict], fresh: list[dict]) -> tuple[list[dict], int]:
    """同一岗位只用核对日期更新的那条；返回（合并去重后的岗位，实际新增或更新的条数）。"""
    have = {r["id"]: r for r in local}
    use = [x for x in fresh if str(have.get(x["id"], {}).get("checked") or "") < x["checked"]]
    ids = {x["id"] for x in use}
    rows, _ = dedupe([r for r in local if r["id"] not in ids] + use)
    # 按结果算：与别的平台上同一岗位合并掉的不算新增
    changed = sum(1 for r in rows if have.get(r["id"]) != r)
    return sorted(rows, key=lambda r: (str(r["deadline"]), r["id"])), changed


def main() -> int:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file")
    src.add_argument("--git-ref", help="读取该 git 引用里的 _data/postings.yml（先 git fetch）")
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    text = (Path(args.file).read_text(encoding="utf-8") if args.file else
            subprocess.run(["git", "show", f"{args.git_ref}:_data/postings.yml"], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout)
    fresh, why = clean(yaml.safe_load(text) or [], args.today)
    local = yaml.safe_load(OUT.read_text(encoding="utf-8")) or []
    rows, n = merge(local, fresh)
    print(f"可用 {len(fresh)} 条（不收：{why or '无'}）；新增或更新 {n} 条；岗位清单共 {len(rows)} 条")
    if n:
        OUT.write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
