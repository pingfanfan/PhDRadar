Research task (web search only; do NOT edit any files). We maintain a catalogue of sources of FULLY FUNDED PhD and POSTDOC opportunities for Chinese (mainland) students (postdocs: salaried positions and individual postdoc fellowships): _data/sources.yml（在仓库根目录下）. First grep it for ids/urls so you only return NEW items.

Load tools with ToolSearch "select:WebSearch,WebFetch". WebFetch only works for github.com here; confirm everything else through WebSearch results. Use up to ~60 searches. Work fast.

Individual recruitment posts by a named PI on social platforms (Xiaohongshu/小红书, Zhihu, WeChat articles, Weibo, Bilibili, X, LinkedIn, Bluesky) COUNT as items: use category recruiting-posts, url = the post itself, name = '<PI 姓名/课题组> · <学校> · <方向> 招生', and put the post date, position level, funding and contact method in notes. Prefer posts from 2026 onward.

Return ONLY items you saw in search results (exact URL from a result). Prefer specific official pages (a graduate school's funded-PhD/vacancies page, a mailing-list archive, a programme's call page) over homepages. Skip paid agencies, content farms, and anything closed/discontinued.

QUALITY OVER QUANTITY (the owner's top priority): there is NO minimum count. Return only entries you are confident about; 5 solid entries beat 40 padded ones. Every entry MUST carry an `evidence` field (the search result title — URL where you saw it). Prefer the official page of the university / institute / funder; skip reposts, aggregators that merely copy an official call, content farms, paid agencies, and anything you could not see funding information for. Never guess funding, deadline or eligibility: leave the field out (or cn_eligible 'check') instead.

Output exactly one YAML code block: a list of entries (as many as you can stand behind, possibly very few) with this schema (notes in Simplified Chinese, 1-2 practical sentences for Chinese applicants: how to use it, international eligibility, typical deadline):
  - id: kebab-case-unique
    name: ...
    url: https://...
    category: recruiting-posts | postdoc-fellowships | aggregators | national-portals | gov-scholarships | university-schemes | doctoral-programs | fellowships | discipline | pathways | people-channels | faculty-aggregators | github-resources | chinese-community | tools
    regions: [GLOBAL | EU | UK | DE | FR | NL | BE | CH | AT | IT | ES | PT | IE | SE | DK | FI | 'NO' | PL | CZ | US | CA | AU | NZ | HK | MO | SG | JP | KR | IL | SA | AE | CN ...]
    disciplines: [all | cs | ai | math | physics | chem | bio | eco | neuro | geo | engineering | social | humanities | econ | business | med]
    funding: position | scholarship | fellowship | mixed | info
    levels: [phd] | [postdoc] | [phd, postdoc]
    cn_eligible: 'yes' | 'partial' | 'check' | 'no'
    access: [web | rss | email | api | login | app]
    language: en | zh | de | fr | ...
    coverage: full | salary | partial | tuition | stipend | varies | none   # 全奖/带薪/半奖/仅免学费/仅生活费/视项目而定
    stipend: "<amount as stated, e.g. €2,100/月>"            # omit if not stated
    deadline: YYYY-MM-DD | rolling | varies | unknown
    deadline_note: "<中文：每年几月截止、下一轮时间>"
    status: open | upcoming | closed | rolling | ongoing     # ongoing = 持续更新的门户/列表
    requirements: "<中文一句：国际生的学历、语言、国籍、年限要求>"
    notes: ...
    verified: 2026-10
    evidence: "<search result title — URL>"
Fill coverage/stipend/deadline/status/requirements only from what the page or search result says; omit a field rather than guess.
If an item has a machine-readable feed (RSS/Atom, mailing-list archive, CSV/JSON, API), add `feed: <url>`.
After the YAML block, add at most 5 lines of things you could not confirm.

YOUR SLICE (focus):
