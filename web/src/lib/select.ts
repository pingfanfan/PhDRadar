// 数据集与筛选、推荐排序。推荐复用 assets/rank.js（与 scripts/rank.py 同一套规则，测试保证两边一致）。
import { useMemo } from "react"
import { create } from "zustand"
import { days, dlOf, isDate, isNow, iso, TODAY, type Labels, type Row } from "@/lib/data"
import { stageOf, useApp, type Profile, type StageRec } from "@/store"

export interface RankItem { id: string; score: number; reasons: string[]; hits: string[]; excluded: string[] }
export interface RankResult {
  ranked: RankItem[]; related: RankItem[]; excluded: RankItem[]; unrelated: number; considered: number
  disc?: string[]; kw_df?: [string, number, number][]
}
declare global {
  interface Window { PhDRank?: { rank: (rows: Row[], profile: unknown, rules: unknown, today: string) => RankResult } }
}

interface DataState { rows: Row[]; labels: Labels | null; byId: Map<string, Row>; rules: unknown; error: string }
export const useData = create<DataState>(() => ({ rows: [], labels: null, byId: new Map(), rules: null, error: "" }))

export const kwList = (s: string) => s.split(/[,，、;；\n]+/).map((k) => k.trim()).filter(Boolean).slice(0, 8)

function profileOf(f: Profile) {
  const lv = [f.phd && "phd", f.pd && "postdoc"].filter(Boolean)
  return {
    nationality: "CN", education: [{ degree: f.deg, status: "completed" }], research: { keywords: kwList(f.kw) },
    target: { levels: lv.length ? lv : ["phd"] },
    languages: { ielts: f.ielts ? +f.ielts : null, toefl: f.toefl ? +f.toefl : null, german: f.de || null },
    countries: { prefer: f.rg, accept: f.only ? f.rg : [] }, funding: { min_coverage: f.fund },
    deadline: { min_prep_days: f.prep }, eligibility: { cn_only: f.cn }, sensitive_field: f.sens,
  }
}
export const exportProfile = (f: Profile) => profileOf(f)

export function useRanking() {
  const { rows, rules } = useData()
  const profile = useApp((s) => s.profile)
  return useMemo(() => {
    if (!rules || !rows.length || !kwList(profile.kw).length || !window.PhDRank) return null
    const res = window.PhDRank.rank(rows, profileOf(profile), rules, iso(TODAY))
    return { res, by: new Map(res.ranked.concat(res.related).map((a) => [a.id, a])), hit: new Set(res.ranked.map((a) => a.id)) }
  }, [rows, rules, profile])
}
export type Ranking = NonNullable<ReturnType<typeof useRanking>>

export function useFiltered(ignoreDay = false) {
  const { rows } = useData()
  const { view, q, region, disc, flags, day, saved } = useApp()
  return useMemo(() => {
    const qq = q.trim().toLowerCase(), f = new Set(flags)
    const out = rows.filter((x) => {
      if (!ignoreDay && day && dlOf(x) !== day) return false
      if (view === "saved") { if (!saved[x.id]) return false }
      else if (view === "now" && !isNow(x)) return false
      else if (view === "ver" && !x.v) return false
      if (f.has("cn") && x.e !== "yes") return false
      const lv = x.l || []
      if (f.has("phd") !== f.has("pd") && !lv.includes(f.has("phd") ? "phd" : "postdoc")) return false
      if (f.has("full") && !["full", "salary"].includes(x.c || "")) return false
      if (f.has("soon")) { const d = dlOf(x); if (!isDate(d) || days(d!) < 0 || days(d!) > 30) return false }
      if (region && !(x.r || []).includes(region)) return false
      if (disc && !(x.d || []).includes(disc)) return false
      if (qq && !x._hay.includes(qq)) return false
      return true
    })
    const key = (x: Row) => { const d = dlOf(x); return isDate(d) && days(d!) >= 0 ? d! : d === "rolling" ? "9998" : "9999" }
    return out.sort((a, b) => (key(a) < key(b) ? -1 : key(a) > key(b) ? 1 : a.n.localeCompare(b.n, "zh")))
  }, [rows, view, q, region, disc, flags, day, saved, ignoreDay])
}

// 准备清单：材料取自公告原文摘出的材料清单；公告没列时给常见材料
export function prepItems(x: Row) {
  const docs = x.af?.dc ? x.af.dc[0].split(/[、，,；;]/).map((t) => t.trim()).filter(Boolean) : []
  const base = docs.length ? docs.map((d) => "准备" + d) : ["准备简历 CV", "准备成绩单与学位证明", "准备动机信 / 个人陈述"]
  return { fromPost: docs.length > 0, items: [...base, "联系推荐人，告知截止日期", "确认截止时刻与时区", "（可选）给导师发套磁信"] }
}

export const exportable = (rows: Row[], saved: Record<string, 1>, status: Record<string, StageRec>) =>
  rows.filter((x) => saved[x.id] && stageOf(status, x.id).s !== "result" && isDate(dlOf(x)) && days(dlOf(x)!) >= 0)
