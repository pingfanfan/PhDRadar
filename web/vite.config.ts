import { resolve } from "node:path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// 构建产物写到仓库根目录：index.html（首页）与 app/*（脚本、样式、字体）；数据沿用根目录 assets/ 下由 build_site.py 生成的文件
export default defineConfig({
  base: "./",
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": resolve(import.meta.dirname, "./src") } },
  build: { outDir: "..", emptyOutDir: false, assetsDir: "app", chunkSizeWarningLimit: 900 },
})
