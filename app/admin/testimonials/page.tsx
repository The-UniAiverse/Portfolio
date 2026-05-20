'use client'

import { useState, useEffect, useCallback } from 'react'
import AdminSidebar from '@/components/admin/AdminSidebar'
import AdminHeader from '@/components/admin/AdminHeader'
import AuthGuard from '@/components/admin/AuthGuard'

interface Testimonial {
  id: number
  quote: string
  author: string
  role: string
  company: string
  avatar: string
  rating: number
}

const emptyForm = { quote: '', author: '', role: '', company: '', avatar: '👤', rating: 5 }
const avatarOptions = ['👤', '👩‍💼', '👨‍💼', '👩‍💻', '👨‍💻', '🧑‍🏫', '👩‍🔬', '👨‍🔬']

export default function TestimonialsAdmin() {
  const [items, setItems] = useState<Testimonial[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState<Testimonial | null>(null)
  const [form, setForm] = useState(emptyForm)
  const [deleteId, setDeleteId] = useState<number | null>(null)
  const [saving, setSaving] = useState(false)

  const fetchItems = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/admin/testimonials')
      const data = await res.json()
      if (data.success) setItems(data.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchItems() }, [fetchItems])

  const openAdd = () => { setEditItem(null); setForm(emptyForm); setShowForm(true) }
  const openEdit = (item: Testimonial) => {
    setEditItem(item)
    setForm({ quote: item.quote, author: item.author, role: item.role, company: item.company, avatar: item.avatar, rating: item.rating })
    setShowForm(true)
  }

  const handleSave = async () => {
    if (!form.quote || !form.author) return
    setSaving(true)
    try {
      let res
      if (editItem) {
        res = await fetch(`/api/admin/testimonials/${editItem.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      } else {
        res = await fetch('/api/admin/testimonials', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      }
      if (res.ok) { setShowForm(false); fetchItems() }
    } catch (err) { console.error(err) }
    finally { setSaving(false) }
  }

  const handleDelete = async (id: number) => {
    await fetch(`/api/admin/testimonials/${id}`, { method: 'DELETE' })
    setDeleteId(null)
    fetchItems()
  }

  const avgRating = items.length > 0 ? (items.reduce((a, b) => a + b.rating, 0) / items.length).toFixed(1) : '0'

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-[#0A0F1E]">
        <AdminSidebar />
        <main className="flex-1 ml-64 p-8">
          <div className="flex items-start justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-white">Testimonials</h1>
              <p className="text-slate-400 mt-1 text-sm">Manage client testimonials — stored in MySQL</p>
            </div>
            <button onClick={openAdd} className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg shadow-blue-600/30">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
              <span>Add Testimonial</span>
            </button>
          </div>

          {/* Stats */}
          <div className="flex items-center space-x-6 mb-6 p-4 bg-[#1E293B] border border-blue-900/30 rounded-2xl">
            <div className="text-center"><p className="text-2xl font-bold text-white">{items.length}</p><p className="text-xs text-slate-400">Total</p></div>
            <div className="w-px h-10 bg-blue-900/40" />
            <div className="text-center"><p className="text-2xl font-bold text-yellow-400">{avgRating}</p><p className="text-xs text-slate-400">Avg Rating</p></div>
            <div className="w-px h-10 bg-blue-900/40" />
            <div className="flex items-center space-x-1">
              {[1,2,3,4,5].map((s) => <svg key={s} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 24 24"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>)}
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-16"><div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" /></div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
              {items.map((item) => (
                <div key={item.id} className="bg-[#1E293B] border border-blue-900/30 rounded-2xl p-5 hover:border-blue-700/50 transition-all flex flex-col">
                  <div className="flex items-center space-x-0.5 mb-3">
                    {[1,2,3,4,5].map((s) => <svg key={s} className={`w-4 h-4 ${s <= item.rating ? 'text-yellow-400' : 'text-slate-600'}`} fill="currentColor" viewBox="0 0 24 24"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>)}
                  </div>
                  <p className="text-slate-300 text-sm italic leading-relaxed flex-1 mb-4">&ldquo;{item.quote}&rdquo;</p>
                  <div className="flex items-center space-x-3 mb-4">
                    <span className="text-2xl">{item.avatar}</span>
                    <div><p className="text-white font-semibold text-sm">{item.author}</p><p className="text-slate-400 text-xs">{item.role}{item.role && item.company ? ', ' : ''}{item.company}</p></div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => openEdit(item)} className="flex-1 text-xs text-blue-400 bg-blue-900/20 hover:bg-blue-600 hover:text-white border border-blue-800/40 hover:border-blue-600 rounded-lg py-2 transition-all">Edit</button>
                    <button onClick={() => setDeleteId(item.id)} className="flex-1 text-xs text-red-400 bg-red-900/10 hover:bg-red-600 hover:text-white border border-red-900/30 hover:border-red-600 rounded-lg py-2 transition-all">Delete</button>
                  </div>
                </div>
              ))}
              {items.length === 0 && <div className="col-span-3 text-center py-12"><p className="text-slate-500">No testimonials yet. Add one!</p></div>}
            </div>
          )}
        </main>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl p-6 w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-white font-bold text-lg">{editItem ? 'Edit Testimonial' : 'Add Testimonial'}</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-500 hover:text-white transition-colors"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg></button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Quote *</label>
                <textarea value={form.quote} onChange={(e) => setForm({ ...form, quote: e.target.value })} rows={3} placeholder="Enter the client testimonial..." className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-3 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all resize-none" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Author Name *</label>
                  <input value={form.author} onChange={(e) => setForm({ ...form, author: e.target.value })} placeholder="John Doe" className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
                </div>
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Role</label>
                  <input value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} placeholder="CEO" className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
                </div>
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Company</label>
                <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} placeholder="Company Name" className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-2 block">Avatar</label>
                <div className="flex gap-2 flex-wrap">
                  {avatarOptions.map((a) => <button key={a} type="button" onClick={() => setForm({ ...form, avatar: a })} className={`text-2xl w-10 h-10 rounded-xl flex items-center justify-center transition-all ${form.avatar === a ? 'bg-blue-600 ring-2 ring-blue-400' : 'bg-[#1E293B] hover:bg-blue-900/30'}`}>{a}</button>)}
                </div>
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-2 block">Rating</label>
                <div className="flex space-x-1">
                  {[1,2,3,4,5].map((s) => <button key={s} type="button" onClick={() => setForm({ ...form, rating: s })} className="transition-transform hover:scale-110"><svg className={`w-7 h-7 ${s <= form.rating ? 'text-yellow-400' : 'text-slate-600'}`} fill="currentColor" viewBox="0 0 24 24"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg></button>)}
                </div>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setShowForm(false)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all">Cancel</button>
              <button onClick={handleSave} disabled={!form.quote || !form.author || saving} className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed text-white py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2">
                {saving ? <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/><span>Saving...</span></> : <span>{editItem ? 'Save Changes' : 'Add Testimonial'}</span>}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirm */}
      {deleteId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-red-900/40 rounded-2xl p-6 w-full max-w-sm shadow-2xl text-center">
            <div className="w-14 h-14 bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4"><svg className="w-7 h-7 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></div>
            <h3 className="text-white font-bold text-lg mb-2">Delete Testimonial?</h3>
            <p className="text-slate-400 text-sm mb-6">This will permanently remove it from the database.</p>
            <div className="flex gap-3">
              <button onClick={() => setDeleteId(null)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all">Cancel</button>
              <button onClick={() => handleDelete(deleteId)} className="flex-1 bg-red-600 hover:bg-red-500 text-white py-2.5 rounded-xl font-medium text-sm transition-all">Delete</button>
            </div>
          </div>
        </div>
      )}
    </AuthGuard>
  )
}
