# 申请者画像（profile.yml）与简历要点（cv-facts.yml）

画像驱动 `/rank` 的硬性筛选和打分，也是网站“为我推荐”表单的完整版。示例见 [`profile.example.yml`](../profile.example.yml)。

**隐私**：`profile.yml`、`cv-facts.yml`、`applications/`、`rankings/` 都写进了 `.gitignore`，只留在申请者自己的电脑或私有仓库里，永不提交到公开仓库。网站版画像只存在浏览器 localStorage，不上传。

## profile.yml

| 字段 | 类型 | 用途 | 没填时 |
| --- | --- | --- | --- |
| `nationality` | ISO 两位代码 | `CN` 时按“中国学生能否申请”（数据里的 `cn_eligible`）筛选和加分 | 视为 `CN` |
| `education[]` | 列表 | 每段学历：`degree`（`bachelor`/`master`/`phd`）、`school`、`major`、`gpa`、`end`（`YYYY-MM`）、`status`（`completed`/`ongoing`） | — |
| `research.keywords` | 列表 | 研究方向关键词，中英文都可；按同义词表扩展（“机器学习”也会匹配 machine learning） | 不推荐任何机会 |
| `research.disciplines` | 列表 | 学科代码（同 `docs/schema.md`）；补充从关键词推断出的学科 | 从关键词推断 |
| `research.interests` | 文本 | 一段研究兴趣描述；`/rank` 里 Claude 读岗位简介时用来写一句话判断（程序打分不用） | — |
| `publications[]` / `projects[]` | 列表 | 论文、项目；`/apply` 起草套磁信时用 | — |
| `languages.ielts` / `toefl` | 数字 | 岗位写了雅思 / 托福要求且你的分数不够 → 排除 | 不按语言排除 |
| `languages.german` | `A1`–`C2` / `native` | 德语岗位（标题是德语或要求德语）需要 B2 以上 | 视为不会德语 |
| `languages.other` | 列表 | 其他语言，如 `[{lang: Norwegian, level: B2}]`；写了挪威 / 瑞典 / 丹麦 / 荷兰语，才保留用这些语言发布的公告 | 用这些语言发布的公告排除 |
| `target.levels` | 列表 | `phd` / `postdoc` | `[phd]` |
| `target.start` | `YYYY-MM` | 最早入学时间；岗位写明的开始时间早一个月以上 → 排除；也用来判断入学前能否拿到学位 | 不按开始时间排除 |
| `countries.accept` | 列表 | 可接受的国家；`EU`、`GLOBAL` 范围的项目视为可接受 | 都可以 |
| `countries.prefer` | 列表 | 偏好国家，加分 | — |
| `countries.exclude` | 列表 | 不考虑的国家 → 排除 | — |
| `funding.min_coverage` | 枚举 | `any` 不限 · `partial` 至少部分资助 · `full` 全奖或带薪（官网没写的保留、降分）· `confirmed` 只要官网写明全奖或带薪 | `any` |
| `funding.min_monthly_eur` | 数字 | 每月最低金额（约合欧元）；只在官网写了金额时比较 | 不比较 |
| `deadline.min_prep_days` | 整数 | 离截止不足这么多天 → 排除 | 14 |
| `eligibility.cn_only` | 布尔 | 只看明确写了中国学生可申请的（排除“待核实”） | `false` |
| `sensitive_field` | 布尔 | 方向敏感时，公告提到安全审查的岗位降分更多；英国理工科岗位提示 ATAS | `false` |

## 排序规则（scripts/rank.py 与网站共用）

**只看“现在可申请”的机会**（核实员或采集程序确认今天仍开放、截止没过）。

**硬性筛选**（命中任一条就排除，并写明原因）：
中国学生不可申请 / 公告写明限本国学生 · 层次不符 / 博后要求博士学位 · 要求硕士学位而入学前只有学士 · 雅思 / 托福不够 · 要求德语 · 公告用挪威语 / 瑞典语 / 丹麦语 / 荷兰语发布（画像 `languages.other` 写了该语言则保留）·
截止太近 · 开始时间早于你能入学的时间 · 资助低于底线（金额低于底线）· 不在可接受的国家。
官网没写的条件一律**不排除**（不猜），只在理由里提示“待核实”。

**打分**（0–100，规则与权重在 `scripts/rank_rules.py`，评测见 [`docs/rank-eval.md`](rank-eval.md)）：

| 项 | 满分 | 依据 |
| --- | --- | --- |
| 研究匹配 | 70 | 关键词（含中英文同义词）出现在标题：第 1/2/3 个命中的词 28 / 14 / 9 分，只在简介里 ×0.6，只命中复合词的一部分 ×0.5，方法类词（机器学习等）用在别的学科 ×0.5，越常见的词分越低，上限 50；岗位学科里属于你方向的比例 × 20 |
| 资助 | 10 | 全奖 / 带薪 10，部分或仅生活费 6，视项目而定 5，未写明 3 |
| 截止 | 8 | 还有 21–75 天最合适 8；更远 6 / 4；不足 21 天 5；滚动 6；即将开放 5；未写明 2 |
| 地区 | 7 | 偏好国家 7，没设偏好 4，其他 2 |
| 资格 | 5 | 中国学生可申 5，部分 3，待核实 1 |
| 安全审查 | 扣分 | 公告提到安全审查 −5（方向敏感 −15）；英国 + 敏感方向 + 理工科 −5 |

关键词匹配的细则（为什么“神经网络”不算神经科学、“Economic and Social Research Council”不算经济学）见 `scripts/rank_rules.py` 开头的说明。

**只推荐命中关键词的机会**：标题或简介里没有出现你的关键词（或同义词）的，即使学科相同也不进推荐，单列为“学科相同、未命中关键词”；学科与你的方向冲突的命中视为字面巧合，不算。
关键词和学科都没对上的，只计数为“方向不相关”。

## cv-facts.yml（简历要点）

`/setup` 从简历里**逐条摘录**的事实，之后 `/apply` 写的每一句经历都必须能在这里找到。只记录简历里写了的，不推断、不美化。

```yaml
source: cv.pdf               # 来自哪份简历
extracted: 2026-10-19
facts:
  - id: edu-1
    type: education          # education / publication / project / award / skill / work / language / other
    text: 2024-09 至 2027-06 某某大学 生物医学工程 硕士（在读），GPA 3.7/4.0
    quote: "M.Eng. Biomedical Engineering, XX University, 2024–2027 (expected), GPA 3.7/4.0"   # 简历原文
  - id: pub-1
    type: publication
    text: 第一作者论文，MICCAI 2026 Workshop 接收
    quote: "..."
```
