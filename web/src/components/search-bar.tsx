import { useMemo } from "react"
import { CalendarClock, MapPin, Search, ShieldCheck, X } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { Toggle } from "@/components/ui/toggle"
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
    <section className="mx-auto flex max-w-7xl flex-col gap-4 px-4 pt-8 pb-4">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-semibold tracking-tight text-balance md:text-3xl">
          <span className="font-mono text-primary">{nNow ? nNow.toLocaleString() : "…"}</span> 个海外带奖博士 / 博后机会，现在就能申请
        </h1>
        <p className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-muted-foreground">
          <span className="inline-flex items-center gap-1.5"><ShieldCheck className="size-4 text-primary" />每条都核对过官网原句</span>
          <span className="inline-flex items-center gap-1.5"><CalendarClock className="size-4 text-primary" />截止后自动下架</span>
        </p>
      </div>
      <div className="flex max-w-4xl flex-col gap-2 sm:flex-row">
        <InputGroup className="h-11 flex-1 bg-background">
          <InputGroupAddon><Search /></InputGroupAddon>
          <InputGroupInput value={q} onChange={(e) => set({ q: e.target.value })} placeholder="学校、项目、学科，如：神经、机器学习" aria-label="关键词" />
          {q && <InputGroupAddon align="inline-end"><Button variant="ghost" size="icon-xs" aria-label="清空" onClick={() => set({ q: "" })}><X /></Button></InputGroupAddon>}
        </InputGroup>
        <CountSelect value={region} onChange={(v) => set({ region: v })} placeholder="全部地区" counts={rc} names={labels.region} icon={<MapPin />} className="h-11! bg-background sm:w-48" />
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <ToggleGroup type="multiple" variant="outline" size="sm" spacing={2} value={flags} onValueChange={(v) => set({ flags: v as Flag[] })} className="flex-wrap">
          {FLAGS.map(([k, t]) => <ToggleGroupItem key={k} value={k} className="rounded-full px-3 data-[state=on]:border-primary data-[state=on]:bg-primary/10 data-[state=on]:text-primary">{t}</ToggleGroupItem>)}
        </ToggleGroup>
        <CountSelect value={disc} onChange={(v) => set({ disc: v })} placeholder="全部学科" counts={dc} names={labels.discipline} />
      </div>
    </section>
  )
}

// 未来 35 天的截止条：每格一天，颜色越深当天截止越多；点一格只看这天截止的
export function DeadlineStrip() {
  const list = useFiltered(true)
  const { day, set } = useApp()
  const { counts, total, max, peaks } = useMemo(() => {
    const counts: Record<string, number> = {}
    list.forEach((x) => { const d = dlOf(x); if (isDate(d) && days(d!) >= 0 && days(d!) < 35) counts[d!] = (counts[d!] || 0) + 1 })
    const vals = Object.values(counts)
    const peaks = Object.entries(counts).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1)).slice(0, 3)
    return { counts, total: vals.reduce((a, b) => a + b, 0), max: Math.max(1, ...vals), peaks }
  }, [list])
  const WK = "日一二三四五六"
  const level = (n: number) => !n ? "bg-muted text-muted-foreground/60" : n >= max * 0.7 ? "bg-primary text-primary-foreground"
    : n >= max * 0.4 ? "bg-primary/70 text-primary-foreground" : n >= max * 0.15 ? "bg-primary/40 text-foreground" : "bg-primary/15 text-foreground"
  const cells = Array.from({ length: 35 }, (_, k) => { const d = new Date(TODAY); d.setDate(TODAY.getDate() + k); return d })

  return (
    <section className="mx-auto max-w-7xl px-4 pb-4">
      <div className="flex flex-col gap-3 rounded-xl border bg-card p-4">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-sm">
          <h2 className="font-medium">未来 5 周的截止</h2>
          <span className="text-muted-foreground">共 <b className="font-mono text-foreground">{total}</b> 个</span>
          <span className="hidden items-center gap-1.5 sm:flex">
            {peaks.map(([d, n]) => (
              <Badge key={d} variant="secondary" asChild><button onClick={() => set({ day: day === d ? "" : d })}>{md(d)} · {n}</button></Badge>
            ))}
          </span>
          {day && <Button size="xs" variant="destructive" onClick={() => set({ day: "" })}>只看 {md(day)} 截止<X /></Button>}
        </div>
        <div className="overflow-x-auto pb-1">
          <div className="grid min-w-max grid-cols-[repeat(35,minmax(30px,1fr))] gap-1">
            {cells.map((d, k) => {
              const key = iso(d), n = counts[key] || 0
              return (
                <Tooltip key={key}>
                  <TooltipTrigger asChild>
                    <Toggle
                      pressed={day === key} onPressedChange={() => set({ day: day === key ? "" : key })} aria-label={`${md(key)} ${n} 个截止`}
                      className={cn("h-11 min-w-0 flex-col justify-between gap-0 rounded-md px-0 py-1 font-mono transition-transform hover:-translate-y-0.5 hover:bg-inherit data-[state=on]:ring-2 data-[state=on]:ring-destructive", level(n), k === 0 && "ring-1 ring-foreground")}
                    >
                      <span className="text-[10px] leading-none opacity-80">{k === 0 ? "今天" : d.getDate()}</span>
                      <span className="text-[11px] leading-none font-semibold">{n || ""}</span>
                    </Toggle>
                  </TooltipTrigger>
                  <TooltipContent>{md(key)}（周{WK[d.getDay()]}）· {n} 个截止</TooltipContent>
                </Tooltip>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
