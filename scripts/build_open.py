#!/usr/bin/env python3
"""生成“现在可申请”清单 OPEN.md（数据来自 _data/open_now.yml，由 apply_open_check.py 写入）。

    python scripts/build_open.py

只列出核实员按官网正文确认“今天可以申请 / 即将开放”的条目；截止日已过的自动隐藏，
超过 14 天未复核的滚动招生条目也会隐藏，避免把过时信息当成可申请。
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import load_catalog  # noqa: E402
from build_site import LABELS  # noqa: E402

OPEN_FILE = ROOT / "_data" / "open_now.yml"
STALE_DAYS = 14
CN = {"yes": "✅ 可申", "partial": "🟡 部分可申", "check": "❔ 官网未写明", "no": "⛔ 不可申"}


def live_rows(today: str | None = None) -> list[dict]:
    """返回今天仍然有效的清单行（已过截止、滚动条目超期未复核的都剔除）。"""
    today = today or date.today().isoformat()
    stale = (date.fromisoformat(today) - timedelta(days=STALE_DAYS)).isoformat()
    if not OPEN_FILE.exists():
        return []
    rows = []
    for r in yaml.safe_load(OPEN_FILE.read_text(encoding="utf-8")) or []:
        dl = str(r.get("deadline") or "")
        if dl and dl != "rolling" and dl < today:
            continue
        if (dl == "rolling" or r["state"] == "upcoming") and str(r.get("checked")) < stale:
            continue
        rows.append(r)
    return rows


def cell(s) -> str:
    return " ".join(str(s or "").split()).replace("|", "\\|")


def main() -> int:
    today = date.today().isoformat()
    src = {s["id"]: s for s in load_catalog()["sources"]}
    rows = [r for r in live_rows(today) if r["id"] in src and src[r["id"]].get("cn_eligible") != "no"]
    region = LABELS["region"]

    def line(r: dict) -> str:
        s = src[r["id"]]
        regions = "、".join(region.get(x, x) for x in s.get("regions") or []) or "—"
        levels = "、".join(LABELS["level"].get(x, x) for x in s.get("levels") or ["phd"])
        cov = LABELS["coverage"].get(s.get("coverage") or "unknown", "官网未写明")
        when = "滚动招生" if r.get("deadline") == "rolling" else (r.get("deadline") or "—")
        if r["state"] == "upcoming":
            when = f"{r.get('opens')} 开放" + (f"，截止 {r['deadline']}" if r.get("deadline") else "")
        note = cell(r.get("note"))
        quote = cell(r.get("quote"))
        return (f"| {when} | [{cell(s['name'])}]({s['url']}) | {regions} | {levels} | {cov} | "
                f"{CN.get(s.get('cn_eligible') or 'check')} | {note}<br>官网原句：“{quote}” |")

    head = "| 截止 | 机会 | 地区 | 层次 | 资助 | 中国学生 | 说明 |\n| --- | --- | --- | --- | --- | --- | --- |"
    dated = [r for r in rows if r["state"] == "open" and r.get("deadline") != "rolling"]
    rolling = [r for r in rows if r["state"] == "open" and r.get("deadline") == "rolling"]
    upcoming = [r for r in rows if r["state"] == "upcoming"]
    dated.sort(key=lambda r: r["deadline"])
    soon = (date.fromisoformat(today) + timedelta(days=30)).isoformat()

    parts = [
        "# 现在可以申请的带奖博士 / 博后",
        "",
        f"> 生成日期：{today}。共 **{len(rows)}** 条，每一条都由核实员打开官网正文、确认“今天仍可申请”"
        f"（或即将开放），并摘录了官网原句作证据。截止日已过的会自动移出；滚动招生条目每 {STALE_DAYS} 天复核一次。",
        "> 截止时间以官网为准（注意时区），投递前请再打开官网确认。“中国学生”一列只反映官网是否写明国际生可申请。",
        "",
        f"- [30 天内截止](#30-天内截止)（{sum(1 for r in dated if r['deadline'] <= soon)}）",
        f"- [之后截止](#之后截止)（{sum(1 for r in dated if r['deadline'] > soon)}）",
        f"- [滚动招生 / 招满为止](#滚动招生--招满为止)（{len(rolling)}）",
        f"- [即将开放](#即将开放)（{len(upcoming)}）",
        "",
        "## 30 天内截止", "", head, *[line(r) for r in dated if r["deadline"] <= soon], "",
        "## 之后截止", "", head, *[line(r) for r in dated if r["deadline"] > soon], "",
        "## 滚动招生 / 招满为止", "", head, *[line(r) for r in rolling], "",
        "## 即将开放", "", head, *[line(r) for r in upcoming], "",
    ]
    (ROOT / "OPEN.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"OPEN.md：{len(rows)} 条（定期截止 {len(dated)} · 滚动 {len(rolling)} · 即将开放 {len(upcoming)}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
