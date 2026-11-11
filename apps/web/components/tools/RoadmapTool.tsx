'use client'

import { useState, type FormEvent } from 'react'
import { buildRoadmap, type Mode, type RoadmapResult, type UseCase, errorText } from '@/lib/ai-services'
import { Card, ErrorBanner, inputClass, labelClass, ModeSelector, SourceBadge, SubmitButton } from './ToolUI'

const MAX_USE_CASES = 25

const emptyUseCase = (): UseCase => ({ name: '', value: 3, feasibility: 3, risk: 2, effort_weeks: 4, function: 'General' })

const QUADRANT_STYLE: Record<string, string> = {
  'Quick win': 'bg-green-400/15 text-green-300',
  'Strategic bet': 'bg-purple-400/15 text-purple-300',
  'Fill-in': 'bg-primary/10 text-primary',
  Deprioritise: 'bg-white/10 text-white/60',
}

function Rating({ label, value, onChange, hint }: { label: string; value: number; onChange: (v: number) => void; hint: string }) {
  return (
    <div>
      <span className={labelClass} title={hint}>{label}</span>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((v) => (
          <button key={v} type="button" aria-label={`${label} ${v}`} aria-pressed={value === v} onClick={() => onChange(v)}
            className={`w-9 h-9 rounded-full text-sm font-bold transition-all duration-300 ${
              value === v ? 'bg-primary text-secondary' : 'bg-secondary text-primary-dark border border-primary/20 hover:border-primary-light'
            }`}>
            {v}
          </button>
        ))}
      </div>
    </div>
  )
}

export default function RoadmapTool() {
  const [organisation, setOrganisation] = useState('')
  const [readiness, setReadiness] = useState('')
  const [useCases, setUseCases] = useState<UseCase[]>([emptyUseCase()])
  const [mode, setMode] = useState<Mode>('rules')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<RoadmapResult | null>(null)

  const update = (i: number, patch: Partial<UseCase>) =>
    setUseCases(useCases.map((u, j) => (j === i ? { ...u, ...patch } : u)))

  async function submit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      setResult(await buildRoadmap({
        organisation: organisation.trim(),
        readiness_score: readiness === '' ? null : Number(readiness),
        use_cases: useCases.map((u) => ({ ...u, name: u.name.trim(), function: u.function.trim() || 'General' })),
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
      <form onSubmit={submit} className="space-y-8">
        <Card>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="rm-org" className={labelClass}>Organisation *</label>
              <input id="rm-org" required maxLength={120} className={inputClass} value={organisation}
                onChange={(e) => setOrganisation(e.target.value)} placeholder="Acme Logistics" />
            </div>
            <div>
              <label htmlFor="rm-score" className={labelClass}>Readiness score (optional, 0–100)</label>
              <input id="rm-score" type="number" min={0} max={100} step="0.1" className={inputClass} value={readiness}
                onChange={(e) => setReadiness(e.target.value)} placeholder="From the AI Readiness Audit" />
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-2xl font-bold text-primary-dark mb-2">Candidate use cases</h3>
          <p className="text-primary-dark/60 mb-6">Rate each from 1 (low) to 5 (high). Risk 5 means the highest regulatory or operational risk.</p>
          <div className="space-y-6">
            {useCases.map((u, i) => (
              <div key={i} className="bg-secondary rounded-xl p-5 border border-primary/10 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-[2fr_1fr_1fr_auto] gap-4 items-end">
                  <div>
                    <label htmlFor={`uc-name-${i}`} className={labelClass}>Use case *</label>
                    <input id={`uc-name-${i}`} required maxLength={120} className={inputClass} value={u.name}
                      onChange={(e) => update(i, { name: e.target.value })} placeholder="Invoice data extraction" />
                  </div>
                  <div>
                    <label htmlFor={`uc-fn-${i}`} className={labelClass}>Function</label>
                    <input id={`uc-fn-${i}`} maxLength={60} className={inputClass} value={u.function}
                      onChange={(e) => update(i, { function: e.target.value })} placeholder="Finance" />
                  </div>
                  <div>
                    <label htmlFor={`uc-effort-${i}`} className={labelClass}>Effort (weeks)</label>
                    <input id={`uc-effort-${i}`} type="number" min={1} max={104} required className={inputClass} value={u.effort_weeks}
                      onChange={(e) => update(i, { effort_weeks: Number(e.target.value) })} />
                  </div>
                  <button type="button" disabled={useCases.length === 1}
                    onClick={() => setUseCases(useCases.filter((_, j) => j !== i))}
                    className="text-red-300 hover:text-red-300 font-semibold px-2 py-3 disabled:opacity-30 disabled:cursor-not-allowed">
                    Remove
                  </button>
                </div>
                <div className="flex flex-wrap gap-8">
                  <Rating label="Value" hint="Business value" value={u.value} onChange={(v) => update(i, { value: v })} />
                  <Rating label="Feasibility" hint="Data and technology readiness" value={u.feasibility} onChange={(v) => update(i, { feasibility: v })} />
                  <Rating label="Risk" hint="Regulatory / operational risk" value={u.risk} onChange={(v) => update(i, { risk: v })} />
                </div>
              </div>
            ))}
          </div>
          <button type="button" disabled={useCases.length >= MAX_USE_CASES}
            onClick={() => setUseCases([...useCases, emptyUseCase()])}
            className="mt-6 border-2 border-primary text-primary px-6 py-2 rounded-full font-semibold hover:bg-primary hover:text-secondary transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed">
            + Add use case
          </button>
        </Card>

        <Card>
          <ModeSelector mode={mode} onChange={setMode} />
          <div className="mt-8"><SubmitButton loading={loading}>Build my roadmap →</SubmitButton></div>
          <div className="mt-6"><ErrorBanner error={error} /></div>
        </Card>
      </form>

      {result && (
        <div className="space-y-10">
          <Card>
            <h3 className="text-2xl font-bold text-primary-dark mb-6">Prioritised backlog</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-sm text-primary-dark/60 border-b border-primary/10">
                    <th className="py-3 pr-4">#</th><th className="py-3 pr-4">Use case</th><th className="py-3 pr-4">Function</th>
                    <th className="py-3 pr-4">Score</th><th className="py-3">Quadrant</th>
                  </tr>
                </thead>
                <tbody>
                  {result.backlog.map((b) => (
                    <tr key={b.rank} className="border-b border-primary/5">
                      <td className="py-3 pr-4 font-bold text-primary">{b.rank}</td>
                      <td className="py-3 pr-4 font-semibold text-primary-dark">{b.name}</td>
                      <td className="py-3 pr-4 text-primary-dark/70">{b.function}</td>
                      <td className="py-3 pr-4 text-primary-dark/70">{b.score}</td>
                      <td className="py-3">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${QUADRANT_STYLE[b.quadrant] ?? 'bg-white/10'}`}>{b.quadrant}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(result.phases).map(([phase, items]) => (
              <Card key={phase} className="!p-6">
                <h4 className="text-lg font-bold text-primary mb-3">{phase}</h4>
                {items.length === 0 ? (
                  <p className="text-sm text-primary-dark/50">Nothing scheduled in this phase.</p>
                ) : (
                  <ul className="space-y-2">
                    {items.map((i) => (
                      <li key={i} className="flex items-start text-sm text-primary-dark/80"><span className="text-primary mr-2">✓</span>{i}</li>
                    ))}
                  </ul>
                )}
              </Card>
            ))}
          </div>

          <Card>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
              <h3 className="text-2xl font-bold text-primary-dark">Rationale</h3>
              <SourceBadge source={result.rationale_source} notice={result.rationale_notice} />
            </div>
            <p className="text-primary-dark/80 leading-relaxed whitespace-pre-line">{result.rationale}</p>
          </Card>
        </div>
      )}
    </div>
  )
}
