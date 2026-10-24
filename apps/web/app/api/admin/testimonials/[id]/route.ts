import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

// PUT - update a testimonial
export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { quote, author, role, company, avatar, rating } = body

    await pool.execute(
      'UPDATE testimonials SET quote=?, author=?, role=?, company=?, avatar=?, rating=? WHERE id=?',
      [quote, author, role || '', company || '', avatar || '👤', rating || 5, id]
    )

    const [rows] = await pool.execute('SELECT * FROM testimonials WHERE id = ?', [id])
    const items = rows as unknown[]
    if (!items.length) return NextResponse.json({ success: false, error: 'Not found' }, { status: 404 })

    return NextResponse.json({ success: true, data: items[0] })
  } catch (error) {
    console.error('PUT /api/admin/testimonials/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update testimonial' }, { status: 500 })
  }
}

// DELETE - delete a testimonial
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await pool.execute('DELETE FROM testimonials WHERE id = ?', [id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('DELETE /api/admin/testimonials/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to delete testimonial' }, { status: 500 })
  }
}
