import { useMemo } from "react"
import { X } from "lucide-react"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { cn } from "@/lib/utils"
import { days, dlOf, isDate, isNow } from "@/lib/data"
import { useData } from "@/lib/select"
import { useApp, type Flag } from "@/store"

const ALL = "__all"

function CountSelect({ value, onChange, label, counts, names }: {
  value: string; onChange: (v: string) => void; label: string; counts: Record<string, number>; names: Record<string, string>
}) {
  const opts = Object.entries(counts).sort((a, b) => b[1] - a[1])
  return (
    <Select value={value || ALL} onValueChange={(v) => onChange(v === ALL ? "" : v)}>
      <SelectTrigger size="sm" aria-label={label} className="h-8 gap-1 border-0 bg-transparent px-0 text-[13px] shadow-none dark:bg-transparent">
        <span>{label}</span><SelectValue />
      </SelectTrigger>
      <SelectContent className="max-h-80">
        <SelectItem value={ALL}>全部</SelectItem>
        {opts.map(([k, n]) => <SelectItem key={k} value={k}>{names[k] || k}<span className="ml-1 font-mono text-xs text-muted-foreground">{n}</span></SelectItem>)}
      </SelectContent>
    </Select>
  )
}

export function Hero({ found }: { found: number }) {
  const { q, region, disc, flags, set } = useApp()
  const { rows, labels } = useData()
  const now = useMemo(() => rows.filter(isNow), [rows])
  const stat = useMemo(() => {
    const n = (f: (k: number) => boolean) => now.filter((x) => { const d = dlOf(x); return isDate(d) && f(days(d!)) }).length
    return { today: n((k) => k === 0), week: n((k) => k >= 0 && k <= 6) }
  }, [now])
  const [rc, dc, lc] = useMemo(() => {
    const rc: Record<string, number> = {}, dc: Record<string, number> = {}, lc: Record<string, number> = {}
    now.forEach((x) => {
      (x.r || []).forEach((r) => (rc[r] = (rc[r] || 0) + 1));
      (x.d || []).forEach((d) => d !== "all" && (dc[d] = (dc[d] || 0) + 1));
      (x.l || ["phd"]).forEach((l) => (lc[l] = (lc[l] || 0) + 1))
    })
    return [rc, dc, lc]
  }, [now])
  if (!labels) return null
  const lv = flags.includes("phd") ? "phd" : flags.includes("pd") ? "pd" : ""
  const setLv = (v: "" | "phd" | "pd") => set({ flags: [...flags.filter((f) => f !== "phd" && f !== "pd"), ...(v ? [v] : [])] as Flag[] })
  const toggle = (f: Flag) => set({ flags: flags.includes(f) ? flags.filter((x) => x !== f) : [...flags, f] })
  const levelBtn = (v: "" | "phd" | "pd", text: string) => (
    <button type="button" onClick={() => setLv(v)} aria-pressed={lv === v}
      className={cn("cursor-pointer border-b-2 py-1 text-[13px]", lv === v ? "border-urgent font-bold text-foreground" : "border-transparent text-muted-foreground hover:text-foreground")}>
      {text}
    </button>
  )

  return (
    <section className="mx-auto flex max-w-[1280px] flex-col gap-4 px-4 pt-8 pb-4 sm:px-10">
      <div className="flex flex-wrap items-baseline justify-between gap-x-8 gap-y-2">
        <h1 className="text-2xl font-bold tracking-wide sm:text-[28px]">海外带奖博士 · 博后</h1>
        <p className="font-mono text-[13px] text-muted-foreground">开放 {now.length.toLocaleString()} · 今天截止 {stat.today} · 7 天内截止 {stat.week.toLocaleString()}</p>
      </div>
      <div className="flex flex-col gap-2">
        <label className="flex h-[52px] items-center gap-3.5 rounded border bg-card px-4 focus-within:border-foreground/40">
          <span className="font-mono text-sm font-semibold text-urgent">搜索</span>
          <input
            type="search" value={q} onChange={(e) => set({ q: e.target.value })} placeholder="方向、学校或国家" aria-label="搜索"
            className="min-w-0 flex-1 bg-transparent text-base outline-none placeholder:text-muted-foreground [&::-webkit-search-cancel-button]:hidden"
          />
          {q && <button type="button" onClick={() => set({ q: "" })} aria-label="清空" className="cursor-pointer p-2 text-muted-foreground hover:text-foreground"><X className="size-4" /></button>}
        </label>
        {q.trim() && <p className="text-[13px] text-muted-foreground">找到 <b className="font-mono text-foreground">{found.toLocaleString()}</b> 条</p>}
      </div>
      <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
        <span role="group" aria-label="类型" className="flex gap-4">
          {levelBtn("", "全部")}
          {levelBtn("phd", `博士 ${(lc.phd || 0).toLocaleString()}`)}
          {levelBtn("pd", `博后 ${(lc.postdoc || 0).toLocaleString()}`)}
        </span>
        <span className="hidden h-4 w-px bg-border sm:block" />
        <Label className="cursor-pointer text-[13px] font-normal"><Checkbox checked={flags.includes("cn")} onCheckedChange={() => toggle("cn")} />写明中国学生可申</Label>
        <Label className="cursor-pointer text-[13px] font-normal"><Checkbox checked={flags.includes("amt")} onCheckedChange={() => toggle("amt")} />写明资助金额</Label>
        <CountSelect value={region} onChange={(v) => set({ region: v })} label="地区" counts={rc} names={labels.region} />
        <CountSelect value={disc} onChange={(v) => set({ disc: v })} label="学科" counts={dc} names={labels.discipline} />
      </div>
    </section>
  )
}
