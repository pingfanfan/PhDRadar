"""适配器注册表。键必须与 _data/sources.yml 中的信源 id 一致。

未收录（2026-10 实测）：FindAPhD、ScholarshipDb 拦截脚本访问（403）；
Nature Careers 的 robots.txt 禁止抓取其 RSS。这些信源请在浏览器中订阅邮件提醒。

每个适配器是一个函数：fetch(fetcher, *, keywords: list[str], limit: int) -> list[Job]
"""
from __future__ import annotations

from . import (
    academictransfer,
    bluesky,
    daad_phdgermany,
    euraxess,
    inspire,
    jobbnorge,
    jobs_ac_uk,
    varbi,
)
from .feeds import make_feed_adapter

ADAPTERS = {
    m.SOURCE_ID: m.fetch
    for m in (academictransfer, bluesky, daad_phdgermany, euraxess, inspire, jobbnorge, jobs_ac_uk, varbi)
}

# Madgex 职位站共用 /jobsrss/ 接口；{q} 为搜索词
FEEDS = {
    "science-careers": "https://jobs.sciencecareers.org/jobsrss/?keywords={q}",
    "chemistry-world-jobs": "https://jobs.chemistryworld.com/jobsrss/?keywords={q}",
    "physics-today-jobs": "https://jobs.physicstoday.org/jobsrss/?keywords={q}",
    "agu-careers": "https://findajob.agu.org/jobsrss/?keywords={q}",
    "sfn-neurojobs": "https://neurojobs.sfn.org/jobsrss/?keywords={q}",
    "the-unijobs": "https://www.timeshighereducation.com/unijobs/jobsrss/?keywords={q}",
    # WordPress 职位板
    "cstheory-jobs": "https://cstheory-jobs.org/feed/",
    "jobrxiv": "https://jobrxiv.org/feed/?post_type=job_listing",
}
for _sid, _url in FEEDS.items():
    ADAPTERS[_sid] = make_feed_adapter(_sid, _url)
