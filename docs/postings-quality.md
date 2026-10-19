# 岗位数据质量抽检

首页“现在可申请”里的具体岗位（`_data/postings.yml`，由 `scripts/collect_postings.py` 从各招聘平台详情页自动提取）
要经得起点开官网对照。本文记录抽检方法、各平台各字段的错误率、按错误模式做的修正和修正后的复查结果。

## 方法

- **抽样**：从截止 ≥ 当天（或滚动招生）的岗位里按平台分层随机抽样（第一轮 300 条：FindAPhD 50、jobs.ac.uk 40、Nature Careers 35、
  THE Unijobs 30、AcademicTransfer 25、INSPIRE 25、Varbi 20、Jobbnorge 20、AJO 15、Science Careers 12、Inria 10、DAAD 10、
  Physics Today 6、ETH 2），包括判为“限本土”的条目，以便检查误判。
- **取原文**：用 `Fetcher`（遵守 robots.txt、限速）重新抓每条的官网详情页，存为纯文本（INSPIRE 取官方接口的岗位记录）。
- **逐条对照**：Sonnet 子代理按统一规则（`标题 / 机构 / 国家 / 层次 / 截止日期 / 截止原句 / 资助 / 中国学生资格 / 安全审查标记 / 简介`）
  对照页面原文判 ok / wrong / unsure，wrong 必须附页面原句。
- **准确率** = ok ÷（ok + wrong）；unsure 和无法读取的不计入分母，单独列出。

## 第一轮（2026-10-19，修正前）

可读页面 234 / 300 条：FindAPhD 对本环境和 WebFetch 都返回 403（50 条），Jobbnorge 详情页是脚本渲染的空壳、PDF 版被 robots.txt
禁止（16 条只能核对标题和机构）。

**字段准确率 96.4%（2279 个可判字段里 81 个错误）；所有字段都对的记录 170 / 234 = 72.6%。**

| 平台 | 样本 | 可读/打不开 | 标题 | 机构 | 国家 | 层次 | 截止 | 原句 | 资助 | 资格 | 安全审查 | 简介 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 全部 | 300 | 234/66 | 100% | 96%(10) | 96%(9) | 98%(4) | 92%(17) | 99%(2) | 96%(9) | 94%(13) | 95%(12) | 98%(5) |
| jobs.ac.uk | 40 | 40/0 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 89%(4) | 100% | 96%(1) |
| Nature Careers | 35 | 35/0 | 100% | 100% | 89%(4) | 100% | 91%(3) | 100% | 97%(1) | 94%(2) | 100% | 97%(1) |
| THE Unijobs | 30 | 30/0 | 100% | 100% | 100% | 100% | 96%(1) | 100% | 100% | 97%(1) | 100% | 100% |
| AcademicTransfer | 25 | 25/0 | 100% | 100% | 100% | 100% | 96%(1) | 100% | 100% | 100% | 100% | 100% |
| INSPIRE-HEP | 25 | 25/0 | 100% | 100% | 92%(2) | 96%(1) | 80%(4) | 100% | 79%(5) | 87%(3) | 100% | 96%(1) |
| Varbi | 20 | 20/0 | 100% | 89%(2) | 100% | 100% | 95%(1) | 95%(1) | 100% | 100% | 100% | 100% |
| Jobbnorge | 20 | 4/16 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 75%(1) | 25%(3) | 100% |
| Academic Jobs Online | 15 | 15/0 | 100% | 100% | 100% | 100% | 93%(1) | 100% | 100% | 100% | 100% | 100% |
| Science Careers | 12 | 12/0 | 100% | 92%(1) | 75%(3) | 91%(1) | 91%(1) | 100% | 100% | 100% | 100% | 91%(1) |
| Inria | 10 | 10/0 | 100% | 100% | 100% | 100% | 100% | 100% | 90%(1) | 100% | **10%(9)** | 100% |
| DAAD PhDGermany | 10 | 10/0 | 100% | **30%(7)** | 100% | 100% | 100% | 100% | 90%(1) | 89%(1) | 100% | 100% |
| Physics Today | 6 | 6/0 | 100% | 100% | 100% | 67%(2) | **17%(5)** | 83%(1) | 83%(1) | 83%(1) | 100% | 83%(1) |
| ETH Zurich | 2 | 2/0 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

括号里是错误数。FindAPhD 改用搜索官方 / 其他可读页面交叉核对：50 条里只找到 10 条可读版本，其中截止 1 处、简介 1 处不符
（简介照抄了 FindAPhD 模板占位符 “INSERT”），样本太少，不单独给准确率。

### 错误模式

| 模式 | 平台 | 例子 |
|---|---|---|
| 页头“Closing date”是广告下架日，正文另写申请截止 | Nature / Science Careers、Physics Today、THE、AcademicTransfer | 页头 23 Oct，正文 “Applications and letters are due November 1, 2026” |
| 结构化截止字段与正文不同，正文只写招满为止 | INSPIRE、AJO、THE | INSPIRE `deadline_date` 2026-12-15，正文 “will remain open until filled” |
| 法国 ZRR 国防安全审查没标 | Inria（9/10） | “This position is likely to be situated in a restricted area (ZRR)” |
| 机构名混入课题组和导师名 | DAAD（7/10） | “Leipzig University Molecular Nanophotonics Group … Frank Cichos” |
| 机构写成子域名缩写 | Varbi（全部 138 条） | “LU”“UU”“KI” |
| 国家留空 | Nature / Science Careers、INSPIRE | 地点 “Houston, TX”、JSON-LD 有 `addressCountry` 但没用 |
| 只付 Home 学费、国际生自付差额，仍判可申 | jobs.ac.uk | “International students must pay the difference between the Home and International tuition fees” |
| 页面写明任何国籍可申，仍判待确认 | Nature Careers、INSPIRE、DAAD、THE | “we welcome applications from any nationality” |
| 需美国公民的岗位没判限本土 | Physics Today / Science Careers（LBNL） | “DOE Q-level security clearance, which requires U.S. citizenship” |
| 竞争性奖学金的意向征集当成带资助岗位 | INSPIRE（JdC、FCT / la Caixa） | “welcomes expressions of interest … through the Juan de la Cierva fellowship program” |
| 资助尚未落实 | Inria | “Funding for this postdoc position has not yet been secured.” |
| 不是博士 / 博后岗位 | Physics Today（Turing 时薪远程合同工）、Science Careers（初级教职） | “Remote Chemistry Expert (PhD) … Pay rate: $100+/hour” |
| 跨平台重复没合并 | Nature ↔ Science Careers 等 | 同一岗位在两个平台截止日期不同，旧规则要求截止相同才合并 |

## 修正（2026-10-19）

`scripts/collect_postings.py`：

- **截止日期**：Madgex 系、INSPIRE、AJO、AcademicTransfer 用 `refine_deadline`——正文写了今天以后的申请截止就用正文（取最早一个，原句也换成正文原句）；
  正文没有任何截止日期、只写招满为止 / 滚动审核 → `rolling`；Inria 等机构页取所有截止句里最早的一个。截止关键词补了
  “applications are due”“full consideration … by”“no later than”“deadline for receipt of applications”。
- **中国学生资格**：各平台共用 `cn_of`（限本土 → no；写明任何国籍 / 国际生可申 → yes；否则 check）。限本土补了
  “国际生自付学费差额”“只限有 Home 学费资格者”“需美国公民”；jobs.ac.uk 页头标签只写 UK 但正文写按国际学费资助、
  或标签含国际生但只写 UK / Home 学费时改为待确认。
- **安全审查**：补法国 ZRR / PPST、瑞典《保护性安全法》、挪威安全法 / 出口管制、DOE Q 级许可。
- **资助**：排除竞争性奖学金意向征集、资助未落实、“more projects than funded opportunities”、时薪远程合同工；标题排除教职（faculty position 等）与 “Expert” 合同工。
- **机构 / 国家**：DAAD 取联系人栏第一段；Varbi 写学校全称；Madgex 用 JSON-LD 国家和美国州缩写补国家。
- **去重**：第二遍按“标题足够具体（去掉博后 / 研究员等泛词后 ≥ 3 个词）+ 机构一致 + 不同平台”合并，不再要求截止相同；保留截止最早的一条，其余链接进 `also`。
- **重采时清理**：页面读到了但按现行规则不再收录的旧岗位直接去掉（以前会一直保留到截止）。

`scripts/apply_intros.py`：简介里说“国际生 / 不限国籍可申”的，岗位 cn 必须是 yes；说“仅限本土”的必须是 no；博后不能写“全奖”；
不得含模板占位符；“面议”要有原文依据。`--recheck` 用现有岗位数据重查全部岗位简介，删掉不再通过的。

## 尚未解决

- **FindAPhD**（约 670 条，占岗位四分之一）只在公开仓库的 GitHub Actions 上能访问，本环境无法逐条对照原页；交叉核对只覆盖 10 / 50。
- **Jobbnorge** 详情页是脚本渲染、PDF 版被 robots.txt 禁止，只能用公开接口的标题、机构、截止日期；资格一律“待确认”，安全审查标记无法判断
  （抽到可读 PDF 的 4 条里 3 条有出口管制 / 背景审查句）。
