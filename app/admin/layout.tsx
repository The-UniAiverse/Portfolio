import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Admin Panel - uniAiverse',
  description: 'uniAiverse Admin Dashboard',
}

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#0A0F1E]">
      {children}
    </div>
  )
}
