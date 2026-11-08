'use client'

import { createAuthClient } from 'better-auth/react'
import { safeNext } from './safe-next'

export const authClient = createAuthClient()
export const { useSession, signOut } = authClient

export type Provider = 'google' | 'github'


export function signInWith(provider: Provider, next: string) {
  return authClient.signIn.social({ provider, callbackURL: safeNext(next) })
}

// Short-lived API token (15 min), cached in memory and refreshed a minute before it expires.
let cached: { token: string; exp: number } | null = null

export async function getApiToken(): Promise<string | null> {
  if (cached && cached.exp - 60 > Date.now() / 1000) return cached.token
  const res = await fetch('/api/auth/token', { credentials: 'include' })
  if (!res.ok) {
    cached = null
    return null
  }
  const { token } = (await res.json()) as { token: string }
  const exp = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))).exp as number
  cached = { token, exp }
  return token
}

export function clearApiToken() {
  cached = null
}
