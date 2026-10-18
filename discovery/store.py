"""发现结果的持久化：data/discovery/*.json，按 key 合并，记录首次/最近发现时间与审核状态。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "discovery"
STATUSES = {"new", "reviewed", "promoted", "rejected"}
# 第三方个人信息（帖子原文、个人简介、联系方式、帖子链接）只在本次运行内存中使用，不写入仓库。
PRIVATE_FIELDS = {"snippets", "bio", "contact", "evidence"}


def norm_url(url: str) -> str:
    """规范化 URL 用作去重键：小写域名、去 www、去 query/fragment 与末尾斜杠。"""
    p = urlparse(url.strip())
    host = p.netloc.lower().removeprefix("www.")
    path = re.sub(r"/(index\.html?)?$", "", p.path)
    return f"{host}{path}"


class Store:
    def __init__(self, name: str):
        self.path = DIR / f"{name}.json"
        self.items: dict[str, dict] = (
            json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        )
        self.added: list[str] = []

    def upsert(self, key: str, record: dict, channel: str) -> dict:
        today = date.today().isoformat()
        cur = self.items.get(key)
        if cur is None:
            cur = {**record, "channels": [channel], "first_seen": today, "last_seen": today, "status": "new"}
            self.items[key] = cur
            self.added.append(key)
        else:
            for k, v in record.items():
                if v not in (None, "", [], {}):
                    if k == "score":
                        cur[k] = max(cur.get(k, 0), v)
                    elif k == "snippets":
                        cur[k] = list(dict.fromkeys((cur.get(k) or []) + v))[:5]
                    else:
                        cur[k] = v
            if channel not in cur["channels"]:
                cur["channels"].append(channel)
            cur["last_seen"] = today
        return cur

    def save(self) -> None:
        DIR.mkdir(parents=True, exist_ok=True)
        items = {k: {f: v for f, v in r.items() if f not in PRIVATE_FIELDS} for k, r in self.items.items()}
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def known_source_urls() -> set[str]:
    from catalog import load_sources

    return {norm_url(s["url"]) for s in load_sources()}
