---
description: 申请追踪看板：想投 → 准备中 → 已投 → 面试 → 结果，提醒截止、套磁跟进与面试准备
argument-hint: [自然语言，如 "findaphd:195793 已投了" / "给 Prof. X 发了套磁" / "看看看板"]
---

看板数据在 `applications/tracker.yml`，是申请者的私有数据：**不要提交、不要推送、不要复制进公开数据**（`applications/` 应在 `.gitignore` 中；如果 `git status` 里出现了它，先停下提醒用户）。所有改动都通过 `python scripts/track.py` 完成，不要手改 YAML。

1. **每次先运行提醒**：`python scripts/track.py remind`，把输出原样转述给用户放在回复最前面（截止前 14 / 7 / 1 天、已过期但仍在想投/准备中、套磁 10 天未回复、3 天内的面试）。没有提醒就一句话带过。
2. **按 `$ARGUMENTS` 和用户的话更新看板**（id 可以是 `_data/postings.yml` 的岗位 id、信源 id 或网址）：
   - 收藏 / 想投：`python scripts/track.py add <id或网址>`；在目录里查不到时要补 `--title` 和 `--url`（可加 `--org`、`--deadline YYYY-MM-DD|rolling|unknown`）。截止日期只写官网上看到的，不确定就不填（记为 unknown）。
   - 换阶段：`python scripts/track.py stage <id> <想投|准备中|已投|面试|结果>`；结果要加 `--result offer|reject|withdraw`；补记过去的日期用 `--date YYYY-MM-DD`；约了面试加 `--interview YYYY-MM-DD`。
   - 套磁：`python scripts/track.py contact <id> --to "Prof. X" [--date YYYY-MM-DD] [--note "..."]`；收到回复：`python scripts/track.py reply <id> [--to "Prof. X"]`。
   - 看全部：`python scripts/track.py board`（五列 Markdown 看板，带截止剩余天数与待办）。
3. **网站收藏导入**：用户在 PhDRadar 网站上点的“收藏”和状态存在浏览器本地。让用户在网站页面打开浏览器控制台（F12 → Console），运行下面这一行，内容会复制到剪贴板，再粘贴保存成 JSON 文件（例如 `applications/site.json`）：

   ```js
   copy(JSON.stringify({saved:JSON.parse(localStorage['phdradar-saved']||'{}'),status:JSON.parse(localStorage['phdradar-status']||'{}')}))
   ```

   然后运行 `python scripts/track.py import-site applications/site.json`，岗位信息会用岗位库和信源目录自动补全。
4. **日历**：更新完截止日期后运行 `python scripts/track.py ics`，生成 `applications/deadlines.ics`（截止日全天事件，提前 14 / 7 / 1 天提醒；面试也会导出），建议用户导入手机或电脑日历，这样即使不打开本命令也不会错过截止。日期有变化时重新导出、重新导入。
5. **每周摘要**：建议每周运行一次 `python scripts/track.py weekly`（写入 `applications/weekly-YYYY-MM-DD.md`）：新匹配机会（有 `profile.yml` 时直接按画像用 `/rank` 同一套规则排序，列出不在看板、以前没列过的前 10 条；没有画像时读 `rankings/` 最新结果）、未来 14 天截止、待跟进套磁、各阶段计数。
6. 回复用户时用简体中文：先提醒，再说明这次改了什么，最后给出下一步最紧要的一两件事。不要替用户编造截止日期、导师回复或面试时间。
