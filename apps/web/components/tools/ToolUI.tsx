'use client'

import { useEffect, useState, type ReactNode } from 'react'
import { getHealth, type Mode } from '@/lib/ai-services'

// Shared building blocks for the AI tool pages, styled to match the service pages.

export const inputClass =
  'w-full px-4 py-3 rounded-xl border border-primary/20 bg-secondary text-primary-dark placeholder-primary-dark/40 focus:outline-none focus:ring-2 focus:ring-primary-light focus:border-transparent transition-all duration-300'

export const labelClass = 'block text-sm font-semibold text-primary-dark mb-2'

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`bg-secondary-light p-8 rounded-2xl shadow-lg ${className}`}>{children}</div>
}

export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-primary-dark mb-4">{title}</h2>
      {subtitle && <p className="text-xl text-primary-dark/70 max-w-3xl mx-auto">{subtitle}</p>}
    </div>
  )
}

export function ErrorBanner({ error }: { error: string | null }) {
  if (!error) return null
  return (
    <div role="alert" className="bg-red-400/15 border border-red-400/30 text-red-300 px-6 py-4 rounded-xl">
      {error}
    </div>
  )
}

export function SubmitButton({ loading, children, disabled }: { loading: boolean; children: ReactNode; disabled?: boolean }) {
  return (
    <button
      type="submit"
      disabled={loading || disabled}
      className="bg-primary hover:bg-primary-light text-secondary px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50 disabled:opacity-60 disabled:cursor-not-allowed"
    >
      {loading ? 'Working…' : children}
    </button>
  )
}

export function Loading({ label = 'Loading…' }: { label?: string }) {
  return (
    <div className="flex items-center justify-center py-16 text-primary-dark/60">
      <div className="w-6 h-6 border-2 border-primary/30 border-t-primary rounded-full animate-spin mr-3" />
      {label}
    </div>
  )
}

/** Standard vs AI-enhanced output. AI is offered only when the API reports a configured provider. */
export function ModeSelector({ mode, onChange }: { mode: Mode; onChange: (m: Mode) => void }) {
  const [aiAvailable, setAiAvailable] = useState<boolean | null>(null)

  useEffect(() => {
    getHealth()
      .then((h) => setAiAvailable(h.ai_enhanced_available))
      .catch(() => setAiAvailable(false))
  }, [])

  const options: { value: Mode; title: string; desc: string; disabled: boolean }[] = [
    { value: 'rules', title: 'Standard', desc: 'Instant, deterministic write-up.', disabled: false },
    {
      value: 'ai',
      title: 'AI-enhanced',
      desc: aiAvailable === false ? 'Not available right now.' : 'Narrative written by our AI model.',
      disabled: aiAvailable !== true,
    },
  ]

  return (
    <div>
      <span className={labelClass}>Write-up style</span>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {options.map((o) => (
          <button
            key={o.value}
            type="button"
            disabled={o.disabled}
            onClick={() => onChange(o.value)}
            className={`text-left px-5 py-4 rounded-xl border-2 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed ${
              mode === o.value ? 'border-primary bg-primary/5' : 'border-primary/15 bg-secondary hover:border-primary-light'
            }`}
          >
            <div className="font-semibold text-primary-dark">{o.title}</div>
            <div className="text-sm text-primary-dark/60">{o.desc}</div>
          </button>
        ))}
      </div>
    </div>
  )
}

/** Shows which engine produced a narrative, so rules output is never presented as AI-written. */
export function SourceBadge({ source, notice }: { source: 'llm' | 'rules'; notice?: string | null }) {
  return (
    <div className="space-y-2">
      <span
        className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
          source === 'llm' ? 'bg-purple-400/15 text-purple-300' : 'bg-primary/10 text-primary'
        }`}
      >
        {source === 'llm' ? '✨ AI-written' : 'Standard write-up'}
      </span>
      {notice && <p className="text-sm text-amber-300 bg-amber-400/15 border border-amber-400/30 rounded-lg px-4 py-2">{notice}</p>}
    </div>
  )
}
