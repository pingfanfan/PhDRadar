import { BookOpen, Bookmark, Download, Moon, Radar, Rss, Sun } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { useTheme } from "@/components/theme-provider"
import { isNow } from "@/lib/data"
import { useData } from "@/lib/select"
import { useApp, type View } from "@/store"

const REPO = "https://github.com/pingfanfan/PhDRadar"

export function Brand({ small = false }: { small?: boolean }) {
  return (
    <a href="./" className="flex shrink-0 items-center gap-2 font-semibold tracking-tight text-foreground no-underline">
      <span className={`grid place-items-center rounded-lg bg-primary text-primary-foreground ${small ? "size-6" : "size-8"}`}>
        <Radar className={small ? "size-3.5" : "size-[18px]"} strokeWidth={2.2} />
      </span>
      <span className={small ? "text-sm" : "text-base"}>PhDRadar</span>
    </a>
  )
}

function IconLink({ href, label, icon: Icon }: { href: string; label: string; icon: typeof Rss }) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button variant="ghost" size="sm" asChild>
          <a href={href} aria-label={label}>
            <Icon />
            <span className="hidden lg:inline">{label}</span>
          </a>
        </Button>
      </TooltipTrigger>
      <TooltipContent>{label}</TooltipContent>
    </Tooltip>
  )
}

export function AppHeader() {
  const { view, setView, saved } = useApp()
  const rows = useData((s) => s.rows)
  const nNow = rows.filter(isNow).length, nVer = rows.filter((x) => x.v).length
  const { theme, setTheme } = useTheme()
  const dark = theme === "dark" || (theme === "system" && document.documentElement.classList.contains("dark"))
  const nSaved = Object.keys(saved).length

  return (
    <header className="sticky top-0 z-30 border-b bg-background/80 backdrop-blur-md supports-[backdrop-filter]:bg-background/70">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-4 gap-y-2 px-4 py-2.5 md:flex-nowrap">
        <Brand />
        <Tabs value={view === "saved" ? "" : view} onValueChange={(v) => setView(v as View)} className="order-3 w-full md:order-none md:w-auto">
          <TabsList className="w-full justify-start overflow-x-auto md:w-auto">
            <TabsTrigger value="now">现在可申请{nNow > 0 && <span className="font-mono text-xs text-muted-foreground">{nNow.toLocaleString()}</span>}</TabsTrigger>
            <TabsTrigger value="rec">为我推荐</TabsTrigger>
            <TabsTrigger value="ver">全部已核对{nVer > 0 && <span className="font-mono text-xs text-muted-foreground">{nVer.toLocaleString()}</span>}</TabsTrigger>
          </TabsList>
        </Tabs>
        <div className="ml-auto flex items-center gap-1">
          <IconLink href="docs/guide-cn.html" label="申请指南" icon={BookOpen} />
          <IconLink href="feeds/" label="订阅" icon={Rss} />
          <IconLink href={`${REPO}/tree/main/data/export`} label="数据" icon={Download} />
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="icon-sm" aria-label="切换深浅色" onClick={() => setTheme(dark ? "light" : "dark")}>
                {dark ? <Sun /> : <Moon />}
              </Button>
            </TooltipTrigger>
            <TooltipContent>切换深浅色</TooltipContent>
          </Tooltip>
          <Button variant={view === "saved" ? "default" : "outline"} size="sm" onClick={() => setView(view === "saved" ? "now" : "saved")}>
            <Bookmark className={view === "saved" ? "fill-current" : ""} />
            <span className="hidden sm:inline">我的申请</span>
            <Badge variant={view === "saved" ? "secondary" : "outline"} className="font-mono">{nSaved}</Badge>
          </Button>
        </div>
      </div>
    </header>
  )
}
