import type { Metadata } from 'next'
import Link from 'next/link'
import ToolPage from '@/components/tools/ToolPage'
import { tools } from '@/data/tools.data'

export const metadata: Metadata = {
  title: 'AI Tools | uniAiverse',
  description: 'Free AI tools: readiness audit, use-case roadmap builder, AI risk classifier and automation ROI calculator.',
}

export default function ToolsPage() {
  return (
    <ToolPage
      icon="🧰"
      subtitle="Free AI Tools"
      title="Plan Your AI Journey"
      description="Assess readiness, prioritise use cases, check risk and size the savings — the same tools our consultants use, free to try."
      gradient="bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {tools.map((t) => (
          <Link
            key={t.slug}
            href={`/tools/${t.slug}`}
            className="group bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
          >
            <div className="text-5xl mb-4">{t.icon}</div>
            <div className="text-sm font-semibold text-primary mb-2">{t.subtitle}</div>
            <h2 className="text-2xl font-bold text-primary-dark mb-3">{t.title}</h2>
            <p className="text-primary-dark/70 leading-relaxed mb-6">{t.description}</p>
            <span className="text-primary font-semibold group-hover:text-primary-light">
              Open tool <span className="inline-block group-hover:translate-x-1 transition-transform duration-300">→</span>
            </span>
          </Link>
        ))}
      </div>
    </ToolPage>
  )
}
