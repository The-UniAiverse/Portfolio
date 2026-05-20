import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

// PATCH - update contact status
export async function PATCH(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await req.json()
    const { status } = body

    if (!['new', 'in-progress', 'resolved'].includes(status)) {
      return NextResponse.json({ success: false, error: 'Invalid status' }, { status: 400 })
    }

    await pool.execute('UPDATE contacts SET status=? WHERE id=?', [status, id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('PATCH /api/admin/contacts/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to update contact status' }, { status: 500 })
  }
}

// DELETE - delete a contact
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await pool.execute('DELETE FROM contacts WHERE id = ?', [id])
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('DELETE /api/admin/contacts/[id] error:', error)
    return NextResponse.json({ success: false, error: 'Failed to delete contact' }, { status: 500 })
  }
}
