import { CalendarPlus, CircleCheck, Clock, ExternalLink, MousePointerClick, Sparkles, TriangleAlert } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { cn } from "@/lib/utils"
import { AF_LABELS, days, dlOf, download, due, icsCalendar, isDate, isNow, shortPay, screened, type Row } from "@/lib/data"
import { prepItems, useData, type Ranking } from "@/lib/select"
import { RESULTS, STAGES, stageOf, useApp, type Result, type Stage } from "@/store"
import { OrgLine, SaveButton, TONE } from "@/components/opportunity-list"

const REPO = "https://github.com/pingfanfan/PhDRadar"

function Section({ title, children, extra }: { title: string; children: React.ReactNode; extra?: React.ReactNode }) {
  return (
    <section className="flex flex-col gap-2.5">
      <h3 className="flex items-baseline gap-2 text-xs font-medium tracking-wide text-muted-foreground">{title}{extra}</h3>
      {children}
    </section>
  )
}

export function StageControl({ id }: { id: string }) {
  const { status, setStage } = useApp()
  const v = stageOf(status, id)
  return (
    <div className="flex flex-col gap-2">
      <ToggleGroup type="single" variant="outline" size="sm" value={v.s} onValueChange={(s) => s && setStage(id, s as Stage)} className="w-full">
        {STAGES.map(([k, t]) => <ToggleGroupItem key={k} value={k} className="flex-1">{t}</ToggleGroupItem>)}
      </ToggleGroup>
      {v.s === "result" && (
        <ToggleGroup type="single" variant="outline" size="sm" value={v.r || ""} onValueChange={(r) => r && setStage(id, "result", r as Result)} className="w-full max-w-xs">
          {RESULTS.map(([k, t]) => <ToggleGroupItem key={k} value={k} className="flex-1">{t}</ToggleGroupItem>)}
        </ToggleGroup>
      )}
    </div>
  )
}

function PrepList({ x }: { x: Row }) {
  const { status, toggleCheck } = useApp()
  const { fromPost, items } = prepItems(x)
  const c = status[x.id]?.c || {}
  const done = items.filter((_, i) => c[i]).length
  return (
    <Section title="准备清单" extra={<span className="font-mono">{done} / {items.length}</span>}>
      <div className="flex flex-col divide-y rounded-lg border">
        {items.map((t, i) => (
          <Label key={i} className="flex cursor-pointer items-start gap-3 px-3 py-2.5 font-normal">
            <Checkbox checked={!!c[i]} onCheckedChange={() => toggleCheck(x.id, i)} className="mt-0.5" />
            <span className={cn("text-sm", c[i] && "text-muted-foreground line-through")}>{t}</span>
          </Label>
        ))}
      </div>
      <p className="text-xs text-muted-foreground">{fromPost ? "材料摘自公告原文" : "公告里没摘到材料清单，以上是常见材料"}，提交前请再读一遍官网要求。勾选只保存在你的浏览器里。</p>
    </Section>
  )
}

export function DetailPanel({ x, rank }: { x?: Row; rank?: Ranking | null }) {
  const labels = useData((s) => s.labels)!
  const { saved, status } = useApp()
  if (!x)
    return (
      <Empty className="h-full">
        <EmptyHeader>
          <EmptyMedia variant="icon"><MousePointerClick /></EmptyMedia>
          <EmptyTitle>选一个机会</EmptyTitle>
          <EmptyDescription>这里会显示资助、截止、申请须知和官网原句。</EmptyDescription>
        </EmptyHeader>
      </Empty>
    )
  const [dt, tone] = due(x, labels), now = isNow(x), d = dlOf(x)
  const quote = now ? x.o!.q : x.pq, checked = now ? x.o!.ck : x.vd
  const what = now ? (x.o!.st === "upcoming" ? "确认即将开放" : "确认今天仍可申请") : "核对过官网正文"
  const sp = shortPay(x, labels), fullPay = x.s && x.s.trim() !== sp ? x.s : ""
  const facts: [string, string, string?][] = [
    ["资助", labels.coverage[x.c || ""] || "官网未写明"], ["金额", x.s ? sp || "见官网原文" : "官网未写明", fullPay],
    ["截止", d === "rolling" ? "滚动招生" : isDate(d) ? d! : labels.deadline[d || ""] || "官网未写明"],
    ["层次", (x.l || ["phd"]).map((l) => labels.level[l] || l).join(" / ")],
    ["地区", (x.r || []).map((r) => labels.region[r] || r).join(" · ") || "—"],
    ["中国学生", (labels.cn[x.e || "check"] || labels.cn.check)[0]], ...(x.lt ? [["语言", x.lt] as [string, string]] : []),
  ]
  const af = AF_LABELS.filter(([k]) => x.af?.[k])
  const rq = af.length && x.rq ? x.rq.split("；").filter((t) => !/^(学位要求|工作语言|开始时间)：/.test(t)).join("；") : x.rq
  const notes = [rq, x.dn].filter(Boolean) as string[]
  const st = stageOf(status, x.id), isSaved = !!saved[x.id]
  const a = rank?.by.get(x.id)
  const disc = (x.d || []).filter((k) => k !== "all").map((k) => labels.discipline[k] || k)

  return (
    <article className="flex flex-col">
      <header className="flex flex-col gap-4 p-6 pb-5">
        <div className="flex min-w-0 flex-col gap-2">
          <OrgLine x={x} labels={labels} className="text-sm text-muted-foreground" />
          <h2 className="text-xl leading-snug font-semibold tracking-tight text-balance md:text-2xl">{x.n}</h2>
          {disc.length > 0 && <div className="flex flex-wrap gap-1.5">{disc.map((t) => <Badge key={t} variant="secondary" className="rounded-md font-normal">{t}</Badge>)}</div>}
        </div>
        {x.in && <p className="text-[15px] leading-relaxed text-foreground/85">{x.in}</p>}
        <div className="sticky bottom-0 z-10 -mx-6 flex flex-wrap items-center gap-2 border-t bg-background/95 px-6 py-3 backdrop-blur md:static md:mx-0 md:border-0 md:bg-transparent md:p-0 md:backdrop-blur-none">
          <Button size="lg" asChild className="flex-1 md:flex-none"><a href={x.u} target="_blank" rel="noopener">去官网申请<ExternalLink /></a></Button>
          <SaveButton id={x.id} withText />
          {isDate(d) && days(d!) >= 0 && (
            <Button variant="outline" size="lg" onClick={() => download(`phdradar-${d}.ics`, icsCalendar([x]), "text/calendar;charset=utf-8")} title="截止前 14 天、7 天和 1 天提醒">
              <CalendarPlus /><span className="hidden sm:inline">加入日历</span>
            </Button>
          )}
          <span className={cn("ml-auto hidden items-center gap-1.5 text-sm font-medium md:inline-flex", TONE[tone])}><Clock className="size-4" />{dt}</span>
        </div>
        {isSaved && (
          <div className="flex flex-col gap-2">
            <p className="text-xs text-muted-foreground">申请进度{st.t && <span className="ml-2 font-mono">{st.t} 更新</span>}</p>
            <StageControl id={x.id} />
          </div>
        )}
      </header>
      <Separator />
      <dl className="grid grid-cols-2 gap-px bg-border md:grid-cols-3">
        {facts.map(([k, v, more]) => (
          <div key={k} className="flex min-w-0 flex-col gap-0.5 bg-background px-6 py-3">
            <dt className="text-xs text-muted-foreground">{k}</dt>
            <dd className="text-sm font-medium break-words">{v}</dd>
            {more && <dd className="text-xs leading-relaxed text-muted-foreground break-words">{more}</dd>}
          </div>
        ))}
      </dl>
      <Separator />
      <div className="flex flex-col gap-6 p-6">
        {isSaved && ["want", "prep"].includes(st.s) && <PrepList x={x} />}
        {quote && (
          <Section title="官网原句">
            <figure className="flex gap-3 rounded-lg bg-primary/8 p-4">
              <CircleCheck className="mt-0.5 size-4 shrink-0 text-primary" />
              <div className="min-w-0">
                <blockquote className="font-mono text-[13px] leading-relaxed break-words">{quote}</blockquote>
                <figcaption className="mt-1.5 text-xs text-muted-foreground">{checked} 打开{x.via ? ` ${x.via} 公告` : "官网"}{what}</figcaption>
              </div>
            </figure>
          </Section>
        )}
        {a && (
          <Section title={`为什么推荐 · 匹配 ${a.score}`}>
            <div className="flex flex-col gap-1.5 text-sm">{a.reasons.map((r, i) => <p key={i} className={i ? "text-muted-foreground" : ""}>{i === 0 && <Sparkles className="mr-1 inline size-3.5 text-primary" />}{r}</p>)}</div>
            <p className="text-xs text-muted-foreground">按关键词与条件自动排序，可能有字面巧合；投递前请读官网原文确认方向与资格。</p>
          </Section>
        )}
        {screened(x) && (
          <Alert variant="destructive">
            <TriangleAlert />
            <AlertTitle>留意安全审查</AlertTitle>
            <AlertDescription>公告原文提到出口管制、ATAS 或知识安全审查等要求。中国大陆学生可能需要额外审查，部分方向可能受限，投递前请先读原文确认。</AlertDescription>
          </Alert>
        )}
        {(af.length > 0 || notes.length > 0) && (
          <Section title="申请须知">
            {af.length > 0 && (
              <Accordion type="multiple" className="rounded-lg border px-4">
                {af.map(([k, label]) => (
                  <AccordionItem key={k} value={k}>
                    <AccordionTrigger className="gap-3 hover:no-underline">
                      <span className="flex min-w-0 flex-col gap-0.5 text-left sm:flex-row sm:gap-3">
                        <span className="w-16 shrink-0 text-xs text-muted-foreground sm:pt-0.5">{label}</span>
                        <span className="font-normal">{x.af![k]![0]}</span>
                      </span>
                    </AccordionTrigger>
                    <AccordionContent>
                      <blockquote className="rounded-md bg-muted px-3 py-2 font-mono text-xs leading-relaxed break-words">{x.af![k]![1]}</blockquote>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            )}
            {notes.map((n, i) => <p key={i} className="text-sm text-foreground/85">{n}</p>)}
            {af.length > 0 && <p className="text-xs text-muted-foreground">由程序从公告原文摘录，展开可看原句；没列出的项目公告里没写，请以官网为准。</p>}
          </Section>
        )}
        <p className="text-xs leading-relaxed text-muted-foreground">
          {x.al && <>同一岗位也发布在：{x.al.map((u, i) => <span key={u}>{i > 0 && "、"}<a className="underline underline-offset-2" href={u} target="_blank" rel="noopener">{new URL(u).hostname.replace(/^www\./, "")}</a></span>)}。</>}
          {x.via && `岗位来自 ${x.via}，截止日期由程序从公告原文提取。`}信息以官网为准，截止时间注意时区。发现错误？<a className="underline underline-offset-2" href={`${REPO}/issues`}>告诉我们</a>
        </p>
      </div>
    </article>
  )
}
