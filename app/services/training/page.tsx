'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

// ─── Programme Data ──────────────────────────────────────────────────────────

const PROGRAMMES = [
  {
    id: 'ai-engineer',
    icon: '🤖',
    badge: 'Most Popular',
    title: 'AI Engineer Track',
    shortDesc: 'From Python basics to production ML systems deployed on Azure or GCP.',
    duration: '12 Weeks',
    level: 'Intermediate → Advanced',
    format: 'In-Person / Virtual / Hybrid',
    sessions: '36 Sessions',
    accentColor: '#f59e0b',
    target:
      'Software engineers, backend developers, and CS graduates transitioning into AI. Prerequisites: Python basics and some data experience.',
    goal:
      'Build a job-ready AI engineer capable of designing, training, evaluating, and deploying ML/DL models in production environments.',
    cert: 'uniAiverse Certified AI Engineer + OpenAI and HuggingFace project portfolio on GitHub',
    delivery: '3 sessions per week (2 hrs each) + weekend project lab + mentor office hours',
    capstone:
      'End-to-end ML system: data ingestion → model training → REST API → cloud deployment on Azure or GCP',
    weeks: [
      { week: 1,  topic: 'AI & ML Foundations + Python Environment Setup', tools: 'Python, NumPy, Pandas, Jupyter', outcome: 'Set up ML dev environment; understand supervised, unsupervised, and reinforcement learning concepts.' },
      { week: 2,  topic: 'Data Engineering and Feature Engineering',        tools: 'Scikit-learn, SQL, Pandas',          outcome: 'Clean, transform, and engineer features from raw datasets for model input.' },
      { week: 3,  topic: 'Classical ML: Regression, Classification, Clustering', tools: 'Scikit-learn, Matplotlib, Seaborn', outcome: 'Implement and evaluate core ML models; understand bias-variance tradeoff.' },
      { week: 4,  topic: 'Model Evaluation, Tuning & Explainability',       tools: 'GridSearchCV, Cross-validation, SHAP', outcome: 'Select, tune, and interpret ML models; build explainability into outputs.' },
      { week: 5,  topic: 'Deep Learning: ANNs and CNNs',                    tools: 'TensorFlow, Keras, PyTorch',          outcome: 'Build and train neural networks for image and tabular data tasks.' },
      { week: 6,  topic: 'NLP Fundamentals and Transformers',               tools: 'HuggingFace, NLTK, spaCy',           outcome: 'Text classification, NER, sentiment analysis using transformers.' },
      { week: 7,  topic: 'Generative AI and LLM Fundamentals',              tools: 'OpenAI API, LangChain, Anthropic',   outcome: 'Prompt engineering, API integration, building GenAI-powered application features.' },
      { week: 8,  topic: 'RAG Systems and Vector Databases',                tools: 'FAISS, Pinecone, LangChain, ChromaDB', outcome: 'Build retrieval-augmented generation pipelines for domain-specific Q&A systems.' },
      { week: 9,  topic: 'Agentic AI and Tool Use',                        tools: 'LangChain Agents, OpenAI Tools, MCPs', outcome: 'Build multi-step autonomous agents with tool access, memory, and planning.' },
      { week: 10, topic: 'MLOps: Experiment Tracking & CI/CD',              tools: 'MLflow, DVC, GitHub Actions, Docker', outcome: 'Track experiments, version models, build CI/CD pipelines for AI applications.' },
      { week: 11, topic: 'Cloud Deployment and Monitoring',                 tools: 'Azure ML, GCP AI Platform, FastAPI',  outcome: 'Deploy models as APIs; set up monitoring, alerting, and retraining triggers.' },
      { week: 12, topic: 'Capstone Project + Portfolio & Interview Prep',   tools: 'Full stack (learner\'s choice)',      outcome: 'Present end-to-end AI system; code review session + interview preparation.' },
    ],
    dos: [
      'Always version your datasets and models using DVC or MLflow',
      'Write modular, testable code — treat AI code like production software',
      'Document every experiment: hypothesis, parameters, result, decision',
      'Use reproducible environments: Docker and requirements.txt',
      'Build model explainability in from day one using SHAP or LIME',
      'Test edge cases and out-of-distribution inputs before every deployment',
    ],
    donts: [
      'Training models without establishing a baseline evaluation first',
      'Skipping cross-validation; overfitting by evaluating on the test set',
      'Ignoring data leakage — it inflates metrics and breaks production models',
      'Deploying models to production without monitoring or alerting in place',
      'Using black-box models for high-stakes decisions without explainability',
      'Assuming production data will behave exactly like training data',
    ],
  },
  {
    id: 'data-analyst',
    icon: '📊',
    badge: 'Beginner Friendly',
    title: 'Data Analyst Track',
    shortDesc: 'Transform raw data into compelling business insights and live dashboards.',
    duration: '10 Weeks',
    level: 'Beginner → Intermediate',
    format: 'In-Person / Virtual / Hybrid',
    sessions: '30 Sessions',
    accentColor: '#34d399',
    target:
      'Business analysts, operations staff, finance teams, and fresh graduates who want to work professionally with data.',
    goal:
      'Transform raw data into clear business insights using modern analytics tools, dashboards, and predictive techniques.',
    cert: 'uniAiverse Certified Data Analyst + BI dashboard portfolio in Power BI or Looker Studio',
    delivery: '3 sessions per week (1.5 hrs each) + weekly business case analysis + 1-on-1 mentor check-in',
    capstone:
      'End-to-end analytics project: data cleaning → EDA → dashboard → business recommendation presentation',
    weeks: [
      { week: 1,  topic: 'Data Fundamentals and Excel Mastery',          tools: 'Excel, Google Sheets',                           outcome: 'Understand data types, clean datasets, use pivot tables and advanced formulas.' },
      { week: 2,  topic: 'SQL for Data Analysis',                        tools: 'PostgreSQL, MySQL, BigQuery',                    outcome: 'Write queries, joins, aggregations, and CTEs against real datasets.' },
      { week: 3,  topic: 'Python for Data Analysis',                     tools: 'Python, Pandas, NumPy',                          outcome: 'Load, explore, and transform structured datasets programmatically.' },
      { week: 4,  topic: 'Data Visualisation and Storytelling',          tools: 'Matplotlib, Seaborn, Plotly',                    outcome: 'Build charts that communicate insights clearly to non-technical stakeholders.' },
      { week: 5,  topic: 'Business Intelligence and Dashboards',         tools: 'Power BI, Looker Studio, Tableau',               outcome: 'Design interactive dashboards; connect and refresh live data sources.' },
      { week: 6,  topic: 'Exploratory Data Analysis Deep Dive',          tools: 'Pandas Profiling, Sweetviz',                     outcome: 'Perform systematic EDA; identify patterns, outliers, and data quality issues.' },
      { week: 7,  topic: 'Statistics for Analysts',                      tools: 'SciPy, Statsmodels',                             outcome: 'Hypothesis testing, A/B testing, confidence intervals, correlation vs causation.' },
      { week: 8,  topic: 'Introduction to Predictive Analytics',         tools: 'Scikit-learn: Linear & Logistic Regression',     outcome: 'Build and interpret simple predictive models; explain outputs to stakeholders.' },
      { week: 9,  topic: 'Time Series Analysis and Forecasting',         tools: 'Prophet, ARIMA, Pandas',                        outcome: 'Forecast KPIs, sales, and demand; understand seasonality and trend decomposition.' },
      { week: 10, topic: 'Capstone Project + Stakeholder Presentation',  tools: 'Full analytics stack',                           outcome: 'Present data-driven business recommendation; sharpen slide and communication skills.' },
    ],
    dos: [
      'Always understand the business question before opening the data',
      'Document your data sources, transformations, and key assumptions',
      'Validate data quality before any analysis: check nulls, duplicates, and types',
      'Present insights with a "So what?" — every finding needs a recommendation',
      'Keep dashboards focused: maximum 5–7 KPIs per page',
      'Version your SQL queries and notebooks in Git for reproducibility',
    ],
    donts: [
      'Building dashboards before confirming what decision they will drive',
      'Confusing correlation with causation when presenting findings to leadership',
      'Using 3D pie charts or misleading axis scales in executive presentations',
      'Sharing raw data tables with stakeholders without context or narrative',
      'Over-engineering analysis when a simple average or percentage answers the question',
      'Presenting analysis without checking if the underlying data has been refreshed',
    ],
  },
  {
    id: 'genai-engineer',
    icon: '⚡',
    badge: 'Cutting Edge',
    title: 'Full Stack GenAI Engineer',
    shortDesc: 'Build production-grade chatbots, RAG systems, and agentic AI applications.',
    duration: '14 Weeks',
    level: 'Intermediate → Advanced',
    format: 'In-Person / Virtual / Hybrid',
    sessions: '42 Sessions',
    accentColor: '#a78bfa',
    target:
      'Python developers, ML engineers, and backend developers who want to specialise in building production-ready GenAI products: chatbots, RAG systems, and agentic applications.',
    goal:
      'Design, build, and ship full-stack GenAI applications from LLM API integration through vector databases, deployment, and observability.',
    cert: 'uniAiverse Certified GenAI Engineer + live deployed GenAI application in portfolio',
    delivery: '3 sessions per week (2 hrs each) + project sprints + weekly code review with mentor',
    capstone:
      'Deploy a production-grade RAG-powered AI assistant with custom UI, user authentication, and live monitoring dashboard',
    weeks: [
      { week: 1,  topic: 'GenAI Landscape and LLM Fundamentals',          tools: 'OpenAI API, Anthropic Claude API',          outcome: 'Understand LLM architecture, tokenisation, context windows, and API usage patterns.' },
      { week: 2,  topic: 'Prompt Engineering Mastery',                    tools: 'OpenAI, LangChain, PromptFlow',             outcome: 'Zero-shot, few-shot, chain-of-thought prompting; system prompt design; injection defence.' },
      { week: 3,  topic: 'LangChain and LlamaIndex Deep Dive',            tools: 'LangChain, LlamaIndex, Python',            outcome: 'Build chains, memory systems, and document loaders for GenAI pipelines.' },
      { week: 4,  topic: 'Vector Databases and Semantic Search',          tools: 'FAISS, Pinecone, ChromaDB, Weaviate',      outcome: 'Understand embeddings, index types, similarity search; choose the right vector DB.' },
      { week: 5,  topic: 'RAG Architecture: Design and Build',            tools: 'LangChain, HuggingFace, OpenAI',           outcome: 'Build a production RAG system with document ingestion, chunking, and retrieval evaluation.' },
      { week: 6,  topic: 'Hybrid RAG and Advanced Retrieval',             tools: 'BM25, HuggingFace Reranker, Cohere',       outcome: 'Combine dense and sparse retrieval; implement reranking; evaluate pipeline quality with RAGAS.' },
      { week: 7,  topic: 'Fine-Tuning and Model Customisation',           tools: 'LoRA, QLoRA, HuggingFace PEFT',            outcome: 'Fine-tune open-source LLMs on domain data; understand when to fine-tune vs use RAG.' },
      { week: 8,  topic: 'Agentic AI: Planning, Tool Use & Memory',       tools: 'LangChain Agents, OpenAI Function Calling', outcome: 'Build agents with tool calling, persistent memory, and multi-step task execution.' },
      { week: 9,  topic: 'Model Context Protocols (MCPs)',                tools: 'MCP SDK, FastAPI, Custom Tool Servers',    outcome: 'Implement MCP servers and clients; connect agents to external APIs and data systems.' },
      { week: 10, topic: 'Full Stack Backend: Production API Layer',      tools: 'FastAPI, Docker, PostgreSQL, Auth',        outcome: 'Wrap GenAI pipelines in production REST APIs with authentication and rate limiting.' },
      { week: 11, topic: 'Frontend for AI Applications',                  tools: 'Streamlit, React basics, Vercel',          outcome: 'Build and deploy AI-powered UI with streaming responses and chat interfaces.' },
      { week: 12, topic: 'Observability, Evaluation & Guardrails',        tools: 'LangSmith, RAGAS, PromptLayer',            outcome: 'Trace, evaluate, and monitor LLM apps in production; implement input/output guardrails.' },
      { week: 13, topic: 'MLOps for GenAI: CI/CD and Deployment',        tools: 'GitHub Actions, Docker, Azure & GCP',      outcome: 'Automate testing and deployment of GenAI apps; implement rollback and canary strategies.' },
      { week: 14, topic: 'Capstone: Full Stack GenAI Product — Demo Day', tools: 'End-to-end production stack',              outcome: 'Ship a live monitored GenAI application; demo day + portfolio review + interview prep.' },
    ],
    dos: [
      'Evaluate your RAG pipeline with RAGAS metrics before going to production',
      'Use streaming responses for all chat interfaces — the UX improvement is dramatic',
      'Implement guardrails: input validation, PII filtering, and toxicity checks',
      'Design for observability from day one: log every prompt, token count, and latency',
      'Version your prompts in Git like code — prompt changes can silently break outputs',
      'Test adversarial inputs: prompt injection attempts, jailbreaks, and edge cases',
    ],
    donts: [
      'Assuming the LLM always gets it right — evaluation is non-negotiable',
      'Sending entire document libraries into the context window instead of using RAG',
      'Exposing raw LLM outputs without any sanitisation in customer-facing applications',
      'Hardcoding API keys — always use environment variables and secrets managers',
      'Ignoring context window limits — plan your chunking and retrieval strategy upfront',
      'Building monolithic pipelines — modularise components for testability and reuse',
    ],
  },
  {
    id: 'aiops',
    icon: '⚙️',
    badge: 'Infrastructure Focus',
    title: 'AIOps Engineering Track',
    shortDesc: 'Operationalise AI at scale with CI/CD pipelines, monitoring, and governance.',
    duration: '12 Weeks',
    level: 'Intermediate → Advanced',
    format: 'In-Person / Virtual / Hybrid',
    sessions: '36 Sessions',
    accentColor: '#fb923c',
    target:
      'DevOps engineers, cloud engineers, and platform engineers who want to specialise in operationalising AI systems at scale.',
    goal:
      'Build the infrastructure, automation, and observability layers that make AI models reliable, scalable, and maintainable in production.',
    cert: 'uniAiverse Certified AIOps Engineer + full MLOps pipeline on GitHub with CI/CD and live monitoring',
    delivery: '3 sessions per week (2 hrs each) + hands-on cloud lab environment + weekly architecture review with mentor',
    capstone:
      'Design and deploy a full MLOps pipeline: data versioning → training → model registry → deployment → monitoring → automated retraining trigger',
    weeks: [
      { week: 1,  topic: 'AIOps Fundamentals and ML System Design',                     tools: 'System design patterns, Python',              outcome: 'Understand the ML production lifecycle, common failure modes, and AIOps vs standard DevOps.' },
      { week: 2,  topic: 'Data Versioning and Pipeline Orchestration',                  tools: 'DVC, Apache Airflow, Prefect',                 outcome: 'Version datasets; build automated data ingestion and transformation pipelines.' },
      { week: 3,  topic: 'Experiment Tracking and Model Registry',                      tools: 'MLflow, Weights and Biases',                   outcome: 'Log experiments, compare runs, register models, manage staging and production versions.' },
      { week: 4,  topic: 'Containerisation for AI Workloads',                           tools: 'Docker, Docker Compose',                      outcome: 'Package ML models and APIs into portable, reproducible containers ready for deployment.' },
      { week: 5,  topic: 'Kubernetes for ML at Scale',                                  tools: 'Kubernetes, Helm, kubectl',                   outcome: 'Deploy and scale containerised ML services on Kubernetes; manage CPU and GPU resources.' },
      { week: 6,  topic: 'CI/CD Pipelines for Machine Learning',                        tools: 'GitHub Actions, Jenkins, Azure DevOps',        outcome: 'Automate model testing, validation gating, and deployment with approval workflows.' },
      { week: 7,  topic: 'Model Serving: REST APIs and Batch Inference',                tools: 'FastAPI, TorchServe, Triton',                 outcome: 'Serve models via REST API and scheduled batch pipelines; handle concurrency and latency.' },
      { week: 8,  topic: 'Monitoring: Data Drift, Degradation & Alerts',               tools: 'EvidentlyAI, Prometheus, Grafana',             outcome: 'Detect data drift and performance degradation; set up dashboards and alerting.' },
      { week: 9,  topic: 'Automated Retraining Pipelines & Feedback Loops',            tools: 'MLflow, Airflow, DVC',                         outcome: 'Automate model retraining on schedule or drift trigger; validate new models before promotion.' },
      { week: 10, topic: 'Feature Stores and Data Management',                          tools: 'Feast, Tecton, Redis',                        outcome: 'Build and manage feature stores for consistent and reusable training and serving data.' },
      { week: 11, topic: 'AI Governance, Security & Compliance',                        tools: 'Azure Policy, OPA, Model Cards',              outcome: 'Implement model auditing, access control, bias monitoring, and compliance documentation.' },
      { week: 12, topic: 'Capstone: Production AIOps System — Demo Day',               tools: 'Full AIOps stack',                            outcome: 'Present fully automated AI system with CI/CD, monitoring, and governance — live demo.' },
    ],
    dos: [
      'Version everything together: data, code, configs, and model artifacts',
      'Monitor for data drift and model degradation from the very first deployment',
      'Implement automated retraining gates: validate the new model before promoting it',
      'Strictly separate training, staging, and production environments',
      'Document model cards for every model: inputs, outputs, limitations, known bias',
      'Design for failure: circuit breakers, fallbacks, and shadow deployment strategies',
    ],
    donts: [
      'Deploying to production without a tested rollback strategy in place',
      'Treating AI monitoring the same as application monitoring — they have different failure modes',
      'Relying on manual deployments — every production change must go through CI/CD',
      'Sharing feature stores between training and serving without proper versioning',
      'Skipping integration tests for ML pipelines — silent failures are extremely common',
      'Leaving GPU clusters running when idle — it is the number one hidden infrastructure cost',
    ],
  },
]

const TECH_TAGS = [
  'Machine Learning','Deep Learning','NLP','Computer Vision','MLOps',
  'Python','TensorFlow','PyTorch','LangChain','Vector DBs',
  'FastAPI','Docker','Kubernetes','OpenAI API','RAG Systems','LLM Fine-Tuning',
]

const OFFER_CARDS = [
  {
    emoji: '💻',
    title: 'Hands-On Technical Workshops',
    desc: 'Real-world training in ML, NLP, Computer Vision, and Generative AI — led by practitioners with live coding and weekly project labs.',
    tags: ['ML', 'NLP', 'GenAI', 'CV'],
    accent: '#f59e0b',
  },
  {
    emoji: '💼',
    title: 'Business-Focused AI Programs',
    desc: 'Enabling non-technical teams to understand, evaluate, and apply AI strategically — bridging the gap between business goals and technology.',
    tags: ['Strategy', 'Analytics', 'BI', 'ROI'],
    accent: '#34d399',
  },
  {
    emoji: '⚖️',
    title: 'Ethics & Responsible AI',
    desc: 'Fostering a culture of trust, safety, and accountability — covering bias detection, governance frameworks, and responsible deployment practices.',
    tags: ['Governance', 'Bias', 'Safety', 'Trust'],
    accent: '#a78bfa',
  },
]

// ─── Page Component ──────────────────────────────────────────────────────────

export default function TrainingPage() {
  const [activeTrack, setActiveTrack] = useState<string | null>(null)
  const [activeTab, setActiveTab]   = useState('overview')
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null)

  const selected = PROGRAMMES.find((p) => p.id === activeTrack)

  function selectTrack(id: string) {
    if (activeTrack === id) {
      setActiveTrack(null)
    } else {
      setActiveTrack(id)
      setActiveTab('overview')
      setExpandedWeek(null)
    }
  }

  return (
    <main className="min-h-screen" style={{ fontFamily: "'Outfit', sans-serif" }}>

      {/* ── Google Fonts + Custom Animations ───────────────────────────── */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap');

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0);    }
        }
        @keyframes shimmer {
          0%   { background-position: -200% center; }
          100% { background-position:  200% center; }
        }
        @keyframes pulseGlow {
          0%,100% { box-shadow: 0 0 0 0 rgba(245,158,11,0.35); }
          50%     { box-shadow: 0 0 0 10px rgba(245,158,11,0);  }
        }
        @keyframes floatIn {
          from { opacity: 0; transform: scale(0.97) translateY(16px); }
          to   { opacity: 1; transform: scale(1)    translateY(0);     }
        }

        .syne           { font-family: 'Syne', sans-serif; }
        .outfit         { font-family: 'Outfit', sans-serif; }

        .track-card     { transition: transform 0.28s cubic-bezier(.4,0,.2,1), box-shadow 0.28s ease; cursor: pointer; }
        .track-card:hover { transform: translateY(-4px); }
        .track-card.active { animation: pulseGlow 2.2s infinite; }

        .week-pill      { transition: transform 0.18s ease, background 0.18s ease; cursor: pointer; }
        .week-pill:hover { transform: scale(1.03); }

        .shimmer-tag {
          background: linear-gradient(90deg, #92400e 0%, #d97706 45%, #f59e0b 55%, #92400e 100%);
          background-size: 250% auto;
          animation: shimmer 3.5s linear infinite;
          transition: transform 0.2s ease;
        }
        .shimmer-tag:hover { transform: scale(1.1); }

        .do-row   { transition: transform 0.18s ease; }
        .do-row:hover   { transform: translateX(5px);  }
        .dont-row { transition: transform 0.18s ease; }
        .dont-row:hover { transform: translateX(-5px); }

        .section-reveal { animation: fadeUp  0.45s ease both; }
        .float-in       { animation: floatIn 0.5s  ease both; }

        .amber-text {
          background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .tab-btn {
          padding: 0.9rem 1.6rem;
          background: none;
          border: none;
          cursor: pointer;
          font-family: 'Outfit', sans-serif;
          font-weight: 600;
          font-size: 0.88rem;
          letter-spacing: 0.02em;
          transition: color 0.2s ease;
          border-bottom: 2px solid transparent;
          white-space: nowrap;
        }
        .tab-btn.active  { border-bottom-color: currentColor; }
        .tab-btn:hover:not(.active) { color: rgba(255,255,255,0.7) !important; }

        .grid-dots {
          background-image: radial-gradient(circle, rgba(245,158,11,0.12) 1px, transparent 1px);
          background-size: 28px 28px;
        }
      `}</style>

      <Header />

      <ServiceHero
        icon="📚"
        subtitle="AI Education & Upskilling"
        title="Training and Workshops"
        description="Build AI fluency through interactive workshops—tailored to professionals for real-world innovation and confident tech leadership."
        gradient="bg-gradient-to-br from-amber-900 via-yellow-800 to-orange-700"
      />

      {/* ── Stats Banner ─────────────────────────────────────────────── */}
      <div style={{ background: 'linear-gradient(100deg, #0d0800, #1a0e02, #0d0800)', borderBottom: '1px solid rgba(245,158,11,0.18)' }}>
        <div className="container mx-auto px-6 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto text-center">
            {[
              { num: '4',    label: 'Career Tracks',   icon: '🛤️' },
              { num: '14',   label: 'Max Weeks',        icon: '📅' },
              { num: '2 hr', label: 'Per Session',      icon: '⏱️' },
              { num: '100%', label: 'Project-Based',    icon: '🏗️' },
            ].map((s) => (
              <div key={s.label}>
                <div style={{ fontSize: '1.4rem', marginBottom: '2px' }}>{s.icon}</div>
                <div className="syne amber-text" style={{ fontSize: '2.1rem', fontWeight: 800, lineHeight: 1.1 }}>
                  {s.num}
                </div>
                <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.8rem', fontWeight: 500, marginTop: '3px', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── What We Offer ────────────────────────────────────────────── */}
      <section className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">

            {/* Header */}
            <div className="text-center mb-14">
              <span style={{ background: 'linear-gradient(135deg,#92400e,#d97706)', color: '#fff', padding: '4px 18px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase' }}>
                Our Approach
              </span>
              <h2 className="syne text-primary-dark mt-5 mb-5" style={{ fontSize: 'clamp(2rem,4vw,2.75rem)', fontWeight: 800, letterSpacing: '-0.02em' }}>
                What We Offer
              </h2>
              <p className="text-primary-dark/70 text-xl max-w-3xl mx-auto leading-relaxed">
                Equip your teams with the skills and mindset to innovate, adapt, and lead in an AI-driven world.
              </p>
            </div>

            {/* Three Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-7 mb-20">
              {OFFER_CARDS.map((card) => (
                <div key={card.title} className="bg-secondary-light rounded-2xl shadow-md overflow-hidden track-card">
                  <div style={{ height: '3px', background: `linear-gradient(90deg, ${card.accent}, transparent)` }} />
                  <div className="p-8">
                    <div style={{ width: '54px', height: '54px', background: `${card.accent}18`, borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', marginBottom: '1.25rem' }}>
                      {card.emoji}
                    </div>
                    <h3 className="syne text-primary-dark mb-3" style={{ fontSize: '1.2rem', fontWeight: 700 }}>
                      {card.title}
                    </h3>
                    <p className="text-primary-dark/65 leading-relaxed mb-5 text-sm">
                      {card.desc}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {card.tags.map((tag) => (
                        <span key={tag} style={{ background: `${card.accent}14`, color: card.accent, border: `1px solid ${card.accent}35`, padding: '3px 11px', borderRadius: '100px', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.04em' }}>
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Technologies */}
            <div className="text-center mb-2">
              <span style={{ background: 'linear-gradient(135deg,#92400e,#d97706)', color: '#fff', padding: '4px 18px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase' }}>
                Curriculum Coverage
              </span>
              <h2 className="syne text-primary-dark mt-5 mb-8" style={{ fontSize: 'clamp(1.75rem,3.5vw,2.5rem)', fontWeight: 800, letterSpacing: '-0.02em' }}>
                Technologies You'll Master
              </h2>
              <div className="flex flex-wrap gap-3 justify-center">
                {TECH_TAGS.map((tag) => (
                  <span key={tag} className="shimmer-tag outfit text-white px-5 py-2.5 rounded-full font-semibold text-sm cursor-default select-none">
                    {tag}
                  </span>
                ))}
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ── Choose Your Track ─────────────────────────────────────────── */}
      <section className="grid-dots py-24" style={{ background: 'linear-gradient(180deg, #0a0600 0%, #140c01 60%, #0a0600 100%)' }}>
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">

            {/* Header */}
            <div className="text-center mb-12">
              <span style={{ background: 'rgba(245,158,11,0.12)', color: '#f59e0b', border: '1px solid rgba(245,158,11,0.28)', padding: '4px 18px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase' }}>
                Career Roadmaps
              </span>
              <h2 className="syne mt-5 mb-4" style={{ fontSize: 'clamp(2rem,4vw,2.9rem)', fontWeight: 800, color: '#fff', letterSpacing: '-0.02em' }}>
                Choose Your Career Track
              </h2>
              <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '1.1rem', maxWidth: '560px', margin: '0 auto' }}>
                Four structured pathways. Expert mentors. Industry certifications. Real projects from day one.
              </p>
            </div>

            {/* Track Selection Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
              {PROGRAMMES.map((prog) => {
                const isActive = activeTrack === prog.id
                return (
                  <div
                    key={prog.id}
                    onClick={() => selectTrack(prog.id)}
                    className={`track-card rounded-2xl p-6 ${isActive ? 'active' : ''}`}
                    style={{
                      background: isActive
                        ? `linear-gradient(135deg, ${prog.accentColor}1a, ${prog.accentColor}08)`
                        : 'rgba(255,255,255,0.035)',
                      border: isActive
                        ? `2px solid ${prog.accentColor}55`
                        : '2px solid rgba(255,255,255,0.07)',
                    }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-4">
                        <div style={{ width: '52px', height: '52px', background: `${prog.accentColor}1c`, borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', flexShrink: 0 }}>
                          {prog.icon}
                        </div>
                        <div>
                          <span style={{ background: `${prog.accentColor}1c`, color: prog.accentColor, padding: '2px 10px', borderRadius: '100px', fontSize: '0.68rem', fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', display: 'inline-block', marginBottom: '5px' }}>
                            {prog.badge}
                          </span>
                          <h3 className="syne" style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', lineHeight: 1.25 }}>
                            {prog.title}
                          </h3>
                        </div>
                      </div>
                      <div style={{ color: isActive ? prog.accentColor : 'rgba(255,255,255,0.3)', fontSize: '1.1rem', flexShrink: 0, transition: 'transform 0.35s ease', transform: isActive ? 'rotate(180deg)' : 'none', marginTop: '4px' }}>
                        ↓
                      </div>
                    </div>

                    <p style={{ color: 'rgba(255,255,255,0.52)', fontSize: '0.875rem', margin: '1rem 0', lineHeight: 1.65 }}>
                      {prog.shortDesc}
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {[`📅 ${prog.duration}`, `📊 ${prog.level}`, `🎯 ${prog.sessions}`].map((badge) => (
                        <span key={badge} style={{ background: 'rgba(255,255,255,0.07)', color: 'rgba(255,255,255,0.65)', padding: '4px 13px', borderRadius: '100px', fontSize: '0.78rem', fontWeight: 500 }}>
                          {badge}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>

            {/* ── Programme Detail Panel ─────────────────────────────── */}
            {selected && (
              <div
                key={selected.id}
                className="float-in rounded-3xl overflow-hidden"
                style={{ background: 'rgba(255,255,255,0.025)', border: `1px solid ${selected.accentColor}28` }}
              >
                {/* Panel Header */}
                <div style={{ background: `linear-gradient(135deg, ${selected.accentColor}22, rgba(0,0,0,0))`, padding: '2rem 2.5rem', borderBottom: `1px solid ${selected.accentColor}1e` }}>
                  <div className="flex flex-wrap items-center justify-between gap-5">
                    <div className="flex items-center gap-4">
                      <span style={{ fontSize: '2.5rem' }}>{selected.icon}</span>
                      <div>
                        <h3 className="syne" style={{ fontSize: 'clamp(1.4rem,3vw,1.85rem)', fontWeight: 800, color: '#fff', letterSpacing: '-0.02em', lineHeight: 1.15 }}>
                          {selected.title}
                        </h3>
                        <p style={{ color: 'rgba(255,255,255,0.5)', marginTop: '5px', fontSize: '0.9rem' }}>
                          {selected.format}
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-wrap gap-3">
                      {[
                        { icon: '📅', val: selected.duration },
                        { icon: '📊', val: selected.level    },
                        { icon: '🎓', val: 'Certified'        },
                      ].map((b) => (
                        <div key={b.val} style={{ background: 'rgba(255,255,255,0.07)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', padding: '8px 16px', textAlign: 'center', minWidth: '80px' }}>
                          <div style={{ fontSize: '1.1rem' }}>{b.icon}</div>
                          <div style={{ color: '#fff', fontSize: '0.8rem', fontWeight: 600, marginTop: '3px', whiteSpace: 'nowrap' }}>{b.val}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Tabs */}
                <div style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', padding: '0 1.5rem', overflowX: 'auto' }}>
                  <div style={{ display: 'flex' }}>
                    {[
                      { id: 'overview',      label: 'Overview'       },
                      { id: 'roadmap',       label: 'Weekly Roadmap' },
                      { id: 'bestpractices', label: 'Best Practices' },
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => { setActiveTab(tab.id); setExpandedWeek(null) }}
                        className={`tab-btn outfit ${activeTab === tab.id ? 'active' : ''}`}
                        style={{ color: activeTab === tab.id ? selected.accentColor : 'rgba(255,255,255,0.38)' }}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Tab Body */}
                <div style={{ padding: '2.5rem' }}>

                  {/* ── Overview ── */}
                  {activeTab === 'overview' && (
                    <div className="section-reveal grid grid-cols-1 md:grid-cols-2 gap-5">
                      {[
                        { icon: '🎯', label: 'Target Audience', value: selected.target  },
                        { icon: '🏆', label: 'Programme Goal',  value: selected.goal    },
                        { icon: '📜', label: 'Certification',   value: selected.cert    },
                        { icon: '🗓️', label: 'Delivery Format', value: selected.delivery},
                      ].map((item) => (
                        <div key={item.label} style={{ background: 'rgba(255,255,255,0.04)', borderRadius: '16px', padding: '1.5rem', border: '1px solid rgba(255,255,255,0.07)' }}>
                          <div className="flex items-center gap-2 mb-3">
                            <span style={{ fontSize: '1.2rem' }}>{item.icon}</span>
                            <span style={{ color: selected.accentColor, fontSize: '0.72rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.1em' }}>{item.label}</span>
                          </div>
                          <p style={{ color: 'rgba(255,255,255,0.78)', lineHeight: 1.75, fontSize: '0.93rem' }}>
                            {item.value}
                          </p>
                        </div>
                      ))}

                      {/* Capstone — full width */}
                      <div className="md:col-span-2" style={{ background: `${selected.accentColor}12`, borderRadius: '16px', padding: '1.6rem', border: `1px solid ${selected.accentColor}30` }}>
                        <div className="flex items-center gap-2 mb-3">
                          <span style={{ fontSize: '1.2rem' }}>🚀</span>
                          <span style={{ color: selected.accentColor, fontSize: '0.72rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Capstone Project</span>
                        </div>
                        <p style={{ color: '#fff', lineHeight: 1.75, fontWeight: 500, fontSize: '0.97rem' }}>
                          {selected.capstone}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* ── Weekly Roadmap ── */}
                  {activeTab === 'roadmap' && (
                    <div className="section-reveal">
                      <p style={{ color: 'rgba(255,255,255,0.4)', marginBottom: '1.5rem', fontSize: '0.85rem', letterSpacing: '0.02em' }}>
                        Tap any week to expand the learning outcome.
                      </p>
                      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                        {selected.weeks.map((w, idx) => {
                          const open = expandedWeek === idx
                          return (
                            <div
                              key={w.week}
                              className="week-pill rounded-xl overflow-hidden"
                              style={{
                                background: open ? `${selected.accentColor}16` : 'rgba(255,255,255,0.04)',
                                border: open ? `1px solid ${selected.accentColor}45` : '1px solid rgba(255,255,255,0.07)',
                                animationDelay: `${idx * 0.04}s`,
                              }}
                              onClick={() => setExpandedWeek(open ? null : idx)}
                            >
                              <div style={{ padding: '1rem 1.25rem' }}>
                                <div className="flex items-start gap-3">
                                  <div style={{ width: '34px', height: '34px', background: `linear-gradient(135deg, ${selected.accentColor}, ${selected.accentColor}99)`, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', fontWeight: 800, color: '#000', flexShrink: 0, marginTop: '1px' }}>
                                    W{w.week}
                                  </div>
                                  <div style={{ flex: 1 }}>
                                    <h4 style={{ color: '#fff', fontSize: '0.87rem', fontWeight: 600, lineHeight: 1.4, marginBottom: '6px' }}>
                                      {w.topic}
                                    </h4>
                                    <div className="flex flex-wrap gap-1">
                                      {w.tools.split(', ').slice(0, 3).map((tool) => (
                                        <span key={tool} style={{ background: 'rgba(255,255,255,0.07)', color: 'rgba(255,255,255,0.55)', padding: '2px 8px', borderRadius: '100px', fontSize: '0.68rem', fontWeight: 500 }}>
                                          {tool}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                  <span style={{ color: open ? selected.accentColor : 'rgba(255,255,255,0.3)', transition: 'transform 0.25s ease', transform: open ? 'rotate(180deg)' : 'none', display: 'block', flexShrink: 0, marginTop: '4px' }}>
                                    ↓
                                  </span>
                                </div>

                                {open && (
                                  <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: `1px solid ${selected.accentColor}28` }}>
                                    <p style={{ color: 'rgba(255,255,255,0.72)', fontSize: '0.82rem', lineHeight: 1.7 }}>
                                      {w.outcome}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )}

                  {/* ── Best Practices ── */}
                  {activeTab === 'bestpractices' && (
                    <div className="section-reveal grid grid-cols-1 md:grid-cols-2 gap-8">

                      {/* Do's */}
                      <div>
                        <div className="flex items-center gap-3 mb-5">
                          <div style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg,#10b981,#059669)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '0.85rem', fontWeight: 700, flexShrink: 0 }}>
                            ✓
                          </div>
                          <h4 className="syne" style={{ fontWeight: 700, color: '#10b981', fontSize: '1.1rem', letterSpacing: '-0.01em' }}>
                            Best Practices
                          </h4>
                        </div>
                        <div className="flex flex-col gap-3">
                          {selected.dos.map((text, i) => (
                            <div key={i} className="do-row" style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.18)', borderLeft: '3px solid #10b981', borderRadius: '10px', padding: '0.875rem 1rem' }}>
                              <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.84rem', lineHeight: 1.65 }}>
                                {text}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Don'ts */}
                      <div>
                        <div className="flex items-center gap-3 mb-5">
                          <div style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg,#ef4444,#dc2626)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '0.85rem', fontWeight: 700, flexShrink: 0 }}>
                            ✗
                          </div>
                          <h4 className="syne" style={{ fontWeight: 700, color: '#f87171', fontSize: '1.1rem', letterSpacing: '-0.01em' }}>
                            Common Mistakes to Avoid
                          </h4>
                        </div>
                        <div className="flex flex-col gap-3">
                          {selected.donts.map((text, i) => (
                            <div key={i} className="dont-row" style={{ background: 'rgba(239,68,68,0.06)', border: '1px solid rgba(239,68,68,0.18)', borderLeft: '3px solid #ef4444', borderRadius: '10px', padding: '0.875rem 1rem' }}>
                              <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.84rem', lineHeight: 1.65 }}>
                                {text}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>

                    </div>
                  )}

                </div>
              </div>
            )}

          </div>
        </div>
      </section>

      {/* ── Why Our Training Works ───────────────────────────────────── */}
      <section style={{ background: 'linear-gradient(135deg, #78350f 0%, #b45309 45%, #d97706 100%)' }} className="py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto text-center">
            <h2 className="syne" style={{ fontSize: 'clamp(2rem,4vw,2.75rem)', fontWeight: 800, color: '#fff', letterSpacing: '-0.02em', marginBottom: '1rem' }}>
              Why Our Training Works
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '1.15rem', maxWidth: '560px', margin: '0 auto 3.5rem', lineHeight: 1.7 }}>
              Built for professionals who need real outcomes — not just theory.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-7">
              {[
                { icon: '👨‍💼', title: 'Industry Experts',       desc: 'Every instructor is actively working in AI — bringing real problems and real solutions into the classroom.' },
                { icon: '🏗️', title: 'Real-World Projects',     desc: 'Build portfolio-quality projects from week one. Every programme culminates in a deployed, working AI system.' },
                { icon: '📜', title: 'Industry Certification',  desc: 'Earn uniAiverse certification recognised by leading technology companies and AI-forward organisations.' },
              ].map((item) => (
                <div key={item.title} className="track-card" style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(12px)', borderRadius: '22px', padding: '2.5rem 2rem', border: '1px solid rgba(255,255,255,0.22)' }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1.1rem' }}>{item.icon}</div>
                  <h3 className="syne" style={{ fontWeight: 700, color: '#fff', fontSize: '1.25rem', marginBottom: '0.75rem', letterSpacing: '-0.01em' }}>
                    {item.title}
                  </h3>
                  <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.75, fontSize: '0.93rem' }}>
                    {item.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </main>
  )
}