# /apply 端到端演示：3 个虚构申请者 × 3 个真实岗位

> 申请者的人物、学校、论文、成绩**全部是虚构的**（事实文件在 `tests/fixtures/apply/`）；岗位是 2026-10-19 网站上真实在招的岗位。
> 导师是岗位原文列出的真实老师，本文统一写作“［导师］”，不展示其姓名；演示生成的文书只存在本地 `applications/`（已在 `.gitignore`），没有发给任何人。

## 结论

| 指标 | 结果 |
| --- | --- |
| 端到端跑通 | 3 / 3 份申请：申请清单 → 导师论文 → 起草 → 程序校验 → 审稿 → 按审稿修改 → 再校验 → 定稿草稿 |
| 定稿草稿程序校验 | 13 个文件全部 0 错误、0 提醒 |
| 测试里的编造经历 | 27 条常见编造（改数字、编奖项、编机构、无出处经历句等）+ 14 条“只换说法不换事实词”的编造，全部被程序拦下（`tests/test_apply.py`） |
| **读过校验器源码的红队** | 子代理先读 `apply_check.py` 再专门写绕过它的编造 45 条：**第一版只拦下 8 条（18%）**；改成白名单规则后拦下 44 条（98%），15 条忠实句里 2 条被保守误报（见下） |
| 自动红队（`apply_eval.py`，对定稿草稿逐句造编造变体） | 345 / 348 拦下（99%）；剩下 3 条是中文句的出处互换和一句提问 |
| 审稿子代理 | 每份申请里藏 2 句程序当时查不出的编造（数字对调、凭空加职责、全称量词、把二作说成主导），**6 / 6 全部被审稿子代理指出**，另外还发现了多处真实问题 |

结论要说清楚：程序校验是规则，聪明的改写总能找到规则的缝隙——第一版就被读过源码的红队绕过了 82%。现在的做法是两层加一道人：
程序用白名单拦下“出处里没有的说法”（数字、名称、身份、角色动词、成果物、程度词），审稿子代理逐句对照查语义上的歪曲，最后申请者本人发送前通读。
在这次演示里，所有藏进去的编造都在这两层之一被拦下；但这不等于“任何编造都过不了”，红队评测要随规则一起持续跑。

## 三个虚构申请者与岗位

| 申请者（虚构） | 背景（虚构） | 岗位（真实） | 截止 |
| --- | --- | --- | --- |
| 林晓舟 | Northbridge University 统计学硕士，MCMC 调参硕士论文，1 篇在审论文 | [University of Birmingham · Monte Carlo Methods for Constrained and Aggregated Data](https://www.jobs.ac.uk/job/DTG436/phd-studentship-monte-carlo-methods-for-constrained-and-aggregated-data) | 2027-01-10 |
| 周沐阳 | Eastriver University of Technology 物理化学硕士，锂硫电池，一作 + 二作论文各 1 篇 | [University of Nottingham · Electrocatalysis of sulfur redox in the solid state](https://www.jobs.ac.uk/job/DTH265/phd-studentship-electrocatalysis-of-sulfur-redox-in-the-solid-state) | 2026-12-08 |
| 陈若溪 | Southbay Ocean University 海洋生物学学士，珊瑚热胁迫水族实验，水族馆志愿者 | [University of Essex · Promoting Coral Recovery After Bleaching Events](https://www.jobs.ac.uk/job/DTG070/phd-studentship-promoting-coral-recovery-after-bleaching-events-case-project-with-tropical-marine-centre) | 2026-12-16 |

三份事实文件用了两种格式：林晓舟是分节结构（education / publications / projects …），另两位是 `docs/profile-schema.md` 的 `facts` 列表（产品 C 的 `/setup` 输出），校验程序两种都能读。

## 流程与每一步看到了什么

### 1. 申请清单（`apply_check.py prepare`）

程序走 `Fetcher`（robots.txt、限速）取岗位正文，按规则摘原句，每项都附原文。以 Birmingham 岗位为例：

- 材料：CV、成绩单、**一页以内的陈述，说明对哪个 strand 感兴趣及原因**（原句："a short statement (no more than one page) saying which strand interests you and why"）
- 资格："a 2:1 four-year degree (or equivalent) in a mathematics-related subject"
- 资助：**"International students would need to cover the difference between the Home and International tuition fees themselves."**（对中国学生是关键信息）
- 开始时间 "September 2027"；推荐信数量与截止时刻原文没写 → 清单里明确写“原文未写明”，并提示按当地时间当天 00:00 前提交。

演示中改进：网页正文常把一句话拆成几行（标签与取值、括号里的邮箱），先并行再切句；“short statement (…) saying …”这类写法也算进陈述材料。

### 2. 导师与论文（`lab.yml`）

OpenAlex 在云端环境被限流（429），三个起草子代理都改用导师官方主页 + 网页搜索，只收能确认是同一个人、带 DOI 的论文：分别收了 1、2、2 篇；摘要没读到的论文要么不收，要么在 summary 里注明，套磁信里不引用。第二轮按审稿意见补了作者列表，确认导师是作者后才写 “your paper”。

### 3. 起草与程序校验

起草子代理按 `research/apply-draft-prompt.md` 写 4–5 个文件，每句经历都标出处。第一轮校验：

| 申请 | 第一轮错误 | 修改轮数 | 典型问题 |
| --- | --- | --- | --- |
| Birmingham | 14 | 1 | 出处 id 写错（awards.1 → award1）、计划里的编号与月份、“已接收”说法 |
| Nottingham | 10 | 1 | 称呼里的联合导师姓名没标 [post]、“第二位”被当成数字 |
| Essex | 4 | 1 | 计划时长、缩写 OCT |

误报都记录下来并改进了规则（缩写可由出处里连续词的首字母拼出、计划时长和中文序数不算事实、姓名与“如实说明缺口”的句子不算经历）。

### 4. 红队评测（`apply_eval.py`）——校验规则是这样一步步补全的

对通过校验的初稿，程序把每个带 [cv:…] 的句子改出 7 类编造变体，再跑校验：

| 轮次 | 拦截率 | 暴露的漏洞 → 补上的规则 |
| --- | --- | --- |
| 初版规则 | 89–95% | 少见动词的经历句（“I maintained… / I analyse… / 我操作过…”）没被识别；年份区间 2023–2024 改成 2024–2024 看不出；cv-facts 的元数据 `source:` 被当成出处 |
| 补规则后 | 96–99% | 出处张冠李戴（引用 A 却写 B 的内容）→ 加“句子内容与所引出处几乎不重合”检测 |
| 加“只换说法”的 14 条编造 | 10 / 14 → 14 / 14 | 被引用、被采用、首次、彻底消除、证明了、负责全部、从零独立完成、频率（每天 vs 每周两次）等说法都要在出处里有同义说法 |
| 定稿草稿 | 343 / 347（99%） | 剩下 4 条：3 条是中文句子的出处互换（中文转述英文事实，内容重合度算不出来）、1 条是提问句“只有基础共聚焦经验的申请者有竞争力吗”去掉出处——都交给审稿子代理 |

### 4b. 读过源码的红队——白名单是怎么来的

演示后另派一个子代理读完校验器源码，专门写骗过它的编造（每个虚构申请者 15 条，中英文都有），再写 15 条忠实句测误报：

- 第一版只拦下 8 / 45，而且其中 6 条是碰巧被别的规则拦下。漏掉的大多是**换个说法**：ran / coordinated / mentored / set up 代替 led，“is now in 期刊”代替 published，“on real regional data”（出处是合成数据），“released it as an open-source package”，“with distinction”，“two first-author papers”（一篇一作一篇二作），中文的“显著延长”“唯一操作者”“会议海报”“长期”“丰富”。
- 原因是规则是**黑名单**（列出“一作 / 已接收 / 主导”等说法），同义改写就绕过去了。
- 改法：经历句改成**白名单**——句子里的实词（动词、名词、修饰语）必须在所引出处里出现（按词干、同义词组和常见中英对应比对）；每段文字只能用紧跟它的那个出处（岗位里的说法要另标 `[post]`）；“两篇一作”这类计数要求每条出处都满足；非一作论文不能说“我的论文 / 我发现”；外加成果物、熟练程度、独占、程度词等说法须有出处。
- 结果：44 / 45 拦下。剩下 1 条（“作为持证潜水员完成了野外调查”，暗示证书在先）涉及时间先后，程序判断不了，交给审稿。误报 2 条都是保守的：出处只写了“L8 R8.5 W6.5 S7”，句子写“阅读 8.5、写作 6.5”；出处只写“R（lme4、ggplot2）”，句子写“用 R 做数据分析”。
- 代价：起草时必须贴着出处的原词写，转述多一层就会被拦，三份定稿草稿为此又改了 8 句。我们认为对申请文书这是值得的。

这 60 句都放进了 `tests/fixtures/apply/redteam.yml` 做回归测试。

### 5. 审稿子代理（程序之外的第二层）

每份申请复制一份，在 cover letter 里藏 2 句程序查不出的编造，交给另一个子代理按 `research/apply-review-prompt.md` 审稿（不告诉它藏了什么）：

| 藏进去的编造（均能通过程序校验） | 审稿结果 |
| --- | --- |
| “which I consider the leading journal for this work”（无依据的评价） | 指出：夸大 / 无出处 |
| “working alone rather than in a team”（出处是 3 人小组组长） | 指出：与出处矛盾 |
| “more than 200 coin cells, all of which kept 78%”（出处是 best cell） | 指出：把最好的一块写成全部 |
| “I was the lead researcher on … ChemElectroChem”（出处是二作） | 指出：没有主导的依据 |
| “12-week experiment in a 6-tank system”（出处是 6 周、12 缸，数字对调） | 指出：数字对调 |
| “trained new volunteers in coral fragment husbandry”（凭空加职责） | 指出：凭空添加 |

审稿还发现了不少真实问题，例如：Birmingham 的文书没有按原文要求说明选哪个 strand，且两份文书方向矛盾；“finishing an MSc” 与事实里 2026-06 结束不符；“This work led to a first-author paper” 是事实之间凭空加的因果；导师论文的结论被写强（“shows / govern”）；两份申请没有提醒国际生名额有限或只覆盖 Home 学费。这些都写进了起草与审稿提示词，所有修改记录在各申请的 `review-response.md`。

全称量词（“all of which”）这一条事后也补进了程序规则。

### 6. 定稿草稿（示例，已去掉出处标记）

**陈若溪 → Essex 套磁信（虚构申请者）**

> Subject: Question about the coral recovery PhD studentship (CASE, Tropical Marine Centre) for an international applicant
>
> Dear Dr ［导师］,
>
> My name is Chen Ruoxi, and I am writing about the PhD Studentship "Promoting Coral Recovery After Bleaching Events (CASE Project with Tropical Marine Centre)" at the University of Essex.
>
> The advert asks what makes corals more or less likely to recover after bleaching, using imaging and microsensors to study symbionts inside coral tissue. Your review "The role of host pigments in coral photobiology" discusses how host pigments may reshape the light field inside coral tissue, which relates to the optical methods in this project.
>
> My closest experience is a 6-week heat-stress experiment on Acropora and Pocillopora fragments in a 12-tank recirculating aquarium system, with photosynthetic efficiency measured by PAM fluorometry twice a week. I also assisted with daily water-quality checks and coral fragment husbandry as a volunteer at Southbay Public Aquarium.
>
> The advert says a limited number of studentships are available for international applicants; could you tell me how those places are decided? And would an applicant with only basic confocal microscopy experience be competitive?
>
> Best regards,
> Chen Ruoxi

**周沐阳 → Nottingham 套磁信（节选）**

> I recently completed an MSc in Physical Chemistry at Eastriver University of Technology, with a thesis on polyoxometalate-modified carbon hosts for lithium-sulfur battery cathodes. In that work I synthesised five polyoxometalate clusters, characterised them by XRD, XPS and cyclic voltammetry, and assembled and cycled more than 200 coin cells. I also operated an in situ Raman cell for solid-state electrodes. …
> The advert says the studentship covers fees at the Home rate, so I would also like to ask whether an international applicant can be considered.

**林晓舟 → Birmingham 一页陈述（节选）**

> The studentship has two strands: fusion methods under exact constraints, and optimal scaling in constrained domains. I would like to focus on the second, optimal scaling in constrained domains. … This is the setting of my MSc thesis at Northbridge University, "Adaptive tuning of Metropolis-adjusted Langevin algorithms on the probability simplex". … Diffusion-limit theory is something I would still need to learn during the PhD.

## 还没做到的

- **修改量 < 30% 的标准还没法评估**：需要真实申请者改稿后放到 `sent/`，用 `apply_check.py edit-ratio` 统计。演示里只能保证“初稿没有编造”，不能代表初稿写得好。
- 中文句子转述英文事实时，程序算不出内容是否对得上（出处互换只能靠审稿）；建议 cv-facts 同时保留中文 `text` 与英文 `quote`（产品 C 的格式就是这样）。
- 程序校验是基于规则的：白名单能拦下“出处里没有的说法”，但拦不住用出处原词拼出来的歪曲（例如把两条事实之间加上时间先后或因果）。审稿子代理和本人通读不能省；规则改了要重跑红队。
- OpenAlex 在云端被限流；在申请者自己的电脑上可设置 `OPENALEX_API_KEY` 后用 `apply_check.py papers`。

## 复现

```bash
python scripts/apply_check.py prepare jobs-ac-uk:DTG436
# 起草子代理按 research/apply-draft-prompt.md 写 applications/jobs-ac-uk-DTG436/drafts/*.md，并填 lab.yml
python scripts/apply_check.py check applications/jobs-ac-uk-DTG436 --facts tests/fixtures/apply/lin-xiaozhou.yml
python scripts/apply_eval.py applications/jobs-ac-uk-DTG436 --facts tests/fixtures/apply/lin-xiaozhou.yml
# 审稿子代理按 research/apply-review-prompt.md 写 review.md；按意见修改后再 check
python scripts/apply_check.py clean applications/jobs-ac-uk-DTG436 --facts tests/fixtures/apply/lin-xiaozhou.yml
```
