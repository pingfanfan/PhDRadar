---
description: 抽查信源是否仍然有效、政策是否变化
argument-hint: [分类 id 或信源 id，可选]
---

对 `_data/sources.yml` 中 `$ARGUMENTS` 指定的信源（为空则抽查 `verified` 最早的 15 条）逐条核实：

1. 访问 `url`，确认页面仍存在且内容相关；失效时搜索正确的新地址。
2. 核对 `notes` 中的政策性描述（国际生资格、截止时间、金额等）是否仍然准确。
3. 更新有变化的条目和 `verified` 字段，运行 `python scripts/build_sources.py`。
4. 汇总：哪些已更新、哪些无法确认（保留原样并说明原因）。
