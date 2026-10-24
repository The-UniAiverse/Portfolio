export interface ServicePageData {
    slug: string
    icon: string
    subtitle: string
    title: string
    description: string
    gradient: string
    mainDescription: string
    features: {
        icon: string
        title: string
        description: string
    }[]
    technologies: string[]
    benefits: {
        icon: string
        title: string
        description: string
    }[]
    useCases?: {
        title: string
        description: string
    }[]
    deliverables?: string[]
}

export const servicePages: ServicePageData[] = [
    {
        slug: 'ai-strategy',
        icon: '🎯',
        subtitle: 'Strategic AI Planning',
        title: 'AI Strategy & Roadmap Development',
        description: 'Turn AI from a buzzword into a clear plan. We assess your business processes, data, and opportunities to create a tailor-made, actionable AI roadmap.',
        gradient: 'bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600',
        mainDescription: 'Get a comprehensive AI strategy that aligns with your business goals and delivers measurable ROI.',
        features: [
            {
                icon: '🔍',
                title: 'AI Readiness Assessment',
                description: 'Evaluate your current infrastructure, data maturity, and team capabilities to identify AI opportunities.'
            },
            {
                icon: '💡',
                title: 'Opportunity Discovery',
                description: 'Interactive workshops to uncover high-impact use cases specific to your business challenges.'
            },
            {
                icon: '🗺️',
                title: '90-Day Roadmap',
                description: 'Detailed implementation plan with milestones, timelines, and resource requirements.'
            }
        ],
        technologies: ['Strategic Planning', 'Business Analysis', 'AI Assessment Tools', 'ROI Modeling', 'Change Management'],
        benefits: [
            {
                icon: '⚡',
                title: 'Clear Direction',
                description: 'Know exactly where to start and what to prioritize'
            },
            {
                icon: '💰',
                title: 'Cost Clarity',
                description: 'Understand investment requirements and expected returns'
            },
            {
                icon: '🎯',
                title: 'Risk Mitigation',
                description: 'Identify and address potential challenges early'
            }
        ],
        deliverables: [
            'AI Readiness Assessment Report',
            'Opportunity Discovery Workshop',
            'Technology & Tools Recommendations',
            '90-Day Implementation Roadmap',
            'Cost & Timeline Estimates'
        ]
    },
    {
        slug: 'ai-automation',
        icon: '⚙️',
        subtitle: 'Intelligent Automation',
        title: 'AI Automation & Workflow Optimization',
        description: 'Automate repetitive work. Improve speed. Reduce cost. We design and deploy automation systems that enhance productivity while maintaining high accuracy.',
        gradient: 'bg-gradient-to-br from-orange-900 via-red-800 to-pink-600',
        mainDescription: 'Transform your operations with intelligent automation that learns and adapts to your business processes.',
        features: [
            {
                icon: '📄',
                title: 'Document Processing',
                description: 'Automated extraction, classification, and processing of documents with high accuracy.'
            },
            {
                icon: '📧',
                title: 'Email & Workflow Automation',
                description: 'Intelligent routing, response generation, and task automation across your workflows.'
            },
            {
                icon: '🔄',
                title: 'CRM & Operations',
                description: 'Streamline customer relationship management and operational processes with AI-powered automation.'
            }
        ],
        technologies: ['UiPath', 'Power Automate', 'Zapier', 'Python', 'OCR', 'NLP', 'Machine Learning', 'API Integration'],
        benefits: [
            {
                icon: '⚡',
                title: '10x Faster',
                description: 'Dramatically reduce processing time for repetitive tasks'
            },
            {
                icon: '💰',
                title: 'Cost Savings',
                description: 'Reduce operational costs by up to 70%'
            },
            {
                icon: '🎯',
                title: 'Higher Accuracy',
                description: 'Minimize human errors and improve consistency'
            }
        ],
        useCases: [
            {
                title: 'Invoice Processing',
                description: 'Automatically extract, validate, and process invoices from multiple formats'
            },
            {
                title: 'Customer Support',
                description: 'Auto-route tickets, suggest responses, and escalate when needed'
            },
            {
                title: 'Data Entry',
                description: 'Eliminate manual data entry across systems with intelligent automation'
            }
        ]
    },
    {
        slug: 'ai-chatbots',
        icon: '💬',
        subtitle: 'Conversational AI',
        title: 'AI Chatbots & Virtual Assistants',
        description: 'Smart chatbots that understand your business. We build custom chatbots that handle FAQs, customer queries, lead qualification, support, and internal knowledge.',
        gradient: 'bg-gradient-to-br from-green-900 via-teal-800 to-cyan-600',
        mainDescription: 'Deploy intelligent conversational AI that provides 24/7 support and enhances customer experience.',
        features: [
            {
                icon: '🌐',
                title: 'Website Chatbots',
                description: 'Engage visitors, answer questions, and capture leads with intelligent website chatbots.'
            },
            {
                icon: '📱',
                title: 'WhatsApp & CRM Bots',
                description: 'Integrate with WhatsApp, Slack, Teams, and CRM systems for seamless communication.'
            },
            {
                icon: '🧠',
                title: 'Knowledge Assistants',
                description: 'Internal AI assistants that help employees find information and complete tasks faster.'
            }
        ],
        technologies: ['GPT-4', 'Claude', 'Dialogflow', 'Rasa', 'LangChain', 'WhatsApp API', 'Twilio', 'WebSocket'],
        benefits: [
            {
                icon: '⏰',
                title: '24/7 Availability',
                description: 'Never miss a customer inquiry, day or night'
            },
            {
                icon: '🚀',
                title: 'Instant Response',
                description: 'Provide immediate answers to common questions'
            },
            {
                icon: '💰',
                title: 'Reduce Support Costs',
                description: 'Handle 80% of queries without human intervention'
            }
        ],
        deliverables: [
            'Custom chatbot design & branding',
            'Knowledge base ingestion',
            'Multi-channel integration',
            'Analytics dashboard',
            '30-day support & optimization'
        ]
    },
    {
        slug: 'llm-integration',
        icon: '🤖',
        subtitle: 'Large Language Models',
        title: 'Custom LLM Integrations (GenAI Apps)',
        description: 'Bring ChatGPT-like intelligence into your tools and workflows. We integrate advanced large language models into your existing systems.',
        gradient: 'bg-gradient-to-br from-purple-900 via-blue-800 to-indigo-600',
        mainDescription: 'Harness the power of GPT-4, Claude, and other LLMs to build intelligent applications tailored to your business.',
        features: [
            {
                icon: '🔍',
                title: 'AI-Powered Search',
                description: 'Semantic search that understands intent and context, not just keywords.'
            },
            {
                icon: '🤝',
                title: 'Sales & Support Co-pilots',
                description: 'AI assistants that help your team work faster and smarter.'
            },
            {
                icon: '📚',
                title: 'RAG Knowledge Engines',
                description: 'Retrieval-augmented generation systems that provide accurate, source-backed answers.'
            }
        ],
        technologies: ['GPT-4', 'Claude', 'Llama', 'LangChain', 'Vector DBs', 'OpenAI API', 'Pinecone', 'Weaviate'],
        benefits: [
            {
                icon: '⚡',
                title: 'Boost Productivity',
                description: 'Help teams complete tasks 5x faster with AI assistance'
            },
            {
                icon: '🎯',
                title: 'Better Decisions',
                description: 'Access insights and information instantly'
            },
            {
                icon: '🔒',
                title: 'Secure & Private',
                description: 'Your data stays within your infrastructure'
            }
        ]
    },
    {
        slug: 'data-analytics',
        icon: '📊',
        subtitle: 'Data Intelligence',
        title: 'Data Engineering, Dashboards & Predictive Analytics',
        description: 'Make data useful. Make decisions faster. We clean, transform, and analyze your data to reveal insights and predict future outcomes.',
        gradient: 'bg-gradient-to-br from-yellow-900 via-orange-800 to-red-600',
        mainDescription: 'Transform raw data into actionable insights with advanced analytics and predictive modeling.',
        features: [
            {
                icon: '📈',
                title: 'Sales Forecasting',
                description: 'Predict future revenue with ML-powered forecasting models.'
            },
            {
                icon: '📦',
                title: 'Inventory Optimization',
                description: 'Optimize stock levels and reduce waste with predictive analytics.'
            },
            {
                icon: '👥',
                title: 'Customer Analytics',
                description: 'Predict churn, segment customers, and personalize experiences.'
            }
        ],
        technologies: ['Python', 'SQL', 'Power BI', 'Tableau', 'BigQuery', 'Snowflake', 'Apache Spark', 'TensorFlow'],
        benefits: [
            {
                icon: '📊',
                title: 'Data-Driven Decisions',
                description: 'Make confident decisions backed by data'
            },
            {
                icon: '🔮',
                title: 'Predict Outcomes',
                description: 'Anticipate trends and prepare accordingly'
            },
            {
                icon: '💰',
                title: 'Increase Revenue',
                description: 'Identify opportunities and optimize operations'
            }
        ]
    },
    {
        slug: 'rag-systems',
        icon: '🔍',
        subtitle: 'Knowledge Intelligence',
        title: 'RAG (Retrieval-Augmented Generation) Systems',
        description: 'Your company\'s private, secure ChatGPT. We build domain-specific knowledge assistants that use your internal documents, SOPs, and systems.',
        gradient: 'bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-600',
        mainDescription: 'Build intelligent systems that provide accurate, source-backed answers from your proprietary knowledge base.',
        features: [
            {
                icon: '📚',
                title: 'Document Ingestion',
                description: 'Automated pipeline to process PDFs, docs, wikis, and databases.'
            },
            {
                icon: '🗄️',
                title: 'Vector Database',
                description: 'Efficient storage and retrieval of embeddings for semantic search.'
            },
            {
                icon: '🎯',
                title: 'Accuracy Testing',
                description: 'Continuous evaluation and fine-tuning for optimal performance.'
            }
        ],
        technologies: ['LangChain', 'Pinecone', 'Weaviate', 'ChromaDB', 'GPT-4', 'Embeddings', 'Vector Search'],
        benefits: [
            {
                icon: '🔒',
                title: 'Private & Secure',
                description: 'Your data never leaves your infrastructure'
            },
            {
                icon: '✅',
                title: 'Accurate Answers',
                description: 'Source-backed responses with citations'
            },
            {
                icon: '⚡',
                title: 'Instant Access',
                description: 'Find information in seconds, not hours'
            }
        ]
    },
    {
        slug: 'mlops',
        icon: '🚀',
        subtitle: 'Production AI',
        title: 'MLOps & Model Deployment',
        description: 'Make your AI models scalable, secure, and production-ready. We help you deploy, monitor, and improve AI models with modern MLOps practices.',
        gradient: 'bg-gradient-to-br from-slate-900 via-gray-800 to-zinc-600',
        mainDescription: 'Deploy and manage ML models at scale with enterprise-grade MLOps infrastructure.',
        features: [
            {
                icon: '🔄',
                title: 'CI/CD for AI',
                description: 'Automated pipelines for training, testing, and deploying ML models.'
            },
            {
                icon: '📊',
                title: 'Monitoring & Logging',
                description: 'Track model performance, drift, and data quality in real-time.'
            },
            {
                icon: '☁️',
                title: 'Cloud Deployment',
                description: 'Deploy on AWS, GCP, Azure, or on-premise infrastructure.'
            }
        ],
        technologies: ['MLflow', 'Kubeflow', 'Docker', 'Kubernetes', 'AWS SageMaker', 'Azure ML', 'TensorFlow Serving'],
        benefits: [
            {
                icon: '⚡',
                title: 'Fast Deployment',
                description: 'Go from model to production in days, not months'
            },
            {
                icon: '📈',
                title: 'Scalable',
                description: 'Handle millions of predictions per day'
            },
            {
                icon: '🔒',
                title: 'Reliable',
                description: '99.9% uptime with automated monitoring'
            }
        ]
    },
    {
        slug: 'genai-business',
        icon: '🎨',
        subtitle: 'Business GenAI',
        title: 'GenAI for Marketing, HR, Sales & Operations',
        description: 'AI tools that improve real business functions. We build GenAI systems tailored to your teams.',
        gradient: 'bg-gradient-to-br from-pink-900 via-rose-800 to-red-600',
        mainDescription: 'Empower every department with custom GenAI tools that automate and enhance their workflows.',
        features: [
            {
                icon: '📢',
                title: 'Marketing Automation',
                description: 'Generate content, emails, and campaigns with AI-powered creativity.'
            },
            {
                icon: '👥',
                title: 'HR & Recruitment',
                description: 'Screen candidates, draft job descriptions, and automate HR workflows.'
            },
            {
                icon: '💼',
                title: 'Sales Enablement',
                description: 'Generate proposals, emails, and presentations tailored to each prospect.'
            }
        ],
        technologies: ['GPT-4', 'Claude', 'Jasper', 'Copy.ai', 'Custom Models', 'API Integration', 'Workflow Automation'],
        benefits: [
            {
                icon: '⚡',
                title: '10x Content Output',
                description: 'Create more content in less time'
            },
            {
                icon: '🎯',
                title: 'Consistent Quality',
                description: 'Maintain brand voice and quality standards'
            },
            {
                icon: '💰',
                title: 'Reduce Costs',
                description: 'Lower content creation and operational costs'
            }
        ]
    }
]

export function getServiceBySlug(slug: string): ServicePageData | undefined {
    return servicePages.find(service => service.slug === slug)
}

