# PhDRadar 前端

React + Vite 单页应用，构建后就是网站首页（仓库根目录的 `index.html` 与 `app/`）。

```bash
cd web
npm ci
npm run dev     # 本地开发：需先在仓库根目录运行 python scripts/build_site.py 生成 assets/ 数据，再把根目录作为静态目录
npm run build   # 类型检查并构建，产物写到仓库根目录（会先清空 ../app）
```

统一用这些库，能用已有依赖表达的就不自己写组件和行为：

| 用途 | 库 |
|---|---|
| UI 组件与风格 | shadcn/ui（Nova 预设，Radix），组件源码在 `src/components/ui/` |
| 图标 | Lucide |
| 动画 | Motion（`MotionConfig reducedMotion="user"`） |
| 可拖动分栏 | react-resizable-panels（shadcn Resizable） |
| 拖拽 | dnd-kit（“我的申请”看板） |
| 状态 | Zustand（`src/store.ts`，收藏、进度、画像用 persist 存在浏览器本地） |

数据：`assets/catalog.json`、`assets/labels.json`、`assets/rank-rules.json` 与 `assets/rank.js`（推荐排序，与 `scripts/rank.py` 同一套规则）都由 `scripts/build_site.py` 生成，前端运行时读取，所以每天数据更新不需要重新构建前端。
