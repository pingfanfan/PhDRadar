# 信源可用性报告

生成时间：2026-10-26T09:18:03+00:00（由 `scripts/probe_sources.py` 在 GitHub Actions 中真实访问生成）

- 链接：4007 个，✅ 可访问 3760，⚠️ 被拦截/需登录 226，❌ 失效 21
- 抓取器：16 个，能拿到岗位 14 个

## 抓取器

| 信源 | 状态 | 样例岗位 | 耗时 | 错误 |
| --- | :-: | --- | --- | --- |
| `academictransfer` | ✅ 5 | PhD Position in Cloud-Native and AI-Native 6G Networks | 111.0s |  |
| `agu-careers` | ✅ 5 | Pennsylvania State University, Department of Ecosystem Science and Management: P | 1.9s |  |
| `bluesky-phd-position` | ✅ 5 | 📢 Congratulations to our Alix Vidal ✨ who just got a NWO Vidi grant for research | 2.2s |  |
| `chemistry-world-jobs` | ✅ 1 | Los Alamos National Laboratory: Postdoctoral Research Associate in Chemical Desi | 2.0s |  |
| `cstheory-jobs` | ✅ 4 | Postdoctoral Research Associate at Princeton University at Princeton University  | 1.3s |  |
| `daad-phdgermany` | ❌  |  | 2.0s | HTTPError: 403 Client Error: Forbidden for url: https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/?phd-p=1 |
| `euraxess` | ❌  |  | 1.1s | HTTPError: 403 Client Error: Forbidden for url: https://euraxess.ec.europa.eu/jobs/search?f%5B0%5D=offer_type%3Ajob_offer&page=0 |
| `inspire-jobs` | ✅ 5 | PhD Positions in Theoretical Developments for searches of high frequency Gravita | 3.5s |  |
| `jobbnorge` | ✅ 5 | PhD Candidate in AI-driven smart material characterisation and modelling | 3.2s |  |
| `jobrxiv` | ✅ 5 | PHD student in Epigenetics and Chromatin Dynamics | 3.8s |  |
| `jobs-ac-uk` | ✅ 5 | PhD Studentship: AI Optimisation of Green Roofs and Facades for Low-Carbon, Heat | 2.7s |  |
| `physics-today-jobs` | ✅ 5 | International Max Planck Research School for Chemistry and Physics of Quantum Ma | 2.2s |  |
| `science-careers` | ✅ 5 | International Max Planck Research School for Ultrafast Imaging and Structural Dy | 1.5s |  |
| `sfn-neurojobs` | ✅ 5 | Oregon Health and Science University: Postdoctoral Fellow | 1.8s |  |
| `the-unijobs` | ✅ 5 | KINGS COLLEGE LONDON: Phd Studentship, Analytics, Environmental & Forensics | 1.4s |  |
| `varbi` | ✅ 5 | Doctoral student in Numerical simulations of turbulent heat transfer over rough  | 19.9s |  |

## 需要关注的链接

⚠️ 多为网站拦截脚本访问（403/429）或需要登录，浏览器中通常可正常打开；❌ 需修复。

| 信源 | 状态 | 详情 |
| --- | :-: | --- |
| `anrs-mie-allocations-2026` ANRS MIE 博士/博后研究分配（Allocations de recherche，2026 规则） | ❌ | DNS 解析失败 |
| `auckland-csc-phd` 奥克兰大学–CSC 博士奖学金 | ❌ | HTTP 404 |
| `bauhaus-weimar-doctorate` 魏玛包豪斯大学艺术与设计博士 | ❌ | HTTP 404 → https://www.uni-weimar.de/en/university/research-and-art/academic-careers/doctorate/doctoral-programmes |
| `cita-postdoc-2026` CITA 理论天体物理博后（多伦多大学，2027 入职） | ❌ | HTTP 404 |
| `courtauld-phd-funding-scholarships` 考陶德艺术学院博士奖学金与资助 | ❌ | HTTP 404 |
| `csc-paris-cite-doctoral` 巴黎大学（Université Paris Cité）CSC 博士奖学金 | ❌ | HTTP 404 |
| `cyber-valley-jobs` Cyber Valley 职位总页（图宾根/斯图加特） | ❌ | HTTP 404 |
| `data61-phd-rmit` RMIT Data61 博士奖学金 | ❌ | HTTP 404 → https://www.rmit.edu.au/scholarships/research/phd-data61 |
| `eiffel-u-paris-2027` 法国 Eiffel 卓越奖学金 2027 校内申请说明（巴黎大学） | ❌ | HTTP 404 |
| `eth-ai-center-doctoral-fellowships` ETH AI Center Doctoral Fellowships | ❌ | HTTP 404 |
| `fr-paris-cite-csc-appel-2026` 巴黎城市大学 · CSC 博士征集 2026（PDF） | ❌ | HTTP 404 |
| `fu-berlin-csc-phd-program-2026` 柏林自由大学（FU Berlin）CSC 博士合作项目 2026 岗位说明 | ❌ | HTTP 404 |
| `imprs-qd-heidelberg-application` IMPRS-QD 海德堡量子动力学与凝聚态国际研究生院（申请页） | ❌ | HTTP 404 |
| `northumbria-solar-space-phd` 诺森比亚大学太阳与空间物理全奖博士机会 | ❌ | HTTP 404 |
| `onera-doctoral-training` ONERA 法国航空航天研究院博士合同 | ❌ | HTTP 404 |
| `riken-aip-postdoc-26-548-xai` RIKEN AIP 博士后（26-548，可解释 AI 团队） | ❌ | HTTP 404 |
| `swinburne-research-stipend` Swinburne 博士研究津贴奖学金 | ❌ | HTTP 404 |
| `swinburne-supra` 斯威本科技大学研究生研究奖（SUPRA） | ❌ | HTTP 404 |
| `unisa-phd-xlii` 萨莱诺大学（UNISA）博士课程与 XLII 周期公告 | ❌ | HTTP 404 |
| `uts-irtp-scholarship` UTS 国际研究训练计划奖学金（IRTP） | ❌ | HTTP 404 |
| `wur-coastal-peat-flooding-phd` WUR 博士岗位：沿海泥炭地景观形成与洪水模拟（Re-Flex Zeeland） | ❌ | HTTP 404 |
| `aa-school-phd-programme` 伦敦 AA 建筑联盟学院博士项目 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `aalto-msca-solar-wind-sail-phd` Aalto 大学 MSCA 博士网络岗：电推进太阳风帆任务设计 | ⚠️ | HTTP 403 |
| `abs-positions-news` Animal Behavior Society · Positions & News（Jobs & Postdocs / Grad Positions） | ⚠️ | HTTP 403 |
| `acce-dtp-noc-dla` ACCE+ 博士培训伙伴 NOC 博士学位机会（DLA） | ⚠️ | HTTP 429 |
| `agu-findajob-geology` AGU FindAJob 地质学职位页 | ⚠️ | HTTP 403 |
| `agu-findajob-ocean-science-phd` AGU FindAJob 海洋科学博士/博后筛选页 | ⚠️ | HTTP 403 |
| `ai-decisions-cdt` AI Decisions CDT（EPSRC） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `airc-short-term-fellowships-abroad` AIRC 癌症研究短期海外访学（Short-term Fellowships） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ajou-university-graduate-scholarship` 亚洲大学（Ajou University）研究生奖学金（BK21 与校内奖学金） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `alliance-paris-lumieres-postdoc-2026` Alliance Paris Lumières 博士后合同（2027 批次） | ⚠️ | HTTP 403 |
| `almoa-dn-positions` ALMOA 博士网络（Klagenfurt 协调，13 个博士岗） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-doctoral-contracts` 普罗旺斯大学（AMU）博士合同竞争（2026–2029） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-ed372-financing` 艾克斯-马赛大学 ED372 博士资助 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-ed659-funding` 艾克斯-马赛大学 ED659 博士资助 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-ed67-contrat-doc-2026-2029` Aix-Marseille 大学 ED 67 博士合同申请表（2026–2029） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-inter-ed-doctoral-contracts` Aix-Marseille 大学跨博士学院合同征集（Collège doctoral） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `anii-uruguay-posgrados-2026` 乌拉圭 ANII 2026 年国内硕博奖学金（基础文件） | ⚠️ | HTTP 403 |
| `antwerp-eveco-job-opportunities` 安特卫普大学进化与生态组（EvECo）招聘页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `aries-dtp-studentships` ARIES 博士培训伙伴奖学金（含 Cefas 合作 CASE 项目） | ⚠️ | HTTP 405 |
| `asea-uninet-scholarships` ASEA-UNINET 奖学金分类页（东盟—欧洲大学网络） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `asea-uninet-thailand-list` ASEA-UNINET 泰国大学博士项目列表 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `astrobetter-rumor-mill` AstroBetter 天文职位 Rumor Mill（博后与任期岗位） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `aviz-inria-hci-jobs` Inria AVIZ 可视化与人机交互团队招聘页 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `bbsrc-nwdp-manchester-liverpool` BBSRC 西北生物科学博士项目（NWDP，曼彻斯特 + 利物浦） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `berlin-neuroscience-network-funding-hub` Neurocure · 柏林神经科学网络博后资助汇总 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `bif` Boehringer Ingelheim Fonds PhD Fellowships | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `birmingham-sr-phd-admissions` 伯明翰大学空间研究与引力波博士招生页 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `biu-presidential-phd-scholarship` 巴伊兰大学（BIU）校长博士奖学金（Presidential Scholarship for Outstanding PhD Students） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `bms-berlin` Berlin Mathematical School（MATH+） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `bordeaux-csc` 波尔多大学 CSC 博士奖学金（年度征集） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `brandeis-heller-phd-funding` 布兰迪斯大学 Heller 学院博士资助页 | ⚠️ | HTTP 403 |
| `brandeis-ibs-econ-finance-phd` Brandeis 国际商学院国际经济与金融博士（全额资助） | ⚠️ | HTTP 403 |
| `brandeis-neuroscience-funding` 布兰迪斯大学（Brandeis）神经科学博士资助 | ⚠️ | HTTP 403 |
| `bristol-pg-research-scholarship` 布里斯托大学 PGR 研究生奖学金（理工与医学，含国际生） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ca-uoft-ece-funding` U of T ECE 博士保障资助 | ⚠️ | HTTP 500 |
| `cam-esrc-dtp-studentship` 剑桥 CAM-DTP ESRC 社科博士奖学金页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `che-intl-scholarship-programs` 以色列高教委（CHE）国际生奖学金项目总目录 | ⚠️ | HTTP 403 |
| `cispa-cristal-lab-trustworthy-ai-phd-postdoc` CISPA CRISTAL 实验室 可信 AI 博士与博后招聘 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cispa-jobs-portal-phd-postdoc` CISPA 亥姆霍兹信息安全中心招聘门户（博士与博后岗位列表） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cispa-phd` CISPA 亥姆霍兹信息安全中心博士 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cispa-postdoc-general` CISPA 博士后岗位（通用页） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cispa-rossow-system-security-jobs` CISPA System Security 研究组（Rossow）博士/博后招聘页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cnic-predoctoral-program` CNIC 预博士项目（马德里心血管研究中心） | ⚠️ | ReadTimeout（超时） |
| `cnr-istc-vacancies-scala` CNR 意大利科学技术研究所（ISTC）招聘页 | ⚠️ | HTTP 503 |
| `compound-semi-cdt` 化合物半导体 EPSRC CDT（MRes + PhD） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `crest-genes-doctoral-contracts` CREST / GENES 博士合同（ENSAE 经济与统计） | ⚠️ | HTTP 503 |
| `cruk-manchester-phd-studentships` CRUK 曼彻斯特研究所 PhD 资助（BMH 全额资助项目） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `cvut-pictus-phd-cofund` 捷克理工大学 PICTUS MSCA COFUND 博士项目 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `daad-ainet-postdoc-network` DAAD AInet 国际 AI 早期职业研究者项目（Postdoc-NeT-AI） | ⚠️ | HTTP 403 |
| `daad-dlr-research-fellowships` DAAD-DLR 研究奖学金（航空航天/能源/交通） | ⚠️ | HTTP 403 |
| `daad-ifi-postdoc-ai-cs` DAAD IFI 研究奖学金（AI 与计算机科学国际流动项目，博后线） | ⚠️ | HTTP 403 |
| `daad-international-programmes-db` DAAD International Programmes 数据库（英文博士项目筛选） | ⚠️ | HTTP 403 |
| `daad-phdgermany` DAAD PhDGermany 数据库 | ⚠️ | HTTP 403 |
| `daad-phdgermany-programme-page` DAAD PhDGermany 项目说明页 | ⚠️ | HTTP 403 |
| `daad-prime-postdoc` DAAD PRIME 博士后研究项目（德国） | ⚠️ | HTTP 403 |
| `daad-scholarship-db` DAAD 奖学金数据库 | ⚠️ | HTTP 403 |
| `diw-graduate-center-phd` DIW Berlin Graduate Center 博士项目（经济学，柏林） | ⚠️ | HTTP 403 |
| `dlr-graduate-program` DLR 博士研究生培训计划（DLR Graduate Program） | ⚠️ | HTTP 403 |
| `doaks-fellowships` Dumbarton Oaks 拜占庭与古典研究初级研究员奖 | ⚠️ | HTTP 403 |
| `dumbarton-oaks-mellon-landscape-fellowships` Dumbarton Oaks Mellon 园林与景观研究员奖学金 | ⚠️ | HTTP 403 |
| `ecn-berlin-phd` 柏林爱因斯坦神经科学中心（ECN）博士奖学金 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `eco-n-leipzig-graduiertenkolleg` ECO-N 莱比锡博士培训组（Graduiertenkolleg） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ed3c-doctoral-contract-terms` ED3C 大脑·认知·行为博士学校 博士合同（PAC 竞争分配）条款 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `enerhy-cdt` EnerHy 绿氢与风能博士培训中心（CDT） | ⚠️ | HTTP 403 |
| `erasmus-mc-phd-vacancies` Erasmus MC（鹿特丹）· PhD 岗位总览 | ⚠️ | HTTP 503 |
| `erc-dashboard-projects` ERC 项目与统计数据库（找 PI 与项目） | ⚠️ | HTTP 403 |
| `erc-research-in-germany-stg` Research in Germany：ERC Starting Grants 说明 | ⚠️ | HTTP 403 |
| `erc-stg-staple-ifj-krakow-phd` IFJ PAN Poncelet 组 · ERC StG STAPLE 博士岗 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `esrf-phd-conditions` 欧洲同步辐射装置（ESRF）· 博士生项目与招聘条件 | ⚠️ | HTTP 403 |
| `esrf-phd-programme` ESRF 欧洲同步辐射装置博士项目（PhD Programme） | ⚠️ | HTTP 403 |
| `eu-euraxess-jobs` EURAXESS 欧洲研究者职位门户 | ⚠️ | HTTP 403 |
| `euraxess` EURAXESS Jobs | ⚠️ | HTTP 403 |
| `euraxess-china` EURAXESS China | ⚠️ | HTTP 403 |
| `euraxess-dn-2025-results` EURAXESS 北美站：MSCA 博士网络 2025 结果通报 | ⚠️ | HTTP 403 |
| `euraxess-erc-funded-filter-news` EURAXESS 新闻：ERC 资助项目岗位（按 ERC 筛选） | ⚠️ | HTTP 403 |
| `euraxess-funded-phd-news` EURAXESS 全球新闻：欧洲全奖博士职位汇总 | ⚠️ | HTTP 403 |
| `euraxess-japan` EURAXESS Japan（欧日科研职位与流动信息） | ⚠️ | HTTP 403 → https://euraxess.ec.europa.eu/worldwide/japan |
| `eurofusion-engineering-grants` EUROfusion 工程资助（Engineering Grants） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fau-imprs-sc` IMPRS-SC 突触与神经回路国际马普研究生院（FAU） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `fbk-international-phd` 布鲁诺·凯斯勒基金会（FBK）国际博士项目 | ⚠️ | ReadTimeout（超时） |
| `fesb-split-doctoral-2026` 斯普利特大学 FESB 博士研究 2026/27 招生 | ⚠️ | HTTP 403 |
| `fr-insa-lyon-utt-csc` INSA Lyon × UTT CSC 全额博士项目 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fr-lille-engsys-phd` 里尔大学 ED ENGSYS · 博士申请与选拔页 | ⚠️ | HTTP 403 |
| `fr-lille-engsys-thesis-funding-2026` 里尔大学 ENGSYS 博士资助征集汇总（2026） | ⚠️ | HTTP 403 → https://egengsys.univ-lille.fr/en/welcome/news/news-detail/campagnes-de-financements-de-these-2026 |
| `fr-saclay-plant-sciences-phd` Saclay Plant Sciences（SPS）博士奖学金 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `fraunhofer-individual-doctoral-projects` Fraunhofer 个人博士项目（Individual Doctoral Projects） | ⚠️ | HTTP 403 |
| `fwo` FWO（Research Foundation – Flanders） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fwo-junior-postdoc` FWO 比利时初级博士后奖学金（Junior Postdoctoral） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fwo-phd-fundamental` FWO 博士研究员奖学金（基础研究，佛兰德） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fwo-senior-postdoc` FWO 比利时高级博士后奖学金（Senior Postdoctoral） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `g-evol-muenster-open-phd` G-Evol 开放博士岗位列表（明斯特大学） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `gal-predoc-usc` 加利西亚大区预博士资助（含 USC） | ⚠️ | HTTP 500 |
| `gifu-english-agri-phd` 岐阜大学联合农学研究科英文授课博士项目（2027） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `grass-fellowship-mbl` Grass Fellowship（MBL 神经科学夏季研究基金） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `gsi-hgs-hire-graduate-school` GSI 亥姆霍兹重离子研究中心 HGS-HIRe for FAIR 研究生院 | ⚠️ | HTTP 503 → https://hgs-hire.de/ |
| `gurdon-wellcome-masters-phd` Gurdon Institute（剑桥）Wellcome Masters+PhD 发育生物学项目 | ⚠️ | HTTP 403 |
| `hec-paris-robust-optimization-postdoc` HEC 巴黎 稳健优化与统计博士后（ANR/RGC 资助） | ⚠️ | HTTP 503 |
| `helsinki-doctoral-researcher-positions` 赫尔辛基大学博士生院统一资助的博士研究员职位 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `hku-cs-how-to-apply-2027` HKU 计算机科学系 2027 年研究型博士申请指南 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `hku-cs-phd-admissions` HKU 计算与数据科学学院 PhD/MPhil 招生页 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `hku-shenzhen-hospital-joint-phd` HKU 深圳医院联合培养博士项目（HKU-SZH） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `huji-csc-scholarship` 希伯来大学 CSC–HUJI 联合奖学金（中国籍博士/博后） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `huji-racah-international-students` 希伯来大学 Racah 物理研究所国际学生与博士资助说明 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `icgeb-arturo-falaschi-fellowships` ICGEB Arturo Falaschi 博士/博后奖学金（生命科学，的里雅斯特/新德里/开普敦） | ⚠️ | HTTP 520 |
| `icipe-scholarships-portal` icipe 奖学金门户（scholarships.icipe.org，博士与硕士征集汇总） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `icmat-severo-ochoa-fpi-past` ICMAT Severo Ochoa 博士研究奖学金（FPI，马德里） | ⚠️ | ReadTimeout（超时） |
| `idrc-idra-doctoral-awards` IDRC 国际博士研究奖（Universities Canada） | ⚠️ | HTTP 403 |
| `ieee-eds-phd-student-fellowship` IEEE 电子器件学会（EDS）博士生奖学金 | ⚠️ | ReadTimeout（超时） |
| `ieee-npss-graduate-scholarship` IEEE 核与等离子体科学学会（NPSS）研究生奖学金 | ⚠️ | ReadTimeout（超时） |
| `ieee-photonics-graduate-scholarship` IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship） | ⚠️ | HTTP 403 |
| `ieee-photonics-gs-scholarship` IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship） | ⚠️ | HTTP 403 |
| `ifom-cancer-biology-phd` IFOM 癌症生物学博士项目（米兰） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ift-madrid-cosmo-job-offers` 马德里 IFT 宇宙学组招聘与职位列表 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ift-madrid-predoctorales` IFT 马德里（UAM-CSIC）预博士合同与奖学金页 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `igbmc-job-offers` IGBMC（斯特拉斯堡）招聘与职位页 | ⚠️ | HTTP 503 |
| `igbmc-thesis-internships` IGBMC 博士课题与实习页 | ⚠️ | HTTP 503 |
| `iisc-google-phd-fellowship` IISc Google PhD 奖学金项目 | ⚠️ | HTTP 502 |
| `iisc-international-phd` 印度科学院 IISc 国际博士研究项目 | ⚠️ | HTTP 502 |
| `iit-ccht-doctoral-programme` 意大利理工学院（IIT）CCHT 博士项目 | ⚠️ | HTTP 403 |
| `iit-cognitive-architecture-openings` IIT 协作技术认知架构实验室招聘页 | ⚠️ | HTTP 503 |
| `iitkgp-rolling-phd` IIT Kharagpur 滚动制博士招生 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `imprs-ml` IMPRS-ML 分子生命科学国际研究生院（慕尼黑） | ⚠️ | HTTP 403 |
| `imprs-neuro-goettingen` IMPRS Neurosciences（哥廷根） | ⚠️ | HTTP 403 |
| `imprs-qdc-dresden` IMPRS Quantum Dynamics and Control（德累斯顿） | ⚠️ | HTTP 403 |
| `imt-lucca-phd-admissions` IMT 高等研究院（Lucca）博士招生页（Systems Science / MBHT / Cultural Systems / CySec 等） | ⚠️ | HTTP 403 |
| `imtlucca-phd-programmes-admissions` IMT 卢卡高等研究院 · 博士项目招生总页（Systems Science / Cultural Systems） | ⚠️ | HTTP 403 |
| `iza-jobs-portal` IZA 劳动经济研究所招聘平台 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `jhu-xdbio-phd-2026` 约翰霍普金斯大学 XDBio 跨学科生物博士项目（2026 年 9 月入学要求） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `jk-icems-join` 京都大学 iCeMS 入学与加入页（研究生与博后） | ⚠️ | HTTP 503 |
| `jsmc-jena` 耶拿微生物通讯研究生院（JSMC） | ⚠️ | HTTP 403 |
| `kas-auslaender-promotion` 康拉德·阿登纳基金会（KAS）外国博士生奖学金（2026 指南） | ⚠️ | HTTP 403 |
| `koc-gsb-phd-business` 科奇大学商学院博士项目 | ⚠️ | HTTP 403 |
| `koc-gsse-financial-aid` 科奇大学理工研究生院奖学金与资助 | ⚠️ | HTTP 403 |
| `kuwait-university-gse` 科威特大学研究生学术卓越奖学金 | ⚠️ | HTTP 429 |
| `lanl-postdoc-eligibility-appointments` Los Alamos National Laboratory 博士后项目 · 资格与聘任说明 | ⚠️ | HTTP 403 |
| `leibniz-graduate-schools-rig` 莱布尼茨研究生院（Leibniz Graduate Schools）奖学金 | ⚠️ | HTTP 403 |
| `leibniz-individual-doctoral-projects` Leibniz 个人博士项目（Individual Doctoral Projects） | ⚠️ | HTTP 403 |
| `leipzig-gsgas-daad` 莱比锡大学 GSGAS DAAD 研究生院奖学金（GSSP） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `lille-doctoral-funding-2026` 里尔大学博士资助汇总（2026 年附件 PDF） | ⚠️ | HTTP 403 → https://egsesam.univ-lille.fr/fileadmin/user_upload/edsesam/Documents/Webinaires_Helene/Annexe_synthese_financements_de_theses_2026.pdf |
| `lille-institutional-funding` 里尔大学博士院校资助国际生选拔 | ⚠️ | HTTP 403 → https://egbsl.univ-lille.fr/en/apply-for-a-phd/selection-for-institutional-fundings |
| `lsmu-postdoctoral-fellowships` 立陶宛健康科学大学（LSMU）博士后奖学金 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `lzp-latvia-postdoc-1119` 拉脱维亚科学委员会 1.1.1.9 博后研究项目 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `lzp-postdoc-activity-1119` 拉脱维亚科学委员会（LZP）1.1.1.9 博士后研究活动 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `mahidol-cmmu-phd-scholarship` 泰国玛希隆大学管理学院 PhD 奖学金（CMMU） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `manchester-csc-joint-humanities` 曼彻斯特–CSC 联合奖学金（人文学院） | ⚠️ | ReadTimeout（超时） |
| `manchester-csc-joint-scholarship` 曼彻斯特大学 CSC 联合奖学金（2027 入学） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `manchester-heilbronn-studentship` Manchester Heilbronn Doctoral Partnership studentship | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `manchester-international-partnership-phd` 曼彻斯特大学国际合作 PhD 奖学金（4 年） | ⚠️ | ReadTimeout（超时） |
| `manchester-maths-scholarship` Manchester 数学系博士奖学金（Department of Mathematics Scholarship Award） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `manchester-peking-dual-award` 曼彻斯特大学–北京大学双学位博士（Dual-award） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `manchester-stfc-physics-studentship` 曼彻斯特大学物理与天文 STFC 博士奖学金 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `manchester-tsinghua-dual-award` 曼彻斯特大学–清华大学双学位博士（Dual-award） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `martingale-scholarships-2027` Martingale 基金会 2027 入学奖学金（数学科学与人工智能） | ⚠️ | HTTP 403 |
| `mat-bordeaux-edsc40-funded-theses` 波尔多大学 EDSC 40 带合同博士课题清单（2026/2027） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `mat-ubc-chemistry-phd-funding` 英属哥伦比亚大学（UBC）化学博士资助保障 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `mat-unisalento-materials-phd` 萨伦托大学材料与结构工程及纳米技术博士（含 IIT 资助名额） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `mfc-cdt-climate-maths` MFC CDT（未来气候数学 CDT） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ml-news` ML-news（Machine Learning News）Google Group | ⚠️ | HTTP 500 |
| `mount-sinai-icahn-phd-intl` 西奈山伊坎医学院国际学生资助页（生物医学科学与神经科学博士） | ⚠️ | HTTP 403 |
| `msca-dn-flexcat-phd-2026` MSCA 博士网络 FlexCAT：15 个博士岗位（β-catenin / 无序蛋白与癌症药物发现，多国） | ⚠️ | HTTP 403 |
| `munich-aerospace-doctoral-scholarships` Munich Aerospace 博士奖学金（TUM 与慕尼黑联邦国防军大学） | ⚠️ | HTTP 403 |
| `mur-bandi-dottorato-portal` 意大利教育部博士公告门户（bandi.mur.gov.it） | ⚠️ | HTTP 403 |
| `neurosciences-asso-intl-contracts` 法国神经科学学会：国际生博士合同汇总 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `nextstep-esrf-ill-cofund` NEXTSTEP 博士项目（ESRF 与 ILL，MSCA COFUND） | ⚠️ | HTTP 403 → https://www.esrf.fr/home/UsersAndScience/the-phd-programme-at-the-esrf/nextstep.html |
| `nl-euraxess-netherlands` EURAXESS Netherlands（荷兰科研职位与资助门户） | ⚠️ | HTTP 403 → https://www.euraxess.nl:443/ |
| `nsf-grfp` NSF GRFP（仅作提醒） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ntu-ai-for-x-postdoc` NTU AI-for-X 博士后奖学金（NRF 联合资助） | ⚠️ | HTTP 403 |
| `ntu-wen-tzu-hsiang-scholarship` 台湾大学温子祥纪念奖学金（陆生/港澳侨生，GOCFS 公告） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `nwssdtp-1-3` 西北社会科学 DTP 1+3 studentship（ESRC） | ⚠️ | ReadTimeout（超时） |
| `ohio-state-ece-funding` Ohio State ECE 博士资助 | ⚠️ | HTTP 403 |
| `paris8-arte-cd-2026-2029` 巴黎第八大学 ARTE 博士合同（2026–2029） | ⚠️ | HTTP 403 |
| `penn-state-philosophy-phd-funding` Penn State 哲学系博士资助与支持 | ⚠️ | HTTP 403 |
| `penn-state-political-science-funding` 宾州州立大学政治学系资助 | ⚠️ | HTTP 403 |
| `pitt-civil-transport-gra` 匹兹堡大学 Pitts 实验室交通/土木研究生助研岗 | ⚠️ | HTTP 503 |
| `polito-dbdmg-phd-opportunities` 都灵理工大学 DBDMG 组 · PhD 机会分类页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `polito-dottorato-42-second-session` 都灵理工大学第 42 周期博士招生第二批次 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `polito-msca-doctoral-networks-2026` 都灵理工大学 MSCA 博士网络 2026 招生入口 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `polito-phd-42nd-cycle-funded-positions` 都灵理工大学（Politecnico di Torino）第42周期博士岗位逐项更新表 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `porsche-industrial-doctorate` 保时捷博士项目（Doktorarbeit bei Porsche） | ⚠️ | HTTP 403 |
| `postech-financial-aid` POSTECH 国际研究生资助政策 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `postech-intl-admission-guide-2026` POSTECH 国际研究生招生指南（2026） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `psa-uk-opportunities` 英国政治研究协会（PSA）机会页 | ⚠️ | HTTP 520 |
| `psu-graduate-scholarship` 宋卡王子大学（PSU）硕博研究生奖学金（部分资助） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `queens-iris-join-us` 女王大学 IRIS 机器人实验室 Join us（博士） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `rbi-available-research-jobs` 鲁杰·博什科维奇研究所（RBI）研究岗位页 | ⚠️ | HTTP 403 → https://euraxess.ec.europa.eu/search?keys=RU%C4%90ER%20BO%C5%A0KOVI%C4%86%20INSTITUTE&type=job_offer |
| `research-in-germany-phd-portals` Research in Germany 博士岗位招聘门户汇总 | ⚠️ | HTTP 403 |
| `rheinmetall-doctoral-positions` 莱茵金属博士岗位（Einstieg für Doktoranden） | ⚠️ | ReadTimeout（超时） |
| `saarland-demberg-nlp-jobs` 萨尔大学 Demberg 计算语言学实验室招聘页 | ⚠️ | ReadTimeout（超时） |
| `science-careers` Science Careers | ⚠️ | HTTP 403 |
| `sfe-bourses-page` 法国生态与进化学会（SFE²）资助与奖学金栏目 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `sgbm-freiburg` 弗赖堡 Spemann 生物与医学研究生院（SGBM） | ⚠️ | HTTP 403 |
| `sk-nsp-scholarships` 斯洛伐克国家奖学金计划（NSP，博士/研究） | ⚠️ | HTTP 403 |
| `sorbonne-ed515-contrat-doctoral` 索邦大学 ED 515（复杂生命系统）博士合同 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `study-in-india-portal` Study in India 外国学生统一门户（含奖学金入口） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `sussex-ids-development-phd` 萨塞克斯大学发展研究所（IDS）博士项目 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `tml-tuebingen-jobs` 图宾根大学机器学习理论组（TML）职位页 | ⚠️ | HTTP 503 |
| `uab-csc-agreement` 巴塞罗那自治大学（UAB）CSC 协议与博士项目清单 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `uab-csc-phd-opportunities` 巴塞罗那自治大学 UAB 博士机会与 CSC 联合资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ubc-4yf-doctoral` UBC Four Year Doctoral Fellowship（4YF） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-asian-studies-phd-funding` UBC 亚洲研究博士项目（四年保障资助） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-awards` UBC Graduate Awards | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-csc-doctoral` UBC CSC 博士奖学金 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-kinesiology-phd` UBC Kinesiology 博士（最低资助保障） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-min-funding-policy` UBC 博士最低资助政策（Minimum Funding Policy） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-phd-funding` 英属哥伦比亚大学（UBC）博士资助保障 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-phd-funding-guarantee` UBC 研究生院 博士资助保障页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-rehab-sciences-phd` UBC 康复科学博士（PhD in Rehabilitation Sciences） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-sauder-marketing-phd` 不列颠哥伦比亚大学 Sauder 商学院市场营销与行为科学博士 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `ubc-stats-phd-programme` UBC 统计学 PhD 项目（最低资助保障） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `uclouvain-fsr-incoming-postdoc` UCLouvain FSR 2027 国际博士后（Incoming Postdoc） | ⚠️ | HTTP 403 |
| `ucsd-biochem-phd-stipend` UCSD 生物化学与分子生物学（BMB）博士资助页 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `uea-csc` 东英吉利大学 CSC 博士奖学金 | ⚠️ | HTTP 405 |
| `uea-phd-funding-deadlines-2027` 东英吉利大学（UEA）博士资助截止日期总表 | ⚠️ | HTTP 405 |
| `uea-senss-studentships` 东英吉利 SENSS 学生主导 ESRC 博士奖学金 | ⚠️ | HTTP 405 |
| `uk-2027-esrc-dwssdtp` ESRC 东北/西北社科博士培训伙伴关系（DWSSDTP，曼彻斯特） | ⚠️ | ReadTimeout（超时） |
| `uk-manchester-csc-joint-scholarship` 曼彻斯特大学 CSC 联合奖学金（各学科） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `unibo-42-ciclo-programmes` 博洛尼亚大学第 42 周期博士项目（数据科学与计算等） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `unibo-csc-joint-phd` 博洛尼亚大学 CSC 联合博士选拔页 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `unibo-industrial-chemistry-2026-27` 博洛尼亚大学工业化学博士（第 42 期 2026-27） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `unibo-physics-phd-2026` 博洛尼亚大学物理博士（2026–2027，INFN 合作） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `univ-eiffel-theses-candidates` Université Gustave Eiffel 博士课题（外部候选人入口） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `univpm-phd-xlii` 马尔凯理工大学（UNIVPM）XLII 周期博士公告 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-cs-osu-cse-graduate-associateship` 俄亥俄州立大学 CSE 博士研究/教学助理资助 | ⚠️ | HTTP 403 |
| `us-stanford-sail-postdoc` Stanford SAIL 博士后（AI 实验室） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-uci-bren-funding` UC Irvine Bren 信息与计算机学院博士资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-umich-presidents-postdoc` 密歇根大学总统博士后项目 | ⚠️ | HTTP 403 |

## 发生跳转的链接（可考虑更新为最终地址）

| 信源 | 详情 |
| --- | --- |
| `mpg-jobboard` | HTTP 200 → https://www.mpg.de/jobboard |
| `helmholtz-jobs` | HTTP 200 → https://www.helmholtz.de/en/career |
| `daad-china` | HTTP 200 → https://www.daad.org.cn/zh/ |
| `gks` | HTTP 200 → https://www.studyinkorea.go.kr/ko/main.do;jsessionid=G100sSLZH1L3trm235tZTWhdxt34Sy4Ki9r-Xo2x.studyinkorea20 |
| `rhodes` | HTTP 200 → https://www.rhodeshouse.ox.ac.uk/scholarships/applications/china/ |
| `hkust-pgs` | HTTP 200 → https://fytgs.hkust.edu.hk/admissions/Admissions-to-Hong-Kong-Campus/submitting-an-application/scholarships-and-fees |
| `hkbu-pg-scholarships` | HTTP 200 → https://gs.hkbu.edu.hk/fees-scholarships-and-financial-aid/other-funding-and-scholarship |
| `eduhk-phd` | HTTP 200 → https://gs.eduhk.hk/prospective/rpg/scholarship-and-financial-assistance/ |
| `cryolist` | HTTP 200 → https://lists.cryolist.org/mailman/listinfo/cryolist |
| `jrec-in` | HTTP 200 → https://jrecin.jst.go.jp/seek/SeekTop |
| `aicentre-dk-phd` | HTTP 200 → https://www.aicentre.dk/phd-fellowships |
| `saarbrucken-gscs` | HTTP 200 → https://www.graduateschool-computerscience.de/ |
| `helmholtz-graduate-schools` | HTTP 200 → https://www.helmholtz.de/en/career/careers-at-helmholtz/phd-candidates/helmholtz-graduate-schools |
| `hida-data-science-schools` | HTTP 200 → https://www.helmholtz.de/en/career/science/helmholtz-information-data-science-academy-hida |
| `fnr-pride` | HTTP 200 → https://www.fnr.lu/funding-instruments/pride/ |
| `mrc-dtp` | HTTP 200 → https://www.ukri.org/manage-your-award/support-for-ukri-funded-students/ |
| `lsz-graduate-school` | HTTP 200 → https://www.lifescience-graduateschool.uzh.ch/en.html |
| `tuwien-jobs` | HTTP 200 → https://jobs.tuwien.ac.at/Jobs |
| `polimi-phd` | HTTP 200 → https://www.polimi.it/dottorato |
| `champalimaud-indp` | HTTP 200 → https://fchampalimaud.org/education-art-science/research |
| `sutd-pgf` | HTTP 200 → https://www.sutd.edu.sg/admissions/graduate/scholarship/sutd-graduate-fellowships-scholarships/ |
| `unist-grad-admissions` | HTTP 200 → https://admg-intl.unist.ac.kr/admg-eng/admission/graduate-admissions.do |
| `usyd-rtp-international` | HTTP 200 → https://www.sydney.edu.au/scholarships/australian-government-research-training-program/rtp-international.html |
| `ibm-academic-awards-phd` | HTTP 200 → https://research.ibm.com/labs/yorktown-heights/ibm-academic-awards-program |
| `innovation-fund-denmark-industrial-phd` | HTTP 200 → https://danmarksinnovationsfond.dk/en/calls/industrial-phd-all-areas-private/ |
| `aisg-phd-fellowship` | HTTP 200 → https://aisingapore.org/research/phd-fellowship-programme/ |
| `warwick-stats-cdt-funding` | HTTP 200 → https://warwick.ac.uk/fac/sci/statistics/postgrad/centre-for-doctoral-training/fees-funding/ |
| `oxford-maths-scholarships` | HTTP 200 → https://www.maths.ox.ac.uk/study-here/postgraduate-study/scholarships |
| `oxford-gresearch-scholarship` | HTTP 200 → https://www.maths.ox.ac.uk/study-here/postgraduate-study/scholarships/g-research-graduate-scholarships |
| `plymouth-marine-research-studentship` | HTTP 200 → https://www.plymouth.ac.uk/research/institutes/marine-institute/funding-support-development-and-recognition/marine-research-plymouth-phd-studentship |
| `imperial-maths-cdts-list` | HTTP 200 → https://www.imperial.ac.uk/mathematics/postgraduate/cdts/ |
| `chem-kekule-fci` | HTTP 200 → https://www.vci.de/fonds/stipendien/kekule-stipendium/seiten-2.jsp |
| `chem-epfl-doctoral-salary` | HTTP 200 → https://www.epfl.ch/education/phd/doctoral-studies-structure/doctoral-students-salary/ |
| `chem-epfl-lpdc-openings` | HTTP 200 → https://www.epfl.ch/labs/lpdc/openings/ |
| `chem-weizmann-graduate` | HTTP 200 → https://www.weizmann.ac.il/pages/science/academics/weizmann-school-of-science |
| `chem-york-wild-fund` | HTTP 200 → https://www.york.ac.uk/chemistry/study/funding/wild-fund-scholarship/ |
| `pasteur-doctoral-programs` | HTTP 200 → https://www.pasteur.fr/en/about-us/our-missions/education/training-programs/doctoral-programs |
| `simons-fellows-to-faculty` | HTTP 200 → https://www.simonsfoundation.org/news/applications-open-for-2027-fellows-to-faculty-award-program/ |
| `fyssen-postdoc-grants` | HTTP 200 → https://www.fondationfyssen.fr/en/our-actions/study-grants/ |
| `edinburgh-neuroscience-jobs` | HTTP 200 → https://edinburghneuroscience.ed.ac.uk/opportunities/jobs-internships-phds |
| `mpi-cbs-leipzig-jobs` | HTTP 200 → https://www.mpg.de/149614/human-cognitive-and-brain-sciences?filter=jobs |
| `laval-goodman-doctoral-studentship` | HTTP 200 → https://www.pha.ulaval.ca/en/research/translate-to-english-bourses-detudes-doctorales-goodman |
| `ubc-pharmsci-funding-awards` | HTTP 200 → https://pharmsci.ubc.ca/programs/msc-phd-degrees/tuition-funding-and-awards |
| `utoronto-pharmacy-funding-policy` | HTTP 200 → https://www.pharmacy.utoronto.ca/sites/default/files/2024-07/PHM%20Graduate%20Student%20Financial%20Support%20Policy%20-%20Sept%202024_0.pdf |
| `miccai-job-board` | HTTP 200 → https://miccai.org/job-board/ |
| `hku-airlab-open-positions` | HTTP 200 → https://airlab.hku.hk/open-positions/ |
| `epfl-cvlab-positions` | HTTP 200 → https://www.epfl.ch/labs/cvlab/employment/ |
| `tudelft-bk-phd-vacatures` | HTTP 200 → https://www.tudelft.nl/bk/over-faculteit/afdelingen/architectural-engineering-and-technology/onderzoek/phd-vacatures |
| `aag-student-opportunities` | HTTP 200 → https://www.aag.org/studentopportunities/ |
| `tamu-architecture-pathways` | HTTP 200 → http://www.arch.tamu.edu/academics/graduate-programs/nextgen-built-environments-scholars/ |
| `aalto-doctoral-programme-arts-design-architecture` | HTTP 200 → https://www.aalto.fi/en/study-options/aalto-doctoral-programme-in-arts-design-and-architecture |
| `surrey-csc-awards` | HTTP 200 → https://www.surrey.ac.uk/fees-and-funding/studentships/china-scholarship-council-surrey-awards |
| `bath-china-doctoral-funding` | HTTP 200 → https://www.bath.ac.uk/campaigns/funding-opportunities-for-new-doctoral-students-from-china/ |
| `sussex-phd-funding-search` | HTTP 200 → https://www.sussex.ac.uk/study/fees-funding/phd-funding |
| `portsmouth-intl-phd-studentships` | HTTP 200 → https://www.port.ac.uk/study/postgraduate-research/funding-your-research-degree |
| `keele-pgr-funding` | HTTP 200 → https://www.keele.ac.uk:443/research/postgraduateresearch/feesandfunding/postgraduateresearchfunding/ |
| `aberystwyth-wgsss` | HTTP 200 → https://www.aber.ac.uk/en/interpol/study-with-us/postgraduate/phd/funding/ |
| `ubc-arthritis-rehab-lab` | HTTP 200 → https://arthritis.rehab.med.ubc.ca/join-us/ |
| `luce-acls-china-studies` | HTTP 200 → https://www.acls.org/news/luce-acls-program-in-china-studies-opens-2026-27-fellowship-and-grant-competitions/ |
| `stanford-shorenstein-contemporary-asia` | HTTP 200 → https://fsi.stanford.edu/news/stanfords-asia-pacific-research-center-invites-applications-2027-2029-postdoctoral-and |
| `sydney-csc-phd-scholarship` | HTTP 200 → https://www.sydney.edu.au/scholarships/e/china-scholarship-council-research-programs-scholarship.html |
| `kyoto-u-mext-scholarship` | HTTP 200 → https://www.kyoto-u.ac.jp/en/education-campus/procedures/scholarships/mext |
| `uclouvain-fsr-postdoc-incoming` | HTTP 200 → https://uclouvain.be/en/news/appel-fsr-bourses-accueil-de-post-doctorants-en-mobilite-internationale |
| `simons-society-of-fellows-junior` | HTTP 200 → https://www.simonsfoundation.org/simons-society-of-fellows/ |
| `miller-research-fellowship` | HTTP 200 → https://miller.berkeley.edu/nominate-apply/miller-research-fellowship |
| `azrieli-international-postdoc` | HTTP 200 → https://azrielifoundation.org/azrieli-fellows-news/call-for-applications-for-the-azrieli-international-postdoctoral-fellowship-2027-28/ |
| `nu-polisci-financial-support` | HTTP 200 → https://polisci.northwestern.edu/graduate/prospective/financial-support.html |
| `nu-religious-studies-funding` | HTTP 200 → https://religious-studies.northwestern.edu/graduate/funding-grants/ |
| `rice-jones-phd-financial-assistance` | HTTP 200 → https://business.rice.edu/graduate-programs/phd-business/financial-assistance |
| `ucsb-idrf-international-fellowship` | HTTP 200 → https://www.graddiv.ucsb.edu/funding-options |
| `pitt-katz-phd-tuition-aid` | HTTP 200 → https://www.business.pitt.edu/katz-admissions/admissions-tuition-phd-program/ |
| `colorado-leeds-phd-funding` | HTTP 200 → https://www.colorado.edu/business/phd/funding |
| `arizona-eller-accounting-phd` | HTTP 200 → https://eller.arizona.edu/programs/doctoral/accounting/admissions |
| `rochester-biostat-phd-financial-aid` | HTTP 200 → https://www.urmc.rochester.edu/education/graduate/phd/statistics/apply/financial-aid |
| `ub-economics-phd` | HTTP 200 → https://www.ub.edu/school-economics/phd-in-economics/ |
| `ie-university-phd-funding` | HTTP 200 → https://www.ie.edu/business-school/programs/doctorates/phd-in-management/admissions-fees/ |
| `kitp-theoretical-physics-postdoc` | HTTP 200 → https://www.kitp.ucsb.edu/about-us/careers/postdoctoral-scholars-in-theoretical-physics |
| `khk-aachen-cultures-of-research` | HTTP 200 → https://khk.rwth-aachen.de/call-for-fellowship-applications-2027-28/ |
| `ntu-npgs` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/npgs |
| `ntu-research-scholarship` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/rss |
| `ictp-saifr-postdoc` | HTTP 200 → https://www.ictp-saifr.org/postdoctoral/ |
| `mibtp-bbsrc-dtp` | HTTP 200 → https://warwick.ac.uk/fac/cross_fac/mibtp/ |
| `foodbiosystems-bbsrc-dtp` | HTTP 200 → https://ourresearch.reading.ac.uk/foodbiosystems/about-us/ |
| `cdt-aqt-applied-quantum` | HTTP 200 → https://www.aqt.ac.uk/apply/ |
| `babraham-institute-phd` | HTTP 200 → https://www.babraham.ac.uk/work-and-study/phd-opportunities |
| `jic-international-scholarship` | HTTP 200 → https://jic.ac.uk/training-careers/postgraduate-opportunities/international-scholarships/ |
| `hbigs-heidelberg` | HTTP 200 → https://www.hbigs.uni-heidelberg.de/en |
| `cim-imprs-muenster` | HTTP 200 → https://www.uni-muenster.de/CiM-IMPRS/about/introduction.html |
| `imt-lucca-phd` | HTTP 200 → https://www.imtlucca.it/news/202122-phd-call-for-applications-now-open |
| `wustl-dbbs-financial-support` | HTTP 200 → https://dbbs.wustl.edu/about/stipends-benefits-grants/ |
| `penn-phd-funding-minimum` | HTTP 200 → https://valuing-grad-students.upenn.edu/node/5 |
| `sbfi-eskas` | HTTP 200 → https://www.sbfi.admin.ch/en/swiss-government-excellence-scholarships |
| `cnes-theses-postdocs` | HTTP 200 → https://cnes.fr/theses-post-doctorats |
| `ens-paris-saclay-cdsn` | HTTP 200 → https://ens-paris-saclay.fr/en/research/phd/specific-doctoral-contracts-normaliens-cdsn |
| `boell-studienwerk-phd` | HTTP 200 → https://www.boell.de/en/applying-scholarship |
| `oxford-bsg-dphil-funding` | HTTP 200 → https://www.bsg.ox.ac.uk/study/dphil/dphil-fees-and-funding |
| `hku-law-phd-pgs` | HTTP 200 → https://www.law.hku.hk/prospective-students/research-programmes-introduction/ |
| `gii-geneva-financing-phd` | HTTP 200 → https://www.graduateinstitute.ch/scholarships |
| `nidirect-dfe-pgr-scheme` | HTTP 200 → https://www.nidirect.gov.uk/articles/department-economy-postgraduate-researcher-pgr-scheme |
| `polyu-dual-phd-degree` | HTTP 200 → https://www.polyu.edu.hk/gs/prospective-students/collaborative-phd-programmes/dual-phd-degree-programmes/ |
| `ualberta-csc-prospective` | HTTP 200 → https://www.ualberta.ca/en/admissions-programs/sponsored-student-program/csc-information-for-prospective-students.html |
| `toulouse-csc-phd` | HTTP 200 → https://en.univ-toulouse.fr/research-dynamics-phd/international-phd-programmes |
| `google-deepmind-student-researcher` | HTTP 200 → https://deepmind.google/student-researcher-program/ |
| `nyu-courant-postdoc` | HTTP 200 → https://math.nyu.edu:443/dynamic/research/postdoctoral-and-visitor-programs/ |
| `eiffel-france-excellence-campusfrance` | HTTP 200 → https://www.campusfrance.org/en/france-excellence-eiffel-scholarship-program |
| `uk-liverpool-pgr-scholarships` | HTTP 200 → https://www.liverpool.ac.uk/study/fees-and-funding/scholarships-and-bursaries/postgraduate-researchers/ |
| `uk-newcastle-pgr-funding` | HTTP 200 → https://www.ncl.ac.uk/postgraduate-research/fees-and-funding/ |
| `research-in-bavaria-phd-programmes` | HTTP 200 → https://www.research-in-bavaria.de/fileadmin-research/user_upload/Research_in_Bavaria/PDFs/PhD_Programs_in_English.pdf |
| `studyinholland-phd-info` | HTTP 200 → https://www.studyinnl.org/dutch-education/phd |
| `sheffield-fully-funded-epsrc-phds` | HTTP 200 → https://sheffield.ac.uk/postgraduate/phd/scholarships/science-engineering |
| `sutd-istd-phd-opportunities` | HTTP 200 → https://www.sutd.edu.sg/programme-listing/istd-phd-programme |
| `oru-available-positions` | HTTP 200 → https://www.oru.se/english/career/available-positions/ |
| `kaw-postdoc-calls` | HTTP 200 → https://kaw.wallenberg.org/en/funding-guide/calls |
| `uts-international-research-scholarship` | HTTP 200 → https://www.uts.edu.au/for-students/admissions-entry/scholarships/scholarships-search/international-research-scholarship |
| `rmit-vcp-phd-scholarship` | HTTP 200 → https://www.rmit.edu.au/scholarships/research/vcps |
| `rmit-international-tuition-fee-scholarships` | HTTP 200 → https://www.rmit.edu.au/scholarships/research/international-tuition-fee-scholarships |
| `grenoble-quang2-quantum-phd-call` | HTTP 200 → https://phdquantumgrenoble.univ-grenoble-alpes.fr/phd-application |
| `fraunhofer-iee-jobs-theses-phd` | HTTP 200 → https://www.iee.fraunhofer.de/en/career.html |
| `mathjobs-bonn-karriere` | HTTP 200 → https://www.mathematics.uni-bonn.de/hcm/opportunities |
| `salford-industry-phd` | HTTP 200 → https://www.salford.ac.uk/business/grow-your-business/collaborative-rd/knowledge-transfer-partnership-and-industry-phd |
| `usn-norway-industrial-phd` | HTTP 200 → https://www.usn.no/english/research/our-research-centres-and-groups/technology/norwegian-industrial-systems-engineering-research-group/research/industrial-ph-d-in-systems-engineering |
| `paris-cifre-city-call` | HTTP 200 → https://www.paris.fr/pages/cifre-un-dispositif-d-accueil-de-doctorants-a-paris-candidatez-en-ligne-4222/ |
| `uk-bbsrc-cambridge-biosciences-dtp` | HTTP 200 → https://bbsrcdtp.lifesci.cam.ac.uk/how-apply |
| `uk-glasgow-csc-phd` | HTTP 200 → https://www.gla.ac.uk/colleges/socialsciences/studentfundingopportunities/postgraduateresearch/chinascholarshipcouncilcscphdscholarships/ |
| `uk-birmingham-csc-phd` | HTTP 200 → https://www.birmingham.ac.uk/study/scholarships-funding/china-scholarship-council-university-of-birmingham-phd-scholarships |
| `uw-biostat-funding-guarantee` | HTTP 200 → https://www.biostat.washington.edu/apply/costs |
| `lund-stats-doctoral-studentship` | HTTP 200 → https://www.lusem.lu.se/organisation/department-statistics/doctoral-studies-department-statistics |
| `chem-epfl-lcsa-cramer-openings` | HTTP 200 → https://www.epfl.ch/labs/lcsa/job-openings/ |
| `chem-imperial-studentships` | HTTP 200 → https://www.imperial.ac.uk/chemistry/postgraduate/phd/phd-studentships/ |
| `chem-durham-postgrad-opportunities` | HTTP 200 → https://www.durham.ac.uk/departments/academic/chemistry/postgraduate-study/postgraduate-opportunities/ |
| `chem-rseq-jobs` | HTTP 200 → https://rseq.org/socios-y-profesionales/ofertas-de-empleo/ |
| `uol-jobs-icbm-marine` | HTTP 200 → https://uol.de/jobs |
| `noc-student-hub-opportunities` | HTTP 200 → https://www.noc.ac.uk/work-with-us/student-gateway/current-opportunities |
| `cobene-vienna-how-to-apply` | HTTP 200 → https://zid.univie.ac.at/webserver-wartung/ |
| `cobene-pooled-calls` | HTTP 200 → https://zid.univie.ac.at/webserver-wartung/ |
| `excellent-brains-coe-vienna` | HTTP 200 → https://coe.univie.ac.at/?page_id=55 |
| `az-cambridge-noncl-phd` | HTTP 200 → https://www.ats.cam.ac.uk/az-funded-non-clinical-phd-studentship |
| `imperial-bioeng-studentships` | HTTP 200 → https://www.imperial.ac.uk/bioengineering/study/postgraduate-research/doctoral/funding/studentships/ |
| `mila-research-masters-and-phd` | HTTP 200 → https://mila.quebec/en/prospective-students/research-masters-and-phd |
| `glasgow-jws-phd` | HTTP 200 → https://www.gla.ac.uk/schools/engineering/phdopportunities/ |
| `lund-vacancies` | HTTP 200 → https://www.lunduniversity.lu.se/vacancies |
| `arch-epfl-edar-enac` | HTTP 200 → https://www.epfl.ch/schools/enac/education/test_archi-hub/labs-epfl-architecture-under-construction/ |
| `arch-daniels-postdoc-funding` | HTTP 200 → https://www.daniels.utoronto.ca/research/postdoctoral-funding-opportunities/research-excellence-postdoctoral-fellowship-program |
| `arch-zgis-salzburg-news` | HTTP 200 → https://www.plus.ac.at/geoinformatik/news-jobs/news/ |
| `arch-lse-geography-phd-funding` | HTTP 200 → https://www.lse.ac.uk/geography-and-environment/study/phd/mphil-phd-frequently-asked-questions |
| `essex-government-scholarships` | HTTP 200 → https://www.essex.ac.uk/departments/government/scholarships-and-funding |
| `columbia-jsd-financing` | HTTP 200 → https://www.law.columbia.edu/admissions/graduate-admissions/jsd-admissions/financing-your-jsd-degree |
| `uaces-vacancies-board` | HTTP 200 → https://www.uaces.org/resources/vacancies |
| `jobs-ac-uk-politics-studentships` | HTTP 200 → https://www.jobs.ac.uk:443/categories/politics |
| `cambridge-ames-postgraduate-funding` | HTTP 200 → https://www.ames.cam.ac.uk/study-with-us/postgraduate-study/postgraduate-funding |
| `hku-arts-pgs-rates` | HTTP 200 → https://arts.hku.hk/admissions/research-postgraduate-admissions/research-postgraduate/ |
| `ucalgary-kinesiology-phd` | HTTP 200 → https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/kinesiology-phd |
| `utoronto-kpe-phd` | HTTP 200 → https://kpe.utoronto.ca/academics-researchfuture-students/phd-kinesiology |
| `uwe-sww-dtp-studentships` | HTTP 200 → https://www.uwe.ac.uk/research/postgraduate-research-study/studentships |
| `teesside-funded-opportunities` | HTTP 200 → https://www.tees.ac.uk/sections/research/funded_opportunities.cfm |
| `bcu-phd-studentships` | HTTP 200 → https://www.bcu.ac.uk/research/our-phds/phd-opportunities |
| `leeds-beckett-graduate-school-studentships` | HTTP 200 → https://www.leedsbeckett.ac.uk/research-degrees-and-research-students/studentships/ |
| `aston-phd-health-life-sciences` | HTTP 200 → https://www.aston.ac.uk/study/courses/phd-health-and-life-sciences-bsc |
| `bu-ssw-phd-funding` | HTTP 200 → https://www.bu.edu/ssw/admissions-financial-aid/phd-program/phd-funding/ |
| `uoregon-lundquist-phd-funding` | HTTP 200 → https://business.uoregon.edu/programs/phd/apply/tuition-financing |
| `clemson-graduate-finance` | HTTP 200 → https://www.clemson.edu/admissions/graduate-admissions/cost-and-aid.html |
| `uga-graduate-funding` | HTTP 200 → https://grad.uga.edu/funding/ |
| `miami-um-fellowship` | HTTP 200 → https://www.grad.miami.edu/about/costs-fellowships-and-other-funding/fellowships,-financial-aid,-and-other-funding-opportunities/graduate-school-fellowships-and-scholarships/um-fellowship/index.html |
| `unl-future-phd-students` | HTTP 200 → https://business.unl.edu/graduate-programs/phd-programs/phd-economics/ |
| `drexel-lebow-phd-funding` | HTTP 200 → https://www.lebow.drexel.edu/admissions/doctorate/phd-admissions/assistantships-and-financial-aid |
| `nsf-msprf-postdoc` | HTTP 200 → https://simpler.grants.gov/opportunity/793e4716-44ff-4f29-9a06-326f00e9bae9 |
| `slac-panofsky-fellowship` | HTTP 200 → https://ddst.slac.stanford.edu/career-pathways-development/panofsky-fellowship |
| `acs-postdoc-fellowship` | HTTP 200 → https://www.cancer.org/research/we-fund-cancer-research/apply-research-grant/grant-types/postdoctoral-fellowships.html |
| `nimh-postdoc-irta` | HTTP 200 → https://www.nimh.nih.gov/research/research-conducted-at-nimh/scientific-director/office-of-fellowship-and-training/fellowships-and-training-programs/postdoctoral-intramural-research-awards-program |
| `inside-higher-ed-postdoc-na` | HTTP 200 → https://careers.insidehighered.com/jobs/postdoc/north-america/4/ |
| `academia-sinica-postdoc-guidelines` | HTTP 200 → https://www.sinica.edu.tw/en/cp/331 |
| `sutd-external-fellowships` | HTTP 200 → https://www.sutd.edu.sg/admissions/graduate/scholarship/external-fellowships-scholarships |
| `uk-2027-swbio-bristol` | HTTP 200 → https://www.bristol.ac.uk/study/postgraduate/research/south-west-biosciences-doctoral-training-partnership-bbsrc/ |
| `uniud-phd-scholarships` | HTTP 200 → https://www.uniud.it/it/ricerca/lavorare-nella-ricerca/dottorato-ricerca/il-percorso-dottorale/borse-di-studio-dottorato |
| `nigms-t32-faq` | HTTP 200 → https://www.nigms.nih.gov/training/instpostdoc/Pages/Research-Training-Grant-Programs-faqs |
| `tri-i-mdphd-intl-restriction` | HTTP 200 → https://teach.weill.cornell.edu/mdphd/admissions/financial-support |
| `lund-medicine-prospective-phd` | HTTP 200 → https://www.lunduniversity.lu.se/study/study-opportunities-lund-university/doctoral-studies |
| `newberry-long-term-fellowships` | HTTP 200 → https://www.newberry.org/research/fellowships/long-term-fellowships |
| `herchel-smith-postdoc` | HTTP 200 → https://www.herchelsmith.cam.ac.uk/postdoctoral-fellowships/how-apply |
| `fes-auslaender-promotion` | HTTP 200 → https://www.fes.de/studienfoerderung/stipendium/promotionsfoerderung-fuer-auslaender-innen |
| `oist-phd-program` | HTTP 200 → https://www.oist.jp/admissions |
| `merl-phd-internships` | HTTP 200 → https://merl.com/employment/internship-openings |
| `mit-mathworks-fellows` | HTTP 200 → https://engineering.mit.edu/graduate/mathworks-fellowships |
| `graz-doctoral-admission` | HTTP 200 → https://doctorate.uni-graz.at/en/study-service/admission/ |
| `psi-phds-careercenter` | HTTP 200 → https://www.psi.ch/en/hr/job-opportunities |
| `hbku-scholarship-policy-pdf` | HTTP 200 → https://www.hbku.edu.qa/en/scholarship |
| `nyuad-global-phd-electrical-engineering` | HTTP 200 → https://nyuad.nyu.edu/en/academics/graduate-and-phd/phd-programs/global-phd-student-fellowship-in-electrical-engineering.html |
| `weizmann-merbl-lab-recruiting` | HTTP 200 → https://www.weizmann.ac.il/immunology/merbl/join-us |
| `oxford-law-clarendon-scholarships` | HTTP 200 → https://www.law.ox.ac.uk/admissions/scholarships-index/other-sources-funding-index/clarendon-scholarships |
| `umu-industrial-doctoral-school` | HTTP 200 → https://www.umu.se/en/research/research-with-us/doctoral-studies/research-schools/industrial-doctoral-school-for-research-and-innovation/call-for-applications/ |
| `research-ireland-placement` | HTTP 200 → https://www.researchireland.ie/funding/enterprise-fellowships/ |
| `eit-digital-industrial-phd` | HTTP 200 → https://www.eit.europa.eu/our-activities/opportunities/eit-digital-call-phd-students-and-partners |
| `khalifa-tsinghua-sigs-joint-phd` | HTTP 200 → https://www.ku.ac.ae/khalifa-university-phd-students-begin-jointly-awarded-program-at-tsinghua-sigs?p=124233 |
| `ihes-nonspecific-postdoc` | HTTP 200 → https://www.ihes.fr/en/applications/post-docs/non-specific-postdoctoral-programme/ |
| `cambridge-maths-phd-funding` | HTTP 200 → https://www.maths.cam.ac.uk/postgrad/research-degrees |
| `warwick-chancellors-intl-scholarship` | HTTP 200 → https://warwick.ac.uk/services/dc/schols_fund/applicants/competitions/ |
| `surrey-cs-funded-phd` | HTTP 200 → https://www.surrey.ac.uk/fees-and-funding/studentships |
| `tigp-biodiv-taiwan` | HTTP 200 → https://tigp-biodiv.biodiv.tw/index.php/2019-admission-information/ |
| `cambridge-creates-nerc-dla-funding` | HTTP 200 → https://nercdtp.esc.cam.ac.uk/prospective-students/funding-information-updated-2026-entry |
| `roehampton-leverhulme-doctoral` | HTTP 200 → https://www.roehampton.ac.uk/connected-waters/how-to-apply/ |
| `utoronto-utm-university-fellowship` | HTTP 200 → https://www.utm.utoronto.ca/cps/graduate/chemistry/financial-support/scholarshipsfellowshipsawards/regular-university-toronto |
| `nyu-shanghai-doctoral-fellowship` | HTTP 200 → https://shanghai.nyu.edu/page/neural-science-phd-program |
| `rajan-lab-comp-neuro-join` | HTTP 200 → https://www.rajanlab.com/join-us |
| `mcgill-integrated-program-neuroscience` | HTTP 200 → https://www.mcgill.ca/gradapplicants/program/neuroscience-phd |
| `uts-urban-planning-phd` | HTTP 200 → https://www.uts.edu.au/courses/doctor-of-philosophy-phd-thesis-urban-planning |
| `gsd-phd-program` | HTTP 200 → https://www.gsd.harvard.edu/offices-and-facilities/advanced-studies-programs/programs/doctor-of-philosophy/ |
| `berkeley-gateway-fellowship` | HTTP 200 → https://ihouse.berkeley.edu/live-i-house/i-house-financial-aid/gateway-fellowship-program |
| `qmul-csc-eecs-studentships` | HTTP 200 → https://www.qmul.ac.uk/eecs/phd/phd-studentships/csc-phd-studentships-in-electronic-engineering-and-computer-science/ |
| `aberdeen-elphinstone-funding` | HTTP 200 → https://www.abdn.ac.uk/elphinstone/programmes/funding/ |
| `salford-phd-studentships` | HTTP 200 → https://www.salford.ac.uk/postgraduate-research/fees |
| `surrey-doctoral-college-awards` | HTTP 200 → https://www.surrey.ac.uk/doctoral-college/prospective-postgraduate-researchers/funding-opportunities |
| `huji-frieberg-postdoc-s42` | HTTP 200 → https://eacenter.huji.ac.il/research-grants |
| `ulpgc-contratos-predoctorales-info` | HTTP 200 → https://www.ulpgc.es/sites/default/files/ArchivosULPGC/sinvestigacion/informacion_contratos_predoct_y_convocatorias.pdf |
| `unive-msca-pf-ca-foscari` | HTTP 200 → https://www.unive.it/pag/28536/#c767421 |
| `ip-paris-phd-track-scholarships` | HTTP 200 → https://www.ip-paris.fr/en/education/useful-information/scholarships |
| `simons-plant-biology-postdoc` | HTTP 200 → https://www.simonsfoundation.org/life-sciences/simons-postdoctoral-fellowships-in-plant-biology/ |
| `mcgill-postdoc-funding-portal` | HTTP 200 → https://www.mcgill.ca/gps/funding/opportunities/postdocs |
| `northwestern-energy-fellows` | HTTP 200 → https://trienens-institute.northwestern.edu/research/postdoctoral-fellowships/sustainability-and-energy-fellows-program/ |
| `fredhutch-postdoc-programs` | HTTP 200 → https://www.fredhutch.org/en/education-training/postdoctoral-fellows-programs.html |
| `ictp-phd-sandwich-programmes` | HTTP 200 → https://www.ictp.it/sti/phd-and-sandwich-programmes |
| `hkustgz-iot-thrust-phd` | HTTP 200 → https://infh.hkust-gz.edu.cn/academics/iot/about-iot/ |
| `cuhksz-lam-robotics-group` | HTTP 200 → https://freeformrobotics.org/contact/ |
| `hhmi-gilliam-fellowship` | HTTP 200 → https://www.hhmi.org/programs/gilliam-fellows |
| `qmul-doctoral-training-studentships` | HTTP 200 → https://www.qmul.ac.uk/postgraduate/research/funding_phd/doctoral-training-studentships/ |
| `ulb-uni-international-phd` | HTTP 200 → https://crcn.ulb.ac.be/news/call-for-the-international-uni-ph-d-program-2026/ |
| `ijs-cobotat-funded-phd` | HTTP 200 → https://cobotat.ijs.si/news/prosta-delovna-mesta-2/ |
| `kf-graduate-studies-scholarship` | HTTP 200 → https://www.kf.or.kr/kfEng/main.do?menuno=3793 |
| `uiuc-geography-gis-graduate-funding` | HTTP 200 → https://ggis.illinois.edu/academics/graduate-programs/assistantships-fellowships |
| `washu-complit-phd-funding` | HTTP 200 → https://complitandthought.washu.edu/complit-thought-graduate |
| `polyu-xu-shengduo-phd-studentship` | HTTP 200 → https://www.polyu.edu.hk/me/people/academic-teaching-staff/xu-shengduo-prof/-/media/3e74d0a55b494249b4ba46b79bff914a.ashx |
| `ada-postdoctoral-fellowship` | HTTP 200 → https://professional.diabetes.org/research-grants/current-funding-opportunities/postdoctoral-fellowships |
| `fr-culture-contrats-doctoraux-architecture` | HTTP 200 → https://www.culture.gouv.fr/catalogue-des-demarches-et-subventions/appels-a-projets-candidatures/attribution-des-contrats-doctoraux-du-ministere-de-la-culture-en-architecture-ville-et-paysage |
| `sheffield-science-engineering-scholarships` | HTTP 200 → https://sheffield.ac.uk/postgraduate/phd/scholarships/science-engineering/about |
| `kth-how-to-apply-phd` | HTTP 200 → https://www.kth.se/en/studies/phd/how-to-apply-1.520089 |
| `scilifelab-pulse-postdoc-programme` | HTTP 200 → https://www.scilifelab.se/research/pulse/ |
| `mcgill-fmhs-min-funding` | HTTP 200 → https://www.mcgill.ca/medhealthsci-gradstudies/fmhs-graduate-student-funding-policy/minimum-funding-packages-fmhs-graduate-programs-2025-2026 |
| `lmu-gsn-funding` | HTTP 200 → https://www.lmu.de/gsn/en/studying-at-gsn-lmu/become-a-gsn-student/ |
| `owlf-oberwolfach-leibniz-fellows` | HTTP 200 → https://www.mfo.de/scientific-program/longer-term/oberwolfach-leibniz-fellows |
| `ucalgary-linguistics-phd-funding` | HTTP 200 → https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/linguistics-phd |
| `tudelft-qutech-taminiau-quantum-control-phd` | HTTP 200 → https://www.academictransfer.com/en/jobs/364776/phd-position-on-quantum-control/ |
| `imprs-physics-of-light-erlangen` | HTTP 200 → https://mpl.mpg.de/study-work-or-visit/careers-science |
| `imperial-materials-scholarship-hub` | HTTP 200 → https://www.imperial.ac.uk/materials/study/materialsphd/phd-application-process--scholarship-hub/ |
| `imperial-materials-phd-projects` | HTTP 200 → https://www.imperial.ac.uk/materials/study/materialsphd/phdprojects/ |
| `cambridge-zoology-2026-27` | HTTP 200 → https://www.zoo.cam.ac.uk/2027-28-project-list |
| `simons-ee-fellowships` | HTTP 200 → https://www.simonsfoundation.org/life-sciences/simons-graduate-fellowships-in-ecology-and-evolution/ |
| `kent-leverhulme-space-for-nature` | HTTP 200 → https://www.kent.ac.uk/durrell-institute-conservation-ecology/research/leverhulme-scholars |
| `cifor-cgiar-germany-hub-phd` | HTTP 200 → https://hub.landscapealliance.org/phd-research-scholarship/about-phd-research-scholarship |
| `wur-phd-programme` | HTTP 200 → https://www.wur.nl/en/education/phd-programme?utm_source=verkorte_url&utm_medium=redirect |
| `jobs-ac-uk-agri-food-vet-phd` | HTTP 200 → https://www.jobs.ac.uk:443/search/agriculture-food-and-veterinary/phd |
| `penn-state-abe-job-postings` | HTTP 200 → https://abe.psu.edu/graduate/resources/job-postings |
| `imperial-life-sciences-phd-2027` | HTTP 200 → https://www.imperial.ac.uk/life-sciences/postgraduate/research/phd-opportunities/department-of-life-sciences-phd-studentships/ |
| `bu-bioinformatics-funding` | HTTP 200 → https://www.bu.edu/bioinformatics/admissions/finaid/ |
| `illc-uva-tcs-positions` | HTTP 200 → https://www.illc.uva.nl/NewsandEvents/News/Positions |
| `mpi-inf-automation-logic-offers` | HTTP 200 → https://www.mpi-inf.mpg.de/departments/automation-of-logic/offers |
| `aea-grad-funding` | HTTP 200 → https://www.aeaweb.org/resources/students/grad-prep/funding |
| `durham-business-finance-phd` | HTTP 200 → https://www.durham.ac.uk/business/about/departments/finance/phd-in-finance-/ |
| `lse-econ-costs-financial-aid` | HTTP 200 → https://www.lse.ac.uk/economics/study/research/costs-and-financial-aid |
| `lse-sociology-phd` | HTTP 200 → https://www.lse.ac.uk/sociology/phd |
| `iussp-jobs` | HTTP 200 → https://iussp.org/en/jobs |
| `asa-career-center` | HTTP 200 → https://www.asanet.org/academic-professional-resources/career-center/ |
| `kth-vehicle-maritime-aerospace-phd` | HTTP 200 → https://www.kth.se/en/sci/forskning/forskarutbildning/forskaramnet-farkostteknik-1.1304809 |
| `uts-research-degree-closing-dates` | HTTP 200 → https://www.uts.edu.au/for-students/admissions-entry/how-to-apply/masters-by-research-phd/application-closing-dates |
| `canberra-research-scholarships` | HTTP 200 → https://www.canberra.edu.au/uc-research/graduate-research/university-research-scholarships |
| `bond-hdr-scholarships` | HTTP 200 → https://bond.edu.au/researchers/research-degrees/hdr-scholarships |
| `vuw-wellington-doctoral-scholarship` | HTTP 200 → https://www.wgtn.ac.nz/scholarships/current/wellington-doctoral-scholarships |
| `birmingham-csc-joint-phd` | HTTP 200 → https://www.birmingham.ac.uk/study/scholarships-funding/china-scholarship-council-university-of-birmingham-phd-scholarships |
| `naples-federico-ii-csc-humanities` | HTTP 200 → https://www.dottoratostoria.unina.it/index.php/call-for-pre-selection-china-scholarship-council-csc-grant-2025/ |
| `leiden-graduate-school-archaeology-phd` | HTTP 200 → https://www.universiteitleiden.nl/en/archaeology/graduate-school-archaeology/prospective-phd-candidates |
| `tohoku-insc-scholarships` | HTTP 200 → https://www.insc.tohoku.ac.jp/english/scholarship-for-international-students/ |
| `kyushu-isc-mext-info` | HTTP 200 → https://www.isc.kyushu-u.ac.jp/intlweb/en/student/government-expense |
| `snu-president-fellowship` | HTTP 200 → https://oga.snu.ac.kr/ |
| `dfg-walter-benjamin` | HTTP 200 → https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/walter-benjamin |
| `tcd-trda-school-based` | HTTP 200 → https://www.tcd.ie/graduatestudies/awards/trda-school-based/ |
| `optica-workinoptics` | HTTP 200 → https://www.optica.org/careers |
| `mila-postdoctoral-fellowships` | HTTP 200 → https://mila.quebec/en/prospective-students/postdoctoral-fellowships |
| `simons-institute-research-fellowships` | HTTP 200 → https://simons.berkeley.edu/research-fellowship-call-applications |
| `ca-uoft-glse-postdoc` | HTTP 200 → https://rhse.temertymedicine.utoronto.ca/postdoctoral-fellowship-programs-awards-and-funds |
| `ca-mitacs-global-excellence-postdoc` | HTTP 200 → https://research.ucalgary.ca/opportunity/2026-2026-mitacs-accelerate-global-excellence-award-gea |
| `ca-ualberta-killam-postdoc` | HTTP 200 → https://www.ualberta.ca/en/graduate-studies/fees-funding/scholarships-awards/funding-for-postdoctoral-scholars.html |
| `ca-ubc-okanagan-min-funding` | HTTP 200 → https://okanagan.calendar.ubc.ca/faculties-schools-and-colleges/college-graduate-studies/minimum-funding |
| `ca-mcgill-desautels-tuition-aid` | HTTP 200 → https://www.mcgill.ca/desautels/programs/phd/admissions/tuition-financial-aid |
| `csc-paris-saclay-joint-doctoral` | HTTP 200 → https://www.universite-paris-saclay.fr/en/csc-joint-doctoral-programme-universite-paris-saclay-and-chinese-scholarship-council |
| `mcgill-csc-joint` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/international/csc-chinese-students |
| `utoronto-csc-joint` | HTTP 200 → https://www.sgs.utoronto.ca/awards/china-scholarship-council/ |
| `tcd-csc-joint` | HTTP 200 → https://www.tcd.ie:443/study/international/scholarships/postgraduate/csc/ |
| `goettingen-ugoe-csc-phd` | HTTP 200 → https://uni-goettingen.de/en/308975.html |
| `gu-vacancies` | HTTP 200 → https://www.gu.se/en/work-at-the-university-of-gothenburg/vacancies |
| `gu-sahlgrenska-doctoral-studies` | HTTP 200 → https://www.gu.se/en/sahlgrenska-akademin/doctoral-studies |
| `uib-vacant-positions` | HTTP 200 → https://www.uib.no/en/positions |
| `oslomet-job-openings` | HTTP 200 → https://www.oslomet.no/en/work/job-openings |
| `simula-job-openings` | HTTP 200 → https://www.simula.no/careers/job-openings |
| `wehi-international-phd-scholar` | HTTP 200 → https://www.wehi.edu.au/education/phd/international-phd-scholar-initiative/ |
| `wehi-phd-scholarship` | HTTP 200 → https://www.wehi.edu.au/education/phd/phd-scholarships/ |
| `qimr-international-phd` | HTTP 200 → https://www.qimrb.edu.au/people-and-careers/international-phd-scholarships |
| `ukro-msca-dn-guidance` | HTTP 200 → https://reg.nerc.ac.uk/ukro-closure/ |
| `centa-birmingham-phds` | HTTP 200 → https://www.birmingham.ac.uk/study/postgraduate/research/funding/centa-studentships |
| `epfl-grid-ess-positions` | HTTP 200 → https://www.epfl.ch/labs/grid-ess/grid-integrated-energy-storage-systems-lab/open-positions/ |
| `physics-utah-phd-appguide` | HTTP 200 → https://www.physics.utah.edu/wp-content/uploads/sites/65/2024/08/AppGuideF25.pdf |
| `chem-stanford-phd-financial-support` | HTTP 200 → https://chemistry.stanford.edu/academics/about-phd-program/financial-support |
| `epfl-edma-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edma-mathematics/edma-how-to-apply/ |
| `epfl-edey-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edey-energy/edey-how-to-apply/ |
| `epfl-edce-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edce-civil-and-environmental-engineering/edce-how-to-apply/ |
| `epfl-admission-criteria` | HTTP 200 → https://www.epfl.ch/education/admission/admission-2/phd-admission-criteria-and-application/ |
| `epfl-lab-head-positions` | HTTP 200 → https://www.epfl.ch/labs/head/home/open-positions/ |
| `snf-doctoral-salary-news` | HTTP 200 → https://www.snf.ch/en/kHunysxdKHpyUL8s/news/salary-increase-for-doctoral-students |
| `pasteur-paris-university-phd` | HTTP 200 → https://www.pasteur.fr/en/about-us/our-missions/education/training-programs/doctoral-programs/ppu |
| `cifar-ai-strategy-portal` | HTTP 200 → https://cifar.ca/ai/ |
| `amii-career-opportunities` | HTTP 200 → https://www.amii.ca/about/career-opportunities |
| `taiwan-scholarship-2026-guidelines` | HTTP 200 → https://www.roc-taiwan.org/Embassy_Error/error-vpn_data_url.html |
| `studyinjapan-mext-research-2027` | HTTP 200 → https://www.studyinjapan.go.jp/en/smap-stopj-applications-research.html |
| `rca-studentships` | HTTP 200 → https://www.rca.ac.uk/study/apply-to-study/funding-your-studies/funding-for-mphil-and-phd-students/ |
| `rca-funding-research-students` | HTTP 200 → https://www.rca.ac.uk/study/apply-to-study/funding-your-studies/funding-for-mphil-and-phd-students/ |
| `itatti-2027-2028-fellowships` | HTTP 200 → https://itatti.harvard.edu/news/applications-are-now-open-i-tatti%E2%80%99s-202728-fellowships |
| `sydney-architecture-design-planning-rs` | HTTP 200 → https://www.sydney.edu.au/scholarships/a/architecture-design-and-planning-research-scholarship.html |
| `oslomet-lui-educational-sciences-phd` | HTTP 200 → https://www.oslomet.no/en/study/lui/educational-sciences-phd |
| `oxford-education-dphil` | HTTP 200 → https://www.education.ox.ac.uk/course/dphil/ |
| `imprs-cim-muenster` | HTTP 200 → https://www.uni-muenster.de/CiM-IMPRS/application/ |
| `mpi-cbg-phd-program` | HTTP 200 → https://www.mpi-cbg.de/join-us/phd-program |
| `simons-dissertation-math` | HTTP 200 → https://www.simonsfoundation.org/mathematics-physical-sciences/simons-dissertation-fellowship-in-mathematics/ |
| `us-priv-brown-five-year-guarantee` | HTTP 200 → https://graduateschool.brown.edu/financing-support/funding-guarantee |
| `us-priv-nyu-global-public-health-fellowship` | HTTP 200 → https://publichealth.nyu.edu/admissions/financial-aid |
| `us-priv-bu-engineering-ece-funding` | HTTP 200 → https://www.bu.edu/eng/academics/departments-and-divisions/electrical-and-computer-engineering/resources/resources-current-students/phd-financial/ |
| `us-priv-vanderbilt-physics-aid` | HTTP 200 → https://as.vanderbilt.edu/physics-astronomy/phd-financial-aid/ |
| `us-priv-vanderbilt-philosophy-funding` | HTTP 200 → https://as.vanderbilt.edu/philosophy/graduate-admissions/ |
| `unimib-dottorato-interesse-nazionale` | HTTP 200 → https://www.unimib.it/studiare/dottorato-ricerca/corsi-dottorato/dottorato-interesse-nazionale |
| `iusspavia-phd-cycle42` | HTTP 200 → https://www.iusspavia.it:443/en/news/applications-phd-programmes-scuola-universitaria-superiore-iuss-di-pavia-42nd-cycle-academic |
| `imperial-frontier-ai-phd` | HTTP 200 → https://www.imperial.ac.uk/frontier-ai/join-us-for-a-phd/ |
| `igradu-ulm-application` | HTTP 200 → https://www.uni-ulm.de/en/einrichtungen/igradu/info-applicants |
| `helmholtz-current-calls` | HTTP 200 → https://www.helmholtz.de/en/research/current-calls-for-applications |
| `quantum-informatics-cdt` | HTTP 200 → https://www.quantuminformatics-cdt.ac.uk/apply/ |
| `kent-leverhulme-space-for-nature-phd-3` | HTTP 200 → https://www.kent.ac.uk/durrell-institute-conservation-ecology/research/leverhulme-scholars |
| `utep-eeb-funded-ra-phd` | HTTP 200 → https://www.utep.edu/science/eeb/academic%20programs/phd.html |
| `rmit-arc-coe-combs-phd` | HTTP 200 → https://www.rmit.edu.au/scholarships/research/phd-scholarship-in-arc-coe-combs |
| `mpi-susmat-admission` | HTTP 200 → https://www.mpie.de/2941513/admission |
| `sheffield-energy-storage-cdt` | HTTP 200 → https://sheffield.ac.uk/energy2050/study/phd-opportunities/energy-storage-fully-funded-phd |
| `kaust-bioscience-phd` | HTTP 200 → https://www.kaust.edu.sa/en/study/biomed/bioscience |
| `ethz-cs-doctoral-study-program` | HTTP 200 → https://inf.ethz.ch/doctorate/doctoral-study-program.html |
| `kit-kastel-doctoral-research` | HTTP 200 → https://www.kastel.kit.edu/1827.php |
| `imperial-structures-phd-study` | HTTP 200 → https://www.imperial.ac.uk/civil-engineering/research/research-disciplines/structures/study-with-us/phd-study/ |
| `mit-aeroastro-funding` | HTTP 200 → https://aeroastro.mit.edu/education/funding/ |
| `isae-supaero-doctoral-teams` | HTTP 200 → https://www.isae-supaero.fr/notre-offre-de-formations/formation-doctorale-isae-supaero/ |
| `sedarc-royal-holloway-esrc` | HTTP 200 → https://www.royalholloway.ac.uk/studying-here/fees-and-funding/research-degrees/sources-of-funding/sedarc-student-led-studentships/ |
| `senss-dtp-reading-esrc` | HTTP 200 → https://www.reading.ac.uk/doctoral-researcher-college/funding/phd-studentships/esrc-sedarc-dtp |
| `scdtp-southampton-esrc` | HTTP 200 → https://www.southampton.ac.uk/study/fees-funding/scholarships/scdtp |
| `asu-sanford-sociology-phd` | HTTP 200 → https://degrees.asu.edu/masters-phd/major/ASU00/LASOCPHD/sociology-phd |
| `dfk-paris-doctoral-contracts` | HTTP 200 → https://www.dfk-paris.org/en/page/contracts-doctoral-candidates-3928.html |
| `leiden-nwo-phd-humanities-archaeology` | HTTP 200 → https://www.universiteitleiden.nl/en/archaeology/graduate-school-archaeology/prospective-phd-candidates/nwo-call-phds-in-the-humanities |
| `classics-l-mailing-list` | HTTP 200 → https://mcl.as.uky.edu/listservs |
| `sheffield-philosophy-phd-funding` | HTTP 200 → https://sheffield.ac.uk/hpdh/postgraduate/phd-funding |
| `frankfurt-school-doctoral` | HTTP 200 → https://www.frankfurt-school.de/en/study/doctoral |
| `bis-phd-fellowship` | HTTP 200 → https://www.bis.org/about/careers/early-careers |
| `milano-bicocca-ecostatdata` | HTTP 200 → https://www.dems.unimib.it/en/news/call-applications-phd-economics-statistics-and-data-science-ecostatdata |
| `erasmus-ese-phd` | HTTP 200 → https://www.eur.nl/en/ese/working/phd-vacancies |
| `eea-job-market-hub` | HTTP 200 → https://eeassoc.org/job-market |
| `federation-hdr-scholarships` | HTTP 200 → https://www.federation.edu.au/research/graduate-research-school/scholarships-for-research |
| `potsdam-job-advertisements` | HTTP 200 → https://www.uni-potsdam.de/en/arbeiten-an-der-up/application/job-advertisements |
| `tu-berlin-irtg-stochastics` | HTTP 200 → https://www3.math.tu-berlin.de/stoch/IRTG/2025/08/25/new-call-for-applications-2/ |
| `eu-dfg-emmy-noether` | HTTP 200 → https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/emmy-noether |
| `upatras-chemeng-phd-scholarships` | HTTP 200 → https://www.chemeng.upatras.gr/en/announces/1185 |
| `microsoft-research-careers` | HTTP 200 → https://www.microsoft.com/en-us/research/careers/ |
| `ca-mcgill-intl-external-awards` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/additional-international-funding-opportunities |
| `ru-is-phd-positions` | HTTP 200 → https://www.ru.is/en/namid/find-your-study-programme/doctoral#department-of-computer-science |
| `au-csiro-topup-uow` | HTTP 200 → https://www.uow.edu.au/research/graduate-research/scholarships/items/csiro-top-up-scholarships.php |
| `qmul-csc-projects` | HTTP 200 → https://www.qmul.ac.uk/maths/postgraduate/postgraduate-research/phd-projects/current-phd-projects/china-scholarship-council-projects/ |
| `maastricht-csc-paused` | HTTP 200 → https://www.maastrichtuniversity.nl/um-china-team |
| `polito-csc-phd` | HTTP 200 → https://www.polito.it/ateneo/un-ateneo-internazionale/il-politecnico-nel-mondo/china-center/polito-csc |
| `cambridge-studentships-list` | HTTP 200 → https://www.cam.ac.uk/taxonomy/jobs-categories/studentships |
| `ntu-erian-phd` | HTTP 200 → https://www.ntu.edu.sg/erian/about-us/join-us/phd-scholarships |
| `unige-earth-sciences-jobs` | HTTP 200 → https://www.unige.ch/sciences/terre/en/informations/jobs |
| `unipd-mlg-phd-scholarships` | HTTP 200 → https://mlg.math.unipd.it/open-positions/ |
| `mila-faq` | HTTP 200 → https://mila.quebec/en/prospective-students-postdocs/frequently-asked-questions |
| `eur-research-master-economics` | HTTP 200 → https://www.eur.nl/en/research-master/research-master-economics |
| `leiden-scholarships` | HTTP 200 → https://www.universiteitleiden.nl/en/scholarships |
| `oxford-china-oxford-scholarship-fund` | HTTP 200 → https://www.oxforduchina.org/scholarships/ |
| `nanogune-combined-master-phd` | HTTP 200 → https://www.nanogune.eu/en/combined-master-phd-positions |
| `quantum-informatics-cdt-faq` | HTTP 200 → https://www.quantuminformatics-cdt.ac.uk/faqs/ |
| `imprs-tp-application` | HTTP 200 → https://www.imprs-tp.mpg.de/2879/application |
| `ictp-postdoc-positions` | HTTP 200 → https://www.ictp.it/opportunity/2026-cmsp-postdoctoral-position |
| `oead-shanghai-office` | HTTP 200 → https://oead.at/en/the-oead/oead-cooperation-offices-abroad/scientific-cooperation-office-in-shanghai |
| `mff-cuni-scholarships` | HTTP 200 → https://www.mff.cuni.cz/en/admissions/scholarships |
| `lmu-life-science-munich-csc` | HTTP 200 → https://www.bio.lmu.de/lsm/en/ |
| `clay-research-fellowship` | HTTP 200 → https://www.claymath.org/fellowship-nominations/ |
| `uchicago-linguistics-funding` | HTTP 200 → https://linguistics.uchicago.edu/graduate/graduate-program/funding |
| `uchicago-humanities-financing` | HTTP 200 → https://artshumanities.uchicago.edu/admissions/tuition-and-financial-aid |
| `brown-five-year-guarantee` | HTTP 200 → https://graduateschool.brown.edu/financing-support/funding-guarantee |
| `tulane-interdisciplinary-phd-stipend` | HTTP 200 → https://medicine.tulane.edu/interdisciplinary-phd-program/stipends-and-benefits |
| `raeng-research-fellowships-entry` | HTTP 200 → https://raeng.org.uk/programmes-and-prizes/programmes/uk-grants-and-prizes/support-for-research/research-fellowships/ |
| `nyu-shanghai-phd-programs` | HTTP 200 → https://shanghai.nyu.edu/page/phd-programs |
| `oxford-csae-economics-scholarships` | HTTP 200 → https://csae.site.ox.ac.uk/scholarships |
| `cbs-economics-doctoral-fellowships-mpi` | HTTP 200 → https://www.econ.mpg.de/419085/application |
| `cuhk-hkpfs` | HTTP 200 → https://www.gs.cuhk.edu.hk/admissions/scholarships-fees/hkpfs |
| `usc-ilab-phd-fall-2027` | HTTP 200 → https://www.i-lab.usc.edu/ |
| `aalto-doctoral-pilot` | HTTP 200 → https://www.aalto.fi/en/doctoralpilot |
| `northwestern-theory-group-prospective` | HTTP 200 → https://theory.cs.northwestern.edu/prospective-graduate-students/ |
| `hpi-database-group-positions` | HTTP 200 → https://hpi.de/en/database-group/home/ |
| `imdea-networks-job-listings` | HTTP 200 → https://networks.imdea.org/taxonomy_jobs/research-2/ |
| `rocq-prover-jobs-board` | HTTP 200 → https://discourse.rocq-prover.org/tag/jobs/15 |
| `warwick-csc-2027` | HTTP 200 → https://warwick.ac.uk/services/dc/schols_fund/applicants/competitions/ |
| `fub-csc-application-procedure` | HTTP 200 → https://www.fu-berlin.de/en/sites/china/foerdermoeglichkeiten/fuer_chinesen/csc-phd-program/application-procedure-phd/index.html |
| `bergamo-csc` | HTTP 200 → https://www.unibg.it/internazionale/destinazione-unibg/riconoscimento-dottorati-ricerca-conseguiti-allestero/phd-grants |
| `qmul-sbcs-csc` | HTTP 300 → https://www.qmul.ac.uk:443/sbcs/postgraduate/phd-programmes/studentships/china-scholarship-council |
| `ualberta-csc-medicine` | HTTP 200 → https://www.ualberta.ca/en/medicine/programs/graduatestudies/china-scholarship-council.html |
| `ucalgary-ages` | HTTP 200 → https://grad.ucalgary.ca/awards-and-funding/award-opportunities/ages |
| `mcgill-pharma-stipend` | HTTP 200 → https://www.mcgill.ca/pharma/students/graduate/financial-aid-and-funding/stipends-and-tuition-assistance |
| `stonybrook-chem-how-to-apply` | HTTP 200 → https://www.stonybrook.edu/chemistry-new/academics/phd-program/how-to-apply.html |
| `aarhus-phd-salary-employment-info` | HTTP 200 → https://phd.arts.au.dk/financing/salary-and-employment/salary-5-3 |
| `lund-psychology-phd-programme` | HTTP 200 → https://www.psy.lu.se/en/education/study-psychology-0/study-phd-programme |
| `mdc-berlin-phd` | HTTP 200 → https://www.mdc-berlin.de/phd |
| `basf-nao-asia-phd` | HTTP 200 → https://www.basf.com/cn/en/microsites/nao/how-to-apply |
| `airbus-vie-phds` | HTTP 200 → https://www.airbus.com/en/careers/students-and-graduates/vie-and-phds |
| `sfi-swiss-finance-phd` | HTTP 200 → https://www.sfi.ch/en/phd/apply-now-2022 |
| `kochi-tech-csc-kut-phd` | HTTP 200 → https://www.kochi-tech.ac.jp/english/admission/csc_kut_scholarship_program/guideline-full-time-phd-student.html |
| `canada-postdoctoral-research-award` | HTTP 200 → https://nserc-crsng.canada.ca/en/funding-opportunity/canada-postdoctoral-research-award-program |
| `us-pcm-uw-ess-funding` | HTTP 200 → https://ess.uw.edu/education/graduate-program/ |
| `dff-sapere-aude-research-leader` | HTTP 200 → https://dff.dk/en/managing-your-grant/previous-calls-and-guidelines/previous-calls-and-guidelines/expired-instruments/2026/oktober/sapere-aude-dff-research-leader-e26/ |
| `bifold-graduate-school-berlin` | HTTP 200 → https://www.bifold.berlin/education/graduate-school/admission |
| `econ-princeton-phd-admissions` | HTTP 200 → https://economics.princeton.edu/graduate-program/ |
| `iocb-prague-phd-call` | HTTP 200 → https://www.uochb.cz/en/call-for-phd-applications |
| `mcgill-csc-joint-doctoral` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/international/csc-chinese-students |
| `ucla-chemistry-biochem-phd-support` | HTTP 200 → https://www.chemistry.ucla.edu/awards-and-fellowships/ |
| `uiuc-psychology-phd-funding` | HTTP 200 → https://psychology.illinois.edu/academics/phd-psychology/psychology-phd-financial-information |
| `berkeley-psych-phd-funding` | HTTP 200 → https://psychology.berkeley.edu/graduate/admission/funding-residency |
| `calgary-werklund-phd-funding` | HTTP 200 → https://werklund.ucalgary.ca/graduate-programs/phd-funding |
| `toronto-eeb-graduate-stipends` | HTTP 200 → https://eeb.utoronto.ca/education/graduate/graduate-finances/graduate-stipends/ |
| `imprs-trust` | HTTP 200 → https://www.imprs-trust.mpg.de/ |
| `usc-dornsife-econ-phd-financial-support` | HTTP 200 → https://dornsife.usc.edu/econ/doctoral/financial-support/ |
| `bu-econ-phd-five-year-funding` | HTTP 200 → https://www.bu.edu/econ/admissions/apply-for-a-phd/expenses-financial-aid/ |
| `psi-hr-higher-education` | HTTP 200 → https://www.psi.ch/en/hr/higher-education |
| `immunosensation2-bonn-phd-program` | HTTP 200 → https://www.uni-bonn.de/de/forschung-lehre/early-career/eine-promotion-planen/spps/immunosensation3 |
| `pitt-linguistics-financial-aid` | HTTP 200 → https://www.linguistics.pitt.edu/graduate/financial-aid |
| `unito-csc-phd-preselection` | HTTP 200 → https://en.unito.it/research/opportunities-research-careers/phd/internationalization-phd-courses |
| `au-qimr-positions-vacant` | HTTP 200 → https://www.qimrb.edu.au/people-and-careers |
| `eapls-job-vacancies` | HTTP 200 → https://eapls.org/jobs/vacancies/ |
| `eso-studentship` | HTTP 200 → https://www.eso.org/sci/activities/fellowships-and-studentships/FeSt-overview/ESOstudentship.html |
| `portsmouth-cosmology-astro-phd` | HTTP 200 → https://www.port.ac.uk/study/courses/postgraduate-research/cosmology-and-astrophysics-postgraduate-research-degrees |
| `nerc-creates-dla` | HTTP 200 → https://nercdtp.esc.cam.ac.uk/nerc-creates-dla |
| `stanford-doerr-postdoc` | HTTP 200 → https://sustainability.stanford.edu/about-school/postdoctoral-resources/postdoctoral-fellowship-program/ |
| `cuhk-ees-hkpfs` | HTTP 200 → https://www.ees.cuhk.edu.hk/programme/postgraduate-programmes/postgraduate-programme/ |
| `ucalgary-geoscience-phd` | HTTP 200 → https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/geoscience-phd?page=1 |
| `ocb-jobs` | HTTP 200 → https://www.us-ocb.org/science-support/jobs-and-postdocs/ |
| `tampere-ippe-epi-phd` | HTTP 200 → https://www.tuni.fi/en/tau/doctoral-programmes/international-doctoral-programme-epidemiology-and-public-health-ippe |
| `cuhk-sph-research-postgrad` | HTTP 200 → https://sphpc.cuhk.edu.hk/rpg-programme/ |
| `cuhk-phd-public-health-hkpfs` | HTTP 200 → https://sphpc.cuhk.edu.hk/phd-in-public-health-2025-26-hong-kong-phd-fellowship-scheme-hkpfs-open-for-application-2/?lang=zh |
| `cambridge-dtp-mr` | HTTP 200 → https://www.medschl.cam.ac.uk/school-clinical-medicine-doctoral-training-programme |
| `illinois-ischool-phd-assistantships` | HTTP 200 → https://ischool.illinois.edu/academics/graduate/phd-information-sciences/tuition-financial-support |
| `indiana-luddy-funding` | HTTP 200 → https://luddy.iu.edu/cost-financial-aid/graduate-funding/index.html |
| `mila-edi-scholarships` | HTTP 200 → https://mila.quebec/en/news/twenty-one-edi-scholarships-awarded-to-exceptional-researchers |
| `schmidt-ai2050-early-career` | HTTP 200 → https://www.schmidtsciences.org/ai2050-early-career-fellows-2024/ |
| `hkust-hkpfs` | HTTP 200 → https://fytgs.hkust.edu.hk/scholarships/hong-kong-phd-fellowship-scheme |
| `sheffield-energy2050-phd` | HTTP 200 → https://sheffield.ac.uk/energy2050/study/phd-opportunities |
| `toronto-chemeng-grad` | HTTP 200 → https://chem-eng.utoronto.ca/graduate-studies/ |
| `ntu-nie-phd-scholarship` | HTTP 200 → https://www.ntu.edu.sg/nie/admissions/graduate-education/scholarships-awards/nie-phd-scholarship |
| `oise-funded-phd-cohort` | HTTP 200 → https://www.oise.utoronto.ca/registrar-students/grad-funding |
| `durham-psychology-funding` | HTTP 200 → https://www.durham.ac.uk/departments/academic/psychology/postgraduate-study/funding/ |
| `sse-phd-economics` | HTTP 200 → https://www.hhs.se/education/phd/economics/ |
| `cjbs-phd-funding` | HTTP 200 → https://www.jbs.cam.ac.uk/phd-research-masters/financing-your-phd/ |
| `nl-utrecht-phd-vacancies` | HTTP 200 → https://www.uu.nl/en/organisation/phd-programmes/starting-a-phd-track/phd-vacancies |
| `nl-rug-phd-vacancies` | HTTP 200 → https://www.rug.nl/cf/research/phd-programme/phd-vacancies |
| `be-imec-phd` | HTTP 200 → https://www.imec-int.com/en/work-at-imec/job-opportunities/phd-at-imec |
| `getty-predoc-postdoc-fellowships` | HTTP 200 → https://www.getty.edu/projects/pre-and-postdoctoral-fellowships/ |
| `uottawa-phd-intl-research-scholarship` | HTTP 200 → https://www.uottawa.ca/study/graduate-studies/funding-financing/awards/phd-student-international-research-scholarship |
| `utoronto-sgs-financial-support` | HTTP 200 → https://sgs.calendar.utoronto.ca/financial-support |
| `ucalgary-funding-floor` | HTTP 200 → https://grad.ucalgary.ca/awards-and-funding/funding-TB-students |
| `sfu-physics-funding` | HTTP 200 → https://www.sfu.ca/physics/graduate/prospective/financial-support.html |
| `laval-doctorate-tuition-exemption` | HTTP 200 → https://www.ulaval.ca/etudes/droits-de-scolarite/etudiant-de-linternational |
| `dal-research-excellence` | HTTP 200 → https://www.dal.ca/faculty/gradstudies/finance-your-studies/scholarships-bursaries/research-excellence-scholarship.html |
| `osgoode-phd-funding` | HTTP 200 → https://www.osgoode.yorku.ca/programs/graduate-program/admissions/funding-and-fees/ |
| `mcmaster-eng-min-funding` | HTTP 200 → https://www.eng.mcmaster.ca//app/uploads/2025/01/Minimum-Funding-Packages-for-Graduate-Students_May-28-2024.pdf |
| `mitacs-elevate-postdoc` | HTTP 200 → https://www.mitacs.ca/our-programs/elevate/ |
| `pims-postdoc` | HTTP 200 → https://pims.math.ca/programs/scientific/postdoctoral |
| `gov-canada-intl-scholarships` | HTTP 200 → https://www.educanada.ca/scholarships-bourses/index.aspx?lang=eng |
| `polyu-hkpfs` | HTTP 200 → https://www.polyu.edu.hk/engl/study/research-postgraduate-programme/hong-kong-phd-fellowship-scheme/ |
| `um-umps-phd` | HTTP 200 → https://grs.um.edu.mo/index.php/prospective-students/phd-funding/um-phd-scholarship/ |
| `purdue-education-grad-funding` | HTTP 200 → https://education.purdue.edu/students/graduate-students/graduate-fellowships-and-assistantships/ |
| `osu-german-admissions-funding` | HTTP 200 → https://germanic.osu.edu/graduate-studies-0/admissions-and-funding |
| `uiowa-engineering-grad-funding` | HTTP 200 → https://engineering.uiowa.edu/future-students/graduate-programs/graduate-funding |
| `uiowa-microbiology-financial-support` | HTTP 200 → https://microbiology.medicine.uiowa.edu/graduate-education/admissions/financial-support |
| `umd-smith-phd-financial-support` | HTTP 200 → https://www.rhsmith.umd.edu/programs/phd/admissions/financial-support |
| `paris-saclay-adi-cotutelle` | HTTP 200 → https://www.universite-paris-saclay.fr/en/adi-international-doctoral-cotutelle-funding-programme-2026 |
| `best-toulouse-cofund` | HTTP 200 → https://www.utoulouse.fr/medias/fichier/2025-11-27-un-nouveau-programme-doctoral-europe-en_1764324558566-pdf?INLINE=FALSE&jsonLdModel= |
| `arcane-grenoble-cofund` | HTTP 200 → https://arcane.univ-grenoble-alpes.fr/news/phd-cofund-call |
| `research-luxembourg-phd-portal` | HTTP 200 → https://www.researchluxembourg.org/en/be-with-us/start-your-phd-with-us/ |
| `us-cornell-cs-phd-funding` | HTTP 200 → https://www.cs.cornell.edu/phd-computer-science |
| `us-harvard-seas-phd-funding` | HTTP 200 → https://seas.harvard.edu/current-prospective-students/prospective-gradaute-students/funding-scholarship-graduate-programs |
| `us-umd-cs-phd-funding` | HTTP 200 → https://www.cs.umd.edu/node/25572 |
| `us-uchicago-social-sciences-funding` | HTTP 200 → https://socialsciences.uchicago.edu/admissions/funding-and-financing |
| `us-cmu-epp-phd-faq` | HTTP 200 → https://epp.engineering.cmu.edu/education/graduate/phd-program/index.html |
| `erc-avcr-selection-procedures` | HTTP 200 → https://www.avcr.cz/en/about-us/career/selection-procedures |
| `iisc-ipdf-postdoc` | HTTP 200 → https://www.iisc.ac.in/careers/post-doctoral-fellowship/ |
| `iiser-pune-intl-phd` | HTTP 200 → https://www.iiserpune.ac.in/education/programmes/international-programmes |
| `um-talent-programme-rskto` | HTTP 200 → https://rskto.um.edu.mo/umtp/ |
| `jpl-nasa-npp` | HTTP 200 → https://www.jpl.nasa.gov/site/postdocs/prospective-postdocs/postdoc-programs/ |
| `nki-vacancies` | HTTP 200 → https://www.nki.nl/careers-study/vacancies/ |
| `biozentrum-phd-faq` | HTTP 200 → https://phdstudents.biozentrum.unibas.ch/phd-at-the-biozentrum/ |
| `lancaster-funded-phd-opportunities` | HTTP 200 → https://www.lancaster.ac.uk/study/fees-and-funding/scholarships-and-bursaries/funded-phd-opportunities/ |
| `sheffield-csc-scholarship` | HTTP 200 → https://sheffield.ac.uk/postgraduate/phd/scholarships/csc |
| `sussex-csc-scholarships` | HTTP 200 → https://archive.sussex.ac.uk/study/scholarships/1756-China-Scholarship-Council-CSC-University-of-Sussex-Scholarships |
| `durham-business-phd-scholarships` | HTTP 200 → https://www.durham.ac.uk/business/programmes/phd/phd-scholarships/ |
| `loughborough-csc-phd` | HTTP 200 → https://www.lboro.ac.uk/study/postgraduate/fees-funding/research-degree-funding/china-scholarship-council/ |
| `reading-international-phd-studentships` | HTTP 200 → https://www.reading.ac.uk/doctoral-researcher-college/funding/phd-studentships/international-phd-studentships |
| `qmul-csc-joint-phd` | HTTP 200 → https://www.qmul.ac.uk/maths/postgraduate/postgraduate-research/fees-and-funding/china-scholarship-council/ |
| `amolf-phd-jobs` | HTTP 200 → https://www.amolf.nl/vacancy-overview/?position%5B%5D=phd |
| `4tu-sai-engd-vacancies` | HTTP 200 → https://www.4tu.nl/sai/education/vacancies/ |
| `ut-ids-vacancy` | HTTP 200 → https://www.utwente.nl/en/eemcs/ids/work/vacancy/ |
| `lumc-graduate-school-phd` | HTTP 200 → https://www.lumc.nl/en/research/graduate-school/becoming-a-phd-candidate/ |
| `nus-cs-phd-scholarships` | HTTP 200 → https://www.comp.nus.edu.sg/programmes/pg/phdcs/scholarships/ |
| `ntu-ccds-phd-cs-engineering` | HTTP 200 → https://www.ntu.edu.sg/spms/admissions/grad/detail/ccds-phd-computing-datascience |
| `hkust-science-rpg` | HTTP 200 → https://science.hkust.edu.hk/academic_programs/postgrad_prog/research_postgraduate/admissions |
| `uts-csc-phd` | HTTP 200 → https://www.uts.edu.au/for-students/admissions-entry/scholarships/scholarships-search/csc-uts-phd-scholarship |
| `uow-csc-joint-phd` | HTTP 200 → https://www.uow.edu.au/research/graduate-research/scholarships/items/joint-postgraduate-scholarships-program---china-scholarship-council-csc.php |
| `ufz-higrade-doctoral` | HTTP 200 → https://www.ufz.de/higrade/index.php?en=41184 |
| `mpib-jobs-page` | HTTP 200 → https://www.mpg.de/149875/human-development?filter=jobs |
| `cerge-ei-phd-economics` | HTTP 200 → https://ei.cerge-ei.cz/phd-in-economics/ |
| `jagiellonian-doctoral-scholarship` | HTTP 200 → https://phd.uj.edu.pl/pl-PL/scholarship-financial-support/regular |
| `rockefeller-graduate-program` | HTTP 200 → https://www.rockefeller.edu/education-and-training/graduate-program-in-bioscience/ |
| `mitacs-accelerate-phd-fellowship` | HTTP 200 → https://www.mitacs.ca/our-programs/accelerate-fellowship/ |
| `salk-academic-training` | HTTP 200 → https://www.salk.edu/about/careers/academic-training/ |
| `fred-hutch-graduate-program` | HTTP 200 → https://www.fredhutch.org/en/education-training/graduate-program.html |
| `uwo-ivey-phd-funding` | HTTP 200 → https://www.ivey.uwo.ca/phd/admissions/funding/ |
| `dartmouth-graduate-stipends` | HTTP 200 → https://graduate.dartmouth.edu/financial-support/funding/stipends-and-benefits |
| `mpi-cbg-imprs-celldevosys` | HTTP 200 → https://imprs.mpi-cbg.de/3869/in-a-nutshell |
| `cruk-scotland-institute-phd` | HTTP 200 → https://www.crukscotlandinstitute.ac.uk/study/studentships/ |
| `fr-paris-ed562-funding` | HTTP 200 → https://ed562.u-paris.fr/en/pages-anglais/funding/ |
| `nl-erasmus-mc-phd-routes` | HTTP 200 → https://www.eur.nl/en/erasmusmc/graduate-school/phd-tracks/obtaining-phd-position |
| `nl-erasmus-mc-scholarships` | HTTP 200 → https://www.eur.nl/en/erasmusmc/programmes/practical-matters/scholarships |
| `nl-erasmus-mc-vacancies` | HTTP 200 → https://www.werkenbijerasmusmc.nl/en/vacancies |
| `lu-lih-doctoral-training` | HTTP 200 → https://www.lih.lu/en/article/new-phd-grants/ |
| `jobs-ac-uk-microbiology-studentships` | HTTP 200 → https://www.jobs.ac.uk:443/categories/microbiology |
| `studyinfinland-doctoral-admissions` | HTTP 200 → https://www.studyinfinland.fi/admissions/doctoral-admissions |
| `edinburgh-doctoral-other-funding` | HTTP 200 → https://login.microsoftonline.com/2e9f06b0-1669-4589-8789-10a06934dc61/saml2?SAMLRequest=fVJdb9sgFP0riHcbTBNqozhR1mhapG6NancPe5kwvqnRMGSA2%2B3fj3xNnTT1BemKe86595y7WP0aDXoBH7SzNS5yihFY5Xptn2v81H7MSrxaLoIcDTuI9RQH%2Bwg%2FJwgRJaAN4vxT48lb4WTQQVg5QhBRiWb9%2BV6wnIqDd9EpZzBahwA%2BJqk7Z8M0gm%2FAv2gFT4%2F3NR5iPARBiO4POfS5VPn041iQhN9rA%2BQkT460jOwempY0zQNGmzSMtjKeFrhyGPesbT5q5V1w%2B%2Bis0RZy5UbCoNpT3tGs4LzKZvOyysrb9BRUUl7dzHrFC3LaavU6%2BPo6CEbbTY2%2F0x7mN7xSs6qcl7cgFe2LriyYTMiOQZnaQphga0OUNtaYUcYTdcZ4SytRMMHKnPPyG0a7iykftD2b%2FZ6D3bkpiE9tu8uOu2P09RpaasCXiMRJ3b%2FN5n1ieQ0EL%2F9rfxh01zkDcViQtwp%2FT%2BJLotxuds5o9RutjXGvdx5khBpHPwEmywvu3%2BNZ%2FgE%3D&RelayState=e1s1&whr=ed.ac.uk |
| `durham-csc-joint-award` | HTTP 200 → https://www.durham.ac.uk/study/scholarships/international/chinese-scholarships-council/ |
| `harvard-international-graduate-funding` | HTTP 200 → https://scholarships.harvard.edu/international-graduate-students/ |
| `stanford-bioengineering-financial-aid` | HTTP 200 → https://bioengineering.stanford.edu/academics-admission/graduate-funding |
| `cambridge-guimaraes-phd-2027` | HTTP 200 → https://guimaraes.phy.cam.ac.uk/join-our-group/ |
| `utexas-ml-research-fellows` | HTTP 200 → https://ml.utexas.edu/postdoctoral-positions |
| `us-uiuc-cs-financial-aid` | HTTP 200 → https://siebelschool.illinois.edu/admissions/financial-aid |
| `us-berkeley-statistics-phd-financial-support` | HTTP 200 → https://statistics.berkeley.edu/academics/phd/admissions/financial-support |
| `us-berkeley-grad-division-funding` | HTTP 200 → https://grad.berkeley.edu/financial/options-for-financial-support/doctoral-funding-packages/ |
| `us-utaustin-grad-recruitment-fellowship` | HTTP 200 → https://graduate.utexas.edu/funding/fellowships/grad-school/recruitment |
| `lebesgue-math-phd-grants` | HTTP 200 → https://www.lebesgue.fr/en/phdgrants |
| `bonn-hcm-postdoc-positions` | HTTP 200 → https://www.mathematics.uni-bonn.de/hsm-school/postdoctoral-positions |
| `mpifr-imprs-applicants` | HTTP 200 → https://blog.mpifr-bonn.mpg.de/imprs/ |
| `mpia-imprs-heidelberg` | HTTP 200 → https://www.imprs-hd.mpg.de/3192/Application |
| `exeter-nerc-gw4-dtp` | HTTP 200 → https://www.exeter.ac.uk/study/pg-research/funding/phdfunding/fundedcentres/gw4/ |
| `daad-china-foerderprogramme-deutschland` | HTTP 200 → https://www.daad.org.cn/de/foerderung-finden/foerderprogramme-in-deutschland/ |
| `tum-life-sciences-doctorate` | HTTP 200 → https://www.ls.tum.de/en/ls/research/doctorate/ |
| `bern-gcb-graduate-school` | HTTP 200 → https://www.gcb.unibe.ch/ |
| `ihub-iitmandi-postdoc-call` | HTTP 200 → https://www.ihubiitmandi.in/wp-content/uploads/2025/01/Advertisement-new.pdf |
| `imperial-gida-studentships` | HTTP 200 → https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/opportunities/studentships/ |
| `toronto-phs-phd-funding-policy` | HTTP 200 → https://www.dlsph.utoronto.ca/academic-policies/phd-funding-policy-for-phs-students-2025-26/ |
| `mlai-ellis-phd-admission-guidelines` | HTTP 200 → https://ellis.eu/research/phd-postdoc/guidelines-phd-admission-process |
| `psyedu-swdtp-psychology-pathway` | HTTP 200 → https://www.swdtp.ac.uk/prospective-students-and-fellows/esrc-funded-studentships/psychology/ |
| `psyedu-sheffield-psychology-phd-opportunities` | HTTP 200 → https://sheffield.ac.uk/psychology/postgraduate/phd |
| `psyedu-colorado-psych-neuro-recruiting` | HTTP 200 → https://www.colorado.edu/psych-neuro/graduate-programs/application-information/faculty-recruiting-graduate-students |
| `hec-paris-phd-fees-funding` | HTTP 200 → https://www.hec.edu/en/phd-program/financing |
| `temple-fox-marketing-phd` | HTTP 200 → https://bulletin.temple.edu/graduate/scd/fox/business-admin-marketing-phd/ |
| `utep-business-phd-2026-applications` | HTTP 200 → https://www.utep.edu/business/graduate/phd/admission.html |
| `tudelft-cheme-careers` | HTTP 200 → https://www.tudelft.nl/tnw/over-faculteit/afdelingen/chemical-engineering/career-at-cheme |
| `imperial-cheme-phd-scholarships` | HTTP 200 → https://www.imperial.ac.uk/chemical-engineering/courses/postgraduate/phd/scholarships/ |
| `green-cdt-nuclear-sheffield` | HTTP 200 → https://sheffield.ac.uk/cmbe/phd/doctoral-training-centres/nuclear-energy |
| `ainse-postgraduate-research-award` | HTTP 200 → https://www.ainse.edu.au/postgraduate/ |
| `uva-phd-vacancies-page` | HTTP 200 → https://werkenbij.uva.nl/en/vacancies?o=0&n=10&of=66546&hl=0&hh=38&s=0&f=74#vacancy-overview |
| `ut-careers-phd-page` | HTTP 200 → https://utwentecareers.nl/en/ut-as-employer/phd/ |
| `eur-university-phd-vacancies` | HTTP 200 → https://www.eur.nl/en/working-at-eur/vacancies/overview |
| `uoft-utias-funding-2026-27` | HTTP 200 → https://www.utias.utoronto.ca/graduate-students/2026-27-funding-and-financial-support/ |
| `uoft-cs-funding-tuition` | HTTP 200 → https://web.cs.toronto.edu/graduate/funding-tuition-awards |
| `waterloo-international-doctoral-funding` | HTTP 200 → https://uwaterloo.ca/environment/graduate/future-graduate-students/funding-packages/funding-international-doctoral-students |
| `ubc-okanagan-phd-minimum-funding` | HTTP 200 → https://gradstudies.ok.ubc.ca/prospective-students/research-graduate-programs/ |
| `mcgill-chiu-kay-lui-csc-fellowships` | HTTP 200 → https://www.mcgill.ca/gps/funding/chiu-kay-lui-csc-fellowships |
| `qub-dfe-media-broadcast-studentships` | HTTP 200 → https://www.qub.ac.uk/courses/postgraduate-research/phd-opportunities/dfe-fully-funded-phd-studentships--media-and-broadcast.html |
| `imperial-design-engineering-deps` | HTTP 200 → https://www.imperial.ac.uk/design-engineering/study/phd/funding-opportunities/design-engineering-scholarships/design-engineering-phd-scholarships-deps/ |
| `nus-overseas-postdoc-fellowship` | HTTP 200 → https://www.nus.edu.sg/careers/wp-content/uploads/2024/01/NUS-OPF-scheme.pdf |
| `bar-ilan-postdoc-fellowship` | HTTP 200 → https://validate.perfdrive.com/?ssa=08eab304-b569-476f-81e0-42aa7c9bde5c&ssb=50307291771&ssc=https%3A%2F%2Facad-sec.biu.ac.il%2FPostDrE&ssi=061176bc-dzai-454a-beab-1a24af491366&ssk=botmanager_support@radware.com&ssm=25277936506051561103118702490263&ssn=4c84f318154e334e859a9cfa0f8e6bfb7a5c3bb19381-ddcc-4304-8f262a&sso=fae25319-58f2dbf1973871f4582dd88cbcc0eff6197aedc0d3784d2e&ssp=65816922971793043908179307356720967&ssq=37310330597417726300205974562788868532238&ssr=NTIuMTYwLjE0OS4xMzE=&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/126.0%20Safari/537.36&ssu=&ssv=&ssw=&ssx=eyJ1em14IjoiN2ZjMDAwNzJiMTliMzQtNDA3Yy00ZWQyLTllNDUtYjJhMzNkZmMyM2I5MS0xNzkzMDA1OTc0NzMxMC0wMGJmMGNkNGZmYjM0MGU5MWIwMTAiLCJfX3V6bWYiOiI3ZjkwMDAzYmIxOTM4MS1kZGNjLTQzMDQtODMxOS01OGYyZGJmMTk3MzgxLTE3OTMwMDU5NzQ3MzEwLTAwMTY5NzIwZGZkNmMyN2VjYmMxMCIsInJkIjoiYml1LmFjLmlsIn0= |
| `hkust-fytgs-fees` | HTTP 200 → https://fytgs.hkust.edu.hk/admissions/Admissions-to-Hong-Kong-Campus/submitting-an-application/scholarships-and-fees#fees |
| `polyu-ise-fellowship-schemes` | HTTP 200 → https://www.polyu.edu.hk/gs/prospective-students/fellowship-scholarship-schemes/ |
| `nus-soc-graduate-scholarships` | HTTP 200 → https://www.comp.nus.edu.sg/financial-support/graduate-scholarships/ |
| `cshl-graduate-program` | HTTP 200 → https://www.cshl.edu/phd-program/how-to-apply/ |
| `shanahan-fellowship-allen-institute` | HTTP 200 → https://alleninstitute.org/careers/shanahan-foundation-fellowship |
| `northwestern-tgs-phd-funding-faq` | HTTP 200 → https://www.tgs.northwestern.edu/funding/about-graduate-funding/funding-faqs.html |
| `stonybrook-genetics-graduate-program` | HTTP 200 → https://www.stonybrook.edu/gradgenetics/about/welcome.html |
| `nl-tue-jobs-vacancies` | HTTP 200 → https://www.tue.nl/en/working-at-tue/vacancy-overview/ |
| `lu-fnr-afdoc` | HTTP 200 → https://www.fnr.lu/funding-instruments/afdoc/ |
| `fr-ens-csc-call-2024` | HTTP 200 → https://ens-paris-saclay.fr/en/actualite/china-scholarship-council-call-applications-2024 |
| `hhmi-hanna-gray-postdoc` | HTTP 200 → https://www.hhmi.org/programs/hanna-h-gray-fellows?utm_source=mpd&utm_medium=online-ad&utm_campaign=hgf-2022 |
| `telethon-global-call` | HTTP 200 → https://www.fondazionetelethon.it/en/what-we-do/research-management/call-for-proposals/global-call-for-scientific-talent-at-the-fondazione-telethon-institutes/ |
| `cruk-career-development-fellowship` | HTTP 200 → https://www.cancerresearchuk.org:443/for-researchers/apply-for-and-manage-your-funding/our-funding-schemes/career-development-fellowship |
| `us-rochester-urmc-biostat-financial-aid` | HTTP 200 → https://www.urmc.rochester.edu/education/graduate/phd/statistics/apply/financial-aid |
| `us-georgetown-biology-phd-funding` | HTTP 200 → https://biology.georgetown.edu/phd-program/funding/ |
| `us-georgetown-grad-school-phd-fellowships` | HTTP 200 → https://grad.georgetown.edu/financial-support/merit-based-financial-aid/fellowships/ |
| `sofinaboel-fellowship-2027` | HTTP 200 → https://www.frs-fnrs.be/fr/financements/sofinaboel-fellowships-2027 |
| `uni-lu-yadias-doctoral-fellowship-2026` | HTTP 200 → https://yadias.uni.lu/call-information/ |
| `us-umass-cics-funding` | HTTP 200 → https://www.cics.umass.edu/academics/academic-policies/graduate-programs-policies/msphd-degree-requirements/other-msphd-program-information |
| `us-brown-cs-phd` | HTTP 200 → https://cs.brown.edu/degrees/doctoral/ |
| `bath-research-with-impact-phd` | HTTP 200 → https://www.bath.ac.uk/announcements/university-of-bath-launches-research-with-impact-phd-scholarships/ |
| `aberdeen-csc-china-funding` | HTTP 200 → https://www.abdn.ac.uk/study/international/country-territory/china/funding |
| `aberystwyth-aberdoc-scholarships` | HTTP 200 → https://www.aber.ac.uk/en/study-with-us/pg-studies/scholarships/ |
| `bangor-postgraduate-funding` | HTTP 200 → https://www.bangor.ac.uk/studentfinance/postgraduate/funding |
| `hk-sg-hkust-weihan-phd-openings` | HTTP 200 → https://weihan.people.ust.hk/?page_id=40 |
| `ru-phd-physics-informed-genai-energy-2026` | HTTP 200 → https://www.ru.nl/en/working-at/job-opportunities/opportunity-expired |
| `eur-future-phd-candidates` | HTTP 200 → https://www.eur.nl/en/working-at-eur/working-areas/phd |
| `mpip-mainz-landfester-jobs` | HTTP 200 → https://www.mpip-mainz.mpg.de/en/landfester/jobs |
| `mpg-susmat-jobs-page` | HTTP 200 → https://www.mpg.de/152964/sustainable-materials?filter=jobs |
| `macdiarmid-phd-scholarships` | HTTP 200 → https://www.macdiarmid.ac.nz/about-us/join-us/phd-scholarships |
| `dodd-walls-phd-projects` | HTTP 200 → https://www.doddwalls.ac.nz/about-us/join-us |
| `unibuc-physics-phd-admission-en` | HTTP 200 → https://doctorat.fizica.unibuc.ro/Doctorat/Admitere/Main.php |
| `adum-offers-explainer` | HTTP 200 → https://www.universite-paris-saclay.fr/recherche/doctorat-et-hdr/proposer-un-sujet-de-these |
| `kiel-chem-job-links` | HTTP 200 → https://ravel.pctc.uni-kiel.de/boss/links/job-search/ |
| `mit-media-lab-mas-phd` | HTTP 200 → https://www.media.mit.edu/graduate-program/apply/ |
| `rcs-phd-mphil` | HTTP 200 → https://www.rcs.ac.uk/courses/phd-mphil/ |
| `reading-afesp-phd` | HTTP 200 → https://ourresearch.reading.ac.uk/earth-system-prediction/phd-opportunities/ |
| `gsnz-student-opportunities` | HTTP 200 → https://gsnz.org.nz/geoscience-study-and-work/student-opportunities/ |
| `nber-predoc-postings` | HTTP 200 → https://www.nber.org/career-resources/research-assistant-positions-not-nber |
| `jpal-predoc-programs` | HTTP 200 → https://www.povertyactionlab.org/resource/pre-doctoral-programs |
| `cz-gacr-postdoc-calls` | HTTP 200 → https://www.med.muni.cz/en/research-and-development/project-support/news-calls/ga-cr-calls-for-2027-announced |
| `sk-upjs-postdoc-2026` | HTTP 200 → https://www.upjs.sk/en/actualities/call-for-applications-for-postdoctoral-research-positions/ |
| `chicago-booth-phd-financial-aid` | HTTP 200 → https://www.chicagobooth.edu/phd/admissions/financial-aid |
| `scheller-phd-funding` | HTTP 200 → https://www.scheller.gatech.edu/explore-programs/phd/funding/index.html |
| `ohio-state-fisher-phd-funding` | HTTP 200 → https://fisher.osu.edu/graduate/phd-programs |
| `lmb-phd` | HTTP 200 → https://mrclmb.ac.uk/careers-and-people/phd-students/how-to-apply/ |
| `nl-maastricht-phd-vacancies-page` | HTTP 200 → https://www.maastrichtuniversity.nl/about-um/faculties/school-business-and-economics/research/phd/prospective-phd-candidate-looking |
| `nl-tudelft-radiation-science-vacancies` | HTTP 200 → https://www.tudelft.nl/tnw/over-faculteit/afdelingen/radiation-science-technology/about-us/vacancies |
| `be-vub-csc-phd` | HTTP 200 → https://www.vub.be/en/studying-vub/practical-info-for-students/how-much-does-studying-cost/financial-support/csc-vub-scholarship-programme |
| `fr-ens-csc-phd-cooperation` | HTTP 200 → https://www.ens.psl.eu/en/une-formation-d-exception/formations/echanges-internationaux/other-exchange-programs-and |
| `reading-darc-vacancies` | HTTP 200 → https://ourresearch.reading.ac.uk/met-darc/aboutus/vacancies-in-darc/ |
| `oxford-earth-sciences-dphil-admissions` | HTTP 200 → https://www.earth.ox.ac.uk/graduate/admissions |
| `mcgill-eps-funding` | HTTP 200 → https://www.mcgill.ca/eps/programs/graduate-programs/funding |
| `hku-sph-research-postgraduate` | HTTP 200 → https://sph.hku.hk/en/Teaching-and-Learning/Research-Postgraduate |
| `toronto-epic-doctoral-awards` | HTTP 200 → https://epic.utoronto.ca/opportunities/doctoral-awards/ |
| `uoregon-cms-phd-ge-funding` | HTTP 200 → https://journalism.uoregon.edu/scholarships-funding/graduate-funding |
| `ascor-uva-phd-salaried-openings` | HTTP 200 → https://ascor.uva.nl/phd-programme/faq/faq.html |
| `lindner-cincinnati-phd` | HTTP 200 → https://www.business.uc.edu/programs-degrees/graduate/phd.html |
| `iowa-state-ivy-phd` | HTTP 200 → https://www.ivybusiness.iastate.edu/academics/phd-program/ |
| `lancaster-lums-phd-funding` | HTTP 200 → https://www.lancaster.ac.uk/lums/phd/funding/ |
| `hitotsubashi-mext-business-doctoral` | HTTP 200 → https://international.hit-u.ac.jp/en/pros/mext/apply/ |
| `guelph-idts-award` | HTTP 200 → https://www.uoguelph.ca/regweb/studentfinance/apps/grawards?id=I5982 |
| `cmu-cee-phd-costs-funding` | HTTP 200 → https://cee.engineering.cmu.edu/education/graduate/costs-funding.html |
| `yale-political-science-funding` | HTTP 200 → https://politicalscience.yale.edu/academics/graduate-program/funding-professional-development-resources |
| `tamu-ece-funding-policy` | HTTP 200 → https://engineering.tamu.edu/electrical/admissions-and-aid/scholarships-aid/graduate/index.html |
| `berkeley-math-financial-aid` | HTTP 200 → https://math.berkeley.edu/graduate/funding |
| `us-cs-uf-cise-fellowship-ta` | HTTP 200 → https://cise.ufl.edu/admissions/graduate/ |
| `us-cs-colorado-boulder-funding` | HTTP 200 → https://www.colorado.edu/cs/admissions/graduate-admissions/funding-opportunities |
| `us-cs-uh-phd-assistantship` | HTTP 200 → https://www.uh.edu/nsm/computer-science/graduate/admissions/funding/index.php |
| `us-ucsc-graduate-division-support` | HTTP 200 → https://graduateadmissions.ucsc.edu/help-for-applicants/financial-support/ |
| `boeckler-promotionsstipendium` | HTTP 200 → https://www.boeckler.de/de/stipendium-fur-promovierende-2670.htm |
| `giessen-gcsc-doctoral-scholarships` | HTTP 200 → https://www.uni-giessen.de/de/fbz/ggkgcsc/graduierten-programme/index/promotion/stipendien/ausschreibung |
| `aspen-summer-program` | HTTP 200 → https://aspenphys.org/for-physicists/admissions-and-eligibility-criteria/ |
| `ictp-math-postdoc-2026` | HTTP 200 → https://2022.ictp.it/opportunity/mathematics-postdoctoral-positions-2027 |
| `cruk-scotland-centre-phd-studentship` | HTTP 200 → https://www.crukscotlandcentre.ac.uk/training/phd-studentships |
| `irish-cancer-society-fellowships` | HTTP 200 → https://www.cancer.ie/cancer-research/researchers-hub/apply-for-funding/fellowships |
| `janelia-careers-lab-postdoc` | HTTP 200 → https://www.hhmi.org/careers/janelia |
| `ualberta-math-stats-funding` | HTTP 200 → https://www.ualberta.ca/en/mathematical-and-statistical-sciences/graduate-studies/funding.html |
| `bih-phd-programme-en` | HTTP 200 → https://www.bihealth.org/en/platforms-programs/bih-biomedical-innovation-academy-bia/promotion-of-young-talents/bih-phd-program |
| `gfz-career-doctoral-entry` | HTTP 200 → https://www.gfz.de/en/career/phd-at-gfz |
| `mittag-leffler-junior-fellowship` | HTTP 200 → https://www.mittag-leffler.se/calls/call-for-junior-fellowships/ |
| `rmit-hci-phd-scholarship` | HTTP 200 → https://www.rmit.edu.au/scholarships/research/phd-scholarship-in-computer-science-human-computer-interaction |
| `cu-boulder-cs-fall-2027-recruiting` | HTTP 200 → https://www.colorado.edu/cs/admissions/graduate-admissions/discover-graduate-programs |
| `hhmi-freeman-hrabowski-scholars` | HTTP 200 → https://www.hhmi.org/programs/freeman-hrabowski-scholars |
| `cuhk-sph-phd-public-health` | HTTP 200 → https://sphpc.cuhk.edu.hk/phd-in-public-health-2025-26-hong-kong-phd-fellowship-scheme-hkpfs-open-for-application-2/ |
| `uwindsor-doctoral-entrance-award` | HTTP 200 → https://www.uwindsor.ca/graduate-studies/456/scholarships-and-awards |
| `uiceland-doctoral-grants-fund` | HTTP 200 → https://english.hi.is/research/funds-and-grants/internal-grants/phd-grants-fund |
| `usc-annenberg-communication-phd` | HTTP 200 → https://annenberg.usc.edu/admissions/tuition-and-financial-aid |
| `dzne-doctoral-researchers` | HTTP 200 → https://www.dzne.de/en/career/career-options/science/ |
| `gfz-potsdam-job-offers` | HTTP 200 → https://www.gfz.de/en/career/job-offers |
| `herbert-miami-marketing-phd` | HTTP 200 → https://www.mbs.miami.edu/graduate/find-and-compare-programs/phd-in-marketing/index.html |
| `marshall-usc-phd-funding` | HTTP 200 → https://www.marshall.usc.edu/programs/graduate-programs/phd-program |
| `arizona-infosci-phd-funding` | HTTP 200 → https://infosci.arizona.edu/phd-information/admissions-funding |
| `jic-foundation-rotation-phd` | HTTP 200 → https://jic.ac.uk/training-careers/postgraduate-opportunities/rotation-phd/ |
| `clemson-cs-phd-faq` | HTTP 200 → https://www.clemson.edu/cecas/departments/computing/academics/graduates/faq.html |
| `gatech-public-policy-phd-guaranteed-funding` | HTTP 200 → https://spp.gatech.edu/graduate/phd |
| `oulu-open-positions` | HTTP 200 → https://oulunyliopisto.varbi.com/en/ |
| `sokendai-statistical-science-phd` | HTTP 200 → http://www.soken.ac.jp/en/admission/application_info/stat/ |
| `ncsu-ece-phd-funding` | HTTP 200 → https://ece.ncsu.edu/grad/phd/funding/ |
| `ntu-npgs-scholarship` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/npgs |
| `eurasip-jobs-phd` | HTTP 200 → https://jobs.eurasip.org/ |
| `imperial-itp-phd-recruitment` | HTTP 200 → https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/intelligent-transmission/PhD-recruitment.pdf |
| `loughborough-sehs-funding-opportunities` | HTTP 200 → https://www.lboro.ac.uk/schools/sport-exercise-health-sciences/postgraduate-research/funding/ |
| `gmu-history-art-history-phd-funding` | HTTP 200 → https://historyarthistory.gmu.edu/graduate/graduate-student-resources/funding |
| `unlv-graduate-assistantship-benefits` | HTTP 200 → https://www.unlv.edu/graduatecollege/ga/benefits |
| `fwf-hertha-firnberg-postdoc` | HTTP 200 → https://zid.univie.ac.at/webserver-wartung/ |
| `siepr-young-scholars-postdoc` | HTTP 200 → https://siepr.stanford.edu/programs/young-scholars-program/young-scholars-program-postdoctoral-fellows-application |
| `jk-kaist-kim-group-openings` | HTTP 200 → https://kimgroup.kaist.ac.kr/openings/ |
| `jk-science-tokyo-wise-sss` | HTTP 200 → https://www.wise-sss.titech.ac.jp/en/news/doctoral-level-education-and-student-support-system/ |
| `rsu-doctoral-grants-erdf` | HTTP 200 → https://www.rsu.lv/en/news/second-selection-competition-doctoral-grants-riga-stradins-university-announced |
| `gu-cul-doctoral-school` | HTTP 200 → https://www.gu.se/culf/forskarskolan-cul/ansokan-till-forskarskolan-cul |
| `prismas-maxiv-doctoral` | HTTP 200 → https://www.maxiv.lu.se/education-outreach/programs-and-activities/prismas/ |
| `isye-or-doctoral-program` | HTTP 200 → https://www.isye.gatech.edu/academics/doctoral/degrees/operations-research |
| `ibm-goldstine-postdoc-fellowship` | HTTP 200 → https://research.ibm.com/labs/yorktown-heights/goldstine |
| `unsw-canberra-csc-phd` | HTTP 200 → https://www.unsw.edu.au/canberra/study-with-us/scholarships |
| `pitt-biostat-phd-faq` | HTTP 200 → https://www.publichealth.pitt.edu/biostatistics/financial-aid/frequently-asked-questions-financial-aid |
| `huji-leonard-davis-postdoc` | HTTP 200 → https://en.davis.huji.ac.il/leonard-davis-institute-post-doctoral-fellowship-2025-2026 |
| `hirszfeld-doctoral-school-recruitment` | HTTP 200 → https://szkoladoktorska.hirszfeld.pl/en/doctoral-school/recruitment/current-recruitment/ |
| `bse-upf-economics-phd-track` | HTTP 200 → https://bse.eu/masters-degrees/economics-finance/upf-phd-track |
| `cuni-physics-phd-quantum-optics` | HTTP 200 → https://www.mff.cuni.cz/en/physicsphd/f6/program-overview |
| `hku-biosch-ecology-biodiversity-postgrad` | HTTP 200 → https://www.biosch.hku.hk/research/eb-research-studies-2/ |
| `hokkaido-lfs-igp-scholarship` | HTTP 200 → https://www.lfsci.hokudai.ac.jp/en/info/2323.html |
| `edinburgh-sps-doctoral-college-scholarship` | HTTP 200 → https://www.sps.ed.ac.uk/study/prospective/postgraduate-research-programmes/scholarships/sps-awards/edinburgh-doctoral-college-scholarship-school-of-social-and-political-science |
| `manchester-mae-pgrta-dse516` | HTTP 200 → https://www.jobs.ac.uk/search/?academicDisciplineFacet[0]=engineering-and-technology&subDisciplineFacet[0]=mechanical-engineering&subDisciplineFacet[1]=aerospace-engineering&jobTypeFacet[0]=phds&salaryBandFacet[0]=10000-14999&salaryBandFacet[1]=up-to-9999&salaryBandFacet[2]=15000-19999&expired-job-redirect=true |
| `sheffield-mecheng-phd` | HTTP 200 → https://sheffield.ac.uk/mac/phd/projects |
| `dfg-gefoerderte-verfahren-jobs` | HTTP 200 → https://www.dfg.de/de/ueber-uns/geschaeftsstelle/karriereseite/dfg-gefoerderte-verfahren |
| `iuj-scholarship` | HTTP 200 → https://www.iuj.ac.jp/admissions/cost/ |
| `burnet-study` | HTTP 200 → https://www.burnet.edu.au/careers-and-study/study-at-burnet/ |
| `rki-berlin-global-health-phd` | HTTP 200 → https://www.rki.de/EN/Institute/The-RKI/Career/Training-programmes/PhD-Global-Health/phd-global-health-node.html |
| `isglobal-phd-programme` | HTTP 200 → https://www.isglobal.org/-/isglobal-phd-programme |
| `smith-school-oxford-dphil-route` | HTTP 200 → https://www.smithschool.ox.ac.uk/page/graduate-students |
| `stanford-sdss-deans-graduate-scholars` | HTTP 200 → https://sustainability.stanford.edu/our-community/access-belonging-community/community-resources/prospective-students/sdss-deans-graduate-scholars-award/ |
| `epfl-edmx-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edmx-materials-science-and-engineering/edmx-how-to-apply/ |
| `stipendium-hungaricum-study-finder` | HTTP 200 → https://stipendiumhungaricum.hu/study-finder/ |
| `stockholm-zoology-work-with-us` | HTTP 200 → https://www.su.se/english/divisions/department-of-zoology/about-the-department/work-with-us |
| `ista-phd-program` | HTTP 200 → https://phd.pages.ista.ac.at/apply/ |
| `syracuse-maxwell-phd-admission` | HTTP 200 → https://www.maxwell.syr.edu/academics/public-administration-international-affairs-department/public-administration-all-programs/phd-in-public-administration/admission |
| `ku-graduate-scholarships` | HTTP 200 → https://www.ku.ac.ae/scholarships-postgraduate |
| `fraunhofer-promovieren-guide` | HTTP 200 → https://www.fraunhofer.de/content/dam/zv/de/jobs-karriere/Promovieren-mit-Fraunhofer.pdf |
| `usyd-defence-innovation-network-phd-supplement` | HTTP 200 → https://www.sydney.edu.au/scholarships/a/defence-innovation-network-postgraduate-research-supplementary-s.html |
| `edinburgh-bs-phd-scholarships` | HTTP 200 → https://www.business-school.ed.ac.uk/phd/scholarships-funding |
| `york-history-of-art-ahrc-dla-2027` | HTTP 200 → https://www.york.ac.uk/history-of-art/study/partnerships/ |
| `nber-fellowship-calls` | HTTP 200 → https://www.nber.org/career-resources/calls-fellowship-applications |
| `mit-sfs-overview-funding` | HTTP 200 → https://sfs.mit.edu/graduate-students/funding-and-aid/departmental-funding/ |
| `rochester-phd-funding-faq` | HTTP 200 → https://rochester.edu/college/gradstudies/costs-financial-support/financial-support.html |
| `rcsi-star-phd` | HTTP 200 → https://www.rcsi.com/dublin/research-and-innovation/research-careers/star-programme/star-phd |
| `passau-dfg-rtg-2720-dpe` | HTTP 200 → https://www.wiwi.uni-passau.de/en/strategy-innovation/research/dfg-research-training-group-digital-platform-ecosystems-dpe |
| `hanken-doctoral-funding-routes` | HTTP 200 → https://www.hanken.fi/en/apply/programmes/phd-programme/financing-doctoral-studies |
| `usm-postdoctoral-research-program` | HTTP 200 → https://dgiie.usm.cl/concursos/postdoctoral-research-program-2026/ |
| `auckland-fmhs-deans-intl-doctoral` | HTTP 200 → https://www.auckland.ac.nz/en/study/scholarships-and-awards/find-a-scholarship/deans-international-doctoral-scholarship-640-fmhs.html |
| `ruc-vacant-positions` | HTTP 200 → https://ruc.dk/en/working-roskilde-university |
| `mit-fellowship-stipend-ay2027` | HTTP 200 → https://gue.mit.edu/news/ay2027-stipend-levels/ |
| `nyu-tandon-phd-fellowship` | HTTP 200 → https://engineering.nyu.edu/research/office-research/phd-student-funding |
| `jax-phd-cooperative` | HTTP 200 → https://www.jax.org/education-and-learning/pre-and-postdoctoral-program/phd-programs |
| `bcm-phd-benefits` | HTTP 200 → https://www.bcm.edu/education/graduate-school-of-biomedical-sciences/admissions/stipends-benefits/fees-and-expenses/2021-22-fees-and-expenses |
| `trent-phd-guaranteed-funding` | HTTP 200 → https://www.trentu.ca/graduatestudies/funding-tuition/funding |
| `bc-chemistry-funding` | HTTP 200 → https://www.bc.edu/content/bc-web/schools/morrissey/departments/chemistry/academics/graduate/welcome/ |
| `dtu-framebio-recruitment` | HTTP 200 → https://framebio.dtu.dk/Recruitment |
| `camk-doctoral-recruitment-2026` | HTTP 200 → https://geoplanetschool.camk.edu.pl/2026-2027-recruitment-in-the-discipline-of-astronomy/ |
| `esa-exploration-science-cofunded-phd` | HTTP 200 → https://explorationscience.esa.int/research-opportunities/call-for-co-funded-phd-research-proposals-for-esa-exploration-science/ |
| `mila-supervision-requests` | HTTP 200 → https://mila.quebec/en/prospective-students-and-postdocs/research-programs/request-supervisor |
| `riken-aip-student-recruitment` | HTTP 200 → https://aip.riken.jp/aip-osc2-0/ |
| `hessian-ai-research` | HTTP 200 → https://www.hessian.ai/research/ |
| `nef-cdt-southwest-nuclear` | HTTP 200 → https://southwestnuclearhub.ac.uk/cdt-nuclear-energy-futures/ |
| `cambridge-ieef-phd` | HTTP 200 → https://ieef.cam.ac.uk/new-phd-scholarships-available/ |
| `uclouvain-iris-financer-doctorat` | HTTP 200 → https://uclouvain.be/fr/instituts-recherche/iris/financer-son-doctorat |
| `polyu-hkpfs-portal` | HTTP 200 → https://www.polyu.edu.hk/gs/prospective-students/hkpfs/ |
| `osu-comparative-studies-graduate-funding` | HTTP 200 → https://comparativestudies.osu.edu/graduate/prospective-graduate-students/graduate-funding |
| `gatech-eas-graduate-financial-assistance` | HTTP 200 → https://eas.gatech.edu/graduate-student-financial-assistance |
| `colorado-mechanical-phd-funding` | HTTP 200 → https://www.colorado.edu/mechanical/academics/ms-programs/funding-and-fellowships |
| `ua-grad-college-ga-benefits` | HTTP 200 → https://grad.arizona.edu/gaships/ |
| `uci-socsci-funding-within` | HTTP 200 → https://www.gradstudies.socsci.uci.edu/funding/funding_within_uci.php |
| `queens-psych-funding` | HTTP 200 → https://www.queensu.ca/psychology/graduate-program/prospective-students/funding-awards-and-financial-support |
| `dal-psych-financial-information` | HTTP 200 → https://www.dal.ca/faculty/science/psychology_neuroscience/programs/graduate-programs/financial-information.html |
| `mcgill-spgh-funding-policy` | HTTP 200 → https://www.mcgill.ca/spgh/about-us/governance/graduate-student-funding-policy |
| `mqv-imprs-qst-doctoral-fellowships` | HTTP 200 → https://www.munich-quantum-valley.de/education/doctoral-fellowships |
| `huji-imric-positions` | HTTP 200 → https://imric.huji.ac.il/Open-Positions |
| `chalmers-ees-graduate-school` | HTTP 200 → https://www.chalmers.se/en/research/doctoral-studies/graduate-schools/energy-environment-and-systems/ |
| `kth-energy-phd-studies` | HTTP 200 → https://www.energy.kth.se/education/doctoral-studies/doctoral-studies-in-energy-technology-1.942695 |
| `ijs-young-researchers-fellowships` | HTTP 200 → https://www.ijs.si/ijsw/Young%20researchers%2C%20fellowships |
| `semmelweis-sh-social-science` | HTTP 200 → https://apply.stipendiumhungaricum.hu/courses/course/4126-phd-semmelweis-university-doctoral-school-social-science-sociological-sciences |
| `unicamp-pppd-imecc-2026` | HTTP 200 → https://prpg.unicamp.br/wp-content/uploads/sites/10/2026/03/Edital-PPPD-IMECC-2026.pdf |
| `tobb-etu-full-scholarship` | HTTP 200 → https://www.etu.edu.tr/en/uluslararasi/sayfa/tuition-fees-and-scholarship-opportunities-2 |
| `ozyegin-gsb-phd-scholarship` | HTTP 200 → https://library.ozyegin.edu.tr/en/phd-business/scholarship-opportunities-2026-2027 |
| `bocconi-phd-econ-fin-fellowships` | HTTP 200 → https://www.unibocconi.it/en/programs/phd/admission-phd-programs/financial-conditions |
| `sciences-po-econ-doctoral-contract` | HTTP 200 → https://www.sciencespo.fr/ecole-recherche/en/academics/phd/doctorate-economics/ |
| `ip-paris-econ-phd-track` | HTTP 200 → https://www.ip-paris.fr/education/phd-track/phd-track-economie |
| `cuhk-econ-phd-camp-2026` | HTTP 200 → https://www.econ.cuhk.edu.hk/en/news-and-events/event/cuhk-economics-phd-recruitment-camp-2026/ |
| `frbsf-sargent-dissertation-fellowship` | HTTP 200 → https://www.frbsf.org/work-with-us/careers/thomas-j-sargent-dissertation-fellowship/ |
| `harvard-hou-family-taiwan-fellowship` | HTTP 200 → https://fairbank.fas.harvard.edu/affiliation-2/hou-family-fellows-in-taiwan-studies/ |
