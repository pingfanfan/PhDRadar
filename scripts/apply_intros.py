#!/usr/bin/env python3
"""校验子代理写的申请者简介并写入 _data/intros.yml。

    python scripts/apply_intros.py --bundles '/tmp/intro/bundle-*.yml' --outs '/tmp/intro/out-*.yml'

校验规则（不通过的简介丢弃，网页上就不显示简介）：
- 简介里的每个数字都必须出现在该条的输入字段里（不允许编金额、年份、名额）；
- 长度 20–140 字；不得含维护过程用语或“官网未写明”之类的空话。
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_data" / "intros.yml"
BANNED = re.compile(r"核实|条目|信源|核对|未写明|待确认|未确认|不详|绝佳|不容错过|推断|推测")


def numbers(text: str) -> set[str]:
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def check(src: dict, intro: str) -> str | None:
    if not isinstance(intro, str) or not 20 <= len(intro) <= 140:
        return "长度不符"
    if BANNED.search(intro):
        return "含禁用词"
    allowed = numbers(" ".join(str(v) for v in src.values()))
    extra = {n for n in numbers(intro) if n not in allowed and not any(n in a for a in allowed)}
    return f"数字不在原文：{sorted(extra)}" if extra else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundles", required=True)
    ap.add_argument("--outs", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    src = {}
    for f in glob.glob(args.bundles):
        for it in yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []:
            src[it["id"]] = it
    intros = yaml.safe_load(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    intros = intros or {}
    stats: dict[str, int] = {}
    for f in sorted(glob.glob(args.outs)):
        try:
            rows = yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []
        except yaml.YAMLError as e:
            print(f"{f}: YAML 解析失败 {e}")
            continue
        for r in rows:
            sid = r.get("id")
            if sid not in src:
                stats["id 不在输入"] = stats.get("id 不在输入", 0) + 1
                continue
            why = check(src[sid], r.get("intro"))
            if why:
                stats[why.split("：")[0]] = stats.get(why.split("：")[0], 0) + 1
                if args.dry_run:
                    print(f"  ✗ {sid}: {why} | {r.get('intro')}")
                continue
            intros[sid] = r["intro"].strip()
            stats["通过"] = stats.get("通过", 0) + 1
    print(stats, f"→ 共 {len(intros)} 条简介")
    if not args.dry_run:
        OUT.write_text(yaml.safe_dump(dict(sorted(intros.items())), allow_unicode=True, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
