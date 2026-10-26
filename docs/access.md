# 信源可访问性报告

更新于 2026-10-26 06:12 UTC，由 `scripts/access_report.py` 实际访问生成：从两个网络位置各访问一次（我们的服务器，以及 GitHub Actions，2026-10-25 06:44 UTC），任一处能打开即算能打开。

## 招聘平台：能否被程序接入

我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。

| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 访问（本服务器 / Actions） | 说明 |
|---|---|---|---:|---|---|---|
| [FindAPhD](https://www.findaphd.com/) | ✅ 已接入 | 站点地图 + 岗位页（在 GitHub Actions 上采集） | 476 | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 200 | 本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行 |
| [jobs.ac.uk](https://www.jobs.ac.uk/) | ✅ 已接入 | 搜索列表 + 岗位页 | 358 | 允许 | HTTP 200 / HTTP 200 | — |
| [Nature Careers](https://www.nature.com/naturecareers/) | ✅ 已接入 | 站点地图 + 岗位页 | 254 | 允许 | HTTP 200 / HTTP 200 | — |
| [学校自建招聘页（理大、剑桥、ANU、哥本哈根、RWTH、TUM、苏黎世大学等）](https://employment.ku.dk/all-vacancies/) | ✅ 已接入 | 各校列表页 / 站点地图 + 岗位页 | 233 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [CNRS Emploi（法国国家科研中心）](https://emploi.cnrs.fr/) | ✅ 已接入 | 站点地图 + 岗位页（博士合同与研究员 CDD） | 224 | 允许 | HTTP 200 / HTTP 200 | — |
| [THE Unijobs](https://www.timeshighereducation.com/unijobs/) | ✅ 已接入 | 站点地图 + 岗位页 | 200 | 允许 | HTTP 200 / HTTP 200 | — |
| [AcademicTransfer（荷兰）](https://www.academictransfer.com/en/) | ✅ 已接入 | 站点地图 + 岗位页 | 199 | 允许，要求每 10 秒一次 | HTTP 200 / HTTP 200 | — |
| [INSPIRE-HEP Jobs](https://inspirehep.net/jobs) | ✅ 已接入 | 官方公开接口 | 196 | 允许 | HTTP 200 / HTTP 200 | — |
| [Jobbnorge（挪威）](https://www.jobbnorge.no/) | ✅ 已接入 | 官方公开接口 | 134 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Varbi（瑞典高校）](https://lu.varbi.com/en/) | ✅ 已接入 | 各校列表页 + 岗位页 | 129 | 允许 | HTTP 200 / HTTP 200 | — |
| [德国联邦劳动局职位搜索（Jobsuche）](https://jobsuche.api.bund.dev/) | ✅ 已接入 | 劳动局自己的搜索接口（文档公开的通用 clientId，无需申请密钥） | 123 | 无 robots.txt（HTTP 403） | HTTP 200 / HTTP 200 | 旧版 /pc/v4/jobs 已返回 403，改用文档里的 /pc/v6/jobs；截止日期从岗位描述原文取，取不到不收 |
| [SAP SuccessFactors（大学招聘系统：EPFL、TU Delft、维也纳、赫尔辛基、根特等）](https://careers.epfl.ch/) | ✅ 已接入 | 各校站点地图 + 岗位页 | 108 | 允许 | HTTP 200 / HTTP 200 | — |
| [Oracle Recruiting（大学招聘系统：DTU、南丹麦大学）](https://efzu.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions) | ✅ 已接入 | 候选人站点的公开接口 | 101 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Academic Jobs Online](https://academicjobsonline.org/ajo/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 100 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [TAMU 自然资源招聘板（生态/林学）](https://jobs.rwfm.tamu.edu/) | ✅ 已接入 | 列表页 + 岗位页 | 84 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Science Careers](https://jobs.sciencecareers.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 58 | 允许 | HTTP 200 / HTTP 200 | — |
| [Inria Jobs](https://jobs.inria.fr/public/classic/en/offres) | ✅ 已接入 | 列表页 + 岗位页 | 56 | 允许 | HTTP 200 / HTTP 200 | — |
| [EconJobMarket（经济学）](https://econjobmarket.org/) | ✅ 已接入 | 列表页 + 岗位页（只收博后） | 52 | 允许 | HTTP 200 / HTTP 200 | — |
| [FAPESP Oportunidades（巴西圣保罗州研究基金会）](https://fapesp.br/oportunidades/) | ✅ 已接入 | 列表页 + 公告页（博士 / 博后奖学金） | 50 | 允许 | HTTP 200 / HTTP 200 | — |
| [Workday（大学招聘系统：Aalto、NTU、悉尼、墨尔本、UQ、UBC 等）](https://aalto.wd3.myworkdayjobs.com/aalto) | ✅ 已接入 | 各校站点地图 + 公开岗位接口 | 49 | 允许 | HTTP 200 / HTTP 200 | — |
| [MathJobs（美国数学会）](https://www.mathjobs.org/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 48 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [FENS Job Market（神经科学）](https://www.fens.org/careers/job-market) | ✅ 已接入 | 列表页 + 岗位页 | 40 | 允许 | HTTP 200 / HTTP 200 | — |
| [DAAD PhDGermany](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | ✅ 已接入 | 列表页 + 岗位页（链接需带 phd-id） | 28 | 允许 | HTTP 200 / HTTP 200 | — |
| [Aarhus University（丹麦）](https://international.au.dk/about/profile/vacant-positions/) | ✅ 已接入 | 列表页内嵌数据 + 岗位页 | 26 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [ReachMee（大学招聘系统：Chalmers）](https://www.chalmers.se/en/about-chalmers/work-with-us/vacancies/) | ✅ 已接入 | 外部招聘站列表页 + 岗位页 | 19 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [EGU Jobs（欧洲地球科学联合会）](https://www.egu.eu/jobs/) | ✅ 已接入 | 列表页 + 岗位页（结构化截止字段） | 18 | 允许 | HTTP 200 / HTTP 200 | — |
| [Physics Today Jobs](https://jobs.physicstoday.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 16 | 允许 | HTTP 200 / HTTP 200 | — |
| [Universität Innsbruck 招聘门户](https://lfuonline.uibk.ac.at/public/karriereportal.home?rubrik_in=PSP) | ✅ 已接入 | 列表页 + 岗位页 | 15 | 允许 | HTTP 200 / HTTP 200 | — |
| [INFN（意大利国家核物理研究院）](https://jobs.dsi.infn.it/) | ✅ 已接入 | 列表页 + 公告页（博后合同） | 10 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [ELLIS Jobs（欧洲 AI 研究网络）](https://ellis.eu/research/jobs) | ✅ 已接入 | 列表页 + 岗位页 | 8 | 允许 | HTTP 200 / HTTP 200 | — |
| [LINGUIST List（语言学）](https://linguistlist.org/) | ✅ 已接入 | RSS + 公告页 | 7 | 允许 | HTTP 200 / HTTP 200 | — |
| [PSI（瑞士保罗谢勒研究所）](https://www.psi.ch/en/hr/job-opportunities) | ✅ 已接入 | 列表页 + 岗位页 | 6 | 允许 | HTTP 200 / HTTP 200 | — |
| [Institut Pasteur](https://research.pasteur.fr/en/jobs/) | ✅ 已接入 | 列表页 + 岗位页 | 5 | 允许 | HTTP 200 / HTTP 200 | — |
| [IBS（韩国基础科学研究院）](https://www.ibs.re.kr/prog/recruit/eng/sub04_01/list.do) | ✅ 已接入 | 列表页 + 岗位页（不下载附件，robots.txt 禁止） | 4 | 允许 | HTTP 200 / HTTP 200 | — |
| [ETH Zurich Jobs](https://jobs.ethz.ch/) | ✅ 已接入 | 列表页 + 岗位页 | 2 | 允许 | HTTP 200 / HTTP 200 | — |
| [PageUp（大学招聘系统：港大、La Trobe）](https://jobs.hku.hk/en/listing/) | ✅ 已接入 | 列表页 + 岗位页（每 4 秒一次） | 2 | 允许 | HTTP 202 / HTTP 200 | 列表页能读，但岗位页对程序访问一律弹 AWS WAF 人机验证（HTTP 202）；不绕过，遇到就停 |
| [ESO（欧洲南方天文台）](https://recruitment.eso.org/) | ✅ 已接入 | 列表页 + 岗位页 | 1 | 允许 | HTTP 200 / HTTP 200 | — |
| [马普学会（Max Planck）](https://www.mpg.de/stellenboerse) | ✅ 已接入 | RSS + 岗位页 | — | 允许 | HTTP 200 / HTTP 200 | — |
| [H-Net Job Guide（人文社科）](https://networks.h-net.org/jobs) | ✅ 已接入 | 列表页 + 岗位页（每 5 秒一次） | — | 允许，要求每 5 秒一次 | HTTP 404 / HTTP 404 | — |
| [EURAXESS](https://euraxess.ec.europa.eu/jobs/search) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请 |
| [academics.de（德国）](https://www.academics.de/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 写明自动采集需书面许可；已起草数据合作申请 |
| [FindAPostdoc](https://www.findapostdoc.com/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [Academic Positions](https://academicpositions.com/) | ⛔ 不允许 | — | — | 允许 | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [ADUM（法国博士论文岗位）](https://adum.fr/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [JREC-IN Portal（日本）](https://jrecin.jst.go.jp/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 允许，但使用条款第 3 条规定转载岗位信息需事先向 JST 申请许可；未申请前不收 |
| [PhilJobs（哲学）](https://philjobs.org/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 使用条款禁止把内容录入数据库（个人使用除外） |
| [AEA JOE（经济学）](https://www.aeaweb.org/joe/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 页面写明未经美国经济学会书面许可不得抓取 |
| [APS Careers（物理）](https://jobs.aps.org/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [HiBrain（韩国）](https://www.hibrain.net/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 403 | robots.txt 对所有程序 Disallow: / |
| [Chronicle Jobs（美国）](https://jobs.chronicle.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但抽查 40 个岗位页都不写截止日期 |
| [Inside Higher Ed Careers](https://careers.insidehighered.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但岗位页只有广告下架日期，没有申请截止日期 |

## 核对过的高质量信源：能否打开

对 3968 条逐页核对过官网的信源实际访问一次：✅ 能打开 3837（96%）· ⚠️ 服务器拦截脚本或需登录 116 · ❌ 失效 15。

“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。

### ❌ 失效（15）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [CITA 理论天体物理博后（多伦多大学，2027 入职）](https://www.cita.utoronto.ca/opportunities/post-docs/) | HTTP 404 |
| [IMPRS-QD 海德堡量子动力学与凝聚态国际研究生院（申请页）](https://www.mpi-hd.mpg.de/imprs-qd/appladmiss1.html?&L=458) | HTTP 404 |
| [ONERA 法国航空航天研究院博士合同](https://w3.onera.fr/formationparlarecherche/node/4) | HTTP 404 |
| [RIKEN AIP 博士后（26-548，可解释 AI 团队）](https://www.riken.jp/en/careers/researchers/20260609_2/index.html) | HTTP 404 |
| [Swinburne 博士研究津贴奖学金](https://www.swinburne.edu.au/study/options/scholarships/510/swinburne-research-stipend-scholarships/) | HTTP 404 |
| [奥克兰大学–CSC 博士奖学金](https://www.auckland.ac.nz/en/study/international-students/scholarships-loans-and-funding/country-specific-scholarships-and-funding0/china.html) | HTTP 404 |
| [巴黎城市大学 · CSC 博士征集 2026（PDF）](https://u-paris.fr/doctorat/wp-content/uploads/sites/10/2026/03/Appel_CSC_2026_CED-1.pdf) | HTTP 404 |
| [巴黎大学（Université Paris Cité）CSC 博士奖学金](https://u-paris.fr/doctorat/csc/) | HTTP 404 |
| [斯威本科技大学研究生研究奖（SUPRA）](https://www.swinburne.edu.au/study/options/scholarships/221/swinburne-university-postgraduate-research-award/) | HTTP 404 |
| [柏林自由大学（FU Berlin）CSC 博士合作项目 2026 岗位说明](https://www.fu-berlin.de/en/sites/china/foerdermoeglichkeiten/fuer_chinesen/csc-phd-program/PhD-positions-2026/diverse_own-research-proposal.pdf) | HTTP 404 |
| [法国 Eiffel 卓越奖学金 2027 校内申请说明（巴黎大学）](https://u-paris.fr/language/en/eiffel-excellence-scholarship-2027/) | HTTP 404 |
| [考陶德艺术学院博士奖学金与资助](https://courtauld.ac.uk/study/postgraduate/ph-d-funding-and-scholarships) | HTTP 404 |
| [萨莱诺大学（UNISA）博士课程与 XLII 周期公告](https://web.unisa.it/home/bandi/corsi-di-studio/dottorati) | HTTP 404 |
| [诺森比亚大学太阳与空间物理全奖博士机会](https://www.northumbria.ac.uk/about-us/academic-departments/mathematics-physics-and-electrical-engineering/research/solar-and-space-physics/fully-funded-phd-opportunities/) | HTTP 404 |
| [魏玛包豪斯大学艺术与设计博士](https://uni-weimar.de/en/university/research-and-art/academic-careers/doctorate/doctoral-programmes) | HTTP 404 |

</details>

### ⚠️ 拦截脚本 / 需登录（116）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [AIRC 癌症研究短期海外访学（Short-term Fellowships）](https://www.direzionescientifica.airc.it/other-funding-opportunities/) | ProxyError |
| [ALMOA 博士网络（Klagenfurt 协调，13 个博士岗）](https://almoa.aau.at/?page_id=48) | ConnectionError |
| [ANRS MIE 博士/博后研究分配（Allocations de recherche，2026 规则）](https://anrs.fr/wp-content/uploads/2026/06/reglement-allocations-de-recherche-2027-1.pdf) | ProxyError |
| [ASEA-UNINET 奖学金分类页（东盟—欧洲大学网络）](https://asea-uninet.org/category/scholarships) | ConnectionError |
| [ASEA-UNINET 泰国大学博士项目列表](https://asea-uninet.org/category/thailand/) | ConnectionError |
| [Aalto 大学 MSCA 博士网络岗：电推进太阳风帆任务设计](https://www.aalto.fi/en/open-positions/doctoral-researcher-msca-doctoral-network-position-electric-solar-wind-sail-mission-design) | HTTP 403 |
| [Alliance Paris Lumières 博士后合同（2027 批次）](https://www.univ-paris8.fr/Contrats-Post-doctoraux-2026-Paris-Lumieres-Alliance) | HTTP 403 |
| [Berlin Mathematical School（MATH+）](https://math-berlin.de/application) | ConnectionError |
| [Boehringer Ingelheim Fonds PhD Fellowships](https://bifonds.de/fellowships-grants/phd-fellowships.html) | SSLError |
| [CEA 论文博士合同说明（INSTN）](https://instn.cea.fr/en/theses-and-phds-at-the-cea/preparing-your-thesis-at-the-cea/) | ConnectionError |
| [CIFRE（法国企业联合培养博士）说明](https://static.psl.eu/sites/default/files/2026-07/Webinaire%20CIFRE%20COFRA%2007.04.26.pdf) | ConnectionError |
| [CISPA CRISTAL 实验室 可信 AI 博士与博后招聘](https://career.cispa.de/jobs/cristal-lab-26-146) | ConnectionError |
| [CISPA System Security 研究组（Rossow）博士/博后招聘页](https://cispa.saarland/group/rossow/jobs) | ConnectionError |
| [CISPA 亥姆霍兹信息安全中心博士](https://career.cispa.de/phd/) | ConnectionError |
| [CISPA 亥姆霍兹信息安全中心招聘门户（博士与博后岗位列表）](https://jobs.cispa.saarland/jobs/detail/phd-students-1) | ConnectionError |
| [CISPA 博士后岗位（通用页）](https://jobs.cispa.saarland/jobs/detail/3) | ConnectionError |
| [CNIC 预博士项目（马德里心血管研究中心）](https://cnic.es/es/node/191) | HTTP 502 |
| [CNR 意大利科学技术研究所（ISTC）招聘页](https://istc.cnr.it/en/opportunities/vacancies) | HTTP 503 |
| [CREST / GENES 博士合同（ENSAE 经济与统计）](https://crest.science/?p=11510) | HTTP 503 |
| [Cyber Valley 职位总页（图宾根/斯图加特）](https://cyber-valley.de/en/jobs) | HTTP 500 |
| [ED3C 大脑·认知·行为博士学校 博士合同（PAC 竞争分配）条款](https://ed3c.sorbonne-universite.fr/en/financements/doctoral-contract-allocation-process-su-psl-upc/terms-and-conditions-doctoral-contract) | ConnectionError |
| [ELLIS Freiburg 新闻与职位公告](https://ellis.uni-freiburg.de/news) | ConnectionError |
| [ELLIS PhD & Postdoc Program（弗赖堡单元页）](https://ellis-d.cs.uni-freiburg.de/programs/ellis-phd-postdoc-program) | ConnectionError |
| [ERC 项目与统计数据库（找 PI 与项目）](https://erc.europa.eu/projects-statistics) | HTTP 403 |
| [ESRC 东北/西北社科博士培训伙伴关系（DWSSDTP，曼彻斯特）](https://www.humanities.manchester.ac.uk/study/postgraduate-research/funding/list-of-awards/esrc-nwssdtp/) | ReadTimeout |
| [EURAXESS China](https://euraxess.ec.europa.eu/worldwide/china) | HTTP 403 |
| [EURAXESS Japan（欧日科研职位与流动信息）](https://japan.euraxess.org) | HTTP 403 |
| [EURAXESS Netherlands（荷兰科研职位与资助门户）](https://euraxess.nl) | HTTP 403 |
| [EURAXESS 全球新闻：欧洲全奖博士职位汇总](https://euraxess.ec.europa.eu/worldwide/africa/news/over-1000-fully-funded-new-phd-job-openings-euraxess-all-international) | HTTP 403 |
| [EURAXESS 北美站：MSCA 博士网络 2025 结果通报](https://euraxess.ec.europa.eu/worldwide/north-america/news/msca-doctoral-networks-2025-call-results) | HTTP 403 |
| [EURAXESS 新闻：ERC 资助项目岗位（按 ERC 筛选）](https://euraxess.ec.europa.eu/worldwide/india/news/europe-90-positions-available-erc-funded-research-projects) | HTTP 403 |
| [EURAXESS 欧洲研究者职位门户](https://euraxess.ec.europa.eu/cs/node/5) | HTTP 403 |
| [EUROfusion 工程资助（Engineering Grants）](https://euro-fusion.org/eurofusion-news/applications-open-for-the-2027-eurofusion-engineering-grants/) | SSLError |
| [FWO 博士研究员奖学金（基础研究，佛兰德）](https://fwo.be/en/support-programmes/all-calls/phd/phd-fellowship-fundamental-research) | SSLError |
| [FWO 比利时初级博士后奖学金（Junior Postdoctoral）](https://fwo.be/en/support-programmes/all-calls/postdoctoral-researchers/junior-postdoctoral-fellowship/) | SSLError |
| [FWO 比利时高级博士后奖学金（Senior Postdoctoral）](https://www.fwo.be/en/fellowships-funding/postdoctoral-fellowships/senior-postdoctoral-fellowship/) | SSLError |
| [FWO（Research Foundation – Flanders）](https://www.fwo.be/en/support-programmes/phd-fellowships/) | SSLError |
| [G-Evol 开放博士岗位列表（明斯特大学）](https://g-evol.uni-muenster.de/?p=14) | ConnectionError |
| [GSI 亥姆霍兹重离子研究中心 HGS-HIRe for FAIR 研究生院](https://gsi.de/work/wissenschaftliche_netzwerke/hgs_hire.htm) | HTTP 503 |
| [HEC 巴黎 稳健优化与统计博士后（ANR/RGC 资助）](https://people.hec.edu/grand-clement/wp-content/uploads/sites/51/2026/02/Postdoctoral-researcher-position-HEC-Paris.pdf) | HTTP 503 |
| [HKU 计算与数据科学学院 PhD/MPhil 招生页](https://cs.hku.hk/programmes/research-based/mphil-phd-admission) | ConnectionError |
| [HKU 计算机科学系 2027 年研究型博士申请指南](https://cs.hku.hk/programmes/research-based/how-to-apply-2027) | ConnectionError（连接失败，可能限制境外访问） |
| [IFJ PAN Poncelet 组 · ERC StG STAPLE 博士岗](https://th.ifj.edu.pl/poncelet/team/) | ConnectionError |
| [IFOM 癌症生物学博士项目（米兰）](https://ifom.eu/en/training/phd-cancer-biology.php) | ConnectionError |
| [IFT 马德里（UAM-CSIC）预博士合同与奖学金页](https://www.ift.uam-csic.es/categoria-oferta/predoctorales) | ConnectionError |
| [IGBMC 博士课题与实习页](https://www.igbmc.fr/en/training/internships-and-thesis) | HTTP 503 |
| [IGBMC（斯特拉斯堡）招聘与职位页](https://www.igbmc.fr/en/igbmc/life-at-igbmc/job-offers) | HTTP 503 |
| [IISc Google PhD 奖学金项目](https://odaa.iisc.ac.in/google-phd-fellowship-program/) | HTTP 502 |
| [IIT 协作技术认知架构实验室招聘页](https://www.iit.it/en/web/cognitive-architecture-for-collaborative-technologies/openings) | HTTP 503 |
| [IMPRS Moduli Spaces（马普数学所·波恩）](https://www.mpim-bonn.mpg.de/node/82) | HTTP 503 |
| [INSA Lyon × UTT CSC 全额博士项目](https://fedora.insa-lyon.fr/en/page/ut-insacsc-program) | ConnectionError |
| [INSTN 博士与博后课题清单（CEA）](https://instn.cea.fr/en/theses-and-phds-at-the-cea/) | ConnectionError |
| [IZA 劳动经济研究所招聘平台](https://jobs.iza.org/) | ConnectionError |
| [Implanteus（阿维尼翁大学 EUR）2026–2029 博士合同课题](https://implanteus.univ-avignon.fr/theses/) | HTTP 403 |
| [Inria AVIZ 可视化与人机交互团队招聘页](https://www.aviz.fr/Research/Jobs) | ConnectionError |
| [MFC CDT（未来气候数学 CDT）](https://mfccdt.ac.uk/) | ConnectionError |
| [MSCA 博士网络 FlexCAT：15 个博士岗位（β-catenin / 无序蛋白与癌症药物发现，多国）](https://euraxess.ec.europa.eu/worldwide/india/news/europe-15-phd-positions-available-msca-flexcat-doctoral-network) | HTTP 403 |
| [Neurocure · 柏林神经科学网络博后资助汇总](https://neurocure.de/career/career-support.html) | SSLError |
| [Ohio State ECE 博士资助](https://ece.osu.edu/funding-your-graduate-education) | HTTP 403 |
| [PSL / Institut Curie 免疫学博士后岗位（2026）](https://recrutement.psl.eu/en/node/9995) | HTTP 503 |
| [PSL PhD Tracks（五年制硕士转博士通道）](https://psl.eu/formation/choisir-sa-formation/psl-phd-tracks) | HTTP 503 |
| [PSL 博士学院与各学院博士合同](https://psl.eu/formation/choisir-sa-formation/doctorat) | HTTP 503 |
| [PSL 数学与应用研究生项目博士合同（2026 批次）](https://static.psl.eu/sites/default/files/2026-03/Contrats_doctoraux_PG-Mathematiques-et-applications-PSL%20%28FR%29%20Campagne%202026.pdf) | ConnectionError |
| [PSL「古代的工坊」（Les Fabriques de l'Antique）博士合同](https://psl.eu/actualites/appel-candidature-pour-des-contrats-doctoraux-les-fabriques-de-lantique) | HTTP 503 |
| [Penn State 哲学系博士资助与支持](https://philosophy.la.psu.edu/graduate/prospectivegrads/funding-and-support/) | HTTP 403 |
| [RMIT Data61 博士奖学金](https://www.rmit.edu.au/students/careers-opportunities/scholarships/research/phd-data61) | ConnectionError |
| [Saclay Plant Sciences（SPS）博士奖学金](https://eng-saclay-plant-sciences.hub.inrae.fr/vertical-headings/sps-calls-and-job-offers/sps-funding/sps-phd-fellowships) | SSLError |
| [Stanford SAIL 博士后（AI 实验室）](https://ai.stanford.edu/postdoctoralfellows) | ConnectionError |
| [UBC CSC 博士奖学金](https://grad.ubc.ca/awards/china-scholarship-council-doctoral-scholarships) | ProxyError |
| [UBC Four Year Doctoral Fellowship（4YF）](https://grad.ubc.ca/node/3313) | ProxyError |
| [UBC Kinesiology 博士（最低资助保障）](https://grad.ubc.ca/prospective-students/graduate-degree-programs/phd-kinesiology) | ProxyError |
| [UBC 亚洲研究博士项目（四年保障资助）](https://grad.ubc.ca/prospective-students/graduate-degree-programs/phd-asian-studies) | ProxyError |
| [UC Irvine Bren 信息与计算机学院博士资助](https://www.informatics.uci.edu/?p=100) | SSLError |
| [UCLouvain FSR 2027 国际博士后（Incoming Postdoc）](https://euraxess.ec.europa.eu/worldwide/africa/news/uclouvain-opens-2027-call-incoming-international-postdoctoral-fellowships) | HTTP 403 |
| [UCSD 生物化学与分子生物学（BMB）博士资助页](https://biochemistry.ucsd.edu/node/27) | SSLError |
| [Université Gustave Eiffel 博士课题（外部候选人入口）](https://theses.univ-eiffel.fr/pages_candidats_externes/index.php?lang=en) | SSLError |
| [icipe 奖学金门户（scholarships.icipe.org，博士与硕士征集汇总）](https://scholarships.icipe.org/calls/5) | ConnectionError |
| [不列颠哥伦比亚大学 Sauder 商学院市场营销与行为科学博士](https://grad.ubc.ca/node/21007) | ProxyError |
| [京都大学 iCeMS 入学与加入页（研究生与博后）](https://www.icems.kyoto-u.ac.jp/en/join) | HTTP 503 |
| [伯明翰大学空间研究与引力波博士招生页](https://www.sr.bham.ac.uk/phd/index.php) | ConnectionError |
| [俄亥俄州立大学 CSE 博士研究/教学助理资助](https://cse.osu.edu/graduate) | HTTP 403 |
| [化合物半导体 EPSRC CDT（MRes + PhD）](https://www.cdt-compound-semiconductor.org/?p=522) | ConnectionError |
| [印度科学院 IISc 国际博士研究项目](https://oir.iisc.ac.in/?p=318) | HTTP 502 |
| [台湾大学温子祥纪念奖学金（陆生/港澳侨生，GOCFS 公告）](https://gocfs.ntu.edu.tw/en/board/detail/sn/1808) | ProxyError |
| [图宾根大学机器学习理论组（TML）职位页](https://www.tml.cs.uni-tuebingen.de/jobs/index.php) | HTTP 503 |
| [女王大学 IRIS 机器人实验室 Join us（博士）](https://iris.smithengineering.queensu.ca/join-us) | ConnectionError |
| [安特卫普大学进化与生态组（EvECo）招聘页](https://www.uantwerpen.be/en/research-groups/eveco/organisation/job-opportunities) | ConnectionError |
| [宋卡王子大学（PSU）硕博研究生奖学金（部分资助）](https://asea-uninet.org/scholarship-opportunities-graduate-study-phd-scholarships-at-prince-of-songkla-university-psu-thailand/) | ConnectionError |
| [宾州州立大学政治学系资助](https://polisci.la.psu.edu/?p=373) | HTTP 403 |
| [密歇根大学总统博士后项目](https://presidentspostdoc.umich.edu/appointment.php) | HTTP 403 |
| [巴伊兰大学（BIU）校长博士奖学金（Presidential Scholarship for Outstanding PhD Students）](https://graduate-school.biu.ac.il/en/node/1944) | ConnectionError |
| [巴黎第八大学 ARTE 博士合同（2026–2029）](https://edesta.univ-paris8.fr/IMG/pdf/arte-contrats_doctoraux_2026-2029.pdf) | HTTP 403 |
| [布雷斯特欧洲海洋研究所（IUEM）招聘页](https://www-iuem.univ-brest.fr/the-institute/recruitment/?lang=en) | ConnectionError |
| [意大利教育部博士公告门户（bandi.mur.gov.it）](https://bandi.mur.gov.it) | HTTP 403 |
| [意大利理工学院（IIT）CCHT 博士项目](https://ccht.iit.it/doctoral-programme) | HTTP 403 |
| [拉脱维亚科学委员会 1.1.1.9 博后研究项目](https://www.lzp.gov.lv/en/4th-call-research-applications-under-1119-activity-post-doctoral-research) | ConnectionError |
| [拉脱维亚科学委员会（LZP）1.1.1.9 博士后研究活动](https://lzp.gov.lv/lv/call-research-applications-under-1119-activity-post-doctoral-research) | ConnectionError |
| [捷克理工大学 PICTUS MSCA COFUND 博士项目](https://international.cvut.cz/jobs-at-ctu/pictus-phd-fellowship-programme/) | ConnectionError |
| [斯普利特大学 FESB 博士研究 2026/27 招生](https://eng.fesb.unist.hr/?p=21386) | HTTP 403 |
| [曼彻斯特–CSC 联合奖学金（人文学院）](https://www.humanities.manchester.ac.uk/study/postgraduate-research/funding/list-of-awards/university-of-manchester-joint-award-china-scholarship-council) | ReadTimeout |
| [柏林爱因斯坦神经科学中心（ECN）博士奖学金](https://neurocure.de/career/educational-programs/einstein-center-for-neurosciences-berlin.html) | SSLError |
| [法国生态与进化学会（SFE²）资助与奖学金栏目](https://sfecologie.org/category/bourses) | SSLError |
| [法国神经科学学会：国际生博士合同汇总](https://www.neurosciences.asso.fr/en/?p=29195) | ConnectionError |
| [波尔多大学 CSC 博士奖学金（年度征集）](https://doctorat.u-bordeaux.fr/en/before-phd/international/CSC) | ConnectionError |
| [波尔多大学 EDSC 40 带合同博士课题清单（2026/2027）](https://doctorat.u-bordeaux.fr/download_file/view/840d7c6e-e11f-4227-b914-a2dd6a2921d8/2967) | ConnectionError |
| [波恩马普数学研究所（MPIM）博士后与访问职位](https://www.mpim-bonn.mpg.de/Karriere) | HTTP 503 |
| [索邦大学 ED 515（复杂生命系统）博士合同](https://ed515.sorbonne-universite.fr/en/financements/doctoral-contract) | ConnectionError |
| [西北社会科学 DTP 1+3 studentship（ESRC）](https://www.humanities.manchester.ac.uk/study/postgraduate-research/funding/list-of-awards/1-3-esrc-nwssdtp) | ReadTimeout |
| [都灵理工大学 DBDMG 组 · PhD 机会分类页](https://dbdmg.polito.it/dbdmg_web/category/phd-opportunities) | ConnectionError |
| [里尔大学 ED ENGSYS · 博士申请与选拔页](https://egengsys.univ-lille.fr/en/before-phd/application-to-a-phd) | HTTP 403 |
| [里尔大学 ENGSYS 博士资助征集汇总（2026）](https://edengsys.univ-lille.fr/en/welcome/news/news-detail/campagnes-de-financements-de-these-2026) | HTTP 403 |
| [里尔大学博士资助汇总（2026 年附件 PDF）](https://edsesam.univ-lille.fr/fileadmin/user_upload/edsesam/Documents/Webinaires_Helene/Annexe_synthese_financements_de_theses_2026.pdf) | HTTP 403 |
| [里尔大学博士院校资助国际生选拔](https://edbsl.univ-lille.fr/en/apply-for-a-phd/selection-for-institutional-fundings) | HTTP 403 |
| [马尔凯理工大学（UNIVPM）XLII 周期博士公告](https://www.univpm.it/Entra/Universita_Politecnica_delle_Marche_Home/Bando_Corsi_di_Dottorato_Di_Ricerca_XLII) | ConnectionError |
| [马德里 IFT 宇宙学组招聘与职位列表](https://projects.ift.uam-csic.es/cosmo/job-offers/) | ConnectionError |
| [鲁杰·博什科维奇研究所（RBI）研究岗位页](https://www.irb.hr/eng/About-RBI/Available-Research-Jobs) | HTTP 403 |

</details>

