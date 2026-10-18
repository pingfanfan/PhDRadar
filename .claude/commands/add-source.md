---
description: 向信源库添加一个新的 PhD 资助信源
argument-hint: <URL 或信源名称>
---

把用户给出的信源 `$ARGUMENTS` 加入 `_data/sources.yml`：

1. 先在 `_data/sources.yml` 中搜索名称和域名，确认没有重复。
2. 打开该网页，确认它确实提供（或帮助找到）带资助的 PhD 机会，并判断：
   - 最合适的 `category`（见文件顶部 categories）；
   - `regions`、`disciplines`、`funding`、`access`（是否有 RSS/邮件订阅/API）；
   - 中国大陆学生是否可申（`cn_eligible`，不确定就标 `'check'`）。
3. 尽量把 `url` 设为 PhD/带奖筛选后的页面，而不是首页。
4. 用简体中文写 1–2 句 `notes`，告诉中国申请者怎么用、要注意什么；`verified` 写当前年月。
5. 将条目插入对应分类区块末尾，运行 `python scripts/build_sources.py`，确认校验通过。
6. 向用户简要汇报新增条目。
