// Training catalogue. Source of truth: the official "Corporate AI Training Catalogue" brochure
// (25 courses, 10 tracks) and the "Agentic AI & LLM Economics" workshop preview deck.
// Do not add courses, durations or claims here that are not in those documents.

export type Level = 1 | 2 | 3 | 4

export const levels: Record<Level, { label: string; short: string }> = {
  1: { label: 'Awareness', short: 'L1' },
  2: { label: 'Practitioner', short: 'L2' },
  3: { label: 'Builder', short: 'L3' },
  4: { label: 'Advanced', short: 'L4' },
}

export interface Course {
  id: string
  title: string
  /** Text the brochure prints after the title (scope or format). */
  detail?: string
  level: Level
  /** Contact hours as printed in the brochure. */
  duration: string
}

export interface Track {
  id: string
  icon: string
  label: string
  audience: string
  courses: Course[]
  /** The career track for individuals; shown apart from the corporate tracks. */
  individual?: boolean
}

export const tracks: Track[] = [
  {
    id: 'ai-for-all',
    icon: '🌍',
    label: 'AI for All',
    audience: 'Every employee',
    courses: [
      { id: 'ai-for-all', title: 'AI for All', level: 1, duration: '4 h' },
      { id: 'safe-responsible-ai', title: 'Safe & Responsible AI Use at Work', level: 1, duration: '1.5 h' },
      { id: 'ai-productivity-workflows', title: 'AI Productivity Workflows', level: 1, duration: '4 h' },
    ],
  },
  {
    id: 'leadership',
    icon: '🏛️',
    label: 'AI Leadership & Board',
    audience: 'CXOs · board · founders',
    courses: [
      { id: 'executive-board-briefing', title: 'AI Executive & Board Briefing', level: 2, duration: '2 h' },
      { id: 'ai-for-business-leaders', title: 'AI for Business Leaders', level: 2, duration: '8 h' },
      { id: 'ai-governance-for-leaders', title: 'AI Governance for Leaders', level: 2, duration: '4 h' },
      { id: 'llm-cost-estimation', title: 'Calculating LLM Cost & Estimation Strategies', level: 1, duration: '4 h' },
    ],
  },
  {
    id: 'business',
    icon: '💼',
    label: 'AI for Business',
    audience: 'Managers · analysts · product',
    courses: [
      { id: 'use-case-design', title: 'AI Use-Case Design & Product Ownership', level: 2, duration: '8 h' },
      { id: 'build-your-own-ai-bot', title: 'Build Your Own AI Bot', detail: 'RAG, non-technical', level: 2, duration: '22 h' },
      { id: 'agentic-ai-llm-economics', title: 'Agentic AI & LLM Economics', detail: 'Working workshop', level: 2, duration: '1–2 days' },
    ],
  },
  {
    id: 'sales',
    icon: '📈',
    label: 'AI for Sales',
    audience: 'Reps · SDRs · RevOps',
    courses: [
      { id: 'ai-for-sales', title: 'AI for Sales', level: 1, duration: '4 h' },
      { id: 'agents-for-sales-ops', title: 'AI Agents for Sales Operations', level: 2, duration: '4 h' },
    ],
  },
  {
    id: 'marketing',
    icon: '📣',
    label: 'AI for Marketing',
    audience: 'Marketing · content · brand',
    courses: [
      { id: 'ai-for-marketing', title: 'AI for Marketing', level: 1, duration: '4 h' },
      { id: 'content-governance', title: 'AI Content Governance & Brand Safety', level: 2, duration: '2 h' },
    ],
  },
  {
    id: 'genai-engineer',
    icon: '🧠',
    label: 'GenAI Engineer',
    audience: 'Developers building LLM apps',
    courses: [
      { id: 'genai-engineer', title: 'GenAI Engineer', level: 3, duration: '32 h' },
      { id: 'advanced-rag', title: 'Advanced, Hybrid & Agentic RAG', level: 3, duration: '8 h' },
      { id: 'agentic-ai-engineer', title: 'Agentic AI Engineer', detail: 'Tools, MCP, memory, reliability, evals', level: 4, duration: '24 h' },
      { id: 'ai-evaluation', title: 'AI Evaluation & Quality Engineering', level: 3, duration: '8 h' },
      { id: 'ai-security', title: 'AI Security for Builders', level: 3, duration: '8 h' },
    ],
  },
  {
    id: 'ai-engineer',
    icon: '⚙️',
    label: 'AI Engineer',
    audience: 'Software & data engineers',
    courses: [
      { id: 'ai-engineer', title: 'AI Engineer', level: 2, duration: '32 h' },
      { id: 'ai-dev-lifecycle', title: 'AI Development & Deployment Lifecycle', level: 2, duration: '8 h' },
    ],
  },
  {
    id: 'data-mlops',
    icon: '🗄️',
    label: 'Data & MLOps',
    audience: 'Data · ML · platform teams',
    courses: [
      { id: 'data-foundations', title: 'Data Foundations for AI', level: 2, duration: '16 h' },
      { id: 'mlops-llmops', title: 'MLOps & LLMOps', level: 3, duration: '16 h' },
      { id: 'ai-finops', title: 'AI FinOps', level: 2, duration: '4 h' },
    ],
  },
  {
    id: 'grc',
    icon: '🛡️',
    label: 'AI Governance, Risk & Compliance',
    audience: 'Risk · legal · audit · security',
    courses: [
      { id: 'governance-practitioner', title: 'AI Governance Practitioner', detail: 'EU AI Act · NIST AI RMF · ISO 42001', level: 3, duration: '16 h' },
    ],
  },
  {
    id: 'individual',
    icon: '🚀',
    label: 'Individual Professionals',
    audience: 'Career track → mentorship program',
    individual: true,
    courses: [
      {
        id: 'genai-agentic-cohort',
        title: 'Generative & Agentic AI Engineer',
        detail: '3-month cohort · capstone, audits, verified certificate',
        level: 3,
        duration: '12 wk',
      },
    ],
  },
]

export const corporateTracks = tracks.filter((t) => !t.individual)
export const individualTrack = tracks.find((t) => t.individual)!
export const allCourses = tracks.flatMap((t) => t.courses.map((c) => ({ ...c, track: t })))
export type CourseWithTrack = (typeof allCourses)[number]

/** The course that has its own workshop preview section on the training page. */
export const WORKSHOP_COURSE_ID = 'agentic-ai-llm-economics'

export const brochure = {
  title: 'Corporate AI Training Catalogue',
  intro:
    'Every course ships as a delivery kit: slides with speaker notes, facilitator guide, exercises, handouts, runnable demos and an assessment with a rubric.',
  aiModes: 'Runs offline with zero AI keys, or live with a budgeted classroom AI pool.',
  chips: [
    { icon: '📍', text: 'Onsite Pune & travel · virtual' },
    { icon: '🗣️', text: 'English' },
    { icon: '🎯', text: 'Customised to your context before delivery' },
    { icon: '📦', text: 'Materials stay usable after delivery' },
    { icon: '🏅', text: 'Verified certificates' },
  ],
  kit: [
    { icon: '🖥️', text: 'Slides with speaker notes' },
    { icon: '🧑‍🏫', text: 'Facilitator guide' },
    { icon: '✍️', text: 'Exercises' },
    { icon: '📄', text: 'Handouts' },
    { icon: '💻', text: 'Runnable demos' },
    { icon: '✅', text: 'Assessment with a rubric' },
  ],
  legend:
    'Hours are contact hours; labs and assessments included. Tracks can be combined into a role-based programme with baseline and exit readiness audits.',
  process: [
    { title: 'Discover', description: 'Free readiness check or a 30-min call → the right track and level for each audience.' },
    { title: 'Customise', description: 'Your documents, your workflows and your sector go into the labs before day one.' },
    { title: 'Deliver', description: 'Mixed rooms work: every lab has a no-code path and a code path. Offline or live AI.' },
    { title: 'Verify', description: 'Assessment with rubric, verified certificate, cohort report for L&D and managers.' },
  ],
  cta: 'Book a track, a course, or a 2-day workshop',
  email: 'training@uniaiverse.ai',
}

// ── Workshop preview: "Agentic AI & LLM Economics" (slides 1–5 of 41) ──────

export type WorkshopSlide =
  | { kind: 'cover'; kicker: string; title: string; meta: string; lead: string; chips: string[] }
  | { kind: 'analogy'; kicker: string; title: string; story: string[]; mapping: { thing: string; is: string }[] }
  | { kind: 'lab'; kicker: string; title: string; steps: string[]; badge: string; note: string[] }
  | { kind: 'concept'; kicker: string; title: string; points: string[]; quote: string }
  | { kind: 'tokens'; kicker: string; title: string; facts: { value: string; label: string }[]; example: { label: string; pasted: number; fetched: number } }

export const workshop: { title: string; totalSlides: number; more: string; slides: WorkshopSlide[] } = {
  title: 'Agentic AI & LLM Economics',
  totalSlides: 41,
  more: '36 more slides, 5 labs, 7 runnable demos',
  slides: [
    {
      kind: 'cover',
      kicker: 'Corporate workshop · 1 or 2 days · onsite or virtual',
      title: 'Understand, build, cost, decide.',
      meta: 'Agentic AI & LLM Economics — a working workshop',
      lead: 'By 5 pm on day two you’ll have built a grounded assistant and a working agent on your own material — and you’ll know what it costs and what it returns.',
      chips: ['Leaders decide', 'Analysts frame', 'Engineers build', 'Every lab: no-code path + code path'],
    },
    {
      kind: 'analogy',
      kicker: 'The one analogy for two days',
      title: 'A brilliant new colleague',
      story: [
        'They have read everything public and nothing internal.',
        'Ask them about your refund policy and you get a confident, plausible, invented answer.',
        'You don’t fire them. You build them a library.',
        'An agent is that colleague with a phone, a budget and permission to make calls — which is why you give them rules.',
      ],
      mapping: [
        { thing: 'The library', is: 'RAG' },
        { thing: 'The phone', is: 'Tools & MCP' },
        { thing: 'The budget', is: 'Tokens' },
        { thing: 'The rules', is: 'The harness' },
      ],
    },
    {
      kind: 'lab',
      kicker: 'Lab 0 · 45 min',
      title: 'The hour-one win',
      steps: [
        'Upload 2–3 of your own documents',
        'Ask five real questions',
        'Ask one thing it cannot know',
        'Flipchart what worked and what failed',
      ],
      badge: '0 → 1',
      note: [
        'Never start with theory. The failures on the flipchart are the curriculum.',
        'We come back to it at the close of day two — every failure gets a name and a fix.',
      ],
    },
    {
      kind: 'concept',
      kicker: 'Module 2',
      title: 'It’s a prediction machine',
      points: [
        'Autocomplete that has read most of the internet',
        'No database inside',
        'It always produces a next word',
        'When it doesn’t know, it doesn’t say so',
        'It writes the most plausible continuation',
        'Fluent, confident, wrong = hallucination',
      ],
      quote: 'A hallucination isn’t a fault. It’s the machine doing its job in a situation where its job is the wrong thing to do.',
    },
    {
      kind: 'tokens',
      kicker: 'Economics',
      title: 'Tokens: the unit you’re billed in',
      facts: [
        { value: '1 token', label: '≈ ¾ of a word' },
        { value: '1 page', label: '≈ 700 tokens' },
        { value: 'Input', label: 'cheap' },
        { value: 'Output', label: '≈ 5× input' },
        { value: 'Cached input', label: 'repeated prefix ≈ 90% off' },
        { value: '“Reasoning”', label: 'billed as output — buy it deliberately' },
      ],
      example: { label: '500-page handbook, 1,000 questions a day', pasted: 20000, fetched: 300 },
    },
  ],
}

// ── Course finder ──────────────────────────────────────────────────────────

export interface FinderOption {
  id: string
  label: string
  icon: string
}

export const finderQuestions: { id: 'track' | 'level'; question: string; options: FinderOption[] }[] = [
  {
    id: 'track',
    question: 'Who is the training for?',
    options: tracks.map((t) => ({ id: t.id, label: t.individual ? 'Myself: I want a career in AI engineering' : t.audience, icon: t.icon })),
  },
  {
    id: 'level',
    question: 'How deep should it go?',
    options: [
      { id: '1', icon: '💡', label: 'Awareness: understand AI and use it safely' },
      { id: '2', icon: '🛠️', label: 'Practitioner: apply AI in day-to-day work' },
      { id: '3', icon: '🏗️', label: 'Builder: build AI systems hands-on' },
      { id: '4', icon: '🚀', label: 'Advanced: agents and production reliability' },
    ],
  },
]

export interface FinderResult {
  best: CourseWithTrack
  reason: string
  alternatives: CourseWithTrack[]
}

export function recommend(answers: Record<string, string>): FinderResult {
  const track = tracks.find((t) => t.id === answers.track) ?? tracks[0]
  const want = (Number(answers.level) || 1) as Level
  const distance = (c: CourseWithTrack) => Math.abs(c.level - want)
  const inTrack = allCourses.filter((c) => c.track.id === track.id).sort((a, b) => distance(a) - distance(b))
  const best = inTrack[0]
  const reason =
    best.level === want
      ? `it is the ${levels[want].label.toLowerCase()}-level course in the ${track.label} track, built for ${track.audience.toLowerCase()}`
      : `the ${track.label} track has no ${levels[want].label.toLowerCase()}-level course, and this ${levels[best.level].short} course is the closest match`
  const sameLevelElsewhere = allCourses.filter((c) => c.track.id !== track.id && c.level === want && !c.track.individual)
  return { best, reason, alternatives: [...inTrack.slice(1), ...sameLevelElsewhere].slice(0, 2) }
}

export const courseHref = (id: string) => `/services/training#course-${id}`
