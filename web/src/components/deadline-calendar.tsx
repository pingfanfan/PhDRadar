// 截止日历：平时是 6 个月的小月历，只有颜色；展开后每格写日期和当天截止数。点一天筛选大屏。
import { useMemo } from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { dlOf, isDate, iso, md, TODAY, weekday } from "@/lib/data"
import { openOn, useFiltered } from "@/lib/select"
import { useApp } from "@/store"

const MONTHS = 6
const heat = (n: number) => (!n ? "var(--line-soft)" : `rgba(var(--sig), ${n < 10 ? 0.25 : n < 40 ? 0.45 : n < 100 ? 0.7 : 1})`)

function Legend() {
  return (
    <span className="flex items-center gap-[3px] text-[11px] text-muted-foreground">
      <span className="mr-1">少</span>
      {[0, 5, 20, 60, 150].map((n) => <span key={n} className="size-2.5 rounded-[2px]" style={{ background: heat(n) }} />)}
      <span className="ml-1">多</span>
    </span>
  )
}

interface Cell { key: string; date?: string; n: number; past: boolean }

export function DeadlineCalendar() {
  const list = useFiltered(true)
  const { day, dayMode, calOpen, set } = useApp()
  const counts = useMemo(() => {
    const c: Record<string, number> = {}
    list.forEach((x) => { const d = dlOf(x); if (isDate(d)) c[d!] = (c[d!] || 0) + 1 })
    return c
  }, [list])
  const today = iso(TODAY)
  const months = useMemo(() => Array.from({ length: MONTHS }, (_, i) => {
    const y = TODAY.getFullYear(), m = TODAY.getMonth() + i, first = new Date(y, m, 1)
    const lead = (first.getDay() + 6) % 7, total = new Date(y, m + 1, 0).getDate()
    const cells: Cell[] = Array.from({ length: lead }, (_, k) => ({ key: `b${k}`, n: 0, past: true }))
    for (let d = 1; d <= total; d++) {
      const date = iso(new Date(first.getFullYear(), first.getMonth(), d))
      cells.push({ key: date, date, n: counts[date] || 0, past: date < today })
    }
    return { title: `${first.getFullYear()}年${first.getMonth() + 1}月`, short: (first.getMonth() === 0 || i === 0 ? `${first.getFullYear()}年` : "") + `${first.getMonth() + 1}月`, cells }
  }), [counts, today])
  const range = `${months[0].title} – ${months[MONTHS - 1].title}`
  const pick = (c: Cell, open = false) => { if (c.date && !c.past) set({ day: day === c.date && !open ? "" : c.date, dayMode: "due", ...(open ? { calOpen: true } : {}) }) }
  const ring = (c: Cell) => (c.date === day ? "0 0 0 2px var(--foreground)" : c.date === today ? "inset 0 0 0 1px var(--foreground)" : undefined)
  const label = (c: Cell) => (c.date ? `${md(c.date)} ${weekday(c.date)}，${c.n} 个截止` : undefined)
  const stillOpen = useMemo(() => (day ? list.filter((x) => openOn(x, day)).length : 0), [list, day])

  return (
    <section id="deadline-calendar" className="mx-auto max-w-[1280px] scroll-mt-4 px-4 pb-4 sm:px-10">
      <div className="flex flex-col gap-4 rounded border bg-card px-4 py-4 sm:px-5">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
          <h2 className={cn("font-bold", calOpen ? "text-[15px]" : "text-[13px]")}>{calOpen ? "截止日历" : "截止分布"}</h2>
          <span className="font-mono text-[11px] text-muted-foreground">{range}</span>
          <div className="ml-auto flex items-center gap-5">
            <Legend />
            <Button variant="outline" size="sm" onClick={() => set({ calOpen: !calOpen })}>{calOpen ? "收起" : "展开日历"}</Button>
          </div>
        </div>

        {!calOpen ? (
          <div className="flex flex-wrap justify-between gap-x-6 gap-y-5">
            {months.map((m, i) => (
              <div key={m.title} className={cn("flex flex-col gap-2", i >= 2 && "max-sm:hidden")}>
                <span className="text-[11px] text-muted-foreground">{m.short}</span>
                <div className="grid grid-cols-[repeat(7,14px)] gap-1">
                  {m.cells.map((c) => (
                    <button
                      key={c.key} type="button" disabled={c.past} onClick={() => pick(c, true)} aria-label={label(c)} title={label(c)}
                      className="size-3.5 cursor-pointer rounded-[3px] disabled:cursor-default"
                      style={{ background: !c.date ? "transparent" : c.past ? "var(--line-soft)" : heat(c.n), opacity: c.past ? 0.5 : 1, boxShadow: ring(c) }}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="month-grid pt-1">
            {months.map((m) => (
              <div key={m.title} className="flex flex-col gap-2.5">
                <span className="text-sm font-bold">{m.title}</span>
                <div className="grid grid-cols-7 gap-1.5 text-center text-[11px] text-muted-foreground">
                  {"一二三四五六日".split("").map((w) => <span key={w}>{w}</span>)}
                </div>
                <div className="grid grid-cols-7 gap-1.5">
                  {m.cells.map((c) => (
                    <button
                      key={c.key} type="button" disabled={c.past} onClick={() => pick(c)} aria-label={label(c)} aria-pressed={c.date === day}
                      className={cn("flex h-12 min-w-0 cursor-pointer flex-col justify-between rounded-[5px] px-1.5 py-1 text-left font-mono disabled:cursor-default", c.past && "text-muted-foreground opacity-45")}
                      style={{ background: c.past ? "transparent" : heat(c.n), boxShadow: ring(c) }}
                    >
                      <span className="text-[11px]">{c.date ? +c.date.slice(8) : ""}</span>
                      <span className="self-end text-xs font-semibold">{!c.past && c.n ? c.n : ""}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {day && (
          <div className="flex flex-wrap items-center gap-x-6 gap-y-2 border-t border-line-soft pt-3">
            <span className="font-bold">{md(day)} {weekday(day)}</span>
            <span className="font-mono text-[13px]">当天截止 <b className="text-urgent">{counts[day] || 0}</b> 个 · 到这天仍可申请 <b>{stillOpen.toLocaleString()}</b> 个</span>
            <span className="flex flex-wrap gap-2 sm:ml-auto">
              {(["due", "open"] as const).map((k) => (
                <Button key={k} size="sm" variant={dayMode === k ? "default" : "outline"} onClick={() => set({ dayMode: k })}>
                  {k === "due" ? "只看这天截止" : "这天仍可申请的全部"}
                </Button>
              ))}
              <Button size="sm" variant="ghost" className="text-muted-foreground" onClick={() => set({ day: "" })}>取消</Button>
            </span>
          </div>
        )}
      </div>
    </section>
  )
}
