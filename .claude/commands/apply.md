---
description: 为选中的一个机会生成申请清单，起草套磁信、cover letter、研究计划要点与简历调整建议（每条经历都要能在 cv-facts.yml 找到）
argument-hint: <岗位 id 或官网链接> [补充要求，如 "强调 MCMC 经历，语气正式"]
---

原则：**AI 起草，本人修改和发送。** 文书里申请者的每条经历都必须来自 `cv-facts.yml`；申请目录 `applications/` 是申请者的私有数据，**绝不提交、不推送**（已在 `.gitignore`；如果 `git status` 里出现 `applications/` 或 `cv-facts.yml`，先停下提醒用户）。

## 0. 前提

- 找到申请者的事实文件：`profile/cv-facts.yml` 或仓库根目录 `cv-facts.yml`（由 `/setup` 生成；没有就请用户先运行 `/setup`，或按 `tests/fixtures/apply/lin-xiaozhou.yml` 的结构手写）。每个条目要有 `id`。
- 有画像 `profile.yml` 时读一下研究兴趣与偏好，用来决定强调哪些经历；画像里的说法不能当作事实写进文书，事实只来自 cv-facts。

## 1. 准备申请目录与申请清单

```bash
python scripts/apply_check.py prepare <岗位 id 或链接>
```

- 生成 `applications/<id>/`：`posting.yml`（岗位基本信息）、`posting.txt`（岗位原文）、`checklist.md`（从原文摘出的材料、推荐信数量、格式字数、截止时刻与时区、申请方式、开始时间、资格、资助与学费差额、联系人，每项都附原句）、`lab.yml`（待填）。
- 如果提示“网页没取到”（例如 FindAPhD 只对 GitHub Actions 开放），用 WebFetch 打开官网，把岗位正文原样保存为 `applications/<id>/posting.txt`，再运行一次 prepare。不要自己总结代替原文。
- 把 `checklist.md` 的要点告诉用户：缺哪些材料、要几封推荐信、截止时刻与时区、是否要先联系导师。原文没写的明确说“原文未写明”，不猜。

## 2. 导师与课题组（lab.yml）

- 导师姓名以岗位原文为准。查近期论文：`python scripts/apply_check.py papers "<导师姓名>" --affil "<机构关键词>"`（OpenAlex；失败时用网页搜索导师官方主页、Google Scholar、DBLP）。
- **确认是同一个人**（机构、方向一致）后，挑 2–4 篇近 3 年、与岗位课题最相关的论文写进 `lab.yml` 的 `papers`，每篇必须有能打开的链接（DOI 或官方页面）；`summary` 只写摘要里的原话或忠实转述。查不到就留空，套磁信改为只引用岗位原文 `[post]`。

## 3. 起草（子代理）

派一个子代理（model: sonnet），把 `research/apply-draft-prompt.md` 全文、`cv-facts.yml`、`posting.txt`、`checklist.md`、`lab.yml` 与用户的补充要求（`$ARGUMENTS` 里岗位 id 之后的部分）交给它，让它写 `drafts/email.md`、`drafts/cover-letter.md`、`drafts/research-plan.md`、`drafts/cv-advice.md`，并自己运行校验改到 0 错误。

## 4. 程序校验（硬性）

```bash
python scripts/apply_check.py check applications/<id>
```

- 逐句检查：经历句必须标 `[cv:…]`；数字、比值、机构 / 人名、论文题目、奖项名、网址都必须出现在所标出处里；出处 id 必须存在；占位符判错；空话只提醒。
- 有错误就把 `check-report.md` 交回起草子代理改（只能删改，不能用新事实“补”），直到 0 错误。**不要用 `--force` 跳过。**

## 5. 审稿（子代理）

另派一个子代理（model: sonnet，不要用起草的那个），给它 `research/apply-review-prompt.md`、`cv-facts.yml`、`lab.yml`、`posting.txt`、`checklist.md` 与 `drafts/`，让它写 `applications/<id>/review.md`。“必须改”里的问题交回起草子代理修改，再跑一次第 4 步。

程序和审稿是两层防线：程序拦下凭空出现的数字、名称、标题和“一作 / 已接收 / 主导 / 首次 / 被引用”这类说法；审稿子代理逐句对照出处，查程序看不出的张冠李戴、因果和夸大。想评估校验本身，可运行 `python scripts/apply_eval.py applications/<id>`（自动把合格文书改出编造变体，统计拦截率）。

## 6. 定稿草稿与交给用户

```bash
python scripts/apply_check.py clean applications/<id>     # 去掉出处标记 → final/
python scripts/track.py add <岗位 id> && python scripts/track.py stage <岗位 id> 准备中
```

向用户汇报（中文）：
- 申请清单要点与截止（附官网链接），推荐信要提前联系；
- `final/` 下四个文件的路径，套磁信全文贴出来；
- 审稿意见里仍需本人决定的地方、`cv-advice.md` 里列出的“缺口”；
- 提醒：**发送前请本人逐句读一遍并改成自己的话**；改好的版本放到 `applications/<id>/sent/` 同名文件，可运行 `python scripts/apply_check.py edit-ratio applications/<id>` 看修改比例（帮助我们评估初稿质量）；发出套磁后运行 `python scripts/track.py contact <id> --to "<导师>"`，10 天未回复会提醒跟进。
