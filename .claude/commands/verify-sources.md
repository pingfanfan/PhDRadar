---
description: 专职核实：把全部信源分片，派多个 Haiku 子代理并行核实“机会是否仍然存在、链接、资格”，写回数据
argument-hint: <核实员编号 k> <核实员总数 n> <截止日期 YYYY-MM-DD>（如 "1 3 2026-10-14"）
---

**质量优先**：准确比速度重要；证据不足的结论改成 keep（不改字段），宁可留空也不要写错；资格拿不准保持 `'check'`。
目标：把**全部信源**核实一遍——机会是否还存在、链接是否有效、中国大陆学生能否申请，
并补全结构化字段：资助力度（coverage 全奖/带薪/半奖…）、金额（stipend）、截止（deadline/deadline_note）、状态（status）、国际生要求（requirements）。
同一轮对话里所有子代理**共享 200 次网页搜索额度**，所以每轮 80 条、4 个子代理各 20 条。

1. `git pull --rebase`。解析 `$ARGUMENTS` 为 k、n、截止日期 D（只核实 verified 早于 D 的条目）。
2. 运行 `python scripts/verify_queue.py --scope all --worker k --of n --before D --need-fields --n 80 --chunks 4 --out research/inbox/<今天>-<时分>-verify-v<k>`。
   若输出“剩余 0 条”：本分片已全部核实。用 `list_triggers` 找到名为“PhD 信源专职核实 · 核实员k”的 Routine，`update_trigger` 设 `enabled=false`，回复“核实员 k 已完成全量核实”，结束。
3. 读取 `research/verify-prompt.md`，为每个分片文件并行启动一个子代理（model: haiku，后台运行），提示词 = verify-prompt.md 全文 + 该分片文件内容。
4. 等全部子代理返回，把每个子代理的 YAML 列表合并存为 `research/inbox/<同名前缀>-result.yml`。
   抽查：`update`/`delete` 的 evidence 是否真的支持结论；不支持的改成 `keep`（不改字段）。`cn_eligible` 只能依据官方页面改，拿不准保持 `'check'`。
   子代理漏掉的条目不要写入结果（下轮会再排进队列）。
5. `python scripts/apply_verification.py research/inbox/<同名前缀>-result.yml`。
6. 提交前运行 `python -m pytest -q tests` 和 `python scripts/build_sources.py --validate-only`，都通过才提交；
   **不要提交生成文件**（`git checkout -- SOURCES.md sources README.md docs/assets data/export 2>/dev/null`）。
   只提交 `_data/` 与 `research/inbox/` 下本轮文件。推送前 `git pull --rebase`，冲突时以远端为准重新运行第 5 步，最多重试 3 次。
7. 三行中文总结：本轮核实条数、保留/更新/删除、本分片剩余条数。
