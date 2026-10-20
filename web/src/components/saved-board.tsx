// 我的申请：五列看板（想投 → 准备中 → 已投 → 面试 → 结果），拖动卡片改变进度（dnd-kit）
import { useState } from "react"
import { DndContext, DragOverlay, KeyboardSensor, PointerSensor, TouchSensor, useDraggable, useDroppable, useSensor, useSensors, type DragEndEvent } from "@dnd-kit/core"
import { Bookmark, CalendarPlus, Clock, FileJson, GripVertical } from "lucide-react"
import { motion } from "motion/react"
import { toast } from "sonner"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import { download, due, icsCalendar, iso, TODAY, type Labels, type Row } from "@/lib/data"
import { exportable, useData } from "@/lib/select"
import { STAGES, stageOf, stageText, useApp, type Stage } from "@/store"
import { OrgAvatar, TONE } from "@/components/opportunity-list"

function BoardCard({ x, labels, onOpen, overlay = false }: { x: Row; labels: Labels; onOpen?: () => void; overlay?: boolean }) {
  const status = useApp((s) => s.status)
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id: x.id, disabled: overlay })
  const [dt, tone] = due(x, labels), v = stageOf(status, x.id)
  return (
    <motion.div ref={overlay ? undefined : setNodeRef} layout={!overlay} animate={overlay ? { rotate: 1.5, scale: 1.03 } : { rotate: 0, scale: 1 }}
      className={cn(isDragging && "opacity-40")}>
      <Card size="sm" className={cn("gap-0 py-0 transition-shadow hover:shadow-md", overlay && "shadow-xl ring-2 ring-primary/30")}>
        <CardContent className="flex items-start gap-2 p-3">
          <button className="mt-0.5 cursor-grab touch-none text-muted-foreground active:cursor-grabbing" aria-label="拖动改变进度" {...listeners} {...attributes}>
            <GripVertical className="size-4" />
          </button>
          <button className="flex min-w-0 flex-1 items-start gap-2.5 text-left" onClick={onOpen}>
            <OrgAvatar x={x} />
            <span className="flex min-w-0 flex-col gap-1">
              <span className="line-clamp-2 text-sm leading-snug font-medium">{x.n}</span>
              <span className={cn("inline-flex items-center gap-1 text-xs", TONE[tone])}><Clock className="size-3" />{dt}</span>
              {v.s === "result" && v.r && <Badge variant="secondary" className="w-fit">{stageText(v)}</Badge>}
            </span>
          </button>
        </CardContent>
      </Card>
    </motion.div>
  )
}

function Column({ stage, title, items, labels, onOpen }: { stage: Stage; title: string; items: Row[]; labels: Labels; onOpen: (id: string) => void }) {
  const { setNodeRef, isOver } = useDroppable({ id: stage })
  return (
    <div ref={setNodeRef} className={cn("flex w-72 shrink-0 flex-col gap-2 rounded-xl border bg-muted/40 p-2 transition-colors", isOver && "border-primary bg-primary/5")}>
      <div className="flex items-center justify-between px-1.5 py-1 text-sm font-medium">{title}<Badge variant="outline" className="font-mono">{items.length}</Badge></div>
      {items.map((x) => <BoardCard key={x.id} x={x} labels={labels} onOpen={() => onOpen(x.id)} />)}
      {!items.length && <p className="rounded-lg border border-dashed px-3 py-6 text-center text-xs text-muted-foreground">拖到这里</p>}
    </div>
  )
}

export function SavedBoard({ onOpen }: { onOpen: (id: string) => void }) {
  const { rows, labels, byId } = useData()
  const { saved, status, setStage } = useApp()
  const [drag, setDrag] = useState<string | null>(null)
  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),
    useSensor(TouchSensor, { activationConstraint: { delay: 180, tolerance: 6 } }), useSensor(KeyboardSensor))
  if (!labels) return null
  const list = rows.filter((x) => saved[x.id])
  const gone = Object.keys(saved).filter((id) => !byId.has(id)).length
  const ex = exportable(rows, saved, status)

  const end = (e: DragEndEvent) => {
    setDrag(null)
    const to = e.over?.id as Stage | undefined
    if (to && to !== stageOf(status, String(e.active.id)).s) {
      setStage(String(e.active.id), to)
      toast(`已移到「${STAGES.find(([k]) => k === to)![1]}」`)
    }
  }

  if (!list.length)
    return (
      <Empty className="mx-auto max-w-7xl border border-dashed bg-card">
        <EmptyHeader>
          <EmptyMedia variant="icon"><Bookmark /></EmptyMedia>
          <EmptyTitle>还没有收藏</EmptyTitle>
          <EmptyDescription>在机会卡片上点书签，就会出现在这里。之后可以拖动卡片记录申请进度。</EmptyDescription>
        </EmptyHeader>
      </Empty>
    )

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-4">
      <div className="flex flex-wrap items-center gap-2">
        <p className="mr-auto text-sm text-muted-foreground">拖动卡片记录进度。收藏与进度只保存在你的浏览器里。{gone > 0 && ` 另有 ${gone} 个收藏已截止或撤下。`}</p>
        <Button variant="outline" size="sm" disabled={!ex.length} onClick={() => download(`phdradar-saved-${iso(TODAY)}.ics`, icsCalendar(ex), "text/calendar;charset=utf-8")}>
          <CalendarPlus />导出截止到日历<Badge variant="secondary" className="font-mono">{ex.length}</Badge>
        </Button>
        <Button variant="outline" size="sm" onClick={() => download(`phdradar-saved-${iso(TODAY)}.json`, JSON.stringify({ saved, status, exported: iso(TODAY) }, null, 1), "application/json")}>
          <FileJson />下载收藏与进度
        </Button>
      </div>
      <DndContext sensors={sensors} onDragStart={(e) => setDrag(String(e.active.id))} onDragEnd={end} onDragCancel={() => setDrag(null)}>
        <ScrollArea className="w-full pb-3">
          <div className="flex gap-3">
            {STAGES.map(([k, t]) => <Column key={k} stage={k} title={t} items={list.filter((x) => stageOf(status, x.id).s === k)} labels={labels} onOpen={onOpen} />)}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
        <DragOverlay>{drag && byId.get(drag) ? <BoardCard x={byId.get(drag)!} labels={labels} overlay /> : null}</DragOverlay>
      </DndContext>
    </div>
  )
}
