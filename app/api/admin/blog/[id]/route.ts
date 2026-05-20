import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

// PUT - update a blog post
export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { title, slug, excerpt, content, category, tags, status, read_time, date } = body

    const tagsJson = JSON.stringify(Array.isArray(tags) ? tags : (tags ? tags.split(',').map((t: string) => t.trim()).filter(Boolean) : []))

    await pool.execute(
      'UPDATE blog_posts SET title=?, slug=?, excerpt=?, content=?, category=?, tags=?, status=?, read_time=?, date=? WHERE id=?',
      [title, slug, excerpt || '', content || '', category || 'General', tagsJson, status || 'draft', read_time || '5 min read', date, id]
    )

    const [rows] = await pool.execute('SELECT * FROM blog_posts WHERE id = ?', [id])
    const posts = rows as unknown[]
    if (!posts.length) return NextResponse.json({ success: false, error: 'Post not found' }, { status: 404 })

    return NextResponse.json({ success: true, data: posts[0] })
  } catch (error) {
    console.error('PUT /api/admin/blog/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update blog post' }, { status: 500 })
  }
}

// PATCH - update only status
export async function PATCH(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { status } = body

    await pool.execute('UPDATE blog_posts SET status=? WHERE id=?', [status, id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('PATCH /api/admin/blog/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update status' }, { status: 500 })
  }
}

// DELETE - delete a blog post
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await pool.execute('DELETE FROM blog_posts WHERE id = ?', [id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('DELETE /api/admin/blog/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to delete blog post' }, { status: 500 })
  }
}
