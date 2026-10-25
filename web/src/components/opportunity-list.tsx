import { Bookmark, Clock, SearchX, Sparkles } from "lucide-react"
import { AnimatePresence, motion } from "motion/react"
import { toast } from "sonner"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty"
import { cn } from "@/lib/utils"
import { dueShort, flag, group, screened, shortPay, type Labels, type Row, type Tone } from "@/lib/data"
import { useData, type Ranking } from "@/lib/select"
import { stageOf, stageText, useApp } from "@/store"

export const TONE: Record<Tone, string> = { urgent: "text-destructive", soon: "text-amber-600 dark:text-amber-400", rolling: "text-primary", "": "text-muted-foreground" }

// 机构那一行：旗帜 + 机构 · 地区
export function OrgLine({ x, labels, className }: { x: Row; labels: Labels; className?: string }) {
  const f = flag(x.r?.[0]), region = (x.r || []).map((r) => labels.region[r] || r).join(" · ")
  return (
    <span className={cn("min-w-0 truncate", className)}>
      {f && <span className="mr-1.5" aria-hidden>{f}</span>}{[x.org, region].filter(Boolean).join(" · ")}
    </span>
  )
}

export function SaveButton({ id, withText = false }: { id: string; withText?: boolean }) {
  const { saved, toggleSave } = useApp()
  const on = !!saved[id]
  const click = (e: React.MouseEvent) => {
    e.stopPropagation()
    toast(toggleSave(id) ? "已加入我的申请" : "已取消收藏")
  }
  return withText ? (
    <Button variant="outline" size="lg" onClick={click} aria-pressed={on}><Bookmark className={on ? "fill-current text-primary" : ""} />{on ? "已收藏" : "收藏"}</Button>
  ) : (
    <Button variant="ghost" size="icon-sm" onClick={click} aria-pressed={on} aria-label={on ? "取消收藏" : "收藏"} className={cn("-mt-1 -mr-1.5 shrink-0", on ? "text-primary" : "text-muted-foreground/60 hover:text-foreground")}>
      <Bookmark className={on ? "fill-current" : ""} />
    </Button>
  )
}

function Why({ x, rank }: { x: Row; rank: Ranking }) {
  const a = rank.by.get(x.id)
  if (!a) return null
  const strong = rank.hit.has(x.id)
  return (
    <span className={cn("mt-1 flex flex-col gap-0.5 rounded-md px-2.5 py-1.5 text-xs", strong ? "bg-primary/10 text-foreground" : "bg-muted text-muted-foreground")}>
      <b className="inline-flex items-center gap-1 font-mono text-primary"><Sparkles className="size-3" />匹配 {a.score}</b>
      <span>{a.reasons[0]?.replace(/^[^：]+：/, "")}</span>
    </span>
  )
}

const TAG = "h-5 rounded-md px-1.5 text-[11px] font-normal"

export function OpportunityItem({ x, labels, active, onOpen, rank }: { x: Row; labels: Labels; active: boolean; onOpen: () => void; rank?: Ranking | null }) {
  const status = useApp((s) => s.status), saved = useApp((s) => !!s.saved[x.id])
  const [dt, tone] = dueShort(x, labels), pay = shortPay(x, labels)
  return (
    <div
      role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && (e.preventDefault(), onOpen())}
      aria-current={active || undefined}
      className={cn("relative flex cursor-pointer flex-col gap-1.5 px-4 py-3.5 outline-none transition-colors hover:bg-accent/60 focus-visible:bg-accent",
        active && "bg-accent before:absolute before:inset-y-3 before:left-0 before:w-[3px] before:rounded-r-full before:bg-primary")}
    >
      <div className="flex items-center gap-3 text-xs text-muted-foreground">
        <OrgLine x={x} labels={labels} />
        <span className={cn("ml-auto inline-flex shrink-0 items-center gap-1 font-medium", TONE[tone])}><Clock className="size-3" />{dt}</span>
      </div>
      <div className="flex items-start gap-2">
        <h4 className="line-clamp-2 flex-1 text-[15px] leading-snug font-medium">{x.n}</h4>
        <SaveButton id={x.id} />
      </div>
      {x.in && <p className="line-clamp-2 text-[13px] leading-relaxed text-muted-foreground">{x.in}</p>}
      {rank && <Why x={x} rank={rank} />}
      <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
        {pay && <span className="mr-1 font-mono text-xs font-medium">{pay}</span>}
        {saved && <Badge variant="outline" className={TAG}>{stageText(stageOf(status, x.id))}</Badge>}
        <Badge variant="secondary" className={TAG}>{(x.l || ["phd"]).map((l) => labels.level[l] || l).join(" / ")}</Badge>
        {x.e === "yes" && <Badge className={cn(TAG, "bg-primary/10 text-primary")}>中国学生可申</Badge>}
        {x.e === "partial" && <Badge variant="secondary" className={TAG}>部分可申</Badge>}
        {screened(x) && <Badge variant="destructive" className={TAG}>留意安全审查</Badge>}
      </div>
    </div>
  )
}

export function OpportunityList({ list, onOpen, rank, emptyText }: { list: Row[]; onOpen: (id: string) => void; rank?: Ranking | null; emptyText: string }) {
  const labels = useData((s) => s.labels)!
  const { sel, shown, more } = useApp()
  if (!list.length)
    return (
      <Empty className="border border-dashed bg-card">
        <EmptyHeader>
          <EmptyMedia variant="icon"><SearchX /></EmptyMedia>
          <EmptyTitle>没有找到</EmptyTitle>
          <EmptyDescription>{emptyText}</EmptyDescription>
        </EmptyHeader>
      </Empty>
    )
  const counts: Record<string, number> = {}
  const head = (x: Row) => (rank ? (rank.hit.has(x.id) ? "命中你的关键词 · 按匹配度排序" : "学科相同、没有命中关键词") : group(x))
  list.forEach((x) => { const g = head(x); counts[g] = (counts[g] || 0) + 1 })
  const page = list.slice(0, shown), heads = page.map(head)
  return (
    <div className="flex flex-col">
      <AnimatePresence initial={false}>
        {page.flatMap((x, i) => {
          const g = heads[i], fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.15 } }
          const item = (
            <motion.div key={x.id} layout="position" {...fade} className={cn(i > 0 && g === heads[i - 1] && "border-t")}>
              <OpportunityItem x={x} labels={labels} active={x.id === sel} onOpen={() => onOpen(x.id)} rank={rank} />
            </motion.div>
          )
          return i === 0 || g !== heads[i - 1] ? [
            <motion.h3 key={"h:" + g} layout="position" {...fade}
              className="z-10 flex items-center justify-between border-y bg-muted/80 px-4 py-1.5 text-xs font-medium text-muted-foreground backdrop-blur first:border-t-0 md:sticky md:top-0">
              {g}<span className="font-mono">{counts[g]}</span>
            </motion.h3>, item] : [item]
        })}
      </AnimatePresence>
      {list.length > shown && <div className="border-t p-4 text-center"><Button variant="outline" size="sm" onClick={more}>加载更多（还有 {list.length - shown} 个）</Button></div>}
    </div>
  )
}
