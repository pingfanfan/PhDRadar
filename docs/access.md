# 信源可访问性报告

更新于 2026-10-22 06:04 UTC，由 `scripts/access_report.py` 实际访问生成：从两个网络位置各访问一次（我们的服务器，以及 GitHub Actions，2026-10-21 06:30 UTC），任一处能打开即算能打开。

## 招聘平台：能否被程序接入

我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。

| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 访问（本服务器 / Actions） | 说明 |
|---|---|---|---:|---|---|---|
| [FindAPhD](https://www.findaphd.com/) | ✅ 已接入 | 站点地图 + 岗位页（在 GitHub Actions 上采集） | 442 | 允许 | HTTP 403 / HTTP 200 | 本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行 |
| [jobs.ac.uk](https://www.jobs.ac.uk/) | ✅ 已接入 | 搜索列表 + 岗位页 | 258 | 允许 | HTTP 200 / HTTP 200 | — |
| [Nature Careers](https://www.nature.com/naturecareers/) | ✅ 已接入 | 站点地图 + 岗位页 | 247 | 允许 | HTTP 200 / HTTP 200 | — |
| [学校自建招聘页（理大、剑桥、ANU、哥本哈根、RWTH、TUM、苏黎世大学等）](https://employment.ku.dk/all-vacancies/) | ✅ 已接入 | 各校列表页 / 站点地图 + 岗位页 | 235 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [CNRS Emploi（法国国家科研中心）](https://emploi.cnrs.fr/) | ✅ 已接入 | 站点地图 + 岗位页（博士合同与研究员 CDD） | 233 | 允许 | HTTP 200 / HTTP 200 | — |
| [AcademicTransfer（荷兰）](https://www.academictransfer.com/en/) | ✅ 已接入 | 站点地图 + 岗位页 | 190 | 允许，要求每 10 秒一次 | HTTP 200 / HTTP 200 | — |
| [THE Unijobs](https://www.timeshighereducation.com/unijobs/) | ✅ 已接入 | 站点地图 + 岗位页 | 182 | 允许 | HTTP 200 / HTTP 200 | — |
| [INSPIRE-HEP Jobs](https://inspirehep.net/jobs) | ✅ 已接入 | 官方公开接口 | 177 | 允许 | HTTP 200 / HTTP 200 | — |
| [Varbi（瑞典高校）](https://lu.varbi.com/en/) | ✅ 已接入 | 各校列表页 + 岗位页 | 138 | 允许 | HTTP 200 / HTTP 200 | — |
| [Jobbnorge（挪威）](https://www.jobbnorge.no/) | ✅ 已接入 | 官方公开接口 | 132 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [德国联邦劳动局职位搜索（Jobsuche）](https://jobsuche.api.bund.dev/) | ✅ 已接入 | 劳动局自己的搜索接口（文档公开的通用 clientId，无需申请密钥） | 119 | 无 robots.txt（HTTP 403） | HTTP 200 / HTTP 200 | 旧版 /pc/v4/jobs 已返回 403，改用文档里的 /pc/v6/jobs；截止日期从岗位描述原文取，取不到不收 |
| [SAP SuccessFactors（大学招聘系统：EPFL、TU Delft、维也纳、赫尔辛基、根特等）](https://careers.epfl.ch/) | ✅ 已接入 | 各校站点地图 + 岗位页 | 104 | 允许 | HTTP 200 / HTTP 200 | — |
| [Oracle Recruiting（大学招聘系统：DTU、南丹麦大学）](https://efzu.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions) | ✅ 已接入 | 候选人站点的公开接口 | 96 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Academic Jobs Online](https://academicjobsonline.org/ajo/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 95 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [TAMU 自然资源招聘板（生态/林学）](https://jobs.rwfm.tamu.edu/) | ✅ 已接入 | 列表页 + 岗位页 | 84 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Science Careers](https://jobs.sciencecareers.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 61 | 允许 | HTTP 200 / HTTP 200 | — |
| [Inria Jobs](https://jobs.inria.fr/public/classic/en/offres) | ✅ 已接入 | 列表页 + 岗位页 | 54 | 允许 | HTTP 200 / HTTP 200 | — |
| [FAPESP Oportunidades（巴西圣保罗州研究基金会）](https://fapesp.br/oportunidades/) | ✅ 已接入 | 列表页 + 公告页（博士 / 博后奖学金） | 51 | 允许 | HTTP 200 / HTTP 200 | — |
| [Workday（大学招聘系统：Aalto、NTU、悉尼、墨尔本、UQ、UBC 等）](https://aalto.wd3.myworkdayjobs.com/aalto) | ✅ 已接入 | 各校站点地图 + 公开岗位接口 | 50 | 允许 | HTTP 200 / HTTP 200 | — |
| [EconJobMarket（经济学）](https://econjobmarket.org/) | ✅ 已接入 | 列表页 + 岗位页（只收博后） | 48 | 允许 | HTTP 200 / HTTP 200 | — |
| [MathJobs（美国数学会）](https://www.mathjobs.org/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 45 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [FENS Job Market（神经科学）](https://www.fens.org/careers/job-market) | ✅ 已接入 | 列表页 + 岗位页 | 40 | 允许 | HTTP 200 / HTTP 200 | — |
| [Aarhus University（丹麦）](https://international.au.dk/about/profile/vacant-positions/) | ✅ 已接入 | 列表页内嵌数据 + 岗位页 | 28 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [DAAD PhDGermany](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | ✅ 已接入 | 列表页 + 岗位页（链接需带 phd-id） | 24 | 无 robots.txt（HTTP 503） | HTTP 200 / HTTP 200 | — |
| [Physics Today Jobs](https://jobs.physicstoday.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 17 | 允许 | HTTP 200 / HTTP 200 | — |
| [EGU Jobs（欧洲地球科学联合会）](https://www.egu.eu/jobs/) | ✅ 已接入 | 列表页 + 岗位页（结构化截止字段） | 17 | 允许 | HTTP 200 / HTTP 200 | — |
| [ReachMee（大学招聘系统：Chalmers）](https://www.chalmers.se/en/about-chalmers/work-with-us/vacancies/) | ✅ 已接入 | 外部招聘站列表页 + 岗位页 | 16 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Universität Innsbruck 招聘门户](https://lfuonline.uibk.ac.at/public/karriereportal.home?rubrik_in=PSP) | ✅ 已接入 | 列表页 + 岗位页 | 12 | 允许 | HTTP 200 / HTTP 200 | — |
| [INFN（意大利国家核物理研究院）](https://jobs.dsi.infn.it/) | ✅ 已接入 | 列表页 + 公告页（博后合同） | 11 | robots.txt 取不到（ConnectionError） | ConnectionError / HTTP 200 | — |
| [LINGUIST List（语言学）](https://linguistlist.org/) | ✅ 已接入 | RSS + 公告页 | 9 | 允许 | HTTP 200 / HTTP 200 | — |
| [ELLIS Jobs（欧洲 AI 研究网络）](https://ellis.eu/research/jobs) | ✅ 已接入 | 列表页 + 岗位页 | 9 | 允许 | HTTP 200 / HTTP 200 | — |
| [Institut Pasteur](https://research.pasteur.fr/en/jobs/) | ✅ 已接入 | 列表页 + 岗位页 | 5 | 允许 | HTTP 200 / HTTP 200 | — |
| [PSI（瑞士保罗谢勒研究所）](https://www.psi.ch/en/hr/job-opportunities) | ✅ 已接入 | 列表页 + 岗位页 | 4 | 允许 | HTTP 200 / HTTP 200 | — |
| [IBS（韩国基础科学研究院）](https://www.ibs.re.kr/prog/recruit/eng/sub04_01/list.do) | ✅ 已接入 | 列表页 + 岗位页（不下载附件，robots.txt 禁止） | 3 | 允许 | HTTP 200 / HTTP 200 | — |
| [ETH Zurich Jobs](https://jobs.ethz.ch/) | ✅ 已接入 | 列表页 + 岗位页 | 2 | 允许 | HTTP 200 / HTTP 200 | — |
| [ESO（欧洲南方天文台）](https://recruitment.eso.org/) | ✅ 已接入 | 列表页 + 岗位页 | 1 | 允许 | HTTP 200 / HTTP 200 | — |
| [马普学会（Max Planck）](https://www.mpg.de/stellenboerse) | ✅ 已接入 | RSS + 岗位页 | — | 允许 | HTTP 200 / HTTP 200 | — |
| [H-Net Job Guide（人文社科）](https://networks.h-net.org/jobs) | ✅ 已接入 | 列表页 + 岗位页（每 5 秒一次） | — | 允许，要求每 5 秒一次 | HTTP 404 / HTTP 404 | — |
| [PageUp（大学招聘系统：港大、La Trobe）](https://jobs.hku.hk/en/listing/) | ✅ 已接入 | 列表页 + 岗位页（每 4 秒一次） | — | 允许 | HTTP 200 / HTTP 200 | 列表页能读，但岗位页对程序访问一律弹 AWS WAF 人机验证（HTTP 202）；不绕过，遇到就停 |
| [EURAXESS](https://euraxess.ec.europa.eu/jobs/search) | ⏸ 未接入 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 200 | robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请 |
| [academics.de（德国）](https://www.academics.de/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 写明自动采集需书面许可；已起草数据合作申请 |
| [FindAPostdoc](https://www.findapostdoc.com/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [Academic Positions](https://academicpositions.com/) | ⛔ 不允许 | — | — | 允许 | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [ADUM（法国博士论文岗位）](https://adum.fr/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [JREC-IN Portal（日本）](https://jrecin.jst.go.jp/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 允许，但使用条款第 3 条规定转载岗位信息需事先向 JST 申请许可；未申请前不收 |
| [PhilJobs（哲学）](https://philjobs.org/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 使用条款禁止把内容录入数据库（个人使用除外） |
| [AEA JOE（经济学）](https://www.aeaweb.org/joe/) | ⏸ 未接入 | — | — | 允许 | ReadTimeout / HTTP 200 | 页面写明未经美国经济学会书面许可不得抓取 |
| [APS Careers（物理）](https://jobs.aps.org/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 对所有程序 Disallow: / |
| [HiBrain（韩国）](https://www.hibrain.net/) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 403 | robots.txt 对所有程序 Disallow: / |
| [Chronicle Jobs（美国）](https://jobs.chronicle.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但抽查 40 个岗位页都不写截止日期 |
| [Inside Higher Ed Careers](https://careers.insidehighered.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但岗位页只有广告下架日期，没有申请截止日期 |

## 核对过的高质量信源：能否打开

对 3968 条逐页核对过官网的信源实际访问一次：✅ 能打开 3936（99%）· ⚠️ 服务器拦截脚本或需登录 31 · ❌ 失效 1。

“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。

### ❌ 失效（1）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [奥克兰大学–CSC 博士奖学金](https://www.auckland.ac.nz/en/study/international-students/scholarships-loans-and-funding/country-specific-scholarships-and-funding0/china.html) | HTTP 404 |

</details>

### ⚠️ 拦截脚本 / 需登录（31）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [Aalto 大学 MSCA 博士网络岗：电推进太阳风帆任务设计](https://www.aalto.fi/en/open-positions/doctoral-researcher-msca-doctoral-network-position-electric-solar-wind-sail-mission-design) | HTTP 403 |
| [Cold Spring Harbor Laboratory 研究生项目（博士）](https://www.cshl.edu/?p=395) | HTTP 403 |
| [Cold Spring Harbor Laboratory（CSHL）研究生博士项目](https://www.cshl.edu/wp-content/uploads/2019/10/PHD_and_URP_Program_Flyer.pdf) | HTTP 403 |
| [Cyber Valley 职位总页（图宾根/斯图加特）](https://cyber-valley.de/en/jobs) | HTTP 500 |
| [EUROfusion 工程资助（Engineering Grants）](https://euro-fusion.org/eurofusion-news/applications-open-for-the-2027-eurofusion-engineering-grants/) | SSLError |
| [FWO 博士研究员奖学金（基础研究，佛兰德）](https://fwo.be/en/support-programmes/all-calls/phd/phd-fellowship-fundamental-research) | SSLError |
| [FWO 比利时初级博士后奖学金（Junior Postdoctoral）](https://fwo.be/en/support-programmes/all-calls/postdoctoral-researchers/junior-postdoctoral-fellowship/) | SSLError |
| [FWO 比利时高级博士后奖学金（Senior Postdoctoral）](https://www.fwo.be/en/fellowships-funding/postdoctoral-fellowships/senior-postdoctoral-fellowship/) | SSLError |
| [FWO（Research Foundation – Flanders）](https://www.fwo.be/en/support-programmes/phd-fellowships/) | SSLError |
| [IGBMC 博士课题与实习页](https://www.igbmc.fr/en/training/internships-and-thesis) | ConnectionError |
| [MIT-WHOI 联合项目（Joint Program）博士录取与资助说明](https://mit.whoi.edu/admissions/funding) | SSLError |
| [Ohio State ECE 博士资助](https://ece.osu.edu/funding-your-graduate-education) | HTTP 403 |
| [RMIT Data61 博士奖学金](https://www.rmit.edu.au/students/careers-opportunities/scholarships/research/phd-data61) | ConnectionError |
| [UC Irvine Bren 信息与计算机学院博士资助](https://www.informatics.uci.edu/?p=100) | SSLError |
| [UCSD 生物化学与分子生物学（BMB）博士资助页](https://biochemistry.ucsd.edu/node/27) | SSLError |
| [UMD 计算机系博士资助保障](https://cs.umd.edu/node/25572) | SSLError |
| [University of Maine 研究生资助页（助教/助研）](https://umaine.edu/graduate/funding/current) | SSLError |
| [亚当·密茨凯维奇大学环境生物学院 博士招生公告](https://envbiol.web.amu.edu.pl/en/category/announcements-for-phd-students/) | SSLError |
| [佛罗里达大学政治学系资助](https://polisci.ufl.edu/graduate/financial-aid) | SSLError |
| [佛罗里达大学经济系博士资助](https://economics.clas.ufl.edu/academics/phd/financial-aid/) | SSLError |
| [俄亥俄州立大学 CSE 博士研究/教学助理资助](https://cse.osu.edu/graduate) | HTTP 403 |
| [冷泉港实验室 BioAI 博士项目（生物与人工智能）](https://www.cshl.edu/phd-program/bioai-phd-program/) | HTTP 403 |
| [冷泉港实验室 CSHL 生物科学学院博士项目 · 申请与资助](https://www.cshl.edu/phd-program/how-to-apply/) | HTTP 403 |
| [冷泉港实验室（CSHL）Fellows 独立研究员计划](https://www.cshl.edu/about-us/careers/fellows-positions/) | HTTP 403 |
| [剑桥 CAM-DTP ESRC 社科博士奖学金页](https://www.esrcdtp.group.cam.ac.uk/programme/the-studentship/) | ReadTimeout |
| [北卡州立大学自然资源学院研究生资助（CNR Graduate Support）](https://cnr.ncsu.edu/fb/graduate/graduate-support) | SSLError |
| [匹兹堡大学语言学系研究生资助](https://linguistics.pitt.edu/graduate/financial-aid) | SSLError |
| [奥本大学化学工程博士（助研/助教资助）](https://eng.auburn.edu/chen/academics/graduate/graduate-faq) | SSLError |
| [都灵理工大学 DBDMG 组 · PhD 机会分类页](https://dbdmg.polito.it/dbdmg_web/category/phd-opportunities) | ConnectionError |
| [里尔大学 ENGSYS 博士资助征集汇总（2026）](https://edengsys.univ-lille.fr/en/welcome/news/news-detail/campagnes-de-financements-de-these-2026) | HTTP 403 |
| [阿拉巴马大学伯明翰分校生物医学研究生院（GBS）资助与福利](https://www.uab.edu/gbs/home/admissions/financial-support) | SSLError |

</details>

