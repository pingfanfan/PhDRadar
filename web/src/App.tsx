import { useEffect, useState } from "react"
import { Skeleton } from "@/components/ui/skeleton"
import { AppHeader, Brand } from "@/components/app-header"
import { Board, pageHref } from "@/components/board"
import { DeadlineCalendar } from "@/components/deadline-calendar"
import { DetailPanel } from "@/components/detail-panel"
import { Hero } from "@/components/search-bar"
import { RecommendForm } from "@/components/recommend-form"
import { SavedBoard } from "@/components/saved-board"
import { loadData, type Row } from "@/lib/data"
import { useData, useFiltered, useRanking } from "@/lib/select"
import { useApp } from "@/store"

const REPO = "https://github.com/pingfanfan/PhDRadar"

// 地址里 #/p/<id> 是单个机会的完整页面；#<id> 是在大屏上展开这一条
const pageId = () => (location.hash.startsWith("#/p/") ? decodeURIComponent(location.hash.slice(4)) : "")

function useBoot() {
  useEffect(() => {
    loadData()
      .then(({ rows, labels }) => {
        useData.setState({ rows, labels, byId: new Map(rows.map((x) => [x.id, x])) })
        const h = decodeURIComponent(location.hash.slice(1))
        if (h && !h.startsWith("/p/") && rows.some((x) => x.id === h)) useApp.getState().select(h)
      })
      .catch(() => useData.setState({ error: "数据加载失败，请刷新页面。" }))
    fetch("assets/rank-rules.json").then((r) => r.json()).then((rules) => useData.setState({ rules })).catch(() => {})
  }, [])
}

function usePage() {
  const [id, setId] = useState(pageId)
  useEffect(() => {
    const on = () => { setId(pageId()); window.scrollTo(0, 0) }
    window.addEventListener("hashchange", on)
    return () => window.removeEventListener("hashchange", on)
  }, [])
  return id
}

function DetailPage({ id }: { id: string }) {
  const x = useData((s) => s.byId.get(id))
  const back = () => (history.length > 1 ? history.back() : (location.hash = ""))
  return (
    <main className="mx-auto max-w-[1080px] px-4 pt-6 pb-16 sm:px-10">
      <button type="button" onClick={back} className="mb-4 cursor-pointer text-sm text-muted-foreground hover:text-foreground">← 返回</button>
      <div className="overflow-hidden rounded border bg-card">
        {x ? <DetailPanel x={x} /> : <p className="p-10 text-center text-muted-foreground">没有找到这个机会，它可能已经截止下架。</p>}
      </div>
    </main>
  )
}

export default function App() {
  useBoot()
  const page = usePage()
  const { rows, error, byId } = useData()
  const view = useApp((s) => s.view)
  const filtered = useFiltered()
  const ranking = useRanking()
  const recList = ranking ? ranking.res.ranked.concat(ranking.res.related.slice(0, 40)).map((a) => byId.get(a.id)).filter(Boolean) as Row[] : []
  const emptyText = view === "rec"
    ? (ranking ? "没有命中你关键词的机会。换个说法（加英文、同义词），或放宽国家、资助、截止条件。" : "在上面填研究方向关键词，就会按你的条件排序。")
    : view === "skipped" ? "还没有跳过的机会。" : "没有找到。换个说法试试，或去掉上面的筛选。"

  let body
  if (error) body = <p className="p-10 text-center text-muted-foreground">{error}</p>
  else if (!rows.length) body = (
    <div className="mx-auto flex max-w-[1280px] flex-col gap-3 px-4 pt-8 sm:px-10">
      <Skeleton className="h-9 w-1/3" /><Skeleton className="h-[52px] w-full" /><Skeleton className="h-32 w-full" />
      {Array.from({ length: 5 }, (_, i) => <Skeleton key={i} className="h-16 w-full" />)}
    </div>
  )
  else if (page) body = <DetailPage id={page} />
  else if (view === "saved") body = <div className="mx-auto max-w-[1280px] px-4 pt-6 pb-16 sm:px-10"><SavedBoard onOpen={(id) => (location.hash = pageHref(id))} /></div>
  else body = (
    <main>
      {view === "rec" ? <RecommendForm rank={ranking} /> : view !== "skipped" && <><Hero found={filtered.length} /><DeadlineCalendar /></>}
      {view === "skipped" && <div className="mx-auto max-w-[1280px] px-4 pt-6 pb-3 text-sm text-muted-foreground sm:px-10">跳过的机会不会出现在大屏上；点开一条可以撤销。</div>}
      <Board list={view === "rec" ? recList : filtered} rank={view === "rec" ? ranking : null} emptyText={emptyText} />
    </main>
  )

  return (
    <div className="min-h-dvh bg-page">
      <AppHeader />
      {body}
      <footer className="border-t">
        <div className="mx-auto flex max-w-[1280px] flex-wrap items-center gap-x-6 gap-y-2 px-4 py-6 text-xs text-muted-foreground sm:px-10">
          <Brand small />
          <p className="flex-1 basis-80">信息以各机构官网为准。本站与所列机构无关；发现错误请<a className="underline underline-offset-2" href={`${REPO}/issues`}>在 GitHub 提 Issue</a>。数据 CC BY 4.0，代码 MIT。</p>
        </div>
      </footer>
    </div>
  )
}
