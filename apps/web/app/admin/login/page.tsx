import type { Metadata } from 'next'
import ProviderButtons from '@/components/auth/ProviderButtons'
import { enabledProviders } from '@/lib/auth'
import BrandLogo from '@/components/BrandLogo'

export const metadata: Metadata = { title: 'Admin sign-in - uniAiverse' }

// Admins sign in with Google (or GitHub) like everyone else; access is granted on the server to the
// emails in ADMIN_EMAILS (see lib/admin.ts).
export default function AdminLogin() {
  return (
    <div className="min-h-screen bg-[#0A0F1E] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-900/20 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md relative z-10">
        <div className="bg-[#0F172A] border border-blue-900/40 rounded-3xl p-8 shadow-2xl shadow-blue-950/50">
          <div className="flex flex-col items-center mb-8">
            <div className="flex items-center space-x-3 mb-3">
              <BrandLogo size={52} />
            </div>
            <span className="text-xs font-semibold text-blue-500 uppercase tracking-widest bg-blue-900/30 px-3 py-1 rounded-full border border-blue-800/40">
              Admin Portal
            </span>
          </div>

          <h2 className="text-xl font-bold text-white text-center mb-1">Welcome back</h2>
          <p className="text-slate-400 text-sm text-center mb-8">Sign in with an approved admin account</p>

          <ProviderButtons providers={enabledProviders} next="/admin/dashboard" />
        </div>
      </div>
    </div>
  )
}
