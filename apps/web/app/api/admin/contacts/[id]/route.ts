import { NextRequest, NextResponse } from 'next/server'
import { requireAdmin } from '@/lib/admin'
import { CONTACT_STATUSES, contactMessages, parseId, type ContactStatus } from '@/lib/contacts'

const notFound = () => NextResponse.json({ success: false, error: 'Contact not found' }, { status: 404 })

// PATCH - update contact status
export async function PATCH(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const denied = await requireAdmin()
  if (denied) return denied
  try {
    const _id = parseId((await params).id)
    if (!_id) return notFound()
    const { status } = await req.json()
    if (!CONTACT_STATUSES.includes(status as ContactStatus)) {
      return NextResponse.json({ success: false, error: 'Invalid status' }, { status: 400 })
    }
    const res = await contactMessages().updateOne({ _id }, { $set: { status, updated_at: new Date() } })
    return res.matchedCount ? NextResponse.json({ success: true }) : notFound()
  } catch (error) {
    console.error('PATCH /api/admin/contacts/[id] error:', error instanceof Error ? error.name : error)
    return NextResponse.json({ success: false, error: 'Failed to update contact status' }, { status: 500 })
  }
}

// DELETE - delete a contact
export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const denied = await requireAdmin()
  if (denied) return denied
  try {
    const _id = parseId((await params).id)
    if (!_id) return notFound()
    const res = await contactMessages().deleteOne({ _id })
    return res.deletedCount ? NextResponse.json({ success: true }) : notFound()
  } catch (error) {
    console.error('DELETE /api/admin/contacts/[id] error:', error instanceof Error ? error.name : error)
    return NextResponse.json({ success: false, error: 'Failed to delete contact' }, { status: 500 })
  }
}
