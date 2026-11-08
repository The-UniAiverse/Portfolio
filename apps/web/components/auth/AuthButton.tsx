'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { clearApiToken, signOut, useSession } from '@/lib/auth-client'

/** Header control: "Sign in" when signed out; avatar + menu when signed in. */
export default function AuthButton({ mobile = false, onNavigate }: { mobile?: boolean; onNavigate?: () => void }) {
  const { data, isPending } = useSession()
  const [open, setOpen] = useState(false)
  const pathname = usePathname()
  const router = useRouter()

  if (isPending) return null

  if (!data?.user) {
    return (
      <Link href={`/login?next=${encodeURIComponent(pathname)}`} onClick={onNavigate}
        className="text-secondary hover:text-primary-light transition-colors duration-300 font-medium">
        Sign in
      </Link>
    )
  }

  const { name, email, image } = data.user
  const initial = (name || email || '?').charAt(0).toUpperCase()

  async function logout() {
    clearApiToken()
    await signOut()
    setOpen(false)
    onNavigate?.()
    router.refresh()
  }

  const avatar = image ? (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={image} alt="" className="w-8 h-8 rounded-full object-cover" referrerPolicy="no-referrer" />
  ) : (
    <span className="w-8 h-8 rounded-full bg-primary-light text-secondary flex items-center justify-center font-bold text-sm">{initial}</span>
  )

  if (mobile) {
    return (
      <div className="flex items-center justify-between">
        <span className="flex items-center gap-2 text-secondary text-sm">{avatar}{name || email}</span>
        <button type="button" onClick={logout} className="text-primary-light font-medium text-sm">Sign out</button>
      </div>
    )
  }

  return (
    <div className="relative">
      <button type="button" onClick={() => setOpen(!open)} aria-label="Account menu" aria-expanded={open} className="flex items-center">
        {avatar}
      </button>
      {open && (
        <div className="absolute right-0 mt-3 w-64 bg-primary-dark/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-primary-light/30 p-4 space-y-3">
          <div>
            <div className="text-secondary font-semibold truncate">{name}</div>
            <div className="text-secondary/60 text-sm truncate">{email}</div>
          </div>
          <Link href="/tools" onClick={() => setOpen(false)} className="block text-secondary hover:text-primary-light text-sm">My AI tools</Link>
          <button type="button" onClick={logout} className="w-full bg-primary hover:bg-primary-light text-secondary py-2 rounded-xl font-semibold text-sm transition-all duration-300">
            Sign out
          </button>
        </div>
      )}
    </div>
  )
}
