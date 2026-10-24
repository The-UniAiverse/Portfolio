'use client'

import { useEffect, useState } from 'react'

interface AdminHeaderProps {
  title: string
  subtitle?: string
}

export default function AdminHeader({ title, subtitle }: AdminHeaderProps) {
  const [adminUser, setAdminUser] = useState('Admin')
  const [time, setTime] = useState('')

  useEffect(() => {
    const auth = localStorage.getItem('admin_auth')
    if (auth) {
      try {
        const parsed = JSON.parse(auth)
        setAdminUser(parsed.name || 'Admin')
      } catch {}
    }

    const updateTime = () => {
      setTime(new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }))
    }
    updateTime()
    const interval = setInterval(updateTime, 60000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-center justify-between mb-8">
      <div>
        <h1 className="text-2xl font-bold text-white">{title}</h1>
        {subtitle && <p className="text-slate-400 mt-1 text-sm">{subtitle}</p>}
      </div>
      <div className="flex items-center space-x-4">
        <span className="text-slate-500 text-sm hidden md:block">{time}</span>
        <div className="flex items-center space-x-2 bg-blue-900/30 border border-blue-800/40 rounded-xl px-4 py-2">
          <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold">
            {adminUser.charAt(0).toUpperCase()}
          </div>
          <span className="text-sm text-white font-medium">{adminUser}</span>
        </div>
      </div>
    </div>
  )
}
