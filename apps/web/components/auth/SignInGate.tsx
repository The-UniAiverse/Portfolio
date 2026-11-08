'use client'

import type { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useSession } from '@/lib/auth-client'
import { Card, Loading } from '../tools/ToolUI'

/** Shows `children` to signed-in users; everyone else gets a sign-in prompt. The API enforces this too. */
export default function SignInGate({ children, what = 'this tool' }: { children: ReactNode; what?: string }) {
  const { data, isPending } = useSession()
  const pathname = usePathname()

  if (isPending) return <Loading label="Checking your sign-in…" />
  if (data?.user) return <>{children}</>

  return (
    <Card className="text-center max-w-xl mx-auto">
      <div className="text-5xl mb-4">🔐</div>
      <h3 className="text-2xl font-bold text-primary-dark mb-2">Sign in to use {what}</h3>
      <p className="text-primary-dark/70 mb-6">It&apos;s free. Continue with your Google or GitHub account and you&apos;ll come straight back here.</p>
      <Link href={`/login?next=${encodeURIComponent(pathname)}`}
        className="inline-block bg-primary hover:bg-primary-light text-secondary px-8 py-3 rounded-full font-bold transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50">
        Sign in or create account →
      </Link>
    </Card>
  )
}
