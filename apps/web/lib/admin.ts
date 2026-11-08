// Admin access: a signed-in user (Better Auth session cookie) whose verified email is in ADMIN_EMAILS.
// Checked on the server in every /api/admin/* route handler; the admin UI only mirrors it.
import { headers } from 'next/headers'
import { NextResponse } from 'next/server'
import { auth } from './auth'

function adminEmails(): string[] {
  return (process.env.ADMIN_EMAILS || '').split(',').map((e) => e.trim().toLowerCase()).filter(Boolean)
}

export async function getAdmin() {
  const session = await auth.api.getSession({ headers: await headers() })
  const user = session?.user
  if (!user?.email || !user.emailVerified) return null
  return adminEmails().includes(user.email.toLowerCase()) ? user : null
}

/** Returns a 401/403 response to send back, or null when the caller is an admin. */
export async function requireAdmin(): Promise<NextResponse | null> {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session?.user) return NextResponse.json({ error: 'Sign in required' }, { status: 401 })
  if (!(await getAdmin())) return NextResponse.json({ error: 'Not an admin' }, { status: 403 })
  return null
}
// trial commit 
