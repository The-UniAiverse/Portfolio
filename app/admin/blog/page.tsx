'use client'

import { useState, useEffect, useCallback } from 'react'
import AdminSidebar from '@/components/admin/AdminSidebar'
import AdminHeader from '@/components/admin/AdminHeader'
import AuthGuard from '@/components/admin/AuthGuard'

interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  content: string
  category: string
  tags: string[] | string
  status: 'published' | 'draft'
  date: string
  read_time: string
}

const categories = ['All', 'AI Trends', 'Technical', 'MLOps', 'Case Study', 'News']

const emptyForm = {
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  category: 'AI Trends',
  tags: '',
  status: 'draft' as const,
  date: new Date().toISOString().split('T')[0],
  read_time: '5 min read',
}

function parseTags(tags: string[] | string): string[] {
  if (Array.isArray(tags)) return tags
  try { return JSON.parse(tags) } catch { return [] }
}

export default function BlogAdmin() {
  const [posts, setPosts] = useState<BlogPost[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filterCategory, setFilterCategory] = useState('All')
  const [filterStatus, setFilterStatus] = useState<'all' | 'published' | 'draft'>('all')
  const [showForm, setShowForm] = useState(false)
  const [editPost, setEditPost] = useState<BlogPost | null>(null)
  const [form, setForm] = useState(emptyForm)
  const [deleteId, setDeleteId] = useState<number | null>(null)
  const [saving, setSaving] = useState(false)

  const fetchPosts = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filterStatus !== 'all') params.set('status', filterStatus)
      if (filterCategory !== 'All') params.set('category', filterCategory)
      if (search) params.set('search', search)
      const res = await fetch(`/api/admin/blog?${params}`)
      const data = await res.json()
      if (data.success) setPosts(data.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [filterStatus, filterCategory, search])

  useEffect(() => {
    const t = setTimeout(() => fetchPosts(), 300)
    return () => clearTimeout(t)
  }, [fetchPosts])

  const openAdd = () => { setEditPost(null); setForm(emptyForm); setShowForm(true) }

  const openEdit = (post: BlogPost) => {
    setEditPost(post)
    setForm({
      title: post.title,
      slug: post.slug,
      excerpt: post.excerpt,
      content: post.content,
      category: post.category,
      tags: parseTags(post.tags).join(', '),
      status: post.status,
      date: post.date?.split('T')[0] || new Date().toISOString().split('T')[0],
      read_time: post.read_time,
    })
    setShowForm(true)
  }

  const handleSave = async () => {
    if (!form.title) return
    setSaving(true)
    try {
      const payload = { ...form, tags: form.tags.split(',').map((t) => t.trim()).filter(Boolean) }
      let res
      if (editPost) {
        res = await fetch(`/api/admin/blog/${editPost.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      } else {
        res = await fetch('/api/admin/blog', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      }
      if (res.ok) { setShowForm(false); fetchPosts() }
    } catch (err) {
      console.error(err)
    } finally {
      setSaving(false)
    }
  }

  const toggleStatus = async (post: BlogPost) => {
    const newStatus = post.status === 'published' ? 'draft' : 'published'
    await fetch(`/api/admin/blog/${post.id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: newStatus }) })
    fetchPosts()
  }

  const handleDelete = async (id: number) => {
    await fetch(`/api/admin/blog/${id}`, { method: 'DELETE' })
    setDeleteId(null)
    fetchPosts()
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-[#0A0F1E]">
        <AdminSidebar />
        <main className="flex-1 ml-64 p-8">
          <div className="flex items-start justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-white">Blog Posts</h1>
              <p className="text-slate-400 mt-1 text-sm">Create and manage blog content — stored in MySQL</p>
            </div>
            <button onClick={openAdd} className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg shadow-blue-600/30">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
              <span>New Post</span>
            </button>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-5">
            <div className="relative flex-1">
              <svg className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <input type="text" placeholder="Search posts..." value={search} onChange={(e) => setSearch(e.target.value)} className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
            </div>
            <div className="flex gap-2">
              {(['all', 'published', 'draft'] as const).map((s) => (
                <button key={s} onClick={() => setFilterStatus(s)} className={`px-3 py-2 rounded-xl text-xs font-medium capitalize transition-all ${filterStatus === s ? (s === 'published' ? 'bg-emerald-600 text-white' : s === 'draft' ? 'bg-amber-600 text-white' : 'bg-blue-600 text-white') : 'bg-[#1E293B] text-slate-400 border border-blue-900/30 hover:text-white'}`}>{s}</button>
              ))}
            </div>
          </div>
          <div className="flex gap-2 mb-5 flex-wrap">
            {categories.map((cat) => (
              <button key={cat} onClick={() => setFilterCategory(cat)} className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${filterCategory === cat ? 'bg-purple-600 text-white' : 'bg-[#1E293B] text-slate-400 border border-blue-900/30 hover:text-white'}`}>{cat}</button>
            ))}
          </div>

          <p className="text-slate-500 text-sm mb-4">{posts.length} post{posts.length !== 1 ? 's' : ''}</p>

          {/* Table */}
          <div className="bg-[#1E293B] border border-blue-900/30 rounded-2xl overflow-hidden">
            {loading ? (
              <div className="flex items-center justify-center py-16">
                <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-blue-900/30">
                      <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Title</th>
                      <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider hidden md:table-cell">Category</th>
                      <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider hidden lg:table-cell">Date</th>
                      <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
                      <th className="text-right px-5 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {posts.map((post) => (
                      <tr key={post.id} className="border-b border-blue-900/20 last:border-0 hover:bg-blue-900/10 transition-colors">
                        <td className="px-5 py-4">
                          <div>
                            <p className="text-white font-medium text-sm">{post.title}</p>
                            <p className="text-slate-500 text-xs mt-0.5 line-clamp-1">{post.excerpt}</p>
                            <div className="flex gap-1 mt-1.5">
                              {parseTags(post.tags).slice(0, 3).map((tag) => (
                                <span key={tag} className="text-xs text-blue-400 bg-blue-900/20 px-1.5 py-0.5 rounded">#{tag}</span>
                              ))}
                            </div>
                          </div>
                        </td>
                        <td className="px-5 py-4 hidden md:table-cell">
                          <span className="text-xs text-purple-400 bg-purple-900/20 px-2 py-1 rounded-lg">{post.category}</span>
                        </td>
                        <td className="px-5 py-4 hidden lg:table-cell">
                          <p className="text-slate-400 text-xs">{post.date ? new Date(post.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '-'}</p>
                          <p className="text-slate-500 text-xs">{post.read_time}</p>
                        </td>
                        <td className="px-5 py-4">
                          <button onClick={() => toggleStatus(post)} className={`text-xs px-2.5 py-1 rounded-full font-medium transition-all ${post.status === 'published' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/40 hover:bg-emerald-600 hover:text-white' : 'bg-amber-900/30 text-amber-400 border border-amber-800/40 hover:bg-amber-600 hover:text-white'}`}>
                            {post.status === 'published' ? '● Published' : '○ Draft'}
                          </button>
                        </td>
                        <td className="px-5 py-4">
                          <div className="flex items-center justify-end gap-2">
                            <button onClick={() => openEdit(post)} className="text-xs text-blue-400 hover:text-blue-300 bg-blue-900/20 hover:bg-blue-900/40 border border-blue-800/30 px-3 py-1.5 rounded-lg transition-all">Edit</button>
                            <button onClick={() => setDeleteId(post.id)} className="text-xs text-red-400 hover:text-red-300 bg-red-900/10 hover:bg-red-900/30 border border-red-900/20 px-3 py-1.5 rounded-lg transition-all">Delete</button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {posts.length === 0 && <div className="text-center py-12"><p className="text-slate-500 text-sm">No posts found.</p></div>}
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-blue-900/40 rounded-2xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-white font-bold text-lg">{editPost ? 'Edit Post' : 'New Blog Post'}</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-500 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Title *</label>
                <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="Blog post title..." className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Excerpt</label>
                <textarea value={form.excerpt} onChange={(e) => setForm({ ...form, excerpt: e.target.value })} rows={2} placeholder="Short description..." className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all resize-none" />
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Content</label>
                <textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} rows={6} placeholder="Write your blog post content here..." className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all resize-none" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Category</label>
                  <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all">
                    {categories.filter((c) => c !== 'All').map((c) => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Status</label>
                  <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value as 'published' | 'draft' })} className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all">
                    <option value="draft">Draft</option>
                    <option value="published">Published</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Tags (comma separated)</label>
                  <input value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} placeholder="AI, Business, Automation" className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
                </div>
                <div>
                  <label className="text-xs text-slate-400 font-medium mb-1.5 block">Read Time</label>
                  <input value={form.read_time} onChange={(e) => setForm({ ...form, read_time: e.target.value })} placeholder="5 min read" className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition-all" />
                </div>
              </div>
              <div>
                <label className="text-xs text-slate-400 font-medium mb-1.5 block">Date</label>
                <input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} className="w-full bg-[#1E293B] border border-blue-900/40 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500 transition-all" />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setShowForm(false)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-xl font-medium text-sm transition-all">Cancel</button>
              <button onClick={handleSave} disabled={!form.title || saving} className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed text-white py-2.5 rounded-xl font-medium text-sm transition-all shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2">
                {saving ? <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/><span>Saving...</span></> : <span>{editPost ? 'Save Changes' : 'Create Post'}</span>}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirm */}
      {deleteId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#0F172A] border border-red-900/40 rounded-2xl p-6 w-full max-w-sm shadow-2xl text-center">
            <div className="w-14 h-14 bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </div>
            <h3 className="text-white font-bold text-lg mb-2">Delete Post?</h3>
            <p className="text-slate-400 text-sm mb-6">This will permanently remove the post from the database.</p>
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
