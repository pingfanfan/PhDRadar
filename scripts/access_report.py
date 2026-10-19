#!/usr/bin/env python3
"""可访问性报告：权威招聘平台能否被程序接入、核对过的高质量信源能否打开。

    python scripts/access_report.py              # 平台 + 全部逐页核对过的信源（约 2000 条，需外网，约 10 分钟）
    python scripts/access_report.py --platforms  # 只检查平台

写入：
    docs/access.md              给读者看的报告（平台接入状态 + 打不开的信源清单）
    reports/access.json         逐条结果（失效链接会进入核实队列，见 verify_queue.py）
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.robotparser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import load_catalog  # noqa: E402
from check_links import check_url  # noqa: E402
from scrapers.common import USER_AGENT  # noqa: E402

DOC = ROOT / "docs" / "access.md"
JSON_OUT = ROOT / "reports" / "access.json"

# 权威招聘平台：(名称, 页面, 程序要读的岗位页样例, 接入方式, 岗位清单里的 via 名, 未接入时的原因)
PLATFORMS = [
    ("FindAPhD", "https://www.findaphd.com/", "https://www.findaphd.com/phds/project/x/?p100000", "站点地图 + 岗位页（在 GitHub Actions 上采集）", "FindAPhD",
     "本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行"),
    ("jobs.ac.uk", "https://www.jobs.ac.uk/", "https://www.jobs.ac.uk/job/ABC123/x", "搜索列表 + 岗位页", "jobs.ac.uk", ""),
    ("AcademicTransfer（荷兰）", "https://www.academictransfer.com/en/", "https://www.academictransfer.com/en/jobs/1/x/",
     "站点地图 + 岗位页", "AcademicTransfer", ""),
    ("Nature Careers", "https://www.nature.com/naturecareers/", "https://www.nature.com/naturecareers/job/1/x/", "站点地图 + 岗位页",
     "Nature Careers", ""),
    ("Science Careers", "https://jobs.sciencecareers.org/", "https://jobs.sciencecareers.org/job/1/x/", "站点地图 + 岗位页",
     "Science Careers", ""),
    ("Physics Today Jobs", "https://jobs.physicstoday.org/", "https://jobs.physicstoday.org/job/1/x/", "站点地图 + 岗位页",
     "Physics Today Jobs", ""),
    ("THE Unijobs", "https://www.timeshighereducation.com/unijobs/", "https://www.timeshighereducation.com/unijobs/listing/1/x/",
     "站点地图 + 岗位页", "THE Unijobs", ""),
    ("Jobbnorge（挪威）", "https://www.jobbnorge.no/", "https://publicapi.jobbnorge.no/v1/jobs?lang=2", "官方公开接口", "Jobbnorge", ""),
    ("Varbi（瑞典高校）", "https://lu.varbi.com/en/", "https://lu.varbi.com/en/what:job/jobID:1/", "各校列表页 + 岗位页", "Varbi", ""),
    ("ETH Zurich Jobs", "https://jobs.ethz.ch/", "https://jobs.ethz.ch/job/view/1", "列表页 + 岗位页", "ETH Zurich Jobs", ""),
    ("Inria Jobs", "https://jobs.inria.fr/public/classic/en/offres", "https://jobs.inria.fr/public/classic/en/offres/2026-00001",
     "列表页 + 岗位页", "Inria Jobs", ""),
    ("马普学会（Max Planck）", "https://www.mpg.de/stellenboerse", "https://www.mpg.de/feeds/stellenangebote.rss", "RSS + 岗位页",
     "Max-Planck-Gesellschaft", ""),
    ("INSPIRE-HEP Jobs", "https://inspirehep.net/jobs", "https://inspirehep.net/api/jobs/1", "官方公开接口", "INSPIRE-HEP Jobs", ""),
    ("Academic Jobs Online", "https://academicjobsonline.org/ajo/jobs", "https://academicjobsonline.org/ajo/jobs/1",
     "RSS + 岗位页（每 5 秒一次）", "Academic Jobs Online", ""),
    ("EURAXESS", "https://euraxess.ec.europa.eu/jobs/search", "https://euraxess.ec.europa.eu/jobs/1", "", "",
     "robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请"),
    ("academics.de（德国）", "https://www.academics.de/", "https://www.academics.de/jobs/x", "", "",
     "robots.txt 写明自动采集需书面许可；已起草数据合作申请"),
    ("FindAPostdoc", "https://www.findapostdoc.com/", "https://www.findapostdoc.com/", "", "", "所有程序访问返回 403"),
    ("Academic Positions", "https://academicpositions.com/", "https://academicpositions.com/jobs", "", "", "所有程序访问返回 403"),
    ("DAAD PhDGermany", "https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/",
     "https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/detail/x-1/", "", "",
     "允许访问，但资助说明是浏览器里动态加载的，程序读到的页面没有资助信息，无法核对"),
    ("Chronicle Jobs（美国）", "https://jobs.chronicle.com/", "https://jobs.chronicle.com/job/1/x/", "", "",
     "允许访问，但抽查 40 个岗位页都不写截止日期"),
    ("Inside Higher Ed Careers", "https://careers.insidehighered.com/", "https://careers.insidehighered.com/job/1/x/", "", "",
     "允许访问，但岗位页只有广告下架日期，没有申请截止日期"),
]


def robots_allows(url: str) -> tuple[bool | None, str]:
    p = urlparse(url)
    try:
        r = requests.get(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": USER_AGENT}, timeout=20)
    except requests.RequestException as e:
        return None, f"robots.txt 取不到（{type(e).__name__}）"
    if r.status_code >= 400:
        return True, f"无 robots.txt（HTTP {r.status_code}）"
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text.splitlines())
    ok = rp.can_fetch(USER_AGENT, url)
    delay = rp.crawl_delay(USER_AGENT)
    return ok, ("允许" if ok else "禁止") + (f"，要求每 {delay} 秒一次" if delay else "")


def page_status(url: str) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=25, stream=True)
        r.close()
        return f"HTTP {r.status_code}"
    except requests.RequestException as e:
        return type(e).__name__


def check_platforms() -> list[dict]:
    postings = yaml.safe_load((ROOT / "_data" / "postings.yml").read_text(encoding="utf-8")) or []
    today = datetime.now(timezone.utc).date().isoformat()
    live = Counter(p["via"] for p in postings if p.get("cn") != "no" and (p["deadline"] == "rolling" or p["deadline"] >= today))

    def one(row):
        name, home, sample, method, via, why = row
        ok, robots = robots_allows(sample)
        return {"name": name, "url": home, "method": method, "connected": bool(via), "postings": live.get(via, 0) if via else 0,
                "robots": robots, "robots_ok": ok, "page": page_status(home), "why": why}

    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(one, PLATFORMS))


def check_sources() -> dict[str, dict]:
    sources = [s for s in load_catalog()["sources"] if s.get("verify_method") == "page"]

    def one(s):
        status, detail = check_url(s["url"])
        return s["id"], {"name": s["name"], "url": s["url"], "status": status, "detail": detail}

    with ThreadPoolExecutor(max_workers=16) as pool:
        return dict(pool.map(one, sources))


def write_doc(platforms: list[dict], sources: dict[str, dict] | None, when: str) -> None:
    lines = ["# 信源可访问性报告", "", f"更新于 {when[:16].replace('T', ' ')} UTC，由 `scripts/access_report.py` 从服务器实际访问生成。", "",
             "## 招聘平台：能否被程序接入", "",
             "我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。", "",
             "| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 首页访问 | 说明 |", "|---|---|---|---:|---|---|---|"]
    for p in sorted(platforms, key=lambda p: (not p["connected"], -p["postings"])):
        state = "✅ 已接入" if p["connected"] else ("⛔ 不允许" if p["robots_ok"] is False or "403" in p["why"] else "⏸ 未接入")
        lines.append(f"| [{p['name']}]({p['url']}) | {state} | {p['method'] or '—'} | {p['postings'] or '—'} | {p['robots']} | "
                     f"{p['page']} | {p['why'] or '—'} |")
    if sources is not None:
        c = Counter(v["status"] for v in sources.values())
        n = len(sources)
        lines += ["", "## 核对过的高质量信源：能否打开", "",
                  f"对 {n} 条逐页核对过官网的信源实际访问一次：✅ 能打开 {c['ok']}（{c['ok'] * 100 // max(n, 1)}%）· "
                  f"⚠️ 服务器拦截脚本或需登录 {c['warn']} · ❌ 失效 {c['dead']}。", "",
                  "“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；"
                  "“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。", ""]
        for status, title in (("dead", "❌ 失效"), ("warn", "⚠️ 拦截脚本 / 需登录")):
            rows = sorted(((k, v) for k, v in sources.items() if v["status"] == status), key=lambda kv: kv[1]["name"])
            if not rows:
                continue
            lines += [f"### {title}（{len(rows)}）", "", "<details><summary>展开清单</summary>", "", "| 信源 | 结果 |", "|---|---|"]
            lines += [f"| [{v['name'].replace('|', '/')}]({v['url']}) | {v['detail'].replace('|', '/')} |" for _, v in rows]
            lines += ["", "</details>", ""]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platforms", action="store_true", help="只检查招聘平台")
    args = ap.parse_args()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    platforms = check_platforms()
    old = json.loads(JSON_OUT.read_text(encoding="utf-8")) if JSON_OUT.exists() else {}
    sources = None if args.platforms else check_sources()
    if sources is None and old.get("sources"):
        sources = old["sources"]  # 只查平台时沿用上次的信源结果
    JSON_OUT.write_text(json.dumps({"generated_at": when, "platforms": platforms, "sources": sources or {}},
                                   ensure_ascii=False, indent=1), encoding="utf-8")
    write_doc(platforms, sources, when)
    print(f"平台 {len(platforms)} 个（已接入 {sum(p['connected'] for p in platforms)}）"
          + (f"；信源 {len(sources)} 条：{dict(Counter(v['status'] for v in sources.values()))}" if sources else "") + f" → {DOC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
