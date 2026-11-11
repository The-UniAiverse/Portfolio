export interface Service {
    title: string
    description: string
    icon: string
    href?: string
    whatsIncluded?: string[]
    useCases?: string[]
    deliverables?: string | string[]
    capabilities?: string[]
    examples?: string[]
    idealFor?: string
    poweredBy?: string
    tools?: string
    duration?: string
}

export interface ServiceCategory {
    categoryTitle: string
    categoryIcon: string
    services: Service[]
}

// Core Services
export const coreServices: Service[] = [
    {
    title: 'Training and Mentorship',
    description: 'Corporate AI training catalogue: 25 courses in 10 tracks, from AI for every employee to GenAI and agentic AI engineering, plus a 3-month career cohort for individuals.',
    icon: '🥇',
    href: '/services/training',
    whatsIncluded: [
        'Tracks for every role: leaders, business, sales, marketing, engineers, data and risk teams',
        'Levels L1 awareness to L4 advanced',
        'Customised to your context before delivery',
        'Onsite in Pune & travel, or virtual',
        'Verified certificates'
    ],
    idealFor: 'Organisations building AI capability across teams, and professionals moving into AI engineering.'
},

    {
        title: 'AI Strategy & Roadmap Development',
        description: 'Turn AI from a buzzword into a clear plan. We assess your business processes, data, and opportunities to create a tailor-made, actionable AI roadmap.',
        icon: '🎯',
        whatsIncluded: [
            'AI readiness assessment',
            'Opportunity discovery workshop',
            'Tech & tools recommendation',
            '90-day implementation roadmap',
            'Cost & timeline estimate'
        ],
        idealFor: 'Founders, CXOs, and teams getting started with AI.'
    },
    {
        title: 'AI Automation & Workflow Optimization',
        description: 'Automate repetitive work. Improve speed. Reduce cost. We design and deploy automation systems that enhance productivity while maintaining high accuracy.',
        icon: '⚙️',
        useCases: [
            'Document processing automation',
            'Email & workflow automation',
            'CRM & Ops automation',
            'Support ticket routing',
            'Business process optimization'
        ],
        deliverables: 'End-to-end automation setup + SOPs + training.'
    },
    {
        title: 'AI Chatbots & Virtual Assistants',
        description: 'Smart chatbots that understand your business. We build custom chatbots that handle FAQs, customer queries, lead qualification, support, and internal knowledge.',
        icon: '💬',
        capabilities: [
            'Website chatbots',
            'WhatsApp/CRM bots',
            'Internal knowledge assistants',
            'Lead qualification AI agents',
            'Multilingual support'
        ],
        poweredBy: 'GPT-4/5 models, RAG systems, domain-specific datasets.'
    },
    {
        title: 'Custom LLM Integrations (GenAI Apps)',
        description: 'Bring ChatGPT-like intelligence into your tools and workflows. We integrate advanced large language models into your existing systems.',
        icon: '🤖',
        examples: [
            'AI-powered search',
            'Context-aware assistants',
            'Sales & support co-pilots',
            'RAG-based knowledge engines',
            'Smart document Q&A systems'
        ],
        deliverables: 'Design → Build → Deploy → Monitor'
    },
    {
        title: 'Data Engineering, Dashboards & Predictive Analytics',
        description: 'Make data useful. Make decisions faster. We clean, transform, and analyze your data to reveal insights and predict future outcomes.',
        icon: '📊',
        useCases: [
            'Sales forecasting',
            'Inventory optimization',
            'Customer churn prediction',
            'Market insights dashboards',
            'KPI monitoring'
        ],
        tools: 'Python, SQL, Power BI, BigQuery, Snowflake, etc.'
    }
]

// Advanced Services
export const advancedServices: Service[] = [
    {
        title: 'RAG (Retrieval-Augmented Generation) Systems',
        description: 'Your company\'s private, secure ChatGPT. We build domain-specific knowledge assistants that use your internal documents, SOPs, and systems.',
        icon: '🔍',
        whatsIncluded: [
            'Document ingestion pipeline',
            'Vector database setup',
            'Fine-tuning / prompt engineering',
            'Evaluation & accuracy testing'
        ],
        idealFor: 'Perfect for enterprises, support teams, operations, and compliance-heavy industries.'
    },
    {
        title: 'MLOps & Model Deployment',
        description: 'Make your AI models scalable, secure, and production-ready. We help you deploy, monitor, and improve AI models with modern MLOps practices.',
        icon: '🚀',
        whatsIncluded: [
            'CI/CD for AI models',
            'Monitoring & logging',
            'Cloud deployment (AWS/GCP/Azure)',
            'Model optimization'
        ]
    },
    {
        title: 'GenAI for Marketing, HR, Sales & Operations',
        description: 'AI tools that improve real business functions. We build GenAI systems tailored to your teams.',
        icon: '🎨',
        examples: [
            'Sales enablement AI assistant',
            'Content automation engine',
            'Recruitment screening AI',
            'HR chatbot',
            'Proposal & email generation systems'
        ]
    }
]

// Executive & Enterprise Services
export const enterpriseServices: Service[] = [
    {
        title: 'AI Transformation Consulting',
        description: 'End-to-end guidance to make your company AI-driven. We act as your fractional AI team — from strategy to implementation to training.',
        icon: '🏢',
        whatsIncluded: [
            'Vision & roadmap',
            'Pilot projects',
            'AI governance',
            'Tool selection',
            'Monthly advisory'
        ]
    },
    {
        title: 'AI Governance, Safety & Compliance',
        description: 'Responsible, secure, and compliant AI adoption. We help companies design safe AI workflows, especially in regulated domains.',
        icon: '🛡️',
        whatsIncluded: [
            'AI policy development',
            'Risk assessment',
            'Model audit',
            'Data privacy guidance',
            'Compliance documentation'
        ]
    }
]

// Productized Packages
export const productizedPackages: Service[] = [
    {
        title: 'AI Readiness Audit',
        description: 'Perfect for businesses unsure where to start.',
        icon: '🔬',
        duration: '7-Day Sprint',
        deliverables: 'AI opportunity map, System & process review, Quick wins, Final report + roadmap'
    },
    {
        title: 'AI in a Week',
        description: 'Implementation Package - What we deliver in 7 days.',
        icon: '⚡',
        duration: '7 Days',
        whatsIncluded: [
            '1 automation',
            '1 chatbot',
            '1 internal use-case',
            'Training for your team',
            'Deployment & documentation'
        ]
    },
    {
        title: 'Custom AI Chatbot Package',
        description: 'Complete chatbot solution with ongoing support.',
        icon: '💬',
        whatsIncluded: [
            'Setup & branding',
            'Knowledge ingestion',
            'Custom logic',
            'Website/WhatsApp integration',
            '30-day support'
        ]
    }
]

// All services combined for backward compatibility
export const servicesData: Service[] = [
    ...coreServices,
    ...advancedServices,
    ...enterpriseServices
]

// Service categories for organized display
export const serviceCategories: ServiceCategory[] = [
    {
        categoryTitle: 'Our Core Services',
        categoryIcon: '🚀',
        services: coreServices
    },
    {
        categoryTitle: 'Advanced Services',
        categoryIcon: '⚡',
        services: advancedServices
    },
    {
        categoryTitle: 'Executive & Enterprise Services',
        categoryIcon: '🏢',
        services: enterpriseServices
    },
    {
        categoryTitle: 'Productized Packages',
        categoryIcon: '🎁',
        services: productizedPackages
    }
]

export const servicesPageData = {
    heading: {
        prefix: 'Transform Your Business with Practical High-Impact',
        highlight: 'Artificial Intelligence',
        suffix: ' ',
    },
    subheading:
        'We help businesses unlock the real value of AI — from strategy to automation to custom AI solutions — with fast, measurable outcomes and zero complexity',
    cta: {
        heading: 'Redefine what\'s possible - put AI to work in your business.',
        buttonText: 'Get Started',
        buttonHref: '#contact',
    },
    whyWorkWithUs: {
        title: '🙌 Why Work With Us?',
        benefits: [
            'Practical, business-first approach',
            'Fast execution',
            'Clear communication',
            'Flexible engagement models',
            'Enterprise-quality at startup-friendly cost'
        ]
    }
}


// Homepage carousel: services grouped under the four core pillars (data/pillars.data.ts), in pillar order.
export interface ShowcaseService {
    pillar: 'strategy' | 'engineering' | 'training' | 'academy'
    title: string
    icon: string
    href: string
    blurb: string
    points: string[]
    gradient: string
}

export const serviceShowcase: ShowcaseService[] = [
    {
        pillar: 'strategy',
        title: 'AI Strategy & Roadmap',
        icon: '🎯',
        href: '/services/ai-strategy',
        blurb: 'Turn AI from a buzzword into a clear, actionable plan for your business.',
        points: ['AI maturity & high-value use cases', 'Feasibility and investment case', 'Adoption roadmap'],
        gradient: 'from-slate-900 via-blue-900 to-blue-600',
    },
    {
        pillar: 'strategy',
        title: 'AI Readiness Audit',
        icon: '🔬',
        href: '/tools/readiness-audit',
        blurb: 'Score your organisation across strategy, data, technology, people, process and governance.',
        points: ['Free self-assessment', 'Prioritised 90-day roadmap', 'Downloadable report'],
        gradient: 'from-indigo-950 via-blue-900 to-sky-600',
    },
    {
        pillar: 'engineering',
        title: 'AI Automation & Workflows',
        icon: '⚙️',
        href: '/services/ai-automation',
        blurb: 'Automate repetitive work, improve speed and reduce cost without losing accuracy.',
        points: ['Document processing', 'Email, CRM & ops automation', 'Support ticket routing'],
        gradient: 'from-indigo-900 via-blue-800 to-cyan-600',
    },
    {
        pillar: 'engineering',
        title: 'AI Chatbots & Assistants',
        icon: '💬',
        href: '/services/ai-chatbots',
        blurb: 'Assistants that understand your business: FAQs, support, lead qualification and internal knowledge.',
        points: ['Website & WhatsApp bots', 'Internal knowledge assistants', 'Multilingual support'],
        gradient: 'from-blue-900 via-blue-700 to-sky-500',
    },
    {
        pillar: 'engineering',
        title: 'Custom LLM Integrations',
        icon: '🤖',
        href: '/services/llm-integration',
        blurb: 'Bring large language models into the tools and workflows your teams already use.',
        points: ['AI-powered search', 'Sales & support co-pilots', 'Design → build → deploy → monitor'],
        gradient: 'from-purple-900 via-indigo-800 to-blue-600',
    },
    {
        pillar: 'engineering',
        title: 'RAG Systems',
        icon: '🔍',
        href: '/services/rag-systems',
        blurb: 'A private, secure assistant grounded in your own documents, SOPs and systems.',
        points: ['Document ingestion pipeline', 'Vector database setup', 'Evaluation & accuracy testing'],
        gradient: 'from-slate-900 via-indigo-900 to-violet-600',
    },
    {
        pillar: 'engineering',
        title: 'Agentic AI Systems',
        icon: '🧠',
        href: '/services/agentic-ai',
        blurb: 'Agents that use tools, follow rules and complete multi-step work reliably.',
        points: ['Tool use & integrations', 'Guardrails and evaluations', 'Production monitoring'],
        gradient: 'from-indigo-950 via-purple-800 to-fuchsia-600',
    },
    {
        pillar: 'engineering',
        title: 'Data Engineering & Analytics',
        icon: '📊',
        href: '/services/data-analytics',
        blurb: 'Clean, connected data and dashboards that reveal insights and predict outcomes.',
        points: ['Sales forecasting', 'Churn prediction', 'KPI dashboards'],
        gradient: 'from-blue-950 via-blue-800 to-teal-500',
    },
    {
        pillar: 'engineering',
        title: 'MLOps & Deployment',
        icon: '🚀',
        href: '/services/mlops',
        blurb: 'Make models scalable, secure and production-ready with modern MLOps practice.',
        points: ['CI/CD for AI models', 'Monitoring & logging', 'AWS, GCP or Azure'],
        gradient: 'from-slate-900 via-slate-700 to-blue-600',
    },
    {
        pillar: 'training',
        title: 'Corporate AI Training',
        icon: '🎓',
        href: '/services/training',
        blurb: 'Role-based learning: 25 courses across 10 tracks, from AI for every employee to agentic AI engineering.',
        points: ['Levels L1 awareness to L4 advanced', 'Customised to your context', 'Verified certificates'],
        gradient: 'from-blue-900 via-indigo-800 to-purple-600',
    },
    {
        pillar: 'training',
        title: 'Agentic AI & LLM Economics',
        icon: '🧩',
        href: '/services/training#workshop',
        blurb: 'A working workshop: build a grounded assistant and an agent on your own material, and learn what it costs.',
        points: ['1 or 2 days, onsite or virtual', 'Every lab: no-code + code path', 'Runnable demos'],
        gradient: 'from-slate-950 via-amber-900 to-amber-600',
    },
    {
        pillar: 'academy',
        title: 'GenAI & Agentic AI Engineer Cohort',
        icon: '🚀',
        href: '/services/training#track-individual',
        blurb: '12-week mentorship for professionals moving into AI engineering.',
        points: ['Capstone projects', 'Deployment & evaluation', 'Interview preparation'],
        gradient: 'from-indigo-950 via-violet-800 to-cyan-600',
    },
]
