import type { Metadata } from 'next'
import ToolPage from '@/components/tools/ToolPage'
import GovernanceTool from '@/components/tools/GovernanceTool'
import { getToolBySlug } from '@/data/tools.data'
import SignInGate from '@/components/auth/SignInGate'

const tool = getToolBySlug('governance')!

export const metadata: Metadata = {
  title: `${tool.title} | uniAiverse`,
  description: tool.description,
}

export default function GovernancePage() {
  return (
    <ToolPage icon={tool.icon} subtitle={tool.subtitle} title={tool.title} description={tool.description} gradient={tool.gradient}>
      <SignInGate what={`the ${tool.title}`}>
        <GovernanceTool />
      </SignInGate>
    </ToolPage>
  )
}
