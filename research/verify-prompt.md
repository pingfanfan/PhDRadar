Verification task (web search only; do NOT edit any files). Below is a YAML list of catalogue entries (funded PhD/postdoc sources for Chinese mainland students) whose information is uncertain: dead links (`link_status`), unknown eligibility (`cn_eligible: check`), or stale checks.

Load tools with ToolSearch "select:WebSearch,WebFetch". WebFetch only works for github.com here; confirm everything else through WebSearch results. Use up to ~50 searches, about 2 per entry. Work fast.

QUALITY BAR (the owner's top priority — accuracy beats speed or volume): decide only from what you actually saw in search results; if you cannot confirm something, say so (keep, leave the field out, cn_eligible stays 'check'). A wrong "yes" is far worse than "check". Delete entries that are reposts/aggregator copies of an official call, content farms, paid agencies, or pages with no funding information.

For EACH entry decide one action, based only on what you actually saw in search results:
- keep: the page/programme still exists at that URL and the notes are correct.
- update: something is wrong or can be made more certain. Give only the changed fields among
  name, url, notes, cn_eligible, levels, funding, regions, disciplines, category.
  * Dead link (404/DNS) → find the programme's current official URL (https) and put it in `url`.
  * cn_eligible: set 'yes' only if an official page says international students / all nationalities are eligible and funded; 'partial' if only some routes or a capped share is open to internationals; 'no' if restricted to citizens/home/EU; keep 'check' if you cannot find an official statement. NEVER guess.
  * levels: [phd] / [postdoc] / [phd, postdoc] as the page actually offers.
  * notes: Simplified Chinese, 1–2 practical sentences, cite what the official page says (deadline, eligibility).
- The key question is: **does this opportunity still exist?** A recurring programme/scholarship/portal whose current round is closed still exists → keep (put the next expected round in notes if seen). A one-off posting (a single advertised position or a dated call) whose deadline has passed and that has no newer round → delete.
- delete: the programme is discontinued/closed for good, the URL is a content farm/paid agency, it is unrelated to funded PhD/postdoc, or a dead link with no replacement found.

**Also fill the structured opportunity fields** (readers and a future application agent rely on them). For every entry, add any of these that are missing or wrong to `fields` (this makes the action `update`), using only what the official page / search result states:
  * coverage: full (tuition + living stipend, or salaried where tuition is free) | salary (employment contract: EU PhD posts, postdocs) | partial (part of tuition or living costs) | tuition (tuition waiver only) | stipend (living allowance only) | varies (portal/list where programmes differ) | none | unknown (you looked, but the source does not say — ALWAYS set coverage, use unknown rather than leaving it empty)
  * stipend: amount as stated, e.g. "€2,100/月（税后）", "£20,780/年", "HKD 27,600/月"
  * deadline: next or current application deadline as YYYY-MM-DD, or rolling | varies | unknown
  * deadline_note: Simplified Chinese, e.g. "每年 1 月中旬截止；2027 轮未公布", "首批 11 月 15 日，次批 1 月 15 日"
  * status: open (accepting now) | upcoming (next round announced/expected soon) | closed (this round closed, programme recurs) | rolling | ongoing (portal/job board/list that keeps updating)
  * requirements: Simplified Chinese, one line on international applicant requirements: degree (硕士/本科), language (IELTS/TOEFL), nationality limits, age/years-since-PhD, need a supervisor first, etc.
  Leave a field out rather than guess.

**Only output entries you actually checked with at least one search in this run.** If you ran out of searches or skipped an entry, leave it OUT of the YAML entirely (do not write keep with "not searched") — an unchecked keep would wrongly mark the entry as verified today.

Output exactly one YAML code block, one item per checked entry, in this schema:
  - id: <same id>
    action: keep | update | delete
    fields: {url: https://..., cn_eligible: 'yes', coverage: full, stipend: "€2,100/月", deadline: 2027-01-15, deadline_note: ..., status: upcoming, requirements: ..., notes: ...}   # only for update
    evidence: "<search result title — URL that supports the decision>"
Quote 'yes'/'no'/'NO'. After the block, at most 5 lines on entries you could not decide (those should be `keep` without changing cn_eligible).

ENTRIES:
