export interface ToolInfo {
  slug: string
  icon: string
  title: string
  subtitle: string
  description: string
  gradient: string
}

// AI tools backed by the AI Services API (apps/api). One entry per backend service.
export const tools: ToolInfo[] = [
  {
    slug: 'job-finder',
    icon: '🎓',
    title: 'AI Job Finder',
    subtitle: 'Jobs for Every Career Stage',
    description: 'Search live jobs across India, from internships to leadership roles, see how well you fit each one, and get a tailored cover letter in minutes.',
    gradient: 'bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600',
  },
  {
    slug: 'readiness-audit',
    icon: '🔍',
    title: 'AI Readiness Audit',
    subtitle: 'Free Self-Assessment',
    description: 'Score your organisation across strategy, data, technology, people, process and governance — and get a prioritised 90-day roadmap with a downloadable report.',
    gradient: 'bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600',
  },
  {
    slug: 'roadmap',
    icon: '🗺️',
    title: 'AI Use-Case Roadmap Builder',
    subtitle: 'Strategy & Prioritisation',
    description: 'Rank your AI use cases by value, feasibility, risk and effort, and turn them into a phased 12-month roadmap.',
    gradient: 'bg-gradient-to-br from-indigo-900 via-blue-800 to-cyan-600',
  },
  {
    slug: 'governance',
    icon: '🛡️',
    title: 'AI Risk Classifier',
    subtitle: 'Governance, Safety & Compliance',
    description: 'Find the risk tier of an AI use case, EU AI Act style, and the controls it needs before it goes live.',
    gradient: 'bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-700',
  },
  {
    slug: 'automation-roi',
    icon: '⚙️',
    title: 'Automation ROI Calculator',
    subtitle: 'Automation & Workflow Optimisation',
    description: 'Estimate monthly savings, payback period and year-one ROI for the workflows you want to automate with AI.',
    gradient: 'bg-gradient-to-br from-cyan-900 via-blue-800 to-indigo-600',
  },
]

export const getToolBySlug = (slug: string) => tools.find((t) => t.slug === slug)
