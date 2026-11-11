'use client'

import { useState } from 'react'
import { signInWith, type Provider } from '@/lib/auth-client'

const LABELS: Record<Provider, string> = { google: 'Continue with Google', github: 'Continue with GitHub' }

function Logo({ provider }: { provider: Provider }) {
  return provider === 'google' ? (
    <svg viewBox="0 0 48 48" className="w-5 h-5" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" />
      <path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" />
      <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z" />
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z" />
    </svg>
  ) : (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor" aria-hidden="true">
      <path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.8.1-.7.1-.7 1.2.1 1.9 1.3 1.9 1.3 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17.3 4.7 18.3 5 18.3 5c.7 1.7.3 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5z" />
    </svg>
  )
}

export default function ProviderButtons({ providers, next }: { providers: Provider[]; next: string }) {
  const [busy, setBusy] = useState<Provider | null>(null)
  const [error, setError] = useState<string | null>(null)

  if (providers.length === 0) {
    return <p className="text-primary-dark/60 text-center">Sign-in isn&apos;t configured on this server yet.</p>
  }

  async function go(p: Provider) {
    setError(null)
    setBusy(p)
    const res = await signInWith(p, next)
    if (res?.error) {
      setError('Sign-in could not start. Please try again.')
      setBusy(null)
    }
    // On success the browser is redirected to the provider.
  }

  return (
    <div className="space-y-3">
      {providers.map((p) => (
        <button key={p} type="button" onClick={() => go(p)} disabled={busy !== null}
          className={`w-full flex items-center justify-center gap-3 px-6 py-3 rounded-full font-semibold transition-all duration-300 disabled:opacity-60 ${
            p === 'github' ? 'bg-primary-dark text-secondary hover:bg-primary' : 'bg-secondary text-primary-dark border-2 border-primary/20 hover:border-primary-light'
          }`}>
          <Logo provider={p} />
          {busy === p ? 'Redirecting…' : LABELS[p]}
        </button>
      ))}
      {error && <p role="alert" className="text-sm text-red-300 text-center">{error}</p>}
    </div>
  )
}
