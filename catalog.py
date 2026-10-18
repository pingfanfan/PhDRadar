"""信源目录读取：_data/sources.yml（分类 + 主体条目）加上 _data/sources_extra/*.yml（各研究员追加的条目列表）。

多个研究员会话并行扩充信源时各写各的 extra 文件，避免同时追加同一文件造成冲突。
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "_data" / "sources.yml"
EXTRA_DIR = ROOT / "_data" / "sources_extra"


# ── 机会层面的结构化字段（可选；核实员逐条补全，供阅读页面与后续 agent 使用）──
# coverage：资助力度
COVERAGE = {
    "full": "全奖",            # 学费全免 + 生活费（或学费不收费的国家 + 足额津贴）
    "salary": "带薪岗位",       # 雇员合同/工资（欧洲博士岗、博后岗）
    "partial": "半奖/部分",     # 只覆盖部分学费或部分生活费
    "tuition": "仅免学费",
    "stipend": "仅生活费",
    "varies": "视项目而定",     # 门户、列表、各项目不同
    "none": "不提供资助",
    "unknown": "力度未注明",    # 已核实过但官方页面没写清楚，避免反复排队
}
# status：机会当前状态
STATUS = {
    "open": "🟢 开放申请",
    "upcoming": "🔜 即将开放",
    "closed": "⏸ 本轮已截止",   # 定期项目，本轮已截止，等下一轮
    "rolling": "🔄 随时可申",
    "ongoing": "📋 持续更新",    # 门户、职位库、名单类
}
# deadline：YYYY-MM-DD，或下面的关键字
DEADLINE_WORDS = {"rolling": "滚动", "varies": "各项目不同", "unknown": "未公布"}
OPPORTUNITY_FIELDS = ["coverage", "stipend", "deadline", "deadline_note", "status", "requirements"]


def extra_files() -> list[Path]:
    return sorted(EXTRA_DIR.glob("*.yml")) if EXTRA_DIR.exists() else []


def load_catalog() -> dict:
    """返回 {"categories": [...], "sources": [...]}，sources 已合并所有 extra 文件。"""
    data = yaml.safe_load(MAIN.read_text(encoding="utf-8"))
    for f in extra_files():
        data["sources"] += yaml.safe_load(f.read_text(encoding="utf-8")) or []
    for s in data["sources"]:  # 完整日期（verified、deadline）会被 YAML 解析成 date，统一转成字符串
        for key in ("verified", "deadline"):
            if isinstance(s.get(key), date):
                s[key] = s[key].isoformat()
    return data


def load_sources() -> list[dict]:
    return load_catalog()["sources"]
