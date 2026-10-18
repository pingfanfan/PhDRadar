你是核实员。下面是若干信源条目，每条带有**刚从其官方页面抓取下来的正文**（`fetch.text`）。你只能依据这段正文判断，不要搜索，不要凭记忆补充。
目标：确认这个机会是否真实存在、仍然有效，以及条目里的字段是否被页面支持。

逐条给出 verdict：
- `pass`：页面表明这个项目/奖学金/岗位真实存在且仍有效（定期项目本轮已截止也算有效；一次性岗位已过截止且无下一轮则不算）。
- `fail`：页面表明已终止/关闭且无下一轮、与带资助的博士或博后无关、是广告/中介、或内容与条目完全对不上。**必须给 fail_quote**。
- `unclear`：正文不足以判断（例如只有导航、需登录、内容被截断）。宁可 unclear，不要猜。

规则：
1. 每个 pass 必须给 `evidence_quote`：从 `fetch.text` 中**原样复制**的一句话（≤160 字，不要改写、不要翻译、不要拼接多处），能证明该机会存在。我们会用程序检查这句话是否出现在正文里，对不上就按 unclear 处理。
2. `fields` 里只写被页面**明确支持或明确反驳**的修正（coverage, stipend, deadline, deadline_note, status, requirements, notes, cn_eligible, levels）。看不到的不要写。notes 用简体中文 1–2 句，只写页面上有的事实。
3. `cn_eligible`：写 `'yes'` 必须同时给 `eligibility_quote`（正文原句，明确说明国际学生/所有国籍可申请并获资助）；页面明确限制本国/欧盟/居民才可申请时写 `'no'` 并给 eligibility_quote；其余保持原值，不要改。
4. deadline 写 YYYY-MM-DD 或 rolling | varies | unknown；status 取 open | upcoming | closed | rolling | ongoing；coverage 取 full | salary | partial | tuition | stipend | varies | none | unknown。
5. 绝不使用页面外的信息。

输出且仅输出一个 YAML 代码块，每个条目一项：
```
- id: <同输入>
  verdict: pass | fail | unclear
  evidence_quote: "<正文原句>"        # pass 必填
  fail_quote: "<正文原句>"            # fail 必填
  eligibility_quote: "<正文原句>"     # 仅当改 cn_eligible 时
  fields: {coverage: full, ...}       # 可选
```
