// 全站状态（Zustand）。收藏、申请进度、画像存在浏览器本地（persist），不上传。
import { create } from "zustand"
import { createJSONStorage, persist } from "zustand/middleware"
import { iso } from "@/lib/data"

export type View = "now" | "rec" | "ver" | "saved"
export type Stage = "want" | "prep" | "sent" | "interview" | "result"
export type Result = "offer" | "reject" | "withdraw"
export type Flag = "cn" | "full" | "soon" | "phd" | "pd"

export const STAGES: [Stage, string][] = [["want", "想投"], ["prep", "准备中"], ["sent", "已投"], ["interview", "面试"], ["result", "结果"]]
export const RESULTS: [Result, string][] = [["offer", "录取"], ["reject", "未录取"], ["withdraw", "放弃"]]

export interface StageRec { s: Stage; r?: Result; t?: string; c?: Record<string, 1> }
export interface Profile {
  kw: string; phd: boolean; pd: boolean; deg: string; fund: string; prep: number
  ielts: string; toefl: string; de: string; only: boolean; cn: boolean; sens: boolean; rg: string[]
}
export const EMPTY_PROFILE: Profile = {
  kw: "", phd: true, pd: false, deg: "master", fund: "full", prep: 14, ielts: "", toefl: "", de: "", only: false, cn: false, sens: false, rg: [],
}

interface State {
  view: View
  q: string
  region: string
  disc: string
  flags: Flag[]
  day: string
  sel: string
  shown: number
  saved: Record<string, 1>
  status: Record<string, StageRec>
  profile: Profile
  setView: (v: View) => void
  set: (p: Partial<Pick<State, "q" | "region" | "disc" | "flags" | "day">>) => void
  select: (id: string) => void
  more: () => void
  toggleSave: (id: string) => boolean
  setStage: (id: string, s: Stage, r?: Result) => void
  toggleCheck: (id: string, i: number) => void
  setProfile: (p: Partial<Profile>) => void
  clearProfile: () => void
}

export const PAGE = 40
const today = () => iso(new Date())

// 旧版页面存在这几个键里，第一次打开新版时搬过来
function legacy<T>(key: string, fallback: T): T {
  try {
    const v = JSON.parse(localStorage.getItem(key) || "null")
    return v && typeof v === "object" ? { ...fallback, ...v } : fallback
  } catch {
    return fallback
  }
}

export const useApp = create<State>()(
  persist(
    (set, get) => ({
      view: "now",
      q: "",
      region: "",
      disc: "",
      flags: [],
      day: "",
      sel: "",
      shown: PAGE,
      saved: legacy<Record<string, 1>>("phdradar-saved", {}),
      status: legacy<Record<string, StageRec>>("phdradar-status", {}),
      profile: legacy<Profile>("phdradar-profile", EMPTY_PROFILE),
      setView: (view) => set({ view, shown: PAGE, day: "" }),
      set: (p) => set({ ...p, shown: PAGE }),
      select: (sel) => set({ sel }),
      more: () => set({ shown: get().shown + PAGE }),
      toggleSave: (id) => {
        const saved = { ...get().saved }, status = { ...get().status }
        const on = !saved[id]
        if (on) { saved[id] = 1; status[id] = { s: "want", t: today() } } else { delete saved[id]; delete status[id] }
        set({ saved, status })
        return on
      },
      setStage: (id, s, r) => {
        const prev = get().status[id]
        const v: StageRec = { s, t: today(), c: prev?.c }
        if (s === "result") { const r0 = r || (prev?.s === "result" ? prev.r : undefined); if (r0) v.r = r0 }
        set({ status: { ...get().status, [id]: v } })
      },
      toggleCheck: (id, i) => {
        const prev = get().status[id] || { s: "want" as Stage }
        const c = { ...(prev.c || {}) }
        if (c[i]) delete c[i]; else c[i] = 1
        const s: Stage = prev.s === "want" && c[i] ? "prep" : prev.s  // 开始勾选 = 进入准备中
        set({ status: { ...get().status, [id]: { ...prev, s, c, t: today() } } })
      },
      setProfile: (p) => set({ profile: { ...get().profile, ...p } }),
      clearProfile: () => set({ profile: EMPTY_PROFILE }),
    }),
    {
      name: "phdradar-app",
      storage: createJSONStorage(() => localStorage),
      partialize: (s) => ({ saved: s.saved, status: s.status, profile: s.profile, view: s.view === "saved" ? "now" : s.view }),
    },
  ),
)

export const stageOf = (status: Record<string, StageRec>, id: string): StageRec => {
  const v = status[id]
  return v && STAGES.some(([k]) => k === v.s) ? v : { s: "want" }
}
export const stageText = (v: StageRec) =>
  v.s === "result" && v.r ? RESULTS.find(([k]) => k === v.r)![1] : STAGES.find(([k]) => k === v.s)![1]
