import { Bookmark } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import type { Labels, Row, Tone } from "@/lib/data"
import { useApp } from "@/store"

export const TONE: Record<Tone, string> = { urgent: "text-urgent", soon: "text-urgent", rolling: "text-foreground", "": "text-muted-foreground" }

// 机构那一行：机构 · 地区
export function OrgLine({ x, labels, className }: { x: Row; labels: Labels; className?: string }) {
  const region = (x.r || []).map((r) => labels.region[r] || r).join(" · ")
  return <span className={cn("min-w-0 truncate", className)}>{[x.org, region].filter(Boolean).join(" · ")}</span>
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
