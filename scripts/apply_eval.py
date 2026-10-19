#!/usr/bin/env python3
"""给 /apply 的事实校验做“红队”评测：把已通过校验的文书逐句改出编造经历，看程序能拦下多少。

    python scripts/apply_eval.py applications/jobs-ac-uk-DTG436 --facts tests/fixtures/apply/lin-xiaozhou.yml

对 drafts/ 里每个带 [cv:…] 出处的句子，按下面几类各造一个变体（只改这一句，其余不动），再跑 apply_check 的校验：
  number   改数字（+1 / ×1.5）          entity  换成出处里没有的机构 / 期刊
  status   在审 → 已接收、加“第一作者”   role    参与 → 主导 / 独立完成
  award    句末加一个编造的奖项          uncited 去掉出处标记（经历句无出处）
  swap     出处换成另一条事实（语义张冠李戴；程序只在细节不符时能发现，其余交给审稿子代理）
输出每类拦截率；未拦下的变体逐条列出，供改进规则或交给审稿子代理。结果只打印，不写入申请目录。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import apply_check as ac  # noqa: E402

FAKE_ORGS = ["Imperial College London", "Tsinghua University", "Max Planck Institute for Intelligent Systems", "Nature Communications"]
FAKE_AWARDS = [" and received the Best Poster Award at the 2025 Annual Meeting", "，并获得国家优秀青年科研奖"]


def mutate_number(s: str) -> str | None:
    m = re.search(r"(?<![\w.\[:])(\d+(?:\.\d+)?)(?![\w\]])", ac.CITE.sub(lambda c: "\x00" * len(c.group(0)), s))
    if not m:
        return None
    n = m.group(1)
    new = str(int(n) + 1) if "." not in n else f"{float(n) * 1.5:.2f}"
    return s[:m.start(1)] + new + s[m.end(1):]


def mutate_entity(s: str, i: int) -> str | None:
    names = ac.proper_names(ac.CITE.sub("", s))
    if not names:
        return None
    return s.replace(names[0], FAKE_ORGS[i % len(FAKE_ORGS)], 1)


def before_cite(s: str, add: str) -> str:
    m = ac.CITE.search(s)
    return s[:m.start()].rstrip(" .。") + add + " " + s[m.start():] if m else s + add


def mutate_status(s: str) -> str:
    zh = re.search(r"[一-鿿]", s)
    return before_cite(s, "（第一作者，论文已被接收）" if zh else " (as first author, now accepted)")


def mutate_role(s: str) -> str:
    if re.search(r"\b(I|my)\b", s):
        out = re.sub(r"\bI (implemented|built|developed|ran|designed|conducted|worked on|assisted with|completed|synthesised|maintained)\b",
                     r"I independently led and \1", s, count=1)
        if out != s:
            return out
    zh = re.search(r"[一-鿿]", s)
    return before_cite(s, "，由我主导完成" if zh else ", a project I led")


def mutate_swap(s: str, ids: list[str]) -> str | None:
    m = re.search(r"\[cv:\s*([^\]]+)\]", s)
    if not m:
        return None
    cur = [x.strip() for x in m.group(1).split(",")]
    other = next((x for x in ids if x not in cur), None)
    return None if other is None else s[:m.start()] + f"[cv:{other}]" + s[m.end():]


def supported(orig: str, variant: str, own: str) -> bool:
    """变体新加的身份 / 角色说法，出处本来就支持（例如出处写了 project lead）→ 不算编造。"""
    added = [need for _, said, need in ac.CLAIMS if re.search(said, variant, re.I) and not re.search(said, orig, re.I)]
    return bool(added) and all(re.search(need, own, re.I) for need in added)


def variants(s: str, i: int, ids: list[str]) -> dict[str, str | None]:
    zh = re.search(r"[一-鿿]", s)
    return {
        "number": mutate_number(s),
        "entity": mutate_entity(s, i),
        "status": mutate_status(s),
        "role": mutate_role(s),
        "award": before_cite(s, FAKE_AWARDS[1] if zh else FAKE_AWARDS[0]),
        "uncited": ac.CITE.sub("", s) if re.search(r"\[cv:", s) else None,
        "swap": mutate_swap(s, ids),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--facts")
    args = ap.parse_args()
    d = Path(args.dir)
    facts = ac.load_yaml(ac.find_facts(args.facts)) or {}
    ids = list(ac.fact_index(facts))
    base = ac.check_dir(d, facts)
    if any(r["errors"] for r in base.values()):
        print("原稿还没通过校验，先修好再评测。")
        return 1
    lab_data = ac.load_yaml(d / "lab.yml") or {}
    lab = ac.fact_index(lab_data)
    opp = ac.load_yaml(d / "posting.yml") or {}
    post = (d / "posting.txt").read_text(encoding="utf-8") if (d / "posting.txt").exists() else None
    sup = lab_data.get("supervisor") or {}
    ctx = " ".join([ac.identity_text(facts), str(opp.get("title", "")), str(opp.get("org", "")), str(opp.get("url", "")),
                    ac.flatten(sup) if isinstance(sup, dict) else str(sup)])
    idx = ac.fact_index(facts)
    stats: dict[str, list[int]] = {}
    missed = []
    k = 0
    for f in sorted((d / "drafts").glob("*.md")):
        for ln, s in ac.split_sentences(f.read_text(encoding="utf-8")):
            if not re.search(r"\[cv:", s):
                continue
            own = " ".join(idx.get(i.strip(), "") for m in re.finditer(r"\[cv:\s*([^\]]+)\]", s) for i in m.group(1).split(","))
            for kind, v in variants(s, k, ids).items():
                if not v or v == s:
                    continue
                if kind in ("status", "role", "award") and supported(s, v, own):
                    continue  # 出处本来就支持这种说法（例如出处写了 project lead），不算编造
                k += 1
                errs, _ = ac.check_sentence(v, idx, lab, post, ctx)
                st = stats.setdefault(kind, [0, 0])
                st[1] += 1
                if errs:
                    st[0] += 1
                else:
                    missed.append((kind, f.name, ln, v))
    total = [sum(v[0] for v in stats.values()), sum(v[1] for v in stats.values())]
    print(f"# 红队评测：{d.name}\n")
    print("| 类型 | 拦下 / 变体 | 拦截率 |\n| --- | --- | --- |")
    for kind, (c, n) in stats.items():
        print(f"| {kind} | {c} / {n} | {c / n:.0%} |")
    print(f"| 合计 | {total[0]} / {total[1]} | {total[0] / max(total[1], 1):.0%} |")
    hard = [m for m in missed if m[0] != "swap"]
    if missed:
        print("\n未拦下的变体：")
        for kind, name, ln, v in missed:
            print(f"- [{kind}] {name}:{ln} {v[:200]}")
    print(f"\n编造类（除 swap 外）漏网 {len(hard)} 条。swap 是“出处张冠李戴”，细节一致时程序看不出，靠审稿子代理逐句对照。")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
