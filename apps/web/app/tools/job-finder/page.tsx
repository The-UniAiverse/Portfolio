import type { Metadata } from 'next'
import ToolPage from '@/components/tools/ToolPage'
import JobFinderTool from '@/components/tools/jobs/JobFinderTool'
import { getToolBySlug } from '@/data/tools.data'

const tool = getToolBySlug('job-finder')!

export const metadata: Metadata = {
  title: `${tool.title} | uniAiverse`,
  description: tool.description,
}

export default function JobFinderPage() {
  return (
    <ToolPage icon={tool.icon} subtitle={tool.subtitle} title={tool.title} description={tool.description} gradient={tool.gradient}>
      <JobFinderTool />
    </ToolPage>
  )
}
