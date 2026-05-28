export interface NavLink {
  href: string
  label: string
}

export interface ServiceLink {
  icon: string
  title: string
  href: string
}

export const navLinks: NavLink[] = [
  { href: '/', label: 'Home' },
  { href: '/#about', label: 'About' },
  { href: '/services', label: 'Services' },
  { href: '/blog', label: 'Blog' },
  { href: '/#contact', label: 'Contact' },
]

export const serviceLinks: ServiceLink[] = [
  // Core Services
  { icon: '🎯', title: 'AI Strategy & Roadmap', href: '/services/ai-strategy' },
  { icon: '⚙️', title: 'AI Automation & Workflows', href: '/services/ai-automation' },
  { icon: '💬', title: 'AI Chatbots & Assistants', href: '/services/ai-chatbots' },
  { icon: '🤖', title: 'Custom LLM Integrations', href: '/services/llm-integration' },
  { icon: '📊', title: 'Data Engineering & Analytics', href: '/services/data-analytics' },
  { icon: '🔍', title: 'RAG Systems', href: '/services/rag-systems' },
  
  // Advanced Services
  { icon: '🚀', title: 'MLOps & Deployment', href: '/services/mlops' },
  { icon: '🎨', title: 'GenAI for Business', href: '/services/genai-business' },
  { icon: '🎨', title: 'Generative AI Development', href: '/services/generative-ai' },
  { icon: '🤖', title: 'AI & Machine Learning', href: '/services/ai-ml' },
  { icon: '🧠', title: 'Agentic AI Systems', href: '/services/agentic-ai' },
  { icon: '💬', title: 'Natural Language Processing', href: '/services/nlp' },
  { icon: '📊', title: 'Data Science', href: '/services/data-science' },
  { icon: '👁️', title: 'Computer Vision', href: '/services/computer-vision' },
  { icon: '📚', title: 'Training & Mentorship', href: '/services/training' },
]

