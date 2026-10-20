#!/usr/bin/env python3
"""校验子代理写的申请者简介并写入 _data/intros.yml。

    python scripts/apply_intros.py --bundles '/tmp/intro/bundle-*.yml' --outs '/tmp/intro/out-*.yml'

校验规则（不通过的简介丢弃，网页上就不显示简介）：
- 简介里的每个数字都必须出现在该条的输入字段里（不允许编金额、年份、名额）；
- 长度 20–140 字；不得含维护过程用语或“官网未写明”之类的空话；
- 与该条的结构化字段一致（2026-10 抽检后加）：说“国际生 / 不限国籍可申”的，cn 必须是 yes；说“仅限本土”的，cn 必须是 no；
  博后不能写“全奖”；不能照抄平台模板占位符（INSERT）；“面议”要有原文依据。

    python scripts/apply_intros.py --recheck          # 用现有岗位数据重查全部岗位简介，删掉不再通过的
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
BANNED = re.compile(r"核实|条目|信源|核对|未写明|待确认|未确认|不详|绝佳|不容错过|推测|INSERT|据此推断|可推断|推断出|推断为|由此推断|请看岗位|请查看岗位|详见岗位|请参阅岗位|以岗位页面为准")  # “因果推断”“基于模拟的推断”是研究方向，不禁
OPEN_CLAIM = re.compile(r"面向(国际|海外|全球|各国)|(国际|海外|外国|非本土|全球)(学生|申请人|申请者|候选人)?[^，。；]{0,6}(均可|都可|可以|可)?(申请|报名)|不限国籍|任何国籍|各国(学生|申请人)")
RESTRICT_CLAIM = re.compile(r"仅限|只限|只招(收)?(英国|本国|本地|欧盟|美国)|限(英国|本国|本地|欧盟|美国)|(英国|本国|本地|欧盟|美国)(学生|公民)(才|方)可")


def numbers(text: str) -> set[str]:
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def check(src: dict, intro: str) -> str | None:
    if not isinstance(intro, str) or not 20 <= len(intro) <= 140:
        return "长度不符"
    if BANNED.search(intro):
        return "含禁用词"
    cn = str(src.get("cn") or src.get("cn_eligible") or "")
    if cn and OPEN_CLAIM.search(intro) and cn != "yes":
        return "资格与数据不符：简介说国际生可申"
    if cn and RESTRICT_CLAIM.search(intro) and cn != "no":
        return "资格与数据不符：简介说限本土"
    if src.get("level") == "postdoc" and re.search(r"全奖|全额奖学金", intro):
        return "博后写成全奖"
    if "面议" in intro and not re.search(r"negotiable|competitive|面议|commensurate", " ".join(str(v) for v in src.values()), re.I):
        return "面议无依据"
    allowed = numbers(" ".join(str(v) for v in src.values()))
    extra = {n for n in numbers(intro) if n not in allowed and not any(n in a for a in allowed)}
    return f"数字不在原文：{sorted(extra)}" if extra else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundles")
    ap.add_argument("--outs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--recheck", action="store_true", help="用 _data/postings.yml 重查已有的岗位简介，删掉不通过的")
    args = ap.parse_args()
    if args.recheck:
        return recheck(args.dry_run)
    if not (args.bundles and args.outs):
        ap.error("需要 --bundles 和 --outs（或 --recheck）")
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


POSTING_FIELDS = ("title", "org", "country", "place", "level", "funding_for", "amount", "requirements", "cn")


def posting_input(p: dict) -> dict:
    """岗位简介的输入字段（写简介时给子代理的和重查时用的是同一份）。"""
    return {"id": p["id"], **{k: p[k] for k in POSTING_FIELDS if p.get(k)}}


def recheck(dry_run: bool) -> int:
    postings = {p["id"]: p for p in yaml.safe_load((ROOT / "_data" / "postings.yml").read_text(encoding="utf-8")) or []}
    intros = yaml.safe_load(OUT.read_text(encoding="utf-8")) or {}
    stats: dict[str, int] = {}
    for sid in [k for k in intros if k in postings]:
        why = check(posting_input(postings[sid]), intros[sid])
        if why:
            stats[why.split("：")[0]] = stats.get(why.split("：")[0], 0) + 1
            print(f"  ✗ {sid}: {why} | {intros[sid]}")
            del intros[sid]
    print(stats, f"→ 剩 {len(intros)} 条简介")
    if not dry_run:
        OUT.write_text(yaml.safe_dump(dict(sorted(intros.items())), allow_unicode=True, width=200), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
