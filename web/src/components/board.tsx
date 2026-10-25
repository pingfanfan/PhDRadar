// 截止大屏：按截止时间分组，一行一个机会；点一行就地展开，展开后可打开完整页面。
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { dueCell, group, isNow, payParts, type Labels, type Row } from "@/lib/data"
import { useData, type Ranking } from "@/lib/select"
import { useApp } from "@/store"

export const pageHref = (id: string) => "#/p/" + encodeURIComponent(id)

export function LevelTag({ x, labels }: { x: Row; labels: Labels }) {
  const pd = (x.l || ["phd"])[0] === "postdoc"
  return (
    <span className={cn("mr-2 inline-block rounded-[3px] align-[2px] text-[11px] font-bold", pd ? "border border-foreground px-[5px] leading-4" : "bg-foreground px-1.5 leading-[18px] text-background")}>
      {labels.level[pd ? "postdoc" : "phd"]}
    </span>
  )
}

function Expanded({ x }: { x: Row }) {
  const { saved, skipped, toggleSave, toggleSkip } = useApp()
  const quote = isNow(x) ? x.o!.q : x.pq
  const req: [string, string | undefined][] = [["学位", x.af?.dg?.[0]], ["语言", x.af?.lg?.[0] || x.lt], ["材料", x.af?.dc?.[0]]]
  return (
    <div className="board-exp pt-0.5 pb-5">
      <div className="flex flex-col gap-3.5">
        {x.in && <p className="text-sm leading-7">{x.in}</p>}
        <dl className="grid grid-cols-[64px_minmax(0,1fr)] gap-x-3.5 gap-y-2 text-[13px]">
          {req.map(([k, v]) => [<dt key={k + "t"} className="text-muted-foreground">{k}</dt>, <dd key={k} className={cn(!v && "text-muted-foreground")}>{v || "未写明"}</dd>])}
          <dt className="text-muted-foreground">中国学生</dt>
          <dd className={x.e === "yes" ? "font-bold" : "text-muted-foreground"}>{x.e === "yes" ? "公告写明国际生可申请" : x.e === "no" ? "公告写明仅限本国或特定地区" : "公告未写明，申请前请自行确认"}</dd>
        </dl>
      </div>
      <div className="flex flex-col gap-3.5">
        {quote && (
          <figure className="flex flex-col gap-1 rounded bg-muted px-3.5 py-3">
            <figcaption className="text-xs text-muted-foreground">官网原句</figcaption>
            <blockquote className="font-mono text-[13px] break-words">{quote}</blockquote>
          </figure>
        )}
        <div className="flex flex-wrap gap-2">
          <Button asChild><a href={x.u} target="_blank" rel="noopener">去官网申请 ↗</a></Button>
          <Button variant="outline" onClick={() => toast(toggleSave(x.id) ? "已收藏" : "已取消收藏")}>{saved[x.id] ? "已收藏" : "收藏"}</Button>
          <Button variant="outline" onClick={() => toast(toggleSkip(x.id) ? "已跳过，不再出现在大屏上" : "已撤销跳过")}>{skipped[x.id] ? "撤销跳过" : "跳过，不再显示"}</Button>
          <Button variant="link" asChild className="px-1"><a href={pageHref(x.id)}>完整页面 →</a></Button>
        </div>
      </div>
    </div>
  )
}

function BoardRow({ x, labels, rank }: { x: Row; labels: Labels; rank?: Ranking | null }) {
  const { sel, select, saved } = useApp()
  const open = sel === x.id, due = dueCell(x), pay = payParts(x)
  const why = rank?.by.get(x.id)
  const toggle = () => { select(open ? "" : x.id); history.replaceState(null, "", open ? location.pathname : "#" + encodeURIComponent(x.id)) }
  return (
    <div className={cn("border-b border-line-soft", open && "bg-accent")}>
      <button type="button" onClick={toggle} aria-expanded={open} className="board-grid w-full cursor-pointer px-4 py-3.5 text-left hover:bg-accent sm:px-5">
        <span className="c-due flex flex-col gap-0.5 leading-tight">
          <span className={cn("font-mono text-lg font-semibold", due.tone === "today" ? "text-urgent" : due.tone === "upcoming" ? "text-upcoming" : "")}>{due.main}</span>
          <span className="font-mono text-[11px] text-muted-foreground">{due.sub}</span>
        </span>
        <span className="c-pay min-w-0 leading-snug">
          <span className={cn("font-mono text-[13px] [overflow-wrap:anywhere]", pay.amt ? "font-semibold" : "font-medium", pay.none && "text-muted-foreground")}>{pay.main}</span>
          {pay.note && <span className="text-[11px] text-muted-foreground">{pay.note}</span>}
        </span>
        <span className="c-place text-sm">{(x.r || []).map((r) => labels.region[r] || r).join(" · ") || "—"}</span>
        <span className="c-title flex min-w-0 flex-col gap-0.5">
          <span className="line-clamp-2 text-[15px] leading-snug font-medium"><LevelTag x={x} labels={labels} />{x.n}</span>
          <span className="truncate text-xs text-muted-foreground">
            {[x.org, (x.d || []).filter((d) => d !== "all").map((d) => labels.discipline[d] || d).slice(0, 2).join(" / ")].filter(Boolean).join(" · ")}
            {saved[x.id] && <span className="font-bold text-urgent"> · 已收藏</span>}
          </span>
          {why && <span className="text-xs text-muted-foreground">匹配 {why.score} · {why.reasons[0]?.replace(/^[^：]+：/, "")}</span>}
        </span>
      </button>
      {open && <Expanded x={x} />}
    </div>
  )
}

export function Board({ list, rank, emptyText }: { list: Row[]; rank?: Ranking | null; emptyText: string }) {
  const labels = useData((s) => s.labels)!
  const { shown, more } = useApp()
  const head = (x: Row) => (rank ? (rank.hit.has(x.id) ? "命中你的关键词 · 按匹配度排序" : "学科相同、没有命中关键词") : group(x))
  const counts: Record<string, number> = {}
  list.forEach((x) => { const g = head(x); counts[g] = (counts[g] || 0) + 1 })
  const page = list.slice(0, shown)
  return (
    <section className="mx-auto max-w-[1280px] px-4 pb-16 sm:px-10">
      <div className="overflow-hidden rounded border bg-card">
        <div className="board-head border-b px-5 py-2.5 font-mono text-[11px] tracking-wider text-muted-foreground">
          <span>截止</span><span>资助</span><span>地点</span><span>机会</span>
        </div>
        {!list.length && <p className="px-5 py-12 text-center text-muted-foreground">{emptyText}</p>}
        {page.map((x, i) => {
          const g = head(x), first = i === 0 || g !== head(page[i - 1])
          return (
            <div key={x.id}>
              {first && (
                <div className="flex items-baseline gap-3 border-b border-line-soft px-4 pt-4 pb-2 sm:px-5">
                  <span className="text-[13px] font-bold">{g}</span>
                  <span className="font-mono text-xs text-muted-foreground">{counts[g].toLocaleString()}</span>
                </div>
              )}
              <BoardRow x={x} labels={labels} rank={rank} />
            </div>
          )
        })}
        {list.length > shown && (
          <div className="p-4 text-center"><Button variant="outline" size="sm" onClick={more}>加载更多（还有 {(list.length - shown).toLocaleString()} 个）</Button></div>
        )}
      </div>
      <p className="mt-5 text-xs text-muted-foreground">截止时间以官网为准，注意时区。</p>
    </section>
  )
}
