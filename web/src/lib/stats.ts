// 访问统计：GoatCounter（https://www.goatcounter.com），不用 cookie、不记录 IP 以外的个人信息（IP 只用于去重、不保存）。
// 不加载第三方脚本，直接请求它的计数接口（/count，图片请求）。CODE 为空时什么都不发。
// 记三类数：打开首页（按 ?from= 记来源）、打开单个机会的完整页面、点「去官网申请」（事件，记岗位 id，不记是谁点的）。
const CODE = "pingfanfan" // GoatCounter 站点代码 → https://pingfanfan.goatcounter.com

function send(params: Record<string, string>) {
  if (!CODE || navigator.doNotTrack === "1") return
  const q = new URLSearchParams({ ...params, rnd: Math.random().toString(36).slice(2) })
  new Image().src = `https://${CODE}.goatcounter.com/count?${q}`
}

// 页面访问；?from=xhs 之类的渠道参数作为来源记下（GoatCounter 后台“来源”一栏）
export function countView(path: string) {
  const from = new URLSearchParams(location.search).get("from")
  send({ p: path, r: from ? `from:${from}` : document.referrer, s: `${screen.width},${screen.height}` })
}

// 事件：点「去官网申请」。名字里带岗位 id，后台能看出哪些岗位被点得最多
export function countApply(id: string) {
  send({ p: `apply/${id}`, t: "去官网申请", e: "true" })
}
