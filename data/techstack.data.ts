export interface TechCategory {
    category: string
    id: string
    icon: string
    techs: string[]
}

export interface FilterCategory {
    id: string
    label: string
}

export const techCategories: TechCategory[] = [
    {
        category: 'Programming Languages',
        id: 'languages',
        icon: '💻',
        techs: ['Python', 'R', 'JavaScript', 'SQL'],
    },
    {
        category: 'Development Tools',
        id: 'tools',
        icon: '🛠️',
        techs: [
            'VS Code',
            'Sublime Text',
            'Jupyter',
            'Colab',
            'Anaconda',
            'PyCharm',
            'Firebase',
        ],
    },
    {
        category: 'Frameworks & Libraries',
        id: 'frameworks',
        icon: '📚',
        techs: [
            'NumPy',
            'Pandas',
            'SciPy',
            'Matplotlib',
            'Seaborn',
            'Plotly',
            'OpenCV',
            'Pillow',
            'Scikit-learn',
            'TensorFlow',
            'Keras',
            'PyTorch',
            'NLTK',
            'LangChain',
            'HF Transformers',
            'Fast.ai',
        ],
    },
    {
        category: 'Data & AI Platforms',
        id: 'platforms',
        icon: '🤖',
        techs: ['Dataiku', 'NVIDIA'],
    },
    {
        category: 'Model Ecosystems',
        id: 'models',
        icon: '🧠',
        techs: [
            'OpenAI',
            'Google AI',
            'Perplexity',
            'Anthropic',
            'Kaggle',
            'Hugging Face',
            'Meta',
        ],
    },
    {
        category: 'Databases',
        id: 'databases',
        icon: '🗄️',
        techs: [
            'PostgreSQL',
            'Apache Cassandra',
            'Azure SQL Database',
            'MongoDB',
            'Redis',
        ],
    },
    {
        category: 'Deployment & APIs',
        id: 'deployment',
        icon: '🚀',
        techs: [
            'Flask',
            'FastAPI',
            'Django',
            'Streamlit',
            'Azure DevOps',
            'Git',
            'GitHub',
            'Docker',
            'Kubernetes',
        ],
    },
    {
        category: 'Cloud Platforms',
        id: 'cloud',
        icon: '☁️',
        techs: ['Azure', 'Google Cloud', 'Vercel', 'NameCheap'],
    },
]

export const filterCategories: FilterCategory[] = [
    { id: 'all', label: 'All Technologies' },
    { id: 'languages', label: 'Languages' },
    { id: 'frameworks', label: 'Frameworks' },
    { id: 'cloud', label: 'Cloud' },
    { id: 'models', label: 'AI Models' },
]

export const techStackPageData = {
    heading: {
        prefix: 'Core Technologies for',
        highlight: 'Intelligent Systems',
    },
    subheading: 'Powered by industry-leading tools and frameworks',
    cta: {
        heading: 'Join uniAiverse today to unlock AI-driven growth',
        subheading: 'Transform your enterprise with cutting-edge AI solutions',
        buttonText: 'Discover More',
        buttonHref: '#contact',
    },
}

