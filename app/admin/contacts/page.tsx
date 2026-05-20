'use client'

import { useState, useEffect, useCallback } from 'react'
import AdminSidebar from '@/components/admin/AdminSidebar'
import AdminHeader from '@/components/admin/AdminHeader'
import AuthGuard from '@/components/admin/AuthGuard'

// ─── Inquiries ────────────────────────────────────────────────────────────────

interface Inquiry {
  id: number
  name: string
  email: string
  company: string
  service: string
  message: string
  status: 'new' | 'in-progress' | 'resolved'
  created_at: string
}

const statusConfig = {
  new: { label: 'New', color: 'bg-blue-900/30 text-blue-400 border-blue-800/40' },
  'in-progress': { label: 'In Progress', color: 'bg-amber-900/30 text-amber-400 border-amber-800/40' },
  resolved: { label: 'Resolved', color: 'bg-emerald-900/30 text-emerald-400 border-emerald-800/40' },
}

// ─── Contact Info ─────────────────────────────────────────────────────────────

interface ContactInfoItem {
  id: number
  icon: string
  title: string
  details: string[] | string
  link: string | null
  sort_order: number
}

type InfoForm = {
  icon: string
  title: string
  details: string
  link: string
  sort_order: number
}

const EMPTY_INFO_FORM: InfoForm = { icon: '📍', title: '', details: '', link: '', sort_order: 0 }

function parseDetails(val: string[] | string | null | undefined): string[] {
  if (!val) return []
  if (Array.isArray(val)) return val
  try { return JSON.parse(val) } catch { return [String(val)] }
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ContactsAdmin() {
  const [activeTab, setActiveTab] = useState<'inquiries' | 'contact-info'>('inquiries')

  // ── Inquiries state ──
  const [inquiries, setInquiries] = useState<Inquiry[]>([])
  const [loadingInq, setLoadingInq] = useState(true)
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState<'all' | 'new' | 'in-progress' | 'resolved'>('all')
  const [viewItem, setViewItem] = useState<Inquiry | null>(null)

  // ── Contact Info state ──
  const [infoItems, setInfoItems] = useState<ContactInfoItem[]>([])
  const [loadingInfo, setLoadingInfo] = useState(true)
  const [editInfo, setEditInfo] = useState<ContactInfoItem | null>(null)
  const [addInfo, setAddInfo] = useState(false)
  const [infoForm, setInfoForm] = useState<InfoForm>(EMPTY_INFO_FORM)
  const [savingInfo, setSavingInfo] = useState(false)
  const [infoError, setInfoError] = useState('')
  const [deleteInfoConfirm, setDeleteInfoConfirm] = useState<ContactInfoItem | null>(null)
  const [infoSaveMsg, setInfoSaveMsg] = useState('')

  // ── Fetch inquiries ──
  const fetchInquiries = useCallback(async () => {
    setLoadingInq(true)
    try {
      const params = new URLSearchParams()
      if (filterStatus !== 'all') params.set('status', filterStatus)
      if (search) params.set('search', search)
      const res = await fetch(`/api/admin/contacts?${params}`)
      const data = await res.json()
      if (data.success) setInquiries(data.data)
    } catch (err) { console.error(err) }
    finally { setLoadingInq(false) }
  }, [filterStatus, search])

  useEffect(() => {
    const t = setTimeout(() => fetchInquiries(), 300)
    return () => clearTimeout(t)
  }, [fetchInquiries])

  // ── Fetch contact info ──
  const fetchContactInfo = useCallback(async () => {
    setLoadingInfo(true)
    try {
      const res = await fetch('/api/admin/contact-info')
      const data = await res.json()
      if (data.success) setInfoItems(data.data)
    } catch (err) { console.error(err) }
    finally { setLoadingInfo(false) }
  }, [])

  useEffect(() => {
    if (activeTab === 'contact-info') fetchContactInfo()
  }, [activeTab, fetchContactInfo])

  // ── Inquiry actions ──
  const updateStatus = async (id: number, status: Inquiry['status']) => {
    await fetch(`/api/admin/contacts/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
    fetchInquiries()
    if (viewItem?.id === id) setViewItem((prev) => prev ? { ...prev, status } : null)
  }

  const counts = {
    all: inquiries.length,
    new: inquiries.filter((i) => i.status === 'new').length,
    'in-progress': inquiries.filter((i) => i.status === 'in-progress').length,
    resolved: inquiries.filter((i) => i.status === 'resolved').length,
  }

  // ── Contact Info actions ──
  const openEditInfo = (item: ContactInfoItem) => {
    setInfoForm({
      icon: item.icon,
      title: item.title,
      details: parseDetails(item.details).join('\n'),
      link: item.link || '',
      sort_order: item.sort_order,
    })
    setInfoError('')
    setInfoSaveMsg('')
    setEditInfo(item)
    setAddInfo(false)
  }

  const openAddInfo = () => {
    setInfoForm(EMPTY_INFO_FORM)
    setInfoError('')
    setInfoSaveMsg('')
    setAddInfo(true)
    setEditInfo(null)
  }

  const handleSaveInfo = async () => {
    if (!infoForm.title.trim()) { setInfoError('Title is required.'); return }
    setSavingInfo(true)
    setInfoError('')
    const payload = {
      ...infoForm,
      details: infoForm.details.split('\n').map((s) => s.trim()).filter(Boolean),
      link: infoForm.link.trim() || null,
    }
    try {
      const res = addInfo
        ? await fetch('/api/admin/contact-info', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        : await fetch(`/api/admin/contact-info/${editInfo!.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      const json = await res.json()
      if (json.success) {
        setEditInfo(null)
        setAddInfo(false)
        setInfoSaveMsg('Contact information saved successfully.')
        fetchContactInfo()
        setTimeout(() => setInfoSaveMsg(''), 4000)
      } else {
        setInfoError(json.error || 'Failed to save')
      }
    } catch { setInfoError('Network error') }
    finally { setSavingInfo(false) }
  }

  const handleDeleteInfo = async () => {
    if (!deleteInfoConfirm) return
    await fetch(`/api/admin/contact-info/${deleteInfoConfirm.id}`, { method: 'DELETE' })
    setDeleteInfoConfirm(null)
    fetchContactInfo()
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-[#0A0F1E]">
        <AdminSidebar />
        <main className="flex-1 ml-64 p-8">
          <AdminHeader title="Contacts" subtitle="Manage inquiries and website contact information" />

          {/* Tab switcher */}
          <div className="flex gap-2 mb-6 bg-[#1E293B] border border-blue-900/30 rounded-2xl p-1 w-fit">
            <button
              onClick={() => setActiveTab('inquiries')}
              className={`px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                activeTab === 'inquiries'
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Contact Inquiries
            </button>
            <button
              onClick={() => setActiveTab('contact-info')}
              className={`px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                activeTab === 'contact-info'
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Contact Information
            </button>
          </div>

          {/* ── INQUIRIES TAB ── */}
          {activeTab === 'inquiries' && (
            <>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                {(['all', 'new', 'in-progress', 'resolved'] as const).map((s) => (
                  <button
                    key={s}
                    onClick={() => setFilterStatus(s)}
                    className={`p-4 rounded-2xl border text-left transition-all ${
                      filterStatus === s
                        ? 'bg-blue-600 border-blue-500 shadow-lg shadow-blue-600/30'
                        : 'bg-[#1E293B] border-blue-900/30 hover:border-blue-700/50'
                    }`}
                  >
                    <p className="text-2xl font-bold text-white">{counts[s]}</p>
                    <p className={`text-xs capitalize mt-0.5 ${filterStatus === s ? 'text-blue-100' : 'text-slate-400'}`}>
                      {s === 'all' ? 'All Inquiries' : s.replace('-', ' ')}
                    </p>
                  </button>
                ))}
              </div>

              <div className="relative mb-5">
                <svg className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Search by name, email, company or service..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all"
                />
              </div>

              <p className="text-slate-500 text-sm mb-4">{inquiries.length} inquir{inquiries.length !== 1 ? 'ies' : 'y'}</p>

              <div className="bg-[#1E293B] border border-blue-900/30 rounded-2xl overflow-hidden">
                {loadingInq ? (
                  <div className="flex items-center justify-center py-16">
                    <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-blue-900/30">
                          <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Contact</th>
                          <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider hidden md:table-cell">Service</th>
                          <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider hidden lg:table-cell">Date</th>
                          <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
                          <th className="text-right px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {inquiries.map((item) => (
                          <tr key={item.id} className="border-b border-blue-900/20 last:border-0 hover:bg-blue-900/10 transition-colors">
                            <td className="px-5 py-4">
                              <div className="flex items-center space-x-3">
                                <div className="w-9 h-9 rounded-xl bg-blue-600/20 border border-blue-600/30 flex items-center justify-center text-blue-400 font-semibold text-sm flex-shrink-0">
                                  {item.name.charAt(0)}
                                </div>
                                <div>
                                  <p className="text-white font-medium text-sm">{item.name}</p>
                                  <p className="text-slate-500 text-xs">{item.email}</p>
                                  <p className="text-slate-500 text-xs">{item.company}</p>
                                </div>
                              </div>
                            </td>
                            <td className="px-5 py-4 hidden md:table-cell">
                              <p className="text-slate-300 text-xs line-clamp-2 max-w-[200px]">{item.service}</p>
                            </td>
                            <td className="px-5 py-4 hidden lg:table-cell">
                              <p className="text-slate-400 text-xs">
                                {new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                              </p>
                            </td>
                            <td className="px-5 py-4">
                              <span className={`text-xs px-2.5 py-1 rounded-full font-medium border ${statusConfig[item.status].color}`}>
                                {statusConfig[item.status].label}
                              </span>
                            </td>
                            <td className="px-5 py-4">
                              <div className="flex items-center justify-end gap-2">
                                <button
                                  onClick={() => setViewItem(item)}
                                  className="text-xs text-blue-400 hover:text-blue-300 bg-blue-900/20 hover:bg-blue-900/40 border border-blue-800/30 px-3 py-1.5 rounded-lg transition-all"
                                >
                                  View
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    {inquiries.length === 0 && (
                      <div className="text-center py-12">
                        <p className="text-slate-500 text-sm">No inquiries found.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          )}

          {/* ── CONTACT INFO TAB ── */}
          {activeTab === 'contact-info' && (
            <>
              <div className="flex items-center justify-between mb-5">
                <p className="text-slate-400 text-sm">
                  Edit the address, phone, email, and business hours shown on the website contact section.
                </p>
                <button
                  onClick={openAddInfo}
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium px-4 py-2 rounded-xl transition-all duration-200 shadow-lg shadow-blue-600/20"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Add Entry
                </button>
              </div>

              {infoSaveMsg && (
                <div className="bg-emerald-900/20 border border-emerald-800/40 rounded-xl px-4 py-2.5 text-emerald-400 text-sm mb-4 flex items-center justify-between">
                  <span>✓ {infoSaveMsg}</span>
                  <button onClick={() => setInfoSaveMsg('')} className="text-xs opacity-60 hover:opacity-100 ml-4">Dismiss</button>
                </div>
              )}

              {loadingInfo ? (
                <div className="flex items-center justify-center py-16">
                  <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {infoItems.map((item) => (
                    <div key={item.id} className="bg-[#1E293B] border border-blue-900/30 rounded-2xl p-5 hover:border-blue-700/50 transition-all duration-200">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <span className="text-3xl">{item.icon}</span>
                          <div>
                            <h3 className="text-white font-semibold text-sm">{item.title}</h3>
                            {item.link && (
                              <a href={item.link} className="text-blue-400 text-xs hover:underline truncate block max-w-[200px]">{item.link}</a>
                            )}
                          </div>
                        </div>
                        <div className="flex gap-2 flex-shrink-0">
                          <button
                            onClick={() => openEditInfo(item)}
                            className="text-xs text-blue-400 bg-blue-900/20 hover:bg-blue-600 hover:text-white border border-blue-800/40 px-3 py-1.5 rounded-lg transition-all duration-200"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => setDeleteInfoConfirm(item)}
                            className="text-xs text-red-400 bg-red-900/10 hover:bg-red-600 hover:text-white border border-red-800/30 px-3 py-1.5 rounded-lg transition-all duration-200"
                          >
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                      <div className="space-y-1 pl-12">
                        {parseDetails(item.details).map((d, i) => (
                          <p key={i} className="text-slate-400 text-xs">{d}</p>
                        ))}
                      </div>
                    </div>
                  ))}

                  {infoItems.length === 0 && (
                    <div className="col-span-2 text-center py-16 text-slate-500">
                      <p className="text-sm">No contact info entries found.</p>
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </main>
      </div>

      {/* ── Inquiry Detail Modal ── */}
      {viewItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl p-6 w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-white font-bold text-lg">Inquiry Details</h2>
              <button onClick={() => setViewItem(null)} className="text-slate-500 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="flex items-center space-x-4 mb-5 p-4 bg-blue-900/20 border border-blue-800/30 rounded-xl">
              <div className="w-12 h-12 rounded-xl bg-blue-600/30 border border-blue-600/40 flex items-center justify-center text-blue-400 font-bold text-lg">
                {viewItem.name.charAt(0)}
              </div>
              <div>
                <p className="text-white font-semibold">{viewItem.name}</p>
                <p className="text-slate-400 text-sm">{viewItem.email}</p>
                <p className="text-slate-500 text-xs">{viewItem.company}</p>
              </div>
            </div>
            <div className="space-y-4 mb-5">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider font-medium mb-1">Service Interested In</p>
                <p className="text-slate-200 text-sm bg-[#1E293B] px-3 py-2 rounded-lg">{viewItem.service}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider font-medium mb-1">Message</p>
                <p className="text-slate-200 text-sm bg-[#1E293B] px-3 py-2 rounded-lg leading-relaxed">{viewItem.message}</p>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wider font-medium mb-1">Received</p>
                  <p className="text-slate-300 text-sm">
                    {new Date(viewItem.created_at).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                  </p>
                </div>
                <span className={`text-xs px-3 py-1.5 rounded-full font-medium border ${statusConfig[viewItem.status].color}`}>
                  {statusConfig[viewItem.status].label}
                </span>
              </div>
            </div>
            <div className="border-t border-blue-900/30 pt-4">
              <p className="text-xs text-slate-400 font-medium mb-3">Update Status</p>
              <div className="flex gap-2">
                {(['new', 'in-progress', 'resolved'] as const).map((s) => (
                  <button
                    key={s}
                    onClick={() => updateStatus(viewItem.id, s)}
                    className={`flex-1 text-xs py-2 rounded-xl font-medium capitalize transition-all border ${
                      viewItem.status === s ? statusConfig[s].color : 'bg-[#1E293B] text-slate-400 border-blue-900/30 hover:text-white'
                    }`}
                  >
                    {s.replace('-', ' ')}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex gap-3 mt-5">
              <a
                href={`mailto:${viewItem.email}`}
                className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg shadow-blue-600/30"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>Reply via Email</span>
              </a>
              <button onClick={() => setViewItem(null)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all">
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Contact Info Edit / Add Modal ── */}
      {(editInfo || addInfo) && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl w-full max-w-md shadow-2xl">
            <div className="flex items-center justify-between px-6 pt-6 pb-4 border-b border-blue-900/30">
              <h2 className="text-white font-bold text-lg">{addInfo ? 'Add Contact Info Entry' : 'Edit Contact Info'}</h2>
              <button onClick={() => { setEditInfo(null); setAddInfo(false) }} className="text-slate-500 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="px-6 py-5 space-y-4">
              <div className="grid grid-cols-4 gap-3">
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">Icon</label>
                  <input
                    type="text"
                    value={infoForm.icon}
                    onChange={(e) => setInfoForm((f) => ({ ...f, icon: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-xl text-center focus:outline-none focus:border-blue-500"
                    placeholder="📍"
                  />
                </div>
                <div className="col-span-3">
                  <label className="text-xs text-slate-400 mb-1 block">Title *</label>
                  <input
                    type="text"
                    value={infoForm.title}
                    onChange={(e) => setInfoForm((f) => ({ ...f, title: e.target.value }))}
                    className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
                    placeholder="e.g. Address, Phone, Email..."
                  />
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-400 mb-1 block">Details (one line per item)</label>
                <textarea
                  value={infoForm.details}
                  onChange={(e) => setInfoForm((f) => ({ ...f, details: e.target.value }))}
                  rows={4}
                  className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 resize-none font-mono"
                  placeholder={`e.g.\nF/N. 5. First Floor, F building,\nMonika Garden View,\nPimpri, Pune, 411018.`}
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 mb-1 block">Link (optional — for phone/email)</label>
                <input
                  type="text"
                  value={infoForm.link}
                  onChange={(e) => setInfoForm((f) => ({ ...f, link: e.target.value }))}
                  className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
                  placeholder="e.g. tel:+918956837601 or mailto:you@example.com"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 mb-1 block">Sort Order</label>
                <input
                  type="number"
                  value={infoForm.sort_order}
                  onChange={(e) => setInfoForm((f) => ({ ...f, sort_order: Number(e.target.value) }))}
                  className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
                />
              </div>

              {infoError && (
                <div className="bg-red-900/20 border border-red-800/40 rounded-xl px-4 py-3 text-red-400 text-sm">
                  {infoError}
                </div>
              )}
            </div>

            <div className="flex gap-3 px-6 pb-6">
              <button
                onClick={() => { setEditInfo(null); setAddInfo(false) }}
                className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveInfo}
                disabled={savingInfo}
                className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white py-2.5 rounded-xl font-medium text-sm transition-all flex items-center justify-center gap-2"
              >
                {savingInfo ? (
                  <><span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />Saving...</>
                ) : (
                  addInfo ? 'Add Entry' : 'Save Changes'
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Delete Contact Info Confirm ── */}
      {deleteInfoConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-red-900/40 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-red-900/30 border border-red-800/40 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold">Delete Entry</h3>
                <p className="text-slate-400 text-xs mt-0.5">This cannot be undone.</p>
              </div>
            </div>
            <p className="text-slate-300 text-sm mb-5">
              Delete <span className="text-white font-semibold">&ldquo;{deleteInfoConfirm.title}&rdquo;</span>?
            </p>
            <div className="flex gap-3">
              <button onClick={() => setDeleteInfoConfirm(null)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all">
                Cancel
              </button>
              <button onClick={handleDeleteInfo} className="flex-1 bg-red-600 hover:bg-red-500 text-white py-2.5 rounded-xl font-medium text-sm transition-all">
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </AuthGuard>
  )
}
