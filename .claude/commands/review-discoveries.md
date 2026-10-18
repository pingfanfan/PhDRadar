---
description: 审核自动发现的在招导师和候选信源，把靠谱的加入关注名单或信源库
argument-hint: [数量，默认 20] [方向关键词，可选]
---

1. 读取 `data/discovery/faculty.json`，取 `status: new` 中 `score` 最高的若干条（`$ARGUMENTS` 指定数量与方向关键词）。
2. 逐个打开导师主页核实：
   - 是否明确在招博士生、招生年份是否为当前或下一申请季；
   - 是否提到资助（funded/stipend/RA/TA）以及是否对国际生开放；
   - 研究方向、所在机构与国家。
3. 处理结果：
   - 确认在招 → 加入 `_data/faculty.yml`（name、affiliation、homepage、openings_url、country、areas、added），并把该条 `status` 改为 `promoted`；
   - 证据不足但值得跟踪 → `status: reviewed`；
   - 误报（如“PhD from MIT”、已不招生） → `status: rejected`。
4. 同样审核 `data/discovery/sources.json` 中的候选信源，合格者按 CONTRIBUTING.md 规范加入 `_data/sources.yml`
   并运行 `python scripts/build_sources.py`，对应条目 `status: promoted`。
5. 运行 `python -m pytest -q tests`，提交并推送（先 `git pull --rebase`）。
6. 用中文汇总：新增关注导师（附主页）、加入的信源、拒绝原因分布。
