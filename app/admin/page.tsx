'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function AdminRoot() {
  const router = useRouter()

  useEffect(() => {
    const auth = localStorage.getItem('admin_auth')
    if (auth) {
      router.replace('/admin/dashboard')
    } else {
      router.replace('/admin/login')
    }
  }, [router])

  return (
    <div className="min-h-screen bg-[#0A0F1E] flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
    </div>
  )
}
