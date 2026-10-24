import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

// PUT - update a service
export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const {
      title, description, icon, category, category_icon,
      whats_included, use_cases, deliverables, capabilities,
      examples, ideal_for, powered_by, tools, duration,
      is_active, sort_order
    } = body

    if (!title || !description || !category) {
      return NextResponse.json({ success: false, error: 'Title, description, and category are required' }, { status: 400 })
    }

    await pool.execute(
      `UPDATE services SET
        title=?, description=?, icon=?, category=?, category_icon=?,
        whats_included=?, use_cases=?, deliverables=?, capabilities=?,
        examples=?, ideal_for=?, powered_by=?, tools=?, duration=?,
        is_active=?, sort_order=?
       WHERE id=?`,
      [
        title,
        description,
        icon || '🔧',
        category,
        category_icon || '🚀',
        JSON.stringify(Array.isArray(whats_included) ? whats_included : []),
        JSON.stringify(Array.isArray(use_cases) ? use_cases : []),
        deliverables || '',
        JSON.stringify(Array.isArray(capabilities) ? capabilities : []),
        JSON.stringify(Array.isArray(examples) ? examples : []),
        ideal_for || '',
        powered_by || '',
        tools || '',
        duration || '',
        is_active ? 1 : 0,
        sort_order || 0,
        id,
      ]
    )

    const [rows] = await pool.execute('SELECT * FROM services WHERE id = ?', [id])
    const services = rows as unknown[]
    if (!services.length) return NextResponse.json({ success: false, error: 'Service not found' }, { status: 404 })

    return NextResponse.json({ success: true, data: services[0] })
  } catch (error) {
    console.error('PUT /api/admin/services/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update service' }, { status: 500 })
  }
}

// PATCH - toggle active/inactive status
export async function PATCH(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { is_active } = body

    await pool.execute('UPDATE services SET is_active=? WHERE id=?', [is_active ? 1 : 0, id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('PATCH /api/admin/services/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update status' }, { status: 500 })
  }
}

// DELETE - delete a service
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await pool.execute('DELETE FROM services WHERE id = ?', [id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('DELETE /api/admin/services/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to delete service' }, { status: 500 })
  }
}
