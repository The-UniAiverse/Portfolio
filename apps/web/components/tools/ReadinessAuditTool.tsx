'use client'

import { useEffect, useRef, useState, type FormEvent } from 'react'
import {
  apiUrl, getAuditSample, getQuestionnaire, runAudit,
  type AuditResult, type CompanySize, type Mode, type Questionnaire, errorText
} from '@/lib/ai-services'
import { Card, ErrorBanner, inputClass, labelClass, Loading, ModeSelector, SourceBadge, SubmitButton } from './ToolUI'

const SIZES: { value: CompanySize; label: string }[] = [
  { value: 'small', label: 'Small (<50 staff)' },
  { value: 'medium', label: 'Medium (50–250)' },
  { value: 'large', label: 'Large (250–1000)' },
  { value: 'enterprise', label: 'Enterprise (1000+)' },
]

// Static class names so Tailwind keeps them; one column per roadmap horizon.
const ROADMAP_COLS: Record<number, string> = { 2: 'md:grid-cols-2', 3: 'md:grid-cols-3', 4: 'md:grid-cols-2 lg:grid-cols-4' }

export default function ReadinessAuditTool() {
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [org, setOrg] = useState({ name: '', industry: '', size: 'small' as CompanySize, top_goal: '' })
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [mode, setMode] = useState<Mode>('rules')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AuditResult | null>(null)
  const resultRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    getQuestionnaire().then(setQuestionnaire).catch((e) => setLoadError(errorText(e)))
  }, [])

  useEffect(() => {
    if (result) resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, [result])

  if (loadError) return <ErrorBanner error={loadError} />
  if (!questionnaire) return <Loading label="Loading questionnaire…" />

  const total = questionnaire.dimensions.reduce((n, d) => n + d.questions.length, 0)
  const answered = Object.keys(answers).length
  const scale = Object.entries(questionnaire.scale).sort(([a], [b]) => Number(a) - Number(b))

  async function fillSample() {
    setError(null)
    try {
      const s = await getAuditSample()
      setOrg({ name: s.organisation.name, industry: s.organisation.industry, size: s.organisation.size, top_goal: s.organisation.top_goal || '' })
      setAnswers(s.answers)
    } catch (e) {
      setError(errorText(e))
    }
  }

  async function submit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    if (answered === 0) {
      setError('Answer at least one question to run the audit.')
      return
    }
    setLoading(true)
    try {
      setResult(await runAudit({
        organisation: { name: org.name.trim(), industry: org.industry.trim() || 'General', size: org.size, top_goal: org.top_goal.trim() || null },
        answers,
        mode,
      }))
    } catch (e) {
      setError(errorText(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-12">
      <form onSubmit={submit} className="space-y-10">
        {/* Organisation */}
        <Card>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <h3 className="text-2xl font-bold text-primary-dark">Your organisation</h3>
            <button type="button" onClick={fillSample} className="text-primary hover:text-primary-light font-semibold text-sm underline-offset-4 hover:underline">
              Fill with sample answers
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="org-name" className={labelClass}>Organisation name *</label>
              <input id="org-name" required maxLength={120} className={inputClass} value={org.name}
                onChange={(e) => setOrg({ ...org, name: e.target.value })} placeholder="Acme Logistics" />
            </div>
            <div>
              <label htmlFor="org-industry" className={labelClass}>Industry</label>
              <input id="org-industry" maxLength={80} className={inputClass} value={org.industry}
                onChange={(e) => setOrg({ ...org, industry: e.target.value })} placeholder="Logistics" />
            </div>
            <div>
              <label htmlFor="org-size" className={labelClass}>Company size</label>
              <select id="org-size" className={inputClass} value={org.size}
                onChange={(e) => setOrg({ ...org, size: e.target.value as CompanySize })}>
                {SIZES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
              </select>
            </div>
            <div>
              <label htmlFor="org-goal" className={labelClass}>Top goal for AI</label>
              <input id="org-goal" maxLength={500} className={inputClass} value={org.top_goal}
                onChange={(e) => setOrg({ ...org, top_goal: e.target.value })} placeholder="Cut back-office processing cost by 30%" />
            </div>
          </div>
        </Card>

        {/* Scale legend */}
        <div className="bg-gradient-blue p-8 rounded-2xl shadow-lg text-secondary">
          <h3 className="text-xl font-bold mb-4">How to score each question</h3>
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
            {scale.map(([score, label]) => (
              <div key={score} className="bg-secondary/10 rounded-xl p-3">
                <div className="text-2xl font-bold">{score}</div>
                <div className="text-sm text-secondary/80">{label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Questions by dimension */}
        {questionnaire.dimensions.map((dim) => (
          <Card key={dim.id}>
            <div className="flex items-baseline justify-between mb-6">
              <h3 className="text-2xl font-bold text-primary-dark">{dim.title}</h3>
              <span className="text-sm text-primary-dark/50">Weight {Math.round(dim.weight * 100)}%</span>
            </div>
            <div className="space-y-6">
              {dim.questions.map((q) => (
                <fieldset key={q.id}>
                  <legend className="text-primary-dark/80 mb-3">{q.text}</legend>
                  <div className="flex flex-wrap gap-2">
                    {scale.map(([score, label]) => {
                      const v = Number(score)
                      const active = answers[q.id] === v
                      return (
                        <button key={score} type="button" title={label} aria-pressed={active}
                          onClick={() => setAnswers({ ...answers, [q.id]: v })}
                          className={`w-12 h-12 rounded-full font-bold transition-all duration-300 ${
                            active ? 'bg-primary text-secondary shadow-lg scale-110' : 'bg-secondary text-primary-dark border border-primary/20 hover:border-primary-light'
                          }`}>
                          {score}
                        </button>
                      )
                    })}
                  </div>
                </fieldset>
              ))}
            </div>
          </Card>
        ))}

        <Card>
          <ModeSelector mode={mode} onChange={setMode} />
          <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-4">
            <SubmitButton loading={loading}>Score my readiness →</SubmitButton>
            <span className="text-primary-dark/60">{answered} of {total} questions answered</span>
          </div>
          <div className="mt-6"><ErrorBanner error={error} /></div>
        </Card>
      </form>

      {result && (
        <div ref={resultRef} className="space-y-10 scroll-mt-24">
          {/* Headline score */}
          <div className="bg-gradient-blue p-10 rounded-3xl shadow-2xl text-secondary text-center">
            <p className="uppercase tracking-widest text-sm text-secondary/70 mb-2">{result.organisation.name}</p>
            <div className="text-7xl font-bold">{result.overall_score}<span className="text-3xl text-secondary/70">/100</span></div>
            <div className="text-3xl font-bold mt-2">{result.maturity_level}</div>
            <p className="text-lg text-secondary/80 mt-4 max-w-2xl mx-auto">{result.maturity_summary}</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
              {result.report_pdf_url && (
                <a href={apiUrl(result.report_pdf_url)} target="_blank" rel="noopener noreferrer"
                  className="bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold hover:bg-primary-lighter hover:text-secondary transition-all duration-300">
                  Download PDF report
                </a>
              )}
              {result.report_markdown_url && (
                <a href={apiUrl(result.report_markdown_url)} target="_blank" rel="noopener noreferrer"
                  className="border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold hover:bg-secondary hover:text-primary-dark transition-all duration-300">
                  Download Markdown
                </a>
              )}
            </div>
          </div>

          {/* Narrative */}
          <Card>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
              <h3 className="text-2xl font-bold text-primary-dark">Executive summary</h3>
              <SourceBadge source={result.narrative_source} notice={result.narrative_notice} />
            </div>
            <p className="text-primary-dark/80 leading-relaxed whitespace-pre-line">{result.narrative}</p>
          </Card>

          {/* Dimensions */}
          <Card>
            <h3 className="text-2xl font-bold text-primary-dark mb-6">Dimension scores</h3>
            <div className="space-y-6">
              {result.dimensions.map((d) => (
                <div key={d.id}>
                  <div className="flex justify-between mb-2">
                    <span className="font-semibold text-primary-dark">{d.title}</span>
                    <span className="font-bold text-primary">{d.score}</span>
                  </div>
                  <div className="h-3 bg-primary/10 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full" style={{ width: `${d.score}%` }} />
                  </div>
                  {(d.strengths.length > 0 || d.gaps.length > 0) && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3 text-sm">
                      <ul className="space-y-1">
                        {d.strengths.map((s) => <li key={s} className="text-green-700">+ {s}</li>)}
                      </ul>
                      <ul className="space-y-1">
                        {d.gaps.map((g) => <li key={g} className="text-red-700">– {g}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </Card>

          {/* Recommendations */}
          <Card>
            <h3 className="text-2xl font-bold text-primary-dark mb-6">Prioritised recommendations</h3>
            <div className="space-y-4">
              {result.recommendations.map((r) => (
                <div key={`${r.priority}-${r.action}`} className="bg-secondary rounded-xl p-5 border border-primary/10">
                  <div className="flex flex-wrap items-center gap-3 mb-2">
                    <span className="w-8 h-8 rounded-full bg-primary text-secondary flex items-center justify-center font-bold text-sm">{r.priority}</span>
                    <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-semibold">{r.horizon}</span>
                    <span className="text-xs text-primary-dark/50">{r.dimension} · Owner: {r.owner_hint}</span>
                  </div>
                  <p className="font-semibold text-primary-dark">{r.action}</p>
                  <p className="text-sm text-primary-dark/70 mt-1">{r.why}</p>
                </div>
              ))}
            </div>
          </Card>

          {/* Roadmap */}
          <div>
            <h3 className="text-2xl font-bold text-primary-dark mb-6 text-center">Your roadmap</h3>
            <div className={`grid grid-cols-1 gap-6 ${ROADMAP_COLS[Object.keys(result.roadmap).length] ?? 'md:grid-cols-2 lg:grid-cols-4'}`}>
              {Object.entries(result.roadmap).map(([horizon, items]) => (
                <Card key={horizon} className="!p-6">
                  <h4 className="text-lg font-bold text-primary mb-3">{horizon}</h4>
                  <ul className="space-y-2">
                    {items.map((i) => (
                      <li key={i} className="flex items-start text-sm text-primary-dark/80">
                        <span className="text-primary mr-2">✓</span>{i}
                      </li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
