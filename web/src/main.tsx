import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { MotionConfig } from "motion/react"

import "./index.css"
import App from "./App.tsx"
import { ThemeProvider } from "@/components/theme-provider.tsx"
import { Toaster } from "@/components/ui/sonner"
import { TooltipProvider } from "@/components/ui/tooltip"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider defaultTheme="system" storageKey="phdradar-theme">
      <MotionConfig reducedMotion="user">
        <TooltipProvider delayDuration={300}>
          <App />
          <Toaster position="bottom-center" />
        </TooltipProvider>
      </MotionConfig>
    </ThemeProvider>
  </StrictMode>
)
