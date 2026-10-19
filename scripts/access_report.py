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
# 公开仓库的 GitHub Actions 每天从另一个网络位置跑同样的检查（access.yml 工作流，--raw），结果在这里
REMOTE = "https://raw.githubusercontent.com/pingfanfan/PhDRadar/main/reports/access-actions.json"
RANK = {"ok": 0, "warn": 1, "dead": 2}
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
     "https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/detail/x-1/?phd-id=1",
     "列表页 + 岗位页（链接需带 phd-id）", "DAAD PhDGermany", ""),
    ("德国联邦劳动局职位搜索（Jobsuche）", "https://jobsuche.api.bund.dev/",
     "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs?was=Doktorand&size=1",
     "劳动局自己的搜索接口（文档公开的通用 clientId，无需申请密钥）", "Bundesagentur für Arbeit",
     "旧版 /pc/v4/jobs 已返回 403，改用文档里的 /pc/v6/jobs；截止日期从岗位描述原文取，取不到不收", {"X-API-Key": "jobboerse-jobsuche"}),
    ("CNRS Emploi（法国国家科研中心）", "https://emploi.cnrs.fr/", "https://emploi.cnrs.fr/Offres/Doctorant/UPR3572-HELDUM-001/Default.aspx",
     "站点地图 + 岗位页（博士合同与研究员 CDD）", "CNRS Emploi", ""),
    ("MathJobs（美国数学会）", "https://www.mathjobs.org/jobs", "https://www.mathjobs.org/jobs/list/1",
     "RSS + 岗位页（每 5 秒一次）", "MathJobs", ""),
    ("TAMU 自然资源招聘板（生态/林学）", "https://jobs.rwfm.tamu.edu/", "https://jobs.rwfm.tamu.edu/view-job/?id=1",
     "列表页 + 岗位页", "TAMU Natural Resources Job Board", ""),
    ("H-Net Job Guide（人文社科）", "https://networks.h-net.org/jobs", "https://networks.h-net.org/jobs/1/x",
     "列表页 + 岗位页（每 5 秒一次）", "H-Net Job Guide", ""),
    ("EconJobMarket（经济学）", "https://econjobmarket.org/", "https://econjobmarket.org/positions/1", "列表页 + 岗位页（只收博后）",
     "EconJobMarket", ""),
    ("Aarhus University（丹麦）", "https://international.au.dk/about/profile/vacant-positions/",
     "https://international.au.dk/about/profile/vacant-positions/job/x", "列表页内嵌数据 + 岗位页", "Aarhus University", ""),
    ("PSI（瑞士保罗谢勒研究所）", "https://www.psi.ch/en/hr/job-opportunities", "https://www.psi.ch/en/hr/job-opportunities/1-x",
     "列表页 + 岗位页", "PSI Jobs", ""),
    ("ESO（欧洲南方天文台）", "https://recruitment.eso.org/", "https://recruitment.eso.org/jobs/2026_0001", "列表页 + 岗位页",
     "ESO Recruitment", ""),
    ("IBS（韩国基础科学研究院）", "https://www.ibs.re.kr/prog/recruit/eng/sub04_01/list.do",
     "https://www.ibs.re.kr/prog/recruit/eng/sub04_01/view.do?idx=1", "列表页 + 岗位页（不下载附件，robots.txt 禁止）", "IBS Recruitment", ""),
    # 大学自己的招聘系统（学校清单见 scripts/ats.py）
    ("Workday（大学招聘系统：Aalto、NTU、悉尼、墨尔本、UQ、UBC 等）", "https://aalto.wd3.myworkdayjobs.com/aalto",
     "https://aalto.wd3.myworkdayjobs.com/aalto/siteMap.xml", "各校站点地图 + 公开岗位接口", "Workday", ""),
    ("SAP SuccessFactors（大学招聘系统：EPFL、TU Delft、维也纳、赫尔辛基、根特等）", "https://careers.epfl.ch/",
     "https://careers.epfl.ch/sitemap.xml", "各校站点地图 + 岗位页", "SuccessFactors", ""),
    ("ReachMee（大学招聘系统：Chalmers）", "https://www.chalmers.se/en/about-chalmers/work-with-us/vacancies/",
     "https://web103.reachmee.com/ext/I003/304/main?site=5&lang=UK&validator=a72aeedd63ec10de71e46f8d91d0d57c",
     "外部招聘站列表页 + 岗位页", "ReachMee", ""),
    ("Oracle Recruiting（大学招聘系统：DTU、南丹麦大学）",
     "https://efzu.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions",
     "https://efzu.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&finder=findReqs;"
     "siteNumber=CX_1,limit=1", "候选人站点的公开接口", "Oracle Recruiting", ""),
    ("PageUp（大学招聘系统：港大、La Trobe）", "https://jobs.hku.hk/en/listing/", "https://jobs.hku.hk/en/listing/",
     "列表页 + 岗位页（每 4 秒一次）", "PageUp", "列表页能读，但岗位页对程序访问一律弹 AWS WAF 人机验证（HTTP 202）；不绕过，遇到就停"),
    ("哥本哈根大学招聘页", "https://employment.ku.dk/all-vacancies/", "https://employment.ku.dk/all-vacancies/",
     "列表页 + 岗位页", "University of Copenhagen", ""),
    ("INFN（意大利国家核物理研究院）", "https://jobs.dsi.infn.it/", "https://jobs.dsi.infn.it/dettagli_job.php?id=1", "列表页 + 公告页（博后合同）",
     "INFN Jobs", ""),
    ("Institut Pasteur", "https://research.pasteur.fr/en/jobs/", "https://research.pasteur.fr/en/job/x/", "列表页 + 岗位页", "Institut Pasteur Jobs", ""),
    ("FAPESP Oportunidades（巴西圣保罗州研究基金会）", "https://fapesp.br/oportunidades/", "https://fapesp.br/oportunidades/x/1/",
     "列表页 + 公告页（博士 / 博后奖学金）", "FAPESP Oportunidades", ""),
    ("LINGUIST List（语言学）", "https://linguistlist.org/", "https://linguistlist.org/issues/37/1/", "RSS + 公告页", "LINGUIST List", ""),
    ("ADUM（法国博士论文岗位）", "https://adum.fr/", "https://adum.fr/as/ed/proposition.pl", "", "",
     "robots.txt 对所有程序 Disallow: /"),
    ("JREC-IN Portal（日本）", "https://jrecin.jst.go.jp/", "https://jrecin.jst.go.jp/seek/SeekJorSearch", "", "",
     "robots.txt 允许，但使用条款第 3 条规定转载岗位信息需事先向 JST 申请许可；未申请前不收"),
    ("PhilJobs（哲学）", "https://philjobs.org/", "https://philjobs.org/", "", "",
     "使用条款禁止把内容录入数据库（个人使用除外）"),
    ("AEA JOE（经济学）", "https://www.aeaweb.org/joe/", "https://www.aeaweb.org/joe/listings", "", "",
     "页面写明未经美国经济学会书面许可不得抓取"),
    ("APS Careers（物理）", "https://jobs.aps.org/", "https://jobs.aps.org/", "", "", "robots.txt 对所有程序 Disallow: /"),
    ("HiBrain（韩国）", "https://www.hibrain.net/", "https://www.hibrain.net/", "", "", "robots.txt 对所有程序 Disallow: /"),
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


def page_status(url: str, headers: dict | None = None) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT, **(headers or {})}, timeout=25, stream=True)
        r.close()
        return f"HTTP {r.status_code}"
    except requests.RequestException as e:
        return type(e).__name__


def check_platforms() -> list[dict]:
    postings = yaml.safe_load((ROOT / "_data" / "postings.yml").read_text(encoding="utf-8")) or []
    today = datetime.now(timezone.utc).date().isoformat()
    live = Counter(p["via"] for p in postings if p.get("cn") != "no" and (p["deadline"] == "rolling" or p["deadline"] >= today))

    def one(row):
        name, home, sample, method, via, why, *extra = row
        headers = extra[0] if extra else None
        ok, robots = robots_allows(sample)
        return {"name": name, "url": home, "method": method, "connected": bool(via), "postings": live.get(via, 0) if via else 0,
                "robots": robots, "robots_ok": ok, "page": page_status(sample if headers else home, headers), "why": why}

    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(one, PLATFORMS))


def own_ua(url: str) -> tuple[str, str]:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}, timeout=25, stream=True)
        r.close()
    except requests.RequestException as e:
        return "warn", type(e).__name__
    if r.status_code < 400:
        return "ok", f"HTTP {r.status_code}"
    return ("dead" if r.status_code in (404, 410) else "warn"), f"HTTP {r.status_code}"


def check_sources() -> dict[str, dict]:
    sources = [s for s in load_catalog()["sources"] if s.get("verify_method") == "page"]

    def one(s):
        status, detail = own_ua(s["url"])  # 先用本站的真实标识访问；打不开再按浏览器请求头试一次（check_links 的做法）
        if status != "ok":
            status2, detail2 = check_url(s["url"])
            if RANK[status2] < RANK[status]:
                status, detail = status2, detail2
        return s["id"], {"name": s["name"], "url": s["url"], "status": status, "detail": detail}

    with ThreadPoolExecutor(max_workers=16) as pool:
        return dict(pool.map(one, sources))


def write_doc(platforms: list[dict], sources: dict[str, dict] | None, when: str, remote_when: str = "") -> None:
    lines = ["# 信源可访问性报告", "", f"更新于 {when[:16].replace('T', ' ')} UTC，由 `scripts/access_report.py` 实际访问生成："
             "从两个网络位置各访问一次（我们的服务器" + (f"，以及 GitHub Actions，{remote_when[:16].replace('T', ' ')} UTC" if remote_when else "")
             + "），任一处能打开即算能打开。", "",
             "## 招聘平台：能否被程序接入", "",
             "我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。", "",
             "| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 访问（本服务器 / Actions） | 说明 |", "|---|---|---|---:|---|---|---|"]
    for p in sorted(platforms, key=lambda p: (not p["connected"], -p["postings"])):
        refused = p["page"].startswith("HTTP 403") and (p.get("page_actions") or "HTTP 403").startswith("HTTP 403")
        state = "✅ 已接入" if p["connected"] else ("⛔ 不允许" if p["robots_ok"] is False or refused else "⏸ 未接入")
        lines.append(f"| [{p['name']}]({p['url']}) | {state} | {p['method'] or '—'} | {p['postings'] or '—'} | {p['robots']} | "
                     f"{p['page']} / {p.get('page_actions') or '—'} | {p['why'] or '—'} |")
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


def remote_results() -> dict:
    try:
        r = requests.get(REMOTE, timeout=30)
        return r.json() if r.status_code == 200 else {}
    except (requests.RequestException, ValueError):
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platforms", action="store_true", help="只检查招聘平台")
    ap.add_argument("--raw", help="只把检查结果写到这个 JSON 文件（GitHub Actions 上用），不生成报告")
    args = ap.parse_args()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    platforms = check_platforms()
    sources = None if args.platforms else check_sources()
    if args.raw:
        Path(args.raw).write_text(json.dumps({"generated_at": when, "platforms": platforms, "sources": sources or {}},
                                             ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"原始结果 → {args.raw}")
        return 0
    old = json.loads(JSON_OUT.read_text(encoding="utf-8")) if JSON_OUT.exists() else {}
    if sources is None and old.get("sources"):
        sources = old["sources"]  # 只查平台时沿用上次的信源结果
    remote = remote_results()
    if remote:  # 存一份进主库：同步公开仓库（make_public.py）会整体覆盖，不存就会被冲掉
        (ROOT / "reports" / "access-actions.json").write_text(json.dumps(remote, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in platforms:
        rp = next((x for x in remote.get("platforms", []) if x["name"] == p["name"]), None)
        p["page_actions"] = rp["page"] if rp else ""
    for sid, v in (sources or {}).items():
        rv = (remote.get("sources") or {}).get(sid)
        v["here"] = v.get("here") or v["status"]
        if rv:
            v["actions"] = rv["status"]
            if RANK[rv["status"]] < RANK[v["here"]]:  # 任一网络位置能打开就算能打开
                v["status"], v["detail"] = rv["status"], f"{rv['detail']}（GitHub Actions 上可访问；本服务器：{v['detail']}）"
    JSON_OUT.write_text(json.dumps({"generated_at": when, "remote_generated_at": remote.get("generated_at", ""),
                                    "platforms": platforms, "sources": sources or {}}, ensure_ascii=False, indent=1), encoding="utf-8")
    write_doc(platforms, sources, when, remote.get("generated_at", ""))
    print(f"平台 {len(platforms)} 个（已接入 {sum(p['connected'] for p in platforms)}）"
          + (f"；信源 {len(sources)} 条：{dict(Counter(v['status'] for v in sources.values()))}" if sources else "")
          + f"；Actions 结果 {remote.get('generated_at') or '无'} → {DOC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
