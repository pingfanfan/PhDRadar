# 从岗位原文抽取申请须知字段

你要从海外博士 / 博后岗位公告的正文里，摘出申请者最需要的几项信息，给中国学生看。
**只摘原文里明确写了的**；没写就不输出这一项。宁可少，不可错——程序会逐条校验，不合格的整项丢弃。

## 输入

一个 YAML 文件（bundle-NNN.yml），是一个列表，每项有：
- `id`：岗位编号（原样照抄）
- `title`、`org`、`level`（phd / postdoc）
- `have`：程序已经用规则取到的字段名，**这些字段不用再输出**
- `text`：岗位页面正文（已去掉导航和页脚）

## 输出

用 Write 工具写到同目录的 out-NNN.yml（编号与输入相同），内容是一个 YAML 列表（不要代码块围栏），每个输入岗位一项、顺序相同：

```yaml
- id: varbi:968162
  fields:
    degree:
      value: 社会工作或相近学科硕士（至少 120 学分，其中 30 学分为硕士阶段）
      quote: "the applicant must have completed courses comprising at least 120 credits in social work or an adjacent subject, of which at least 30 credits are at master’s level"
    language:
      value: 英语口语与写作良好；需会瑞典语（博士课程主要用瑞典语授课）
      quote: "A good command of English, both in speech and writing Proficiency in Swedish to facilitate participation in doctoral courses in social work"
    documents:
      value: 求职信、简历、学位证书与成绩单、硕士论文、研究计划（不超过 3,000 词）、两位推荐人
      quote: "The application should include: a cover letter where the applicant details the reasons behind their interest in the position a list of qualifications (CV) degree certificate with a complete transcript of the courses included, or a certified list of completed courses with grades and dates a copy of Master’s thesis (60 or 120 credits), or equivalent where applicable, copies of publications or certificates for other qualifications a brief research plan, no more than 3,000 words, in which the intended thesis project is described, specifying the problem statement, overall aim, possible theoretical perspectives, methods and material two references, such as a teacher, supervisor, or former or current manager"
- id: jobs-ac-uk:DTG436
  fields: {}
```

找不到任何字段的岗位也要输出，写 `fields: {}`。

## 字段

| 字段 | value 写什么（中文，≤80 字） | 例子 |
|---|---|---|
| `degree` | 申请时需要的学位与专业 | `物理、化学或材料科学硕士（两年制，120 ECTS）` |
| `language` | 语言要求；写了考试和分数就照写 | `英语；IELTS 6.5（单项不低于 6.0）或同等` |
| `start` | 开始 / 入职时间 | `2027 年 1 月 15 日或协商` · `2027 年 10 月` · `尽快` |
| `duration` | 资助或合同年限 | `4 年（首份合同 12 个月，考核后延长 36 个月）` |
| `documents` | 需提交的材料，用顿号分隔 | `求职信、简历、成绩单、两封推荐信` |
| `apply_via` | 必须以 `在线系统`、`邮件` 或 `其他` 开头，可加冒号补充 | `在线系统：通过招聘系统提交` · `邮件：发给 x@y.edu` |
| `supervisor` | 导师 / 项目负责人姓名（原文写了才写，保留原文拼写） | `Marian Klamer 教授` |
| `nationality` | 国籍、居留或学费身份限制（原句里写了限制或明确“国际生可申”才写） | `英国、欧盟与国际学生均可申请` · `仅限英国学费身份` |

## quote（原句）的硬性规则

1. **从 text 里逐字复制一段连续文字**，包括原来的标点和大小写；不要翻译、不要改写、不要拼接两处、不要用省略号 `...`。
   程序会检查它是否原样出现在正文里（只容忍空白和弯直引号的差别）。
2. 长度 6–400 个字符（`documents` 可到 900）；尽量选最短、但能独立支撑 value 的那一句。
3. **value 里出现的每个数字都必须在 quote 里出现**（英文数字词 four/two、月份名 January 算数）。不要换算币种、不要推算年份、不要把学分换成年数。
   数字比对忽略前导零和千分位：原句 `01/12/2026`、`15.09.2026`、`2026-09-01` 都可以写成“2026 年 12 月 1 日”这类形式（日月顺序按原文所在国家的写法判断，拿不准就不写）。
4. value 一律写成中文文字（日期写“2026 年 12 月 1 日”，不要写 `2026-12-01` 这种裸日期）。
5. value 只概括 quote 说的内容，不加 quote 里没有的信息；不写“未写明”“不详”之类——没有就不输出。

## 判断要点

- 正文可能是法语、德语、瑞典语、荷兰语等：value 照样写中文，quote 保持原文语言逐字复制，不要翻译。

- `degree`：写申请条件，不是岗位将授予的学位。“PhD position” 本身不是学位要求；博后岗位通常是“博士学位（或即将获得）”。只写“学士或硕士均可”时照写。
- `language`：只有“沟通能力好”这类空泛说法、没提到具体语言时，不要输出。说了“English”就可以写“英语……”。
- `start`：“as soon as possible” → 尽快；“by agreement / to be agreed” → 协商确定。页面上结构化栏目和正文矛盾时，用正文。
- `duration`：只写合同 / 资助年限（例如 “four-year studentship”、“for a period of 4 years”、“2-year contract”）；不要把“3 年制博士项目”与资助年限混为一谈，除非原文说资助覆盖该期限。
- `apply_via`：看“how to apply / application”部分：通过申请系统 / 网站 / 按钮提交 → 在线系统；发邮件给某人 → 邮件（写上邮箱）；其他方式（例如先联系导师再在线申请）→ 其他。
- `supervisor`：只写原文明确是导师、PI、supervisor、项目负责人的人；只是“联系人 / HR”不算。
- `nationality`：例如 “open to UK and international students”、“only UK/home fee status”、“EU citizens only”。只写原句，不要根据学校所在国推断。

只用 Read、Write 工具；不要上网搜索，不要调用任何 mcp__ 工具或 SendMessage。完成后只回复一行：`out-NNN.yml 写好，N 个岗位，共 M 个字段`。
