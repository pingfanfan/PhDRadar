// 首页数据（assets/catalog.json，由 scripts/build_site.py 生成）与通用的日期、文案工具。
export type AfKey = "dg" | "lg" | "sd" | "du" | "dc" | "av" | "sv" | "na"

export interface Row {
  id: string
  n: string
  u: string
  org?: string
  r?: string[]
  d?: string[]
  l?: string[]
  c?: string
  s?: string
  dl?: string
  st?: string
  e?: string
  v?: boolean
  dn?: string
  rq?: string
  pq?: string
  vd?: string
  in?: string
  via?: string
  af?: Partial<Record<AfKey, [string, string]>>
  lt?: string
  fl?: string[]
  al?: string[]
  o?: { st?: string; dl?: string; op?: string; q?: string; ck?: string }
  _hay: string
}

export interface Labels {
  region: Record<string, string>
  discipline: Record<string, string>
  level: Record<string, string>
  coverage: Record<string, string>
  status: Record<string, [string, string]>
  cn: Record<string, [string, string]>
  deadline: Record<string, string>
}

export const AF_LABELS: [AfKey, string][] = [
  ["dg", "学位要求"], ["lg", "语言要求"], ["sd", "开始时间"], ["du", "资助年限"],
  ["dc", "材料清单"], ["av", "申请方式"], ["sv", "导师"], ["na", "身份限制"],
]

export const TODAY = new Date(new Date().toDateString())
export const iso = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`
export const isDate = (d?: string) => /^\d{4}-\d{2}-\d{2}$/.test(d || "")
export const days = (d: string) => Math.round((new Date(d + "T00:00:00").getTime() - TODAY.getTime()) / 864e5)
export const md = (d: string) => `${+d.slice(5, 7)}月${+d.slice(8)}日`

export const isNow = (x: Row) => !!x.o && (!isDate(x.o.dl) || days(x.o.dl!) >= 0)
export const dlOf = (x: Row) => (isNow(x) && x.o!.dl ? x.o!.dl : x.dl)
export const screened = (x: Row) => (x.fl || []).includes("security-screening")

export async function loadData(): Promise<{ rows: Row[]; labels: Labels }> {
  const [rows, labels] = await Promise.all([
    fetch("assets/catalog.json").then((r) => r.json()) as Promise<Omit<Row, "_hay">[]>,
    fetch("assets/labels.json").then((r) => r.json()) as Promise<Labels>,
  ])
  const region = (x: Omit<Row, "_hay">) => (x.r || []).map((r) => labels.region[r] || r).join(" ")
  return {
    labels,
    rows: rows.map((x) => ({
      ...x,
      _hay: [x.n, x.org, x.in, region(x), (x.d || []).map((d) => labels.discipline[d] || d).join(" "),
        x.s, x.rq, x.lt, x.af?.dg?.[0]].join(" ").toLowerCase(),
    })),
  }
}

// 机构标识：中文取首字，英文取两个词的首字母
export function monogram(x: Row) {
  const s = (x.org || x.n).replace(/[（(].*$/, "").trim()
  if (/^[一-鿿]/.test(s)) return s[0]
  const w = s.replace(/^(the|university of|universit[äe]t|universidad)\s+/i, "").match(/[A-Za-z]+/g) || [s]
  return (w.length > 1 ? w[0][0] + w[1][0] : w[0].slice(0, 2)).toUpperCase()
}

// 卡片上只放简短金额（如 €47,000–€64,000/年）；官网原文放在详情里
const CUR = String.raw`(?:[€£$¥]|CHF|EUR|GBP|USD|SEK|NOK|DKK|ISK|PLN|CZK|AUD|CAD|NZD|HKD|SGD|JPY|KRW|A\$|NZ\$|HK\$|S\$|C\$|RMB|kr)`
const NUM = String.raw`\d[\d,.]*(?:\s?[kK])?`
const AMT = new RegExp(String.raw`${CUR}\s?${NUM}(?:\s?(?:–|-|—|to)\s?${CUR}?\s?${NUM})?`)
export function shortPay(x: Row, labels: Labels) {
  const s = String(x.s || "").trim()
  const cov = x.c && x.c !== "unknown" ? labels.coverage[x.c] : ""
  if (!s) return cov
  if (s.length <= 22) return s
  const m = s.match(AMT)
  if (!m) return cov
  const per = /per (year|annum)|\/\s?(year|yr|annum)|p\.\s?a\.|annual|yearly|每年|\/年|年薪/i.test(s) ? "/年"
    : /per month|\/\s?month|monthly|每月|\/月|月薪/i.test(s) ? "/月" : ""
  return m[0].replace(/\s+/g, " ").trim() + per
}

export type Tone = "urgent" | "soon" | "rolling" | ""
export function due(x: Row, labels: Labels): [string, Tone] {
  const d = dlOf(x)
  if (isNow(x) && x.o!.st === "upcoming") return [x.o!.op ? `${x.o!.op} 开放申请` : "即将开放", "soon"]
  if (d === "rolling") return ["滚动招生 · 随时可投", "rolling"]
  if (isDate(d)) {
    const n = days(d!)
    if (n < 0) return [`${d} 已截止`, ""]
    return [`${d!.slice(5).replace("-", "/")} 截止 · ${n === 0 ? "今天截止" : `还有 ${n} 天`}`, n <= 7 ? "urgent" : n <= 30 ? "soon" : ""]
  }
  return [d ? labels.deadline[d] || d : "截止日期官网未写明", ""]
}

export function group(x: Row) {
  const d = dlOf(x)
  if (d === "rolling") return "滚动招生"
  if (!isDate(d)) return "截止日期官网未写明"
  const n = days(d!), wkEnd = (7 - TODAY.getDay()) % 7
  if (n < 0) return "已截止"
  if (n <= wkEnd) return "本周截止"
  if (n <= wkEnd + 7) return "下周截止"
  return `${+d!.slice(0, 4) === TODAY.getFullYear() ? "" : `${d!.slice(0, 4)} 年 `}${+d!.slice(5, 7)} 月截止`
}

// .ics 日历：截止前 14 / 7 / 1 天提醒（RFC 5545 折行，不拆多字节字符）
const icsText = (s: string) => s.replace(/[\\;,]/g, (c) => "\\" + c).replace(/\n/g, "\\n")
function icsFold(line: string) {
  const enc = new TextEncoder(), out: string[] = []
  let cur = "", n = 0
  for (const ch of line) {
    const b = enc.encode(ch).length
    if (n + b > (out.length ? 74 : 75)) { out.push(cur); cur = ""; n = 0 }
    cur += ch; n += b
  }
  out.push(cur)
  return out.join("\r\n ")
}
export function icsCalendar(list: Row[]) {
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "")
  const alarm = (t: string, m: string) => ["BEGIN:VALARM", `TRIGGER:${t}`, "ACTION:DISPLAY", `DESCRIPTION:${icsText(m)}`, "END:VALARM"]
  const events = list.flatMap((x) => {
    const dl = dlOf(x)!, end = new Date(dl + "T00:00:00")
    end.setDate(end.getDate() + 1)
    return ["BEGIN:VEVENT", `UID:${icsText(x.id)}@phdradar`, `DTSTAMP:${stamp}`, `DTSTART;VALUE=DATE:${dl.replace(/-/g, "")}`,
      `DTEND;VALUE=DATE:${iso(end).replace(/-/g, "")}`, `SUMMARY:${icsText("截止：" + x.n)}`,
      `DESCRIPTION:${icsText([x.org, "申请链接：" + x.u, "截止时间以官网为准，注意时区。"].filter(Boolean).join("\n"))}`,
      `URL:${x.u}`, ...alarm("-P14D", "还有 14 天截止：" + x.n), ...alarm("-P7D", "还有 7 天截止：" + x.n),
      ...alarm("-P1D", "明天截止：" + x.n), "END:VEVENT"]
  })
  return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PhDRadar//CN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", ...events, "END:VCALENDAR"]
    .map(icsFold).join("\r\n") + "\r\n"
}

export function download(name: string, body: string, type: string) {
  const a = document.createElement("a")
  a.href = URL.createObjectURL(new Blob([body], { type }))
  a.download = name
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(a.href), 1000)
}
