import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useTheme } from "@/components/theme-provider"
import { cn } from "@/lib/utils"
import { iso, md, TODAY, weekday } from "@/lib/data"
import { useData } from "@/lib/select"
import { useApp, type View } from "@/store"

export function Brand({ small = false }: { small?: boolean }) {
  return (
    <a href="./" className={cn("shrink-0 font-mono font-semibold tracking-[0.2em] text-foreground no-underline", small ? "text-xs" : "text-[15px]")}>
      PHDRADAR
    </a>
  )
}

export function AppHeader() {
  const { view, setView, saved, skipped, set } = useApp()
  const rows = useData((s) => s.rows)
  const { theme, setTheme } = useTheme()
  const dark = theme === "dark" || (theme === "system" && document.documentElement.classList.contains("dark"))
  const nVer = rows.filter((x) => x.v).length
  const tabs: [View, string, number | null][] = [
    ["now", "截止大屏", null], ["rec", "为我推荐", null], ["ver", "全部信源", nVer],
    ["saved", "收藏", Object.keys(saved).length], ["skipped", "已跳过", Object.keys(skipped).length],
  ]
  const openCal = () => {
    if (location.hash.startsWith("#/p/")) location.hash = ""
    if (view !== "now" && view !== "ver") setView("now")
    set({ calOpen: true })
    requestAnimationFrame(() => document.getElementById("deadline-calendar")?.scrollIntoView({ behavior: "smooth", block: "start" }))
  }

  return (
    <header className="border-b bg-page">
      <div className="mx-auto flex max-w-[1280px] flex-wrap items-center gap-x-8 gap-y-1 px-4 sm:px-10">
        <div className="flex h-14 items-center"><Brand /></div>
        <nav aria-label="视图" className="order-3 -mx-4 flex w-[calc(100%+2rem)] gap-6 self-stretch overflow-x-auto px-4 sm:order-none sm:mx-0 sm:w-auto sm:px-0">
          {tabs.map(([k, label, n]) => (
            <button
              key={k} type="button" onClick={() => { if (location.hash.startsWith("#/p/")) location.hash = ""; setView(k) }} aria-current={view === k ? "page" : undefined}
              className={cn("-mb-px flex h-11 shrink-0 cursor-pointer items-center gap-1.5 border-b-2 text-sm whitespace-nowrap sm:h-14",
                view === k ? "border-urgent font-bold text-foreground" : "border-transparent text-muted-foreground hover:text-foreground")}
            >
              {label}{n !== null && <span className="font-mono text-xs font-normal text-muted-foreground">{n.toLocaleString()}</span>}
            </button>
          ))}
        </nav>
        <div className="ml-auto flex h-14 items-center gap-1">
          <Button variant="ghost" size="sm" asChild className="hidden text-muted-foreground md:inline-flex"><a href="docs/guide-cn.html">申请指南</a></Button>
          <Button variant="ghost" size="sm" asChild className="hidden text-muted-foreground md:inline-flex"><a href="feeds/">订阅</a></Button>
          <Button variant="ghost" size="icon-sm" aria-label="切换深浅色" onClick={() => setTheme(dark ? "light" : "dark")} className="text-muted-foreground">
            {dark ? <Sun /> : <Moon />}
          </Button>
          <Button variant="outline" size="sm" onClick={openCal} aria-label="打开截止日历" className="ml-1 bg-card font-mono text-xs">
            {md(iso(TODAY))} {weekday(iso(TODAY))}
          </Button>
        </div>
      </div>
    </header>
  )
}
