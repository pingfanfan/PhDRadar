// 模糊搜索：中英同义词扩展 + 英文拼写容错（编辑距离）+ 中文多打或少打首尾一个字也算。
// 每个词都要命中（同义词任一命中即可）；全站词表只建一次，拼写容错在词表上算，不逐条算。
const SYN = [
  ["气候", "climate", "klima"], ["大气", "atmospher"], ["气象", "meteorolog"], ["空气污染", "air pollution"],
  ["人工智能", "ai", "artificial intelligence", "machine learning", "机器学习"], ["深度学习", "deep learning"],
  ["神经", "neuro"], ["脑", "brain"], ["认知", "cogniti"], ["精神", "psychiatr"], ["记忆", "memory"],
  ["生物", "biolog"], ["基因", "genom", "genetic"], ["细胞", "cell"], ["分子", "molecular"], ["蛋白", "protein"],
  ["物理", "physic"], ["天文", "天体", "astro"], ["量子", "quantum"],
  ["化学", "chemi"], ["催化", "catal"], ["材料", "material"],
  ["医学", "medic"], ["临床", "clinical"], ["健康", "health"], ["癌", "cancer", "oncolog"],
  ["政治", "politic"], ["治理", "governance"], ["社会", "social", "sociolog"], ["经济", "econom"], ["金融", "financ"],
  ["计算机", "computer science", "computing"], ["算法", "algorithm"], ["软件", "software"],
  ["数学", "mathemat"], ["统计", "statistic"], ["工程", "engineering"], ["机器人", "robot"], ["能源", "energy"],
  ["海洋", "ocean", "marine"], ["环境", "environment"], ["生态", "ecolog"],
  ["语言学", "linguist"], ["历史", "histor"], ["哲学", "philosoph"], ["心理", "psycholog"],
  ["苏黎世", "zurich"], ["慕尼黑", "munich"], ["阿姆斯特丹", "amsterdam"], ["哥本哈根", "copenhagen"],
  ["伦敦", "london"], ["剑桥", "cambridge"], ["牛津", "oxford"], ["新加坡", "singapore"], ["香港", "hong kong"],
  ["博后", "postdoc", "post-doc", "postdoctoral"], ["博士", "phd", "doctoral", "doktorand"],
  ["msca", "marie curie", "玛丽·居里", "玛丽居里"],
  ["英国", "united kingdom", "britain", "uk"], ["德国", "germany"], ["法国", "france"], ["荷兰", "netherlands"],
  ["丹麦", "denmark"], ["瑞典", "sweden"], ["挪威", "norway"], ["芬兰", "finland"], ["瑞士", "switzerland"],
  ["美国", "united states", "usa"], ["加拿大", "canada"], ["澳大利亚", "australia"], ["日本", "japan"],
  ["奥地利", "austria"], ["比利时", "belgium"], ["西班牙", "spain"], ["意大利", "italy"], ["爱尔兰", "ireland"],
]

export const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
const cjk = (s: string) => /[一-鿿]/.test(s)
export const words = (hay: string) => hay.split(/[^a-z0-9一-鿿]+/).filter((w) => w.length > 1)

function lev(a: string, b: string, cap: number) {
  if (Math.abs(a.length - b.length) > cap) return cap + 1
  let prev = Array.from({ length: b.length + 1 }, (_, j) => j)
  for (let i = 1; i <= a.length; i++) {
    const cur = [i]
    let best = i
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1))
      best = Math.min(best, cur[j])
    }
    if (best > cap) return cap + 1
    prev = cur
  }
  return prev[b.length]
}

function expand(tok: string) {
  const alts = new Set([tok])
  for (const grp of SYN) {
    const hit = grp.some((g) => g === tok || (cjk(tok) ? tok.length >= 2 && (g.includes(tok) || tok.includes(g)) : g.length >= 4 && tok.length >= 4 && (g.startsWith(tok) || tok.startsWith(g))))
    if (hit) grp.forEach((g) => alts.add(g))
  }
  return [...alts]
}

// 返回判定函数；没有输入时返回 null（不过滤）
export function matcher(q: string, vocab: string[]): ((hay: string, ws: Set<string>) => boolean) | null {
  const toks = norm(q).split(/[\s,，、;；]+/).filter(Boolean)
  if (!toks.length) return null
  const plans = toks.map((t) => expand(t).map((a) => {
    if (cjk(a)) return (hay: string) => {
      if (hay.includes(a)) return true
      return a.length >= 3 && (hay.includes(a.slice(0, -1)) || hay.includes(a.slice(1)))
    }
    if (a.length <= 3) return (_: string, ws: Set<string>) => ws.has(a)
    if (a.includes(" ")) return (hay: string) => hay.includes(a)
    // 词表里与它拼写相近的词：前缀相同，或编辑距离 1（7 个字母以上允许 2）
    const cap = a.length >= 7 ? 2 : 1
    const near = new Set(vocab.filter((w) => w.startsWith(a) || (w.length >= 4 && lev(a, w.slice(0, a.length + cap), cap) <= cap)))
    return (hay: string, ws: Set<string>) => hay.includes(a) || [...ws].some((w) => near.has(w))
  }))
  return (hay, ws) => plans.every((alts) => alts.some((f) => f(hay, ws)))
}
