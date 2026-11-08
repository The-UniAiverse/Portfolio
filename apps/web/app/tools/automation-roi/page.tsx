import type { Metadata } from 'next'
import ToolPage from '@/components/tools/ToolPage'
import AutomationROITool from '@/components/tools/AutomationROITool'
import { getToolBySlug } from '@/data/tools.data'
import SignInGate from '@/components/auth/SignInGate'

const tool = getToolBySlug('automation-roi')!

export const metadata: Metadata = {
  title: `${tool.title} | uniAiverse`,
  description: tool.description,
}

export default function AutomationROIPage() {
  return (
    <ToolPage icon={tool.icon} subtitle={tool.subtitle} title={tool.title} description={tool.description} gradient={tool.gradient}>
      <SignInGate what={`the ${tool.title}`}>
        <AutomationROITool />
      </SignInGate>
    </ToolPage>
  )
}
