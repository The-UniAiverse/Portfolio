'use client'

import Link from 'next/link'
import Image from 'next/image'
import { usePathname, useRouter } from 'next/navigation'

const navItems = [
  { href: '/admin/dashboard', label: 'Dashboard', icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
    </svg>
  )},
  { href: '/admin/services', label: 'Services', icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2v-4M9 21H5a2 2 0 01-2-2v-4m0 0h18" />
    </svg>
  )},
  { href: '/admin/blog', label: 'Blog Posts', icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
    </svg>
  )},
  { href: '/admin/testimonials', label: 'Testimonials', icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  )},
  { href: '/admin/contacts', label: 'Contacts', icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
    </svg>
  )},
]

export default function AdminSidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem('admin_auth')
    router.push('/admin/login')
  }

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-[#0F172A] border-r border-blue-900/40 flex flex-col z-40">
      {/* Logo */}
      <div className="flex items-center space-x-3 px-6 py-5 border-b border-blue-900/40">
        <Image src="/logo.png" alt="uniAiverse" width={36} height={36} className="object-contain" />
        <div className="text-xl font-bold">
          <span className="text-white">uni</span>
          <span className="text-blue-400">Ai</span>
          <span className="text-white">verse</span>
        </div>
      </div>

      {/* Admin Badge */}
      <div className="px-6 py-3 border-b border-blue-900/40">
        <span className="text-xs font-semibold text-blue-400 uppercase tracking-widest">Admin Panel</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/')
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                isActive
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'text-slate-400 hover:bg-blue-900/30 hover:text-white'
              }`}
            >
              <span className={`${isActive ? 'text-white' : 'text-slate-500 group-hover:text-blue-400'} transition-colors`}>
                {item.icon}
              </span>
              <span className="font-medium text-sm">{item.label}</span>
              {isActive && (
                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-white/80" />
              )}
            </Link>
          )
        })}
      </nav>

      {/* Bottom: View Site + Logout */}
      <div className="px-4 py-4 border-t border-blue-900/40 space-y-2">
        <Link
          href="/"
          target="_blank"
          className="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-blue-900/20 hover:text-white transition-all duration-200 group"
        >
          <svg className="w-5 h-5 text-slate-500 group-hover:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          <span className="text-sm font-medium">View Website</span>
        </Link>
        <button
          onClick={handleLogout}
          className="w-full flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-red-900/20 hover:text-red-400 transition-all duration-200 group"
        >
          <svg className="w-5 h-5 text-slate-500 group-hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span className="text-sm font-medium">Logout</span>
        </button>
      </div>
    </aside>
  )
}
