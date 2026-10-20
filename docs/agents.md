# 给 AI agent 用的接口

PhDRadar 的数据每天随网站一起生成一套静态 JSON，放在 GitHub Pages 上：只读、不用密钥、不用服务器。agent（Claude、GPT、自建的申请助手等）应该读这些文件，不要抓网页。

| 文件 | 内容 |
|---|---|
| [`llms.txt`](https://pingfanfan.github.io/PhDRadar/llms.txt) | 给大模型读的站点说明（[llms.txt 约定](https://llmstxt.org)） |
| [`api/v1/index.json`](https://pingfanfan.github.io/PhDRadar/api/v1/index.json) | 接口目录：版本、生成日期、条数、各端点、枚举值、地区与学科中文名、使用规则 |
| [`api/v1/opportunities.json`](https://pingfanfan.github.io/PhDRadar/api/v1/opportunities.json) | 现在可申请的机会，与首页“现在可申请”同一份，按截止日期排序 |
| [`api/v1/sources.json`](https://pingfanfan.github.io/PhDRadar/api/v1/sources.json) | 逐页核对过官网的信源：奖学金、博士项目、招聘平台等 |
| [`api/v1/schema.json`](https://pingfanfan.github.io/PhDRadar/api/v1/schema.json) | 两类记录的 JSON Schema |
| [`api/openapi.json`](https://pingfanfan.github.io/PhDRadar/api/openapi.json) | OpenAPI 3.1 描述，可直接导入成 agent 的工具（如 GPT Actions、各类 tool-calling 框架） |
| [`feeds/`](https://pingfanfan.github.io/PhDRadar/feeds/) | RSS：按学科、地区、中国学生可申等条件推送新机会 |

生成脚本是 `scripts/build_api.py`，由 `scripts/build_site.py` 调用，测试在 `tests/test_api.py`。

## 机会（opportunities.json 的 `items`）

| 字段 | 说明 |
|---|---|
| `id` | 稳定标识。招聘平台岗位是 `平台:编号`（如 `ajo:32802`），项目页是信源 id |
| `kind` | `posting`（招聘平台上的具体岗位）或 `programme`（项目、奖学金页） |
| `title` / `organization` | 标题与机构，保留原文 |
| `url` | **官网链接，以它为准** |
| `detail_url` | PhDRadar 上的这一条 |
| `regions` / `region_names_zh` | 地区代码（UK、DE、US、HK…）与中文名 |
| `levels` | `phd` / `postdoc` |
| `disciplines` | 学科代码，中文名见 index.json 的 `discipline_names_zh`；招聘平台岗位只按标题里的明确词归类，归不上就留空 |
| `funding_coverage` | `full` 全奖 · `salary` 带薪岗位 · `partial` · `tuition` · `stipend` · `varies` · `none` · `unknown` |
| `amount` | 金额，照官网原文 |
| `deadline` / `status` / `opens` | 截止（`YYYY-MM-DD` 或 `rolling` 等）、状态、即将开放的日期 |
| `cn_eligible` | 中国大陆学生能否申请：`yes` / `partial` / `check`（官网没写清）/ `no`。`no` 的不会出现在这里 |
| `evidence_quote` / `checked` | 核对时在官网上看到的原句与核对日期 |
| `first_seen` | 第一次出现在 PhDRadar 的日期，可用来找“新机会” |
| `intro_zh` | 中文简介 |
| `requirements` | 从公告原文摘出的申请须知，每项是 `{summary_zh, quote}`：`degree` 学位、`language` 语言、`start_date` 开始时间、`duration` 资助年限、`documents` 材料清单、`how_to_apply` 申请方式、`supervisor` 导师、`nationality_restriction` 身份限制。没列出的项目公告里没写 |
| `flags` | `security-screening`：公告提到出口管制、ATAS 或研究安全审查 |
| `platform` / `also_posted_at` | 岗位来源平台；同一岗位的其他发布地址 |

信源（sources.json）字段相同的部分含义一样，另有 `name_zh`、`requirements_zh`、`deadline_note_zh` 和 `open_now`。

## 使用规则

这几条也写在 `index.json` 的 `rules` 和 `llms.txt` 里，接入的 agent 必须遵守：

1. **引用原句、指回官网。** 每条都附了核对时的官网原句；给用户的结论要带上它，并请用户到 `url` 确认。
2. **不替用户猜资格。** `cn_eligible: check` 表示官网没写清，不能说成“可以申请”。
3. **截止以官网为准。** 时区没有统一换算；截止后机会会从 opportunities.json 消失。
4. **AI 起草，本人提交。** agent 可以排序、起草套磁信和文书，但每一份申请都由申请者本人检查并提交，不做批量自动投递。
5. **数据 CC BY 4.0。** 转载请注明 PhDRadar 并附官网链接。

## 典型用法

- **按画像筛选排序：** 读 opportunities.json，按 `levels`、`regions`、`funding_coverage`、`cn_eligible`、`requirements.degree` / `language` 做硬性筛选，再按研究方向匹配。仓库里的 `scripts/rank.py`（命令 `/rank`）就是这样做的，浏览器版在 `assets/rank.js`。
- **每天提醒新机会：** 比较 `first_seen`，或订阅对应的 RSS。
- **起草材料：** 用 `/apply` 生成申请清单与草稿，每条经历都要能在申请者自己的 `cv-facts.yml` 里找到。

## 以后的接入方式（规划）

- **MCP 服务器：** 把“搜索机会 / 查看详情 / 按画像排序”做成 MCP 工具，直接读上面的 JSON，让 Claude 等客户端开箱即用。
- **按地区、学科拆分的小文件**（如 `api/v1/opportunities/UK.json`）：数据变大后减少下载量。
- **变更记录：** 每天新增、下架了哪些机会，方便 agent 增量同步。
