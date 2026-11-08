'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { getPricing, getQuote, type CompanySize, type PricingData, type Quote, errorText } from '@/lib/ai-services'
import { ErrorBanner, Loading } from './ToolUI'

const SIZES: { value: CompanySize; label: string }[] = [
  { value: 'small', label: 'Small · <50' },
  { value: 'medium', label: 'Medium · 50–250' },
  { value: 'large', label: 'Large · 250–1000' },
  { value: 'enterprise', label: 'Enterprise · 1000+' },
]

const TIER_STYLE: Record<string, string> = {
  bronze: 'from-amber-700 to-amber-500',
  silver: 'from-slate-500 to-slate-400',
  gold: 'from-yellow-600 to-yellow-400',
  platinum: 'from-primary-dark to-primary',
}

const usd = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)

export default function PricingTool() {
  const [data, setData] = useState<PricingData | null>(null)
  const [service, setService] = useState<string>('')
  const [size, setSize] = useState<CompanySize>('small')
  const [quotes, setQuotes] = useState<{ key: string; list: Quote[] } | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getPricing()
      .then((d) => {
        setData(d)
        setService(Object.keys(d.services)[0] ?? '')
      })
      .catch((e) => setError(errorText(e)))
  }, [])

  // Quotes come from the API so size multipliers stay defined in one place (pricing/tiers.yaml).
  useEffect(() => {
    if (!data || !service) return
    let cancelled = false
    Promise.all(Object.keys(data.services[service].tiers).map((t) => getQuote(service, t, size)))
      .then((list) => !cancelled && setQuotes({ key: `${service}|${size}`, list }))
      .catch((e) => !cancelled && setError(errorText(e)))
    return () => { cancelled = true }
  }, [data, service, size])

  if (error && !data) return <ErrorBanner error={error} />
  if (!data) return <Loading label="Loading pricing…" />
  const current = quotes?.key === `${service}|${size}` ? quotes.list : null

  return (
    <div className="space-y-10">
      {/* Service tabs */}
      <div className="flex flex-wrap gap-3 justify-center">
        {Object.entries(data.services).map(([id, s]) => (
          <button key={id} type="button" onClick={() => setService(id)}
            className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
              service === id ? 'bg-primary text-secondary shadow-lg' : 'bg-secondary-light text-primary-dark hover:bg-primary/10'
            }`}>
            {s.title}
          </button>
        ))}
      </div>

      {/* Company size */}
      <div className="flex flex-wrap gap-2 justify-center">
        <span className="text-primary-dark/60 self-center mr-2">Company size:</span>
        {SIZES.map((s) => (
          <button key={s.value} type="button" onClick={() => setSize(s.value)}
            className={`px-4 py-2 rounded-full text-sm font-semibold border-2 transition-all duration-300 ${
              size === s.value ? 'border-primary text-primary bg-primary/5' : 'border-primary/15 text-primary-dark/70 hover:border-primary-light'
            }`}>
            {s.label}
          </button>
        ))}
      </div>

      <ErrorBanner error={error} />

      {!current ? (
        <Loading label="Calculating quotes…" />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          {current.map((q) => (
            <div key={q.tier} className="bg-secondary-light rounded-2xl shadow-lg overflow-hidden flex flex-col hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
              <div className={`bg-gradient-to-br ${TIER_STYLE[q.tier] ?? 'from-primary to-primary-light'} p-6 text-secondary`}>
                <div className="uppercase tracking-widest text-sm font-semibold">{q.tier}</div>
                <div className="text-4xl font-bold mt-2">{usd(q.quoted_price_usd)}</div>
                {q.quoted_price_usd !== q.base_price_usd && (
                  <div className="text-sm text-secondary/80 mt-1">List {usd(q.base_price_usd)} · adjusted for size</div>
                )}
                <div className="text-sm text-secondary/90 mt-2">{q.duration}</div>
              </div>
              <ul className="p-6 space-y-3 flex-1">
                {q.includes.map((i) => (
                  <li key={i} className="flex items-start text-sm text-primary-dark/80"><span className="text-primary mr-2">✓</span>{i}</li>
                ))}
              </ul>
              <div className="p-6 pt-0">
                <Link href="#contact" className="block text-center bg-primary hover:bg-primary-light text-secondary px-6 py-3 rounded-full font-semibold transition-all duration-300">
                  Talk to us
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      <p className="text-center text-sm text-primary-dark/50 max-w-3xl mx-auto">{data.currency_note}</p>
    </div>
  )
}
