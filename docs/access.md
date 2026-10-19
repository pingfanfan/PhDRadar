# 信源可访问性报告

更新于 2026-10-19 09:24 UTC，由 `scripts/access_report.py` 从服务器实际访问生成。

## 招聘平台：能否被程序接入

我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。

| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 首页访问 | 说明 |
|---|---|---|---:|---|---|---|
| [FindAPhD](https://www.findaphd.com/) | ✅ 已接入 | 站点地图 + 岗位页（在 GitHub Actions 上采集） | 455 | 允许 | HTTP 403 | 本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行 |
| [Nature Careers](https://www.nature.com/naturecareers/) | ✅ 已接入 | 站点地图 + 岗位页 | 315 | 允许 | HTTP 200 | — |
| [jobs.ac.uk](https://www.jobs.ac.uk/) | ✅ 已接入 | 搜索列表 + 岗位页 | 276 | 允许 | HTTP 200 | — |
| [THE Unijobs](https://www.timeshighereducation.com/unijobs/) | ✅ 已接入 | 站点地图 + 岗位页 | 226 | 允许 | HTTP 200 | — |
| [AcademicTransfer（荷兰）](https://www.academictransfer.com/en/) | ✅ 已接入 | 站点地图 + 岗位页 | 186 | 允许，要求每 10 秒一次 | HTTP 200 | — |
| [INSPIRE-HEP Jobs](https://inspirehep.net/jobs) | ✅ 已接入 | 官方公开接口 | 164 | 允许 | HTTP 200 | — |
| [Varbi（瑞典高校）](https://lu.varbi.com/en/) | ✅ 已接入 | 各校列表页 + 岗位页 | 135 | 允许 | HTTP 200 | — |
| [Jobbnorge（挪威）](https://www.jobbnorge.no/) | ✅ 已接入 | 官方公开接口 | 129 | 无 robots.txt（HTTP 404） | HTTP 200 | — |
| [Academic Jobs Online](https://academicjobsonline.org/ajo/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 87 | 允许，要求每 5 秒一次 | HTTP 200 | — |
| [Science Careers](https://jobs.sciencecareers.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 73 | 允许 | HTTP 200 | — |
| [Inria Jobs](https://jobs.inria.fr/public/classic/en/offres) | ✅ 已接入 | 列表页 + 岗位页 | 51 | 允许 | HTTP 200 | — |
| [Physics Today Jobs](https://jobs.physicstoday.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 17 | 允许 | HTTP 200 | — |
| [ETH Zurich Jobs](https://jobs.ethz.ch/) | ✅ 已接入 | 列表页 + 岗位页 | 2 | 允许 | HTTP 200 | — |
| [马普学会（Max Planck）](https://www.mpg.de/stellenboerse) | ✅ 已接入 | RSS + 岗位页 | — | 允许 | HTTP 200 | — |
| [EURAXESS](https://euraxess.ec.europa.eu/jobs/search) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 | robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请 |
| [academics.de（德国）](https://www.academics.de/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 | robots.txt 写明自动采集需书面许可；已起草数据合作申请 |
| [FindAPostdoc](https://www.findapostdoc.com/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 | 所有程序访问返回 403 |
| [Academic Positions](https://academicpositions.com/) | ⛔ 不允许 | — | — | 允许 | HTTP 403 | 所有程序访问返回 403 |
| [DAAD PhDGermany](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | ⏸ 未接入 | — | — | 允许，要求每 2 秒一次 | HTTP 200 | 允许访问，但资助说明是浏览器里动态加载的，程序读到的页面没有资助信息，无法核对 |
| [Chronicle Jobs（美国）](https://jobs.chronicle.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 | 允许访问，但抽查 40 个岗位页都不写截止日期 |
| [Inside Higher Ed Careers](https://careers.insidehighered.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 | 允许访问，但岗位页只有广告下架日期，没有申请截止日期 |

## 核对过的高质量信源：能否打开

对 2134 条逐页核对过官网的信源实际访问一次：✅ 能打开 2059（96%）· ⚠️ 服务器拦截脚本或需登录 74 · ❌ 失效 1。

“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。

### ❌ 失效（1）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [CUHK 历史学系 HKPFS 博士页](https://www.history.cuhk.edu.hk/en/study/phd-programme/hkpfs/) | HTTP 404 |

</details>

### ⚠️ 拦截脚本 / 需登录（74）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [ALCF Margaret Butler 计算科学奖学金](https://www.alcf.anl.gov/margaret-butler-fellowship-computational-science) | HTTP 403 |
| [ANU 博士奖学金（面向国际生）](https://study.anu.edu.au/scholarships/find-scholarship/anu-phd-scholarship) | ConnectionError（连接失败，可能限制境外访问） |
| [Beatriz Galindo 高层次人才合同（西班牙，2026）](https://www.boe.es/boe/dias/2026/01/13/pdfs/BOE-B-2026-678.pdf) | ConnectionError（连接失败，可能限制境外访问） |
| [CCP4 Bulletin Board（结构生物学/晶体学招聘邮件列表）](https://legacy.ccp4.ac.uk/jobs/maillist.html) | ConnectionError（连接失败，可能限制境外访问） |
| [CNRS 招聘门户](https://emploi.cnrs.fr/) | HTTP 503 |
| [CREST / GENES 博士合同（ENSAE 经济与统计）](https://crest.science/?p=11510) | ReadTimeout（超时） |
| [CSIRO Postdoctoral Fellowships（含 CERC 研究员岗位）](https://www.csiro.au/en/careers/career-opportunities/postdoctoral-fellowships) | ConnectionError（连接失败，可能限制境外访问） |
| [Cyber Valley 职位总页（图宾根/斯图加特）](https://cyber-valley.de/en/jobs) | HTTP 500 |
| [DAAD AInet 国际 AI 早期职业研究者项目（Postdoc-NeT-AI）](https://www.daad.de/en/the-daad/postdocnet/details-and-application/) | HTTP 403 |
| [DAAD International Programmes 数据库（英文博士项目筛选）](https://www2.daad.de/deutschland/studienangebote/international-programmes/en/) | HTTP 403 |
| [DAAD PRIME 博士后研究项目（德国）](https://www.daad.de/en/studying-in-germany/scholarships/daad-funding-programmes/prime/faq/) | HTTP 403 |
| [DAAD PhDGermany 数据库](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | HTTP 403 |
| [DAAD 奖学金数据库](https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/) | HTTP 403 |
| [DAAD-DLR 研究奖学金（航空航天/能源/交通）](https://www.research-in-germany.org/en/research-funding/funding-programmes/daad-dlr-research-fellowships-in-space--aeronautics--energy-and-transportation-research.html) | HTTP 403 |
| [DIW Berlin Graduate Center 博士项目（经济学，柏林）](https://www.diw.de/en/diw_01.c.799242.en/application.html) | HTTP 403 |
| [Dan David Society of Fellows（特拉维夫大学两年博后）](https://en-humanities.tau.ac.il/dan-david-fellows) | ConnectionError（连接失败，可能限制境外访问） |
| [Donders 研究所博士项目说明](https://www.ru.nl/en/donders-institute/talent-development/phd-programme) | ConnectionError（连接失败，可能限制境外访问） |
| [ESRF 欧洲同步辐射装置博士项目（PhD Programme）](https://www.esrf.fr/home/UsersAndScience/the-phd-programme-at-the-esrf.html) | HTTP 403 |
| [Fraunhofer 个人博士项目（Individual Doctoral Projects）](https://research-in-germany.org/en/research-funding/funding-programmes/fraunhofer-individual-doctoral-projects-at-fraunhofer-institutes.html) | HTTP 403 |
| [GFZ 德国地学研究中心（亥姆霍兹）博士与博后岗位总览](https://www.gfz-potsdam.de/en/career/job-offers) | ConnectionError（连接失败，可能限制境外访问） |
| [Gurdon Institute（剑桥）Wellcome Masters+PhD 发育生物学项目](https://www.gurdon.cam.ac.uk/our-people/postgraduates/) | HTTP 403 |
| [HKU 数学系研究生申请页](https://hkumath.hku.hk/web/prospective/p-pg-admission.php) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 深圳医院联合培养博士项目（HKU-SZH）](https://www.med.hku.hk/en/teaching-and-learning/postgraduate/rpg/joint-phd/szh) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 理学院研究型博士项目介绍](https://www.scifac.hku.hk/f/page/7141/23978/Science_Poster_RPG%202026-27.pdf) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 理学院研究型研究生资助（PGS/HKPF/HKU-PS）说明页](https://www.scifac.hku.hk/rpg/rpf-rps) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 理学院研究型研究生（RPg）常见问题与导师选择指引](https://www.scifac.hku.hk/rpg/faq) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 理学院研究生项目重要日期](https://www.scifac.hku.hk/rpg-programme/important-dates) | ConnectionError（连接失败，可能限制境外访问） |
| [HKU 计算与数据科学学院 PhD/MPhil 招生页](https://cs.hku.hk/programmes/research-based/mphil-phd-admission) | ConnectionError（连接失败，可能限制境外访问） |
| [HKUST 商学院博士财务资助说明](https://bmphd.hkust.edu.hk/admissions/financial-assistance-scholarships) | ProxyError（连接失败，可能限制境外访问） |
| [HKUST(GZ) CIS Lab（Zeyu Wang）· 博后/博士/MPhil 招生](https://cislab.hkust-gz.edu.cn/openings/) | ConnectionError（连接失败，可能限制境外访问） |
| [HKUST(GZ) 研究生助学金（PGS）说明](https://fytgs.hkust-gz.edu.cn/admissions/before-submitting-an-application/scholarships-fees) | ConnectionError（连接失败，可能限制境外访问） |
| [ICM-CSIC（巴塞罗那海洋科学研究所）PIF 全额资助博士岗位](https://www.icm.csic.es/en/calls/available-phd-positions-next-pif-call) | ConnectionError（连接失败，可能限制境外访问） |
| [ICTP 博士与 sandwich 项目（发展中国家博士生）](https://ictp.it/sti/phd-and-sandwich-programmes) | ConnectionError（连接失败，可能限制境外访问） |
| [IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship）](https://ieeephotonics.org/announcements/call-for-applications-ieee-photonics-society-graduate-student-scholarship-program/) | HTTP 403 |
| [IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship）](https://www.ieeephotonics.org/awards/graduate-student-scholarship/) | HTTP 403 |
| [IIT Kharagpur 滚动制博士招生](https://www.iitkgp.ac.in/rolling-phd-admission) | ReadTimeout（超时） |
| [IIT Mandi iHub 与 HCI 基金会 · 博士后征集](https://www.ihubiitmandi.in/call-for-post-doctoral-fellowships) | ConnectionError（连接失败，可能限制境外访问） |
| [IMPRS Genome Science（哥廷根，与 GönomiX 联合招生）](https://www.uni-goettingen.de//556628.html) | HTTP 502 |
| [IMPRS Neurosciences（哥廷根）](https://www2.daad.de/deutschland/studienangebote/international-programmes/en/detail/3601) | HTTP 403 |
| [IMPRS Quantum Dynamics and Control（德累斯顿）](https://www2.daad.de/deutschland/studienangebote/international-programmes/en/detail/5512/) | HTTP 403 |
| [IMPRS-ML 分子生命科学国际研究生院（慕尼黑）](https://www2.daad.de/deutschland/studienangebote/international-programmes/en/detail/5336) | HTTP 403 |
| [IMPRS-SC 突触与神经回路国际马普研究生院（FAU）](https://mpfi.org/training/imprs/) | ProxyError（连接失败，可能限制境外访问） |
| [IRB Barcelona 国际博士奖学金](https://www.irbbarcelona.org/ca/careers/young-scientists/irb-barcelona-international-phd-fellowships-2026) | ConnectionError（连接失败，可能限制境外访问） |
| [JSPS 外国人研究者访日博士后奖学金（标准项目，FY2027 指南）](https://www.rpd.titech.ac.jp/jsps_tokken/english/kakenhi/d_index.html) | ConnectionError（连接失败，可能限制境外访问） |
| [KAIST Sangsik Kim 课题组招生（博后/博士/硕士）](https://kimgroup.kaist.ac.kr/?p=26) | ConnectionError（连接失败，可能限制境外访问） |
| [KIST 学院（UST KIST School）学位课程招生页](https://kist.re.kr/kist_school_eng/admissionDegree.do) | ConnectionError（连接失败，可能限制境外访问） |
| [KU Leuven Jobsite](https://www.kuleuven.be/personeel/jobsite/en) | ConnectionError（连接失败，可能限制境外访问） |
| [Leibniz 个人博士项目（Individual Doctoral Projects）](https://www.research-in-germany.org/en/research-funding/funding-programmes/leibniz-individual-doctoral-projects-at-leibniz-institutes.html) | HTTP 403 |
| [Research in Germany：ERC Starting Grants 说明](https://research-in-germany.org/en/research-funding/funding-programmes/erc-starting-grants.html) | HTTP 403 |
| [UBC Four Year Doctoral Fellowship（4YF）](https://grad.ubc.ca/node/3313) | ProxyError（连接失败，可能限制境外访问） |
| [UBC 研究生院 博士资助保障页](https://www.grad.ubc.ca/phd) | ProxyError（连接失败，可能限制境外访问） |
| [Wageningen University & Research 博士项目入口](https://www.wur.eu/phd) | ConnectionError（连接失败，可能限制境外访问） |
| [加利西亚大区预博士资助（含 USC）](https://www.xunta.gal/dog/Publicados/2026/20260804/AnuncioG0761-240726-0004_es.html) | HTTP 500 |
| [匈牙利 Stipendium Hungaricum 博士项目（ELTE 页面）](https://wwwold.elte.hu/en/stipendium-hungaricum) | ConnectionError（连接失败，可能限制境外访问） |
| [北京雁栖湖应用数学研究院（BIMSA）博士后（Chern Instructor）](https://www.bimsa.cn/zh-CN/join/join_postdocs.html) | ConnectionError（连接失败，可能限制境外访问） |
| [巴伊兰大学（BIU）校长博士奖学金（Presidential Scholarship for Outstanding PhD Students）](https://graduate-school.biu.ac.il/en/node/1944) | ConnectionError（连接失败，可能限制境外访问） |
| [布拉格有机化学与生物化学研究所（IOCB Prague）博士项目年度招生](https://www.uochb.cz/phd) | ConnectionError（连接失败，可能限制境外访问） |
| [希伯来大学 Mandel 学院奖学金与资助页](https://en.mandelschool.huji.ac.il/book/export/html/9411) | ConnectionError（连接失败，可能限制境外访问） |
| [平和中岛财团留学生奖学金（日本）](https://www.hama-med.ac.jp/uni-e/campus-life/mt_files/heiwanakajima2026.pdf) | ConnectionError（连接失败，可能限制境外访问） |
| [康拉德·阿登纳基金会（KAS）外国博士生奖学金（2026 指南）](https://www.kas.de/documents/d/begabtenfoerderung-und-kultur/rili-internationale-nachwuchsfoerderung-01_2026) | HTTP 403 |
| [拉德堡德大学（Radboud）在职博士候选人说明](https://www.ru.nl/en/working-at/working-in-research-education/working-as-a-phd-candidate) | ConnectionError（连接失败，可能限制境外访问） |
| [欧洲同步辐射装置（ESRF）· 博士生项目与招聘条件](https://www.esrf.fr/Jobs/Conditions/PhDStudents) | HTTP 403 |
| [港大研究型研究生资助总览](https://english.hku.hk/Postgraduate/MPhil_and_PhD/Funding_Opportunities_for_RPG_Students) | ConnectionError（连接失败，可能限制境外访问） |
| [澳门大学 UM Talent Programme（博士后）](https://rskto.um.edu.mo/?p=5096) | HTTP 403 |
| [科威特大学研究生学术卓越奖学金](https://cgs.ku.edu.kw/excellence-scholarship/admission-requirements-excellence-scholarship/) | HTTP 429 |
| [科隆大学地球科学研究生院 DAAD 奖学金（GSGS）](https://geosciences.uni-koeln.de/gsgs/news-and-reports/news-page/call-for-daad-graduate-school-scholarship-programme-2026) | HTTP 500 |
| [耶拿微生物通讯研究生院（JSMC）](https://www2.daad.de/deutschland/studienangebote/international-programmes/en/detail/4005/) | HTTP 403 |
| [莱布尼茨研究生院（Leibniz Graduate Schools）奖学金](https://www.research-in-germany.org/en/research-funding/funding-programmes/leibniz-graduate-schools-and-leibniz-sciencecampi.html) | HTTP 403 |
| [西奈山伊坎医学院国际学生资助页（生物医学科学与神经科学博士）](https://icahn.mssm.edu/education/financial-aid/application/international-students) | HTTP 403 |
| [阿利坎特神经科学研究所（IN, CSIC-UMH）岗位页](https://in.umh-csic.es/en/the-institute/job-offers/) | ConnectionError（连接失败，可能限制境外访问） |
| [韩国国际交流财团（KF）韩国学研究生奖学金](https://en.kf.or.kr/?menuno=3793) | ConnectionError（连接失败，可能限制境外访问） |
| [香港大学商学院（FBE）博士入学与财务支持说明](https://phd.hkubs.hku.hk/admissions/admission-application-and-tuition-fee/1000) | ConnectionError（连接失败，可能限制境外访问） |
| [香港大学生物科学学院 生态与生物多样性方向研究生招生](https://biosch.hku.hk/?p=3675) | ConnectionError（连接失败，可能限制境外访问） |
| [香港科技大学物理系研究生奖学金与奖项](https://physics.hkust.edu.hk/index.php/programs/postgraduate-programs/scholarship-award) | ProxyError（连接失败，可能限制境外访问） |

</details>

