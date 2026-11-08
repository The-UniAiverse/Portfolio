import type { Metadata } from 'next'
import ToolPage from '@/components/tools/ToolPage'
import RoadmapTool from '@/components/tools/RoadmapTool'
import { getToolBySlug } from '@/data/tools.data'
import SignInGate from '@/components/auth/SignInGate'

const tool = getToolBySlug('roadmap')!

export const metadata: Metadata = {
  title: `${tool.title} | uniAiverse`,
  description: tool.description,
}

export default function RoadmapPage() {
  return (
    <ToolPage icon={tool.icon} subtitle={tool.subtitle} title={tool.title} description={tool.description} gradient={tool.gradient}>
      <SignInGate what={`the ${tool.title}`}>
        <RoadmapTool />
      </SignInGate>
    </ToolPage>
  )
}
