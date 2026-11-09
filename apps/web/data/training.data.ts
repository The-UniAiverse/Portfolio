// Training & Mentorship programs (page: app/services/training).
// Rule: no durations anywhere (no weeks, hours or months). Programs are self-paced with live mentorship.

export type TrackId = 'engineering' | 'flagship' | 'business'

export interface SyllabusModule {
  title: string
  topics: string[]
  lab: string
}

export interface Program {
  id: string
  icon: string
  title: string
  tagline: string
  description: string
  track: TrackId
  level: string
  badge?: string
  forWho: string[]
  prerequisites: string[]
  outcomes: string[]
  tools: string[]
  modules: SyllabusModule[]
  projects: string[]
}

export const tracks: { id: TrackId; label: string; description: string }[] = [
  { id: 'engineering', label: 'Engineering tracks', description: 'Deep, hands-on programs for people who build.' },
  { id: 'flagship', label: 'Flagship program', description: 'Every engineering track as one guided roadmap.' },
  { id: 'business', label: 'Business & corporate', description: 'AI fluency for teams, leaders and organisations.' },
]

export const programs: Program[] = [
  {
    id: 'ai-engineering',
    icon: '🤖',
    title: 'AI Engineering',
    tagline: 'Take models from notebook to production.',
    description:
      'Learn to design, ship and operate AI systems that real users rely on: data pipelines, model serving, evaluation, monitoring and MLOps, with LLM features built in from the start.',
    track: 'engineering',
    level: 'Intermediate → Advanced',
    badge: 'Most popular',
    forWho: ['Software and backend engineers moving into AI', 'Data scientists who want to ship to production', 'Engineers owning AI features in a product team'],
    prerequisites: ['Comfortable with Python', 'Basic ML concepts (or take ML & DL first)', 'Git and the command line'],
    outcomes: [
      'Ship an AI feature end to end: data, model, API, deployment and monitoring',
      'Choose between classical ML, fine-tuning and foundation-model APIs for a problem',
      'Set up evaluation, experiment tracking and CI/CD for models',
      'Control latency, cost and reliability of AI services in production',
    ],
    tools: ['Python', 'FastAPI', 'scikit-learn', 'PyTorch', 'MLflow', 'DVC', 'Docker', 'Kubernetes', 'AWS / Azure / GCP', 'Prometheus', 'OpenAI & Anthropic APIs'],
    modules: [
      { title: 'AI systems design', topics: ['Framing problems as ML/AI tasks', 'Choosing build vs buy vs foundation model', 'Data requirements and success metrics', 'Reference architectures for AI products'], lab: 'Write a design doc for an AI feature and defend the trade-offs' },
      { title: 'Data engineering for AI', topics: ['Ingestion, cleaning and validation', 'Feature engineering and feature stores', 'Dataset versioning with DVC', 'Labelling strategies and data quality checks'], lab: 'Build a reproducible training dataset pipeline' },
      { title: 'Training and experiment tracking', topics: ['Reproducible training runs', 'Hyperparameter search', 'Experiment tracking with MLflow', 'Model registry and versioning'], lab: 'Train, compare and register models with MLflow' },
      { title: 'Model serving and APIs', topics: ['Batch vs real-time inference', 'Serving models behind FastAPI', 'Containerising with Docker', 'Scaling, caching and GPU vs CPU trade-offs'], lab: 'Deploy a model as a production-grade REST API' },
      { title: 'LLMs inside products', topics: ['Calling foundation-model APIs well', 'Prompt design and structured outputs', 'Retrieval basics for grounding', 'Fallbacks, timeouts and cost control'], lab: 'Add an LLM-powered feature with a deterministic fallback' },
      { title: 'Evaluation and quality', topics: ['Offline metrics and test sets', 'LLM evaluation and LLM-as-judge', 'A/B testing and online metrics', 'Bias, fairness and robustness checks'], lab: 'Build an evaluation suite that gates releases' },
      { title: 'MLOps and CI/CD', topics: ['CI/CD for models and data', 'Infrastructure as code', 'Canary and shadow deployments', 'Rollbacks and model lifecycle'], lab: 'Automate train → test → deploy with GitHub Actions' },
      { title: 'Monitoring and responsible AI', topics: ['Data and concept drift', 'Latency, errors and cost dashboards', 'Incident response for AI systems', 'Governance, privacy and documentation'], lab: 'Instrument a deployed model and alert on drift' },
    ],
    projects: ['End-to-end prediction service with monitoring and automated retraining', 'LLM-assisted support tool with evaluation dashboard'],
  },
  {
    id: 'generative-ai',
    icon: '✨',
    title: 'Generative AI',
    tagline: 'Build reliable products on top of LLMs and diffusion models.',
    description:
      'Go from how large language models work to shipping grounded, evaluated GenAI applications: prompting, embeddings, RAG, fine-tuning, multimodal models, guardrails and deployment.',
    track: 'engineering',
    level: 'Intermediate',
    badge: 'In demand',
    forWho: ['Developers building LLM-powered apps', 'ML engineers moving to GenAI', 'Product engineers adding AI features'],
    prerequisites: ['Python and REST APIs', 'Basic understanding of ML (helpful, not required)'],
    outcomes: [
      'Explain how transformers, tokenisation and context windows shape LLM behaviour',
      'Build production RAG with chunking, hybrid search, reranking and citations',
      'Decide when to prompt, retrieve or fine-tune, and fine-tune with LoRA when it pays off',
      'Measure quality with evals and ship with guardrails and cost controls',
    ],
    tools: ['OpenAI', 'Anthropic Claude', 'Gemini', 'Hugging Face', 'LangChain', 'LlamaIndex', 'pgvector', 'Pinecone', 'Chroma', 'RAGAS', 'PEFT / LoRA', 'Stable Diffusion'],
    modules: [
      { title: 'How LLMs work', topics: ['Transformers and attention, intuitively', 'Tokens, context windows and sampling', 'Model families: open vs closed, small vs large', 'Strengths, limits and hallucinations'], lab: 'Compare models on the same task and explain the differences' },
      { title: 'Prompt engineering that holds up', topics: ['System prompts, few-shot and chain-of-thought', 'Structured outputs and JSON schemas', 'Prompt injection and how to defend against it', 'Versioning and testing prompts'], lab: 'Build a prompt test harness with regression cases' },
      { title: 'Embeddings and vector search', topics: ['What embeddings capture', 'Vector databases and indexes', 'Similarity, filtering and hybrid (BM25 + dense) search', 'Choosing an embedding model'], lab: 'Semantic search over your own documents' },
      { title: 'Retrieval-augmented generation (RAG)', topics: ['Ingestion and chunking strategies', 'Reranking and query rewriting', 'Citations and grounded answers', 'Advanced RAG: multi-hop, GraphRAG, agentic retrieval'], lab: 'A cited Q&A assistant over a real document set' },
      { title: 'Fine-tuning and adaptation', topics: ['When fine-tuning beats RAG (and when it does not)', 'Dataset preparation', 'LoRA / QLoRA with PEFT', 'Evaluating a fine-tuned model'], lab: 'Fine-tune an open model for a domain task' },
      { title: 'Multimodal generative AI', topics: ['Vision-language models', 'Diffusion models for images', 'Speech: transcription and text-to-speech', 'Document and image understanding'], lab: 'An app that reads invoices or screenshots and acts on them' },
      { title: 'Evaluation, safety and guardrails', topics: ['Building eval datasets', 'Automatic and human evaluation', 'Guardrails, moderation and PII handling', 'Responsible-AI practices'], lab: 'Eval suite with RAGAS plus guardrails on a RAG app' },
      { title: 'Shipping GenAI apps', topics: ['Streaming UIs and latency', 'Caching, batching and cost control', 'Observability and tracing', 'Deployment patterns'], lab: 'Deploy a full-stack GenAI app with monitoring' },
    ],
    projects: ['Production RAG assistant with citations, evals and a chat UI', 'Domain fine-tuned model compared against a RAG baseline'],
  },
  {
    id: 'agentic-ai',
    icon: '🧠',
    title: 'Agentic AI Engineering',
    tagline: 'Design agents that plan, use tools and get real work done.',
    description:
      'Build AI agents and multi-agent systems that are reliable enough for production: tool calling, planning, memory, orchestration with LangGraph, the Model Context Protocol, evaluation and human oversight.',
    track: 'engineering',
    level: 'Advanced',
    badge: 'New',
    forWho: ['Engineers who already build with LLMs', 'Teams automating multi-step workflows', 'Founders building agent-based products'],
    prerequisites: ['Generative AI track or equivalent LLM experience', 'Solid Python and APIs'],
    outcomes: [
      'Choose between a single LLM call, a workflow and an autonomous agent',
      'Build tool-using agents with planning, memory and error recovery',
      'Orchestrate multi-agent systems and connect tools through MCP',
      'Evaluate, observe and safely deploy agents with human-in-the-loop controls',
    ],
    tools: ['LangGraph', 'LangChain', 'OpenAI Agents SDK', 'Claude tool use', 'CrewAI', 'AutoGen', 'Model Context Protocol (MCP)', 'LangSmith', 'Langfuse', 'FastAPI', 'Redis'],
    modules: [
      { title: 'Agent foundations', topics: ['Workflows vs agents: picking the simplest thing that works', 'The ReAct loop and reasoning patterns', 'Function calling and structured tool use', 'Failure modes of agents'], lab: 'A tool-using agent that answers questions from live data' },
      { title: 'Tools, APIs and the Model Context Protocol', topics: ['Designing good tools for models', 'Building and consuming MCP servers', 'Authentication and permissions for tools', 'Sandboxing code execution'], lab: 'Build an MCP server and connect it to an agent' },
      { title: 'Planning and reasoning', topics: ['Task decomposition and planning', 'Reflection and self-correction', 'Routing between specialised prompts and models', 'Long-running tasks and checkpoints'], lab: 'A planner–executor agent for a multi-step research task' },
      { title: 'Memory and state', topics: ['Short-term vs long-term memory', 'Retrieval-based memory', 'State machines and graphs with LangGraph', 'Persistence and resumability'], lab: 'An assistant that remembers users across sessions' },
      { title: 'Multi-agent systems', topics: ['Supervisor, hierarchical and swarm patterns', 'Agent-to-agent communication', 'Shared state and conflict resolution', 'When multi-agent is overkill'], lab: 'A multi-agent team that drafts and reviews a report' },
      { title: 'Evaluation and observability', topics: ['Trajectory and outcome evaluation', 'Tracing with LangSmith / Langfuse', 'Regression testing agents', 'Cost and latency budgets'], lab: 'Trace, evaluate and improve an underperforming agent' },
      { title: 'Safety and human-in-the-loop', topics: ['Guardrails and permission boundaries', 'Prompt injection through tools and content', 'Approval steps and escalation', 'Audit logs and accountability'], lab: 'Add approvals and guardrails to an agent that takes actions' },
      { title: 'Production agent systems', topics: ['Deploying agents as services', 'Queues, retries and timeouts', 'Scaling and rate limits', 'Operating agents in a business'], lab: 'Deploy an agent behind an API with monitoring' },
    ],
    projects: ['Autonomous operations agent that triages tickets with human approval', 'Multi-agent research and reporting system with full tracing'],
  },
  {
    id: 'ml-dl',
    icon: '📈',
    title: 'Machine Learning & Deep Learning',
    tagline: 'The foundations every serious AI career is built on.',
    description:
      'Learn the maths, algorithms and practice behind modern AI: classical machine learning, neural networks, computer vision, sequence models and transformers, built hands-on in Python and PyTorch.',
    track: 'engineering',
    level: 'Beginner → Intermediate',
    forWho: ['Students and graduates starting in AI', 'Developers who want real ML foundations', 'Analysts moving into data science'],
    prerequisites: ['Basic Python', 'School-level maths (we refresh the rest)'],
    outcomes: [
      'Understand the linear algebra, probability and calculus behind models',
      'Build, evaluate and tune classical ML models properly',
      'Train neural networks for vision and language in PyTorch',
      'Read papers and reproduce results with confidence',
    ],
    tools: ['Python', 'NumPy', 'pandas', 'Matplotlib', 'scikit-learn', 'XGBoost', 'PyTorch', 'Hugging Face', 'Jupyter', 'Weights & Biases'],
    modules: [
      { title: 'Python and data for ML', topics: ['NumPy and pandas fluency', 'Exploratory data analysis', 'Visualisation that tells a story', 'Data cleaning and leakage'], lab: 'EDA report on a real-world dataset' },
      { title: 'Maths for machine learning', topics: ['Vectors, matrices and transformations', 'Probability, distributions and Bayes', 'Derivatives, gradients and optimisation', 'Statistics for evaluation'], lab: 'Implement gradient descent from scratch' },
      { title: 'Supervised learning', topics: ['Linear and logistic regression', 'Decision trees and random forests', 'Gradient boosting (XGBoost, LightGBM)', 'Support vector machines'], lab: 'Predict customer churn and explain the drivers' },
      { title: 'Model evaluation and tuning', topics: ['Train/validation/test and cross-validation', 'Metrics for imbalanced problems', 'Hyperparameter tuning', 'Explainability with SHAP'], lab: 'Tune and explain a model for a business decision' },
      { title: 'Unsupervised learning', topics: ['Clustering (k-means, DBSCAN)', 'Dimensionality reduction (PCA, UMAP)', 'Anomaly detection', 'Recommendation basics'], lab: 'Customer segmentation and anomaly detection' },
      { title: 'Neural networks and deep learning', topics: ['Perceptrons to multilayer networks', 'Backpropagation and optimisers', 'Regularisation, dropout and normalisation', 'Training in PyTorch'], lab: 'Build and train a neural network in PyTorch' },
      { title: 'Computer vision', topics: ['Convolutional neural networks', 'Transfer learning', 'Object detection and segmentation', 'Data augmentation'], lab: 'Image classifier with transfer learning' },
      { title: 'Sequence models and transformers', topics: ['Embeddings and RNNs/LSTMs', 'Attention and the transformer', 'Pre-trained language models', 'Fine-tuning with Hugging Face'], lab: 'Fine-tune a transformer for text classification' },
    ],
    projects: ['End-to-end tabular ML project with explainability', 'Deep learning project in vision or NLP, from data to demo'],
  },
  {
    id: 'full-stack',
    icon: '💻',
    title: 'Full Stack Development',
    tagline: 'Build and ship modern web products, front to back.',
    description:
      'Become a product-ready developer: modern JavaScript and TypeScript, React and Next.js, APIs, databases, authentication, testing, DevOps and system design, with AI features woven into what you build.',
    track: 'engineering',
    level: 'Beginner → Intermediate',
    forWho: ['Students and freshers starting a tech career', 'Career switchers into software', 'Developers who want to go full stack'],
    prerequisites: ['None for the core path: we start from web fundamentals'],
    outcomes: [
      'Build responsive, accessible front ends in React and Next.js',
      'Design REST APIs, data models and authentication',
      'Test, containerise and deploy applications with CI/CD',
      'Reason about scalability and basic system design',
    ],
    tools: ['HTML', 'CSS', 'Tailwind', 'JavaScript', 'TypeScript', 'React', 'Next.js', 'Node.js', 'Express', 'PostgreSQL', 'MongoDB', 'Prisma', 'Docker', 'GitHub Actions', 'Vercel'],
    modules: [
      { title: 'Web fundamentals', topics: ['How the web works: HTTP, DNS, browsers', 'Semantic HTML and accessibility', 'Modern CSS, Flexbox, Grid and Tailwind', 'Git and GitHub workflows'], lab: 'A responsive, accessible portfolio site' },
      { title: 'JavaScript and TypeScript', topics: ['Core JavaScript and the event loop', 'Async code, promises and fetch', 'TypeScript types and generics', 'Modules, tooling and debugging'], lab: 'A typed, interactive web app without a framework' },
      { title: 'React and Next.js', topics: ['Components, state and hooks', 'Routing, layouts and data fetching', 'Server components and rendering strategies', 'Forms, validation and UX'], lab: 'A multi-page Next.js app with server rendering' },
      { title: 'Back-end and APIs', topics: ['Node.js and Express', 'REST design and versioning', 'Validation, errors and logging', 'File uploads, email and background jobs'], lab: 'A production-style REST API' },
      { title: 'Databases', topics: ['Relational modelling with PostgreSQL', 'Document modelling with MongoDB', 'ORMs and migrations', 'Indexes, queries and performance'], lab: 'Design and query the data layer of a SaaS product' },
      { title: 'Authentication and security', topics: ['Sessions, JWT and OAuth', 'Authorisation and roles', 'OWASP Top 10 for web apps', 'Secrets and environment management'], lab: 'Add Google sign-in and role-based access' },
      { title: 'Testing, DevOps and deployment', topics: ['Unit, integration and end-to-end tests', 'Docker and containers', 'CI/CD with GitHub Actions', 'Deploying to Vercel and the cloud'], lab: 'Automated test and deploy pipeline' },
      { title: 'System design and AI features', topics: ['Caching, queues and scaling basics', 'Designing for reliability', 'Adding LLM features to web apps', 'Monitoring and analytics'], lab: 'Add an AI assistant to your full-stack app' },
    ],
    projects: ['Full-stack SaaS app with auth, payments-ready architecture and an AI feature', 'Real-time collaborative app deployed with CI/CD'],
  },
  {
    id: 'dsa',
    icon: '🧩',
    title: 'Data Structures & Algorithms',
    tagline: 'Think like an engineer and crack technical interviews.',
    description:
      'Master problem-solving the way top companies test it: complexity analysis, core data structures and the patterns behind hundreds of interview questions, with mock interviews and code reviews.',
    track: 'engineering',
    level: 'Beginner → Advanced',
    forWho: ['Students preparing for placements', 'Developers preparing for product-company interviews', 'Anyone who wants stronger problem-solving'],
    prerequisites: ['Basic programming in Python, Java, C++ or JavaScript'],
    outcomes: [
      'Analyse time and space complexity confidently',
      'Recognise and apply the core problem-solving patterns',
      'Solve medium and hard problems in a structured way',
      'Communicate solutions clearly in technical interviews',
    ],
    tools: ['Python', 'Java', 'C++', 'JavaScript', 'LeetCode', 'Codeforces', 'Excalidraw'],
    modules: [
      { title: 'Foundations', topics: ['Big-O time and space complexity', 'Recursion and the call stack', 'Arrays and strings', 'Problem-solving framework'], lab: 'Analyse and optimise brute-force solutions' },
      { title: 'Core patterns', topics: ['Two pointers and sliding window', 'Prefix sums and hashing', 'Binary search on answers', 'Sorting and intervals'], lab: 'Pattern drills on curated problem sets' },
      { title: 'Linear data structures', topics: ['Linked lists', 'Stacks and monotonic stacks', 'Queues and deques', 'Design problems (LRU cache and more)'], lab: 'Implement core structures from scratch' },
      { title: 'Trees and heaps', topics: ['Binary trees and traversals', 'Binary search trees', 'Heaps and priority queues', 'Tries'], lab: 'Tree and heap problem sprint' },
      { title: 'Graphs', topics: ['BFS and DFS', 'Topological sort', 'Shortest paths (Dijkstra, Bellman–Ford)', 'Union-find and minimum spanning trees'], lab: 'Model real problems as graphs' },
      { title: 'Recursion, backtracking and greedy', topics: ['Subsets, permutations and combinations', 'Constraint problems with backtracking', 'Greedy choices and proofs', 'Divide and conquer'], lab: 'Backtracking and greedy problem sprint' },
      { title: 'Dynamic programming', topics: ['Memoisation vs tabulation', '1D and 2D DP patterns', 'Knapsack, LIS, LCS and edit distance', 'DP on trees and graphs'], lab: 'From recursion to optimised DP' },
      { title: 'Interview mastery', topics: ['Advanced structures: segment trees, Fenwick trees', 'Bit manipulation', 'Communicating your approach', 'Mock interviews with feedback'], lab: 'Timed mock interviews with a mentor' },
    ],
    projects: ['Curated problem roadmap solved with written explanations', 'Mock interview portfolio with mentor feedback'],
  },
  {
    id: 'ai-mastery',
    icon: '🚀',
    title: 'AI Mastery Program',
    tagline: 'Every engineering track as one guided path, zero to agentic.',
    description:
      'Our complete program. Start with problem-solving and full-stack fundamentals, build real ML and deep learning skills, then go deep on AI engineering, generative AI and agentic systems, with a dedicated mentor and career support all the way.',
    track: 'flagship',
    level: 'Beginner → Advanced',
    badge: 'Flagship',
    forWho: ['Students who want a complete, career-ready path', 'Career switchers who want one structured program', 'Developers aiming for AI engineering roles'],
    prerequisites: ['Commitment and curiosity: we start from fundamentals'],
    outcomes: [
      'Everything from the six engineering tracks, in the right order',
      'A portfolio of shipped projects across web, ML, GenAI and agents',
      'Interview readiness for software and AI engineering roles',
      'A capstone product you can demo to employers or investors',
    ],
    tools: ['Everything across the engineering tracks'],
    modules: [
      { title: 'Stage 1 · Problem solving (DSA)', topics: ['Complexity and core data structures', 'Interview patterns', 'Dynamic programming and graphs'], lab: 'Problem-solving roadmap with mentor reviews' },
      { title: 'Stage 2 · Full stack development', topics: ['React, Next.js and TypeScript', 'APIs, databases and auth', 'Testing and deployment'], lab: 'Ship a full-stack web product' },
      { title: 'Stage 3 · Machine learning & deep learning', topics: ['Maths and classical ML', 'Neural networks in PyTorch', 'Vision and transformers'], lab: 'End-to-end ML project' },
      { title: 'Stage 4 · AI engineering', topics: ['Serving and MLOps', 'Evaluation and monitoring', 'LLMs inside products'], lab: 'Production AI service with monitoring' },
      { title: 'Stage 5 · Generative AI', topics: ['Prompting and embeddings', 'Production RAG', 'Fine-tuning and evals'], lab: 'Cited RAG assistant with evals' },
      { title: 'Stage 6 · Agentic AI', topics: ['Tool use and MCP', 'Multi-agent orchestration', 'Safety and observability'], lab: 'Multi-agent system with human approval' },
      { title: 'Capstone and career launch', topics: ['Capstone product, built and demoed', 'Portfolio, résumé and LinkedIn review', 'Mock interviews and referrals guidance'], lab: 'Demo day with industry reviewers' },
    ],
    projects: ['A full-stack AI product combining web, RAG and agents', 'Portfolio of stage projects reviewed by mentors'],
  },
  {
    id: 'ai-for-everyone',
    icon: '🌍',
    title: 'AI for Everyone',
    tagline: 'Put AI to work in your business, no coding required.',
    description:
      'For founders, managers, vendors and teams who want results, not theory: understand what AI can and cannot do, use today’s AI tools well, find the processes worth automating and build a practical AI roadmap for your operations.',
    track: 'business',
    level: 'All levels · No coding',
    forWho: ['Business owners, founders and vendors', 'Managers and operations, sales, marketing, HR and finance teams', 'Anyone who wants to use AI confidently at work'],
    prerequisites: ['None'],
    outcomes: [
      'Explain how modern AI works and where it fails, in plain language',
      'Use AI assistants productively and safely every day',
      'Spot high-value AI use cases in your own operations',
      'Estimate ROI and build a practical adoption roadmap',
    ],
    tools: ['ChatGPT', 'Claude', 'Gemini', 'Microsoft Copilot', 'NotebookLM', 'Zapier', 'Make', 'Canva AI'],
    modules: [
      { title: 'AI, demystified', topics: ['What AI, ML and GenAI really are', 'What AI does well and where it fails', 'Hallucinations and how to catch them', 'The AI landscape for businesses'], lab: 'Live tour of AI tools on your own tasks' },
      { title: 'Working with AI assistants', topics: ['Prompting that gets useful results', 'Writing, summarising and analysing with AI', 'Research and decision support', 'Building your personal AI workflow'], lab: 'Automate one weekly task end to end' },
      { title: 'AI across business functions', topics: ['Sales and marketing', 'Customer service and support', 'Operations, supply chain and procurement', 'Finance, HR and administration'], lab: 'Map AI opportunities in your own business' },
      { title: 'Automating operations', topics: ['No-code automation with Zapier and Make', 'Chatbots and assistants for customers', 'Document processing and data entry', 'Working with vendors and AI solutions'], lab: 'Build a no-code AI automation for a real process' },
      { title: 'Data, privacy and responsible AI', topics: ['What data you can and cannot share', 'Security, IP and compliance basics', 'Bias and fairness', 'An AI usage policy for your team'], lab: 'Draft a one-page AI policy' },
      { title: 'Your AI roadmap and ROI', topics: ['Prioritising use cases by value and effort', 'Estimating cost and ROI', 'Build, buy or partner', 'Change management and adoption'], lab: 'Leave with a prioritised AI roadmap for your business' },
    ],
    projects: ['Your own AI opportunity map and adoption roadmap', 'A working no-code AI automation for one business process'],
  },
  {
    id: 'corporate',
    icon: '🏢',
    title: 'Corporate AI Training',
    tagline: 'Upskill your entire organisation, tailored to your business.',
    description:
      'Custom programs for companies: AI strategy for leadership, hands-on tracks for engineering and data teams, AI productivity for every employee and an AI champions network, built around your tools, data and goals.',
    track: 'business',
    level: 'Leadership to engineering teams',
    forWho: ['Leadership teams setting AI strategy', 'Engineering, data and product teams', 'Whole organisations rolling out AI tools', 'L&D and HR teams planning capability building'],
    prerequisites: ['A short discovery call to understand your goals'],
    outcomes: [
      'A shared AI vocabulary and strategy across leadership',
      'Engineering teams shipping AI features with best practices',
      'Every employee using approved AI tools productively and safely',
      'Measurable adoption and a pipeline of internal AI use cases',
    ],
    tools: ['Microsoft 365 Copilot', 'Google Workspace', 'Azure / AWS / GCP', 'Your internal tools'],
    modules: [
      { title: 'Discovery and skills assessment', topics: ['Goals, current skills and gaps', 'AI readiness of teams and data', 'Use-case discovery workshops', 'Success metrics agreed up front'], lab: 'Assessment report with a recommended program' },
      { title: 'AI strategy for leadership', topics: ['AI opportunities and risks for your industry', 'Building an AI roadmap and business case', 'Governance and responsible AI', 'Leading AI-driven change'], lab: 'Leadership workshop producing a prioritised roadmap' },
      { title: 'AI productivity for every employee', topics: ['Using approved AI tools well', 'Function-specific playbooks', 'Data handling and AI policy', 'Sharing wins and best practices'], lab: 'Team workshops on real day-to-day tasks' },
      { title: 'Technical tracks for engineering teams', topics: ['Any of our engineering tracks, customised', 'Your codebase, your stack, your data', 'Hands-on labs and code reviews', 'Architecture reviews of live projects'], lab: 'Teams ship an internal AI prototype' },
      { title: 'AI champions program', topics: ['Training internal AI champions', 'Running use-case pipelines', 'Internal communities of practice', 'Ongoing mentorship for champions'], lab: 'Champions lead their first internal AI initiative' },
      { title: 'Measurement and continuous improvement', topics: ['Adoption and impact metrics', 'Post-program assessments', 'Follow-up clinics and office hours', 'Refreshers as tools evolve'], lab: 'Impact report for leadership' },
    ],
    projects: ['Internal AI prototype built on your own data', 'Organisation-wide AI adoption playbook'],
  },
]

export const programById = (id: string) => programs.find((p) => p.id === id)

/* ── Course finder ───────────────────────────────────────────────────────────
   Three questions; each answer adds points to programs. Highest score wins. */

export interface FinderOption {
  id: string
  label: string
  icon: string
  scores: Partial<Record<string, number>>
  reason?: string
}

export interface FinderQuestion {
  id: string
  question: string
  options: FinderOption[]
}

export const finderQuestions: FinderQuestion[] = [
  {
    id: 'role',
    question: 'What describes you best?',
    options: [
      { id: 'student', label: 'Student or fresher', icon: '🎓', scores: { dsa: 2, 'full-stack': 2, 'ml-dl': 2, 'ai-mastery': 3 } },
      { id: 'developer', label: 'Software developer', icon: '👩‍💻', scores: { 'ai-engineering': 3, 'generative-ai': 3, 'agentic-ai': 2, dsa: 1 } },
      { id: 'data', label: 'Data or ML practitioner', icon: '📊', scores: { 'ml-dl': 2, 'ai-engineering': 3, 'generative-ai': 3, 'agentic-ai': 2 } },
      { id: 'switcher', label: 'Switching careers into tech', icon: '🔁', scores: { 'ai-mastery': 4, 'full-stack': 2, 'ai-for-everyone': 1 } },
      { id: 'business', label: 'Founder, manager or business team', icon: '💼', scores: { 'ai-for-everyone': 5, corporate: 2 } },
      { id: 'company', label: 'Company or L&D team', icon: '🏢', scores: { corporate: 6, 'ai-for-everyone': 2 } },
    ],
  },
  {
    id: 'goal',
    question: 'What do you want to achieve?',
    options: [
      { id: 'job', label: 'Crack interviews and land a tech job', icon: '🎯', scores: { dsa: 3, 'full-stack': 2, 'ai-mastery': 3 }, reason: 'it builds the problem-solving and portfolio that interviews test' },
      { id: 'web', label: 'Build and ship web products', icon: '💻', scores: { 'full-stack': 5 }, reason: 'it takes you from web fundamentals to deployed products' },
      { id: 'ml', label: 'Build machine learning models', icon: '📈', scores: { 'ml-dl': 5, 'ai-engineering': 2 }, reason: 'it covers the maths, algorithms and deep learning you need' },
      { id: 'genai', label: 'Build apps with LLMs and GenAI', icon: '✨', scores: { 'generative-ai': 5, 'ai-engineering': 2 }, reason: 'it goes deep on prompting, RAG, fine-tuning and evaluation' },
      { id: 'agents', label: 'Build AI agents that do real work', icon: '🧠', scores: { 'agentic-ai': 5, 'generative-ai': 2 }, reason: 'it is built around tool use, planning, MCP and multi-agent systems' },
      { id: 'everything', label: 'Become a complete AI engineer', icon: '🚀', scores: { 'ai-mastery': 6 }, reason: 'it combines every engineering track into one guided path' },
      { id: 'business', label: 'Use AI in my business', icon: '🌍', scores: { 'ai-for-everyone': 5 }, reason: 'it shows how to apply AI across your operations without coding' },
      { id: 'team', label: 'Train my team or company', icon: '🏢', scores: { corporate: 6 }, reason: 'it is tailored to your organisation, tools and goals' },
    ],
  },
  {
    id: 'coding',
    question: 'How comfortable are you with coding?',
    options: [
      { id: 'none', label: 'I don’t code', icon: '🙂', scores: { 'ai-for-everyone': 3, corporate: 1, 'ai-mastery': 1, 'agentic-ai': -4, 'ai-engineering': -3, 'generative-ai': -2, dsa: -2 } },
      { id: 'beginner', label: 'Just getting started', icon: '🌱', scores: { dsa: 1, 'full-stack': 2, 'ml-dl': 1, 'ai-mastery': 2, 'agentic-ai': -3, 'ai-engineering': -2 } },
      { id: 'comfortable', label: 'Comfortable with one language', icon: '👍', scores: { 'generative-ai': 1, 'ai-engineering': 1, 'ml-dl': 1, dsa: 1 } },
      { id: 'advanced', label: 'I build software professionally', icon: '⚡', scores: { 'agentic-ai': 2, 'ai-engineering': 2, 'generative-ai': 1, 'full-stack': -1 } },
    ],
  },
]

export interface FinderResult {
  best: Program
  reason: string
  alternatives: Program[]
}

export function recommend(answers: Record<string, string>): FinderResult {
  const score: Record<string, number> = Object.fromEntries(programs.map((p) => [p.id, 0]))
  for (const q of finderQuestions) {
    const opt = q.options.find((o) => o.id === answers[q.id])
    for (const [id, pts] of Object.entries(opt?.scores ?? {})) score[id] += pts ?? 0
  }
  // Ties keep catalogue order, so results are stable.
  const ranked = [...programs].sort((a, b) => score[b.id] - score[a.id])
  const best = ranked[0]
  const goal = finderQuestions[1].options.find((o) => o.id === answers.goal)
  // Use the goal's explanation only when the goal's main program won; otherwise describe the winner.
  const goalTop = goal && Object.entries(goal.scores).sort((x, y) => (y[1] ?? 0) - (x[1] ?? 0))[0]?.[0]
  const reason = goal?.reason && goalTop === best.id ? goal.reason : `it fits where you are today: ${best.tagline.charAt(0).toLowerCase()}${best.tagline.slice(1)}`
  return { best, reason, alternatives: ranked.slice(1, 3) }
}

export const mentorship = [
  { icon: '🧑‍🏫', title: '1:1 mentorship', description: 'A dedicated mentor who works in industry reviews your progress, unblocks you and adapts the plan to your goals.' },
  { icon: '🔍', title: 'Code and project reviews', description: 'Detailed feedback on every project, the way a senior engineer reviews a pull request.' },
  { icon: '🛠️', title: 'Project-first learning', description: 'Every module ends with a hands-on lab, and every track ends with portfolio projects you can show.' },
  { icon: '🎤', title: 'Mock interviews', description: 'Technical and system-design mock interviews with structured, honest feedback.' },
  { icon: '🧭', title: 'Career guidance', description: 'Portfolio, résumé and LinkedIn reviews, plus guidance on roles, companies and growth.' },
  { icon: '🏅', title: 'Certificate of completion', description: 'A uniAiverse certificate backed by real, reviewed project work.' },
]

export const learningSteps = [
  { title: 'Talk to us', description: 'A free call to understand your background and goals.' },
  { title: 'Get your path', description: 'We recommend the right track and tailor the plan to you.' },
  { title: 'Learn by building', description: 'Live sessions, hands-on labs and projects with your mentor.' },
  { title: 'Launch', description: 'Capstone, portfolio, mock interviews and your next step.' },
]

export const faqs = [
  { q: 'How long does a program take?', a: 'There is no fixed timeline. Programs are mentor-led and adapt to your pace and background, so you move ahead when you have genuinely mastered each module.' },
  { q: 'Do I need a technical background?', a: 'Not for AI for Everyone, Full Stack Development or the AI Mastery Program, which start from fundamentals. The advanced tracks list their prerequisites, and we will suggest where to start.' },
  { q: 'Are classes live or recorded?', a: 'Both. You get live, interactive sessions with mentors plus self-paced materials, labs and projects.' },
  { q: 'Will I get a certificate?', a: 'Yes. You receive a uniAiverse certificate when you complete your track and its reviewed projects.' },
  { q: 'Can you train our whole company?', a: 'Yes. Corporate AI Training is built around your goals, tools and data, from leadership workshops to hands-on engineering tracks. Reach out and we will design a program with you.' },
  { q: 'Do you help with jobs?', a: 'We provide portfolio and résumé reviews, mock interviews and career guidance. We do not promise placements, but we make sure you are ready for them.' },
]
