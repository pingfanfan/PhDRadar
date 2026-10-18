#!/usr/bin/env python3
"""校验信源数据，并生成 GitHub 上阅读用的页面。

生成内容：
    SOURCES.md                       总目录（数据概览 + 按分类/地区/学科的入口）
    sources/category/<分类>.md       每个分类一页，按地区分组
    sources/region/<地区>.md         每个国家/地区一页，按分类分组
    sources/discipline/<学科>.md     每个学科一页，按分类分组
    README.md 中 STATS 标记之间的统计区块

用法：
    python scripts/build_sources.py                  # 校验并生成全部页面
    python scripts/build_sources.py --validate-only  # 只校验数据（研究员提交前用）
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import COVERAGE, DEADLINE_WORDS, STATUS, load_catalog  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts"))
from readme_assets import render_assets  # noqa: E402
DATA = ROOT / "_data" / "sources.yml"

REQUIRED = ["id", "name", "url", "category", "regions", "disciplines", "funding", "cn_eligible", "access", "language", "notes"]
FUNDING = {"position", "scholarship", "fellowship", "mixed", "info"}
CN_ELIGIBLE = {"yes": "✅", "partial": "🟡", "check": "❔", "no": "⛔"}
ACCESS = {"web", "rss", "email", "api", "login", "app"}
FUNDING_LABEL = {
    "position": "带薪岗位",
    "scholarship": "奖学金",
    "fellowship": "Fellowship",
    "mixed": "混合",
    "info": "信息渠道",
}
LEVEL_LABEL = {("phd",): "博士", ("postdoc",): "博后", ("phd", "postdoc"): "博士+博后", ("postdoc", "phd"): "博士+博后"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PAGE_LIMIT = 400_000  # 单页上限（字节）
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load() -> dict:
    return load_catalog()


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    categories = {c["id"] for c in data["categories"]}
    ids = Counter(s.get("id") for s in data["sources"])
    urls = Counter(s.get("url") for s in data["sources"])

    for i, s in enumerate(data["sources"]):
        where = f"sources[{i}] ({s.get('id', '?')})"
        for key in REQUIRED:
            if s.get(key) in (None, "", []):
                errors.append(f"{where}: 缺少字段 {key}")
        if s.get("id") and not ID_RE.match(s["id"]):
            errors.append(f"{where}: id 需为小写 kebab-case")
        if ids[s.get("id")] > 1:
            errors.append(f"{where}: id 重复")
        if urls[s.get("url")] > 1:
            errors.append(f"{where}: url 重复 {s.get('url')}")
        if s.get("url") and not str(s["url"]).startswith("https://"):
            errors.append(f"{where}: url 需为 https")
        if s.get("category") not in categories:
            errors.append(f"{where}: 未知分类 {s.get('category')}")
        if s.get("funding") not in FUNDING:
            errors.append(f"{where}: funding 取值无效 {s.get('funding')}")
        if s.get("cn_eligible") not in CN_ELIGIBLE:
            errors.append(f"{where}: cn_eligible 取值无效 {s.get('cn_eligible')}")
        for lv in s.get("levels") or ["phd"]:
            if lv not in ("phd", "postdoc"):
                errors.append(f"{where}: levels 取值无效 {lv}")
        for key in ("regions", "disciplines", "access"):
            if not all(isinstance(v, str) for v in s.get(key) or []):
                errors.append(f"{where}: {key} 中有非字符串值（YAML 中 NO/yes 等需加引号）")
        for a in s.get("access") or []:
            if a not in ACCESS:
                errors.append(f"{where}: access 取值无效 {a}")
        if s.get("coverage") not in (None, "") and s["coverage"] not in COVERAGE:
            errors.append(f"{where}: coverage 取值无效 {s['coverage']}（{'/'.join(COVERAGE)}）")
        if s.get("status") not in (None, "") and s["status"] not in STATUS:
            errors.append(f"{where}: status 取值无效 {s['status']}（{'/'.join(STATUS)}）")
        dl = s.get("deadline")
        if dl not in (None, "") and not (DATE_RE.match(str(dl)) or dl in DEADLINE_WORDS):
            errors.append(f"{where}: deadline 需为 YYYY-MM-DD 或 {'/'.join(DEADLINE_WORDS)}，现为 {dl}")
    return errors


def cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


REGION_NAMES = {
    "GLOBAL": "全球", "EU": "欧盟/欧洲", "UK": "英国", "US": "美国", "DE": "德国", "CA": "加拿大", "FR": "法国",
    "AU": "澳大利亚", "NL": "荷兰", "JP": "日本", "HK": "中国香港", "CH": "瑞士", "IT": "意大利", "SG": "新加坡",
    "ES": "西班牙", "SE": "瑞典", "AT": "奥地利", "DK": "丹麦", "FI": "芬兰", "BE": "比利时", "IL": "以色列",
    "NO": "挪威", "KR": "韩国", "IN": "印度", "SA": "沙特", "CN": "中国内地", "IE": "爱尔兰", "NZ": "新西兰",
    "PT": "葡萄牙", "AE": "阿联酋", "TW": "中国台湾", "PL": "波兰", "LU": "卢森堡", "TR": "土耳其", "ZA": "南非",
    "MO": "中国澳门", "CZ": "捷克", "HU": "匈牙利", "BR": "巴西", "LT": "立陶宛", "EE": "爱沙尼亚", "GR": "希腊",
    "QA": "卡塔尔", "IS": "冰岛", "LV": "拉脱维亚", "SI": "斯洛文尼亚", "HR": "克罗地亚", "RO": "罗马尼亚",
    "MY": "马来西亚", "TH": "泰国", "CL": "智利", "MX": "墨西哥", "AR": "阿根廷", "RU": "俄罗斯", "SK": "斯洛伐克",
    "CY": "塞浦路斯", "MT": "马耳他", "BG": "保加利亚", "RS": "塞尔维亚", "UA": "乌克兰", "EG": "埃及",
}
DISCIPLINE_NAMES = {
    "all": "全学科", "cs": "计算机", "ai": "人工智能", "math": "数学/统计", "physics": "物理/天文", "chem": "化学/材料",
    "bio": "生物/生命科学", "eco": "生态/进化", "neuro": "神经/认知", "geo": "地球/环境/海洋", "engineering": "工程",
    "social": "社会科学/心理", "humanities": "人文/语言", "econ": "经济/金融", "business": "商科/管理", "med": "医学/公卫",
}
VERIFIED_MARK = "<br><sub>✓ 已核对官网</sub>"
LEGEND = ("图例：**✓ 已核对官网** = 已按官网页面正文逐条核对，可点开官网对照　**大陆生** ✅ 可申 · 🟡 部分可申/有名额限制 · ❔ 需逐条核实 · ⛔ 不可申（仅作提醒）　"
          "**状态** 🟢 开放申请 · 🔜 即将开放 · ⏸ 本轮已截止（等下一轮）· 🔄 随时可申 · 📋 持续更新的门户/列表　"
          "**资助** 全奖 = 学费 + 生活费；带薪岗位 = 雇员合同；半奖/仅免学费需自备部分费用")
HEADER = "<!-- 本文件由 scripts/build_sources.py 自动生成，请勿手动编辑；数据见 _data/sources.yml 与 _data/sources_extra/ -->"


def region_name(code: str) -> str:
    return f"{REGION_NAMES.get(code, code)}（{code}）" if code in REGION_NAMES else code


def funding_cell(s: dict) -> str:
    """资助力度：全奖/带薪/半奖…，下方小字写金额；还没核实到力度时显示资助类型。"""
    head = COVERAGE.get(s.get("coverage")) or f"{FUNDING_LABEL[s['funding']]}<br><sub>力度待核实</sub>"
    return head + (f"<br><sub>{cell(s['stipend'])}</sub>" if s.get("stipend") else "")


def deadline_cell(s: dict) -> str:
    dl = s.get("deadline")
    head = (DEADLINE_WORDS.get(dl) or str(dl)) if dl else "—"
    parts = [f"**{head}**" if dl and DATE_RE.match(str(dl)) else head]
    if s.get("status"):
        parts.append(f"<sub>{STATUS[s['status']]}</sub>")
    if s.get("deadline_note"):
        parts.append(f"<sub>{cell(s['deadline_note'])}</sub>")
    return "<br>".join(parts)


def table(items: list[dict]) -> list[str]:
    """阅读页面的信源表：机会（含地区·学科）| 层级 | 资助 | 截止 / 状态 | 大陆生 | 申请要求与说明。"""
    lines = ["| 机会 | 层级 | 资助 | 截止 / 状态 | 大陆生 | 申请要求与说明 |", "| --- | --- | --- | --- | :-: | --- |"]
    for s in sorted(items, key=lambda x: x["name"].lower()):
        where = f"{'·'.join(REGION_NAMES.get(r, r) for r in s['regions'])} ｜ {'·'.join(DISCIPLINE_NAMES.get(d, d) for d in s['disciplines'])}"
        req = f"**要求：** {cell(s['requirements'])}<br>" if s.get("requirements") else ""
        lines.append(
            f"| [{cell(s['name'])}]({s['url']})<br><sub>{cell(where)}</sub>{VERIFIED_MARK if s.get('verify_method') == 'page' else ''} | {LEVEL_LABEL[tuple(s.get('levels') or ['phd'])]} | "
            f"{funding_cell(s)} | {deadline_cell(s)} | {CN_ELIGIBLE[s['cn_eligible']]} | {req}{cell(s['notes'])} |"
        )
    return lines


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", text.lower()).strip("-") or "x"


def stats(data: dict) -> dict:
    S = data["sources"]
    return {
        "total": len(S),
        "categories": Counter(s["category"] for s in S),
        "regions": Counter(r for s in S for r in s["regions"]),
        "disciplines": Counter(d for s in S for d in s["disciplines"]),
        "levels": Counter("both" if len(set(s.get("levels") or ["phd"])) == 2 else (s.get("levels") or ["phd"])[0] for s in S),
        "eligible": Counter(s["cn_eligible"] for s in S),
        "verified": sum(1 for s in S if s.get("verify_method") == "page"),
    }


def render_all(data: dict) -> dict[Path, str]:
    """生成整站 Markdown：总目录 SOURCES.md + sources/ 下按分类、地区、学科的分页。"""
    st = stats(data)
    cats = {c["id"]: c for c in data["categories"]}
    cat_titles = {k: v["title"] for k, v in cats.items()}
    out: dict[Path, str] = {}

    def paged(base: Path, title: str, intro: str, groups: list[tuple[str, str, list[dict]]], jump: str) -> None:
        """把分组（锚点, 标题, 条目）排成一页或多页，每页不超过 PAGE_LIMIT 字节（GitHub 超过约 512 KB 不渲染）。"""
        total = sum(len(g[2]) for g in groups)
        blocks = []  # (锚点, 小节文本)；单个分组过大时按行切成多个小节
        for anchor, heading, items in groups:
            rows = table(items)
            head, body = rows[:2], rows[2:]
            chunk, size, part = [], 0, 1
            for row in body:
                if chunk and size + len(row.encode()) > PAGE_LIMIT - 20_000:
                    blocks.append((anchor if part == 1 else "", f"## {heading}（{len(items)}，续 {part}）" if part > 1 else f"## {heading}（{len(items)}）", head + chunk))
                    chunk, size, part = [], 0, part + 1
                chunk.append(row)
                size += len(row.encode())
            blocks.append((anchor if part == 1 else "", f"## {heading}（{len(items)}，续 {part}）" if part > 1 else f"## {heading}（{len(items)}）", head + chunk))
        pages: list[list[tuple[str, str, list[str]]]] = [[]]
        used = 0
        for b in blocks:
            size = sum(len(r.encode()) for r in b[2]) + 200
            if pages[-1] and used + size > PAGE_LIMIT - 20_000:
                pages.append([])
                used = 0
            pages[-1].append(b)
            used += size
        names = [f"{base.name}.md" if i == 0 else f"{base.name}-{i + 1}.md" for i in range(len(pages))]
        where = {a: names[i] for i, pg in enumerate(pages) for a, _, _ in pg if a}
        nav = "**按{}跳转：** ".format(jump) + " · ".join(
            f"[{heading} {len(items)}]({where.get(anchor, names[0])}#{anchor})" for anchor, heading, items in groups)
        pager_line = ("**分页：** " + " · ".join(f"[第 {i + 1} 页]({n})" for i, n in enumerate(names))) if len(names) > 1 else ""
        for i, pg in enumerate(pages):
            lines = [HEADER, "", "[← 总目录](../../SOURCES.md)", "",
                     f"# {title}（{total}）" + (f" · 第 {i + 1}/{len(pages)} 页" if len(pages) > 1 else ""), "", intro, "", LEGEND, "", nav, ""]
            if pager_line:
                lines += [pager_line, ""]
            for anchor, heading, rows in pg:
                if anchor:
                    lines += [f'<a id="{anchor}"></a>', ""]
                lines += [heading, "", *rows, ""]
            if pager_line:
                lines += [pager_line, ""]
            out[base.parent / names[i]] = "\n".join(lines) + "\n"

    # ── 分类页：按地区分组 ──
    for cid, c in cats.items():
        items = [s for s in data["sources"] if s["category"] == cid]
        if not items:
            continue
        groups: dict[str, list[dict]] = {}
        for s in items:
            groups.setdefault(s["regions"][0] if s["regions"] else "GLOBAL", []).append(s)
        order = sorted(groups, key=lambda r: (-len(groups[r]), r))
        paged(Path("sources/category") / cid, c["title"], c["description"],
              [(slug("r-" + r), region_name(r), groups[r]) for r in order], "地区")

    # ── 地区页 / 学科页：按分类分组 ──
    def grouped_page(base: Path, title: str, items: list[dict], intro: str) -> None:
        groups: dict[str, list[dict]] = {}
        for s in items:
            groups.setdefault(s["category"], []).append(s)
        paged(base, title, intro, [(cid, cat_titles[cid], groups[cid]) for cid in cats if cid in groups], "分类")

    for code, n in st["regions"].items():
        items = [s for s in data["sources"] if code in s["regions"]]
        grouped_page(Path("sources/region") / slug(code), f"{region_name(code)} 信源", items,
                     f"所有标注了地区 {code} 的信源，共 {n} 条。")
    for d, n in st["disciplines"].items():
        items = [s for s in data["sources"] if d in s["disciplines"]]
        grouped_page(
            Path("sources/discipline") / slug(d), f"{DISCIPLINE_NAMES.get(d, d)} 信源", items,
            "“全学科”信源（综合平台、政府奖学金等）对所有方向都适用，请一并查看[全学科页](all.md)。" if d != "all" else "不限学科的综合信源。")

    # ── 总目录 ──
    lv = st["levels"]
    el = st["eligible"]
    idx = [HEADER, "", "# 海外带奖博士 / 博士后信源总表", "",
           f"共收录 **{st['total']}** 个信源 · 博士 {lv['phd']} · 博后 {lv['postdoc']} · 博士+博后 {lv['both']} · "
           f"大陆学生明确可申 {el['yes']} · 部分可申 {el['partial']} · 需核实 {el['check']} · **已核对官网 {st['verified']}**", "",
           "想只看已核对官网的条目、按截止日期排序，请用[网页版查询页](https://pingfanfan.github.io/PhDRadar/)。", "",
           "按你关心的维度进入对应分页（每页都按地区或分类分组，可直接跳转）：", "",
           "## 按分类", "", "| 分类 | 数量 | 说明 |", "| --- | --: | --- |"]
    for cid, c in cats.items():
        if st["categories"][cid]:
            idx.append(f"| [{c['title']}](sources/category/{cid}.md) | {st['categories'][cid]} | {cell(c['description'])} |")
    idx += ["", "## 按国家 / 地区", "", " · ".join(
        f"[{region_name(code)}](sources/region/{slug(code)}.md) {n}" for code, n in st["regions"].most_common()), "",
        "## 按学科", "", " · ".join(
        f"[{DISCIPLINE_NAMES.get(d, d)}](sources/discipline/{slug(d)}.md) {n}" for d, n in st["disciplines"].most_common()), "",
        "## 机器可读数据", "", "- 全部信源：[`data/export/sources.csv`](data/export/sources.csv) · [`sources.json`](data/export/sources.json)",
        "- 每日新岗位：[`data/jobs.md`](data/jobs.md) · 在招导师线索：[`reports/discovery.md`](reports/discovery.md)", "", LEGEND, ""]
    out[Path("SOURCES.md")] = "\n".join(idx)
    out.update(render_assets(st))  # README 首页的 SVG 横幅与导航卡片
    return out


def readme_stats(data: dict) -> str:
    st = stats(data)
    top_regions = " · ".join(f"[{REGION_NAMES.get(c, c)}](sources/region/{slug(c)}.md) {n}" for c, n in st["regions"].most_common(12))
    top_disc = " · ".join(f"[{DISCIPLINE_NAMES.get(d, d)}](sources/discipline/{slug(d)}.md) {n}" for d, n in st["disciplines"].most_common())
    return "\n".join([
        f"**热门地区：** {top_regions} · [全部 →](SOURCES.md#按国家--地区)",
        "",
        f"**学科：** {top_disc}",
    ])


def write_outputs(data: dict) -> list[Path]:
    """写入整站页面、README 统计区块，返回写入的文件列表。"""
    pages = render_all(data)
    old = set((ROOT / "sources").rglob("*.md")) if (ROOT / "sources").exists() else set()
    written = []
    for rel, content in pages.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            written.append(rel)
    for stale in old - {ROOT / r for r in pages}:  # 删除已不存在的分页
        stale.unlink()
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    block = f"<!-- STATS:START -->\n{readme_stats(data)}\n<!-- STATS:END -->"
    new = re.sub(r"<!-- STATS:START -->.*?<!-- STATS:END -->", lambda _: block, text, flags=re.S)
    if new != text:
        readme.write_text(new, encoding="utf-8")
        written.append(Path("README.md"))
    return written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="校验，并要求生成的页面已是最新")
    parser.add_argument("--validate-only", action="store_true", help="只校验数据，不生成页面")
    args = parser.parse_args()

    data = load()
    errors = validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if args.validate_only:
        print(f"OK: {len(data['sources'])} sources")
        return 0
    if args.check:
        stale = [rel for rel, content in render_all(data).items()
                 if not (ROOT / rel).exists() or (ROOT / rel).read_text(encoding="utf-8") != content]
        if stale:
            print(f"{len(stale)} 个生成页面不是最新的，请运行 python scripts/build_sources.py", file=sys.stderr)
            return 1
        print(f"OK: {len(data['sources'])} sources")
        return 0
    written = write_outputs(data)
    print(f"已生成站点页面：{len(written)} 个文件有更新（共 {len(data['sources'])} 个信源）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
