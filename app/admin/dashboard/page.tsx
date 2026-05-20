'use client'

import { useState, useEffect, useCallback } from 'react'
import AdminSidebar from '@/components/admin/AdminSidebar'
import AdminHeader from '@/components/admin/AdminHeader'
import StatsCard from '@/components/admin/StatsCard'
import AuthGuard from '@/components/admin/AuthGuard'
import Link from 'next/link'

interface DashboardStats {
  services: { total: number; active: number; inactive: number }
  blog: { total: number; published: number; draft: number }
  testimonials: { total: number; avgRating: number }
  contacts: { total: number; new: number; inProgress: number; resolved: number }
}

interface ActivityItem {
  action: string
  time: string
  type: 'contact' | 'blog' | 'testimonial' | 'service'
}

const activityIconMap: Record<string, string> = {
  contact: '📬',
  blog: '📝',
  testimonial: '⭐',
  service: '⚙️',
}

const quickLinks = [
  { href: '/admin/blog', label: 'Write New Blog Post', icon: '✍️', color: 'bg-purple-600/20 border-purple-600/30 hover:bg-purple-600/30' },
  { href: '/admin/services', label: 'Manage Services', icon: '⚙️', color: 'bg-blue-600/20 border-blue-600/30 hover:bg-blue-600/30' },
  { href: '/admin/testimonials', label: 'Add Testimonial', icon: '⭐', color: 'bg-yellow-600/20 border-yellow-600/30 hover:bg-yellow-600/30' },
  { href: '/admin/contacts', label: 'View Inquiries', icon: '📬', color: 'bg-emerald-600/20 border-emerald-600/30 hover:bg-emerald-600/30' },
]

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentActivity, setRecentActivity] = useState<ActivityItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchDashboardData = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      // Fetch all data in parallel
      const [servicesRes, blogRes, testimonialsRes, contactsRes] = await Promise.all([
        fetch('/api/admin/services'),
        fetch('/api/admin/blog'),
        fetch('/api/admin/testimonials'),
        fetch('/api/admin/contacts'),
      ])

      const [servicesData, blogData, testimonialsData, contactsData] = await Promise.all([
        servicesRes.json(),
        blogRes.json(),
        testimonialsRes.json(),
        contactsRes.json(),
      ])

      // Calculate statistics
      const services = servicesData.success ? servicesData.data : []
      const blogPosts = blogData.success ? blogData.data : []
      const testimonials = testimonialsData.success ? testimonialsData.data : []
      const contacts = contactsData.success ? contactsData.data : []

      const servicesStats = {
        total: services.length,
        active: services.filter((s: any) => s.is_active).length,
        inactive: services.filter((s: any) => !s.is_active).length,
      }

      const blogStats = {
        total: blogPosts.length,
        published: blogPosts.filter((p: any) => p.status === 'published').length,
        draft: blogPosts.filter((p: any) => p.status === 'draft').length,
      }

      const avgRating = testimonials.length > 0
        ? (testimonials.reduce((sum: number, t: any) => sum + (t.rating || 5), 0) / testimonials.length).toFixed(1)
        : '0'

      const testimonialsStats = {
        total: testimonials.length,
        avgRating: parseFloat(avgRating as string),
      }

      const contactsStats = {
        total: contacts.length,
        new: contacts.filter((c: any) => c.status === 'new').length,
        inProgress: contacts.filter((c: any) => c.status === 'in-progress').length,
        resolved: contacts.filter((c: any) => c.status === 'resolved').length,
      }

      setStats({
        services: servicesStats,
        blog: blogStats,
        testimonials: testimonialsStats,
        contacts: contactsStats,
      })

      // Build recent activity from actual data
      const activity: ActivityItem[] = []

      // Add recent contacts
      contacts.slice(0, 3).forEach((c: any) => {
        activity.push({
          action: `New inquiry from ${c.name}`,
          time: formatTimeAgo(c.created_at),
          type: 'contact',
        })
      })

      // Add recent blog posts
      blogPosts.slice(0, 2).forEach((p: any) => {
        activity.push({
          action: `Blog post "${p.title}" ${p.status === 'published' ? 'published' : 'created'}`,
          time: formatTimeAgo(p.created_at),
          type: 'blog',
        })
      })

      // Add recent testimonials
      testimonials.slice(0, 2).forEach((t: any) => {
        activity.push({
          action: `Testimonial from ${t.author} added`,
          time: formatTimeAgo(t.created_at),
          type: 'testimonial',
        })
      })

      setRecentActivity(activity.slice(0, 6))
    } catch (err) {
      console.error('Dashboard fetch error:', err)
      setError('Failed to load dashboard data. Please check your database connection.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchDashboardData()
  }, [fetchDashboardData])

  // Helper function to format time ago
  function formatTimeAgo(dateString: string): string {
    if (!dateString) return 'recently'
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'just now'
    if (diffMins < 60) return `${diffMins} min ago`
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-[#0A0F1E]">
        <AdminSidebar />

        <main className="flex-1 ml-64 p-8">
          <AdminHeader
            title="Dashboard"
            subtitle="Welcome back! Here's what's happening with your site."
          />

          {error && (
            <div className="bg-red-900/20 border border-red-800/40 rounded-xl px-4 py-3 text-red-400 text-sm mb-6 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {error}
              </span>
              <button onClick={fetchDashboardData} className="text-xs underline hover:text-red-300">Retry</button>
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="w-10 h-10 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <>
              {/* Stats Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5 mb-8">
                <StatsCard
                  title="Total Services"
                  value={stats?.services.total || 0}
                  color="blue"
                  change={`${stats?.services.active || 0} active, ${stats?.services.inactive || 0} inactive`}
                  changeType="neutral"
                  icon={
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2v-4M9 21H5a2 2 0 01-2-2v-4m0 0h18" />
                    </svg>
                  }
                />
                <StatsCard
                  title="Blog Posts"
                  value={stats?.blog.total || 0}
                  color="purple"
                  change={`${stats?.blog.published || 0} published, ${stats?.blog.draft || 0} draft`}
                  changeType="up"
                  icon={
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                    </svg>
                  }
                />
                <StatsCard
                  title="Testimonials"
                  value={stats?.testimonials.total || 0}
                  color="green"
                  change={`${stats?.testimonials.avgRating || 0}★ avg rating`}
                  changeType="up"
                  icon={
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  }
                />
                <StatsCard
                  title="Contact Inquiries"
                  value={stats?.contacts.total || 0}
                  color="orange"
                  change={`${stats?.contacts.new || 0} new, ${stats?.contacts.inProgress || 0} in progress`}
                  changeType="up"
                  icon={
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  }
                />
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* Recent Activity */}
                <div className="xl:col-span-2 bg-[#1E293B] border border-blue-900/30 rounded-2xl p-6">
                  <div className="flex items-center justify-between mb-5">
                    <h2 className="text-white font-semibold text-lg">Recent Activity</h2>
                    <span className="text-xs text-slate-500 bg-slate-800 px-2 py-1 rounded-lg">Live data from database</span>
                  </div>
                  {recentActivity.length > 0 ? (
                    <div className="space-y-4">
                      {recentActivity.map((item, i) => (
                        <div key={i} className="flex items-center space-x-4 py-3 border-b border-blue-900/20 last:border-0">
                          <div className="w-9 h-9 rounded-xl bg-blue-900/30 flex items-center justify-center text-lg flex-shrink-0">
                            {activityIconMap[item.type]}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-slate-300 truncate">{item.action}</p>
                            <p className="text-xs text-slate-500 mt-0.5">{item.time}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-slate-500">
                      <p className="text-sm">No recent activity found.</p>
                      <p className="text-xs mt-1">Start adding content to see activity here!</p>
                    </div>
                  )}
                </div>

                {/* Quick Actions */}
                <div className="bg-[#1E293B] border border-blue-900/30 rounded-2xl p-6">
                  <h2 className="text-white font-semibold text-lg mb-5">Quick Actions</h2>
                  <div className="space-y-3">
                    {quickLinks.map((link) => (
                      <Link
                        key={link.href}
                        href={link.href}
                        className={`flex items-center space-x-3 px-4 py-3.5 rounded-xl border transition-all duration-200 ${link.color}`}
                      >
                        <span className="text-xl">{link.icon}</span>
                        <span className="text-sm font-medium text-slate-200">{link.label}</span>
                        <svg className="w-4 h-4 text-slate-500 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                    ))}
                  </div>

                  {/* Site Status */}
                  <div className="mt-6 p-4 bg-emerald-900/20 border border-emerald-800/30 rounded-xl">
                    <div className="flex items-center space-x-2 mb-1">
                      <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                      <span className="text-emerald-400 text-sm font-semibold">Admin Panel Online</span>
                    </div>
                    <p className="text-slate-400 text-xs">Connected to MySQL database</p>
                    <Link href="/" target="_blank" className="text-xs text-blue-400 hover:text-blue-300 transition-colors mt-1 block">
                      Visit website →
                    </Link>
                  </div>

                  {/* Refresh Button */}
                  <button
                    onClick={fetchDashboardData}
                    className="w-full mt-4 flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium px-4 py-2.5 rounded-xl transition-all duration-200"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Refresh Data
                  </button>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </AuthGuard>
  )
}
