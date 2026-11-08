'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { signOut } from '@/lib/auth-client'

type Status = 'checking' | 'admin' | 'forbidden'

/** Mirrors the server-side admin check (lib/admin.ts) so the UI can redirect; the API enforces it. */
export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [status, setStatus] = useState<Status>('checking')

  useEffect(() => {
    fetch('/api/admin/me', { credentials: 'include' })
      .then((res) => {
        if (res.ok) setStatus('admin')
        else if (res.status === 403) setStatus('forbidden')
        else router.replace('/admin/login')
      })
      .catch(() => router.replace('/admin/login'))
  }, [router])

  if (status === 'forbidden') {
    return (
      <div className="min-h-screen bg-[#0A0F1E] flex items-center justify-center p-4">
        <div className="bg-[#0F172A] border border-blue-900/40 rounded-3xl p-8 max-w-md text-center">
          <h2 className="text-xl font-bold text-white mb-2">No admin access</h2>
          <p className="text-slate-400 text-sm mb-6">This account isn&apos;t approved for the admin panel.</p>
          <button type="button" onClick={async () => { await signOut(); router.replace('/admin/login') }}
            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2.5 rounded-xl font-semibold text-sm">
            Sign out and use another account
          </button>
        </div>
      </div>
    )
  }

  if (status === 'checking') {
    return (
      <div className="min-h-screen bg-[#0A0F1E] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return <>{children}</>
}
