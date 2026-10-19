/* 网站“为我推荐”的排序：scripts/rank.py 的浏览器版，规则来自 assets/rank-rules.json（由 scripts/rank_rules.py 生成）。
   改这里要同步改 rank.py；tests/test_rank.py 会用 node 跑这份文件，检查两边结果一致。画像只在浏览器里，不上传。 */
(function (root) {
  "use strict";
  const CJK = /[㐀-鿿]/;
  const MONTHS = {jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12};
  const DISC_ZH = {all: "不限学科", cs: "计算机", ai: "人工智能", math: "数学", physics: "物理", chem: "化学与材料", bio: "生物",
    eco: "生态与进化", neuro: "神经科学", geo: "地球与环境", engineering: "工程", social: "社会科学", humanities: "人文",
    econ: "经济", business: "商科", med: "医学与健康"};
  const COVERAGE_ZH = {full: "全奖（学费＋生活费）", salary: "带薪岗位", partial: "半奖 / 部分资助", tuition: "仅免学费",
    stipend: "仅生活费", varies: "视项目而定", none: "不提供资助", unknown: "资助官网未写明", "": "资助官网未写明"};
  const ELIG_ZH = {yes: "中国学生可申", partial: "部分渠道可申", check: "资格待核实（申请前请自己确认）", "": "资格待核实（申请前请自己确认）"};
  const CUR = {"€": "EUR", eur: "EUR", "£": "GBP", gbp: "GBP", "us$": "USD", "$": "USD", usd: "USD", chf: "CHF", sek: "SEK",
    nok: "NOK", dkk: "DKK", "hk$": "HKD", hkd: "HKD", "s$": "SGD", sgd: "SGD", "a$": "AUD", aud: "AUD", "c$": "CAD", cad: "CAD",
    nzd: "NZD", jpy: "JPY", "¥": "JPY"};
  const AMOUNT = /(US\$|HK\$|S\$|A\$|C\$|€|£|\$|¥|EUR|GBP|USD|CHF|SEK|NOK|DKK|HKD|SGD|AUD|CAD|NZD|JPY)\s?(\d[\d.,  ]*\d|\d)|(\d[\d.,  ]*\d|\d)\s?(€|EUR|CHF|SEK|NOK|DKK|kr)/i;
  const has = (a, v) => (a || []).indexOf(v) >= 0;
  const esc = s => s.replace(/([.*+?^${}()|[\]\\\-])/g, "\\$1");

  function compileTerm(t) {
    if (CJK.test(t)) return ["sub", t];
    const prefix = t.endsWith("*"), core = t.replace(/\*+$/, "");
    const cs = core === core.toUpperCase() && core !== core.toLowerCase() && core.replace(/ /g, "").length <= 4;
    const body = core.split(/\s+/).filter(Boolean).map(esc).join("[\\s\\-]+");
    return ["re", new RegExp("(?<![A-Za-z0-9])" + body + (prefix ? "" : "(?![A-Za-z0-9])"), cs ? "" : "i")];
  }
  function find(term, text) {
    if (term[0] === "sub") return text.indexOf(term[1]);
    const m = term[1].exec(text);
    return m ? m.index : -1;
  }
  function span(term, text) {
    if (term[0] === "sub") { const i = text.indexOf(term[1]); return i >= 0 ? [i, i + term[1].length] : null; }
    const m = term[1].exec(text);
    return m ? [m.index, m.index + m[0].length] : null;
  }
  // 日期一律当 UTC 处理，按天数比较
  function ymd(s) {
    const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?$/.exec(String(s == null ? "" : s));
    return m ? Date.UTC(+m[1], +m[2] - 1, +(m[3] || 1)) / 864e5 : null;
  }
  const isoMonth = d => new Date(d * 864e5).toISOString().slice(0, 7);
  function parseStart(rq) {
    const m = /开始时间：(\d{1,2})\.? ([A-Za-z]{3})[a-z]* (\d{4})/.exec(rq || "");
    if (!m || !MONTHS[m[2].toLowerCase()]) return null;
    return Date.UTC(+m[3], MONTHS[m[2].toLowerCase()] - 1, +m[1]) / 864e5;
  }
  function parseNumber(s) {
    s = s.replace(/ /g, "").replace(/ /g, "");
    if (s.includes(",") && s.includes(".")) {
      const dec = s.lastIndexOf(",") > s.lastIndexOf(".") ? "," : ".";
      s = s.split(dec === "," ? "." : ",").join("").replace(/,/g, ".");
    } else if (s.includes(",")) {
      s = /,\d{3}$/.test(s) ? s.replace(/,/g, "") : s.replace(/,/g, ".");
    } else if (s.includes(".") && /\.\d{3}$/.test(s)) {
      s = s.replace(/\./g, "");
    }
    const v = Number(s);
    return /^\d+(\.\d+)?$/.test(s) && isFinite(v) ? v : null;
  }
  function monthlyEur(s, R) {
    s = s || "";
    const m = AMOUNT.exec(s);
    if (!m) return null;
    let cur = (m[1] ? m[1] : m[4]).toLowerCase();
    let num = m[1] ? m[2] : m[3];
    if (!m[1]) { const lo = /(\d[\d.,]*)\s?[-–—]\s?$/.exec(s.slice(0, m.index)); if (lo) num = lo[1]; }  // 范围取下限
    if (cur === "kr") cur = "sek";
    const v = parseNumber(num.trim()), code = CUR[cur];
    if (v === null || !code) return null;
    const tail = s.slice(m.index + m[0].length, m.index + m[0].length + 30).toLowerCase();
    const per = /月|month/.test(tail) ? 1 : /年|annum|year|annual|p\.?a\b|pa\b/.test(tail) ? 12 : (v >= 10000 ? 12 : 1);
    const eur = v * R.fx[code] / per;
    return eur >= 300 && eur <= 20000 ? eur : null;
  }

  // 用来匹配关键词的标题与简介：去掉资助方 / 机构名；标题写了“focus on”时只用它后面的方向（简介里多半是系名，不用）
  function matchTexts(x, P) {
    let mtitle = (x.n || "").replace(P.noise, " ");
    let mbody = (x.in || "").replace(P.noise, " ").replace(P.noise_body, " ");
    const fm = P.focus.exec(mtitle);
    if (fm) { mtitle = mtitle.slice(fm.index + fm[0].length); mbody = ""; }
    return [mtitle, mbody];
  }
  const kwHitsText = (kw, text) => !!text && ((kw.lit && find(kw.lit[0], text) >= 0)
    || kw.concepts.some(([, concept]) => concept.some(t => find(t[0], text) >= 0)));
  // 关键词越常见，每次命中的分越低
  function specificity(df, W) {
    const [a, b, lo, hi] = W.spec;
    const f = a - b * Math.log10(Math.max(df, 1));
    return Math.floor(Math.min(hi, Math.max(lo, f)) * 100 + 0.5) / 100;
  }

  function prepare(profile, R) {
    profile = profile || {};
    const groups = R.groups.map(g => ({d: g.d, m: !!g.m, t: g.t.map(t => t.replace(/^=/, "")), syn: g.t.map(t => compileTerm(t.replace(/^=/, ""))),
      all: g.t.concat(g.n).filter(t => t[0] !== "=").map(t => [compileTerm(t), t.replace(/\*+$/, "").toLowerCase()])}));
    const stop = new RegExp(R.stop, "gi");
    const research = profile.research || {};
    const seen = {}, kws = [];
    (research.keywords || []).forEach(k => {
      k = String(k).trim();
      if (k && !seen[k.toLowerCase()]) { seen[k.toLowerCase()] = 1; kws.push(k); }
    });
    const disc = (research.disciplines || []).filter(Boolean);
    const keywords = kws.map(k => {
      const spans = [];
      groups.forEach((g, gi) => g.syn.forEach(c => { const sp = span(c, k); if (sp) spans.push([sp[0], sp[1], gi]); }));
      // 只保留最长的命中：“神经网络”不应同时算作“神经”
      const kept = [], cover = new Array(k.length).fill(false);
      spans.forEach(a => {
        if (spans.some(b => b[2] !== a[2] && b[0] <= a[0] && a[1] <= b[1] && (b[1] - b[0]) > (a[1] - a[0]))) return;
        for (let i = a[0]; i < a[1]; i++) cover[i] = true;
        if (!has(kept, a[2])) kept.push(a[2]);
      });
      const rest = Array.from(k).map((ch, i) => cover[i] ? " " : ch).join("").replace(stop, " ").trim();
      const own = !kept.some(gi => groups[gi].t.some(t => k.toLowerCase() === t.replace(/\*+$/, "").toLowerCase()));
      kept.forEach(gi => groups[gi].d.forEach(d => { if (!has(disc, d)) disc.push(d); }));
      if (!kept.length) Object.keys(R.disc_words).forEach(d => {
        if (new RegExp(R.disc_words[d], "i").test(k) && !has(disc, d)) disc.push(d);
      });
      return {k, lit: own ? [compileTerm(k), k.toLowerCase()] : null, concepts: kept.map(gi => ["g" + gi, groups[gi].all]),
        need_lit: !!rest || !kept.length, method: kept.length > 0 && kept.every(gi => groups[gi].m)};
    });
    const target = profile.target || {}, start = ymd(target.start);
    let deg = 0;
    (profile.education || []).forEach(e => {
      const lv = R.levels[String(e.degree || "").toLowerCase()] || 0, end = ymd(e.end);
      const done = (e.status || "completed") === "completed" || (start !== null && end !== null && end <= start);
      if (done && lv > deg) deg = lv;
    });
    const langs = profile.languages || {}, countries = profile.countries || {}, funding = profile.funding || {};
    const prep = (profile.deadline || {}).min_prep_days;
    const g = String(langs.german || "").toUpperCase().replace("NATIVE", "native");
    return {
      keywords, disc, deg, levels: target.levels && target.levels.length ? target.levels : ["phd"], start,
      ielts: langs.ielts == null ? null : langs.ielts, toefl: langs.toefl == null ? null : langs.toefl,
      german: R.cefr[g] || 0,
      accept: countries.accept || [], prefer: countries.prefer || [], exclude: countries.exclude || [],
      min_cov: funding.min_coverage || "any", min_eur: funding.min_monthly_eur,
      prep: parseInt(prep == null ? 14 : prep, 10),
      cn: String(profile.nationality || "CN").toUpperCase() === "CN", cn_only: !!(profile.eligibility || {}).cn_only,
      sensitive: !!profile.sensitive_field, R, kwf: {},
      restrict: new RegExp(R.restrict, "i"), german_re: new RegExp(R.german), local_re: new RegExp(R.local_lang, "i"),
      noise: new RegExp(R.noise, "gi"), noise_body: new RegExp(R.noise_body, "g"), focus: new RegExp(R.focus, "i"),
      local_ok: (langs.other || []).some(o => has(R.local_langs, String((o && typeof o === "object" ? o.lang : o) || "").trim().toLowerCase())),
    };
  }

  function assess(x, P, today) {
    const R = P.R, W = R.weights, o = x.o;
    if (!o) return null;
    const dl = o.dl || x.dl || "";
    const dd = String(dl).length === 10 ? ymd(dl) : null;
    if (dd !== null && dd < today) return null;
    const nDays = dd !== null ? dd - today : null;
    const title = x.n || "", body = x.in || "", rq = x.rq || "";  // 不用机构名：“National Institute of Education”不代表教育学
    const regions = x.r || [], levels = x.l && x.l.length ? x.l : ["phd"], xd = x.d || [];
    const c = x.c || "", e = x.e || "", out = [];
    const [mtitle, mbody] = matchTexts(x, P);
    let m;

    if (P.cn && e === "no") out.push("中国学生不可申请");
    if (P.cn && P.cn_only && e !== "yes" && e !== "partial") out.push("资格待核实（你选了只看中国学生可申）");
    if (P.restrict.test(title + " " + rq)) out.push("公告写明限本国 / 本土学生");
    if (!levels.some(lv => has(P.levels, lv))) out.push("层次不符（岗位是" + levels.map(lv => lv === "postdoc" ? "博后" : "博士").join("、") + "）");
    else if (!has(levels, "phd") && P.deg < 3) out.push("博后岗位要求博士学位");
    m = /学位要求：([^；]*)/.exec(rq);
    if (m && has(levels, "phd") && P.deg < 2 && /Master|Magister|Diplom/.test(m[1]) && m[1].indexOf("Bachelor") < 0) out.push("要求硕士学位");
    m = /IELTS[^0-9；]{0,30}(\d(?:\.\d)?)/.exec(rq);
    if (m && P.ielts !== null && +P.ielts < +m[1]) out.push(`雅思要求 ${m[1]}（你 ${P.ielts}）`);
    m = /TOEFL[^0-9；]{0,30}(\d{2,3})/.exec(rq);
    if (m && P.toefl !== null && P.ielts === null && +P.toefl < +m[1]) out.push(`托福要求 ${m[1]}（你 ${P.toefl}）`);
    if (P.german_re.test(title + " " + rq) && P.german < R.cefr.B2) out.push("要求德语");
    if (P.local_re.test(title) && !P.local_ok) out.push("公告用挪威语 / 瑞典语 / 丹麦语 / 荷兰语发布");
    if (nDays !== null && nDays < P.prep) out.push(`截止太近（还有 ${nDays} 天，少于你设的准备期 ${P.prep} 天）`);
    const js = parseStart(rq);
    if (js !== null && P.start !== null && js < P.start - 31) out.push(`开始时间 ${isoMonth(js)} 早于你能入学的 ${isoMonth(P.start)}`);
    const ok = R.coverage_ok[P.min_cov];
    if (ok && !has(ok, c)) out.push(P.min_cov === "confirmed" ? "资助未写明全奖 / 带薪" : `资助低于你的底线（${COVERAGE_ZH[c] || c}）`);
    if (P.min_eur) {
      const eur = monthlyEur(x.s || "", R);
      if (eur !== null && eur < +P.min_eur) out.push(`金额约 €${Math.floor(eur + 0.5).toLocaleString("en")}/月，低于你的底线 €${P.min_eur}`);
    }
    if (regions.some(r => has(P.exclude, r))) out.push("在你排除的国家");
    else if (P.accept.length && regions.length && !has(regions, "GLOBAL") && !regions.some(r => has(P.accept, r))
      && !(has(regions, "EU") && P.accept.some(a => has(R.eu, a)))) out.push("不在你可接受的国家");

    const hits = [], credited = {};
    const strict = xd.length > 0 && !has(xd, "all") && xd.some(d => has(P.disc, d));  // 学科明确对得上
    const clash = P.disc.length > 0 && xd.length > 0 && !has(xd, "all") && !strict;  // 学科明确对不上
    const near = P.disc.concat(...P.disc.map(d => R.siblings[d] || []));
    const elsewhere = xd.some(d => d !== "all" && !has(near, d));  // 岗位还属于你方向以外的学科
    [["标题", mtitle, W.title], ["简介", mbody, W.body]].forEach(([where, text, w]) => {
      if (!text) return;
      P.keywords.forEach(kw => {
        if (hits.some(h => h[1] === kw.k)) return;
        // got：命中的记分标签（组号 + 实际命中的词），同一组或同一个词只记一次分
        let got = kw.lit && find(kw.lit[0], text) >= 0 ? ["k:" + kw.lit[1], kw.lit[1]] : [];
        let full = got.length > 0;
        if (!full) {
          let n = 0;
          kw.concepts.forEach(([tag, concept]) => {
            const t = concept.find(ct => find(ct[0], text) >= 0);
            if (t) { got.push(tag, t[1]); n++; }
          });
          full = n > 0 && n === kw.concepts.length && !kw.need_lit;
        }
        if (!got.length || got.some(t => credited[t])) return;
        // 学科对不上的命中多半是字面巧合；弱命中（只命中一部分、只在简介里、词表外的单个词）要求学科明确对得上
        const weak = !full || where === "简介" || (!kw.concepts.length && kw.k.trim().indexOf(" ") < 0 && !CJK.test(kw.k));
        if (clash || (weak && P.disc.length && !strict && !has(xd, "all"))) return;
        got.forEach(t => { credited[t] = 1; });
        const applied = kw.method && elsewhere && P.disc.length > 0;
        const note = (full ? "" : "·部分") + (applied ? "·用于其他学科" : "");
        hits.push([w * (full ? 1 : W.partial) * (applied ? W.applied : 1) * (kw.k in P.kwf ? P.kwf[kw.k] : 1), kw.k, where + note]);
      });
    });
    hits.sort((a, b) => b[0] - a[0]);
    let kwScore = 0;
    hits.slice(0, 3).forEach((h, i) => { kwScore += W.kw[i] * h[0]; });
    kwScore = Math.min(W.kw_cap, kwScore);
    const overlap = xd.filter(d => d !== "all" && has(P.disc, d));
    const dScore = overlap.length ? W.disc * overlap.length / xd.filter(d => d !== "all").length : (has(xd, "all") && hits.length ? W.all_disc : 0);
    const research = kwScore + dScore;

    const funding = c in W.funding ? W.funding[c] : W.funding[""];
    const WD = W.deadline;
    let dscore;
    if (dl === "rolling") dscore = WD.rolling;
    else if (o.st === "upcoming") dscore = WD.upcoming;
    else if (nDays === null) dscore = WD.unknown;
    else dscore = nDays < 21 ? WD.close : nDays <= 75 ? WD.best : nDays <= 150 ? WD.far : WD.very_far;
    const region = P.prefer.length ? (regions.some(r => has(P.prefer, r)) ? W.region_prefer : W.region_other) : W.region_ok;
    const elig = P.cn ? (e in W.elig ? W.elig[e] : W.elig[""]) : W.elig[""];
    let penalty = 0;
    const flags = [];
    if (has(x.fl, "security-screening")) {
      penalty += P.sensitive ? W.screen_sensitive : W.screen;
      flags.push("⚠ 公告提到安全审查" + (P.sensitive ? "，你的方向较敏感" : ""));
    }
    if (P.sensitive && has(regions, "UK") && P.disc.some(d => has(R.atas_disc, d)) && xd.some(d => has(R.atas_disc, d))) {
      penalty += W.atas;
      flags.push("⚠ 英国理工科敏感方向可能需要 ATAS 审查");
    }
    const total = research + funding + dscore + region + elig + penalty;
    const score = Math.max(0, Math.min(100, Math.floor(total + 0.5)));

    const names = overlap.map(d => DISC_ZH[d] || d);
    let r1;
    if (hits.length) r1 = "研究匹配：命中" + hits.map(h => `「${h[1]}」（${h[2]}）`).join("、") + (names.length ? `；学科：${names.join("、")}` : "");
    else if (names.length) r1 = `研究匹配：学科相同（${names.join("、")}），标题与简介没有直接出现你的关键词`;
    else r1 = "研究匹配：未命中你的关键词与学科";
    const r2 = "资助与资格：" + [c in COVERAGE_ZH ? COVERAGE_ZH[c] : c, x.s && x.s.length <= 60 ? x.s : null,
      P.cn ? (ELIG_ZH[e] || ELIG_ZH[""]) : null].filter(Boolean).join(" · ");
    let when;
    if (dl === "rolling") when = "滚动招生";
    else if (o.st === "upcoming") when = "即将开放" + (o.op ? `（${o.op}）` : "");
    else if (dd !== null) when = `${+dl.slice(5, 7)}/${+dl.slice(8, 10)} 截止（还有 ${nDays} 天）`;
    else when = "截止日期官网未写明";
    let where = regions.join("、") || "地区未写明";
    if (P.prefer.length && regions.some(r => has(P.prefer, r))) where += "（你的偏好）";
    const r3 = "时间与地区：" + [when, where].concat(flags).join(" · ");
    return {id: x.id, score, parts: {research, funding, deadline: dscore, region, elig, penalty},
      hits: hits.map(h => h[1]), reasons: [r1, r2, r3], excluded: out, relevant: hits.length > 0};
  }

  function rank(rows, profile, R, todayIso) {
    const P = prepare(profile, R), today = ymd(todayIso);
    // 先数每个关键词在现在可申请的机会里命中多少条，用来给常见词降权
    const df = {};
    P.keywords.forEach(kw => { df[kw.k] = 0; });
    rows.forEach(x => {
      const o = x.o, dl = (o || {}).dl || x.dl || "";
      if (!o || (String(dl).length === 10 && ymd(dl) < today)) return;
      const [t, b] = matchTexts(x, P);
      P.keywords.forEach(kw => { if (kwHitsText(kw, t) || kwHitsText(kw, b)) df[kw.k]++; });
    });
    P.keywords.forEach(kw => { P.kwf[kw.k] = specificity(df[kw.k], R.weights); });
    const ranked = [], related = [], excluded = [], byId = {};
    let unrelated = 0, considered = 0;
    rows.forEach(x => {
      byId[x.id] = x;
      const a = assess(x, P, today);
      if (!a) return;
      considered++;
      if (a.excluded.length) excluded.push(a);
      else if (!a.relevant) { if (a.parts.research > 0) related.push(a); else unrelated++; }
      else ranked.push(a);
    });
    const dlKey = a => { const x = byId[a.id], d = (x.o || {}).dl || x.dl || ""; return d.length === 10 ? d : "9999"; };
    const cmp = (p, q) => p < q ? -1 : p > q ? 1 : 0;
    const byScore = (a, b) => (b.score - a.score) || cmp(dlKey(a), dlKey(b)) || cmp(a.id, b.id);
    ranked.sort(byScore);
    related.sort(byScore);
    excluded.sort((a, b) => (b.parts.research - a.parts.research) || cmp(a.id, b.id));
    return {ranked, related, excluded, unrelated, considered, disc: P.disc};
  }

  const api = {prepare, assess, rank, monthlyEur, DISC_ZH};
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PhDRank = api;
})(this);
