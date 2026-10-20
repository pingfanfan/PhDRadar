// 为我推荐：画像只存在浏览器里；排序规则与 /rank 相同（assets/rank.js + assets/rank-rules.json）
import { useMemo } from "react"
import { FileDown, Lock, RotateCcw, Sparkles } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { download, isNow, iso, TODAY } from "@/lib/data"
import { exportProfile, useData, type Ranking } from "@/lib/select"
import { useApp, type Profile } from "@/store"

function Pick({ id, label, value, onChange, options }: { id: string; label: string; value: string; onChange: (v: string) => void; options: [string, string][] }) {
  return (
    <Field>
      <FieldLabel htmlFor={id}>{label}</FieldLabel>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger id={id} className="w-full"><SelectValue /></SelectTrigger>
        <SelectContent>{options.map(([v, t]) => <SelectItem key={v} value={v}>{t}</SelectItem>)}</SelectContent>
      </Select>
    </Field>
  )
}

function Check({ id, label, checked, onChange }: { id: string; label: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <Field orientation="horizontal" className="w-auto">
      <Checkbox id={id} checked={checked} onCheckedChange={(v) => onChange(v === true)} />
      <FieldLabel htmlFor={id} className="font-normal">{label}</FieldLabel>
    </Field>
  )
}

// 导出 profile.yml（JSON 字符串本身就是合法的 YAML 标量），只在本机生成
function toYaml(v: unknown, ind = ""): string {
  if (Array.isArray(v)) return v.length ? v.map((x) => `\n${ind}- ${toYaml(x, ind + "  ")}`).join("") : " []"
  if (v && typeof v === "object")
    return Object.entries(v).map(([k, w]) => `\n${ind}${k}:${w && typeof w === "object" ? "" : " "}${toYaml(w, ind + "  ")}`).join("")
  return v === null || v === undefined ? "null" : typeof v === "string" ? JSON.stringify(v) : String(v)
}

export function RecommendForm({ rank }: { rank: Ranking | null }) {
  const { profile: p, setProfile, clearProfile } = useApp()
  const { rows, labels } = useData()
  const regions = useMemo(() => {
    const rc: Record<string, number> = {}
    rows.filter(isNow).forEach((x) => (x.r || []).forEach((r) => (rc[r] = (rc[r] || 0) + 1)))
    return Object.entries(rc).sort((a, b) => b[1] - a[1]).slice(0, 18).map(([k]) => k)
  }, [rows])
  const up = (patch: Partial<Profile>) => setProfile(patch)
  if (!labels) return null
  const r = rank?.res

  return (
    <section className="mx-auto max-w-7xl px-4 pt-8 pb-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg"><Sparkles className="size-5 text-primary" />为我推荐</CardTitle>
          <CardDescription className="flex items-center gap-1.5"><Lock className="size-3.5" />填几项条件，按研究方向的匹配度排序，每条写明命中了什么。画像只存在你的浏览器里。</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-5">
          <Field>
            <FieldLabel htmlFor="rp-kw">研究方向关键词（中英文都可，用逗号或顿号分开，3–6 个最好）</FieldLabel>
            <Input id="rp-kw" className="h-11 text-base" value={p.kw} onChange={(e) => up({ kw: e.target.value })} placeholder="如：医学影像、深度学习、MRI" />
          </Field>
          <Accordion type="single" collapsible defaultValue="more">
            <AccordionItem value="more" className="border-0">
              <AccordionTrigger className="py-0 text-primary hover:no-underline">更多条件</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-5 pt-4">
                <FieldGroup className="grid grid-cols-2 gap-4 md:grid-cols-4">
                  <Field>
                    <FieldLabel>层次</FieldLabel>
                    <div className="flex h-9 items-center gap-4">
                      <Check id="rp-phd" label="博士" checked={p.phd} onChange={(v) => up({ phd: v })} />
                      <Check id="rp-pd" label="博后" checked={p.pd} onChange={(v) => up({ pd: v })} />
                    </div>
                  </Field>
                  <Pick id="rp-deg" label="入学前的最高学历" value={p.deg} onChange={(v) => up({ deg: v })} options={[["bachelor", "本科"], ["master", "硕士"], ["phd", "博士"]]} />
                  <Pick id="rp-fund" label="最低资助" value={p.fund} onChange={(v) => up({ fund: v })} options={[["any", "不限"], ["partial", "至少部分资助"], ["full", "全奖 / 带薪"], ["confirmed", "写明全奖 / 带薪"]]} />
                  <Pick id="rp-prep" label="截止至少还有" value={String(p.prep)} onChange={(v) => up({ prep: +v })} options={[["7", "7 天"], ["14", "14 天"], ["30", "30 天"], ["60", "60 天"]]} />
                  <Field><FieldLabel htmlFor="rp-ielts">雅思总分</FieldLabel><Input id="rp-ielts" type="number" step={0.5} min={0} max={9} inputMode="decimal" value={p.ielts} onChange={(e) => up({ ielts: e.target.value })} placeholder="没有就留空" /></Field>
                  <Field><FieldLabel htmlFor="rp-toefl">托福总分</FieldLabel><Input id="rp-toefl" type="number" step={1} min={0} max={120} inputMode="numeric" value={p.toefl} onChange={(e) => up({ toefl: e.target.value })} placeholder="没有就留空" /></Field>
                  <Pick id="rp-de" label="德语" value={p.de || "none"} onChange={(v) => up({ de: v === "none" ? "" : v })} options={[["none", "不会 / B2 以下"], ["B2", "B2 及以上"]]} />
                </FieldGroup>
                <Field>
                  <FieldLabel>国家偏好（可多选；选了的排前面）</FieldLabel>
                  <ToggleGroup type="multiple" variant="outline" size="sm" spacing={2} value={p.rg} onValueChange={(v) => up({ rg: v })} className="flex-wrap justify-start">
                    {regions.map((k) => <ToggleGroupItem key={k} value={k} className="rounded-full px-3 data-[state=on]:border-primary data-[state=on]:bg-primary/10 data-[state=on]:text-primary">{labels.region[k] || k}</ToggleGroupItem>)}
                  </ToggleGroup>
                </Field>
                <div className="flex flex-wrap items-center gap-x-5 gap-y-3">
                  <Check id="rp-only" label="只看所选国家" checked={p.only} onChange={(v) => up({ only: v })} />
                  <Check id="rp-cn" label="只看官网写明中国学生可申的" checked={p.cn} onChange={(v) => up({ cn: v })} />
                  <Check id="rp-sens" label="方向可能涉及出口管制 / 安全审查" checked={p.sens} onChange={(v) => up({ sens: v })} />
                  <div className="ml-auto flex gap-2">
                    <Button variant="outline" size="sm" title="放进 fork 的仓库，用 Claude Code 的 /rank 做更细的排序"
                      onClick={() => download("profile.yml", `# PhDRadar“为我推荐”导出的画像（${iso(TODAY)}）。放进仓库根目录后运行 /setup 补全，再运行 /rank。\n${toYaml(exportProfile(p)).replace(/^\n/, "")}\n`, "text/yaml;charset=utf-8")}>
                      <FileDown />下载为 profile.yml
                    </Button>
                    <Button variant="ghost" size="sm" onClick={clearProfile}><RotateCcw />清除画像</Button>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
          {r && (
            <p className="rounded-lg bg-muted px-4 py-3 text-sm leading-relaxed text-muted-foreground">
              现在可申请的 <b className="font-mono text-foreground">{r.considered.toLocaleString()}</b> 条里：命中你关键词的 <b className="font-mono text-foreground">{r.ranked.length}</b> 条，
              学科相同但没命中关键词的 <b className="font-mono text-foreground">{r.related.length}</b> 条，被你的条件排除 <b className="font-mono text-foreground">{r.excluded.length.toLocaleString()}</b> 条。
              {r.disc?.length ? ` 识别出的学科：${r.disc.map((d) => labels.discipline[d] || d).join("、")}。` : ""}资格写“待核实”的，投递前请自己读官网确认。
            </p>
          )}
        </CardContent>
      </Card>
    </section>
  )
}
