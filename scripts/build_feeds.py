#!/usr/bin/env python3
"""生成 RSS 订阅源：只收“现在可申请”的条目（首页同一份数据），按条件分成多个源。

由 build_site.py 在写完 assets/catalog.json 后调用，也可单独运行：

    python scripts/build_feeds.py

写入：
    feeds/*.xml              RSS 2.0 订阅源（全部 / 中国学生可申 / 两周内截止 / 博士 / 博后 / 各学科 / 各地区）
    feeds/index.html         订阅说明页（首页“订阅”入口）
    assets/first-seen.json   每条机会第一次出现在首页的日期（RSS 的发布时间；随每日岗位更新提交）
不收集任何读者信息；想用邮件接收的读者可以自己用 RSS 转邮件服务。
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from build_sources import DISCIPLINE_NAMES, REGION_NAMES  # noqa: E402

SITE = "https://pingfanfan.github.io/PhDRadar/"
MAX_ITEMS = 200  # 每个源最多条数（按首次出现日期从新到旧）
MIN_GROUP = 15   # 学科 / 地区源至少要有这么多条在招机会才单独生成
COVERAGE = {"full": "全奖", "salary": "带薪岗位", "partial": "部分资助", "tuition": "免学费", "stipend": "生活费"}
CN = {"yes": "中国学生可申请", "partial": "部分可申请", "check": "资格待核实"}


def deadline_of(r: dict) -> str:
    return (r.get("o") or {}).get("dl") or r.get("dl") or ""


def first_seen(rows: list[dict], path: Path, today: str) -> dict[str, str]:
    """读取并更新首次出现日期；已下架的条目保留记录，重新上架时不当成新机会。"""
    seen = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for r in rows:
        seen.setdefault(r["id"], today)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(dict(sorted(seen.items())), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return seen


def describe(r: dict) -> str:
    parts = []
    dl = deadline_of(r)
    if dl and dl[0].isdigit():
        parts.append(f"截止 {dl}")
    elif dl == "rolling":
        parts.append("滚动截止")
    if r.get("r"):
        parts.append("、".join(REGION_NAMES.get(c, c) for c in r["r"]))
    parts.append("博后" if r.get("l") == ["postdoc"] else "博士")
    if COVERAGE.get(r.get("c")):
        parts.append(COVERAGE[r["c"]])
    if CN.get(r.get("e")):
        parts.append(CN[r["e"]])
    head = " · ".join(parts)
    body = [f"<p>{escape(head)}</p>"]
    if r.get("s"):
        body.append(f"<p>金额（官网原文）：{escape(str(r['s'])[:200])}</p>")
    if r.get("in"):
        body.append(f"<p>{escape(str(r['in']))}</p>")
    quote = (r.get("o") or {}).get("q")
    if quote:
        body.append(f"<blockquote>{escape(str(quote)[:300])}</blockquote>")
    body.append(f'<p><a href="{escape(r["u"])}">官网</a> · <a href="{SITE}">在 PhDRadar 上查看更多</a></p>')
    return "".join(body)


def rss(key: str, title: str, items: list[dict], seen: dict[str, str]) -> str:
    def pub(d: str) -> str:
        return format_datetime(datetime.fromisoformat(d).replace(tzinfo=timezone.utc))

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>',
           f"<title>{escape(title)} · PhDRadar</title>", f"<link>{SITE}</link>",
           f'<atom:link href="{SITE}feeds/{key}.xml" rel="self" type="application/rss+xml"/>',
           "<description>为中国学生整理的海外带奖博士 / 博后机会，每条都核对过官网原句，截止后自动下架。</description>",
           "<language>zh-cn</language>"]
    if items:
        out.append(f"<lastBuildDate>{pub(max(seen[r['id']] for r in items))}</lastBuildDate>")
    for r in items:
        name = r["n"] + (f"（{r['org']}）" if r.get("org") and r["org"] not in r["n"] else "")
        out.append("<item>"
                   f"<title>{escape(name)}</title><link>{escape(r['u'])}</link>"
                   f'<guid isPermaLink="false">phdradar:{escape(r["id"])}</guid>'
                   f"<pubDate>{pub(seen[r['id']])}</pubDate>"
                   f"<description>{escape(describe(r))}</description></item>")
    out.append("</channel></rss>")
    return "\n".join(out) + "\n"


def groups(open_rows: list[dict], today: str) -> list[tuple[str, str, str, list[dict]]]:
    """(文件名, 标题, 分组, 条目)。"""
    soon = (date.fromisoformat(today) + timedelta(days=14)).isoformat()
    out = [("all", "全部现在可申请", "常用", open_rows),
           ("cn", "中国学生可申请", "常用", [r for r in open_rows if r.get("e") == "yes"]),
           ("soon", "两周内截止", "常用", [r for r in open_rows if today <= deadline_of(r)[:10] <= soon and deadline_of(r)[0].isdigit()]),
           ("phd", "博士", "常用", [r for r in open_rows if "phd" in (r.get("l") or ["phd"])]),
           ("postdoc", "博后", "常用", [r for r in open_rows if "postdoc" in (r.get("l") or [])])]
    for code, name in DISCIPLINE_NAMES.items():
        if code == "all":  # “不限学科”不单独成源
            continue
        items = [r for r in open_rows if code in (r.get("d") or [])]
        if len(items) >= MIN_GROUP:
            out.append((f"d-{code}", name, "按学科", items))
    for code, name in REGION_NAMES.items():
        items = [r for r in open_rows if code in (r.get("r") or [])]
        if len(items) >= MIN_GROUP:
            out.append((f"r-{code.lower()}", name, "按地区", items))
    return out


def index_page(feeds: list[tuple[str, str, str, int]]) -> str:
    sections = []
    for group in dict.fromkeys(g for _, _, g, _ in feeds):
        lis = "".join(
            f'<li><span>{escape(t)} <em>{n}</em></span><code>{SITE}feeds/{k}.xml</code>'
            f'<button data-u="{SITE}feeds/{k}.xml">复制链接</button></li>'
            for k, t, g, n in feeds if g == group)
        sections.append(f"<h2>{escape(group)}</h2><ul>{lis}</ul>")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 本文件由 scripts/build_feeds.py 自动生成，请勿手动编辑 -->
<title>订阅 · PhDRadar</title>
<link rel="alternate" type="application/rss+xml" title="PhDRadar 全部现在可申请" href="all.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%230E7A5A'/%3E%3Cg fill='none' stroke='%23fff' stroke-width='2.2' stroke-linecap='round'%3E%3Cpath d='M16 16 23.5 8.5'/%3E%3Cpath d='M9 16a7 7 0 1 0 7-7'/%3E%3C/g%3E%3Ccircle cx='16' cy='16' r='2.4' fill='%23fff'/%3E%3C/svg%3E">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@500&family=Noto+Sans+SC:wght@400;500;700&display=swap">
<style>
:root{{--bg:#F5F7F6;--surface:#fff;--ink:#0F1A17;--muted:#5B6863;--faint:#8A9692;--line:#E4E9E6;--soft:#EFF3F1;--brand:#0E7A5A;--brand-ink:#fff;--brand-soft:#E2F4EC;--brand-text:#0A6448;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0B1110;--surface:#121A18;--ink:#E6EEEA;--muted:#93A29B;--faint:#66746E;--line:#1F2A27;--soft:#18221F;--brand:#34C38F;--brand-ink:#04120C;--brand-soft:#133026;--brand-text:#5FD6A8;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0B1110;--surface:#121A18;--ink:#E6EEEA;--muted:#93A29B;--faint:#66746E;--line:#1F2A27;--soft:#18221F;--brand:#34C38F;--brand-ink:#04120C;--brand-soft:#133026;--brand-text:#5FD6A8;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 "Geist","Noto Sans SC","PingFang SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
main{{max-width:760px;margin:0 auto;padding-block:20px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
a{{color:var(--brand-text)}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:28px}}
.brand{{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700;font-size:17px}}
.mark{{width:30px;height:30px;border-radius:9px;background:var(--brand);color:var(--brand-ink);display:grid;place-items:center}}
.ic{{fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.top a.back{{font-size:14px;text-decoration:none;color:var(--muted)}}
h1{{font-size:clamp(22px,4vw,28px);font-weight:700;letter-spacing:-.02em;margin:0 0 10px;text-wrap:balance}}
h2{{font-size:12.5px;font-weight:600;color:var(--muted);letter-spacing:.04em;margin:30px 0 8px}}
.note{{color:var(--muted);margin:0}} .note b{{color:var(--ink)}}
.how{{margin:16px 0 0;padding:14px 16px;border-radius:12px;background:var(--brand-soft);color:var(--ink);font-size:14px}}
ul{{list-style:none;padding:0;margin:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
li{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;align-items:center;padding:12px 14px;border-top:1px solid var(--line)}}
li:first-child{{border-top:0}}
li span{{font-weight:600}} em{{font-style:normal;font-family:"Geist Mono",ui-monospace,monospace;color:var(--faint);font-size:12.5px;font-weight:500;margin-left:6px}}
code{{grid-column:1;font:12px/1.5 "Geist Mono",ui-monospace,monospace;color:var(--muted);overflow-wrap:anywhere}}
button{{grid-row:1/3;grid-column:2;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--soft);color:var(--ink);border-radius:999px;padding:7px 14px;font:inherit;font-size:13px;cursor:pointer}}
button:hover{{border-color:var(--brand);color:var(--brand-text)}}
:focus-visible{{outline:2px solid var(--brand);outline-offset:2px}}
</style></head><body><main>
<div class="top"><a class="brand" href="../"><span class="mark" aria-hidden="true"><svg class="ic" width="20" height="20" viewBox="0 0 24 24" style="stroke-width:2.2"><path d="M12 12 17.5 6.5"/><path d="M6.5 12A5.5 5.5 0 1 0 12 6.5"/><path d="M3 12a9 9 0 1 0 9-9"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/></svg></span>PhDRadar</a><a class="back" href="../">返回首页</a></div>
<h1>订阅新机会</h1>
<p class="note">每天随岗位更新刷新，只推送“现在可申请”的新机会：核对过官网原句，截止后自动下架。数字是当前在招条数，每个源最多保留最新 {MAX_ITEMS} 条。</p>
<p class="how"><b>怎么用：</b>复制链接，粘贴到 RSS 阅读器（Inoreader、Feedly、NetNewsWire、Folo 等）。想在邮箱里收，把链接交给 RSS 转邮件服务（如 Blogtrottr、FeedRabbit）。本站不收集任何邮箱。</p>
{''.join(sections)}
</main>
<script>
document.querySelectorAll("button[data-u]").forEach(b=>b.addEventListener("click",async()=>{{
  try{{await navigator.clipboard.writeText(b.dataset.u);b.textContent="已复制";}}catch(e){{b.textContent="请手动复制";}}
  setTimeout(()=>b.textContent="复制链接",1500);
}}));
</script>
</body></html>
"""


def write_feeds(rows: list[dict], root: Path = ROOT, today: str | None = None) -> int:
    today = today or datetime.now(timezone.utc).date().isoformat()
    open_rows = [r for r in rows if r.get("o") and r.get("e") != "no"]
    seen = first_seen(open_rows, root / "assets" / "first-seen.json", today)
    open_rows.sort(key=lambda r: deadline_of(r) or "~")  # 同一天新出现的：先截止的在前
    open_rows.sort(key=lambda r: seen[r["id"]], reverse=True)  # 新出现的在前（稳定排序保留上一步顺序）
    out_dir = root / "feeds"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.xml"):
        old.unlink()
    listed = []
    for key, title, group, items in groups(open_rows, today):
        (out_dir / f"{key}.xml").write_text(rss(key, title, items[:MAX_ITEMS], seen), encoding="utf-8")
        listed.append((key, title, group, len(items)))
    (out_dir / "index.html").write_text(index_page(listed), encoding="utf-8")
    return len(listed)


def main() -> int:
    rows = json.loads((ROOT / "assets" / "catalog.json").read_text(encoding="utf-8"))
    n = write_feeds(rows)
    print(f"订阅源：{n} 个 → feeds/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
