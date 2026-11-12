# 信源可访问性报告

更新于 2026-11-12 06:08 UTC，由 `scripts/access_report.py` 实际访问生成：从两个网络位置各访问一次（我们的服务器，以及 GitHub Actions，2026-11-11 08:18 UTC），任一处能打开即算能打开。

## 招聘平台：能否被程序接入

我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。

| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 访问（本服务器 / Actions） | 说明 |
|---|---|---|---:|---|---|---|
| [jobs.ac.uk](https://www.jobs.ac.uk/) | ✅ 已接入 | 搜索列表 + 岗位页 | 544 | 允许 | HTTP 200 / HTTP 200 | — |
| [FindAPhD](https://www.findaphd.com/) | ✅ 已接入 | 站点地图 + 岗位页（在 GitHub Actions 上采集） | 375 | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行 |
| [Nature Careers](https://www.nature.com/naturecareers/) | ✅ 已接入 | 站点地图 + 岗位页 | 251 | 允许 | HTTP 200 / HTTP 200 | — |
| [INSPIRE-HEP Jobs](https://inspirehep.net/jobs) | ✅ 已接入 | 官方公开接口 | 243 | 允许 | HTTP 200 / HTTP 200 | — |
| [学校自建招聘页（理大、剑桥、ANU、哥本哈根、RWTH、TUM、苏黎世大学等）](https://employment.ku.dk/all-vacancies/) | ✅ 已接入 | 各校列表页 / 站点地图 + 岗位页 | 235 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [CNRS Emploi（法国国家科研中心）](https://emploi.cnrs.fr/) | ✅ 已接入 | 站点地图 + 岗位页（博士合同与研究员 CDD） | 200 | 允许 | HTTP 200 / HTTP 200 | — |
| [AcademicTransfer（荷兰）](https://www.academictransfer.com/en/) | ✅ 已接入 | 站点地图 + 岗位页 | 178 | 允许，要求每 10 秒一次 | HTTP 200 / HTTP 200 | — |
| [THE Unijobs](https://www.timeshighereducation.com/unijobs/) | ✅ 已接入 | 站点地图 + 岗位页 | 177 | 允许 | HTTP 200 / HTTP 200 | — |
| [Academic Jobs Online](https://academicjobsonline.org/ajo/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 147 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [Varbi（瑞典高校）](https://lu.varbi.com/en/) | ✅ 已接入 | 各校列表页 + 岗位页 | 142 | 允许 | HTTP 200 / HTTP 200 | — |
| [Jobbnorge（挪威）](https://www.jobbnorge.no/) | ✅ 已接入 | 官方公开接口 | 141 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [德国联邦劳动局职位搜索（Jobsuche）](https://jobsuche.api.bund.dev/) | ✅ 已接入 | 劳动局自己的搜索接口（文档公开的通用 clientId，无需申请密钥） | 128 | 无 robots.txt（HTTP 403） | HTTP 200 / HTTP 200 | 旧版 /pc/v4/jobs 已返回 403，改用文档里的 /pc/v6/jobs；截止日期从岗位描述原文取，取不到不收 |
| [SAP SuccessFactors（大学招聘系统：EPFL、TU Delft、维也纳、赫尔辛基、根特等）](https://careers.epfl.ch/) | ✅ 已接入 | 各校站点地图 + 岗位页 | 100 | 允许 | HTTP 200 / HTTP 200 | — |
| [Oracle Recruiting（大学招聘系统：DTU、南丹麦大学）](https://efzu.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions) | ✅ 已接入 | 候选人站点的公开接口 | 85 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [TAMU 自然资源招聘板（生态/林学）](https://jobs.rwfm.tamu.edu/) | ✅ 已接入 | 列表页 + 岗位页 | 80 | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 200 | — |
| [MathJobs（美国数学会）](https://www.mathjobs.org/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 70 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [EconJobMarket（经济学）](https://econjobmarket.org/) | ✅ 已接入 | 列表页 + 岗位页（只收博后） | 67 | 允许 | HTTP 200 / HTTP 200 | — |
| [Workday（大学招聘系统：Aalto、NTU、悉尼、墨尔本、UQ、UBC 等）](https://aalto.wd3.myworkdayjobs.com/aalto) | ✅ 已接入 | 各校站点地图 + 公开岗位接口 | 64 | 允许 | HTTP 200 / HTTP 200 | — |
| [FAPESP Oportunidades（巴西圣保罗州研究基金会）](https://fapesp.br/oportunidades/) | ✅ 已接入 | 列表页 + 公告页（博士 / 博后奖学金） | 62 | 允许 | HTTP 200 / HTTP 200 | — |
| [Inria Jobs](https://jobs.inria.fr/public/classic/en/offres) | ✅ 已接入 | 列表页 + 岗位页 | 55 | 允许 | HTTP 200 / HTTP 200 | — |
| [Science Careers](https://jobs.sciencecareers.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 54 | 允许 | HTTP 200 / HTTP 200 | — |
| [H-Net Job Guide（人文社科）](https://networks.h-net.org/jobs) | ✅ 已接入 | 列表页 + 岗位页（每 5 秒一次） | 31 | 允许，要求每 5 秒一次 | HTTP 404 / HTTP 404 | — |
| [FENS Job Market（神经科学）](https://www.fens.org/careers/job-market) | ✅ 已接入 | 列表页 + 岗位页 | 30 | 允许 | HTTP 200 / HTTP 200 | — |
| [Physics Today Jobs](https://jobs.physicstoday.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 24 | 允许 | HTTP 200 / HTTP 200 | — |
| [Aarhus University（丹麦）](https://international.au.dk/about/profile/vacant-positions/) | ✅ 已接入 | 列表页内嵌数据 + 岗位页 | 23 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [DAAD PhDGermany](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | ✅ 已接入 | 列表页 + 岗位页（链接需带 phd-id） | 22 | 允许 | HTTP 200 / HTTP 200 | — |
| [ReachMee（大学招聘系统：Chalmers）](https://www.chalmers.se/en/about-chalmers/work-with-us/vacancies/) | ✅ 已接入 | 外部招聘站列表页 + 岗位页 | 20 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [EGU Jobs（欧洲地球科学联合会）](https://www.egu.eu/jobs/) | ✅ 已接入 | 列表页 + 岗位页（结构化截止字段） | 19 | 允许 | HTTP 200 / HTTP 200 | — |
| [Universität Innsbruck 招聘门户](https://lfuonline.uibk.ac.at/public/karriereportal.home?rubrik_in=PSP) | ✅ 已接入 | 列表页 + 岗位页 | 16 | 允许 | HTTP 200 / HTTP 200 | — |
| [LINGUIST List（语言学）](https://linguistlist.org/) | ✅ 已接入 | RSS + 公告页 | 14 | 允许 | HTTP 200 / HTTP 200 | — |
| [PageUp（大学招聘系统：港大、La Trobe）](https://jobs.hku.hk/en/listing/) | ✅ 已接入 | 列表页 + 岗位页（每 4 秒一次） | 7 | 允许 | HTTP 200 / HTTP 200 | 列表页能读，但岗位页对程序访问一律弹 AWS WAF 人机验证（HTTP 202）；不绕过，遇到就停 |
| [INFN（意大利国家核物理研究院）](https://jobs.dsi.infn.it/) | ✅ 已接入 | 列表页 + 公告页（博后合同） | 6 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Institut Pasteur](https://research.pasteur.fr/en/jobs/) | ✅ 已接入 | 列表页 + 岗位页 | 6 | 允许 | HTTP 200 / HTTP 200 | — |
| [PSI（瑞士保罗谢勒研究所）](https://www.psi.ch/en/hr/job-opportunities) | ✅ 已接入 | 列表页 + 岗位页 | 5 | 允许 | HTTP 200 / HTTP 200 | — |
| [ELLIS Jobs（欧洲 AI 研究网络）](https://ellis.eu/research/jobs) | ✅ 已接入 | 列表页 + 岗位页 | 5 | 允许 | HTTP 200 / HTTP 200 | — |
| [ESO（欧洲南方天文台）](https://recruitment.eso.org/) | ✅ 已接入 | 列表页 + 岗位页 | 1 | 允许 | HTTP 200 / HTTP 200 | — |
| [ETH Zurich Jobs](https://jobs.ethz.ch/) | ✅ 已接入 | 列表页 + 岗位页 | — | 允许 | HTTP 200 / HTTP 200 | — |
| [马普学会（Max Planck）](https://www.mpg.de/stellenboerse) | ✅ 已接入 | RSS + 岗位页 | — | 允许 | HTTP 200 / HTTP 200 | — |
| [IBS（韩国基础科学研究院）](https://www.ibs.re.kr/prog/recruit/eng/sub04_01/list.do) | ✅ 已接入 | 列表页 + 岗位页（不下载附件，robots.txt 禁止） | — | 允许 | HTTP 200 / HTTP 200 | — |
| [EURAXESS](https://euraxess.ec.europa.eu/jobs/search) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请 |
| [academics.de（德国）](https://www.academics.de/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 写明自动采集需书面许可；已起草数据合作申请 |
| [FindAPostdoc](https://www.findapostdoc.com/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [Academic Positions](https://academicpositions.com/) | ⛔ 不允许 | — | — | 允许 | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [ADUM（法国博士论文岗位）](https://adum.fr/) | ⛔ 不允许 | — | — | 禁止 | HTTP 429 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [JREC-IN Portal（日本）](https://jrecin.jst.go.jp/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 允许，但使用条款第 3 条规定转载岗位信息需事先向 JST 申请许可；未申请前不收 |
| [PhilJobs（哲学）](https://philjobs.org/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 使用条款禁止把内容录入数据库（个人使用除外） |
| [AEA JOE（经济学）](https://www.aeaweb.org/joe/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 页面写明未经美国经济学会书面许可不得抓取 |
| [APS Careers（物理）](https://jobs.aps.org/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [HiBrain（韩国）](https://www.hibrain.net/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 403 | robots.txt 对所有程序 Disallow: / |
| [Chronicle Jobs（美国）](https://jobs.chronicle.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但抽查 40 个岗位页都不写截止日期 |
| [Inside Higher Ed Careers](https://careers.insidehighered.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但岗位页只有广告下架日期，没有申请截止日期 |

## 核对过的高质量信源：能否打开

对 3967 条逐页核对过官网的信源实际访问一次：✅ 能打开 3861（97%）· ⚠️ 服务器拦截脚本或需登录 56 · ❌ 失效 50。

“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。

### ❌ 失效（50）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [ABG（Association Bernard Gregory）](https://www.abg.asso.fr/en/candidatOffres) | HTTP 404 |
| [CISPA 亥姆霍兹信息安全中心招聘门户（博士与博后岗位列表）](https://jobs.cispa.saarland/jobs/detail/phd-students-1) | HTTP 404 |
| [CISPA 博士后岗位（通用页）](https://jobs.cispa.saarland/jobs/detail/3) | HTTP 404 |
| [CITA 理论天体物理博后（多伦多大学，2027 入职）](https://www.cita.utoronto.ca/opportunities/post-docs/) | HTTP 404 |
| [CoBeNe 定期统一招生（pooled calls）](https://vds-cobene.univie.ac.at/how-to-apply/cobene-pooled-calls) | HTTP 404 |
| [ECO-N 莱比锡博士培训组（Graduiertenkolleg）](https://www.uni-leipzig.de/fileadmin/ul/projekte/Graduiertenkolleg_ECO-N/PDFs/Open_Positions/FAQs_Application_Process_ECO-N_PhD_Positions_20260109.pdf) | HTTP 404 |
| [ETH AI Center Doctoral Fellowships](https://cyber-valley.de/de/jobs/eth-ai-center-doctoral-fellowships) | HTTP 404 |
| [FWF Hertha Firnberg 女性博士后职业项目（奥地利）](https://projektservice-mathematik.univie.ac.at/news/news/call-fwf-hertha-firnberg-programme/) | HTTP 404 |
| [HKU 计算与数据科学学院 PhD/MPhil 招生页](https://cs.hku.hk/programmes/research-based/mphil-phd-admission) | HTTP 404 |
| [HKU 计算机科学系 2027 年研究型博士申请指南](https://cs.hku.hk/programmes/research-based/how-to-apply-2027) | HTTP 404 |
| [IGBMC 博士课题与实习页](https://www.igbmc.fr/en/training/internships-and-thesis) | HTTP 404 |
| [IMPRS-QD 海德堡量子动力学与凝聚态国际研究生院（申请页）](https://www.mpi-hd.mpg.de/imprs-qd/appladmiss1.html?&L=458) | HTTP 404 |
| [KAIST 机器学习与视觉实验室（MLV）招聘页](https://mlv.kaist.ac.kr/openings) | HTTP 404 |
| [KCL EPSRC 成像博士培训中心（Imaging CDT）博士](https://www.kcl.ac.uk/study/postgraduate-research/areas/imaging-cdt) | HTTP 404 |
| [Manjana Milkoreit · OsloMet · CAMELOT（ERC CoG）长期气候治理博士岗](https://www.oslomet.no/en/work/job-openings/phd-position-in-long-term-climate-governance) | HTTP 404 |
| [Novo Nordisk Foundation 海外研究博后（Bioscience and Basic Biomedicine）](https://novonordiskfonden.dk/app/uploads/Postdoc-Fellowships-for-Research-Abroad-2026-Guidelines-Bioscience-and-Basic-Biomedicine.pdf) | HTTP 404 |
| [ONERA 法国航空航天研究院博士合同](https://w3.onera.fr/formationparlarecherche/node/4) | HTTP 404 |
| [OsloMet 教育学与教师教育（LUI）博士招生](https://www.oslomet.no/en/study/lui/educational-sciences-teacher-education-phd) | HTTP 404 |
| [OsloMet 职位公告页](https://oslomet.no/en/work/job-openings) | HTTP 404 |
| [Queen's University Belfast / CSC 博士奖学金（2026 版）](https://www.qub.ac.uk/Study/international-students/international-scholarships/china/queens-university-china-scholarship-council-phd-scholarships-2026/) | HTTP 404 |
| [RIKEN AIP 博士后（26-548，可解释 AI 团队）](https://www.riken.jp/en/careers/researchers/20260609_2/index.html) | HTTP 404 |
| [RMIT Data61 博士奖学金](https://www.rmit.edu.au/students/careers-opportunities/scholarships/research/phd-data61) | HTTP 404 |
| [Strathclyde Diamond Jubilee 博士奖学金（人文与社会科学学院，国际生）](https://www.strath.ac.uk/studywithus/scholarships/diamondjubileeresearchscholarshipinternationalfacultyofhumanitiessocialsciences/) | HTTP 404 |
| [Swinburne 博士研究津贴奖学金](https://www.swinburne.edu.au/study/options/scholarships/510/swinburne-research-stipend-scholarships/) | HTTP 404 |
| [UTS 国际研究训练计划奖学金（IRTP）](https://www.uts.edu.au/for-students/admissions-entry/scholarships/scholarships-search/international-research-training-program-scholarship-irtp) | HTTP 404 |
| [Umeå 大学产业博士学校资助入口](https://www.umu.se/en/research/research-with-us/research-schools/industrial-doctoral-school-for-research-and-innovation/call-for-applications) | HTTP 404 |
| [WUR 博士岗位：沿海泥炭地景观形成与洪水模拟（Re-Flex Zeeland）](https://www.wur.nl/en/vacancy/phd-position-modelling-formation-and-flooding-coastal-peat-landscapes) | HTTP 404 |
| [东京大学 MEXT 一般选拔指南（2027 年 10 月入学）](https://www.i.u-tokyo.ac.jp/edu/MEXT_General_Guidelines_E_Oct2027.pdf) | HTTP 404 |
| [丹麦 DFF 国际博士后资助](https://dff.dk/en/apply-for-funding/see-what-you-can-apply-for/current-funding-opportunities/instruments/2026/november/dff-international-postdoctoral-grant-e26/) | HTTP 404 |
| [佛罗里达大西洋大学数学系博士助教](https://www.math.fau.edu/ta.php) | HTTP 404 |
| [剑桥 Kavli 宇宙学研究所研究员（Kavli Institute Fellowship）](https://www.kicc.cam.ac.uk/jobs/kavli-institute-fellowship) | HTTP 404 |
| [南挪威大学（USN）CELECT 中心职位公告](https://www.usn.no/celect/stillingsutlysninger) | HTTP 404 |
| [图宾根大学机器学习卓越集群岗位页](https://uni-tuebingen.de/en/research/core-research/cluster-of-excellence-machine-learning/home/open-positions/) | HTTP 404 |
| [奥克兰大学–CSC 博士奖学金](https://www.auckland.ac.nz/en/study/international-students/scholarships-loans-and-funding/country-specific-scholarships-and-funding0/china.html) | HTTP 404 |
| [奥斯陆城市大学职位页](https://www.oslomet.no/no/om/ledige-stillinger) | HTTP 404 |
| [慕尼黑大学（LMU）流行病学与公共卫生英文博士项目（DAAD 奖学金）](https://www.ibe.med.uni-muenchen.de/phd-studiengang/daad-scholarship-application/index.html) | HTTP 404 |
| [成均馆大学研究生国际生奖学金](https://admission-global.skku.edu/eng/grad/scholarship_grad.html) | HTTP 404 |
| [拉瓦尔大学 Goodman 药物研发博士奖学金](https://pha.ulaval.ca/en/research/translate-to-english-bourses-detudes-doctorales-goodman) | HTTP 404 |
| [斯威本科技大学研究生研究奖（SUPRA）](https://www.swinburne.edu.au/study/options/scholarships/221/swinburne-university-postgraduate-research-award/) | HTTP 404 |
| [曼海姆商学院运营管理全奖博士项目](https://www.bwl.uni-mannheim.de/news/fully-funded-phd-program-in-operations-management/) | HTTP 404 |
| [曼海姆大学 商业分析与运筹学 博士助研岗位](https://www.bwl.uni-mannheim.de/en/details/job-offer-research-and-teaching-assistant-phd-position-f-m-d-business-analytics-and-operations-research-2/) | HTTP 404 |
| [柏林自由大学（FU Berlin）CSC 博士合作项目 2026 岗位说明](https://www.fu-berlin.de/en/sites/china/foerdermoeglichkeiten/fuer_chinesen/csc-phd-program/PhD-positions-2026/diverse_own-research-proposal.pdf) | HTTP 404 |
| [格勒诺布尔阿尔卑斯大学 EDSTEP 博士经费类型说明（合同博士 / CIFRE）](https://edstep.univ-grenoble-alpes.fr/apply/financing-your-phd/) | HTTP 404 |
| [波鸿鲁尔大学 发展心理学博士研究助理（早期儿童情景记忆项目）](https://www.arbeitsagentur.de/jobsuche/jobdetail/10001-1003809215-S) | HTTP 410 |
| [维也纳 CoBeNe 认知与行为神经科学博士学院 申请入口](https://vds-cobene.univie.ac.at/how-to-apply/) | HTTP 404 |
| [考陶德艺术学院博士奖学金与资助](https://courtauld.ac.uk/study/postgraduate/ph-d-funding-and-scholarships) | HTTP 404 |
| [莱比锡大学 GSGAS DAAD 研究生院奖学金（GSSP）](https://sozphil.uni-leipzig.de/fileadmin/Fakult%C3%A4t_SozPhil/CfA_DAAD_Graduate_School_Scholarship_Programme_2025.pdf) | HTTP 404 |
| [诺森比亚大学太阳与空间物理全奖博士机会](https://www.northumbria.ac.uk/about-us/academic-departments/mathematics-physics-and-electrical-engineering/research/solar-and-space-physics/fully-funded-phd-opportunities/) | HTTP 404 |
| [里尔大学 ENGSYS 博士资助征集汇总（2026）](https://edengsys.univ-lille.fr/en/welcome/news/news-detail/campagnes-de-financements-de-these-2026) | HTTP 404 |
| [魏玛包豪斯大学艺术与设计博士](https://uni-weimar.de/en/university/research-and-art/academic-careers/doctorate/doctoral-programmes) | HTTP 404 |

</details>

### ⚠️ 拦截脚本 / 需登录（56）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [AIST 博士后研究员英文招聘页（innhr）](https://unit.aist.go.jp/innhr/inn-s/en/index.html) | ConnectionError |
| [AIST 英文招聘页（博士后与研究岗）](https://unit.aist.go.jp/ncm/en/recruit/index.html) | ConnectionError |
| [Aalto 大学 MSCA 博士网络岗：电推进太阳风帆任务设计](https://www.aalto.fi/en/open-positions/doctoral-researcher-msca-doctoral-network-position-electric-solar-wind-sail-mission-design) | HTTP 403 |
| [AstroBetter 天文职位 Rumor Mill（博后与任期岗位）](https://astrobetter.com/wiki/Rumor+Mill) | ConnectionError |
| [Berlin Mathematical School（MATH+）](https://math-berlin.de/application) | SSLError |
| [CREST / GENES 博士合同（ENSAE 经济与统计）](https://crest.science/?p=11510) | HTTP 503 |
| [Census Fellowship in the Reception of Antiquity（洪堡大学 / 沃伯格 / Hertziana）](https://www.biblhertz.it/3807501/Census-of-the-Reception-of-Antique-Art-and-Architecture) | SSLError |
| [ESRC SENSS 博士奖学金（埃塞克斯大学牵头的社会科学 DTP）](https://www.essex.ac.uk/postgraduate/research/doctoral-training-partnerships/senss) | SSLError |
| [EUROfusion 工程资助（Engineering Grants）](https://euro-fusion.org/eurofusion-news/applications-open-for-the-2027-eurofusion-engineering-grants/) | SSLError |
| [Edinburgh Neuroscience 职位页](https://edinburghneuroscience.ed.ac.uk/opportunities/jobs) | HTTP 403 |
| [FWO 博士研究员奖学金（基础研究，佛兰德）](https://fwo.be/en/support-programmes/all-calls/phd/phd-fellowship-fundamental-research) | SSLError |
| [FWO 比利时初级博士后奖学金（Junior Postdoctoral）](https://fwo.be/en/support-programmes/all-calls/postdoctoral-researchers/junior-postdoctoral-fellowship/) | SSLError |
| [FWO 比利时高级博士后奖学金（Senior Postdoctoral）](https://www.fwo.be/en/fellowships-funding/postdoctoral-fellowships/senior-postdoctoral-fellowship/) | SSLError |
| [FWO（Research Foundation – Flanders）](https://www.fwo.be/en/support-programmes/phd-fellowships/) | SSLError |
| [Ford Foundation Predoctoral Fellowship（经高校页面介绍）](https://fellowships.sfsu.edu/ford-foundation-predoctoral-fellowships) | SSLError |
| [GSI 亥姆霍兹重离子研究中心 HGS-HIRe for FAIR 研究生院](https://gsi.de/work/wissenschaftliche_netzwerke/hgs_hire.htm) | HTTP 503 |
| [Getty 基金会博士前与博后研究员（艺术史）](https://getty.edu/projects/pre-and-postdoctoral-fellowships/) | SSLError |
| [HKUST 研究生奖学金（Postgraduate Studentship）](https://fytgs.hkust.edu.hk/admissions/Admission-to-Hong-Kong-Campus/submitting-an-application/scholarships-and-fees) | HTTP 403 |
| [HKUST 香港博士学位奖学金计划（HKPFS）入口](https://fytgs.hkust.edu.hk/hkpfs) | HTTP 403 |
| [IMPRS "Global Multiplicity"（MPI 社会人类学 + 哈勒/莱比锡/埃朗根大学）博士项目](https://www.imprs-gm.mpg.de/) | HTTP 406 |
| [IZA 劳动经济研究所招聘平台](https://jobs.iza.org/) | ConnectionError |
| [Inria AVIZ 可视化与人机交互团队招聘页](https://www.aviz.fr/Research/Jobs) | SSLError |
| [Institut Curie 国际博士项目（IC-PhD，巴黎）](https://training.institut-curie.org/landing/2) | ConnectionError |
| [KSU 沙特国王大学全职博士后](https://dsrs.ksu.edu.sa/en/Postdoc) | HTTP 403 |
| [Karimi 课题组 · 普渡大学机械工程 · 计算力学与科学机器学习 博士招生](https://engineering.purdue.edu/karimi/people) | SSLError |
| [Los Alamos National Laboratory 博士后项目 · 资格与聘任说明](https://lanl.gov/engage/collaboration/postdoctoral-research/becoming-a-postdoc/eligibility-and-appointments) | HTTP 403（GitHub Actions 上可访问；本服务器：HTTP 404） |
| [Ohio State ECE 博士资助](https://ece.osu.edu/funding-your-graduate-education) | HTTP 403 |
| [Penn State 哲学系博士资助与支持](https://philosophy.la.psu.edu/graduate/prospectivegrads/funding-and-support/) | HTTP 403 |
| [Purdue · IDEAL 实验室 · 潜在博士生招生说明](https://engineering.purdue.edu/IDEAL/opportunities/) | SSLError |
| [Purdue 工程学院资助 RA 博士机会汇总](https://engineering.purdue.edu/SoSL/news/funded-graduated-research-assistant-opportunities-for-prospective-phd-students) | SSLError |
| [SOAS 教学奖学金（博士）](https://www.soas.ac.uk/study/student-life/finance/scholarships/soas-teaching-scholarships) | HTTP 403 |
| [Scripps Research 研究生院博士资助](https://education.scripps.edu/graduate/financial-support/) | SSLError |
| [Stanford SAIL 博士后（AI 实验室）](https://ai.stanford.edu/postdoctoralfellows) | ConnectionError |
| [俄亥俄州立大学 CSE 博士研究/教学助理资助](https://cse.osu.edu/graduate) | HTTP 403 |
| [加拿大国家研究理事会（NRC）Luise and Gerhard Herzberg 博士后奖学金](https://cnrc.canada.ca/en/corporate/careers/postdoctoral-fellowship-program) | HTTP 403 |
| [埃塞克斯大学 AHRC 博士培训伙伴（DTP）奖学金](https://www.essex.ac.uk/postgraduate/research/doctoral-training-partnerships/ahrc) | SSLError |
| [埃塞克斯大学 Leverhulme 可持续转型博士中心奖学金](https://www.essex.ac.uk/-/media/documents/directories/fees-and-funding/pgr-terms/sustainable-transitions---leverhulme-doctoral-centre-phd-scholarship-26-27.pdf) | SSLError |
| [埃塞克斯大学政府系博士奖学金页](https://essex.ac.uk/departments/government/scholarships-and-funding) | SSLError |
| [埃塞克斯大学研究生奖学金总入口](https://www.essex.ac.uk/postgraduate/research/fees-and-funding/scholarships-and-funding) | SSLError |
| [多伦多大学 Daniels 学院 · 博士后资助机会列表](https://www.daniels.utoronto.ca/research-excellence-postdoctoral-fellowship-program) | HTTP 403 |
| [奥胡斯大学 Perfusion PET 成像工具博士项目 · 招生](https://phd.health.au.dk/for-applicants/opencalls/phd-project-building-tools-for-perfusion-pet) | HTTP 403 |
| [奥胡斯大学 轨道电子学与拓扑物理博士（2026 年 11 月征集）](https://phd.nat.au.dk/for-applicants/open-calls/november-2026/accessing-orbitronics-and-twistronics-with-microscopic-and-ultrafast-angle-resolved-photoemission-spectroscopy) | HTTP 403 |
| [奥胡斯大学数学系博士岗位（概率论与分析，2027 年 2 月起）](https://phd.nat.au.dk/for-applicants/open-calls/november-2026/phd-position-in-probability-theory-and-analysis) | HTTP 403 |
| [宾州州立大学政治学系资助](https://polisci.la.psu.edu/?p=373) | HTTP 403 |
| [密歇根大学总统博士后项目](https://presidentspostdoc.umich.edu/appointment.php) | HTTP 403 |
| [居里研究所国际博士项目 IC-PhD（巴黎）](https://enseignement.curie.fr/article/ic-phd) | ConnectionError |
| [希伯来大学 Mandel 学院奖学金与资助页](https://en.mandelschool.huji.ac.il/book/export/html/9411) | HTTP 403 |
| [普渡大学 Xiaoqian Wang 课题组 · 可信 AI/ML 博士招生](https://engineering.purdue.edu/~joywang) | SSLError |
| [港科大入学奖学金（RedBird PhD Award 等）](https://fytgs.hkust.edu.hk/scholarship/scholarship-admission) | HTTP 403 |
| [爱丁堡 Doctoral College 奖学金列表（Other funding）](https://registryservices.ed.ac.uk/student-funding/postgraduate/international/other-funding/doctoral-college) | HTTP 403 |
| [爱丁堡神经科学中心职位与博士机会汇总](https://edinburghneuroscience.ed.ac.uk/opportunities/jobs-internships-phds) | HTTP 403 |
| [科大研究生院 学费与奖学金页](https://fytgs.hkust.edu.hk/fees) | HTTP 403 |
| [维也纳医科大学 博士岗位页](https://oc.meduniwien.ac.at/open-phd-positions) | HTTP 503 |
| [马尔凯理工大学（UNIVPM）XLII 周期博士公告](https://www.univpm.it/Entra/Universita_Politecnica_delle_Marche_Home/Bando_Corsi_di_Dottorato_Di_Ricerca_XLII) | ConnectionError |
| [马德里 IFT 宇宙学组招聘与职位列表](https://projects.ift.uam-csic.es/cosmo/job-offers/) | ConnectionError |
| [马普可持续材料研究所（MPI-SusMat）博士招生页](https://www.mpie.de/2928204/admission) | SSLError |

</details>

