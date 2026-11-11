'use client'

import { useState, type FormEvent } from 'react'
import { calculateROI, type ROIResult, type Workflow, errorText } from '@/lib/ai-services'
import { Card, ErrorBanner, inputClass, labelClass, SubmitButton } from './ToolUI'

const MAX_WORKFLOWS = 25
const CURRENCIES = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'SGD', 'AED']

const emptyWorkflow = (): Workflow => ({
  name: '',
  volume_per_month: 500,
  minutes_per_item: 10,
  people_involved: 2,
  hourly_cost: 25,
  error_rate_pct: 2,
  cost_per_error: 20,
  automation_potential_pct: 60,
  rule_based: false,
  needs_judgement: true,
})

const NUMBER_FIELDS: { key: keyof Workflow; label: string; min: number; max: number; step?: string }[] = [
  { key: 'volume_per_month', label: 'Items per month', min: 1, max: 10_000_000 },
  { key: 'minutes_per_item', label: 'Minutes per item', min: 0.1, max: 10_000, step: '0.1' },
  { key: 'people_involved', label: 'People involved', min: 1, max: 100_000 },
  { key: 'hourly_cost', label: 'Hourly cost', min: 0, max: 100_000, step: '0.01' },
  { key: 'error_rate_pct', label: 'Error rate %', min: 0, max: 100, step: '0.1' },
  { key: 'cost_per_error', label: 'Cost per error', min: 0, max: 10_000_000, step: '0.01' },
  { key: 'automation_potential_pct', label: 'Automatable %', min: 0, max: 100 },
]

function money(value: number, currency: string) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency, maximumFractionDigits: 0 }).format(value)
  } catch {
    return `${currency} ${Math.round(value).toLocaleString()}`
  }
}

export default function AutomationROITool() {
  const [currency, setCurrency] = useState('USD')
  const [buildCost, setBuildCost] = useState(15000)
  const [runCost, setRunCost] = useState(300)
  const [workflows, setWorkflows] = useState<Workflow[]>([emptyWorkflow()])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<ROIResult | null>(null)

  const update = (i: number, patch: Partial<Workflow>) =>
    setWorkflows(workflows.map((w, j) => (j === i ? { ...w, ...patch } : w)))

  async function submit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      setResult(await calculateROI({
        currency,
        build_cost: buildCost,
        monthly_run_cost: runCost,
        workflows: workflows.map((w) => ({ ...w, name: w.name.trim() })),
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
          <h3 className="text-2xl font-bold text-primary-dark mb-6">Investment</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label htmlFor="roi-currency" className={labelClass}>Currency</label>
              <select id="roi-currency" className={inputClass} value={currency} onChange={(e) => setCurrency(e.target.value)}>
                {CURRENCIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label htmlFor="roi-build" className={labelClass}>One-off build cost</label>
              <input id="roi-build" type="number" min={0} max={1_000_000_000} required className={inputClass} value={buildCost}
                onChange={(e) => setBuildCost(Number(e.target.value))} />
            </div>
            <div>
              <label htmlFor="roi-run" className={labelClass}>Monthly run cost (LLM/API + hosting)</label>
              <input id="roi-run" type="number" min={0} max={100_000_000} required className={inputClass} value={runCost}
                onChange={(e) => setRunCost(Number(e.target.value))} />
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-2xl font-bold text-primary-dark mb-2">Workflows to automate</h3>
          <p className="text-primary-dark/60 mb-6">Costs are in {currency}. Hourly cost is the fully loaded cost per person-hour.</p>
          <div className="space-y-6">
            {workflows.map((w, i) => (
              <div key={i} className="bg-secondary rounded-xl p-5 border border-primary/10 space-y-4">
                <div className="flex flex-col md:flex-row gap-4 md:items-end">
                  <div className="flex-1">
                    <label htmlFor={`wf-name-${i}`} className={labelClass}>Workflow *</label>
                    <input id={`wf-name-${i}`} required maxLength={120} className={inputClass} value={w.name}
                      onChange={(e) => update(i, { name: e.target.value })} placeholder="Supplier invoice processing" />
                  </div>
                  <button type="button" disabled={workflows.length === 1}
                    onClick={() => setWorkflows(workflows.filter((_, j) => j !== i))}
                    className="text-red-300 hover:text-red-300 font-semibold px-2 py-3 disabled:opacity-30 disabled:cursor-not-allowed">
                    Remove
                  </button>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
                  {NUMBER_FIELDS.map((f) => (
                    <div key={f.key}>
                      <label htmlFor={`wf-${f.key}-${i}`} className="block text-xs font-semibold text-primary-dark/70 mb-1">{f.label}</label>
                      <input id={`wf-${f.key}-${i}`} type="number" required min={f.min} max={f.max} step={f.step ?? '1'}
                        className={inputClass} value={w[f.key] as number}
                        onChange={(e) => update(i, { [f.key]: Number(e.target.value) })} />
                    </div>
                  ))}
                </div>
                <div className="flex flex-wrap gap-6">
                  <label className="flex items-center gap-2 text-primary-dark/80 cursor-pointer">
                    <input type="checkbox" className="w-5 h-5 accent-[#1E40AF]" checked={w.rule_based}
                      onChange={(e) => update(i, { rule_based: e.target.checked })} />
                    Steps are rule-based (scripts / RPA fit)
                  </label>
                  <label className="flex items-center gap-2 text-primary-dark/80 cursor-pointer">
                    <input type="checkbox" className="w-5 h-5 accent-[#1E40AF]" checked={w.needs_judgement}
                      onChange={(e) => update(i, { needs_judgement: e.target.checked })} />
                    Needs reading, writing or judgement (LLM fit)
                  </label>
                </div>
              </div>
            ))}
          </div>
          <button type="button" disabled={workflows.length >= MAX_WORKFLOWS}
            onClick={() => setWorkflows([...workflows, emptyWorkflow()])}
            className="mt-6 border-2 border-primary text-primary px-6 py-2 rounded-full font-semibold hover:bg-primary hover:text-secondary transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed">
            + Add workflow
          </button>
        </Card>

        <div className="flex flex-col gap-6">
          <div><SubmitButton loading={loading}>Calculate ROI →</SubmitButton></div>
          <ErrorBanner error={error} />
        </div>
      </form>

      {result && (
        <div className="space-y-10">
          <div className="bg-gradient-blue p-10 rounded-3xl shadow-2xl">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center text-secondary">
              {[
                { label: 'Monthly saving', value: money(result.total_monthly_saving, result.currency) },
                { label: 'Net monthly benefit', value: money(result.net_monthly_benefit, result.currency) },
                { label: 'Payback', value: result.payback_months === null ? 'Not reached' : `${result.payback_months} months` },
                { label: 'Year-one ROI', value: result.year_one_roi_pct === null ? '—' : `${result.year_one_roi_pct}%` },
              ].map((s) => (
                <div key={s.label}>
                  <div className="text-3xl md:text-4xl font-bold">{s.value}</div>
                  <div className="text-secondary/70 mt-1">{s.label}</div>
                </div>
              ))}
            </div>
          </div>

          <Card>
            <h3 className="text-2xl font-bold text-primary-dark mb-6">By workflow</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-sm text-primary-dark/60 border-b border-primary/10">
                    <th className="py-3 pr-4">Workflow</th><th className="py-3 pr-4">Hours / month</th><th className="py-3 pr-4">Labour cost</th>
                    <th className="py-3 pr-4">Error cost</th><th className="py-3 pr-4">Monthly saving</th><th className="py-3">Recommended approach</th>
                  </tr>
                </thead>
                <tbody>
                  {result.workflows.map((w, i) => (
                    <tr key={i} className="border-b border-primary/5">
                      <td className="py-3 pr-4 font-semibold text-primary-dark">{w.workflow}</td>
                      <td className="py-3 pr-4 text-primary-dark/70">{w.hours_per_month}</td>
                      <td className="py-3 pr-4 text-primary-dark/70">{money(w.labour_cost, result.currency)}</td>
                      <td className="py-3 pr-4 text-primary-dark/70">{money(w.error_cost, result.currency)}</td>
                      <td className="py-3 pr-4 font-bold text-primary">{money(w.monthly_saving, result.currency)}</td>
                      <td className="py-3"><span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-semibold">{w.recommended_approach}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}
