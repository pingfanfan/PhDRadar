# 信源可访问性报告

更新于 2026-10-19 10:56 UTC，由 `scripts/access_report.py` 实际访问生成：从两个网络位置各访问一次（我们的服务器，以及 GitHub Actions，2026-10-19 10:43 UTC），任一处能打开即算能打开。

## 招聘平台：能否被程序接入

我们只用平台允许的方式读取（遵守 robots.txt 与访问频率要求），不绕过拦截。

| 平台 | 状态 | 接入方式 | 当前收录岗位 | robots.txt | 访问（本服务器 / Actions） | 说明 |
|---|---|---|---:|---|---|---|
| [FindAPhD](https://www.findaphd.com/) | ✅ 已接入 | 站点地图 + 岗位页（在 GitHub Actions 上采集） | 455 | 允许 | HTTP 403 / HTTP 200 | 本报告所在服务器被拦截（403），采集改在 GitHub Actions 上运行 |
| [Nature Careers](https://www.nature.com/naturecareers/) | ✅ 已接入 | 站点地图 + 岗位页 | 315 | 允许 | HTTP 200 / HTTP 200 | — |
| [jobs.ac.uk](https://www.jobs.ac.uk/) | ✅ 已接入 | 搜索列表 + 岗位页 | 285 | 允许 | HTTP 200 / HTTP 200 | — |
| [THE Unijobs](https://www.timeshighereducation.com/unijobs/) | ✅ 已接入 | 站点地图 + 岗位页 | 226 | 允许 | HTTP 200 / HTTP 200 | — |
| [AcademicTransfer（荷兰）](https://www.academictransfer.com/en/) | ✅ 已接入 | 站点地图 + 岗位页 | 187 | 允许，要求每 10 秒一次 | HTTP 200 / HTTP 200 | — |
| [INSPIRE-HEP Jobs](https://inspirehep.net/jobs) | ✅ 已接入 | 官方公开接口 | 164 | 允许 | HTTP 200 / HTTP 200 | — |
| [Varbi（瑞典高校）](https://lu.varbi.com/en/) | ✅ 已接入 | 各校列表页 + 岗位页 | 138 | 允许 | HTTP 200 / HTTP 200 | — |
| [Jobbnorge（挪威）](https://www.jobbnorge.no/) | ✅ 已接入 | 官方公开接口 | 130 | 无 robots.txt（HTTP 404） | HTTP 200 / HTTP 200 | — |
| [Academic Jobs Online](https://academicjobsonline.org/ajo/jobs) | ✅ 已接入 | RSS + 岗位页（每 5 秒一次） | 88 | 允许，要求每 5 秒一次 | HTTP 200 / HTTP 200 | — |
| [Science Careers](https://jobs.sciencecareers.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 73 | 允许 | HTTP 200 / HTTP 200 | — |
| [Inria Jobs](https://jobs.inria.fr/public/classic/en/offres) | ✅ 已接入 | 列表页 + 岗位页 | 54 | 允许 | HTTP 200 / HTTP 200 | — |
| [DAAD PhDGermany](https://www.daad.de/en/studying-in-germany/phd-studies-research/phd-germany/) | ✅ 已接入 | 列表页 + 岗位页（链接需带 phd-id） | 26 | 允许，要求每 2 秒一次 | HTTP 200 / HTTP 403 | — |
| [Physics Today Jobs](https://jobs.physicstoday.org/) | ✅ 已接入 | 站点地图 + 岗位页 | 17 | 允许 | HTTP 200 / HTTP 200 | — |
| [ETH Zurich Jobs](https://jobs.ethz.ch/) | ✅ 已接入 | 列表页 + 岗位页 | 2 | 允许 | HTTP 200 / HTTP 200 | — |
| [马普学会（Max Planck）](https://www.mpg.de/stellenboerse) | ✅ 已接入 | RSS + 岗位页 | — | 允许 | HTTP 200 / HTTP 200 | — |
| [EURAXESS](https://euraxess.ec.europa.eu/jobs/search) | ⛔ 不允许 | — | — | 禁止 | HTTP 200 / HTTP 200 | robots.txt 禁止程序读取岗位页（Disallow: /jobs/*）；已起草数据合作申请 |
| [academics.de（德国）](https://www.academics.de/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | robots.txt 写明自动采集需书面许可；已起草数据合作申请 |
| [FindAPostdoc](https://www.findapostdoc.com/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [Academic Positions](https://academicpositions.com/) | ⛔ 不允许 | — | — | 允许 | HTTP 403 / HTTP 403 | 所有程序访问返回 403 |
| [德国联邦劳动局职位搜索接口](https://jobsuche.api.bund.dev/) | ⛔ 不允许 | — | — | 无 robots.txt（HTTP 403） | HTTP 403 / HTTP 403 | 官方开放数据接口（bund.dev 公开文档）；本服务器访问被拒，看 GitHub Actions 上能否访问 |
| [Chronicle Jobs（美国）](https://jobs.chronicle.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但抽查 40 个岗位页都不写截止日期 |
| [Inside Higher Ed Careers](https://careers.insidehighered.com/) | ⏸ 未接入 | — | — | 允许 | HTTP 200 / HTTP 200 | 允许访问，但岗位页只有广告下架日期，没有申请截止日期 |

## 核对过的高质量信源：能否打开

对 2134 条逐页核对过官网的信源实际访问一次：✅ 能打开 2129（99%）· ⚠️ 服务器拦截脚本或需登录 4 · ❌ 失效 1。

“拦截”多数是网站拒绝脚本访问（403、Cloudflare 验证、限制境外访问），用浏览器通常能正常打开；“失效”是 404/410 或域名解析失败，已排进核实队列优先处理。

### ❌ 失效（1）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [CUHK 历史学系 HKPFS 博士页](https://www.history.cuhk.edu.hk/en/study/phd-programme/hkpfs/) | HTTP 404 |

</details>

### ⚠️ 拦截脚本 / 需登录（4）

<details><summary>展开清单</summary>

| 信源 | 结果 |
|---|---|
| [CREST / GENES 博士合同（ENSAE 经济与统计）](https://crest.science/?p=11510) | ReadTimeout |
| [Cyber Valley 职位总页（图宾根/斯图加特）](https://cyber-valley.de/en/jobs) | HTTP 500 |
| [EUROfusion 工程资助（Engineering Grants）](https://euro-fusion.org/eurofusion-news/applications-open-for-the-2027-eurofusion-engineering-grants/) | SSLError |
| [波尔图理工学院健康学院（ESS-IPP）康复科学博士项目](https://www.ess.ipp.pt/news/applications-open-2013-doctoral-programme-in-rehabilitation-sciences-202620132027) | ConnectionError |

</details>

