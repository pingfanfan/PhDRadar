---
description: 持续研究：按分配挑选切片，派子代理寻找新的带奖博士/博后信源并入库（首要目标：扩大信源总量）
argument-hint: <研究员编号 k> <研究员总数 n>（如 "1 3"），默认 "1 1"
---

**首要目标：质量优先于数量**（仓库主人要求）。只收经搜索结果确认、有 `evidence`、指向官方页面、带资助的博士与博士后机会（用 `levels` 标层级）；没有数量指标，宁少勿滥。合并时没有 evidence 的条目会被 `merge_sources.py` 拒绝，不要用 `--allow-no-evidence` 绕过。其次才是扩大覆盖。

注意：同一轮对话里所有子代理**共享 200 次网页搜索额度**，所以每轮做 **2 个研究切片 + 1 批核实**（各约 60 次搜索）。

1. `git pull --rebase`。解析参数 `$ARGUMENTS` 为研究员编号 k 与总数 n（默认 1 1），目标文件名为 `worker-k`。
2. 读取 `research/slices.yml`，只看序号满足 `index % n == k-1` 的切片（index 从 0 开始），从中选出 `last_run` 最早的 2 个。
3. 读取 `research/subagent-prompt.md` 作为子代理说明，为每个切片并行启动一个子代理（model: haiku，后台运行），把切片的 `focus` 附在说明末尾。
   提示子代理优先找**列表型、聚合型**信源（一个页面列出许多项目/导师/岗位的那种），以及尚未覆盖的国家、大学、学科。
   同时运行 `python scripts/verify_queue.py --worker k --of n --n 25 > research/inbox/<日期>-verify-queue-worker-k.yml`，
   把 `research/subagent-prompt.md` 换成 `research/verify-prompt.md`、末尾附上队列内容，再启动一个核实子代理（同样 haiku、后台）。
   **核实优先于新增**：失效链接要找到官方新地址或删除；`cn_eligible: 'check'` 只有在官方页面明确说明时才改，不要猜。
4. 等待全部子代理返回，把各自的 YAML 列表存为 `research/inbox/<日期>-<切片id>.yml`。
   剔除：第三方转载/内容农场、两年以前的过期帖、付费中介、与“带资助博士/博后”无关的页面。
5. 运行 `python scripts/merge_sources.py research/inbox/<本轮文件>... --target worker-k`（写入 `_data/sources_extra/worker-k.yml`）。
   把核实子代理的 YAML 存为 `research/inbox/<日期>-verify-worker-k.yml`，抽查几条 evidence 是否支持结论（不支持的改成 keep），
   然后运行 `python scripts/apply_verification.py research/inbox/<日期>-verify-worker-k.yml`。
6. 更新 `research/slices.yml` 中这些切片的 `last_run`（今天）和 `added`（本轮新增条数）。
   **扩展规则**：某切片本轮新增少于 3 条，且上次也少于 3 条 → 把它拆成 2–4 个更细的新切片（按国家×学科、按大学、按资助类型等），
   或新建覆盖空白领域的切片，追加到 `research/slices.yml` 末尾（`last_run: 2000-01-01`），保证总量持续增长。
7. 运行 `python -m pytest -q tests` 与 `python scripts/build_sources.py --validate-only`。
   **不要提交生成文件**（`SOURCES.md`、`sources/`、`README.md`、`data/export/` 由 GitHub Actions 统一生成；提交前执行 `git checkout -- SOURCES.md sources README.md docs/assets data/export 2>/dev/null`）。
   提交并推送到 `main`（推送前 `git pull --rebase`，冲突时以远端为准重新合并自己的 extra 文件，最多重试 3 次）。
8. 若 `reports/source-health.md` 中有本研究员新增的条目被标为 ❌ 失效，修正或删除后再提交。
9. 用三五行中文总结：本轮切片、新增条数、核实结果（保留/更新/删除）、信源总数（`python scripts/build_sources.py --validate-only` 的输出）、剔除原因。
