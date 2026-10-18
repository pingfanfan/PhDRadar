# 抓取器（scrapers）

把信源库里能自动访问的平台变成结构化岗位数据，统一去重、识别国际生资格，输出 `data/jobs.json` 和 `data/jobs.md`。

## 快速使用

```bash
pip install -r requirements.txt
python scripts/scrape.py --list                                  # 列出全部抓取器
python scripts/scrape.py -s euraxess,jobbnorge -k "machine learning"
python scripts/scrape.py --new-only                              # 只看上次之后的新岗位
python scripts/probe_sources.py                                  # 核查全部信源 + 试跑抓取器
```

GitHub Actions 会每天自动抓取（`.github/workflows/scrape.yml`），每周核查一次信源（`probe.yml`），
结果提交到 `data/` 和 `reports/source-health.md`。

## 输出字段

| 字段 | 含义 |
| --- | --- |
| `source` / `id` | 信源 id（与 `_data/sources.yml` 一致）/ 全局唯一 id，用于去重 |
| `title` `url` `institution` `country` `city` | 岗位基本信息 |
| `posted` `deadline` | 发布/截止日期（YYYY-MM-DD，抓不到为空） |
| `eligibility` | `international`（明确对国际生开放）/ `restricted`（限本土、限国籍或只覆盖本土学费）/ `unknown` |
| `funding` | `funded` / `self-funded` / `unknown` |
| `flags` | 如 `security-screening`（提到 ATAS、出口管制、安全审查） |

`eligibility`、`funding`、`flags` 是根据文字的启发式判断，**投递前务必读原文确认**。

## 新增一个抓取器

1. 在 `scrapers/sources/` 新建模块，定义 `SOURCE_ID`（必须是 `_data/sources.yml` 中已有的 id）和
   `fetch(fetcher, *, keywords, limit) -> list[Job]`；
   只有 RSS/Atom 的站点不用写代码，在 `scrapers/sources/__init__.py` 的 `FEEDS` 里加一行即可。
2. 一律通过传入的 `fetcher.get()` 发请求（自动遵守 robots.txt、按站点限速、处理 429 重试）。
3. 在 `tests/test_scrapers.py` 加一个离线样例测试，运行 `python -m pytest -q tests`。
4. 推送后 `probe-sources` 工作流会真实试跑，在运行摘要里查看结果。

## 抓取礼仪

- 默认遵守 robots.txt，每个站点请求间隔 ≥ 1 秒；
- 只抓公开列表页，不登录、不绕过验证码；
- 仅供个人求学检索使用，请遵守各网站的服务条款。
