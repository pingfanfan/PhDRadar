# PhDRadar 长期路线图

目标：从“带奖博士 / 博后信息站”长成 **AI 辅助申请工作流**——像 ai-job-search 那样，帮申请者从海量机会里筛出真正适合自己的，准备材料、追踪进度、按时提醒。

产品有两种形态，共用同一份数据：

| 形态 | 给谁 | 能做什么 |
|---|---|---|
| **网站**（PhDRadar 页面） | 所有人，零门槛 | 浏览、筛选、收藏、日历提醒；填一份简短画像后按匹配度排序 |
| **Claude Code 工作流**（fork 仓库后在本地或云端会话里用） | 想要深度帮助的申请者 | `/setup` 建画像 → `/rank` 逐条打分并解释 → `/apply` 起草套磁信与文书 → `/track` 追踪与提醒 |

## 不变的原则

1. **质量优先**：每条机会都要能在官网找到原句；不确定就标“待确认”，不猜（见 CLAUDE.md）。
2. **申请者的数据只属于申请者**：画像、成绩、简历、文书只存在本人的浏览器或本人的私有仓库里，永不进公开数据、永不上传到我们这里。
3. **AI 起草，人来决定和提交**：投递这一步由申请者本人在官网完成。程序可以帮忙准备材料、预填表格，但不替人批量投递——各校申请系统要求本人账号与声明，批量投递也会伤害申请者在导师那里的印象。
4. **只用平台允许的方式取数据**：遵守 robots.txt 与访问频率；被拒绝就找官方接口、原始发布页或其他网络位置，不伪装、不破解。

## 现状（2026-10-19）

- 信源 6510 条，其中 2134 条逐页核对过官网；在招岗位约 2500 条，来自 16 个招聘平台（FindAPhD、jobs.ac.uk、Nature Careers、THE、AcademicTransfer、INSPIRE-HEP、Varbi、Jobbnorge、AJO、DAAD 等），跨平台去重。
- 每个岗位有：截止日期官网原句、资助对象/金额（写了才有）、中国学生资格（可申 / 待确认 / 限本土）、安全审查提醒、按标题归类的学科、申请者简介。
- 每天自动更新：FindAPhD 与可访问性检查在 GitHub Actions 上跑，其余平台在每日任务里跑，结果同步到公开站。
- 网站：搜索、筛选、截止日历、收藏、加入日历（.ics）。

## 阶段规划

每个阶段都有“做完的标准”，达到了才进下一阶段；数据底座（阶段 1）会一直持续。

### 阶段 1　数据底座：覆盖全、字段全、天天新（持续进行）

- **覆盖**：
  - 优先接入大学自己的招聘系统（Workday、SuccessFactors、各校职位页），把 EURAXESS / Academic Positions 等拒绝程序访问的平台上的岗位从源头拿回来。
  - 按国家补齐：德国（各大学 + 研究所 + 联邦劳动局开放接口）、法国、瑞士、北欧、荷兰、比利时、奥地利、新加坡、中国香港、澳大利亚。
- **字段**：从岗位原文结构化提取申请要用的信息，统一进 `docs/schema.md`：
  - 学位要求、语言要求（IELTS/TOEFL 分数）、开始时间、资助年限与金额
  - 国籍 / 学费身份限制、需提交的材料清单、申请方式（在线系统 / 邮件）、联系人、导师姓名与主页
  - 提取规则：只摘原文，每个字段附原句，取不到就留空。
- **可访问性**：`docs/access.md` 每天更新，目标是核对过的信源 99% 能打开；打不开的进入核实队列。
- **做完的标准**：在招岗位 ≥ 5000 条，覆盖 25 个以上国家；公告里写了的学位要求、语言、材料清单都抽到（每周抽检 20 个岗位，漏抽率 < 10%；公告本身没写的不算缺失。仓库主人 10-24 决定，原标准是“80% 的岗位三项都有”）；每日更新连续 30 天无中断。

### 阶段 2　申请者画像 `/setup`

- 画像文件 `profile.yml`（只在申请者自己的仓库或浏览器里）：
  - 学历、学校、GPA、专业、研究方向关键词与一段研究兴趣描述
  - 论文 / 项目、语言成绩、国籍、可接受的国家与城市、最低资助要求、入学时间
  - 是否涉及敏感学科（决定安全审查风险提示）
- Claude Code 命令 `/setup`：读申请者给的简历 PDF 或文字，对话补全，生成 `profile.yml` 与一份标准化简历要点 `cv-facts.yml`（之后所有文书只许用这里的事实）。
- 网站：一个“我的画像”小表单（存在浏览器本地），用于站内排序。
- **做完的标准**：从一份简历到可用画像不超过 10 分钟；画像字段能驱动阶段 3 的全部硬性筛选。

### 阶段 3　匹配与排序 `/rank`

- **硬性筛选**（不符合直接排除，并说明原因）：国籍 / 学费身份限制、学位要求、语言成绩、截止日期（来得及准备吗）、资助是否达到底线。
- **软性打分**（0–100，每项给出依据）：
  - 研究匹配度：画像研究兴趣 × 岗位描述，用向量相似度初筛，再由模型对前 N 条逐条判断并写一句理由。
  - 资助力度、截止紧迫度、语言与地区偏好。
  - 安全审查风险：公告提及 ATAS / 出口管制 / 知识安全审查，或学科属于敏感方向时降权并提醒。
  - 导师 / 课题组信号：主页是否在招、近期论文方向是否吻合。
- 输出：`rankings/<日期>.md`（前 30 条，每条三行理由 + 官网链接）；网站上“为我推荐”标签页按同样规则在浏览器里排序（轻量版，只用关键词与硬性条件）。
- **评测**：建一份 50 个虚构画像 × 人工标注“该不该推荐”的金标准，排序前 10 的准确率 ≥ 80% 才上线。
- **做完的标准**：申请者每周花 15 分钟就能看完新出现的、真正值得投的机会。

### 阶段 4　材料起草 `/apply`

- 对选中的一个机会：
  1. 生成**申请清单**（从原文提取所需材料、格式、字数、推荐信数量、截止时区）；
  2. 起草**套磁信**（写给导师：说明为什么是这个课题组，引用对方近期论文，并对应到自己的经历）；
  3. 起草 **cover letter / 研究计划要点 / 简历调整建议**。
- 事实约束：文书里的每一条经历都必须来自 `cv-facts.yml`；数字与成果逐条校验（沿用 `apply_intros.py` 的做法）。生成后再跑一遍“审稿人”检查：空话、夸大、与岗位不符之处。
- 输出到申请者自己的 `applications/<机会id>/`，申请者修改后自己发送 / 上传。
- **做完的标准**：申请者对初稿的平均修改量 < 30%；没有一条编造经历通过校验。

### 阶段 5　追踪与提醒 `/track`

- 申请看板：想投 → 准备中 → 已投 → 面试 → 结果，存在 `applications/tracker.yml`（网站版存浏览器本地）。
- 提醒：截止前 14 / 7 / 1 天；套磁后 10 天未回复提示跟进；面试准备清单。
- 每周摘要：新匹配的机会、即将截止的收藏、待跟进的套磁。
- 订阅渠道：先做 RSS / 邮件摘要（按画像筛过的岗位），再考虑 Telegram、微信公众号推送。
- **做完的标准**：用户不会因为忘了时间错过一个收藏过的截止日期。

### 阶段 6　半自动投递助手

- 在申请者自己的浏览器里，按画像和已定稿的材料**预填**大学申请系统的表格（浏览器扩展或 Claude in Chrome），每一步给申请者看，最后由本人确认提交。
- 只做预填，不保存申请者的账号密码，不绕过验证码，不批量提交。
- **做完的标准**：常见申请系统（例如 Workday、SuccessFactors、各校自建系统）预填后，申请者只需检查和上传。

## 横向工作（每个阶段都要做）

- **评测与质量**：每天抽检（现有的每日巡检），排序与文书各有金标准评测；所有数字都能追溯到原文。
- **隐私**：公开仓库只放公开信息；画像与文书模板默认写入 `.gitignore`。
- **成本**：长文本推理只用在前 N 条候选上；岗位的结构化提取一次完成后缓存，不重复花钱。
- **增长**：用数据洞察做内容（截止日历、薪资地图、资格避坑），见推广方案；收集用户反馈决定下一个要接入的平台。

## 近期待办（按顺序）

10-19 至 10-20 冲刺过（14 个云端会话并行，见 `research/workers.yml` 的 `sprint`），10-20 起为省额度全部停用。
10-21 起（仓库主人决定）由每日“路线图推进”任务按下面的顺序一项一项推进：每天只做一个能验证的增量，少派子代理。

1. 岗位结构化字段：学位、语言、材料清单、开始时间、资助年限（先覆盖 jobs.ac.uk、FindAPhD、AcademicTransfer、Varbi、DAAD）。
   - 进度（10-19）：`scripts/enrich_postings.py` 上线（读详情页 → 平台固定栏目规则 → Sonnet 子代理按 `research/enrich-prompt.md` 抽取 → 程序校验原句逐字在正文、数字只来自原句），结果在 `_data/posting_fields.yml`，首页详情页“申请须知”逐项可展开原句，卡片显示语言标签。
     可读取的 1575 个在招岗位全部处理完，68% 有学位/语言/材料至少两项（占全部在招 2160 条的 50%）；各字段命中率：学位 81%、材料 60%、年限 61%、申请方式 60%、开始时间 45%、语言 38%、导师 29%、身份限制 13%。
     准确率：独立 Sonnet 审核员抽查 112 个岗位 436 个字段，ok 418 / 小问题 17 / 错 1（已加 Inria 固定栏目规则修正）；人工抽查 20 个岗位全部准确。
     新平台（10-19 晚）：Workday / Oracle / 联邦劳动局读公开岗位接口正文，CNRS、SuccessFactors、哥本哈根、奥胡斯、MathJobs、EconJobMarket 等读页面；在招 2931 条中可读取的 2349 条 67% 有学位/语言/材料至少两项（占全部 54%）。
     新平台抽查：独立 Sonnet 审核员 100 个岗位 485 个字段，ok 466 / 小问题 19 / 错 0（小问题多为材料清单漏项、页面自身前后日期不一致）。CNRS 只有 35%：公告多不写语言与材料（统一在 CNRS 门户投递），非抽取遗漏。
     已知局限：数字校验无法区分 01/02/2027 的日月顺序，靠子代理按所在国写法判断。
     未覆盖：FindAPhD（455 条，本机被拦，只有 Actions 能访问）；jobs.ac.uk 公告多把要求放在附件 PDF，覆盖只有 25%。
   - 10-22：接入 Jobbnorge（132 条）：详情页靠脚本渲染，改读页面自己加载的公告 JSON（`id.jobbnorge.no/api/joblisting`，robots 未限制、无需登录；有英文版用英文版，只有挪威语版的退回挪威语，原句保留原文）。125 条读到正文，5 个 Sonnet 子代理抽取后程序校验通过 616 个字段（14 个因原句或数字不符丢弃），Jobbnorge 有学位/语言/材料至少两项的 114 条（86%）；全部在招岗位升到 52%（占可读取 60%）。人工抽看 3 条原句与公告一致。下一步：FindAPhD（只有 Actions 能访问，考虑在 Actions 里只做规则提取并缓存正文）或 jobs.ac.uk 附件。
   - 10-22：FindAPhD 接入：Actions 采集时用 `collect_postings.py --save-texts` 把公告正文存为附件（7 天，不提交），本地 `enrich_postings.py import-texts` 导入后照常抽取；10-23 首批 85 条有申请须知，其余随每日任务补完。补抽 477 个积压岗位后全部在招 63%。
   - 10-23：读取失败的岗位里网络类错误（ConnectionError / Timeout / 5xx）改为第二天就重试，其余仍隔 7 天（香港理大 15 条因此从 0 恢复）。
     现状分析：模型已读过的 2844 个岗位里，有学位/语言/材料至少两项的按平台差别很大——北欧、荷兰、德国与各校招聘系统 85–99%，jobs.ac.uk 32%、CNRS 37%、FindAPhD 36%、INSPIRE 62%。差的原因是公告本身不写：英国 / 美国岗位几乎不写语言要求（jobs.ac.uk 只有 8% 写了），CNRS 统一在门户投递、公告不列材料；jobs.ac.uk 的附件（/enhanced/fp/）被 robots.txt 禁止，不读。
     因此“80% 的岗位三项都有”在公告不写的平台上达不到；10-24 仓库主人同意改为“公告里写了的都抽到”（按抽检衡量漏抽率）。
2. 接入大学招聘系统：先做 Workday 与 SuccessFactors 的通用适配器，再按国家列出高价值学校。
   - 10-19：`scripts/ats.py`（经 `platforms_ats.py` 注册，已在本地默认清单）接入 6 类：Workday（24 个站点：Aalto、NTU、NUS、悉尼、墨尔本、Monash、UQ、UBC、McGill 等）、SuccessFactors（12 所：EPFL、TU Delft、维也纳、赫尔辛基、根特、巴塞尔、FU Berlin、NUS 等）、Oracle Recruiting（DTU、SDU）、PageUp（港大、La Trobe）、ReachMee（Chalmers）、学校自建招聘页（哥本哈根大学）。首轮收录 289 条（Oracle 93、SuccessFactors 125、Workday 52、哥本哈根 36、Chalmers 18）。截止日期只取正文原句（数字日期按同页写法判断日月顺序，判断不了不收）；PageUp 访问稍快就弹 AWS WAF 验证，目前被拦，不绕过。
   - 10-20：扩到约 80 个学校 / 研究机构入口：Workday 25、SuccessFactors 17（加多伦多、Fraunhofer、A*STAR、CSIRO）、Oracle 4（加爱丁堡、阿尔伯塔）、ReachMee 1，以及 34 个学校自建招聘页（理大、剑桥、ANU、RWTH、TUM、LMU、汉堡、于利希、KIT、DKFZ、PSI/Eawag/Empa/WSL、苏黎世大学、Leibniz、HZDR、TU Berlin、奥尔堡、奥卢、安特卫普、CBS、塔尔图、SISSA、巴斯德、IRB、IIT、INRAE、博洛尼亚等；列表页、表格行、站点地图或 RSS/Atom）。第二轮采集 546 条（去重后在库 476 条）。新规则：德语 WiMi 岗位按正文判断博士 / 博后；法 / 意 / 西月份；学校自己的页面（非美加）数字日期默认 日/月/年。不接入：robots 禁止（UNIL、海德堡、TU Graz / Uni Graz、阿德莱德 / 塔斯马尼亚、帝国理工 / 布里斯托的 TalentLink、奥克兰接口、Tampere 明确拒绝 AI 爬虫）；人机验证拦截（PageUp 各校、牛津、城大、SMU、OIST、USI、HU Berlin、卢森堡大学、Maynooth）；只能表单 POST（爱尔兰 CoreHR 各校）。
   - 10-24：Workday 维护时（接口跳到 “Workday is currently unavailable” 页）详情返回的不是 JSON：采集改为记“详情页失败”保留旧记录，不再误当成岗位下架删掉；申请须知读取遇到这类错误第二天就重试。
3. 全部信源用更强的模型重新核实一遍（失效 → 资格待核实 → 缺字段 → 最久未核实）。
4. `profile.yml` 结构与 `/setup` 命令；`/rank` 硬性筛选 + 关键词匹配版；网站“为我推荐”。
   - 10-19：画像结构 `docs/profile-schema.md` + `profile.example.yml`（真实画像、简历要点、排序结果写进 .gitignore）；`/setup`、`/rank` 命令；
     `scripts/rank.py`（硬性筛选写明原因 + 0–100 打分 + 三行理由）与浏览器版 `assets/rank.js` 共用 `scripts/rank_rules.py`（中英文同义词表 117 组），
     `tests/test_rank.py` 用构造画像验证筛选与排序，并在全部现在可申请的岗位上核对两边结果一致。
   - 10-19：评测 `docs/rank-eval.md`（`scripts/rank_eval.py`，画像与人工标注在 `tests/rank_eval_*.yml`）：20 个调规则画像前 10 准确率 81%，
     10 个留出画像 74%（第二组写完后不再改规则：79%）。规则改为只推荐命中关键词的机会、同义词与更窄的词分开、学科冲突丢弃、方法类词用在别的学科打折等 11 项。
   - 10-19：网站“为我推荐”标签页（`#rec`）：关键词、层次、学历、最低资助、截止准备期、雅思 / 托福 / 德语、国家偏好、只看中国学生可申、敏感方向；
     画像只存 localStorage（`phdradar-profile`），浏览器里用 `assets/rank.js` 按与 `/rank` 相同的规则排序，卡片写明匹配分、命中的关键词与条件，学科相同但未命中关键词的单列为“相关性较弱”。
5. 根据 GitHub Actions 上的可访问性结果，把只在 Actions 上能访问的信源和平台改在 Actions 上采集；研究德国联邦劳动局开放接口当前的访问方式。
   - 10-19：`collect_postings.py -s actions` 采集 `ACTIONS` 清单（只有 Actions 能访问的平台，目前 FindAPhD），postings 工作流默认用它；`import_postings.py` 默认一次并回清单里全部平台（逐平台比较采集时间）。
   - 10-19：德国联邦劳动局 Jobsuche 接入（`scripts/platforms_de.py`，适配器 `arbeitsagentur`）：bund.dev 文档公开的通用 clientId（请求头 `X-API-Key: jobboerse-jobsuche`，无需 OAuth/申请），旧版 `/pc/v4/jobs` 已 403，改用 `/pc/v6/jobs` + `/pc/v4/jobdetails`；截止日期只从描述原文取（Bewerbungsfrist / 带申请语境的 bis zum，排除合同期），抽样 70 条收 41 条。新平台统一写在 `scripts/platforms_*.py`，collect_postings 自动注册（ADAPTERS / HEADERS / VIA_RANK）。
   - 10-19：新平台（先查 robots.txt、确认截止日期能取到原文）：CNRS Emploi（博士合同 + 研究员 CDD，试跑 243 条）、MathJobs（51）、TAMU 自然资源招聘板（111）、Aarhus University（27）、H-Net（本环境 429，待日常任务验证）、PSI / ESO / IBS（机构招聘页通用适配器）；已加入本地默认清单。调研后不接入：ADUM / APS / HiBrain（robots 全站禁止）、JREC-IN（条款要求转载先获 JST 许可）、PhilJobs / AEA JOE（条款禁止入库或抓取）、Helmholtz（门户无截止日期）、AAS / SIAM / IEEE / ACM / AGU（Cloudflare 拦截）；各校 Workday / SuccessFactors / PageUp 等交给工程 B。
   - 10-19 晚：首轮并入 617 条（CNRS 244、劳动局 119、TAMU 111、MathJobs 49、EconJobMarket 43、Aarhus 27、INFN 9、Pasteur 5、PSI/ESO/IBS 10）。再调研后不接入或暂缓：SISSA（“Open”状态不更新，现无在招博后）、CRG（现无研究型博后）、ICFO / CSIC / CNR（页面无截止日期或只在 PDF）、University Affairs（多为 open until filled）、HigherEdJobs / AcademicKeys / BSC / 卢森堡大学（人机验证拦截）、Chemistry World 与 NeuroJobs（几乎无博士博后或被拦）；法国公务员招聘门户 choisirleservicepublic.gouv.fr 可用但每页 4.5MB、博后占比低，留作候选。
   - 10-20：接入 FAPESP Oportunidades（巴西圣保罗州研究基金会博士/博后奖学金，首轮 51 条，奖学金额取页面原文）与 LINGUIST List（语言学 RSS，9 条）。调研后暂缓：RIKEN（90 个岗位只有 5 个写日期）、EvolDir（邮件列表自由文本、多为其他平台转帖）、巴塞尔大学（Prospective 招聘系统，可见截止只占 7/12，交给工程 B）、KAUST / MBZUAI / ASA（招聘系统或只有 validThrough）、IMS / SCB（人机验证）。不允许程序访问的平台已补进 `research/outreach.md` 的数据合作申请草稿（JREC-IN、ADUM、PhilJobs、AEA JOE、HiBrain）。
   - 10-20：接入 EGU Jobs（地球科学，结构化截止与薪资字段，16 条）、FENS Job Market（神经科学，40 条；字段写日期但正文说“no deadline”的不收）、ELLIS Jobs（AI，8 条）、因斯布鲁克大学招聘门户（今日无在期岗位）。暂缓：KIAS（详情要过同意页、列表与公告页对不上）、Quantiki（用户自发帖，常写“funded and unfunded”）、ICTP（仅 2 个在期征集，适合作为信源条目）、博洛尼亚大学 bandi（薪资只在 PDF）；TU Graz / Uni Graz（robots 全站禁止）、TU Wien / Uni Wien / Fraunhofer / Tyndall（招聘系统）、澳门大学（无截止日期）。
   - 10-24 起（仓库主人同意）：被拦或条款不允许的平台，逐个找**合规**的接入方式，不伪装、不破解人机验证、不违反 robots.txt 与条款。顺序：
     ① 找岗位的原始出处——学校 / 研究所自己的招聘页、RSS、站点地图（先做 PageUp 拦住的港大、La Trobe，牛津、城大等）；
     ② 平台允许的订阅渠道——RSS、邮件提醒、公开检索订阅（JREC-IN、H-Net 等），并按对方限速（H-Net 的 429 说明我们太快）；
     ③ 官方接口 / 数据合作——`research/outreach.md` 的申请草稿由仓库主人本人发出，有回复后再对接。
     每个平台做完在这里记一行：用了哪个渠道、收录多少、robots / 条款依据。
     - 10-25 港大 / La Trobe（PageUp）：robots.txt 允许 `/en/listing/`，放慢到每 15 秒一次后单次能打开列表（402 个链接），但连续访问仍弹 AWS WAF 人机验证（列表页与详情页都会）；港大 HR 站 `hr.hku.hk/career_opportunities/` 返回 403、RSS 也被验证拦住。结论：程序访问不被欢迎，停在这里不绕过；适配器保留 15 秒间隔，列表页被拦时报“被拦截”而不是“没有岗位”。港大的博士资助已由信源覆盖（HKPFS / 研究生院、数学、物理、理学院），博后岗位等数据合作（已列入 `research/outreach.md` 候选）。
     - 10-26 H-Net Job Guide：招聘指南已迁到 jobs.h-net.org（旧 networks.h-net.org/jobs 返回 404），岗位列表仍在 networks.h-net.org/jobs/browse；robots.txt 允许、要求 Crawl-delay 5，招聘指南条款写明公告“供公开发布”。连续 429 的原因是我们自己：取 robots.txt 后紧接着就发第一个请求、没按 Crawl-delay 等。已修正抓取器（取 robots.txt 也计入访问间隔；429 无 Retry-After 时退避 30 / 60 秒，对所有平台生效），H-Net 放慢到每 20 秒一次、翻页中途被拒时保留已拿到的页。当天几次试探触发了对方限流，未能拿到实测收录数，留给次日例行采集验证。
     - 10-27 FindAPhD：10-26、10-27 两天 GitHub Actions 采集都被拒（403），现在整站连 robots.txt 都要先过 Cloudflare 人机验证，属于明确拦截，停止访问。① 原始出处：FindAPhD 的项目大多来自英国高校与博士培训项目，jobs.ac.uk（每天约 460 条）和学校自建招聘页已覆盖一部分，无法一对一替代；② 平台的邮件提醒需要本人注册账号、接收邮件，不能自动化；③ 已并入 research/outreach.md 的数据合作名单（与 FindAPostdoc 一起申请）。另外修正了“采不到也显示成功”：collect_postings.py 新增 --fail-if-none，postings 工作流加 pipefail，所列平台一条都没读到时工作流显示失败。H-Net 10-27 例行采集已恢复收录（8 条）。
     - 10-28 FindAPhD ① 原始出处（续）：核对 709 条 FindAPhD 岗位，与库内其他平台按标题只重合 9 条；但发布方集中，前 40 家机构占 85%，可以逐家回到官方页。今天从最大的华威（89 条）开始：其中大部分是 MIBTP（BBSRC 生物科学博士培训项目）的课题，官方页（robots.txt 只禁 /training/ 等路径，允许访问）四个主题页加 CASE 页共列出 403 个课题，但名额有限（如 Rules of Life 主题每年 13 个），国际生最多占 30% 名额，且 UKRI 不补国际学费差额。按本库岗位规则（竞争性资助不按单个岗位收、国际生自付学费差额算限本土），这类课题不逐条收，改在项目级信源里写清楚：更新 mibtp-bbsrc-dtp（截止 2026-11-23、资格、学费差额、签证费，依据官方申请页原句），删除重复条目 warwick-mibtp-bbsrc-phd。下一步按同样方法逐家看 Crick、Imperial、Oxford 等，有逐个岗位招聘页的接适配器，属于培训项目的在项目级信源里写清楚。
     - 10-28（用户决定）：① 平台岗位超过 7 天没能重新核对就自动下架（build_site.py 的 STALE_DAYS，重新核对到就回来）；FindAPhD 停在 10-25 的岗位将在 11-02 起下架。② FindAPhD 上 UKRI 博士培训项目（DTP / CDT）的课题不再凭平台的“Students Worldwide”标签算中国学生可申，改为待确认（采集规则 UKRI_TRAINING）；现有数据按正文与 MIBTP 官方课题名改了 187 条。用户提议通过其本地电脑上的 agent 获取 FindAPhD，属于绕过 Cloudflare 拦截，不做。
     - 10-29 FindAPhD ① 原始出处：Francis Crick Institute（FindAPhD 上 36 条，全部写明国际生可申）。官方“PhD student positions”列表（robots.txt 只禁 /admin/、/search/、/user/ 等，允许访问）列出 2027 年 26 个博士课题，课题页写“Application close date 03 November 2026, 12:00 GMT”；资助与资格取自招生总页原句（所有国籍可申；学费含国际生；£27,715 免税生活费 × 4 年），对全部课题适用，个别课题另有限制时按课题页判断。新适配器 scripts/platforms_uk.py（crick，已加入默认采集清单），首次收录 26 条，其中 25 条与 FindAPhD 记录合并。顺带修了跨平台去重：截止更早的那条若比组里最新核对的晚 7 天以上没再核对到（如被拦的 FindAPhD），不再优先保留，免得它 7 天后下架时把仍在招的官方岗位一起下架。
     - 10-30 FindAPhD ① 原始出处：Imperial（FindAPhD 上 35 条）。其中 22 条是化学工程系“PhD Scholarship project”，官方奖学金页（robots.txt 只禁 /search/、/campaigns/ 等，允许访问）写明这是系内竞争性奖学金：至多 15 个名额（10 个不限学费身份、5 个只给 Home 学生），三轮选拔 2026-11-02 / 2027-01-11 / 2027-03-01，课题按导师列出、多于名额。按本库规则（竞争性资助不按单个课题收）在项目级信源里写清楚：合并重复的两条（worker-3 与 worker-6 指向同一页），截止按官网改为 11-02（旧记录写 11-01），同步改“现在可申请”清单。其余约 13 条散在生物工程、物理、机械等系，各系页面格式不同，留待逐个看。下一步：CRG（西班牙，18 条）。
     - 10-31 FindAPhD ① 原始出处：CRG（巴塞罗那，FindAPhD 上 18 条，全部写明国际生可申）。官方“CRG International PhD Programme 2027”页面（robots.txt 只禁 /admin/、/search/、/user/ 等，Crawl-delay 10，Fetcher 自动遵守）是一年一次的统一招生：截止 2026-11-22，所有国籍可申，一次申请选两个课题组，录取者签 4 年劳动合同。FindAPhD 上那 18 条就是这次统一招生里各课题组的介绍，属于同一个项目，所以不逐条收，在项目级信源里写清楚：合并重复的两条（crg-intl-phd 仍写着“已关闭”，已删），资格、合同、面试日程按官网原句写，同步改“现在可申请”清单与简介。下一步：Princess Máxima Center（荷兰，15 条）。
     - 11-01 FindAPhD ① 原始出处：Princess Máxima Center（15 条）已于 10-31 全部截止、自动下架，无需处理。改做西交利物浦大学（XJTLU，14 条，全部“招满为止”）：官方 Postgraduate Research Scholarships 页（robots.txt 全部允许）写明奖学金三档（全额 = 三年免学费 + 每月 RMB 5,000，只免学费，最多减半学费），并按学院列出已有经费的在招课题、招满为止。这些课题没有截止日期、且同属一个奖学金计划，在项目级信源里写清楚：原条目指向 2026 招生手册 PDF，改为指向这个在线页面，奖学金档次与课题列表按页面原句写，简介同步修正（原简介说“需先找到导师”，页面写的是可直接申请列出的课题）。下一步：MRC LMS（11 条）。
     - 11-02 FindAPhD ① 原始出处：MRC Laboratory of Medical Sciences（LMS，FindAPhD 上 11 条，全部写明国际生可申）。官方“LMS 4-year PhD studentships”招生页（robots.txt 只禁 /wp-admin/）列出 2027 年 11 个全额资助课题（每题一个名额，课题介绍为 .docx 附件），截止 2026-11-18 09:00，所有国籍可申，免税生活费 £26,500/年 × 4 年、学费与签证费全包。新适配器 lms（scripts/platforms_uk.py，已加入默认采集清单）：列表与详情都读这一页，首次收录 11 条，其中 10 条与 FindAPhD 旧记录合并（FindAPhD 今天按 7 天规则下架，合并时保留官网记录）。下一步：Oxford（40 条，招聘系统有验证码，先看各学院 / DTP 自己的页面）。
     - 11-03 FindAPhD ① 原始出处：Oxford（FindAPhD 上 40 条，24 条是医学部 Kennedy 研究所 / NDM 的课题，截止 12-01）。查下来没有合规渠道：Kennedy 与 NDM 网站（含 robots.txt）对程序访问一律返回 AWS WAF 人机验证页，www.ox.ac.uk 返回 403，属于明确拦截，不访问；生物系网站允许访问，但其“2027 Projects”栏目就是嵌入的 FindAPhD 列表（页面写 Powered By FindAPhD.com），原始出处即 FindAPhD；化学、材料、工程系的几条多为限本土。结论：Oxford 课题级岗位暂无合规来源，只能等 FindAPhD 数据合作；已有的 Oxford 项目级信源保持不变。下一步：Southampton（22 条）。
     - 11-03（用户明确决定的例外，风险由用户承担）：并入用户本人用浏览器采集的 FindAPhD 岗位。原始 104 条中 78 条为竞争性资助 / 自费（按本库规则不收），收 26 条（16 条写明国际生可申、10 条限本土）；修正字段：国家 GB→UK（奥克兰一条为 NZ）、清空被误放学科标签的 flags、quote 原为资助类型标签已清空、cn 套用 UKRI 博士培训项目规则。这批记录核对日期为 11-03，同样适用 7 天未重新核对即下架的规则。自动采集仍不绕过 FindAPhD 的拦截。
     - 11-04 FindAPhD ① 原始出处：University of Southampton（FindAPhD 上 22 条）。学校自己的“当前在招博士课题”列表（/study/postgraduate-research/projects?page=N，24 页共 238 个课题；robots.txt 只禁 /research/search/、/profileview/ 等，不禁此路径）每张卡片写明 Closing date 与 Funding：200 个为竞争性资助（按规则不收），21 个 Fully funded (UK only)，17 个 Fully funded (UK and international)。新适配器 soton（scripts/platforms_uk.py，已加入默认采集清单）：列表只挑全额资助的课题读详情页，以详情页的 Funding 与 Closing date 为准；资助依据原样写 Funding 字段，详情页“Fees and funding”多为学校通用说明、没写金额，amount 留空不猜。首次收录 38 条（17 条国际生可申，21 条限本土不上首页），其中 19 条与 FindAPhD 旧记录合并、保留官网记录。下一步：Edinburgh（29 条）。
     - 11-05 FindAPhD ① 原始出处：University of Edinburgh（FindAPhD 上 29 条）。其中 25 条是 EastBio（BBSRC 博士培训项目，爱丁堡、阿伯丁、邓迪、斯特灵、圣安德鲁斯等联合）的课题；EastBio 官网（biology.ed.ac.uk/eastbio，robots.txt 只禁 /admin/、/search/、/user/ 等）写明课题列表就放在 FindAPhD 上（“Check the EastBio FindAPhD link”），课题级原始出处即 FindAPhD，与 Oxford 生物系相同，不另写适配器。按竞争性奖学金项目的规则写成项目级信源 eastbio-bbsrc-dtp：2027 入学截止 11-16、面向全球学生、资助本地标准学费 + 生活费 + 研究经费、国际生至多 30%、签证与医疗附加费自付（官网原句为证）；同时修正旧的 edinburgh-eastbio-case（原写“截止以公告为准”，改为同轮截止 11-16、状态开放）。其余 4 条为限本土或滚动课题，不另处理。下一步：Coventry（24 条）。
     - 11-06 FindAPhD ① 原始出处：Coventry University（FindAPhD 上 24 条）。学校自己的“Research studentships”列表（一页，当前 10 个带资助课题；无资助课题另在 non-funded-studentships 页，不读；robots.txt 只禁 /episerver、/shared-content、站内搜索等）课题页顶部有固定字段 Eligibility / Application deadline / Start date，资助写在 Funding 小节（“Tuition fees and bursary/stipend”，不写金额 → amount 留空不猜）。新适配器 coventry（scripts/platforms_uk.py，已加入默认采集清单）：首次收录 9 条（全部写明 UK/International 可申，截止 11-15），1 条页面未写资助不收；其中 4 条与 FindAPhD 旧记录合并、保留官网记录。FindAPhD 上其余 19 条截止 11-23、属生命科学，与 MIBTP（Coventry 为成员校，截止 11-23）一致，应为 MIBTP 课题，已由项目级信源 mibtp-bbsrc-dtp 覆盖；Warwick 的 MIBTP 课题页当天返回 429，未逐条核对，属推断。下一步：Durham（24 条）。
     - 11-07 FindAPhD ① 原始出处：Durham University（FindAPhD 上 24 条）。www.durham.ac.uk 对程序访问（连 robots.txt）都返回 CloudFront 403“Request blocked”，属明确拦截，不访问；且 24 条中 23 条写明仅限英国学生、只有 1 条面向全球，对中国学生价值有限。结论：Durham 暂无合规来源，不写适配器。同日修正：Universität Innsbruck 招聘门户改为默认返回英文页（职位名 “University Assistant (PhD position)”、截止 “online application by …”、单位 “Administrative unit:”），原规则只认德文导致 11-07 收录为 0；适配器改为德英两种写法都认，并排除 “Senior Lecturer (Doctorate/PhD)” 这类要求已有博士的教职，重新收录 15 条，配英文页离线测试。下一步：Loughborough（16 条）。
     - 11-08 FindAPhD ① 原始出处：Loughborough University（FindAPhD 上 16 条）。学校自己的“PhD opportunities”列表（/study/postgraduate/research-degrees/phd-opportunities/，一页 99 个课题；robots.txt 不禁此路径）每张卡片写明 Funding status，29 个 Funded；详情页顶部固定写“Fees for 2027-28 (Funded) UK: … International: …”与 Application deadline。新适配器 lboro（scripts/platforms_uk.py，已加入默认采集清单）：国际生一栏 Fully funded 才算可申，Part funded / Not applicable（国际生需自付学费差额）按规则算限本土；生活费按正文原句写（如“stipend of £21,805 per annum”）。首次收录 20 条（1 条国际生可申，19 条限本土，多为 Aura 海上风电 CDT），其中 3 条与 FindAPhD 旧记录合并、保留官网记录（FindAPhD 把 1 条写成“Students Worldwide”，官网写国际生 Part funded，已按官网改为限本土）。另 9 条写明“offered on a competitive basis”的是 CENTA（NERC 培训联盟）课题，课题多于名额，不逐条收。同日修正错误：CENTA 官网（robots.txt 只禁 /wp-admin/）写明 2027 入学课题制奖学金已开放、截止 2027-01-06，而库里 centa-nerc-studentships 还写“2027 窗口未确认”、centa-birmingham-phds 写“已关闭”——两条按官网与伯明翰页原句改为开放、截止 2027-01-06，并加入“现在可申请”清单；leicester-centa-studentships 页面返回 403，未改。下一步：Huddersfield（15 条）。
     - 11-09 FindAPhD ① 原始出处：University of Huddersfield（15 条）与 University of Strathclyde（13 条），都没有合规渠道，不写适配器。Huddersfield：www.hud.ac.uk 首页对程序访问返回 403，研究奖学金页虽可打开但页内埋有 honeypot（诱捕爬虫）链接，表明站方不欢迎自动访问；且 15 条全是同一批心理健康方向课题、全部写明仅限英国学生、11-13 截止，对中国学生价值为零。已有的 huddersfield-vc-scholarship（国际生学费减免）不变。Strathclyde：robots.txt 未限制，但“Postgraduate research & PhD opportunities”列表由页面脚本从学校的 Funnelback 搜索接口（strathclyde-search.funnelback.squiz.cloud）加载，该接口连 robots.txt 都返回 Cloudflare 人机验证（cf-mitigated: challenge），属明确拦截，不访问；主站没有站点地图可代替。13 条中只有 2 条面向全球学生。结论：两校课题级岗位暂无合规来源，只能等 FindAPhD 数据合作。下一步：University of Birmingham（12 条）。
     - 11-10 FindAPhD ① 原始出处：University of Birmingham（12 条）与 King’s College London（12 条），都未接入。Birmingham：robots.txt 允许访问，但学校没有统一的在招博士课题列表，站点地图（sitemap-index.xml）里与 studentship 相关的页面几乎都是 2012–2020 年的新闻存档，在招课题散在各院系页面；且 FindAPhD 上 11 条中 10 条写明仅限英国学生，写适配器不值得。KCL：12 条中 7 条面向全球学生，价值较高；学校的“Scholarships and Studentships”页只介绍 Joint PhD、CSC 联合奖学金、Harold Moody 等计划（项目级），课题级的“Funding database”（/study/funding）由页面脚本从内容管理系统的接口加载，要用页面内嵌的访问令牌才能直接读取——这属于绕过网站给普通访客的使用方式，不做；robots.txt 还禁止带 page= 的翻页地址。结论：两校课题级岗位暂无合规来源，KCL 若要接入需走 ③ 数据合作或请学校提供订阅渠道。下一步：Heriot-Watt University（10 条）。
     - 11-11 FindAPhD ① 原始出处：Heriot-Watt University（10 条）。全校“Current opportunities”总页只链到各学院，没有统一的在招课题列表；逐个查了五个学院：设计学院只收自费申请，数学与计算机学院把课题放在 Maxwell Institute（MIGS）与研究方向说明里、多数未写资助，工程与物理学院只有学位介绍页；只有 Energy, Geoscience, Infrastructure and Society（EGIS）学院有一张“Funded Research Opportunities”表（编号 / 课题 / 截止），课题页顶部固定写 Funding（如“Fully funded (UK students only)”“Fully funded (Students worldwide)”）与 Closing date，资助在“Funding information”小节写明生活费原句（如“stipend (£21,685 in 2026-27) for up to 42 months”）。robots.txt 只禁站内搜索与 /testing/，不禁此路径。新适配器 hw（scripts/platforms_uk.py，已加入默认采集清单，配离线测试）：以课题页的 Funding 与 Closing date 为准（列表上 1 条写 31-10-2026，课题页写 15 November 2026，按课题页）。首次收录 7 条（1 条面向全球学生，6 条限本土不上首页），1 条已截止不收。其余学院的课题暂无可读的结构化来源，不逐条收。下一步：University of Sheffield（10 条）。
     - 11-12 FindAPhD ① 原始出处：University of Sheffield（10 条，其中 FindAPhD 上 8 条写明仅限英国学生），未接入。学校的“PhD project directory”（/postgraduate/phd/projects）本身就是 FindAPhD 的嵌入组件（Powered By FindAPhD.com，页面脚本从 findaphd.com/connect 加载课题）；逐个查了站点地图里的院系课题页——计算机学院“PhD opportunities”、Materials 4.0 CDT、牙医学院“PhD opportunities”——也都是同一个 FindAPhD 组件，电子电气系“Scholarships and funding”只有项目级说明；energy2050 下的课题页是多年前的旧静态页，不是在招列表。robots.txt 只禁后台、站内搜索与 /find，不禁这些路径，但课题数据本身不在学校站点上。结论：谢菲尔德没有独立于 FindAPhD 的课题级来源，只能走 ③ 与 FindAPhD 的数据合作（同 Oxford 等）。下一步：Queen Mary University of London（10 条）。
     - 11-13 FindAPhD ① 原始出处：Queen Mary University of London（10 条）。站点地图（www.qmul.ac.uk/sitemap.xml）里只有电子工程与计算机学院（EECS）有统一的在招课题表“PhD studentships”（课题 / 导师 / 截止，已截止的课题另放 closed-phd-studentships 页）；生物与行为科学学院（FindAPhD 上 7 条 2027-01-27 截止、面向全球学生）在学校站点上没有找到课题列表，Blizard 研究所的 phd-projects 页是旧课题。robots.txt 只禁 /search/、/test/ 与几个旧课程目录，不禁此路径。新适配器 qmul（scripts/platforms_uk.py，已加入默认采集清单，配离线测试）：以课题页正文为准——资助只收写明 stipend 金额或 CSC 联合资助的（1 条未写资助不收），截止取“Application Deadline”一句（列表上 1 条写 31 December，课题页写 30th December，按课题页），“no fixed application deadline”记为滚动；CSC 联合奖学金页写明“available only for Chinese candidates”记为中国学生可申，写明国际生要自付学费差额的记为待确认。首次收录 5 条（含 1 条 CSC 联合奖学金）。下一步：Nottingham Trent University（10 条）。
     - 11-14 FindAPhD ① 原始出处：Nottingham Trent University（10 条）连 robots.txt 都返回 Cloudflare 人机验证，属明确拦截，不访问；De Montfort University（9 条）全是同一批莱斯特本地社会课题、全部仅限英国学生、11-29 截止，对中国学生无价值，不写适配器；Institute of Cancer Research（8 条）robots.txt 为“Disallow: /”，不访问。转而接入 Warwick（FindAPhD 上 87 条）背后的 MIBTP：6 所成员校（Aston、Birmingham、Coventry、Harper Adams、Leicester、Warwick）的课题都列在 Warwick 托管的 MIBTP 站点 4 个研究主题页的课题表里，课题链接到导师页锚点（写明 University of Registration）；robots.txt 只禁 /sitebuilder2/、/training/ 等，不禁 /fac/cross_fac/mibtp/。新适配器 mibtp（scripts/platforms_uk.py，已加入默认采集清单，配离线测试）：截止与资助取申请页原文（“Applications for the MIBTP programme to start in October 2027 are now OPEN … before Monday 23 rd November”；“cover UK tuition fees and provide a stipend at the standard UKRI rate”，不写金额 → amount 留空），申请页不写 now OPEN 或读不出截止就一条不收；国际生最多占 30%、UKRI 不负担学费差额 → 记为待确认。首次收录 392 条（2 条导师页上找不到对应课题不收），与 FindAPhD 等旧记录合并 104 条。注意：这是竞争性课题池（主题页写明每个主题每年资助的名额数，如 “13 studentships will be funded in these areas each year”），不是 392 个独立名额。下一步：Imperial College London（33 条）。
6. `/rank` 金标准评测（50 个虚构画像）；之后加向量与模型打分。
   - 10-19（产品 C）：50 个画像标注完成（`tests/rank_eval_*`，冻结数据 `tests/rank_eval_catalog.json.gz`）；Claude 逐条判断把前 10 准确率从 70% 提到 91%；向量相似度（多语言 MiniLM）AUC 只有 0.63，不采用。`/setup` 让 Claude 把关键词扩写成 6–8 个中英文说法（召回 +6%，准确率由 Claude 判断兜底）。
   - 10-20：硬性筛选接入工程 A 的申请须知字段（学位、语言要求原句、开始时间），“加分项”语言与“或协商”的日期不排除；浏览器与 `/rank` 结果仍逐条一致。岗位语言标签写了 B2 及以上的非英语语言也视为要求。为我推荐新增：关键词建议、方向对口只差一个条件的机会、下载为 profile.yml。10-20：为我推荐标出“上次来之后新出现”的机会（本机按天记住，关键词变了不比较）；重排提速到手机约 0.4 秒。
7. `/apply` 的申请清单与套磁信起草；`/track` 看板与提醒。
   - 10-19：`/apply`（`.claude/commands/apply.md` + `scripts/apply_check.py`）：`prepare` 取岗位原文生成申请清单（材料、推荐信数量、格式字数、截止时刻与时区、申请方式、开始时间、资格、资助，每项附原句），
     `papers` 查导师近期论文（OpenAlex）；起草 / 审稿子代理提示词在 `research/apply-draft-prompt.md`、`research/apply-review-prompt.md`；
     `check` 逐句校验出处标记 `[cv:…]`/`[lab:…]`/`[post]`：数字、比值、机构与人名、标题、奖项、网址必须出现在所引出处里，经历句无出处判错（`tests/test_apply.py` 24 条编造经历全部拦下），`clean` 去标记、`edit-ratio` 统计本人修改比例。
     兼容产品 C 的 cv-facts 格式（`facts` 列表），顶层可加 `name`/`email` 供落款。
   - 10-19：`/track`（`.claude/commands/track.md` + `scripts/track.py`）：`applications/tracker.yml` 五阶段看板，截止前 14/7/1 天与套磁 10 天未回提醒、每周摘要、导出 .ics、导入网站收藏。
   - 10-19：网站“我的收藏”加申请进度（想投 / 准备中 / 已投 / 面试 / 结果，存浏览器本地）、按进度筛选、“导出全部截止到日历”（截止前 14/7/1 天提醒）。
   - 10-19：端到端演示 `docs/apply-demo.md`（3 个虚构申请者 × 3 个真实岗位）：清单 → 导师论文 → 起草 → 校验 → 审稿 → 修改 → 定稿草稿，13 个文件 0 错误；
     红队评测 `scripts/apply_eval.py` 对定稿逐句造编造变体，拦下 343/347（99%）；审稿子代理找出了全部 6 句藏进去的程序查不出的编造。
     校验新增：身份 / 状态 / 角色 / 影响 / 首次 / 结论强度 / 频率 / 全称量词说法须有出处、出处张冠李戴检测、年份区间、缩写首字母。`/track weekly` 有画像时按 `/rank` 规则列新匹配。
   - 10-19：读过源码的红队写 45 条专门绕过校验的编造，第一版只拦下 8 条；改成白名单（经历句的实词须在所引出处里有，按出处标记分段核对）后拦下 44 条，红队句子进回归测试。
     网站收藏：下载收藏与进度（JSON，`track.py import-site` 直接导入）；详情页准备清单（材料取自公告原文摘出的材料清单）。公开站 README 介绍 /setup、/rank、/apply、/track。
   - 10-20：第二轮红队绕过了白名单（45 条只拦下 1 条、自然句误报 16/30）→ 词表比对降为“需核对”，新增证据核对（审稿子代理逐句逐字摘证据、程序验证，`clean` 无绕过）与数字单位、时态、职位、名次等确定性规则；
     两轮红队 89 条编造打乱后交给审稿子代理盲审，程序 + 证据核对全部拦下，忠实句 43/44 通过。`/track` 新增平台截止日期变化 / 提前下架提醒与 `sync`；网站收藏提示已下架的条目。
   - 下一步：真实用户改稿后统计修改比例（`edit-ratio`，目标 < 30%）；中文转述英文事实的对应检查；把 `/apply` 的申请清单接到网站详情页（只用岗位原文，不涉及个人数据）。
8. Agent 接入准备（为以后接入 AI agent 打基础，见 `docs/agents.md`）。
   - 10-20：随网站生成静态接口：`api/v1/index.json`（目录、枚举、规则）、`opportunities.json`（现在可申请，字段用完整英文名，附官网原句与公告原文摘出的申请须知）、`sources.json`（核对过的信源）、
     `schema.json`（JSON Schema）、`api/openapi.json`（OpenAPI 3.1，可导入为 agent 工具）、根目录 `llms.txt`；生成脚本 `scripts/build_api.py`，测试 `tests/test_api.py`。同日上线 RSS 订阅（`feeds/`）与新版界面。
   - 10-21：每日变更记录 `api/v1/changes.json`：和上一次生成的 opportunities.json 比较，按天记新增 / 下架的机会 id，同一天多次生成会合并（当天加了又撤、撤了又回的不计），保留 30 天；已写进 index.json、OpenAPI、llms.txt 与 `docs/agents.md`，`tests/test_api.py` 覆盖。
   - 下一步：MCP 服务器（搜索机会 / 查看详情 / 按画像排序，直接读上述 JSON）；按地区、学科拆分的小文件。
