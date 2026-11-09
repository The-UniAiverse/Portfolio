// Client for the uniAIverse AI Services API (apps/api, FastAPI).
// The browser calls it directly; the API URL is public and holds no secrets.
// Provider keys and all business logic stay in apps/api.
// AI tool calls carry a short-lived sign-in token (see lib/auth-client.ts); the API verifies it.

import { clearApiToken, getApiToken } from './auth-client'

export const AI_SERVICES_URL = (
  process.env.NEXT_PUBLIC_AI_SERVICES_API_URL || 'http://localhost:8000'
).replace(/\/+$/, '')

export type Mode = 'rules' | 'ai' | 'auto'

export class ApiError extends Error {
  constructor(message: string, public status: number, public code?: string) {
    super(message)
  }
}

/** Absolute URL for a path the API returns (report downloads, course files). */
export const apiUrl = (path: string) => `${AI_SERVICES_URL}${path.startsWith('/') ? path : `/${path}`}`

/** User-facing text for anything thrown by these functions. */
export const errorText = (e: unknown) => (e instanceof Error ? e.message : 'Something went wrong. Please try again.')

type ValidationIssue = { loc?: unknown[]; msg: string }

function errorMessage(status: number, body: unknown): { message: string; code?: string } {
  const d = (body as { detail?: unknown } | null)?.detail as
    | { message?: string; code?: string }
    | string
    | ValidationIssue[]
    | undefined
  if (d && typeof d === 'object' && !Array.isArray(d) && d.message) return { message: d.message, code: d.code }
  if (typeof d === 'string') return { message: d }
  if (Array.isArray(d) && d.length) {
    // FastAPI validation errors: [{loc: [...], msg: "..."}]
    const first: ValidationIssue = d[0]
    // loc like ["body", "use_cases", 0, "name"] → "use cases #1 name"
    const field = Array.isArray(first.loc)
      ? first.loc.filter((x: unknown) => x !== 'body')
          .map((x: unknown) => (typeof x === 'number' ? `#${x + 1}` : String(x).replace(/_/g, ' ')))
          .join(' ')
      : ''
    return { message: field ? `${field}: ${first.msg}` : first.msg, code: 'validation_error' }
  }
  if (status === 429) return { message: 'Too many requests. Please wait a moment and try again.', code: 'rate_limited' }
  return { message: `Request failed (${status}).` }
}

const SIGN_IN_REQUIRED = new ApiError('Please sign in to use this tool.', 401, 'auth_required')

async function request<T>(path: string, init?: RequestInit, auth = false): Promise<T> {
  const headers: Record<string, string> = {}
  if (init?.body) headers['Content-Type'] = 'application/json'
  if (auth) {
    const token = await getApiToken()
    if (!token) throw SIGN_IN_REQUIRED
    headers.Authorization = `Bearer ${token}`
  }
  let res: Response
  try {
    res = await fetch(apiUrl(path), { ...init, headers })
  } catch {
    throw new ApiError('Could not reach the AI services API. Please try again shortly.', 0, 'network_error')
  }
  const body = await res.json().catch(() => null)
  if (res.status === 401) {
    clearApiToken()
    throw SIGN_IN_REQUIRED
  }
  if (!res.ok) {
    const { message, code } = errorMessage(res.status, body)
    throw new ApiError(message, res.status, code)
  }
  return body as T
}

const get = <T>(path: string) => request<T>(path)
const post = <T>(path: string, data?: unknown, auth = false) =>
  request<T>(path, { method: 'POST', body: data === undefined ? undefined : JSON.stringify(data) }, auth)
/** POST to an AI tool endpoint: requires a signed-in user. */
const postAuthed = <T>(path: string, data: unknown) => post<T>(path, data, true)

// ─── Health ──────────────────────────────────────────────────────────────────

export interface Health {
  ok: boolean
  ai_enhanced_available: boolean
  services: { id: string; title: string; priority: number; status: string }[]
}
export const getHealth = () => get<Health>('/api/health')

// ─── Readiness audit ─────────────────────────────────────────────────────────

export type CompanySize = 'small' | 'medium' | 'large' | 'enterprise'

export interface Questionnaire {
  scale: Record<string, string>
  maturity_bands: { min: number; max: number; level: string; summary: string }[]
  dimensions: { id: string; title: string; weight: number; questions: { id: string; text: string }[] }[]
}

export interface Organisation {
  name: string
  industry: string
  size: CompanySize
  contact?: string | null
  top_goal?: string | null
}

export interface AuditRequest {
  organisation: Organisation
  answers: Record<string, number>
  mode: Mode
}

export interface AuditResult {
  audit_id: string
  organisation: Organisation
  overall_score: number
  maturity_level: string
  maturity_summary: string
  dimensions: { id: string; title: string; weight: number; score: number; answered: number; total: number; strengths: string[]; gaps: string[] }[]
  recommendations: { priority: number; dimension: string; action: string; why: string; horizon: string; owner_hint: string }[]
  roadmap: Record<string, string[]>
  narrative: string
  narrative_source: 'llm' | 'rules'
  narrative_notice: string | null
  report_markdown_url: string | null
  report_pdf_url: string | null
}

export const getQuestionnaire = () => get<Questionnaire>('/api/readiness_audit/questionnaire')
export const getAuditSample = () => get<{ organisation: Organisation; answers: Record<string, number> }>('/api/readiness_audit/sample')
export const runAudit = (req: AuditRequest) => postAuthed<AuditResult>('/api/readiness_audit/run', req)

// ─── Strategy roadmap ────────────────────────────────────────────────────────

export interface UseCase {
  name: string
  value: number
  feasibility: number
  risk: number
  effort_weeks: number
  function: string
}

export interface RoadmapRequest {
  organisation: string
  readiness_score: number | null
  use_cases: UseCase[]
  mode: Mode
}

export interface RoadmapResult {
  organisation: string
  backlog: { rank: number; name: string; function: string; score: number; quadrant: string }[]
  phases: Record<string, string[]>
  rationale: string
  rationale_source: 'llm' | 'rules'
  rationale_notice: string | null
}

export const buildRoadmap = (req: RoadmapRequest) => postAuthed<RoadmapResult>('/api/strategy/roadmap', req)

// ─── Governance ──────────────────────────────────────────────────────────────

export interface RiskInput {
  use_case: string
  affects_individuals_rights: boolean
  uses_biometrics_or_surveillance: boolean
  safety_critical: boolean
  interacts_with_public: boolean
  processes_personal_data: boolean
  fully_automated_decisions: boolean
  manipulative_or_social_scoring: boolean
}

export type RiskTier = 'prohibited' | 'high' | 'limited' | 'minimal'

export interface RiskResult {
  use_case: string
  risk_tier: RiskTier
  controls: string[]
  note: string
}

export const classifyRisk = (x: RiskInput) => postAuthed<RiskResult>('/api/governance/classify', x)
export const getPolicyTemplate = () => get<{ title: string; sections: string[] }>('/api/governance/policy-template')

// ─── Automation ROI ──────────────────────────────────────────────────────────

export interface Workflow {
  name: string
  volume_per_month: number
  minutes_per_item: number
  people_involved: number
  hourly_cost: number
  error_rate_pct: number
  cost_per_error: number
  automation_potential_pct: number
  rule_based: boolean
  needs_judgement: boolean
}

export interface ROIRequest {
  currency: string
  build_cost: number
  monthly_run_cost: number
  workflows: Workflow[]
}

export interface ROIResult {
  currency: string
  workflows: {
    workflow: string
    hours_per_month: number
    labour_cost: number
    error_cost: number
    monthly_saving: number
    recommended_approach: string
    priority_score: number
  }[]
  total_monthly_saving: number
  net_monthly_benefit: number
  payback_months: number | null
  year_one_roi_pct: number | null
}

export const calculateROI = (req: ROIRequest) => postAuthed<ROIResult>('/api/automation/roi', req)

// ─── Pricing ─────────────────────────────────────────────────────────────────

export interface Tier {
  price_usd: number
  duration: string
  includes: string[]
}

export interface PricingData {
  currency_note: string
  size_multiplier: Record<CompanySize, number>
  services: Record<string, { title: string; tiers: Record<string, Tier> }>
}

export interface Quote {
  service: string
  tier: string
  company_size: CompanySize
  base_price_usd: number
  quoted_price_usd: number
  includes: string[]
  duration: string
}

export const getPricing = () => get<PricingData>('/api/pricing/tiers')
export const getQuote = (service: string, tier: string, companySize: CompanySize) =>
  get<Quote>(
    `/api/pricing/quote?${new URLSearchParams({ service, tier, company_size: companySize })}`
  )

// ─── AI Job Finder (jobs via freehire.me, through apps/api) ──────────────────

export type JobLevel = 'any' | 'entry' | 'intern' | 'junior' | 'mid' | 'senior' | 'lead' | 'executive'
export type WorkMode = '' | 'remote' | 'hybrid' | 'onsite'

export interface JobCard {
  id: string
  title: string
  company: string | null
  location: string | null
  date: string | null
  work_mode: string | null
  skills: string[]
  apply_url: string | null
  freehire_url: string
}

export interface JobDetail extends JobCard {
  description: string
  cities: string[]
  seniority: string | null
  category: string | null
  employment_type: string | null
  salary: string | null
  guard: string
}

export interface JobSearchResult {
  total: number
  page: number
  results: JobCard[]
  attribution: { source: string; url: string; note: string }
}

export interface WorkEntry {
  title: string
  company: string
  period: string
  highlights: string
}

export interface CandidateProfile {
  name: string
  email: string
  phone: string
  link: string
  city: string
  open_to_relocation: boolean
  current_title: string
  years_experience: number | null
  work_history: WorkEntry[]
  education: { degree: string; institution: string; period: string }[]
  skills: string[]
  experience: string
  target_roles: string[]
  career_goals: string
  languages: { language: string; level: string }[]
}

export interface JobMatch {
  source: 'llm' | 'rules'
  scores: Partial<Record<'technical' | 'experience' | 'behavioral' | 'career', number | null>>
  overall: number | null
  band: string | null
  matched_skills: string[]
  missing_skills: string[]
  strengths: string[]
  gaps: string[]
  location_verdict: 'PASS' | 'FAIL' | 'FLAG' | null
  language_gate: 'PASS' | 'FAIL' | 'FLAG' | null
  language_note: string
  experience_verdict: 'PASS' | 'FLAG' | null
  experience_note: string
  recommended_courses: { id: string; title: string; hours: number; covers: string[] }[]
  notice: string | null
  guard: string
}

export interface Letter {
  salutation: string
  paragraphs_before_bullets: string[]
  bullets: string[]
  paragraphs_after_bullets: string[]
  sign_off: string
}

export interface CoverLetterResult {
  letter: Letter
  review_notes: string[]
  word_count: number
  pages: number
  pdf_url: string
  guard: string
}

export const searchJobs = (p: { q: string; city: string; level: JobLevel; work_mode: WorkMode; posted_within_days: number; page: number }) =>
  get<JobSearchResult>(`/api/jobs/search?${new URLSearchParams({ ...p, posted_within_days: String(p.posted_within_days), page: String(p.page) })}`)
export const getJob = (id: string) => get<JobDetail>(`/api/jobs/job/${encodeURIComponent(id)}`)
export const matchJob = (profile: CandidateProfile, job_id: string, mode: Mode) =>
  postAuthed<JobMatch>('/api/jobs/match', { profile, job_id, mode })
export const writeCoverLetter = (profile: CandidateProfile, job_id: string, notes: string) =>
  postAuthed<CoverLetterResult>('/api/jobs/cover-letter', { profile, job_id, notes })
export const renderCoverLetter = (profile: CandidateProfile, letter: Letter) =>
  postAuthed<{ pdf_url: string; pages: number; word_count: number }>('/api/jobs/cover-letter/pdf', { profile, letter })
