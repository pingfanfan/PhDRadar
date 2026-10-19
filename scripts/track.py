#!/usr/bin/env python3
"""申请追踪看板：想投 → 准备中 → 已投 → 面试 → 结果，并给出截止 / 套磁 / 面试提醒。

数据存在 applications/tracker.yml（申请者私有，不提交）。

    python scripts/track.py add findaphd:195793
    python scripts/track.py add https://example.edu/phd --title "..." --org "..." --deadline 2026-11-30
    python scripts/track.py stage findaphd:195793 已投
    python scripts/track.py contact findaphd:195793 --to "Prof. X" --note "发了简历"
    python scripts/track.py reply findaphd:195793 --to "Prof. X"
    python scripts/track.py board | remind | weekly | ics
    python scripts/track.py import-site saved.json      # 网站“我的收藏”导出的 JSON

--file 覆盖看板路径，--today YYYY-MM-DD 覆盖今天（默认北京时间）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "applications" / "tracker.yml"
POSTINGS = ROOT / "_data" / "postings.yml"
RANKING_DIRS = [ROOT / "rankings", ROOT / "applications" / "rankings"]

STAGES = ["want", "prep", "sent", "interview", "result"]
STAGE_CN = {"want": "想投", "prep": "准备中", "sent": "已投", "interview": "面试", "result": "结果"}
STAGE_ALIAS = {**{s: s for s in STAGES}, **{v: k for k, v in STAGE_CN.items()},
               "已申请": "sent", "准备": "prep", "收藏": "want"}
RESULTS = ["offer", "reject", "withdraw"]
RESULT_CN = {"offer": "录取", "reject": "被拒", "withdraw": "已放弃"}
FIELDS = ["id", "title", "org", "url", "deadline", "deadline_note", "stage", "result",
          "contacts", "interview", "notes", "history", "added"]
REMIND_DAYS = (14, 7, 1)
FOLLOW_UP_DAYS = 10
INTERVIEW_DAYS = 3
INTERVIEW_CHECKLIST = ("复习研究计划与代表作、读导师近两年论文、准备 3 分钟自我介绍、"
                       "准备要问导师的问题（资助年限、组里氛围、毕业去向）、测试网络 / 摄像头并确认时区")


# ---------- 基础工具 ----------

def beijing_today() -> date:
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("Asia/Shanghai")
    except Exception:  # 没有时区数据库时退回固定 UTC+8
        tz = timezone(timedelta(hours=8))
    return datetime.now(tz).date()


def to_date(value) -> date | None:
    """把 '2026-11-30' / date 转成 date；rolling、unknown、空值返回 None。"""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.isoformat()[:10]
    return str(value)


def normalize(entry: dict) -> dict:
    """统一字段类型与 key 顺序（日期一律存成字符串）。"""
    e = dict(entry)
    for key in ("id", "title", "org", "url", "deadline", "deadline_note", "result", "interview", "notes", "added"):
        e[key] = _str(e.get(key))
    e["stage"] = STAGE_ALIAS.get(_str(e.get("stage")), "want")
    e["contacts"] = [{"to": _str(c.get("to")), "date": _str(c.get("date")),
                      "replied": bool(c.get("replied")), "note": _str(c.get("note"))}
                     for c in (e.get("contacts") or []) if isinstance(c, dict)]
    e["history"] = [{"date": _str(h.get("date")), "stage": _str(h.get("stage")),
                     **({"result": _str(h["result"])} if h.get("result") else {})}
                    for h in (e.get("history") or []) if isinstance(h, dict)]
    out = {k: e[k] for k in FIELDS if k in e}
    out.update({k: v for k, v in e.items() if k not in FIELDS})
    if not out.get("interview"):
        out.pop("interview", None)
    if not out.get("deadline_note"):
        out.pop("deadline_note", None)
    return out


def load_tracker(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return [normalize(e) for e in data if isinstance(e, dict)]


def save_tracker(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump([normalize(e) for e in entries], sort_keys=False, allow_unicode=True, width=1000)
    path.write_text("# 申请追踪看板（私有数据，不要提交）。由 scripts/track.py 维护。\n" + text, encoding="utf-8")


def load_postings() -> list[dict]:
    if not POSTINGS.exists():
        return []
    return yaml.safe_load(POSTINGS.read_text(encoding="utf-8")) or []


def load_sources() -> list[dict]:
    try:
        sys.path.insert(0, str(ROOT))
        from catalog import load_catalog
        return load_catalog()["sources"]
    except Exception as exc:  # catalog 读不了也不影响看板
        print(f"提示：读取信源目录失败（{exc}），只按 postings 查找。", file=sys.stderr)
        return []


def lookup(key: str, postings: list[dict] | None = None, sources: list[dict] | None = None) -> dict | None:
    """按 id 或 url 在岗位与信源目录里查找，返回看板字段；postings/sources 可注入（测试用）。"""
    postings = load_postings() if postings is None else postings
    for p in postings:
        if key in (_str(p.get("id")), _str(p.get("url"))):
            return {"id": _str(p.get("id")), "title": _str(p.get("title")), "org": _str(p.get("org")),
                    "url": _str(p.get("url")), "deadline": _str(p.get("deadline")) or "unknown",
                    "deadline_note": _str(p.get("quote"))}
    sources = load_sources() if sources is None else sources
    for s in sources:
        if key in (_str(s.get("id")), _str(s.get("url"))):
            dl = _str(s.get("deadline"))
            return {"id": _str(s.get("id")), "title": _str(s.get("name")), "org": _str(s.get("org") or s.get("institution")),
                    "url": _str(s.get("url")), "deadline": dl if to_date(dl) or dl in ("rolling", "unknown") else "unknown",
                    "deadline_note": "" if to_date(dl) or dl in ("rolling", "unknown", "") else dl}
    return None


def find(entries: list[dict], key: str) -> dict | None:
    for e in entries:
        if key in (e.get("id"), e.get("url")):
            return e
    return None


def require(entries: list[dict], key: str) -> dict:
    e = find(entries, key)
    if e is None:
        raise SystemExit(f"看板里没有 {key}，先用 add 添加。")
    return e


def days_left(entry: dict, today: date) -> int | None:
    d = to_date(entry.get("deadline"))
    return (d - today).days if d else None


def deadline_text(entry: dict, today: date) -> str:
    dl = entry.get("deadline") or "unknown"
    n = days_left(entry, today)
    if n is None:
        return {"rolling": "滚动招生", "unknown": "截止未知"}.get(dl, f"截止 {dl}")
    note = f"（{entry['deadline_note']}）" if entry.get("deadline_note") else ""
    if n < 0:
        return f"截止 {dl}{note}，已过 {-n} 天"
    if n == 0:
        return f"截止 {dl}{note}，就是今天"
    return f"截止 {dl}{note}，还剩 {n} 天"


def pending_contacts(entry: dict, today: date) -> list[tuple[dict, int]]:
    """≥10 天未回复的套磁（只看 想投/准备中/已投）。"""
    if entry["stage"] not in ("want", "prep", "sent"):
        return []
    out = []
    for c in entry.get("contacts") or []:
        d = to_date(c.get("date"))
        if d and not c.get("replied") and (today - d).days >= FOLLOW_UP_DAYS:
            out.append((c, (today - d).days))
    return out


def todo(entry: dict, today: date) -> str:
    """看板上每条的待办提示。"""
    stage, n = entry["stage"], days_left(entry, today)
    if pending_contacts(entry, today):
        return "跟进未回复的套磁"
    if stage == "want":
        if n is not None and n < 0:
            return "已过截止，确认是否有下一轮，否则移到结果（withdraw）"
        return "确认资格与材料清单，决定是否开始准备" if entry.get("contacts") else "先套磁导师或确认资格与材料清单"
    if stage == "prep":
        if n is not None and n < 0:
            return "已过截止，确认是否已投或放弃"
        return "完成材料并提交" + (f"（剩 {n} 天）" if n is not None else "")
    if stage == "sent":
        return "等待回复，留意邮箱与申请系统"
    if stage == "interview":
        iv = to_date(entry.get("interview"))
        if iv and iv >= today:
            return f"面试 {iv.isoformat()}，按清单准备"
        return "面试后发感谢信，等待结果"
    return RESULT_CN.get(entry.get("result"), "记录结果")


# ---------- 子命令 ----------

def cmd_add(entries: list[dict], key: str, today: date, title: str = "", org: str = "", deadline: str = "",
            url: str = "", postings: list[dict] | None = None, sources: list[dict] | None = None) -> tuple[dict, bool]:
    """添加一条；已存在则返回原条目（第二个值为 False）。"""
    existing = find(entries, key) or (find(entries, url) if url else None)
    if existing:
        return existing, False
    found = lookup(key, postings, sources) or (lookup(url, postings, sources) if url else None)
    if found:
        existing = find(entries, found["id"]) or find(entries, found["url"])
        if existing:
            return existing, False
        base = found
    else:
        is_url = key.startswith(("http://", "https://"))
        url = url or (key if is_url else "")
        if not title or not url:
            raise SystemExit(f"在岗位和信源目录里没找到 {key}，请至少给出 --title 和 --url。")
        eid = "custom:" + hashlib.sha1(url.encode()).hexdigest()[:8] if is_url else key
        base = {"id": eid, "title": title, "org": org, "url": url, "deadline": "unknown"}
    if deadline:
        if not (to_date(deadline) or deadline in ("rolling", "unknown")):
            raise SystemExit("--deadline 要写成 YYYY-MM-DD，或 rolling / unknown。")
        base["deadline"] = deadline
    for k, v in (("title", title), ("org", org), ("url", url)):
        if v:
            base[k] = v
    entry = normalize({**base, "stage": "want", "result": "", "contacts": [], "notes": "",
                       "history": [{"date": today.isoformat(), "stage": "want"}], "added": today.isoformat()})
    entries.append(entry)
    return entry, True


def cmd_stage(entry: dict, stage: str, today: date, result: str = "", when: str = "") -> None:
    s = STAGE_ALIAS.get(stage.strip())
    if s is None:
        raise SystemExit(f"未知阶段 {stage}；可用：{' / '.join(f'{k}({v})' for k, v in STAGE_CN.items())}")
    if result and result not in RESULTS:
        raise SystemExit(f"--result 只能是 {' / '.join(RESULTS)}")
    if result and s != "result":
        raise SystemExit("--result 只在阶段为 result（结果）时使用。")
    d = when or today.isoformat()
    if not to_date(d):
        raise SystemExit("--date 要写成 YYYY-MM-DD。")
    entry["stage"] = s
    entry["result"] = result if s == "result" else ""
    entry.setdefault("history", []).append({"date": d, "stage": s, **({"result": result} if result else {})})


def cmd_contact(entry: dict, to: str, today: date, when: str = "", note: str = "") -> None:
    d = when or today.isoformat()
    if not to_date(d):
        raise SystemExit("--date 要写成 YYYY-MM-DD。")
    entry.setdefault("contacts", []).append({"to": to, "date": d, "replied": False, "note": note})


def cmd_reply(entry: dict, to: str = "") -> int:
    n = 0
    for c in entry.get("contacts") or []:
        if not c.get("replied") and (not to or c.get("to") == to):
            c["replied"] = True
            n += 1
    return n


def board(entries: list[dict], today: date) -> str:
    lines = [f"# 申请看板（{today.isoformat()}）", ""]
    for s in STAGES:
        items = [e for e in entries if e["stage"] == s]
        items.sort(key=lambda e: (days_left(e, today) is None, days_left(e, today) or 0))
        lines.append(f"## {STAGE_CN[s]}（{len(items)}）")
        lines.append("")
        if not items:
            lines.append("- （空）")
        for e in items:
            name = f"[{e['title'] or e['id']}]({e['url']})" if e.get("url") else (e["title"] or e["id"])
            org = f" · {e['org']}" if e.get("org") else ""
            res = f" · {RESULT_CN.get(e['result'], e['result'])}" if s == "result" and e.get("result") else ""
            lines.append(f"- {name}{org} · {deadline_text(e, today)}{res} · 待办：{todo(e, today)} `{e['id']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def remind(entries: list[dict], today: date) -> list[str]:
    out = []
    for e in entries:
        name = f"{e['title'] or e['id']}" + (f"（{e['org']}）" if e.get("org") else "")
        n = days_left(e, today)
        if e["stage"] in ("want", "prep") and n is not None:
            note = f"，{e['deadline_note']}" if e.get("deadline_note") else ""
            if n < 0:
                out.append(f"【已过期】{name} 截止 {e['deadline']} 已过 {-n} 天，仍在「{STAGE_CN[e['stage']]}」——确认有没有下一轮，否则标为结果（withdraw）。")
            elif n <= 1:
                when = "今天" if n == 0 else "明天"
                out.append(f"【{when}截止】{name} 截止 {e['deadline']}{note}，仍在「{STAGE_CN[e['stage']]}」，尽快提交。 {e['url']}")
            elif n in REMIND_DAYS:
                out.append(f"截止提醒：{name} 还有 {n} 天截止（{e['deadline']}{note}），当前「{STAGE_CN[e['stage']]}」。 {e['url']}")
        for c, d in pending_contacts(e, today):
            out.append(f"套磁跟进：{c['date']} 发给 {c['to']} 的邮件（{name}）已 {d} 天未回复，可以礼貌跟进一次；"
                       f"已回复请运行 reply {e['id']} --to \"{c['to']}\"。")
        iv = to_date(e.get("interview"))
        if iv and e["stage"] != "result" and 0 <= (iv - today).days <= INTERVIEW_DAYS:
            k = (iv - today).days
            when = "今天" if k == 0 else f"{k} 天后"
            out.append(f"面试准备：{name} 面试在{when}（{iv.isoformat()}）。清单：{INTERVIEW_CHECKLIST}。")
    return out


def changes(entries: list[dict], postings: list[dict], today: date) -> list[tuple[dict, str, dict | None]]:
    """看板里来自招聘平台的岗位，与最新 _data/postings.yml 对比：截止日期变了 → ("deadline", 新岗位)；
    截止前从平台消失（可能提前截止、招满或撤下）→ ("gone", None)。只看还在想投 / 准备中的条目。"""
    by_id = {_str(p.get("id")): p for p in postings}
    prefixes = {i.split(":", 1)[0] for i in by_id if ":" in i}
    out = []
    for e in entries:
        if e["stage"] not in ("want", "prep") or ":" not in e["id"] or e["id"].split(":", 1)[0] not in prefixes:
            continue
        p = by_id.get(e["id"])
        if p is None:
            n = days_left(e, today)
            if n is None or n >= 0:
                out.append((e, "gone", None))
        elif _str(p.get("deadline")) and _str(p.get("deadline")) != e["deadline"]:
            out.append((e, "deadline", p))
    return out


def change_lines(found: list[tuple[dict, str, dict | None]]) -> list[str]:
    out = []
    for e, kind, p in found:
        name = e["title"] or e["id"]
        if kind == "deadline":
            out.append(f"截止日期有变：{name} 平台上现在写 {_str(p.get('deadline'))}（原句：{_str(p.get('quote'))}），看板里是 {e['deadline']}。"
                       f"运行 sync 更新，并到官网确认。 {e['url']}")
        else:
            out.append(f"岗位已从平台下架：{name}（截止 {e['deadline']} 之前就不见了，可能已提前截止、招满或撤下），请到官网确认。 {e['url']}")
    return out


def sync(entries: list[dict], postings: list[dict], today: date) -> int:
    """把平台上更新过的截止日期写回看板（下架的不动，只提醒）。"""
    n = 0
    for e, kind, p in changes(entries, postings, today):
        if kind == "deadline":
            e["notes"] = (e.get("notes", "") + f"\n{today.isoformat()} 截止日期 {e['deadline']} → {_str(p.get('deadline'))}").strip()
            e["deadline"], e["deadline_note"] = _str(p.get("deadline")), _str(p.get("quote"))
            n += 1
    return n


def latest_ranking(dirs: list[Path]) -> Path | None:
    files = [f for d in dirs if d.is_dir() for f in d.glob("*.md")]
    return max(files, key=lambda f: (f.stat().st_mtime, f.name)) if files else None


def new_matches(entries: list[dict], today: date, profile: dict, rows: list[dict], seen: set[str], n: int = 10) -> list[dict]:
    """按画像排序（产品 C 的 rank.py，与网站“为我推荐”同一套规则），取不在看板、以前的摘要也没列过的前 n 条。"""
    sys.path.insert(0, str(ROOT / "scripts"))
    from rank import rank

    known = {e["id"] for e in entries} | {e.get("url") for e in entries}
    by_id = {x["id"]: x for x in rows}
    out = []
    for a in rank(rows, profile, today)["ranked"]:
        x = by_id[a["id"]]
        if a["id"] in known or x.get("u") in known or a["id"] in seen:
            continue
        out.append({"id": a["id"], "title": x["n"], "org": x.get("org", ""), "url": x["u"], "score": a["score"],
                    "deadline": (x.get("o") or {}).get("dl") or x.get("dl") or "", "why": (a.get("reasons") or [""])[0]})
        if len(out) >= n:
            break
    return out


def weekly(entries: list[dict], today: date, postings: list[dict] | None = None,
           ranking_dirs: list[Path] | None = None, matches: list[dict] | None = None) -> str:
    postings = load_postings() if postings is None else postings
    ranking_dirs = RANKING_DIRS if ranking_dirs is None else ranking_dirs
    L = [f"# 每周申请摘要（{today.isoformat()}）", "", "## 一、新匹配机会", ""]
    rk = latest_ranking(ranking_dirs)
    if matches is not None:
        L.append(f"按你的画像（profile.yml）排序、不在看板里、以前的摘要没列过的前 {len(matches)} 条（加入看板：`python scripts/track.py add <id>`）：")
        L.append("")
        L += [f"- [{m['title']}]({m['url']})" + (f" · {m['org']}" if m.get("org") else "") +
              f" · {m['score']} 分 · 截止 {m['deadline'] or '未写明'}" + (f" · {m['why']}" if m.get("why") else "") + f" `{m['id']}`"
              for m in matches] or ["- 本周没有新的匹配机会"]
    elif rk:
        links = [ln.strip() for ln in rk.read_text(encoding="utf-8").splitlines()
                 if re.search(r"\]\(https?://|https?://", ln)][:10]
        try:
            shown = rk.relative_to(ROOT)
        except ValueError:
            shown = rk
        L.append(f"最新排序结果 `{shown}` 前 {len(links)} 条：")
        L.append("")
        L += [ln if ln.startswith(("-", "*", "|")) or re.match(r"\d+\.", ln) else f"- {ln}" for ln in links]
    else:
        L.append("还没有排序结果，先运行 /rank 按你的画像排序岗位。")
    known = {e["id"] for e in entries} | {e["url"] for e in entries if e.get("url")}
    week_ago = today - timedelta(days=7)
    fresh = 0
    for p in postings:
        chk, dl = to_date(p.get("checked")), _str(p.get("deadline"))
        if not chk or not (week_ago <= chk <= today):
            continue
        if to_date(dl) and to_date(dl) < today:
            continue
        if _str(p.get("id")) in known or _str(p.get("url")) in known:
            continue
        fresh += 1
    L += [""] if matches is not None else ["", f"本周（{week_ago.isoformat()} 起）新核对、截止未过、且不在看板里的岗位：{fresh} 条。用 /rank 看哪些适合你。", ""]

    L += ["## 二、未来 14 天截止", ""]
    soon = [e for e in entries if e["stage"] != "result" and days_left(e, today) is not None and 0 <= days_left(e, today) <= 14]
    soon.sort(key=lambda e: days_left(e, today))
    L += [f"- {e['title'] or e['id']}" + (f" · {e['org']}" if e.get("org") else "") +
          f" · {deadline_text(e, today)} · {STAGE_CN[e['stage']]}" for e in soon] or ["- 无"]

    L += ["", "## 三、待跟进套磁", ""]
    fol = [(e, c, d) for e in entries for c, d in pending_contacts(e, today)]
    L += [f"- {c['to']}（{e['title'] or e['id']}）：{c['date']} 发出，已 {d} 天未回复" for e, c, d in fol] or ["- 无"]

    L += ["", "## 四、各阶段计数", ""]
    L += [f"- {STAGE_CN[s]}：{sum(1 for e in entries if e['stage'] == s)}" for s in STAGES]
    res = [r for r in RESULTS if any(e["stage"] == "result" and e.get("result") == r for e in entries)]
    if res:
        L.append("- 结果明细：" + "，".join(f"{RESULT_CN[r]} {sum(1 for e in entries if e.get('result') == r)}" for r in res))
    return "\n".join(L) + "\n"


def ics_escape(text: str) -> str:
    return (text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n"))


def fold(line: str) -> str:
    """按 RFC 5545 每行不超过 75 字节折行（不切断 UTF-8 字符）。"""
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def _event(uid: str, day: date, summary: str, desc: str, url: str, stamp: str, alarms=REMIND_DAYS) -> list[str]:
    ev = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}",
          f"DTSTART;VALUE=DATE:{day.strftime('%Y%m%d')}",
          f"DTEND;VALUE=DATE:{(day + timedelta(days=1)).strftime('%Y%m%d')}",
          f"SUMMARY:{ics_escape(summary)}", f"DESCRIPTION:{ics_escape(desc)}"]
    if url:
        ev.append(f"URL:{url}")
    for n in alarms:
        ev += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{ics_escape(summary)}",
               f"TRIGGER:-P{n}D", "END:VALARM"]
    ev.append("END:VEVENT")
    return ev


def ics(entries: list[dict], today: date) -> str:
    stamp = datetime.combine(today, datetime.min.time()).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PhDRadar//track//ZH", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", "X-WR-CALNAME:PhDRadar 申请截止"]
    for e in entries:
        if e["stage"] == "result":
            continue
        name = e["title"] or e["id"]
        org = f"（{e['org']}）" if e.get("org") else ""
        d = to_date(e.get("deadline"))
        if d and d >= today:
            desc = f"{name}{org}\n截止：{e['deadline']}" + (f"（{e['deadline_note']}）" if e.get("deadline_note") else "") + \
                   f"\n阶段：{STAGE_CN[e['stage']]}" + (f"\n{e['url']}" if e.get("url") else "")
            lines += _event(f"{e['id']}@phdradar", d, f"截止：{name}{org}", desc, e.get("url", ""), stamp)
        iv = to_date(e.get("interview"))
        if iv and iv >= today:
            desc = f"{name}{org} 面试\n准备：{INTERVIEW_CHECKLIST}" + (f"\n{e['url']}" if e.get("url") else "")
            lines += _event(f"{e['id']}-interview@phdradar", iv, f"面试：{name}{org}", desc, e.get("url", ""), stamp, alarms=(3, 1))
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(ln) for ln in lines) + "\r\n"


def import_site(entries: list[dict], data: dict, today: date, postings: list[dict] | None = None,
                sources: list[dict] | None = None) -> tuple[int, int]:
    """合并网站“我的收藏”导出的 {"saved":{...},"status":{...}}；返回（新增数，阶段更新数）。"""
    saved = data.get("saved") or {}
    status = data.get("status") or {}
    postings = load_postings() if postings is None else postings
    added = changed = 0
    for key in list(dict.fromkeys([*saved.keys(), *status.keys()])):
        if key in saved and not saved[key] and key not in status:
            continue
        e = find(entries, key)
        if e is None:
            found = lookup(key, postings, sources)
            base = found or {"id": key, "title": key, "org": "", "url": key if key.startswith("http") else "",
                             "deadline": "unknown"}
            e = normalize({**base, "stage": "want", "result": "", "contacts": [], "notes": "" if found else "网站收藏导入，未在目录中找到详情",
                           "history": [{"date": today.isoformat(), "stage": "want"}], "added": today.isoformat()})
            entries.append(e)
            added += 1
        st = status.get(key) or {}
        s = STAGE_ALIAS.get(_str(st.get("s")))
        r = _str(st.get("r")) if _str(st.get("r")) in RESULTS else ""
        if s and (s != e["stage"] or (s == "result" and r and r != e.get("result"))):
            t = _str(st.get("t"))
            cmd_stage(e, s, today, result=r if s == "result" else "", when=t if to_date(t) else "")
            changed += 1
    return added, changed


# ---------- 命令行 ----------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="申请追踪看板与提醒")
    ap.add_argument("--file", type=Path, default=TRACKER, help="看板文件（默认 applications/tracker.yml）")
    ap.add_argument("--today", help="覆盖今天的日期 YYYY-MM-DD（默认北京时间）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="添加岗位 / 信源到看板")
    a.add_argument("key", help="岗位或信源 id，或网址")
    for f in ("title", "org", "deadline", "url"):
        a.add_argument(f"--{f}", default="")
    s = sub.add_parser("stage", help="更新阶段（也接受 想投/准备中/已投/面试/结果）")
    s.add_argument("key")
    s.add_argument("stage")
    s.add_argument("--result", default="", help="offer | reject | withdraw")
    s.add_argument("--date", default="")
    s.add_argument("--interview", default="", help="面试日期 YYYY-MM-DD")
    c = sub.add_parser("contact", help="记录一次套磁")
    c.add_argument("key")
    c.add_argument("--to", required=True)
    c.add_argument("--date", default="")
    c.add_argument("--note", default="")
    r = sub.add_parser("reply", help="标记套磁已回复")
    r.add_argument("key")
    r.add_argument("--to", default="")
    sub.add_parser("board", help="输出 Markdown 看板")
    sub.add_parser("remind", help="输出今天的提醒")
    w = sub.add_parser("weekly", help="每周摘要")
    w.add_argument("--profile", help="画像文件（默认 profile.yml；存在时按画像列出新匹配机会）")
    w.add_argument("--out", type=Path)
    sub.add_parser("sync", help="把平台上更新过的截止日期写回看板")
    i = sub.add_parser("ics", help="导出截止日历 .ics")
    i.add_argument("--out", type=Path)
    im = sub.add_parser("import-site", help="导入网站“我的收藏”导出的 JSON")
    im.add_argument("json", type=Path)
    args = ap.parse_args(argv)

    if args.today:
        if not to_date(args.today):
            raise SystemExit("--today 要写成 YYYY-MM-DD。")
        today = to_date(args.today)
    else:
        today = beijing_today()
    path: Path = args.file
    entries = load_tracker(path)
    outdir = path.parent

    if args.cmd == "add":
        e, new = cmd_add(entries, args.key, today, args.title, args.org, args.deadline, args.url)
        if new:
            save_tracker(path, entries)
            print(f"已加入看板：{e['title']}（{e['id']}）· {deadline_text(e, today)}")
        else:
            print(f"看板里已有：{e['title']}（{e['id']}），未重复添加。")
    elif args.cmd == "stage":
        e = require(entries, args.key)
        cmd_stage(e, args.stage, today, args.result, args.date)
        if args.interview:
            if not to_date(args.interview):
                raise SystemExit("--interview 要写成 YYYY-MM-DD。")
            e["interview"] = args.interview
        save_tracker(path, entries)
        print(f"{e['title']}：阶段 → {STAGE_CN[e['stage']]}" + (f"（{RESULT_CN[e['result']]}）" if e.get("result") else ""))
    elif args.cmd == "contact":
        e = require(entries, args.key)
        cmd_contact(e, args.to, today, args.date, args.note)
        save_tracker(path, entries)
        print(f"已记录套磁：{args.to}（{e['title']}），{FOLLOW_UP_DAYS} 天未回复会提醒跟进。")
    elif args.cmd == "reply":
        e = require(entries, args.key)
        n = cmd_reply(e, args.to)
        save_tracker(path, entries)
        print(f"已标记 {n} 条套磁为已回复（{e['title']}）。")
    elif args.cmd == "board":
        print(board(entries, today), end="")
    elif args.cmd == "remind":
        items = remind(entries, today) + change_lines(changes(entries, load_postings(), today))
        print("\n".join(f"- {x}" for x in items) if items else f"今天（{today.isoformat()}）没有需要提醒的事。")
    elif args.cmd == "weekly":
        matches = None
        prof = Path(args.profile) if args.profile else ROOT / "profile.yml"
        cat = ROOT / "assets" / "catalog.json"
        if prof.exists() and cat.exists():
            seen_file = outdir / "weekly-seen.json"
            seen = set(json.loads(seen_file.read_text(encoding="utf-8"))) if seen_file.exists() else set()
            matches = new_matches(entries, today, yaml.safe_load(prof.read_text(encoding="utf-8")) or {},
                                  json.loads(cat.read_text(encoding="utf-8")), seen)
            seen_file.parent.mkdir(parents=True, exist_ok=True)
            seen_file.write_text(json.dumps(sorted(seen | {m["id"] for m in matches})), encoding="utf-8")
        text = weekly(entries, today, matches=matches)
        out = args.out or outdir / f"weekly-{today.isoformat()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(text, end="")
        print(f"\n已写入 {out}")
    elif args.cmd == "sync":
        n = sync(entries, load_postings(), today)
        save_tracker(path, entries)
        print(f"已更新 {n} 条截止日期。" + ("" if n else "（没有变化）"))
    elif args.cmd == "ics":
        text = ics(entries, today)
        out = args.out or outdir / "deadlines.ics"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(text.encode("utf-8"))
        print(f"已导出 {text.count('BEGIN:VEVENT')} 个日历事件 → {out}（导入手机或电脑日历即可收到提醒）")
    elif args.cmd == "import-site":
        data = json.loads(args.json.read_text(encoding="utf-8"))
        added, changed = import_site(entries, data, today)
        save_tracker(path, entries)
        print(f"网站收藏导入完成：新增 {added} 条，更新阶段 {changed} 条。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
