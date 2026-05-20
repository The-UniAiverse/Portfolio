'use client'

import { useState, useEffect, useCallback } from 'react'
import AdminSidebar from '@/components/admin/AdminSidebar'
import AdminHeader from '@/components/admin/AdminHeader'
import AuthGuard from '@/components/admin/AuthGuard'
import { serviceCategories } from '@/data/services.data'

interface ServiceRecord {
  id: number
  title: string
  description: string
  icon: string
  category: string
  category_icon: string
  whats_included: string[] | string
  use_cases: string[] | string
  deliverables: string
  capabilities: string[] | string
  examples: string[] | string
  ideal_for: string
  powered_by: string
  tools: string
  duration: string
  is_active: number | boolean
  sort_order: number
  created_at?: string
  updated_at?: string
}

type EditForm = {
  title: string
  description: string
  icon: string
  category: string
  category_icon: string
  whats_included: string
  use_cases: string
  deliverables: string
  capabilities: string
  examples: string
  ideal_for: string
  powered_by: string
  tools: string
  duration: string
  is_active: boolean
  sort_order: number
}

const CATEGORY_OPTIONS = serviceCategories.map((c) => ({
  label: c.categoryTitle,
  icon: c.categoryIcon,
}))

const EMPTY_FORM: EditForm = {
  title: '',
  description: '',
  icon: '🔧',
  category: CATEGORY_OPTIONS[0]?.label || '',
  category_icon: CATEGORY_OPTIONS[0]?.icon || '🚀',
  whats_included: '',
  use_cases: '',
  deliverables: '',
  capabilities: '',
  examples: '',
  ideal_for: '',
  powered_by: '',
  tools: '',
  duration: '',
  is_active: true,
  sort_order: 0,
}

function parseJsonField(val: string[] | string | null | undefined): string[] {
  if (!val) return []
  if (Array.isArray(val)) return val
  try { return JSON.parse(val) } catch { return [] }
}

function toTextarea(val: string[] | string | null | undefined): string {
  const arr = parseJsonField(val)
  return arr.join('\n')
}

function fromTextarea(val: string): string[] {
  return val.split('\n').map((s) => s.trim()).filter(Boolean)
}

export default function ServicesAdmin() {
  const [services, setServices] = useState<ServiceRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [statusFilter, setStatusFilter] = useState('all')

  const [viewModal, setViewModal] = useState<ServiceRecord | null>(null)
  const [editModal, setEditModal] = useState<ServiceRecord | null>(null)
  const [addModal, setAddModal] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState<ServiceRecord | null>(null)

  const [editForm, setEditForm] = useState<EditForm>(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState('')
  const [togglingId, setTogglingId] = useState<number | null>(null)
  const [seeding, setSeeding] = useState(false)
  const [seedMsg, setSeedMsg] = useState('')

  const categories = ['All', ...CATEGORY_OPTIONS.map((c) => c.label)]

  const fetchServices = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams()
      if (selectedCategory !== 'All') params.set('category', selectedCategory)
      if (search) params.set('search', search)
      if (statusFilter !== 'all') params.set('status', statusFilter)

      const res = await fetch(`/api/admin/services?${params.toString()}`)
      const json = await res.json()
      if (json.success) {
        setServices(json.data)
      } else {
        setError(json.error || 'Failed to fetch services')
      }
    } catch {
      setError('Network error — could not connect to server')
    } finally {
      setLoading(false)
    }
  }, [selectedCategory, search, statusFilter])

  useEffect(() => {
    fetchServices()
  }, [fetchServices])

  const openEdit = (svc: ServiceRecord) => {
    setEditForm({
      title: svc.title,
      description: svc.description,
      icon: svc.icon,
      category: svc.category,
      category_icon: svc.category_icon,
      whats_included: toTextarea(svc.whats_included),
      use_cases: toTextarea(svc.use_cases),
      deliverables: svc.deliverables || '',
      capabilities: toTextarea(svc.capabilities),
      examples: toTextarea(svc.examples),
      ideal_for: svc.ideal_for || '',
      powered_by: svc.powered_by || '',
      tools: svc.tools || '',
      duration: svc.duration || '',
      is_active: Boolean(svc.is_active),
      sort_order: svc.sort_order || 0,
    })
    setSaveError('')
    setEditModal(svc)
  }

  const openAdd = () => {
    setEditForm(EMPTY_FORM)
    setSaveError('')
    setAddModal(true)
  }

  const handleSave = async () => {
    if (!editForm.title.trim() || !editForm.description.trim() || !editForm.category.trim()) {
      setSaveError('Title, description, and category are required.')
      return
    }
    setSaving(true)
    setSaveError('')

    const payload = {
      ...editForm,
      whats_included: fromTextarea(editForm.whats_included),
      use_cases: fromTextarea(editForm.use_cases),
      capabilities: fromTextarea(editForm.capabilities),
      examples: fromTextarea(editForm.examples),
    }

    try {
      let res: Response
      if (addModal) {
        res = await fetch('/api/admin/services', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
      } else {
        res = await fetch(`/api/admin/services/${editModal!.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
      }

      const json = await res.json()
      if (json.success) {
        setEditModal(null)
        setAddModal(false)
        fetchServices()
      } else {
        setSaveError(json.error || 'Failed to save')
      }
    } catch {
      setSaveError('Network error — could not save')
    } finally {
      setSaving(false)
    }
  }

  const handleToggle = async (svc: ServiceRecord) => {
    setTogglingId(svc.id)
    try {
      const res = await fetch(`/api/admin/services/${svc.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !svc.is_active }),
      })
      const json = await res.json()
      if (json.success) {
        setServices((prev) =>
          prev.map((s) => s.id === svc.id ? { ...s, is_active: svc.is_active ? 0 : 1 } : s)
        )
      }
    } catch {
      // silently fail
    } finally {
      setTogglingId(null)
    }
  }

  const handleSeedFromStatic = async () => {
    setSeeding(true)
    setSeedMsg('')
    try {
      const res = await fetch('/api/admin/services/seed', { method: 'POST' })
      const json = await res.json()
      if (json.success) {
        setSeedMsg(json.message)
        fetchServices()
      } else {
        setSeedMsg(json.error || 'Seed failed')
      }
    } catch {
      setSeedMsg('Network error during seed')
    } finally {
      setSeeding(false)
    }
  }

  const handleDelete = async () => {
    if (!deleteConfirm) return
    try {
      const res = await fetch(`/api/admin/services/${deleteConfirm.id}`, { method: 'DELETE' })
      const json = await res.json()
      if (json.success) {
        setDeleteConfirm(null)
        fetchServices()
      }
    } catch {
      // silently fail
    }
  }

  const handleCategoryIconSync = (cat: string) => {
    const found = CATEGORY_OPTIONS.find((c) => c.label === cat)
    if (found) {
      setEditForm((f) => ({ ...f, category: cat, category_icon: found.icon }))
    } else {
      setEditForm((f) => ({ ...f, category: cat }))
    }
  }

  const activeCount = services.filter((s) => s.is_active).length
  const inactiveCount = services.filter((s) => !s.is_active).length

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-[#0A0F1E]">
        <AdminSidebar />

        <main className="flex-1 ml-64 p-8">
          <AdminHeader title="Services" subtitle="Manage all AI services listed on the website" />

          {/* Stats row */}
          <div className="flex gap-3 mb-6">
            <div className="bg-[#1E293B] border border-blue-900/30 rounded-xl px-4 py-2 text-xs text-slate-400">
              Total: <span className="text-white font-semibold">{services.length}</span>
            </div>
            <div className="bg-[#1E293B] border border-emerald-900/30 rounded-xl px-4 py-2 text-xs text-slate-400">
              Active: <span className="text-emerald-400 font-semibold">{activeCount}</span>
            </div>
            <div className="bg-[#1E293B] border border-red-900/30 rounded-xl px-4 py-2 text-xs text-slate-400">
              Inactive: <span className="text-red-400 font-semibold">{inactiveCount}</span>
            </div>
            <div className="ml-auto flex items-center gap-2">
              <button
                onClick={handleSeedFromStatic}
                disabled={seeding}
                title="Import all services from static data file into database"
                className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-slate-300 hover:text-white text-xs font-medium px-4 py-2 rounded-xl transition-all duration-200 border border-slate-600/50"
              >
                {seeding ? (
                  <span className="w-3.5 h-3.5 border border-current border-t-transparent rounded-full animate-spin" />
                ) : (
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                )}
                Import Static Data
              </button>
              <button
                onClick={openAdd}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium px-4 py-2 rounded-xl transition-all duration-200 shadow-lg shadow-blue-600/20"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Service
              </button>
            </div>
          </div>

          {/* Seed message */}
          {seedMsg && (
            <div className="bg-emerald-900/20 border border-emerald-800/40 rounded-xl px-4 py-2.5 text-emerald-400 text-sm mb-4 flex items-center justify-between">
              <span>✓ {seedMsg}</span>
              <button onClick={() => setSeedMsg('')} className="text-emerald-600 hover:text-emerald-400 text-xs ml-4">Dismiss</button>
            </div>
          )}

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="relative flex-1">
              <svg className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search services..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all"
              />
            </div>
            <div className="flex gap-2 flex-wrap">
              {/* Status filter */}
              {['all', 'active', 'inactive'].map((s) => (
                <button
                  key={s}
                  onClick={() => setStatusFilter(s)}
                  className={`px-3 py-2 rounded-xl text-xs font-medium transition-all duration-200 capitalize ${
                    statusFilter === s
                      ? s === 'active' ? 'bg-emerald-600 text-white' : s === 'inactive' ? 'bg-red-600 text-white' : 'bg-blue-600 text-white'
                      : 'bg-[#1E293B] text-slate-400 border border-blue-900/30 hover:border-blue-700/50 hover:text-white'
                  }`}
                >
                  {s === 'all' ? 'All Status' : s}
                </button>
              ))}
            </div>
          </div>

          {/* Category filter */}
          <div className="flex gap-2 flex-wrap mb-4">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-2 rounded-xl text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                    : 'bg-[#1E293B] text-slate-400 border border-blue-900/30 hover:border-blue-700/50 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Count */}
          <p className="text-slate-500 text-sm mb-4">
            {loading ? 'Loading...' : `${services.length} service${services.length !== 1 ? 's' : ''} found`}
          </p>

          {/* Error */}
          {error && (
            <div className="bg-red-900/20 border border-red-800/40 rounded-xl px-4 py-3 text-red-400 text-sm mb-4 flex items-center gap-2">
              <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
              <button onClick={fetchServices} className="ml-auto underline text-xs">Retry</button>
            </div>
          )}

          {/* Loading skeleton */}
          {loading && (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-[#1E293B] border border-blue-900/20 rounded-2xl p-5 animate-pulse">
                  <div className="flex items-start justify-between mb-3">
                    <div className="h-8 w-32 bg-slate-700/50 rounded" />
                    <div className="h-4 w-4 rounded-full bg-slate-700/50" />
                  </div>
                  <div className="h-4 w-3/4 bg-slate-700/50 rounded mb-2" />
                  <div className="h-3 w-full bg-slate-700/50 rounded mb-1" />
                  <div className="h-3 w-5/6 bg-slate-700/50 rounded mb-4" />
                  <div className="flex gap-2">
                    <div className="h-8 flex-1 bg-slate-700/50 rounded-lg" />
                    <div className="h-8 flex-1 bg-slate-700/50 rounded-lg" />
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Services Grid */}
          {!loading && !error && (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
              {services.length === 0 ? (
                <div className="col-span-3 text-center py-16 text-slate-500">
                  <svg className="w-12 h-12 mx-auto mb-3 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2v-4M9 21H5a2 2 0 01-2-2v-4m0 0h18" />
                  </svg>
                  <p className="text-sm">No services found.</p>
                  <button onClick={openAdd} className="mt-3 text-blue-400 text-sm underline">Add your first service</button>
                </div>
              ) : (
                services.map((service) => {
                  const isActive = Boolean(service.is_active)
                  return (
                    <div
                      key={service.id}
                      className={`bg-[#1E293B] border rounded-2xl p-5 hover:border-blue-700/50 transition-all duration-300 group ${
                        isActive ? 'border-blue-900/30' : 'border-red-900/30 opacity-70'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{service.icon}</span>
                          <span className="text-xs text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded-full border border-blue-800/30">
                            {service.category_icon} {service.category}
                          </span>
                        </div>
                        {/* Active/Inactive toggle */}
                        <button
                          onClick={() => handleToggle(service)}
                          disabled={togglingId === service.id}
                          title={isActive ? 'Click to deactivate' : 'Click to activate'}
                          className="flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full transition-all duration-200 flex-shrink-0 disabled:opacity-50"
                          style={{
                            background: isActive ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)',
                            border: isActive ? '1px solid rgba(16,185,129,0.3)' : '1px solid rgba(239,68,68,0.3)',
                            color: isActive ? '#34d399' : '#f87171',
                          }}
                        >
                          {togglingId === service.id ? (
                            <span className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <span className={`w-2 h-2 rounded-full ${isActive ? 'bg-emerald-400' : 'bg-red-400'}`} />
                          )}
                          {isActive ? 'Active' : 'Inactive'}
                        </button>
                      </div>

                      <h3 className="text-white font-semibold text-sm mb-2 leading-snug">{service.title}</h3>
                      <p className="text-slate-400 text-xs leading-relaxed line-clamp-2 mb-4">{service.description}</p>

                      {service.duration && (
                        <span className="inline-flex items-center text-xs text-amber-400 bg-amber-900/20 border border-amber-800/30 px-2 py-0.5 rounded-full mb-3">
                          ⏱ {service.duration}
                        </span>
                      )}

                      <div className="flex gap-2 mt-auto">
                        <button
                          onClick={() => setViewModal(service)}
                          className="flex-1 text-xs text-slate-400 bg-slate-800/60 hover:bg-blue-900/30 hover:text-blue-400 border border-slate-700/50 hover:border-blue-700/50 rounded-lg py-2 transition-all duration-200"
                        >
                          View Details
                        </button>
                        <button
                          onClick={() => openEdit(service)}
                          className="flex-1 text-xs text-blue-400 bg-blue-900/20 hover:bg-blue-600 hover:text-white border border-blue-800/40 hover:border-blue-600 rounded-lg py-2 transition-all duration-200"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => setDeleteConfirm(service)}
                          className="text-xs text-red-400 bg-red-900/10 hover:bg-red-600 hover:text-white border border-red-800/30 hover:border-red-600 rounded-lg py-2 px-3 transition-all duration-200"
                        >
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  )
                })
              )}
            </div>
          )}
        </main>
      </div>

      {/* View Details Modal */}
      {viewModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl p-6 w-full max-w-lg max-h-[85vh] overflow-y-auto shadow-2xl">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <span className="text-3xl">{viewModal.icon}</span>
                <div>
                  <h2 className="text-white font-bold text-lg leading-snug">{viewModal.title}</h2>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded-full border border-blue-800/30">
                      {viewModal.category_icon} {viewModal.category}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      viewModal.is_active
                        ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/30'
                        : 'bg-red-900/30 text-red-400 border border-red-800/30'
                    }`}>
                      {viewModal.is_active ? '● Active' : '○ Inactive'}
                    </span>
                  </div>
                </div>
              </div>
              <button onClick={() => setViewModal(null)} className="text-slate-500 hover:text-white transition-colors ml-4 flex-shrink-0">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <p className="text-slate-300 text-sm mb-5 leading-relaxed">{viewModal.description}</p>

            {parseJsonField(viewModal.whats_included).length > 0 && (
              <div className="mb-4">
                <h4 className="text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">What&apos;s Included</h4>
                <ul className="space-y-1.5">
                  {parseJsonField(viewModal.whats_included).map((item, i) => (
                    <li key={i} className="text-slate-300 text-sm flex items-center space-x-2">
                      <span className="text-blue-500">✓</span><span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {parseJsonField(viewModal.use_cases).length > 0 && (
              <div className="mb-4">
                <h4 className="text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">Use Cases</h4>
                <ul className="space-y-1.5">
                  {parseJsonField(viewModal.use_cases).map((item, i) => (
                    <li key={i} className="text-slate-300 text-sm flex items-center space-x-2">
                      <span className="text-purple-500">→</span><span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {parseJsonField(viewModal.capabilities).length > 0 && (
              <div className="mb-4">
                <h4 className="text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">Capabilities</h4>
                <ul className="space-y-1.5">
                  {parseJsonField(viewModal.capabilities).map((item, i) => (
                    <li key={i} className="text-slate-300 text-sm flex items-center space-x-2">
                      <span className="text-emerald-500">⚡</span><span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {parseJsonField(viewModal.examples).length > 0 && (
              <div className="mb-4">
                <h4 className="text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">Examples</h4>
                <ul className="space-y-1.5">
                  {parseJsonField(viewModal.examples).map((item, i) => (
                    <li key={i} className="text-slate-300 text-sm flex items-center space-x-2">
                      <span className="text-amber-500">•</span><span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {viewModal.deliverables && (
              <div className="mb-4">
                <h4 className="text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">Deliverables</h4>
                <p className="text-slate-300 text-sm">{viewModal.deliverables}</p>
              </div>
            )}

            {viewModal.ideal_for && (
              <div className="p-3 bg-blue-900/20 border border-blue-800/30 rounded-xl mt-4">
                <p className="text-xs text-blue-400 font-semibold mb-1">Ideal For</p>
                <p className="text-slate-300 text-sm">{viewModal.ideal_for}</p>
              </div>
            )}

            {viewModal.powered_by && (
              <div className="mt-3 p-3 bg-purple-900/20 border border-purple-800/30 rounded-xl">
                <p className="text-xs text-purple-400 font-semibold mb-1">Powered By</p>
                <p className="text-slate-300 text-sm">{viewModal.powered_by}</p>
              </div>
            )}

            {viewModal.tools && (
              <div className="mt-3 p-3 bg-slate-800/50 border border-slate-700/30 rounded-xl">
                <p className="text-xs text-slate-400 font-semibold mb-1">Tools</p>
                <p className="text-slate-300 text-sm">{viewModal.tools}</p>
              </div>
            )}

            {viewModal.duration && (
              <div className="mt-3 inline-flex items-center text-sm text-amber-400 bg-amber-900/20 border border-amber-800/30 px-3 py-1.5 rounded-full">
                ⏱ Duration: {viewModal.duration}
              </div>
            )}

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => { setViewModal(null); openEdit(viewModal) }}
                className="flex-1 bg-blue-900/30 hover:bg-blue-600 text-blue-400 hover:text-white border border-blue-800/40 py-2.5 rounded-xl font-medium transition-all duration-200 text-sm"
              >
                Edit Service
              </button>
              <button
                onClick={() => setViewModal(null)}
                className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium transition-all duration-200 text-sm"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit / Add Modal */}
      {(editModal || addModal) && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 pt-6 pb-4 border-b border-blue-900/30">
              <h2 className="text-white font-bold text-lg">{addModal ? 'Add New Service' : 'Edit Service'}</h2>
              <button
                onClick={() => { setEditModal(null); setAddModal(false) }}
                className="text-slate-500 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="px-6 py-5 space-y-4">
              {/* Title & Icon row */}
              <div className="grid grid-cols-4 gap-3">
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Icon (emoji)</label>
                  <input
                    type="text"
                    value={editForm.icon}
                    onChange={(e) => setEditForm((f) => ({ ...f, icon: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all text-center text-xl"
                    placeholder="🔧"
                  />
                </div>
                <div className="col-span-3">
                  <label className="text-xs text-slate-400 mb-1 block">Title *</label>
                  <input
                    type="text"
                    value={editForm.title}
                    onChange={(e) => setEditForm((f) => ({ ...f, title: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all"
                    placeholder="Service title"
                  />
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="text-xs text-slate-400 mb-1 block">Description *</label>
                <textarea
                  value={editForm.description}
                  onChange={(e) => setEditForm((f) => ({ ...f, description: e.target.value }))}
                  rows={3}
                  className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all resize-none"
                  placeholder="Describe this service..."
                />
              </div>

              {/* Category & Status row */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Category *</label>
                  <select
                    value={editForm.category}
                    onChange={(e) => handleCategoryIconSync(e.target.value)}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all"
                  >
                    {CATEGORY_OPTIONS.map((c) => (
                      <option key={c.label} value={c.label}>{c.icon} {c.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Status</label>
                  <button
                    type="button"
                    onClick={() => setEditForm((f) => ({ ...f, is_active: !f.is_active }))}
                    className={`w-full flex items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium border transition-all duration-200 ${
                      editForm.is_active
                        ? 'bg-emerald-900/30 text-emerald-400 border-emerald-800/40 hover:bg-emerald-600 hover:text-white hover:border-emerald-600'
                        : 'bg-red-900/20 text-red-400 border-red-800/30 hover:bg-red-600 hover:text-white hover:border-red-600'
                    }`}
                  >
                    <span className={`w-2 h-2 rounded-full ${editForm.is_active ? 'bg-emerald-400' : 'bg-red-400'}`} />
                    {editForm.is_active ? 'Active' : 'Inactive'}
                    <span className="text-xs opacity-60">(click to toggle)</span>
                  </button>
                </div>
              </div>

              {/* Duration & Sort order */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Duration</label>
                  <input
                    type="text"
                    value={editForm.duration}
                    onChange={(e) => setEditForm((f) => ({ ...f, duration: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all"
                    placeholder="e.g. 7-Day Sprint"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Sort Order</label>
                  <input
                    type="number"
                    value={editForm.sort_order}
                    onChange={(e) => setEditForm((f) => ({ ...f, sort_order: Number(e.target.value) }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all"
                  />
                </div>
              </div>

              {/* Multi-line list fields */}
              {[
                { key: 'whats_included', label: "What's Included (one per line)" },
                { key: 'use_cases', label: 'Use Cases (one per line)' },
                { key: 'capabilities', label: 'Capabilities (one per line)' },
                { key: 'examples', label: 'Examples (one per line)' },
              ].map(({ key, label }) => (
                <div key={key}>
                  <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                  <textarea
                    value={editForm[key as keyof EditForm] as string}
                    onChange={(e) => setEditForm((f) => ({ ...f, [key]: e.target.value }))}
                    rows={3}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all resize-none font-mono"
                    placeholder={`Enter each item on a new line...`}
                  />
                </div>
              ))}

              {/* Single-line fields */}
              {[
                { key: 'deliverables', label: 'Deliverables', placeholder: 'e.g. Design → Build → Deploy → Monitor' },
                { key: 'ideal_for', label: 'Ideal For', placeholder: 'e.g. Founders, CXOs, and teams...' },
                { key: 'powered_by', label: 'Powered By', placeholder: 'e.g. GPT-4/5 models, RAG systems...' },
                { key: 'tools', label: 'Tools', placeholder: 'e.g. Python, SQL, Power BI...' },
              ].map(({ key, label, placeholder }) => (
                <div key={key}>
                  <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                  <input
                    type="text"
                    value={editForm[key as keyof EditForm] as string}
                    onChange={(e) => setEditForm((f) => ({ ...f, [key]: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all"
                    placeholder={placeholder}
                  />
                </div>
              ))}

              {/* Error */}
              {saveError && (
                <div className="bg-red-900/20 border border-red-800/40 rounded-xl px-4 py-3 text-red-400 text-sm flex items-center gap-2">
                  <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {saveError}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex gap-3 px-6 pb-6">
              <button
                onClick={() => { setEditModal(null); setAddModal(false) }}
                className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium transition-all duration-200 text-sm"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white py-2.5 rounded-xl font-medium transition-all duration-200 text-sm flex items-center justify-center gap-2"
              >
                {saving ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Saving...
                  </>
                ) : (
                  addModal ? 'Add Service' : 'Save Changes'
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-red-900/40 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-red-900/30 border border-red-800/40 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold">Delete Service</h3>
                <p className="text-slate-400 text-xs mt-0.5">This action cannot be undone.</p>
              </div>
            </div>
            <p className="text-slate-300 text-sm mb-5">
              Are you sure you want to delete <span className="text-white font-semibold">&ldquo;{deleteConfirm.title}&rdquo;</span>?
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium transition-all duration-200 text-sm"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 bg-red-600 hover:bg-red-500 text-white py-2.5 rounded-xl font-medium transition-all duration-200 text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </AuthGuard>
  )
}
