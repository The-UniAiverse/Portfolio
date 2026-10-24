export interface Phase {
  phase: string
  title: string
  description: string
  icon: string
  color: string
}

export const aiJourneyPhases: Phase[] = [
  {
    phase: '01',
    title: 'Strategy',
    description: 'Define impact goals, use-cases, and roadmap',
    icon: '📋',
    color: 'from-primary to-primary-light',
  },
  {
    phase: '02',
    title: 'Build',
    description: 'Design & develop Gen AI/ML models',
    icon: '🔧',
    color: 'from-primary-light to-accent-blue',
  },
  {
    phase: '03',
    title: 'Deploy',
    description: 'Scalable MLOps & secure deployments',
    icon: '🚀',
    color: 'from-accent-blue to-primary',
  },
  {
    phase: '04',
    title: 'Upskill',
    description: 'Empower teams with AI training',
    icon: '🎓',
    color: 'from-primary to-primary-dark',
  },
]

export const aiJourneyPageData = {
  heading: {
    prefix: 'Your AI Journey in',
    highlight: '4 Phases',
  },
  subheading: 'A systematic approach to transform your AI vision into reality',
  cta: {
    text: 'Ready to start your AI transformation journey?',
    buttonText: 'Let\'s Begin',
    buttonHref: '#contact',
  },
}

