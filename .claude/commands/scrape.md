---
description: 抓取最新带奖 PhD 岗位并按申请者情况筛选
argument-hint: [关键词，如 "machine learning, robotics"] [--sources a,b]
---

1. 解析 `$ARGUMENTS`：逗号分隔的关键词逐个转成 `-k`；如有 `--sources` 原样传入。
2. 运行 `python scripts/scrape.py --new-only <参数>`。若当前环境无法访问外网，改为提示用户在 GitHub Actions 中手动触发 `scrape` 工作流（可填 sources / keywords），然后读取仓库里的 `data/jobs.json`。
3. 阅读 `data/jobs.json`，向用户汇报：
   - 先列 `eligibility = international` 的岗位，再列 `unknown`，`restricted` 只给数量；
   - 每条给出标题、机构、国家、截止日期和链接，标出 `security-screening` 等风险；
   - 截止日期在 14 天内的单独提醒。
4. 列出抓取失败的信源，并建议是否需要修复。
