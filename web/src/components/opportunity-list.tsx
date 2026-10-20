import { Bookmark, Clock, SearchX, Sparkles } from "lucide-react"
import { AnimatePresence, motion } from "motion/react"
import { toast } from "sonner"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty"
import { Item, ItemActions, ItemContent, ItemDescription, ItemFooter, ItemMedia, ItemTitle } from "@/components/ui/item"
import { cn } from "@/lib/utils"
import { due, group, monogram, screened, shortPay, type Labels, type Row, type Tone } from "@/lib/data"
import { useData, type Ranking } from "@/lib/select"
import { stageOf, stageText, useApp } from "@/store"

export const TONE: Record<Tone, string> = { urgent: "text-destructive", soon: "text-amber-600 dark:text-amber-400", rolling: "text-primary", "": "text-muted-foreground" }

export function OrgAvatar({ x, size = "default" }: { x: Row; size?: "default" | "lg" }) {
  return (
    <Avatar className={cn("rounded-lg border", size === "lg" ? "size-12" : "size-10")}>
      <AvatarFallback className={cn("rounded-lg bg-muted font-semibold text-muted-foreground", size === "lg" ? "text-base" : "text-sm")}>{monogram(x)}</AvatarFallback>
    </Avatar>
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
    <Button variant="ghost" size="icon" onClick={click} aria-pressed={on} aria-label={on ? "取消收藏" : "收藏"} className={on ? "text-primary" : "text-muted-foreground"}>
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

export function OpportunityItem({ x, labels, active, onOpen, rank }: { x: Row; labels: Labels; active: boolean; onOpen: () => void; rank?: Ranking | null }) {
  const status = useApp((s) => s.status), saved = useApp((s) => !!s.saved[x.id])
  const [dt, tone] = due(x, labels), pay = shortPay(x, labels)
  const region = (x.r || []).map((r) => labels.region[r] || r).join(" · ")
  return (
    <Item
      variant="outline" asChild
      className={cn("cursor-pointer items-start bg-card transition-[border-color,box-shadow] hover:border-foreground/20 hover:shadow-sm", active && "border-primary ring-3 ring-primary/15")}
    >
      <div role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && (e.preventDefault(), onOpen())}>
        <ItemMedia><OrgAvatar x={x} /></ItemMedia>
        <ItemContent className="min-w-0 gap-1">
          <ItemTitle className="line-clamp-2 text-[15px] leading-snug">{x.n}</ItemTitle>
          <ItemDescription className="line-clamp-1">{[x.org, region].filter(Boolean).join(" · ")}</ItemDescription>
          {x.in && <p className="line-clamp-2 text-[13px] leading-relaxed text-foreground/80">{x.in}</p>}
          {rank && <Why x={x} rank={rank} />}
        </ItemContent>
        <ItemActions className="self-start"><SaveButton id={x.id} /></ItemActions>
        <ItemFooter className="flex-wrap justify-start gap-x-3 gap-y-1.5 pl-[52px]">
          <span className={cn("inline-flex items-center gap-1 text-xs font-medium", TONE[tone])}><Clock className="size-3.5" />{dt}</span>
          {pay && <span className="font-mono text-xs font-medium">{pay}</span>}
          <span className="flex flex-wrap gap-1.5">
            {saved && <Badge variant="outline">{stageText(stageOf(status, x.id))}</Badge>}
            <Badge variant="secondary">{(x.l || ["phd"]).map((l) => labels.level[l] || l).join(" / ")}</Badge>
            {x.e === "yes" && <Badge className="bg-primary/10 text-primary">中国学生可申</Badge>}
            {x.e === "partial" && <Badge variant="secondary">部分可申</Badge>}
            {screened(x) && <Badge variant="destructive">留意安全审查</Badge>}
          </span>
        </ItemFooter>
      </div>
    </Item>
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
    <div className="flex flex-col gap-2">
      <AnimatePresence initial={false}>
        {page.map((x, i) => {
          const g = heads[i], h = i === 0 || g !== heads[i - 1]
          return (
            <motion.div key={x.id} layout="position" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.18 }} className="flex flex-col gap-2">
              {h && <h3 className="mt-3 flex items-center gap-2 text-xs font-medium tracking-wide text-muted-foreground first:mt-0 after:h-px after:flex-1 after:bg-border">{g}<span className="font-mono">{counts[g]}</span></h3>}
              <OpportunityItem x={x} labels={labels} active={x.id === sel} onOpen={() => onOpen(x.id)} rank={rank} />
            </motion.div>
          )
        })}
      </AnimatePresence>
      {list.length > shown && <Button variant="outline" className="self-center rounded-full px-6" onClick={more}>加载更多（还有 {list.length - shown} 个）</Button>}
    </div>
  )
}
