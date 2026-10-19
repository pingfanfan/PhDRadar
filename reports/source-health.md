# 信源可用性报告

生成时间：2026-10-19T09:10:03+00:00（由 `scripts/probe_sources.py` 在 GitHub Actions 中真实访问生成）

- 链接：2279 个，✅ 可访问 2173，⚠️ 被拦截/需登录 101，❌ 失效 5
- 抓取器：16 个，能拿到岗位 14 个

## 抓取器

| 信源 | 状态 | 样例岗位 | 耗时 | 错误 |
| --- | :-: | --- | --- | --- |
| `academictransfer` | ✅ 5 | Promovendus Governance, Vertrouwen en Data-gedreven Duurzaamheidstransities (0,8 | 101.1s |  |
| `agu-careers` | ✅ 5 | Pennsylvania State University, Department of Ecosystem Science and Management: P | 1.0s |  |
| `bluesky-phd-position` | ✅ 5 | PhD Position: Remote Sensing of Species Assembly Dynamics in Tropical Dry Decidu | 1.2s |  |
| `chemistry-world-jobs` | ⚠️ 0 条  |  | 0.8s |  |
| `cstheory-jobs` | ✅ 4 | Postdoc positions for IAS special year at Institute for Advanced Study (apply by | 0.3s |  |
| `daad-phdgermany` | ❌  |  | 1.2s | HTTPError: 403 Client Error: Forbidden for url: https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/?phd-p=1 |
| `euraxess` | ✅ 5 | Researcher in Epidemiology and Health Systems Evaluation W/M | 1.4s |  |
| `inspire-jobs` | ✅ 5 | AI-Native Physicist Fellowship | 2.1s |  |
| `jobbnorge` | ✅ 5 | PhD Research Fellowship in Circular Battery Strategies | 2.1s |  |
| `jobrxiv` | ✅ 5 | Postdoc (researcher) for Economics and Business | 2.1s |  |
| `jobs-ac-uk` | ✅ 5 | PhD Studentship: Theory of Topological Quantum Many-Body Systems | 4.4s |  |
| `physics-today-jobs` | ✅ 5 | International Max Planck Research School for Chemistry and Physics of Quantum Ma | 1.0s |  |
| `science-careers` | ✅ 5 | International Max Planck Research School for Ultrafast Imaging and Structural Dy | 0.7s |  |
| `sfn-neurojobs` | ✅ 5 | Oregon Health and Science University: Postdoctoral Fellow | 0.9s |  |
| `the-unijobs` | ✅ 5 | KINGS COLLEGE LONDON: Phd Studentship, Analytics, Environmental & Forensics | 0.5s |  |
| `varbi` | ✅ 5 | Doctoral student in Industrial Design with focus on strategic design | 10.9s |  |

## 需要关注的链接

⚠️ 多为网站拦截脚本访问（403/429）或需要登录，浏览器中通常可正常打开；❌ 需修复。

| 信源 | 状态 | 详情 |
| --- | :-: | --- |
| `cmu-hcii-phd-fellowship` 卡内基梅隆大学人机交互研究所（HCII）PhD 招生与资助 | ❌ | DNS 解析失败 |
| `cuhk-history-hkpfs` CUHK 历史学系 HKPFS 博士页 | ❌ | HTTP 404 |
| `hkust-math-pg-funding` HKUST 数学系博士研究生资助说明 | ❌ | DNS 解析失败 |
| `nioo-reading-ecosystems-space-phd` NIOO-KNAW 与乌得勒支大学 · 卫星高光谱读取生态系统 博士 | ❌ | HTTP 404 |
| `tigp-biodiv-taiwan` 中研院 TIGP-BIODIV 生物多样性与生态进化博士项目 | ❌ | DNS 解析失败 |
| `agu-findajob-geology` AGU FindAJob 地质学职位页 | ⚠️ | HTTP 403 |
| `agu-findajob-ocean-science-phd` AGU FindAJob 海洋科学博士/博后筛选页 | ⚠️ | HTTP 403 |
| `amu-doctoral-contracts` 普罗旺斯大学（AMU）博士合同竞争（2026–2029） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-ed372-financing` 艾克斯-马赛大学 ED372 博士资助 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-ed659-funding` 艾克斯-马赛大学 ED659 博士资助 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `amu-inter-ed-doctoral-contracts` Aix-Marseille 大学跨博士学院合同征集（Collège doctoral） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `aries-dtp-studentships` ARIES 博士培训伙伴奖学金（含 Cefas 合作 CASE 项目） | ⚠️ | HTTP 405 |
| `auburn-chemeng-intl-assistantship` 奥本大学化学工程博士（助研/助教资助） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `brandeis-ibs-econ-finance-phd` Brandeis 国际商学院国际经济与金融博士（全额资助） | ⚠️ | HTTP 403 |
| `brandeis-neuroscience-funding` 布兰迪斯大学（Brandeis）神经科学博士资助 | ⚠️ | HTTP 403 |
| `che-intl-scholarship-programs` 以色列高教委（CHE）国际生奖学金项目总目录 | ⚠️ | HTTP 403 |
| `chem-purdue-funding-benefits` 普渡大学化学系博士资助与福利 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `cmu-kantor-lab-openings` Kantor 课题组 · 卡内基梅隆大学 · 机器人 招生 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `cmu-ri-doctoral-robotics` CMU 机器人研究所博士项目（含学费与生活津贴） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `cnrs-jobs` CNRS 招聘门户 | ⚠️ | HTTP 503 |
| `cologne-gsgs-daad-scholarship-2026` 科隆大学地球科学研究生院 DAAD 奖学金（GSGS） | ⚠️ | HTTP 500 |
| `cornell-weinberger-prospective` 康奈尔 Kilian Weinberger · 博士招生说明 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `csd-cmu-phd-admissions-2026` CMU 计算机科学系（CSD）博士招生与资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `cyber-valley-jobs` Cyber Valley 职位总页（图宾根/斯图加特） | ⚠️ | HTTP 500 |
| `daad-ainet-postdoc-network` DAAD AInet 国际 AI 早期职业研究者项目（Postdoc-NeT-AI） | ⚠️ | HTTP 403 |
| `daad-dlr-research-fellowships` DAAD-DLR 研究奖学金（航空航天/能源/交通） | ⚠️ | HTTP 403 |
| `daad-international-programmes-db` DAAD International Programmes 数据库（英文博士项目筛选） | ⚠️ | HTTP 403 |
| `daad-phdgermany` DAAD PhDGermany 数据库 | ⚠️ | HTTP 403 |
| `daad-prime-postdoc` DAAD PRIME 博士后研究项目（德国） | ⚠️ | HTTP 403 |
| `daad-scholarship-db` DAAD 奖学金数据库 | ⚠️ | HTTP 403 |
| `dartmouth-graduate-aid-overview` 达特茅斯学院研究生资助概览 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `dartmouth-graduate-stipends` 达特茅斯学院研究生院津贴与福利 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `dartmouth-mellon-postdoc` Dartmouth Leslie Center 梅隆博士后（Mellon Postdoctoral Fellowships） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `dartmouth-neukom-postdoc-fellows` 达特茅斯学院 Neukom 计算跨学科博士后研究员 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `diw-graduate-center-phd` DIW Berlin Graduate Center 博士项目（经济学，柏林） | ⚠️ | HTTP 403 |
| `doaks-fellowships` Dumbarton Oaks 拜占庭与古典研究初级研究员奖 | ⚠️ | HTTP 403 |
| `dumbarton-oaks-mellon-landscape-fellowships` Dumbarton Oaks Mellon 园林与景观研究员奖学金 | ⚠️ | HTTP 403 |
| `eco-n-leipzig-graduiertenkolleg` ECO-N 莱比锡博士培训组（Graduiertenkolleg） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `econ-princeton-phd-admissions` 普林斯顿大学经济系博士项目（学费 + 生活津贴） | ⚠️ | HTTP 403 |
| `elte-stipendium-hungaricum` 匈牙利 Stipendium Hungaricum 博士项目（ELTE 页面） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `enerhy-cdt` EnerHy 绿氢与风能博士培训中心（CDT） | ⚠️ | HTTP 403 |
| `erc-research-in-germany-stg` Research in Germany：ERC Starting Grants 说明 | ⚠️ | HTTP 403 |
| `es-jobs-net` ES_JOBS_NET 地球与环境科学岗位列表（UCAR） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `esrf-phd-conditions` 欧洲同步辐射装置（ESRF）· 博士生项目与招聘条件 | ⚠️ | HTTP 403 |
| `esrf-phd-programme` ESRF 欧洲同步辐射装置博士项目（PhD Programme） | ⚠️ | HTTP 403 |
| `fau-imprs-sc` IMPRS-SC 突触与神经回路国际马普研究生院（FAU） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `forum-1p3a-rit-yidan-hu-phd-2026` 1point3acres · RIT Yidan Hu 数据隐私/AI 安全全奖博士招生 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fr-ens-lyon-csc` ENS de Lyon CSC 博士资助 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `fraunhofer-individual-doctoral-projects` Fraunhofer 个人博士项目（Individual Doctoral Projects） | ⚠️ | HTTP 403 |
| `gal-predoc-usc` 加利西亚大区预博士资助（含 USC） | ⚠️ | HTTP 500 |
| `getty-predoc-postdoc-fellowships` Getty 基金会博士前与博后研究员（艺术史） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `glasgow-mvls-funded-research-opportunities` 格拉斯哥大学 MVLS 学院 Funded Research Opportunities（带奖博士项目列表） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `grass-fellowship-mbl` Grass Fellowship（MBL 神经科学夏季研究基金） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `graz-doctoral-admission` 格拉茨大学 博士学院入学说明 | ⚠️ | HTTP 403 |
| `gurdon-wellcome-masters-phd` Gurdon Institute（剑桥）Wellcome Masters+PhD 发育生物学项目 | ⚠️ | HTTP 403 |
| `helsinki-doctoral-researcher-positions` 赫尔辛基大学博士生院统一资助的博士研究员职位 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `herbert-miami-marketing-phd` University of Miami Herbert 商学院营销学博士 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `hku-cs-how-to-apply-2027` HKU 计算机科学系 2027 年研究型博士申请指南 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `hku-cs-phd-admissions` HKU 计算与数据科学学院 PhD/MPhil 招生页 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `huji-doctoral-research` 希伯来大学国际办公室：博士研究 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `huji-postdoc-fellowships-2027` 希伯来大学博士后奖学金（2027–28 学年，Scholarship Portal 申请） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `huji-racah-international-students` 希伯来大学 Racah 物理研究所国际学生与博士资助说明 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `icmat-severo-ochoa-fpi-past` ICMAT Severo Ochoa 博士研究奖学金（FPI，马德里） | ⚠️ | ReadTimeout（超时） |
| `ictp-phd-sandwich-programmes` ICTP 博士与 sandwich 项目（发展中国家博士生） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ictp-postdoctoral-opportunities` ICTP 博士后职位（的里雅斯特） | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `icys-nims-recruitment` NIMS 国际青年科学家中心（ICYS）研究员（博后）招募 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ieee-photonics-graduate-scholarship` IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship） | ⚠️ | HTTP 403 |
| `ieee-photonics-gs-scholarship` IEEE Photonics Society 研究生奖学金（Graduate Student Scholarship） | ⚠️ | HTTP 403 |
| `iiser-pune-intl-admissions` IISER Pune 国际生招生总页 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `iitb-ipdf-postdoc` IIT Bombay 博士后研究员（IPDF） | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `iitkgp-rolling-phd` IIT Kharagpur 滚动制博士招生 | ⚠️ | ConnectionError（连接失败，可能限制境外访问） |
| `imani-uconn-robotics-phd-2027` Farhad Imani 课题组 · 康涅狄格大学 (UConn) · 机器人与智能制造 招生 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `imprs-gs-goettingen` IMPRS Genome Science（哥廷根，与 GönomiX 联合招生） | ⚠️ | HTTP 502 |
| `imprs-ml` IMPRS-ML 分子生命科学国际研究生院（慕尼黑） | ⚠️ | HTTP 403 |
| `imprs-neuro-goettingen` IMPRS Neurosciences（哥廷根） | ⚠️ | HTTP 403 |
| `imprs-qdc-dresden` IMPRS Quantum Dynamics and Control（德累斯顿） | ⚠️ | HTTP 403 |
| `indiana-kelley-phd-financial-aid` 印第安纳大学 Kelley 商学院博士财务资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `iowa-state-ivy-phd` 爱荷华州立大学 Ivy 商学院博士助教/助研资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `iucaa-phd-inat` IUCAA 博士项目（INAT/JEST 入学） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `jsmc-jena` 耶拿微生物通讯研究生院（JSMC） | ⚠️ | HTTP 403 |
| `jsps-postdoc-japan` JSPS 外国人特别研究员（Standard，赴日博士后） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `kas-auslaender-promotion` 康拉德·阿登纳基金会（KAS）外国博士生奖学金（2026 指南） | ⚠️ | HTTP 403 |
| `koc-gsb-phd-business` 科奇大学商学院博士项目 | ⚠️ | HTTP 403 |
| `koc-gsse-financial-aid` 科奇大学理工研究生院奖学金与资助 | ⚠️ | HTTP 403 |
| `leibniz-graduate-schools-rig` 莱布尼茨研究生院（Leibniz Graduate Schools）奖学金 | ⚠️ | HTTP 403 |
| `leibniz-individual-doctoral-projects` Leibniz 个人博士项目（Individual Doctoral Projects） | ⚠️ | HTTP 403 |
| `mit-media-lab-mas-phd` MIT Media Lab 媒体艺术与科学（MAS 转 PhD） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `mount-sinai-icahn-phd-intl` 西奈山伊坎医学院国际学生资助页（生物医学科学与神经科学博士） | ⚠️ | HTTP 403 |
| `nims-employment-en` NIMS 英文招聘总页 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `northwestern-chem-financial-support` Northwestern 化学系研究生资助说明 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `northwestern-ibis-faq` 西北大学综合生物科学（IBiS）博士项目 FAQ | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `ntu-ai-for-x-postdoc` NTU AI-for-X 博士后奖学金（NRF 联合资助） | ⚠️ | HTTP 403 |
| `science-careers` Science Careers | ⚠️ | HTTP 403 |
| `sedarc-sussex-esrc-2027` SEDarc (ESRC) PhD 奖学金 · 萨塞克斯大学 · 2027 入学 | ⚠️ | ConnectTimeout（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `stsci-brinson-prize-fellowship` STScI Brinson 奖学金（天体物理博士后） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `uab-gbs-benefits` 阿拉巴马大学伯明翰分校生物医学研究生院（GBS）资助与福利 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `uea-csc` 东英吉利大学 CSC 博士奖学金 | ⚠️ | HTTP 405 |
| `uea-phd-funding-deadlines-2027` 东英吉利大学（UEA）博士资助截止日期总表 | ⚠️ | HTTP 405 |
| `uea-senss-studentships` 东英吉利 SENSS 学生主导 ESRC 博士奖学金 | ⚠️ | HTTP 405 |
| `us-cornell-cs-phd-funding` Cornell CS PhD 资助保障（FAQ） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-northwestern-philosophy-financial` Northwestern 哲学系博士资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-northwestern-stats-financial-aid` Northwestern 统计与数据科学博士资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-priv-northwestern-tgs-funding-faqs` Northwestern 研究生院博士资助常见问题（含国际生条款） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-priv-nyu-global-public-health-fellowship` NYU 全球公共卫生博士奖学金（五年） | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-uconn-rmme-phd-funding` 康涅狄格大学 RMME 博士资助 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |
| `us-umd-cs-phd-funding` UMD 计算机系博士资助保障 | ⚠️ | SSLError（境外服务器访问受限或证书问题，浏览器中通常可打开） |

## 发生跳转的链接（可考虑更新为最终地址）

| 信源 | 详情 |
| --- | --- |
| `mpg-jobboard` | HTTP 200 → https://www.mpg.de/jobboard |
| `helmholtz-jobs` | HTTP 200 → https://www.helmholtz.de/en/career |
| `daad-china` | HTTP 200 → https://www.daad.org.cn/zh/ |
| `rhodes` | HTTP 200 → https://www.rhodeshouse.ox.ac.uk/scholarships/applications/china/ |
| `hkust-pgs` | HTTP 200 → https://fytgs.hkust.edu.hk/admissions/Admissions-to-Hong-Kong-Campus/submitting-an-application/scholarships-and-fees |
| `hkbu-pg-scholarships` | HTTP 200 → https://gs.hkbu.edu.hk/fees-scholarships-and-financial-aid/other-funding-and-scholarship |
| `eduhk-phd` | HTTP 200 → https://gs.eduhk.hk/prospective/rpg/scholarship-and-financial-assistance/ |
| `cryolist` | HTTP 200 → https://lists.cryolist.org/mailman/listinfo/cryolist |
| `jrec-in` | HTTP 200 → https://jrecin.jst.go.jp/seek/SeekTop |
| `aicentre-dk-phd` | HTTP 200 → https://www.aicentre.dk/phd-fellowships |
| `hida-data-science-schools` | HTTP 200 → https://www.helmholtz.de/en/career/science/helmholtz-information-data-science-academy-hida |
| `bms-berlin` | HTTP 200 → https://www.math-berlin.de/application |
| `fnr-pride` | HTTP 200 → https://www.fnr.lu/funding-instruments/pride/ |
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
| `imperial-maths-cdts-list` | HTTP 200 → https://www.imperial.ac.uk/mathematics/postgraduate/cdts/ |
| `chem-epfl-doctoral-salary` | HTTP 200 → https://www.epfl.ch/education/phd/doctoral-studies-structure/doctoral-students-salary/ |
| `chem-epfl-lpdc-openings` | HTTP 200 → https://www.epfl.ch/labs/lpdc/openings/ |
| `chem-weizmann-graduate` | HTTP 200 → https://www.weizmann.ac.il/pages/science/academics/weizmann-school-of-science |
| `chem-york-wild-fund` | HTTP 200 → https://www.york.ac.uk/chemistry/study/funding/wild-fund-scholarship/ |
| `pasteur-doctoral-programs` | HTTP 200 → https://www.pasteur.fr/en/about-us/our-missions/education/training-programs/doctoral-programs |
| `simons-fellows-to-faculty` | HTTP 200 → https://www.simonsfoundation.org/news/applications-open-for-2027-fellows-to-faculty-award-program/ |
| `fyssen-postdoc-grants` | HTTP 200 → https://www.fondationfyssen.fr/en/our-actions/study-grants/ |
| `edinburgh-neuroscience-jobs` | HTTP 200 → https://edinburghneuroscience.ed.ac.uk/opportunities/jobs-internships-phds |
| `laval-goodman-doctoral-studentship` | HTTP 200 → https://www.pha.ulaval.ca/en/research/translate-to-english-bourses-detudes-doctorales-goodman |
| `ubc-pharmsci-funding-awards` | HTTP 200 → https://pharmsci.ubc.ca/programs/msc-phd-degrees/tuition-funding-and-awards |
| `hku-airlab-open-positions` | HTTP 200 → https://airlab.hku.hk/open-positions/ |
| `epfl-cvlab-positions` | HTTP 200 → https://www.epfl.ch/labs/cvlab/employment/ |
| `tudelft-bk-phd-vacatures` | HTTP 200 → https://www.tudelft.nl/bk/over-faculteit/afdelingen/architectural-engineering-and-technology/onderzoek/phd-vacatures |
| `surrey-csc-awards` | HTTP 200 → https://www.surrey.ac.uk/fees-and-funding/studentships/china-scholarship-council-surrey-awards |
| `bath-china-doctoral-funding` | HTTP 200 → https://www.bath.ac.uk/campaigns/funding-opportunities-for-new-doctoral-students-from-china/ |
| `ubc-kinesiology-phd` | HTTP 200 → https://www.grad.ubc.ca/prospective-students/graduate-degree-programs/phd-kinesiology |
| `stanford-shorenstein-contemporary-asia` | HTTP 200 → https://fsi.stanford.edu/news/stanfords-asia-pacific-research-center-invites-applications-2027-2029-postdoctoral-and |
| `sydney-csc-phd-scholarship` | HTTP 200 → https://www.sydney.edu.au/scholarships/e/china-scholarship-council-research-programs-scholarship.html |
| `kyoto-u-mext-scholarship` | HTTP 200 → https://www.kyoto-u.ac.jp/en/education-campus/procedures/scholarships/mext |
| `uclouvain-fsr-postdoc-incoming` | HTTP 200 → https://uclouvain.be/en/news/appel-fsr-bourses-accueil-de-post-doctorants-en-mobilite-internationale |
| `miller-research-fellowship` | HTTP 200 → https://miller.berkeley.edu/nominate-apply/miller-research-fellowship |
| `azrieli-international-postdoc` | HTTP 200 → https://azrielifoundation.org/azrieli-fellows-news/call-for-applications-for-the-azrieli-international-postdoctoral-fellowship-2027-28/ |
| `ucsb-idrf-international-fellowship` | HTTP 200 → https://www.graddiv.ucsb.edu/funding-options |
| `pitt-katz-phd-tuition-aid` | HTTP 200 → https://www.business.pitt.edu/katz-admissions/admissions-tuition-phd-program/ |
| `colorado-leeds-phd-funding` | HTTP 200 → https://www.colorado.edu/business/phd/funding |
| `arizona-eller-accounting-phd` | HTTP 200 → https://eller.arizona.edu/programs/doctoral/accounting/admissions |
| `rochester-biostat-phd-financial-aid` | HTTP 200 → https://www.urmc.rochester.edu/education/graduate/phd/statistics/apply/financial-aid |
| `ie-university-phd-funding` | HTTP 200 → https://www.ie.edu/business-school/programs/doctorates/phd-in-management/admissions-fees/ |
| `kitp-theoretical-physics-postdoc` | HTTP 200 → https://www.kitp.ucsb.edu/about-us/careers/postdoctoral-scholars-in-theoretical-physics |
| `khk-aachen-cultures-of-research` | HTTP 200 → https://khk.rwth-aachen.de/call-for-fellowship-applications-2027-28/ |
| `ntu-npgs` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/npgs |
| `ntu-research-scholarship` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/rss |
| `ictp-saifr-postdoc` | HTTP 200 → https://www.ictp-saifr.org/postdoctoral/ |
| `cdt-aqt-applied-quantum` | HTTP 200 → https://www.aqt.ac.uk/apply/ |
| `babraham-institute-phd` | HTTP 200 → https://www.babraham.ac.uk/work-and-study/phd-opportunities |
| `jic-international-scholarship` | HTTP 200 → https://jic.ac.uk/training-careers/postgraduate-opportunities/international-scholarships/ |
| `hbigs-heidelberg` | HTTP 200 → https://www.hbigs.uni-heidelberg.de/en |
| `cim-imprs-muenster` | HTTP 200 → https://www.uni-muenster.de/CiM-IMPRS/about/introduction.html |
| `wustl-dbbs-financial-support` | HTTP 200 → https://dbbs.wustl.edu/about/stipends-benefits-grants/ |
| `cnes-theses-postdocs` | HTTP 200 → https://cnes.fr/theses-post-doctorats |
| `hku-law-phd-pgs` | HTTP 200 → https://www.law.hku.hk/prospective-students/research-programmes-introduction/ |
| `gii-geneva-financing-phd` | HTTP 200 → https://www.graduateinstitute.ch/scholarships |
| `ubc-csc-doctoral` | HTTP 200 → https://www.grad.ubc.ca/awards/china-scholarship-council-doctoral-scholarships |
| `google-deepmind-student-researcher` | HTTP 200 → https://deepmind.google/student-researcher-program/ |
| `eiffel-france-excellence-campusfrance` | HTTP 200 → https://www.campusfrance.org/en/france-excellence-eiffel-scholarship-program |
| `sutd-istd-phd-opportunities` | HTTP 200 → https://www.sutd.edu.sg/programme-listing/istd-phd-programme |
| `kaw-postdoc-calls` | HTTP 200 → https://kaw.wallenberg.org/en/funding-guide/calls |
| `uts-international-research-scholarship` | HTTP 200 → https://www.uts.edu.au/for-students/admissions-entry/scholarships/scholarships-search/international-research-scholarship |
| `grenoble-quang2-quantum-phd-call` | HTTP 200 → https://phdquantumgrenoble.univ-grenoble-alpes.fr/phd-application |
| `fraunhofer-iee-jobs-theses-phd` | HTTP 200 → https://www.iee.fraunhofer.de/en/career.html |
| `mathjobs-bonn-karriere` | HTTP 200 → https://www.mathematics.uni-bonn.de/hcm/opportunities |
| `uk-bbsrc-cambridge-biosciences-dtp` | HTTP 200 → https://bbsrcdtp.lifesci.cam.ac.uk/how-apply |
| `uk-glasgow-csc-phd` | HTTP 200 → https://www.gla.ac.uk/colleges/socialsciences/studentfundingopportunities/postgraduateresearch/chinascholarshipcouncilcscphdscholarships/ |
| `uk-birmingham-csc-phd` | HTTP 200 → https://www.birmingham.ac.uk/study/scholarships-funding/china-scholarship-council-university-of-birmingham-phd-scholarships |
| `uw-biostat-funding-guarantee` | HTTP 200 → https://www.biostat.washington.edu/apply/costs |
| `lund-stats-doctoral-studentship` | HTTP 200 → https://www.lusem.lu.se/organisation/department-statistics/doctoral-studies-department-statistics |
| `chem-epfl-lcsa-cramer-openings` | HTTP 200 → https://www.epfl.ch/labs/lcsa/job-openings/ |
| `chem-rseq-jobs` | HTTP 200 → https://rseq.org/socios-y-profesionales/ofertas-de-empleo/ |
| `cobene-vienna-how-to-apply` | HTTP 200 → https://vds-cobene.univie.ac.at/how-to-apply/application-process/ |
| `cobene-pooled-calls` | HTTP 200 → https://vds-cobene.univie.ac.at/how-to-apply/closed-calls/ |
| `excellent-brains-coe-vienna` | HTTP 200 → https://coe.univie.ac.at/?page_id=55 |
| `az-cambridge-noncl-phd` | HTTP 200 → https://www.ats.cam.ac.uk/az-funded-non-clinical-phd-studentship |
| `imperial-bioeng-studentships` | HTTP 200 → https://www.imperial.ac.uk/bioengineering/study/postgraduate-research/doctoral/funding/studentships/ |
| `glasgow-jws-phd` | HTTP 200 → https://www.gla.ac.uk/schools/engineering/phdopportunities/ |
| `lund-vacancies` | HTTP 200 → https://www.lunduniversity.lu.se/vacancies |
| `arch-epfl-edar-enac` | HTTP 200 → https://www.epfl.ch/schools/enac/education/test_archi-hub/labs-epfl-architecture-under-construction/ |
| `arch-zgis-salzburg-news` | HTTP 200 → https://www.plus.ac.at/geoinformatik/news-jobs/news/ |
| `arch-lse-geography-phd-funding` | HTTP 200 → https://www.lse.ac.uk/geography-and-environment/study/phd/mphil-phd-frequently-asked-questions |
| `jobs-ac-uk-politics-studentships` | HTTP 200 → https://www.jobs.ac.uk:443/categories/politics |
| `cambridge-ames-postgraduate-funding` | HTTP 200 → https://www.ames.cam.ac.uk/study-with-us/postgraduate-study/postgraduate-funding |
| `hku-arts-pgs-rates` | HTTP 200 → https://arts.hku.hk/admissions/research-postgraduate-admissions/research-postgraduate/ |
| `ucalgary-kinesiology-phd` | HTTP 200 → https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/kinesiology-phd |
| `ubc-phd-funding-guarantee` | HTTP 200 → https://www.grad.ubc.ca/prospective-students/phd |
| `uwe-sww-dtp-studentships` | HTTP 200 → https://www.uwe.ac.uk/research/postgraduate-research-study/studentships |
| `bcu-phd-studentships` | HTTP 200 → https://www.bcu.ac.uk/research/our-phds/phd-opportunities |
| `aston-phd-health-life-sciences` | HTTP 200 → https://www.aston.ac.uk/study/courses/phd-health-and-life-sciences-bsc |
| `bu-ssw-phd-funding` | HTTP 200 → https://www.bu.edu/ssw/admissions-financial-aid/phd-program/phd-funding/ |
| `clemson-graduate-finance` | HTTP 200 → https://www.clemson.edu/admissions/graduate-admissions/cost-and-aid.html |
| `miami-um-fellowship` | HTTP 200 → https://www.grad.miami.edu/about/costs-fellowships-and-other-funding/fellowships,-financial-aid,-and-other-funding-opportunities/graduate-school-fellowships-and-scholarships/um-fellowship/index.html |
| `drexel-lebow-phd-funding` | HTTP 200 → https://www.lebow.drexel.edu/admissions/doctorate/phd-admissions/assistantships-and-financial-aid |
| `fr-lille-engsys-thesis-funding-2026` | HTTP 200 → https://egengsys.univ-lille.fr/en/welcome/news/news-detail/campagnes-de-financements-de-these-2026 |
| `inside-higher-ed-postdoc-na` | HTTP 200 → https://careers.insidehighered.com/jobs/postdoc/north-america/5/ |
| `academia-sinica-postdoc-guidelines` | HTTP 200 → https://www.sinica.edu.tw/en/cp/331 |
| `newberry-long-term-fellowships` | HTTP 200 → https://www.newberry.org/research/fellowships/long-term-fellowships |
| `herchel-smith-postdoc` | HTTP 200 → https://www.herchelsmith.cam.ac.uk/postdoctoral-fellowships/how-apply |
| `fes-auslaender-promotion` | HTTP 200 → https://www.fes.de/studienfoerderung/stipendium/promotionsfoerderung-fuer-auslaender-innen |
| `oist-phd-program` | HTTP 200 → https://www.oist.jp/admissions |
| `hbku-scholarship-policy-pdf` | HTTP 200 → https://www.hbku.edu.qa/en/scholarship |
| `weizmann-merbl-lab-recruiting` | HTTP 200 → https://www.weizmann.ac.il/immunology/merbl/join-us |
| `eit-digital-industrial-phd` | HTTP 200 → https://www.eit.europa.eu/our-activities/opportunities/eit-digital-call-phd-students-and-partners |
| `khalifa-tsinghua-sigs-joint-phd` | HTTP 200 → https://www.ku.ac.ae/khalifa-university-phd-students-begin-jointly-awarded-program-at-tsinghua-sigs?p=124233 |
| `cambridge-maths-phd-funding` | HTTP 200 → https://www.maths.cam.ac.uk/postgrad/research-degrees |
| `warwick-chancellors-intl-scholarship` | HTTP 200 → https://warwick.ac.uk/services/dc/schols_fund/applicants/competitions/ |
| `utoronto-utm-university-fellowship` | HTTP 200 → https://www.utm.utoronto.ca/cps/graduate/chemistry/financial-support/scholarshipsfellowshipsawards/regular-university-toronto |
| `uts-urban-planning-phd` | HTTP 200 → https://www.uts.edu.au/courses/doctor-of-philosophy-phd-thesis-urban-planning |
| `gsd-phd-program` | HTTP 200 → https://www.gsd.harvard.edu/offices-and-facilities/advanced-studies-programs/programs/doctor-of-philosophy/ |
| `berkeley-gateway-fellowship` | HTTP 200 → https://ihouse.berkeley.edu/live-i-house/i-house-financial-aid/gateway-fellowship-program |
| `huji-frieberg-postdoc-s42` | HTTP 200 → https://eacenter.huji.ac.il/research-grants |
| `unive-msca-pf-ca-foscari` | HTTP 200 → https://www.unive.it/pag/28536/#c767421 |
| `ip-paris-phd-track-scholarships` | HTTP 200 → https://www.ip-paris.fr/en/education/useful-information/scholarships |
| `simons-plant-biology-postdoc` | HTTP 200 → https://www.simonsfoundation.org/life-sciences/simons-postdoctoral-fellowships-in-plant-biology/ |
| `fredhutch-postdoc-programs` | HTTP 200 → https://www.fredhutch.org/en/education-training/postdoctoral-fellows-programs.html |
| `hkustgz-iot-thrust-phd` | HTTP 200 → https://infh.hkust-gz.edu.cn/academics/iot/about-iot/ |
| `cuhksz-lam-robotics-group` | HTTP 200 → https://freeformrobotics.org/contact/ |
| `hhmi-gilliam-fellowship` | HTTP 200 → https://www.hhmi.org/programs/gilliam-fellows |
| `ijs-cobotat-funded-phd` | HTTP 200 → https://cobotat.ijs.si/news/prosta-delovna-mesta-2/ |
| `kf-graduate-studies-scholarship` | HTTP 200 → https://www.kf.or.kr/kfEng/main.do?menuno=3793 |
| `uiuc-geography-gis-graduate-funding` | HTTP 200 → https://ggis.illinois.edu/academics/graduate-programs/assistantships-fellowships |
| `washu-complit-phd-funding` | HTTP 200 → https://complitandthought.washu.edu/complit-thought-graduate |
| `polyu-xu-shengduo-phd-studentship` | HTTP 200 → https://www.polyu.edu.hk/me/people/academic-teaching-staff/xu-shengduo-prof/-/media/3e74d0a55b494249b4ba46b79bff914a.ashx |
| `fr-culture-contrats-doctoraux-architecture` | HTTP 200 → https://www.culture.gouv.fr/catalogue-des-demarches-et-subventions/appels-a-projets-candidatures/attribution-des-contrats-doctoraux-du-ministere-de-la-culture-en-architecture-ville-et-paysage |
| `kth-how-to-apply-phd` | HTTP 200 → https://www.kth.se/en/studies/phd/how-to-apply-1.520089 |
| `bbsrc-nwdp-manchester-liverpool` | HTTP 200 → https://www.bmh.manchester.ac.uk/study/research/funding-fees/funded-programmes/bbsrc-nwdp/ |
| `lmu-gsn-funding` | HTTP 200 → https://www.lmu.de/gsn/en/studying-at-gsn-lmu/become-a-gsn-student/ |
| `imprs-physics-of-light-erlangen` | HTTP 200 → https://mpl.mpg.de/study-work-or-visit/careers-science |
| `imperial-materials-scholarship-hub` | HTTP 200 → https://www.imperial.ac.uk/materials/study/materialsphd/phd-application-process--scholarship-hub/ |
| `imperial-materials-phd-projects` | HTTP 200 → https://www.imperial.ac.uk/materials/study/materialsphd/phdprojects/ |
| `cambridge-zoology-2026-27` | HTTP 200 → https://www.zoo.cam.ac.uk/2027-28-project-list |
| `simons-ee-fellowships` | HTTP 200 → https://www.simonsfoundation.org/life-sciences/simons-graduate-fellowships-in-ecology-and-evolution/ |
| `cifor-cgiar-germany-hub-phd` | HTTP 200 → https://hub.landscapealliance.org/phd-research-scholarship/about-phd-research-scholarship |
| `wur-phd-programme` | HTTP 200 → https://www.wur.nl/en/education/phd-programme?utm_source=verkorte_url&utm_medium=redirect |
| `jobs-ac-uk-agri-food-vet-phd` | HTTP 200 → https://www.jobs.ac.uk:443/search/agriculture-food-and-veterinary/phd |
| `bu-bioinformatics-funding` | HTTP 200 → https://www.bu.edu/bioinformatics/admissions/finaid/ |
| `illc-uva-tcs-positions` | HTTP 200 → https://www.illc.uva.nl/NewsandEvents/News/Positions |
| `aea-grad-funding` | HTTP 200 → https://www.aeaweb.org/resources/students/grad-prep/funding |
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
| `kyushu-isc-mext-info` | HTTP 200 → https://www.isc.kyushu-u.ac.jp/intlweb/en/student/government-expense |
| `dfg-walter-benjamin` | HTTP 200 → https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/walter-benjamin |
| `tcd-trda-school-based` | HTTP 200 → https://www.tcd.ie/graduatestudies/awards/trda-school-based/ |
| `ca-uoft-ece-funding` | HTTP 200 → https://www.ece.utoronto.ca/graduates/financial-support/package/ |
| `ca-uoft-glse-postdoc` | HTTP 200 → https://rhse.temertymedicine.utoronto.ca/postdoctoral-fellowship-programs-awards-and-funds |
| `ca-ubc-okanagan-min-funding` | HTTP 200 → https://okanagan.calendar.ubc.ca/faculties-schools-and-colleges/college-graduate-studies/minimum-funding |
| `ca-mcgill-desautels-tuition-aid` | HTTP 200 → https://www.mcgill.ca/desautels/programs/phd/admissions/tuition-financial-aid |
| `csc-paris-saclay-joint-doctoral` | HTTP 200 → https://www.universite-paris-saclay.fr/en/csc-joint-doctoral-programme-universite-paris-saclay-and-chinese-scholarship-council |
| `mcgill-csc-joint` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/international/csc-chinese-students |
| `utoronto-csc-joint` | HTTP 200 → https://www.sgs.utoronto.ca/awards/china-scholarship-council/ |
| `tcd-csc-joint` | HTTP 200 → https://www.tcd.ie:443/study/international/scholarships/postgraduate/csc/ |
| `goettingen-ugoe-csc-phd` | HTTP 200 → https://uni-goettingen.de/en/308975.html |
| `gu-sahlgrenska-doctoral-studies` | HTTP 200 → https://www.gu.se/en/sahlgrenska-akademin/doctoral-studies |
| `cnic-predoctoral-program` | HTTP 200 → https://www.cnic.es/es/node/191 |
| `wehi-international-phd-scholar` | HTTP 200 → https://www.wehi.edu.au/education/phd/international-phd-scholar-initiative/ |
| `wehi-phd-scholarship` | HTTP 200 → https://www.wehi.edu.au/education/phd/phd-scholarships/ |
| `qimr-international-phd` | HTTP 200 → https://www.qimrb.edu.au/people-and-careers/international-phd-scholarships |
| `epfl-grid-ess-positions` | HTTP 200 → https://www.epfl.ch/labs/grid-ess/grid-integrated-energy-storage-systems-lab/open-positions/ |
| `chem-stanford-phd-financial-support` | HTTP 200 → https://chemistry.stanford.edu/academics/about-phd-program/financial-support |
| `epfl-edma-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edma-mathematics/edma-how-to-apply/ |
| `epfl-edey-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edey-energy/edey-how-to-apply/ |
| `epfl-edce-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edce-civil-and-environmental-engineering/edce-how-to-apply/ |
| `epfl-admission-criteria` | HTTP 200 → https://www.epfl.ch/education/admission/admission-2/phd-admission-criteria-and-application/ |
| `epfl-lab-head-positions` | HTTP 200 → https://www.epfl.ch/labs/head/home/open-positions/ |
| `snf-doctoral-salary-news` | HTTP 200 → https://www.snf.ch/en/kHunysxdKHpyUL8s/news/salary-increase-for-doctoral-students |
| `pasteur-paris-university-phd` | HTTP 200 → https://www.pasteur.fr/en/about-us/our-missions/education/training-programs/doctoral-programs/ppu |
| `amii-career-opportunities` | HTTP 200 → https://www.amii.ca/about/career-opportunities |
| `studyinjapan-mext-research-2027` | HTTP 200 → https://www.studyinjapan.go.jp/en/smap-stopj-applications-research.html |
| `itatti-2027-2028-fellowships` | HTTP 200 → https://itatti.harvard.edu/news/applications-are-now-open-i-tatti%E2%80%99s-202728-fellowships |
| `bauhaus-weimar-doctorate` | HTTP 200 → https://www.uni-weimar.de/en/university/research-and-art/academic-careers/doctorate/doctoral-programmes |
| `sydney-architecture-design-planning-rs` | HTTP 200 → https://www.sydney.edu.au/scholarships/a/architecture-design-and-planning-research-scholarship.html |
| `oslomet-lui-educational-sciences-phd` | HTTP 200 → https://www.oslomet.no/en/study/lui/educational-sciences-phd |
| `uab-csc-phd-opportunities` | HTTP 200 → https://www.uab.cat/web/mobility-international-exchange/international-support-service/phd-opportunities-at-the-uab-1345830338586.html |
| `imprs-cim-muenster` | HTTP 200 → https://www.uni-muenster.de/CiM-IMPRS/application/ |
| `mpi-cbg-phd-program` | HTTP 200 → https://www.mpi-cbg.de/join-us/phd-program |
| `unibo-csc-joint-phd` | HTTP 200 → https://www.unibo.it/en/study/phd-professional-masters-specialisation-schools-and-other-programmes/phd/phd-programmes-funded-by-the-china-scholarship-council |
| `simons-dissertation-math` | HTTP 200 → https://www.simonsfoundation.org/mathematics-physical-sciences/simons-dissertation-fellowship-in-mathematics/ |
| `us-priv-brown-five-year-guarantee` | HTTP 200 → https://graduateschool.brown.edu/financing-support/funding-guarantee |
| `us-priv-bu-engineering-ece-funding` | HTTP 200 → https://www.bu.edu/eng/academics/departments-and-divisions/electrical-and-computer-engineering/resources/resources-current-students/phd-financial/ |
| `us-priv-vanderbilt-physics-aid` | HTTP 200 → https://as.vanderbilt.edu/physics-astronomy/phd-financial-aid/ |
| `us-priv-vanderbilt-philosophy-funding` | HTTP 200 → https://as.vanderbilt.edu/philosophy/graduate-admissions/ |
| `imperial-frontier-ai-phd` | HTTP 200 → https://www.imperial.ac.uk/frontier-ai/join-us-for-a-phd/ |
| `igradu-ulm-application` | HTTP 200 → https://www.uni-ulm.de/en/einrichtungen/igradu/info-applicants |
| `helmholtz-current-calls` | HTTP 200 → https://www.helmholtz.de/en/research/current-calls-for-applications |
| `utep-eeb-funded-ra-phd` | HTTP 200 → https://www.utep.edu/science/eeb/academic%20programs/phd.html |
| `mpi-susmat-admission` | HTTP 200 → https://www.mpie.de/2941513/admission |
| `kaust-bioscience-phd` | HTTP 200 → https://www.kaust.edu.sa/en/study/biomed/bioscience |
| `cispa-rossow-system-security-jobs` | HTTP 200 → https://syssec.cispa.de/jobs |
| `ethz-cs-doctoral-study-program` | HTTP 200 → https://inf.ethz.ch/doctorate/doctoral-study-program.html |
| `kit-kastel-doctoral-research` | HTTP 200 → https://www.kastel.kit.edu/1827.php |
| `imperial-structures-phd-study` | HTTP 200 → https://www.imperial.ac.uk/civil-engineering/research/research-disciplines/structures/study-with-us/phd-study/ |
| `isae-supaero-doctoral-teams` | HTTP 200 → https://www.isae-supaero.fr/notre-offre-de-formations/formation-doctorale-isae-supaero/ |
| `sedarc-royal-holloway-esrc` | HTTP 200 → https://www.royalholloway.ac.uk/studying-here/fees-and-funding/research-degrees/sources-of-funding/sedarc-student-led-studentships/ |
| `asu-sanford-sociology-phd` | HTTP 200 → https://degrees.asu.edu/masters-phd/major/ASU00/LASOCPHD/sociology-phd |
| `dfk-paris-doctoral-contracts` | HTTP 200 → https://www.dfk-paris.org/en/page/contracts-doctoral-candidates-3928.html |
| `frankfurt-school-doctoral` | HTTP 200 → https://www.frankfurt-school.de/en/study/doctoral |
| `bis-phd-fellowship` | HTTP 200 → https://www.bis.org/about/careers/early-careers |
| `erasmus-ese-phd` | HTTP 200 → https://www.eur.nl/en/ese/working/phd-vacancies |
| `eea-job-market-hub` | HTTP 200 → https://eeassoc.org/job-market |
| `fwo-senior-postdoc` | HTTP 200 → https://www.fwo.be/en/support-programmes/all-calls/postdoctoral-researchers/senior-postdoctoral-fellowship/ |
| `eu-dfg-emmy-noether` | HTTP 200 → https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/emmy-noether |
| `ca-mcgill-intl-external-awards` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/additional-international-funding-opportunities |
| `cambridge-studentships-list` | HTTP 200 → https://www.cam.ac.uk/taxonomy/jobs-categories/studentships |
| `eur-research-master-economics` | HTTP 200 → https://www.eur.nl/en/research-master/research-master-economics |
| `leiden-scholarships` | HTTP 200 → https://www.universiteitleiden.nl/en/scholarships |
| `compound-semi-cdt` | HTTP 200 → https://www.cdt-compound-semiconductor.org/about-us/ |
| `imprs-tp-application` | HTTP 200 → https://www.imprs-tp.mpg.de/2879/application |
| `imprs-qd-heidelberg-application` | HTTP 200 → https://www.mpi-hd.mpg.de/imprs-qd/imprsqd.html?&L=458 |
| `clay-research-fellowship` | HTTP 200 → https://www.claymath.org/fellowship-nominations/ |
| `brown-five-year-guarantee` | HTTP 200 → https://graduateschool.brown.edu/financing-support/funding-guarantee |
| `cbs-economics-doctoral-fellowships-mpi` | HTTP 200 → https://www.econ.mpg.de/419085/application |
| `cuhk-hkpfs` | HTTP 200 → https://www.gs.cuhk.edu.hk/admissions/scholarships-fees/hkpfs |
| `aalto-doctoral-pilot` | HTTP 200 → https://www.aalto.fi/en/doctoralpilot |
| `hpi-database-group-positions` | HTTP 200 → https://hpi.de/en/database-group/home/ |
| `imdea-networks-job-listings` | HTTP 200 → https://networks.imdea.org/taxonomy_jobs/research-2/ |
| `warwick-csc-2027` | HTTP 200 → https://warwick.ac.uk/services/dc/schols_fund/applicants/competitions/ |
| `fub-csc-application-procedure` | HTTP 200 → https://www.fu-berlin.de/en/sites/china/foerdermoeglichkeiten/fuer_chinesen/csc-phd-program/application-procedure-phd/index.html |
| `bergamo-csc` | HTTP 200 → https://www.unibg.it/internazionale/destinazione-unibg/riconoscimento-dottorati-ricerca-conseguiti-allestero/phd-grants |
| `ubc-4yf-doctoral` | HTTP 200 → https://www.grad.ubc.ca/awards/four-year-doctoral-fellowship-4yf |
| `ucalgary-ages` | HTTP 200 → https://grad.ucalgary.ca/awards-and-funding/award-opportunities/ages |
| `stonybrook-chem-how-to-apply` | HTTP 200 → https://www.stonybrook.edu/chemistry-new/academics/phd-program/how-to-apply.html |
| `aarhus-phd-salary-employment-info` | HTTP 200 → https://phd.arts.au.dk/financing/salary-and-employment/salary-5-3 |
| `basf-nao-asia-phd` | HTTP 200 → https://www.basf.com/cn/en/microsites/nao/how-to-apply |
| `airbus-vie-phds` | HTTP 200 → https://www.airbus.com/en/careers/students-and-graduates/vie-and-phds |
| `kochi-tech-csc-kut-phd` | HTTP 200 → https://www.kochi-tech.ac.jp/english/admission/csc_kut_scholarship_program/guideline-full-time-phd-student.html |
| `dff-sapere-aude-research-leader` | HTTP 200 → https://dff.dk/en/managing-your-grant/previous-calls-and-guidelines/previous-calls-and-guidelines/expired-instruments/2026/oktober/sapere-aude-dff-research-leader-e26/ |
| `bifold-graduate-school-berlin` | HTTP 200 → https://www.bifold.berlin/education/graduate-school/admission |
| `iocb-prague-phd-call` | HTTP 200 → https://www.uochb.cz/en/call-for-phd-applications |
| `mcgill-csc-joint-doctoral` | HTTP 200 → https://www.mcgill.ca/gps/funding/intl/international/csc-chinese-students |
| `uiuc-psychology-phd-funding` | HTTP 200 → https://psychology.illinois.edu/academics/phd-psychology/psychology-phd-financial-information |
| `berkeley-psych-phd-funding` | HTTP 200 → https://psychology.berkeley.edu/graduate/admission/funding-residency |
| `calgary-werklund-phd-funding` | HTTP 200 → https://werklund.ucalgary.ca/graduate-programs/phd-funding |
| `imprs-trust` | HTTP 200 → https://www.imprs-trust.mpg.de/ |
| `bu-econ-phd-five-year-funding` | HTTP 200 → https://www.bu.edu/econ/admissions/apply-for-a-phd/expenses-financial-aid/ |
| `eso-studentship` | HTTP 200 → https://www.eso.org/sci/activities/fellowships-and-studentships/FeSt-overview/ESOstudentship.html |
| `stanford-doerr-postdoc` | HTTP 200 → https://sustainability.stanford.edu/about-school/postdoctoral-resources/postdoctoral-fellowship-program/ |
| `cuhk-ees-hkpfs` | HTTP 200 → https://www.ees.cuhk.edu.hk/programme/postgraduate-programmes/postgraduate-programme/ |
| `ucalgary-geoscience-phd` | HTTP 200 → https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/geoscience-phd?page=1 |
| `tampere-ippe-epi-phd` | HTTP 200 → https://www.tuni.fi/en/tau/doctoral-programmes/international-doctoral-programme-epidemiology-and-public-health-ippe |
| `cuhk-sph-research-postgrad` | HTTP 200 → https://sphpc.cuhk.edu.hk/rpg-programme/ |
| `cuhk-phd-public-health-hkpfs` | HTTP 200 → https://sphpc.cuhk.edu.hk/post/phd-in-public-health-2025-26-hong-kong-phd-fellowship-scheme-hkpfs-open-for-application-2/ |
| `cambridge-dtp-mr` | HTTP 200 → https://www.medschl.cam.ac.uk/school-clinical-medicine-doctoral-training-programme |
| `indiana-luddy-funding` | HTTP 200 → https://luddy.iu.edu/cost-financial-aid/graduate-funding/index.html |
| `hkust-hkpfs` | HTTP 200 → https://fytgs.hkust.edu.hk/scholarships/hong-kong-phd-fellowship-scheme |
| `ntu-nie-phd-scholarship` | HTTP 200 → https://www.ntu.edu.sg/nie/admissions/graduate-education/scholarships-awards/nie-phd-scholarship |
| `oise-funded-phd-cohort` | HTTP 200 → https://www.oise.utoronto.ca/registrar-students/grad-funding |
| `nl-utrecht-phd-vacancies` | HTTP 200 → https://www.uu.nl/en/organisation/phd-programmes/starting-a-phd-track/phd-vacancies |
| `nl-rug-phd-vacancies` | HTTP 200 → https://www.rug.nl/cf/research/phd-programme/phd-vacancies |
| `be-imec-phd` | HTTP 200 → https://www.imec-int.com/en/work-at-imec/job-opportunities/phd-at-imec |
| `uottawa-phd-intl-research-scholarship` | HTTP 200 → https://www.uottawa.ca/study/graduate-studies/funding-financing/awards/phd-student-international-research-scholarship |
| `utoronto-sgs-financial-support` | HTTP 200 → https://sgs.calendar.utoronto.ca/financial-support |
| `ucalgary-funding-floor` | HTTP 200 → https://grad.ucalgary.ca/awards-and-funding/funding-TB-students |
| `laval-doctorate-tuition-exemption` | HTTP 200 → https://www.ulaval.ca/etudes/droits-de-scolarite/etudiant-de-linternational |
| `dal-research-excellence` | HTTP 200 → https://www.dal.ca/faculty/gradstudies/finance-your-studies/scholarships-bursaries/research-excellence-scholarship.html |
| `mcmaster-eng-min-funding` | HTTP 200 → https://www.eng.mcmaster.ca//app/uploads/2025/01/Minimum-Funding-Packages-for-Graduate-Students_May-28-2024.pdf |
| `mitacs-elevate-postdoc` | HTTP 200 → https://www.mitacs.ca/our-programs/elevate/ |
| `gov-canada-intl-scholarships` | HTTP 200 → https://www.educanada.ca/scholarships-bourses/index.aspx?lang=eng |
| `iisc-international-phd` | HTTP 200 → https://oir.iisc.ac.in/index.php/iisc-full-time-international-research-programmes/ |
| `polyu-hkpfs` | HTTP 200 → https://www.polyu.edu.hk/engl/study/research-postgraduate-programme/hong-kong-phd-fellowship-scheme/ |
| `um-umps-phd` | HTTP 200 → https://grs.um.edu.mo/index.php/prospective-students/phd-funding/um-phd-scholarship/ |
| `kavli-ipmu-postdoc` | HTTP 200 → https://www.ipmu.jp/en/job-opportunities/PD2026 |
| `osu-german-admissions-funding` | HTTP 200 → https://germanic.osu.edu/graduate-studies-0/admissions-and-funding |
| `umd-smith-phd-financial-support` | HTTP 200 → https://www.rhsmith.umd.edu/programs/phd/admissions/financial-support |
| `lille-institutional-funding` | HTTP 200 → https://egbsl.univ-lille.fr/en/apply-for-a-phd/selection-for-institutional-fundings |
| `best-toulouse-cofund` | HTTP 200 → https://www.utoulouse.fr/medias/fichier/2025-11-27-un-nouveau-programme-doctoral-europe-en_1764324558566-pdf?INLINE=FALSE&jsonLdModel= |
| `arcane-grenoble-cofund` | HTTP 200 → https://arcane.univ-grenoble-alpes.fr/news/phd-cofund-call |
| `us-harvard-seas-phd-funding` | HTTP 200 → https://seas.harvard.edu/current-prospective-students/prospective-gradaute-students/funding-scholarship-graduate-programs |
| `us-uchicago-social-sciences-funding` | HTTP 200 → https://socialsciences.uchicago.edu/admissions/funding-and-financing |
| `erc-avcr-selection-procedures` | HTTP 200 → https://www.avcr.cz/en/about-us/career/selection-procedures |
| `iisc-ipdf-postdoc` | HTTP 200 → https://www.iisc.ac.in/careers/post-doctoral-fellowship/ |
| `um-talent-programme-rskto` | HTTP 200 → https://rskto.um.edu.mo/umtp/ |
| `jpl-nasa-npp` | HTTP 200 → https://www.jpl.nasa.gov/site/postdocs/prospective-postdocs/postdoc-programs/ |
| `nki-vacancies` | HTTP 200 → https://www.nki.nl/careers-study/vacancies/ |
| `biozentrum-phd-faq` | HTTP 200 → https://phdstudents.biozentrum.unibas.ch/phd-at-the-biozentrum/ |
| `sheffield-csc-scholarship` | HTTP 200 → https://sheffield.ac.uk/postgraduate/phd/scholarships/csc |
| `durham-business-phd-scholarships` | HTTP 200 → https://www.durham.ac.uk/business/programmes/phd/phd-scholarships/ |
| `loughborough-csc-phd` | HTTP 200 → https://www.lboro.ac.uk/study/postgraduate/fees-funding/research-degree-funding/china-scholarship-council/ |
| `reading-international-phd-studentships` | HTTP 200 → https://www.reading.ac.uk/doctoral-researcher-college/funding/phd-studentships/international-phd-studentships |
| `qmul-csc-joint-phd` | HTTP 200 → https://www.qmul.ac.uk/maths/postgraduate/postgraduate-research/fees-and-funding/china-scholarship-council/ |
| `amolf-phd-jobs` | HTTP 200 → https://www.amolf.nl/vacancy-overview/?position%5B%5D=phd |
| `4tu-sai-engd-vacancies` | HTTP 200 → https://www.4tu.nl/sai/education/vacancies/ |
| `nus-cs-phd-scholarships` | HTTP 200 → https://www.comp.nus.edu.sg/programmes/pg/phdcs/scholarships/ |
| `ntu-ccds-phd-cs-engineering` | HTTP 200 → https://www.ntu.edu.sg/spms/admissions/grad/detail/ccds-phd-computing-datascience |
| `hkust-science-rpg` | HTTP 200 → https://science.hkust.edu.hk/academic_programs/postgrad_prog/research_postgraduate/admissions |
| `uts-csc-phd` | HTTP 200 → https://www.uts.edu.au/for-students/admissions-entry/scholarships/scholarships-search/csc-uts-phd-scholarship |
| `uow-csc-joint-phd` | HTTP 200 → https://www.uow.edu.au/research/graduate-research/scholarships/items/joint-postgraduate-scholarships-program---china-scholarship-council-csc.php |
| `ufz-higrade-doctoral` | HTTP 200 → https://www.ufz.de/higrade/index.php?en=41184 |
| `gsi-hgs-hire-graduate-school` | HTTP 200 → https://hgs-hire.de/ |
| `mpib-jobs-page` | HTTP 200 → https://www.mpg.de/149875/human-development?filter=jobs |
| `cerge-ei-phd-economics` | HTTP 200 → https://ei.cerge-ei.cz/phd-in-economics/ |
| `mitacs-accelerate-phd-fellowship` | HTTP 200 → https://www.mitacs.ca/our-programs/accelerate-fellowship/ |
| `fred-hutch-graduate-program` | HTTP 200 → https://www.fredhutch.org/en/education-training/graduate-program.html |
| `cruk-scotland-institute-phd` | HTTP 200 → https://www.crukscotlandinstitute.ac.uk/study/studentships/ |
| `cruk-manchester-phd-studentships` | HTTP 200 → https://www.bmh.manchester.ac.uk/study/research/funding-fees/funded-programmes/cruk-phd-studentships/ |
| `jobs-ac-uk-microbiology-studentships` | HTTP 200 → https://www.jobs.ac.uk:443/categories/microbiology |
| `durham-csc-joint-award` | HTTP 200 → https://www.durham.ac.uk/study/scholarships/international/chinese-scholarships-council/ |
| `harvard-international-graduate-funding` | HTTP 200 → https://scholarships.harvard.edu/international-graduate-students/ |
| `cambridge-guimaraes-phd-2027` | HTTP 200 → https://guimaraes.phy.cam.ac.uk/join-our-group/ |
| `us-berkeley-statistics-phd-financial-support` | HTTP 200 → https://statistics.berkeley.edu/academics/phd/admissions/financial-support |
| `bristol-pg-research-scholarship` | HTTP 200 → https://www.bristol.ac.uk/students/support/finances/scholarships/phd-research-scholarship/ |
| `lebesgue-math-phd-grants` | HTTP 200 → https://www.lebesgue.fr/en/phdgrants |
| `bonn-hcm-postdoc-positions` | HTTP 200 → https://www.mathematics.uni-bonn.de/hsm-school/postdoctoral-positions |
| `mpia-imprs-heidelberg` | HTTP 200 → https://www.imprs-hd.mpg.de/3192/Application |
| `daad-china-foerderprogramme-deutschland` | HTTP 200 → https://www.daad.org.cn/de/foerderung-finden/foerderprogramme-in-deutschland/ |
| `bern-gcb-graduate-school` | HTTP 200 → https://www.gcb.unibe.ch/ |
| `ihub-iitmandi-postdoc-call` | HTTP 200 → https://www.ihubiitmandi.in/wp-content/uploads/2025/01/Advertisement-new.pdf |
| `imperial-gida-studentships` | HTTP 200 → https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/opportunities/studentships/ |
| `hec-paris-phd-fees-funding` | HTTP 200 → https://www.hec.edu/en/phd-program/financing |
| `tudelft-cheme-careers` | HTTP 200 → https://www.tudelft.nl/tnw/over-faculteit/afdelingen/chemical-engineering/career-at-cheme |
| `imperial-cheme-phd-scholarships` | HTTP 200 → https://www.imperial.ac.uk/chemical-engineering/courses/postgraduate/phd/scholarships/ |
| `green-cdt-nuclear-sheffield` | HTTP 200 → https://sheffield.ac.uk/cmbe/phd/doctoral-training-centres/nuclear-energy |
| `uva-phd-vacancies-page` | HTTP 200 → https://werkenbij.uva.nl/en/vacancies?o=0&n=10&of=66546&hl=0&hh=38&s=0&f=74#vacancy-overview |
| `ut-careers-phd-page` | HTTP 200 → https://utwentecareers.nl/en/ut-as-employer/phd/ |
| `eur-university-phd-vacancies` | HTTP 200 → https://www.eur.nl/en/working-at-eur/vacancies/overview |
| `waterloo-international-doctoral-funding` | HTTP 200 → https://uwaterloo.ca/environment/graduate/future-graduate-students/funding-packages/funding-international-doctoral-students |
| `ubc-okanagan-phd-minimum-funding` | HTTP 200 → https://gradstudies.ok.ubc.ca/prospective-students/research-graduate-programs/ |
| `mcgill-chiu-kay-lui-csc-fellowships` | HTTP 200 → https://www.mcgill.ca/gps/funding/chiu-kay-lui-csc-fellowships |
| `courtauld-phd-funding-scholarships` | HTTP 200 → https://courtauld.ac.uk/explore-our-courses/postgraduate/ph-d-funding-and-scholarships/ |
| `bar-ilan-postdoc-fellowship` | HTTP 200 → https://validate.perfdrive.com/?ssa=92e12f30-ffcf-430e-9f29-bee99cc9161d&ssb=11070264037&ssc=https%3A%2F%2Facad-sec.biu.ac.il%2FPostDrE&ssi=a96ddcc1-dzai-4937-b012-055591873eca&ssk=botmanager_support@radware.com&ssm=75432919627997924105643116467238&ssn=96def6adf0e9ddddfea438d9699780328e14f8d5afe1-5cfd-4740-9b9e8a&sso=0ab0c1b2-ccd46e6d4de3c69d28f7430d373c8c7eb2db7859c8e0fdbb&ssp=48559846261792488242179242570821337&ssq=27147800078706465741800787643191774571845&ssr=MjAuMTY5LjUzLjU1&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/126.0%20Safari/537.36&ssu=&ssv=&ssw=&ssx=eyJyZCI6ImJpdS5hYy5pbCIsInV6bXgiOiI3ZmMwMDAwOTg4NjJkYS1iNmFjLTRhNGItOGU2Zi02ZjJjNTk5YzYxNjgxLTE3OTI0MDA3ODcwNzQwLTAwYWI0MWUxNWExYWY1ODFmZTUxMCIsIl9fdXptZiI6IjdmOTAwMGY4ZDVhZmUxLTVjZmQtNDc0MC05MWIyLWNjZDQ2ZTZkNGRlMzEtMTc5MjQwMDc4NzA3NDAtMDAxNjU4OGFjNWQ1ZGQ2NDJmMTEwIn0= |
| `hkust-fytgs-fees` | HTTP 200 → https://fytgs.hkust.edu.hk/admissions/Admissions-to-Hong-Kong-Campus/submitting-an-application/scholarships-and-fees#fees |
| `polyu-ise-fellowship-schemes` | HTTP 200 → https://www.polyu.edu.hk/gs/prospective-students/fellowship-scholarship-schemes/ |
| `nus-soc-graduate-scholarships` | HTTP 200 → https://www.comp.nus.edu.sg/financial-support/graduate-scholarships/ |
| `cshl-graduate-program` | HTTP 200 → https://www.cshl.edu/phd-program/how-to-apply/ |
| `stonybrook-genetics-graduate-program` | HTTP 200 → https://www.stonybrook.edu/gradgenetics/about/welcome.html |
| `lu-fnr-afdoc` | HTTP 200 → https://www.fnr.lu/funding-instruments/afdoc/ |
| `hhmi-hanna-gray-postdoc` | HTTP 200 → https://www.hhmi.org/programs/hanna-h-gray-fellows?utm_source=mpd&utm_medium=online-ad&utm_campaign=hgf-2022 |
| `cruk-career-development-fellowship` | HTTP 200 → https://www.cancerresearchuk.org:443/for-researchers/apply-for-and-manage-your-funding/our-funding-schemes/career-development-fellowship |
| `us-rochester-urmc-biostat-financial-aid` | HTTP 200 → https://www.urmc.rochester.edu/education/graduate/phd/statistics/apply/financial-aid |
| `sofinaboel-fellowship-2027` | HTTP 200 → https://www.frs-fnrs.be/fr/financements/sofinaboel-fellowships-2027 |
| `uni-lu-yadias-doctoral-fellowship-2026` | HTTP 200 → https://yadias.uni.lu/call-information/ |
| `bath-research-with-impact-phd` | HTTP 200 → https://www.bath.ac.uk/announcements/university-of-bath-launches-research-with-impact-phd-scholarships/ |
| `bangor-postgraduate-funding` | HTTP 200 → https://www.bangor.ac.uk/studentfinance/postgraduate/funding |
| `hk-sg-hkust-weihan-phd-openings` | HTTP 200 → https://weihan.people.ust.hk/?page_id=40 |
| `eur-future-phd-candidates` | HTTP 200 → https://www.eur.nl/en/working-at-eur/working-areas/phd |
| `fesb-split-doctoral-2026` | HTTP 200 → https://eng.fesb.unist.hr/2026/04/24/doctoral-study-call-for-applications-for-academic-year-2026-2027/ |
| `lille-doctoral-funding-2026` | HTTP 200 → https://egsesam.univ-lille.fr/fileadmin/user_upload/edsesam/Documents/Webinaires_Helene/Annexe_synthese_financements_de_theses_2026.pdf |
| `adum-offers-explainer` | HTTP 200 → https://www.universite-paris-saclay.fr/recherche/doctorat-et-hdr/proposer-un-sujet-de-these |
| `kiel-chem-job-links` | HTTP 200 → https://ravel.pctc.uni-kiel.de/boss/links/job-search/ |
| `rcs-phd-mphil` | HTTP 200 → https://www.rcs.ac.uk/courses/phd-mphil/ |
| `chicago-booth-phd-financial-aid` | HTTP 200 → https://www.chicagobooth.edu/phd/admissions/financial-aid |
| `lmb-phd` | HTTP 200 → https://mrclmb.ac.uk/careers-and-people/phd-students/how-to-apply/ |
| `be-vub-csc-phd` | HTTP 200 → https://www.vub.be/en/studying-vub/practical-info-for-students/how-much-does-studying-cost/financial-support/csc-vub-scholarship-programme |
| `fr-ens-csc-phd-cooperation` | HTTP 200 → https://www.ens.psl.eu/en/une-formation-d-exception/formations/echanges-internationaux/other-exchange-programs-and |
| `ascor-uva-phd-salaried-openings` | HTTP 200 → https://ascor.uva.nl/phd-programme/faq/faq.html |
| `lindner-cincinnati-phd` | HTTP 200 → https://www.business.uc.edu/programs-degrees/graduate/phd.html |
| `lancaster-lums-phd-funding` | HTTP 200 → https://www.lancaster.ac.uk/lums/phd/funding/ |
| `hitotsubashi-mext-business-doctoral` | HTTP 200 → https://international.hit-u.ac.jp/en/pros/mext/apply/ |
| `guelph-idts-award` | HTTP 200 → https://www.uoguelph.ca/regweb/studentfinance/apps/grawards?id=I5982 |
| `cmu-cee-phd-costs-funding` | HTTP 200 → https://cee.engineering.cmu.edu/education/graduate/costs-funding.html |
| `yale-political-science-funding` | HTTP 200 → https://politicalscience.yale.edu/academics/graduate-program/funding-professional-development-resources |
| `berkeley-math-financial-aid` | HTTP 200 → https://math.berkeley.edu/graduate/funding |
| `boeckler-promotionsstipendium` | HTTP 200 → https://www.boeckler.de/de/stipendium-fur-promovierende-2670.htm |
| `giessen-gcsc-doctoral-scholarships` | HTTP 200 → https://www.uni-giessen.de/de/fbz/ggkgcsc/graduierten-programme/index/promotion/stipendien/ausschreibung |
| `aspen-summer-program` | HTTP 200 → https://aspenphys.org/for-physicists/admissions-and-eligibility-criteria/ |
| `ictp-math-postdoc-2026` | HTTP 200 → https://2022.ictp.it/opportunity/mathematics-postdoctoral-positions-2027 |
| `cruk-scotland-centre-phd-studentship` | HTTP 200 → https://www.crukscotlandcentre.ac.uk/training/phd-studentships |
| `airc-short-term-fellowships-abroad` | HTTP 200 → https://www.direzionescientifica.airc.it/funding-for-research/other-funding-opportunities/ |
| `irish-cancer-society-fellowships` | HTTP 200 → https://www.cancer.ie/cancer-research/researchers-hub/apply-for-funding/fellowships |
| `janelia-careers-lab-postdoc` | HTTP 200 → https://www.hhmi.org/careers/janelia |
| `bih-phd-programme-en` | HTTP 200 → https://www.bihealth.org/en/platforms-programs/bih-biomedical-innovation-academy-bia/promotion-of-young-talents/bih-phd-program |
| `gfz-career-doctoral-entry` | HTTP 200 → https://www.gfz.de/en/career/phd-at-gfz |
| `mittag-leffler-junior-fellowship` | HTTP 200 → https://www.mittag-leffler.se/calls/call-for-junior-fellowships/ |
| `cu-boulder-cs-fall-2027-recruiting` | HTTP 200 → https://www.colorado.edu/cs/admissions/graduate-admissions/discover-graduate-programs |
| `hhmi-freeman-hrabowski-scholars` | HTTP 200 → https://www.hhmi.org/programs/freeman-hrabowski-scholars |
| `dzne-doctoral-researchers` | HTTP 200 → https://www.dzne.de/en/career/career-options/science/ |
| `gfz-potsdam-job-offers` | HTTP 200 → https://www.gfz.de/en/career/job-offers |
| `arizona-infosci-phd-funding` | HTTP 200 → https://infosci.arizona.edu/phd-information/admissions-funding |
| `clemson-cs-phd-faq` | HTTP 200 → https://www.clemson.edu/cecas/departments/computing/academics/graduates/faq.html |
| `gatech-public-policy-phd-guaranteed-funding` | HTTP 200 → https://spp.gatech.edu/graduate/phd |
| `ntu-npgs-scholarship` | HTTP 200 → https://www.ntu.edu.sg/admissions/graduate/financialmatters/scholarships/npgs |
| `eurasip-jobs-phd` | HTTP 200 → https://jobs.eurasip.org/ |
| `imperial-itp-phd-recruitment` | HTTP 200 → https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/intelligent-transmission/PhD-recruitment.pdf |
| `loughborough-sehs-funding-opportunities` | HTTP 200 → https://www.lboro.ac.uk/schools/sport-exercise-health-sciences/postgraduate-research/funding/ |
| `gmu-history-art-history-phd-funding` | HTTP 200 → https://historyarthistory.gmu.edu/graduate/graduate-student-resources/funding |
| `jk-kaist-kim-group-openings` | HTTP 200 → https://kimgroup.kaist.ac.kr/openings/ |
| `jk-science-tokyo-wise-sss` | HTTP 200 → https://www.wise-sss.titech.ac.jp/en/news/doctoral-level-education-and-student-support-system/ |
| `gu-cul-doctoral-school` | HTTP 200 → https://www.gu.se/culf/forskarskolan-cul/ansokan-till-forskarskolan-cul |
| `isye-or-doctoral-program` | HTTP 200 → https://www.isye.gatech.edu/academics/doctoral/degrees/operations-research |
| `ibm-goldstine-postdoc-fellowship` | HTTP 200 → https://research.ibm.com/labs/yorktown-heights/goldstine |
| `hirszfeld-doctoral-school-recruitment` | HTTP 200 → https://szkoladoktorska.hirszfeld.pl/en/doctoral-school/recruitment/current-recruitment/ |
| `bse-upf-economics-phd-track` | HTTP 200 → https://bse.eu/masters-degrees/economics-finance/upf-phd-track |
| `cuni-physics-phd-quantum-optics` | HTTP 200 → https://www.mff.cuni.cz/en/physicsphd/f6/program-overview |
| `edinburgh-sps-doctoral-college-scholarship` | HTTP 200 → https://www.sps.ed.ac.uk/study/prospective/postgraduate-research-programmes/scholarships/sps-awards/edinburgh-doctoral-college-scholarship-school-of-social-and-political-science |
| `g-evol-muenster-open-phd` | HTTP 200 → https://g-evol.uni-muenster.de/open-positions/ |
| `dfg-gefoerderte-verfahren-jobs` | HTTP 200 → https://www.dfg.de/de/ueber-uns/geschaeftsstelle/karriereseite/dfg-gefoerderte-verfahren |
| `iuj-scholarship` | HTTP 200 → https://www.iuj.ac.jp/admissions/cost/ |
| `burnet-study` | HTTP 200 → https://www.burnet.edu.au/careers-and-study/study-at-burnet/ |
| `isglobal-phd-programme` | HTTP 200 → https://www.isglobal.org/-/isglobal-phd-programme |
| `epfl-edmx-applicants` | HTTP 200 → https://www.epfl.ch/education/phd/edmx-materials-science-and-engineering/edmx-how-to-apply/ |
| `stipendium-hungaricum-study-finder` | HTTP 200 → https://stipendiumhungaricum.hu/study-finder/ |
| `ista-phd-program` | HTTP 200 → https://phd.pages.ista.ac.at/apply/ |
| `ku-graduate-scholarships` | HTTP 200 → https://www.ku.ac.ae/scholarships-postgraduate |
| `fraunhofer-promovieren-guide` | HTTP 200 → https://www.fraunhofer.de/content/dam/zv/de/jobs-karriere/Promovieren-mit-Fraunhofer.pdf |
| `edinburgh-bs-phd-scholarships` | HTTP 200 → https://www.business-school.ed.ac.uk/phd/scholarships-funding |
| `york-history-of-art-ahrc-dla-2027` | HTTP 200 → https://www.york.ac.uk/history-of-art/study/partnerships/ |
| `nber-fellowship-calls` | HTTP 200 → https://www.nber.org/career-resources/calls-fellowship-applications |
| `hanken-doctoral-funding-routes` | HTTP 200 → https://www.hanken.fi/en/apply/programmes/phd-programme/financing-doctoral-studies |
| `auckland-fmhs-deans-intl-doctoral` | HTTP 200 → https://www.auckland.ac.nz/en/study/scholarships-and-awards/find-a-scholarship/deans-international-doctoral-scholarship-640-fmhs.html |
| `cispa-jobs-portal-phd-postdoc` | HTTP 200 → https://career.cispa.de/jobs |
| `jax-phd-cooperative` | HTTP 200 → https://www.jax.org/education-and-learning/pre-and-postdoctoral-program/phd-programs |
| `bcm-phd-benefits` | HTTP 200 → https://www.bcm.edu/education/graduate-school-of-biomedical-sciences/admissions/stipends-benefits/fees-and-expenses/2021-22-fees-and-expenses |
| `bc-chemistry-funding` | HTTP 200 → https://www.bc.edu/content/bc-web/schools/morrissey/departments/chemistry/academics/graduate/welcome/ |
| `dtu-framebio-recruitment` | HTTP 200 → https://framebio.dtu.dk/Recruitment |
| `camk-doctoral-recruitment-2026` | HTTP 200 → https://geoplanetschool.camk.edu.pl/2026-2027-recruitment-in-the-discipline-of-astronomy/ |
| `esa-exploration-science-cofunded-phd` | HTTP 200 → https://explorationscience.esa.int/research-opportunities/call-for-co-funded-phd-research-proposals-for-esa-exploration-science/ |
| `hessian-ai-research` | HTTP 200 → https://www.hessian.ai/research/ |
| `cambridge-ieef-phd` | HTTP 200 → https://ieef.cam.ac.uk/new-phd-scholarships-available/ |
| `polyu-hkpfs-portal` | HTTP 200 → https://www.polyu.edu.hk/gs/prospective-students/hkpfs/ |
| `osu-comparative-studies-graduate-funding` | HTTP 200 → https://comparativestudies.osu.edu/graduate/prospective-graduate-students/graduate-funding |
| `gatech-eas-graduate-financial-assistance` | HTTP 200 → https://eas.gatech.edu/graduate-student-financial-assistance |
| `colorado-mechanical-phd-funding` | HTTP 200 → https://www.colorado.edu/mechanical/academics/ms-programs/funding-and-fellowships |
| `ua-grad-college-ga-benefits` | HTTP 200 → https://grad.arizona.edu/gaships/ |
| `cispa-postdoc-general` | HTTP 200 → https://career.cispa.de/jobs |
| `chalmers-ees-graduate-school` | HTTP 200 → https://www.chalmers.se/en/research/doctoral-studies/graduate-schools/energy-environment-and-systems/ |
| `kth-energy-phd-studies` | HTTP 200 → https://www.energy.kth.se/education/doctoral-studies/doctoral-studies-in-energy-technology-1.942695 |
| `univ-paris-cite-eiffel-doctorat-2027` | HTTP 200 → https://u-paris.fr/bourse-dexcellence-eiffel-2027/ |
| `erasmus-mc-phd-vacancies` | HTTP 200 → https://www.eur.nl/en/erasmusmc/graduate-school/phd-tracks/obtaining-phd-position/phd-vacancies |
| `ijs-young-researchers-fellowships` | HTTP 200 → https://www.ijs.si/ijsw/Young%20researchers%2C%20fellowships |
| `crest-genes-doctoral-contracts` | HTTP 200 → https://crest.science/research/doctoral-studies-and-phd-track/ |
| `ip-paris-econ-phd-track` | HTTP 200 → https://www.ip-paris.fr/education/phd-track/phd-track-economie |
| `cuhk-econ-phd-camp-2026` | HTTP 200 → https://www.econ.cuhk.edu.hk/en/news-and-events/event/cuhk-economics-phd-recruitment-camp-2026/ |
| `frbsf-sargent-dissertation-fellowship` | HTTP 200 → https://www.frbsf.org/work-with-us/careers/thomas-j-sargent-dissertation-fellowship/ |
| `harvard-hou-family-taiwan-fellowship` | HTTP 200 → https://fairbank.fas.harvard.edu/affiliation-2/hou-family-fellows-in-taiwan-studies/ |
