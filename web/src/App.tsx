import { useEffect } from "react"
import { AnimatePresence, motion } from "motion/react"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetDescription, SheetTitle } from "@/components/ui/sheet"
import { Skeleton } from "@/components/ui/skeleton"
import { AppHeader, Brand } from "@/components/app-header"
import { DeadlineStrip, SearchBar } from "@/components/search-bar"
import { DetailPanel } from "@/components/detail-panel"
import { OpportunityList } from "@/components/opportunity-list"
import { RecommendForm } from "@/components/recommend-form"
import { SavedBoard } from "@/components/saved-board"
import { useIsMobile } from "@/hooks/use-mobile"
import { loadData, type Row } from "@/lib/data"
import { useData, useFiltered, useRanking, type Ranking } from "@/lib/select"
import { useApp } from "@/store"

const REPO = "https://github.com/pingfanfan/PhDRadar"

function useBoot() {
  useEffect(() => {
    loadData()
      .then(({ rows, labels }) => {
        useData.setState({ rows, labels, byId: new Map(rows.map((x) => [x.id, x])) })
        const h = decodeURIComponent(location.hash.slice(1))
        if (h && rows.some((x) => x.id === h)) useApp.getState().select(h)
      })
      .catch(() => useData.setState({ error: "数据加载失败，请刷新页面。" }))
    fetch("assets/rank-rules.json").then((r) => r.json()).then((rules) => useData.setState({ rules })).catch(() => {})
  }, [])
}

function Workspace({ list, rank, emptyText }: { list: Row[]; rank: Ranking | null; emptyText: string }) {
  const mobile = useIsMobile()
  const { sel, select, view } = useApp()
  const byId = useData((s) => s.byId)
  const current = byId.get(sel) || (mobile ? undefined : list[0])
  const open = (id: string) => { select(id); history.replaceState(null, "", "#" + encodeURIComponent(id)) }
  const header = (
    <div className="flex items-baseline justify-between border-b px-4 py-2.5 text-xs text-muted-foreground">
      <span><b className="font-mono text-sm text-foreground">{list.length.toLocaleString()}</b> 个机会</span>
      <span>{rank ? "按匹配度排序" : "按截止日期分组"}</span>
    </div>
  )
  const detail = (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div key={current?.id || "none"} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.16 }} className="h-full">
        <DetailPanel x={current} rank={rank} />
      </motion.div>
    </AnimatePresence>
  )

  if (view === "saved") return <div className="px-4 pt-6 pb-16"><SavedBoard onOpen={open} />{sel && <MobileOrSideSheet rank={rank} />}</div>

  if (mobile)
    return (
      <div className="px-4 pb-16">
        <div className="overflow-hidden rounded-xl border bg-card">
          {header}
          <OpportunityList list={list} onOpen={open} rank={rank} emptyText={emptyText} />
        </div>
        <MobileOrSideSheet rank={rank} />
      </div>
    )

  return (
    <div className="mx-auto max-w-7xl px-4 pb-10">
      <ResizablePanelGroup orientation="horizontal" className="h-[calc(100dvh-5rem)] rounded-xl border bg-card shadow-xs">
        <ResizablePanel defaultSize="40" minSize="28">
          <ScrollArea className="h-full [&_[data-slot=scroll-area-viewport]>div]:block!">
            <div>{header}<OpportunityList list={list} onOpen={open} rank={rank} emptyText={emptyText} /></div>
          </ScrollArea>
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize="60" minSize="36">
          <ScrollArea className="h-full">{detail}</ScrollArea>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  )
}

// 手机上（以及看板里点开）用 Sheet 展示详情
function MobileOrSideSheet({ rank }: { rank: Ranking | null }) {
  const { sel, select } = useApp()
  const x = useData((s) => s.byId.get(sel))
  return (
    <Sheet open={!!x} onOpenChange={(o) => !o && select("")}>
      <SheetContent side="right" className="w-full gap-0 overflow-y-auto p-0 sm:max-w-xl">
        <SheetTitle className="sr-only">{x?.n || "详情"}</SheetTitle>
        <SheetDescription className="sr-only">机会详情</SheetDescription>
        {x && <DetailPanel x={x} rank={rank} />}
      </SheetContent>
    </Sheet>
  )
}

export default function App() {
  useBoot()
  const { rows, error } = useData()
  const view = useApp((s) => s.view)
  const filtered = useFiltered()
  const ranking = useRanking()
  const byId = useData((s) => s.byId)
  const recList = ranking ? ranking.res.ranked.concat(ranking.res.related.slice(0, 40)).map((a) => byId.get(a.id)).filter(Boolean) as Row[] : []
  const list = view === "rec" ? recList : filtered
  const emptyText = view === "rec"
    ? (ranking ? "没有命中你关键词的机会。换个说法（加英文、同义词），或放宽国家、资助、截止条件。" : "在上面填研究方向关键词，就会按你的条件排序。")
    : "没有符合条件的机会，试试放宽筛选。"

  return (
    <div className="min-h-dvh bg-muted/40">
      <AppHeader />
      {error ? <p className="p-10 text-center text-muted-foreground">{error}</p>
        : !rows.length ? (
          <div className="mx-auto flex max-w-7xl flex-col gap-3 p-4 pt-8">
            <Skeleton className="h-9 w-2/3" /><Skeleton className="h-11 w-full max-w-4xl" /><Skeleton className="h-28 w-full" />
            {Array.from({ length: 4 }, (_, i) => <Skeleton key={i} className="h-28 w-full max-w-xl" />)}
          </div>
        ) : (
          <main>
            {view === "rec" ? <RecommendForm rank={ranking} /> : view !== "saved" && <><SearchBar /><DeadlineStrip /></>}
            <Workspace list={list} rank={view === "rec" ? ranking : null} emptyText={emptyText} />
          </main>
        )}
      <footer className="border-t bg-background">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-6 text-xs text-muted-foreground">
          <Brand small />
          <p className="flex-1 basis-80">信息以各机构官网为准，截止时间注意时区。本站与所列机构无关；发现错误请<a className="underline underline-offset-2" href={`${REPO}/issues`}>在 GitHub 提 Issue</a>。数据 CC BY 4.0，代码 MIT。</p>
        </div>
      </footer>
    </div>
  )
}
