#!/usr/bin/env python3
"""逐条打开信源的官方页面，抓取可见正文，供核实子代理比对（核实必须基于页面本身，而不是搜索摘要）。

    python scripts/fetch_pages.py --pick yes --n 60 --out /tmp/pages/pilot      # 取 60 条 cn_eligible=yes 且未页面核实的条目
    python scripts/fetch_pages.py --ids a,b,c --out /tmp/pages/x

输出目录：
  bundle-<i>.yml   每个文件一批条目：id、字段摘要、页面抓取结果（status/final_url/text）
  index.yml        每条的抓取结局：ok / dead（404/410/域名不存在）/ blocked（403、被拒、超时、robots 禁止）/ pdf_empty

所有请求走 Fetcher.get()（robots.txt、限速、重试）。不保存到仓库，仅供核实使用。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import load_sources  # noqa: E402
from scrapers.common import Disallowed, Fetcher  # noqa: E402

MAX_TEXT = 7000
SHOW = ["id", "name", "url", "levels", "cn_eligible", "coverage", "stipend", "deadline", "deadline_note", "status",
        "requirements", "notes", "verify_method"]


def page_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "nav", "footer", "header", "svg", "form"]):
        t.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip()
    return text.replace("�", "")


def fetch_one(entry: dict) -> dict:
    f = Fetcher(delay=1.0, timeout=25)
    url = entry["url"]
    out = {"id": entry["id"], "outcome": "blocked", "status": None, "final_url": None, "text": ""}
    try:
        r = f.get(url)
    except Disallowed:
        out["outcome"] = "blocked"
        out["error"] = "robots.txt 禁止"
        return out
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else None
        out["status"] = code
        out["outcome"] = "dead" if code in (404, 410) else "blocked"
        out["error"] = f"HTTP {code}"
        return out
    except requests.exceptions.ConnectionError as e:
        msg = str(e)
        # 经代理访问时 DNS 报错并不可靠（试跑中误报过），所以连接类错误一律算“打不开”，不据此判定链接已死
        out["outcome"] = "blocked"
        out["error"] = "连接失败/被断开"
        return out
    except requests.RequestException as e:
        out["error"] = type(e).__name__
        return out
    out["status"] = r.status_code
    out["final_url"] = r.url
    ctype = r.headers.get("Content-Type", "").lower()
    if "pdf" in ctype or urlparse(r.url).path.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(r.content)
            tmp.flush()
            res = subprocess.run(["pdftotext", "-l", "6", "-layout", tmp.name, "-"], capture_output=True, text=True)
        text = re.sub(r"\n\s*\n+", "\n", res.stdout).strip()
    else:
        r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
        text = page_text(r.text)
    if len(text) < 200:
        out["outcome"] = "thin"  # 页面几乎没有正文（多半是前端渲染或登录墙），不能据此判断
    else:
        out["outcome"] = "ok"
    out["text"] = text[:MAX_TEXT]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pick", choices=["yes", "check", "all"], help="按 cn_eligible 选条目")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--skip", type=int, default=0, help="跳过前 N 条（分批用）")
    ap.add_argument("--ids", help="逗号分隔的 id")
    ap.add_argument("--attempted", help="已尝试过的 id 列表文件（每行一个）；本次选中的也会追加进去，避免重复抓取")
    ap.add_argument("--chunks", type=int, default=4)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sources = load_sources()
    if args.ids:
        want = set(args.ids.split(","))
        picked = [s for s in sources if s["id"] in want]
    else:
        pool = [s for s in sources if s.get("verify_method") != "page" and s.get("url", "").startswith("https://")]
        if args.pick in ("yes", "check"):
            pool = [s for s in pool if str(s.get("cn_eligible")) == args.pick]
        if args.attempted and Path(args.attempted).exists():
            done = set(Path(args.attempted).read_text().split())
            pool = [s for s in pool if s["id"] not in done]
        pool.sort(key=lambda s: s["id"])
        picked = pool[args.skip:args.skip + args.n]

    out_dir = Path(args.out)
    if args.attempted:
        with open(args.attempted, "a") as fh:
            fh.write("".join(s["id"] + "\n" for s in picked))
    out_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(fetch_one, picked))

    index = {}
    rows = []
    for s, res in zip(picked, results):
        index[s["id"]] = {"outcome": res["outcome"], "status": res.get("status"), "error": res.get("error")}
        rows.append({"entry": {k: s[k] for k in SHOW if s.get(k) not in (None, "")}, "fetch": res})
    (out_dir / "index.yml").write_text(yaml.safe_dump(index, allow_unicode=True, sort_keys=False), encoding="utf-8")
    # 只把有正文的条目发给核实子代理；dead/blocked/thin 不需要读页面
    readable = [r for r in rows if r["fetch"]["outcome"] == "ok"]
    per = max(1, -(-len(readable) // args.chunks))
    for i in range(0, len(readable), per):
        (out_dir / f"bundle-{i // per + 1}.yml").write_text(
            yaml.safe_dump(readable[i:i + per], allow_unicode=True, sort_keys=False), encoding="utf-8")
    from collections import Counter
    c = Counter(v["outcome"] for v in index.values())
    print(f"共 {len(picked)} 条：{dict(c)} → {out_dir}")


if __name__ == "__main__":
    main()
