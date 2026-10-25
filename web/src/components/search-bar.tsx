import { useMemo } from "react"
import { CalendarClock, MapPin, Search, ShieldCheck, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import { days, dlOf, isDate, isNow, iso, md, TODAY } from "@/lib/data"
import { useData, useFiltered } from "@/lib/select"
import { useApp, type Flag } from "@/store"

const ALL = "__all"
const FLAGS: [Flag, string][] = [["cn", "中国学生可申"], ["full", "全奖 / 带薪"], ["soon", "30 天内截止"], ["phd", "博士"], ["pd", "博后"]]

function CountSelect({ value, onChange, placeholder, counts, names, icon, className }: {
  value: string; onChange: (v: string) => void; placeholder: string
  counts: Record<string, number>; names: Record<string, string>; icon?: React.ReactNode; className?: string
}) {
  const opts = Object.entries(counts).sort((a, b) => b[1] - a[1])
  return (
    <Select value={value || ALL} onValueChange={(v) => onChange(v === ALL ? "" : v)}>
      <SelectTrigger className={cn("min-w-36", className)} aria-label={placeholder}>{icon}<SelectValue placeholder={placeholder} /></SelectTrigger>
      <SelectContent className="max-h-80">
        <SelectItem value={ALL}>{placeholder}</SelectItem>
        {opts.map(([k, n]) => <SelectItem key={k} value={k}>{names[k] || k}<span className="ml-1 font-mono text-xs text-muted-foreground">{n}</span></SelectItem>)}
      </SelectContent>
    </Select>
  )
}

export function SearchBar() {
  const { q, region, disc, flags, set } = useApp()
  const { rows, labels } = useData()
  const nNow = rows.filter(isNow).length
  const [rc, dc] = useMemo(() => {
    const rc: Record<string, number> = {}, dc: Record<string, number> = {}
    rows.filter((x) => x.v).forEach((x) => {
      (x.r || []).forEach((r) => (rc[r] = (rc[r] || 0) + 1));
      (x.d || []).forEach((d) => d !== "all" && (dc[d] = (dc[d] || 0) + 1))
    })
    return [rc, dc]
  }, [rows])
  if (!labels) return null

  return (
    <section className="mx-auto flex max-w-7xl flex-col gap-3 px-4 pt-6 pb-3">
      <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1.5">
        <h1 className="text-xl font-semibold tracking-tight text-balance md:text-2xl">
          <span className="font-mono text-primary">{nNow ? nNow.toLocaleString() : "…"}</span> 个海外带奖博士 / 博后机会，现在就能申请
        </h1>
        <p className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1.5"><ShieldCheck className="size-3.5 text-primary" />每条都核对过官网原句</span>
          <span className="inline-flex items-center gap-1.5"><CalendarClock className="size-3.5 text-primary" />截止后自动下架</span>
        </p>
      </div>
      <div className="flex flex-col gap-2 lg:flex-row lg:items-center">
        <InputGroup className="h-9 bg-background lg:max-w-sm lg:flex-1">
          <InputGroupAddon><Search /></InputGroupAddon>
          <InputGroupInput value={q} onChange={(e) => set({ q: e.target.value })} placeholder="学校、项目、学科，如：神经、机器学习" aria-label="关键词" />
          {q && <InputGroupAddon align="inline-end"><Button variant="ghost" size="icon-xs" aria-label="清空" onClick={() => set({ q: "" })}><X /></Button></InputGroupAddon>}
        </InputGroup>
        <div className="flex flex-wrap items-center gap-2">
          <CountSelect value={region} onChange={(v) => set({ region: v })} placeholder="全部地区" counts={rc} names={labels.region} icon={<MapPin />} className="h-9! bg-background" />
          <CountSelect value={disc} onChange={(v) => set({ disc: v })} placeholder="全部学科" counts={dc} names={labels.discipline} className="h-9! bg-background" />
          <ToggleGroup type="multiple" variant="outline" size="sm" spacing={2} value={flags} onValueChange={(v) => set({ flags: v as Flag[] })} className="flex-wrap">
            {FLAGS.map(([k, t]) => <ToggleGroupItem key={k} value={k} className="h-9 bg-background px-3 text-[13px] font-normal data-[state=on]:border-primary/50 data-[state=on]:bg-primary/10 data-[state=on]:text-primary">{t}</ToggleGroupItem>)}
          </ToggleGroup>
        </div>
      </div>
    </section>
  )
}

// 未来 35 天的截止：每天一根柱，越高当天截止越多；点一根只看这天截止的
export function DeadlineStrip() {
  const list = useFiltered(true)
  const { day, set } = useApp()
  const { counts, total, max, peak } = useMemo(() => {
    const counts: Record<string, number> = {}
    list.forEach((x) => { const d = dlOf(x); if (isDate(d) && days(d!) >= 0 && days(d!) < 35) counts[d!] = (counts[d!] || 0) + 1 })
    const vals = Object.values(counts)
    const peak = Object.entries(counts).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1))[0]
    return { counts, total: vals.reduce((a, b) => a + b, 0), max: Math.max(1, ...vals), peak }
  }, [list])
  const WK = "日一二三四五六"
  const cells = Array.from({ length: 35 }, (_, k) => { const d = new Date(TODAY); d.setDate(TODAY.getDate() + k); return d })

  return (
    <section className="mx-auto max-w-7xl px-4 pb-4">
      <div className="flex flex-col gap-3 rounded-xl border bg-card px-4 py-3 shadow-xs md:flex-row md:items-stretch md:gap-6">
        <div className="flex shrink-0 flex-col justify-between gap-1 md:w-44">
          <span className="text-xs text-muted-foreground">未来 5 周截止</span>
          <span className="font-mono text-2xl font-semibold tracking-tight">{total.toLocaleString()}</span>
          {day ? <Button size="xs" variant="secondary" className="w-fit" onClick={() => set({ day: "" })}>只看 {md(day)} 截止<X /></Button>
            : peak && <span className="text-xs text-muted-foreground">最多：{md(peak[0])} · {peak[1]} 个</span>}
        </div>
        <div className="min-w-0 flex-1 overflow-x-auto">
          <div className="flex h-16 min-w-[440px] items-end gap-[3px]">
            {cells.map((d) => {
              const key = iso(d), n = counts[key] || 0, on = day === key
              return (
                <Tooltip key={key}>
                  <TooltipTrigger asChild>
                    <button onClick={() => set({ day: on ? "" : key })} aria-pressed={on} aria-label={`${md(key)} ${n} 个截止`} className="group flex h-full flex-1 flex-col justify-end outline-none">
                      <span
                        className={cn("w-full rounded-[3px] transition-colors", !n ? "bg-border" : on ? "bg-primary" : day ? "bg-primary/25 group-hover:bg-primary/50" : "bg-primary/45 group-hover:bg-primary group-focus-visible:bg-primary")}
                        style={{ height: n ? `${Math.max(10, (n / max) * 100)}%` : 3 }}
                      />
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>{md(key)}（周{WK[d.getDay()]}）· {n} 个截止</TooltipContent>
                </Tooltip>
              )
            })}
          </div>
          <div className="mt-1.5 flex min-w-[440px] gap-[3px] font-mono text-[10px] text-muted-foreground">
            {cells.map((d, k) => <span key={k} className="flex-1 overflow-visible whitespace-nowrap">{k === 0 ? "今天" : d.getDay() === 1 && k > 2 ? `${d.getMonth() + 1}/${d.getDate()}` : ""}</span>)}
          </div>
        </div>
      </div>
    </section>
  )
}
