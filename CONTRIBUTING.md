# 贡献指南

所有信源都保存在 [`_data/sources.yml`](_data/sources.yml) 中，`SOURCES.md` 和网页版都由它生成。**请只修改 YAML，不要手动编辑 `SOURCES.md`。**

## 添加一个信源

在对应分类下追加一条：

```yaml
  - id: example-portal            # 唯一，小写 kebab-case
    name: Example Portal
    url: https://example.org/phd  # 尽量指向 PhD/带奖筛选页，必须是 https
    category: aggregators         # 见文件顶部 categories
    regions: [EU, DE]             # GLOBAL / EU / UK / DE / NL / 'NO' / SE / ... / US / CA / AU / HK / SG / JP / KR
    disciplines: [all]            # all / cs / ai / math / physics / chem / bio / eco / neuro / geo / engineering / social / humanities / econ / business / med
    funding: position             # position / scholarship / fellowship / mixed / info
    levels: [phd, postdoc]        # 可选：phd / postdoc，缺省为 [phd]
    cn_eligible: 'yes'            # 'yes' / 'partial' / 'check' / 'no'（务必加引号）
    access: [web, rss]            # web / rss / email / api / login / app
    language: en
    coverage: full                # 可选：full 全奖 / salary 带薪 / partial 半奖 / tuition 仅免学费 / stipend 仅生活费 / varies / none / unknown
    stipend: €2,100/月（税后）     # 可选：金额原文
    deadline: 2027-01-15          # 可选：YYYY-MM-DD 或 rolling / varies / unknown
    deadline_note: 每年 1 月中旬截止  # 可选
    status: upcoming              # 可选：open / upcoming / closed / rolling / ongoing
    requirements: 需硕士；IELTS 6.5；国际生可申  # 可选：国际生要求
    notes: 给中国申请者的一两句说明：如何筛选、是否收国际生、截止时间等。
    verified: 2026-10             # 你核实的年月
```

> 字段的完整定义（供程序/agent 使用）见 [docs/schema.md](docs/schema.md)。

> ⚠️ YAML 会把 `yes`、`no`、`NO`（挪威）等解析成布尔值，所以 `cn_eligible` 和挪威地区代码都要加引号。

## 收录标准

- 能找到**带资助**（学费减免 + 生活费，或带薪岗位）的 PhD 机会，或能帮助找到这类机会（导师名单、邮件列表、工具）；
- 中国大陆学生**不可申**的信源仅在容易误解时收录（如 NSF GRFP），并标为 `'no'`；
- 不收录收费中介、付费“内推”渠道。

## 本地校验

```bash
pip install pyyaml
python scripts/build_sources.py          # 校验并重新生成 SOURCES.md
python scripts/build_sources.py --check  # CI 使用：校验 + 确认 SOURCES.md 已更新
python scripts/check_links.py            # 检查所有链接（需外网）
```

## 报告失效链接或政策变化

直接开 Issue，注明信源 `id`、问题和官方出处链接即可。
