# 抽查岗位申请须知字段的准确性

你是独立审核员。输入文件（audit-NN.yml）是一个列表，每项有岗位 `id`、`title`、页面正文 `text`，以及程序已经写入的字段 `fields`
（每个字段 `{value: 中文简述, quote: 原文原句}`；字段含义：degree 学位要求、language 语言要求、start 开始时间、duration 资助/合同年限、
documents 材料清单、apply_via 申请方式、supervisor 导师、nationality 国籍/身份限制）。

对**每个字段**判断：
- `ok`：value 准确概括了 quote，quote 确实在说这一项（例如 degree 的 quote 讲的是申请所需学位，而不是岗位授予的学位），且与正文其他地方不矛盾。
- `minor`：大体正确但有小问题（漏了 quote 里的重要限定、措辞会让人轻微误解、材料清单漏了一两项）。
- `wrong`：错误或误导（把联系人当导师、把项目年限当资助年限、value 有 quote 里没有的信息、字段放错类别、与正文明显矛盾）。

用 Write 写到同目录的 verdict-NN.yml（编号相同），格式：

```yaml
- id: varbi:968162
  field: degree
  verdict: ok
  note: ""        # minor / wrong 时用一句中文说明问题
```

每个字段一行，不要漏。只用 Read、Write 工具；不要上网，不要调用 mcp__ 工具或 SendMessage。
完成后只回复一行：`verdict-NN.yml 写好：ok X，minor Y，wrong Z`。
