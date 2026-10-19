# CLAUDE.md

本仓库是面向中国学生的「海外带奖 PhD / 博士后信源库」，后续将扩展为类似 ai-job-search 的 AI 辅助申请工作流。

## 产品形态（2026-10-19 起）

**公开站 PhDRadar（https://github.com/pingfanfan/PhDRadar ，网站 https://pingfanfan.github.io/PhDRadar/ ）是主产品**，所有最新进展都要反映到它上面。
本仓库只当后台：所有会话在这里工作，每小时由“PhDRadar 每小时同步”任务用 `scripts/make_public.py` 同步过去（只公开页面核对过的信源 `verify_method: page`、现在可申请清单与在招岗位；未核实条目、导师线索、收件箱不公开）。
本仓库自己的阅读页面、数据中台不再维护。

## 首要目标

**质量优先于数量**（仓库主人 2026-10-13 明确要求，优先级高于一切扩量任务）：宁可少收，也不收不确定的。
一条信源的价值在于读者点进去能确认“这个机会真实存在、资助是什么、截止何时、中国学生能不能申请”。

质量标准（每个会话、每个子代理都必须遵守）：
- **有依据才入库**：每条新信源必须带 `evidence`（搜索结果里看到的标题 + 链接）；没有依据的不收，`merge_sources.py` 会拒绝。
- **指向官方页面**：优先学校/研究所/资助机构的官方页；第三方转载、内容农场、付费中介、聚合站复制品不收；已有官方页时不收转载页。
- **不猜**：资助力度、金额、截止、国际生资格只写页面上看到的；看不到就留空或标 `'check'` / `unknown`。宁可留空，不要编。
- **过期就处理**：一次性岗位过了截止且没有下一轮 → 删除；定期项目本轮截止 → 保留并写下一轮时间。
- **不凑数**：子代理没有数量下限；找不到好的就少交，不要为了凑数收录弱条目。
- 发现错误（失效、过期、资格写错）比新增更重要，要优先修正。

其次才是扩大覆盖：持续收录带资助的博士与博士后信源（所有学科、所有国家），包括导师个人主页、邮件列表、院系招生页这类细粒度渠道——但必须满足上面的质量标准。

## 关键约定

- 信源数据在 `_data/sources.yml`（分类 + 主体条目）和 `_data/sources_extra/*.yml`（各研究员追加的条目列表），由 `catalog.py` 合并读取。
  阅读页面（`SOURCES.md` 总目录、`sources/` 下按分类/地区/学科的分页、README 中 STATS 区块、`docs/assets/` 首页 SVG 横幅与导航卡片）和 `data/export/` 数据集
  由巡检会话（每天）或 GitHub Actions（每 6 小时的 `sources` 工作流）统一生成（`scripts/build_sources.py` + `scripts/export_data.py`），不要手动编辑，研究员/核实员也不要提交这些文件。
  **Actions 免费额度有限**（私有仓库每月 2000 分钟）：私有仓库不再有定时工作流；sources / probe / postings / access 只在公开仓库 PhDRadar 上运行（公开仓库不计分钟数，用 `if: github.repository == 'pingfanfan/PhDRadar'` 限定），
  discover / scrape 只保留手动触发。不要新增在私有仓库定时或随推送运行的工作流。
- 字段含义见 `CONTRIBUTING.md`，完整数据结构（含 coverage/stipend/deadline/status/requirements 等机会字段，供 agent 使用）见 `docs/schema.md`。`cn_eligible` 和挪威地区代码 `'NO'` 必须加引号（YAML 布尔值陷阱）。
- 新增信源前先 `grep` 检查 URL/名称是否已存在；URL 必须是 https，并尽量指向 PhD/带奖筛选页。
- 不确定中国大陆学生能否申请时标 `'check'`，不要猜。政策类说明要能在官方页面找到出处。
- 面向用户的文字使用简体中文。

## 常用命令

```bash
python scripts/build_sources.py          # 校验 + 生成阅读页面
python scripts/export_data.py            # 导出 data/export/ 数据集
python scripts/build_dashboard.py        # 生成数据中台页面 dashboard/dist/index.html（发布为私密 Artifact）
python scripts/build_sources.py --validate-only  # 只校验数据（研究员提交前用这个）
python scripts/check_links.py            # 链接检查（需外网）
python -m pytest -q tests                # 抓取器离线测试
python scripts/scrape.py --list          # 列出抓取器
python scripts/probe_sources.py          # 真实核查信源 + 试跑抓取器（需外网）
```

## 抓取器

- 代码在 `scrapers/`，说明见 `scrapers/README.md`。适配器的 `SOURCE_ID` 必须是 `sources.yml` 中已有的 id（有测试保证）。
- 所有请求必须走 `Fetcher.get()`（robots.txt、限速、重试）。新增适配器要配离线样例测试。
- 云端/沙箱环境通常无法直接访问这些网站：推送后看 `probe-sources` 工作流的运行摘要，或读取 `reports/source-health.md`。

## 持续发现（长期自动运行）

- `scripts/discover.py`（每日岗位更新任务里在本地运行；私有仓库的 Actions 额度有限，不再定时跑）：轮换扫描 CSRankings 教授主页、Bluesky 招生帖作者、GitHub 新汇总仓库、AIOpenings 自填表、`_data/faculty.yml` 关注导师主页 → `data/discovery/*.json` 与 `reports/discovery.md`。
- `/research-sources k 6`（6 个研究员会话并行、各自每小时一轮）：按 `research/slices.yml` 分配切片派 Haiku 子代理搜索新信源，结果存 `research/inbox/`，经 `scripts/merge_sources.py --target worker-k` 去重写入各自的 extra 文件；产出少的切片不用硬凑数量；确实枯竭的切片才会被拆细或新建，用来覆盖尚未触及的国家、学科、平台。
  一轮对话内所有子代理共享 200 次网页搜索额度，所以每轮做 2 个研究切片 + 1 批核实。
- **不确定的信息要核实**：`scripts/verify_queue.py` 按“失效链接 → cn_eligible 'check' → 最久未核实”生成队列，
  核实子代理按 `research/verify-prompt.md` 给出 keep/update/delete 与证据，`scripts/apply_verification.py` 写回数据。
- **全量核实冲刺**：8 个专职核实员会话（`/verify-sources k 8 截止日期`，每小时一轮、每轮 4 个 Haiku 子代理共 80 条）按序号分片核实全部信源，分片清空后自动停用。
- 研究员与核实员会话每天轮换重开（`research/workers.yml` 记录当前会话与定时任务）。
- **每日岗位更新**（北京时间）：09:23 公开仓库 PhDRadar 的 `postings` 工作流用 `-s actions` 采集只对 GitHub Actions 开放的平台（`collect_postings.ACTIONS`，目前是 FindAPhD）；11:17 本地任务依次运行
  `collect_postings.py`（本地默认清单；新平台的适配器写在 `scripts/platforms_*.py`，自动注册）→ `import_postings.py`（一次并回 `ACTIONS` 里的全部平台）→ `discover.py`（在招导师线索）→ 为新岗位写简介（`research/intro-prompt.md` + `apply_intros.py`）→
  新岗位的申请须知字段（`enrich_postings.py fetch` → `bundle --dir D` → 每批派一个 Sonnet 子代理按 `research/enrich-prompt.md` 写 `D/out-*.yml` → `apply --dir D`，结果在 `_data/posting_fields.yml`）→
  `access_report.py`（平台接入状态与核对过信源能否打开，写 `docs/access.md`）→ `build_site.py` → 提交 → `make_public.py` 同步公开站。
- `/review-discoveries`：人工/Claude 审核自动发现的在招导师与候选信源。
- 所有自动任务都直接推送到 `main`，推送前务必 `git pull --rebase`。

## 路线图

完整规划见 `docs/roadmap.md`：数据底座（持续）→ 申请者画像 `/setup` → 匹配排序 `/rank` → 材料起草 `/apply` → 追踪提醒 `/track` → 半自动投递助手（只预填、本人提交）。
每个阶段有“做完的标准”；推进时从文末“近期待办”按顺序取，完成后更新该文档。申请者的画像与文书只存在本人那里，不进公开数据。
