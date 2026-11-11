'use client'

import { useEffect, useState, type FormEvent } from 'react'
import { classifyRisk, getPolicyTemplate, type RiskInput, type RiskResult, type RiskTier, errorText } from '@/lib/ai-services'
import { Card, ErrorBanner, inputClass, labelClass, SubmitButton } from './ToolUI'

type Flag = Exclude<keyof RiskInput, 'use_case'>

const FLAGS: { key: Flag; label: string; hint: string }[] = [
  { key: 'affects_individuals_rights', label: "Affects people's rights or access", hint: 'Employment, credit, education, access to services' },
  { key: 'uses_biometrics_or_surveillance', label: 'Uses biometrics or surveillance', hint: 'Face, voice, fingerprint, tracking' },
  { key: 'safety_critical', label: 'Safety-critical', hint: 'Medical, transport, infrastructure' },
  { key: 'interacts_with_public', label: 'Interacts with the public', hint: 'Chatbots, generated content' },
  { key: 'processes_personal_data', label: 'Processes personal data', hint: 'Names, contact details, records about people' },
  { key: 'fully_automated_decisions', label: 'Makes fully automated decisions', hint: 'No human reviews the outcome' },
  { key: 'manipulative_or_social_scoring', label: 'Manipulation or social scoring', hint: 'Exploits vulnerabilities or scores social behaviour' },
]

const TIERS: Record<RiskTier, { label: string; style: string }> = {
  prohibited: { label: 'Prohibited', style: 'from-red-700 to-red-500' },
  high: { label: 'High risk', style: 'from-orange-600 to-amber-500' },
  limited: { label: 'Limited risk', style: 'from-primary to-primary-light' },
  minimal: { label: 'Minimal risk', style: 'from-green-700 to-green-500' },
}

const initial: RiskInput = {
  use_case: '',
  affects_individuals_rights: false,
  uses_biometrics_or_surveillance: false,
  safety_critical: false,
  interacts_with_public: false,
  processes_personal_data: false,
  fully_automated_decisions: false,
  manipulative_or_social_scoring: false,
}

export default function GovernanceTool() {
  const [input, setInput] = useState<RiskInput>(initial)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<RiskResult | null>(null)
  const [policy, setPolicy] = useState<{ title: string; sections: string[] } | null>(null)

  useEffect(() => {
    getPolicyTemplate().then(setPolicy).catch(() => setPolicy(null))
  }, [])

  async function submit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      setResult(await classifyRisk({ ...input, use_case: input.use_case.trim() }))
    } catch (e) {
      setError(errorText(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-12">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        <form onSubmit={submit}>
          <Card>
            <h3 className="text-2xl font-bold text-primary-dark mb-6">Describe the AI use case</h3>
            <label htmlFor="gov-use-case" className={labelClass}>Use case *</label>
            <input id="gov-use-case" required maxLength={200} className={inputClass} value={input.use_case}
              onChange={(e) => setInput({ ...input, use_case: e.target.value })} placeholder="CV screening for hiring" />
            <div className="mt-6 space-y-3">
              {FLAGS.map((f) => (
                <label key={f.key} className="flex items-start gap-3 bg-secondary rounded-xl p-4 border border-primary/10 cursor-pointer hover:border-primary-light transition-all duration-300">
                  <input type="checkbox" className="mt-1 w-5 h-5 accent-[#1E40AF]" checked={input[f.key]}
                    onChange={(e) => setInput({ ...input, [f.key]: e.target.checked })} />
                  <span>
                    <span className="block font-semibold text-primary-dark">{f.label}</span>
                    <span className="block text-sm text-primary-dark/60">{f.hint}</span>
                  </span>
                </label>
              ))}
            </div>
            <div className="mt-8"><SubmitButton loading={loading}>Classify risk →</SubmitButton></div>
            <div className="mt-6"><ErrorBanner error={error} /></div>
          </Card>
        </form>

        <div className="space-y-6">
          {result ? (
            <>
              <div className={`bg-gradient-to-br ${TIERS[result.risk_tier].style} p-8 rounded-2xl shadow-2xl text-secondary`}>
                <p className="uppercase tracking-widest text-sm text-secondary/80 mb-1">{result.use_case}</p>
                <div className="text-4xl font-bold">{TIERS[result.risk_tier].label}</div>
              </div>
              <Card>
                <h4 className="text-xl font-bold text-primary-dark mb-4">Required controls</h4>
                <ul className="space-y-3">
                  {result.controls.map((c) => (
                    <li key={c} className="flex items-start text-primary-dark/80"><span className="text-primary text-xl mr-3">✓</span>{c}</li>
                  ))}
                </ul>
                <p className="mt-6 text-sm text-primary-dark/50">{result.note}</p>
              </Card>
            </>
          ) : (
            <Card>
              <h4 className="text-xl font-bold text-primary-dark mb-2">Risk tiers</h4>
              <p className="text-primary-dark/60 mb-6">Tiers follow the EU AI Act structure. Tick everything that applies to see the tier and the controls it needs.</p>
              <div className="space-y-3">
                {(Object.keys(TIERS) as RiskTier[]).map((t) => (
                  <div key={t} className={`bg-gradient-to-r ${TIERS[t].style} text-secondary px-5 py-3 rounded-xl font-semibold`}>{TIERS[t].label}</div>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>

      {policy && (
        <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
          <h2 className="text-3xl font-bold text-secondary mb-2 text-center">{policy.title}</h2>
          <p className="text-secondary/70 text-center mb-8">The sections every organisation&apos;s responsible-AI policy should cover.</p>
          <ol className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {policy.sections.map((s, i) => (
              <li key={s} className="bg-white/10 rounded-xl p-5 text-secondary">
                <span className="text-primary-lighter font-bold mr-2">{i + 1}.</span>{s}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  )
}
