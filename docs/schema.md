# 数据结构（供程序与 AI agent 使用）

所有信源都在 `_data/sources.yml` 与 `_data/sources_extra/*.yml`，合并后导出为
[`data/export/sources.json`](../data/export/sources.json) 与 [`sources.csv`](../data/export/sources.csv)（每天自动更新）。
后续的 `/rank`（按申请者画像打分）和 `/apply`（起草套磁信）都直接读这些字段。

## 一条信源 = 一个“机会入口”

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `id` | 字符串 | 唯一标识（kebab-case），永久不变，可作外键 |
| `name` | 字符串 | 机会 / 项目 / 平台名称（中文为主，括号内保留原名） |
| `url` | https 链接 | 官方页面，尽量直接指向博士/博后或带奖筛选页 |
| `category` | 枚举 | 信源类型，见 `sources.yml` 顶部 `categories`（聚合平台、政府奖学金、博士项目、博后 fellowship、导师招生帖…） |
| `levels` | 列表 | `phd` / `postdoc`（缺省视为 `[phd]`） |
| `regions` | 列表 | 国家/地区代码（ISO 两位，另有 `GLOBAL`、`EU`） |
| `disciplines` | 列表 | `all` `cs` `ai` `math` `physics` `chem` `bio` `eco` `neuro` `geo` `engineering` `social` `humanities` `econ` `business` `med` |
| `funding` | 枚举 | 资助**类型**：`position` 带薪岗位 · `scholarship` 奖学金 · `fellowship` · `mixed` · `info` 信息渠道 |
| `coverage` | 枚举，可空 | 资助**力度**：`full` 全奖（学费+生活费）· `salary` 带薪雇员合同 · `partial` 半奖/部分 · `tuition` 仅免学费 · `stipend` 仅生活费 · `varies` 视项目而定 · `none` 不资助 · `unknown` 已核实但官方未写明 |
| `stipend` | 文本，可空 | 金额原文，如 `€2,100/月（税后）`、`£20,780/年` |
| `deadline` | 日期或关键字，可空 | 当前或下一轮截止：`YYYY-MM-DD`，或 `rolling` 滚动 · `varies` 各项目不同 · `unknown` 未公布 |
| `deadline_note` | 文本，可空 | 截止规律与下一轮时间，如“每年 1 月中旬；2027 轮未公布” |
| `status` | 枚举，可空 | `open` 开放申请 · `upcoming` 即将开放 · `closed` 本轮已截止（定期项目）· `rolling` 随时可申 · `ongoing` 持续更新的门户/列表 |
| `requirements` | 文本，可空 | 国际生申请要求：学历、语言成绩、国籍/年限限制、是否需先联系导师 |
| `cn_eligible` | 枚举 | 中国大陆学生能否申请：`yes` / `partial`（部分渠道或名额受限）/ `check`（官方未写明，需核实）/ `no` |
| `access` | 列表 | 获取方式：`web` `rss` `email` `api` `login` `app` |
| `language` | 文本 | 页面语言 |
| `notes` | 文本 | 给中国申请者的实用说明（怎么筛、注意事项） |
| `verify_method` | `page` | 仅当核实员**打开了官方页面本身**并据正文核对过时为 `page`；缺省表示只基于搜索摘要，**不算已核实** |
| `page_evidence` | 字符串 | 页面上的一句原文（≤200 字），可在页面中检索到，用来支撑 `verify_method: page` |
| `verified` | 日期 | 最近一次核实日期（`YYYY-MM` 或 `YYYY-MM-DD`） |
| `feed` | 链接，可空 | 机器可读源（RSS/Atom、邮件列表归档、API） |

可空字段由核实员逐步补全；agent 使用时应把空值当作“未知”，不要推断。

## 使用建议

- **筛“现在能申请的全奖”**：`coverage in (full, salary)` 且 `status in (open, rolling)` 且 `cn_eligible in (yes, partial)`。
- **按截止排序**：`deadline` 为日期的优先，关键字放后；`closed` 的看 `deadline_note` 里的下一轮时间。
- **核实可信度**：`verified` 越新越可靠；`cn_eligible: check` 的条目在推荐给用户前应提示其自行确认。
- 链接可用性另见 [`reports/source-health.md`](../reports/source-health.md)（GitHub Actions 真实访问每个链接）。
