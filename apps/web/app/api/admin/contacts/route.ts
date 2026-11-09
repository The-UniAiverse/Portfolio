import { NextRequest, NextResponse } from 'next/server'
import type { Filter } from 'mongodb'
import { requireAdmin } from '@/lib/admin'
import { CONTACT_STATUSES, contactMessages, toInquiry, type ContactMessage, type ContactStatus } from '@/lib/contacts'

// Contact-form messages for the admin panel (stored in MongoDB by the public /api/contact route).

const escapeRegex = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

// GET - list messages, newest first; optional ?status= and ?search=
export async function GET(req: NextRequest) {
  const denied = await requireAdmin()
  if (denied) return denied
  try {
    const { searchParams } = new URL(req.url)
    const status = searchParams.get('status')
    const search = searchParams.get('search')?.trim()

    const filter: Filter<ContactMessage> = {}
    if (status && status !== 'all' && CONTACT_STATUSES.includes(status as ContactStatus)) {
      filter.status = status as ContactStatus
    }
    if (search) {
      const rx = { $regex: escapeRegex(search.slice(0, 100)), $options: 'i' }
      filter.$or = [{ name: rx }, { email: rx }, { company: rx }, { service: rx }]
    }

    const rows = await contactMessages().find(filter).sort({ created_at: -1 }).limit(1000).toArray()
    return NextResponse.json({ success: true, data: rows.map(toInquiry) })
  } catch (error) {
    console.error('GET /api/admin/contacts error:', error instanceof Error ? error.name : error)
    return NextResponse.json({ success: false, error: 'Failed to fetch contacts' }, { status: 500 })
  }
}
