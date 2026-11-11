// The four core business pillars (source: uniAiVerse website strategy & content document).
// AI Readiness sits under pillar 01, Strategy & Consulting.

export interface Pillar {
  id: string
  number: string
  icon: string
  title: string
  verbs: [string, string, string]
  scope: string
  href: string
  cta: string
}

export const pillars: Pillar[] = [
  {
    id: 'strategy',
    number: '01',
    icon: '🧭',
    title: 'AI Strategy & Consulting',
    verbs: ['Assess', 'Prioritize', 'Strategize'],
    scope: 'AI maturity, high-value use cases, feasibility, investments and adoption roadmaps for CXOs, founders and business leaders.',
    href: '/services/ai-strategy',
    cta: 'Plan your AI strategy',
  },
  {
    id: 'engineering',
    number: '02',
    icon: '⚙️',
    title: 'AI Development & Engineering',
    verbs: ['Design', 'Build', 'Deploy'],
    scope: 'Custom AI apps, assistants, platforms, predictive systems and automation: GenAI, RAG, agents, ML/DL, MLOps and deployment.',
    href: '/services',
    cta: 'See what we build',
  },
  {
    id: 'training',
    number: '03',
    icon: '🎓',
    title: 'Corporate AI Training & Workshops',
    verbs: ['Upskill', 'Apply', 'Transform'],
    scope: 'Role-based learning: 25 courses across 10 tracks, tailored workshops, runnable demos, exercises and assessments.',
    href: '/services/training',
    cta: 'Browse the catalogue',
  },
  {
    id: 'academy',
    number: '04',
    icon: '🚀',
    title: 'AI Academy & Mentorship',
    verbs: ['Learn', 'Build', 'Grow'],
    scope: '12-week GenAI and Agentic AI mentorship with capstones, deployment, evaluation and interview preparation.',
    href: '/services/training#track-individual',
    cta: 'Join the cohort',
  },
]
