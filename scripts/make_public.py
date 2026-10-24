#!/usr/bin/env python3
"""生成公开仓库（PhDRadar）的快照：只保留核实过的条目。

    python scripts/make_public.py /home/user/phdradar

公开的条目 = 逐页核对过官网（verify_method: page）∪ 现在可申请清单（_data/open_now.yml，已核对官网原句）
∪ 抓取器对应的招聘平台本身。
未核实的信源、自动发现的导师线索、抓取到的原始岗位、研究员收件箱等内部文件都不公开。
复制后在目标目录重新生成阅读页面与导出数据；不负责提交与推送。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import load_catalog  # noqa: E402

PUBLIC_NAME = "PhDRadar"
# 不公开的内部文件（前缀匹配）
PRIVATE = ("research/inbox/", "research/verify-sprint.txt", "research/workers.yml", "data/discovery/",
           "data/jobs.json", "data/jobs.md", "data/seen.json", "reports/discovery.md", "research/outreach.md",
           "reports/access-all.csv",  # 含未核实的信源
           # 这两个定时工作流会提交未核实的导师线索与原始岗位，公开仓库不运行
           ".github/workflows/discover.yml", ".github/workflows/scrape.yml")
# 公开仓库自己的工作流生成并提交的文件：以公开仓库里的版本为准，同步时保留，不用私有库的旧副本覆盖
PUBLIC_OWNED = ("reports/source-health.json", "reports/source-health.md", "reports/access-actions.json")
REBUILD = ["scripts/build_sources.py", "scripts/export_data.py", "scripts/build_open.py", "scripts/build_site.py"]


def newer_platform_rows(mine: list[dict], public: list[dict], names) -> list[dict]:
    """只能在公开仓库 Actions 上采集的平台（names）：公开仓库里的那份更新（checked 更晚）就用公开仓库的，其余平台用本仓库的。
    避免同步把 Actions 刚采到、本仓库还没并回的岗位冲掉。"""
    plat = lambda r: r["id"].split(":")[0]  # noqa: E731
    out = list(mine)
    for name in names:
        latest = lambda rows: max((str(r.get("checked") or "") for r in rows if plat(r) == name), default="")  # noqa: E731
        if latest(public) > latest(mine):
            out = [r for r in out if plat(r) != name] + [r for r in public if plat(r) == name]
    return sorted(out, key=lambda r: (str(r.get("deadline")), r["id"]))


def public_ids() -> set[str]:
    open_ids = {r["id"] for r in yaml.safe_load((ROOT / "_data" / "open_now.yml").read_text(encoding="utf-8")) or []}
    from scrapers.sources import ADAPTERS  # 抓取器对应的招聘平台本身（EURAXESS、jobs.ac.uk 等）也保留

    platforms = set(ADAPTERS)  # 键就是 SOURCE_ID
    return {s["id"] for s in load_catalog()["sources"]
            if s.get("verify_method") == "page" or s["id"] in open_ids or s["id"] in platforms}


def dump(path: Path, data) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    dest = Path(sys.argv[1]).resolve()
    if not (dest / ".git").exists():
        print(f"{dest} 不是 git 仓库")
        return 2
    keep = public_ids()
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    owned = {f: (dest / f).read_bytes() for f in PUBLIC_OWNED if (dest / f).exists()}
    pub_postings = dest / "_data" / "postings.yml"
    public_rows = yaml.safe_load(pub_postings.read_text(encoding="utf-8")) or [] if pub_postings.exists() else []
    # 先清空目标（保留 .git），保证删掉的文件在公开仓库里也删掉
    for p in dest.iterdir():
        if p.name != ".git":
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    for f in files:
        if f.startswith(PRIVATE):
            continue
        src, out = ROOT / f, dest / f
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(src, out)
            continue
        out.write_text(text.replace("PhDRadar", PUBLIC_NAME), encoding="utf-8")
    for f, data in owned.items():
        (dest / f).parent.mkdir(parents=True, exist_ok=True)
        (dest / f).write_bytes(data)
    (dest / "research" / "inbox").mkdir(parents=True, exist_ok=True)
    (dest / "research" / "inbox" / ".gitkeep").touch()

    if public_rows:
        sys.path.insert(0, str(ROOT / "scripts"))
        from collect_postings import ACTIONS
        mine = yaml.safe_load(pub_postings.read_text(encoding="utf-8")) or []
        merged = newer_platform_rows(mine, public_rows, ACTIONS)
        if merged != mine:
            dump(pub_postings, merged)
            print("保留公开仓库里更新的平台岗位：" + ", ".join(sorted(ACTIONS)))

    main_file = dest / "_data" / "sources.yml"
    data = yaml.safe_load(main_file.read_text(encoding="utf-8"))
    data["sources"] = [s for s in data["sources"] if s["id"] in keep]
    dump(main_file, data)
    for extra in sorted((dest / "_data" / "sources_extra").glob("*.yml")):
        dump(extra, [s for s in (yaml.safe_load(extra.read_text(encoding="utf-8")) or []) if s["id"] in keep])
    dump(dest / "_data" / "faculty.yml", {"faculty": []})  # 导师线索未逐条核实，不公开
    # 公开仓库用自己的 README（不链接内部报告与私密中台）；STATS 区块由 build_sources.py 填充
    shutil.copy2(ROOT / "scripts" / "public_readme.md", dest / "README.md")

    for script in REBUILD:
        subprocess.run([sys.executable, script], cwd=dest, check=True)
    print(f"公开快照：{len(keep)} 条核实过的信源 → {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
