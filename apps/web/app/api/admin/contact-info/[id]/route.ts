import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

// PUT - update a contact info entry
export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { icon, title, details, link, sort_order } = body

    if (!title) {
      return NextResponse.json({ success: false, error: 'Title is required' }, { status: 400 })
    }

    const detailsArr = Array.isArray(details)
      ? details
      : String(details).split('\n').map((s: string) => s.trim()).filter(Boolean)

    await pool.execute(
      'UPDATE contact_info SET icon=?, title=?, details=?, link=?, sort_order=? WHERE id=?',
      [icon || '📍', title, JSON.stringify(detailsArr), link || null, sort_order || 0, id]
    )

    const [rows] = await pool.execute('SELECT * FROM contact_info WHERE id = ?', [id])
    const items = rows as unknown[]
    if (!items.length) return NextResponse.json({ success: false, error: 'Not found' }, { status: 404 })

    return NextResponse.json({ success: true, data: items[0] })
  } catch (error) {
    console.error('PUT /api/admin/contact-info/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update' }, { status: 500 })
  }
}

// DELETE - remove a contact info entry
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await pool.execute('DELETE FROM contact_info WHERE id = ?', [id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('DELETE /api/admin/contact-info/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to delete' }, { status: 500 })
  }
}
