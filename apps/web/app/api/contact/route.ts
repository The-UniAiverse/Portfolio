import { createHash } from 'crypto'
import { NextRequest, NextResponse } from 'next/server'
import { contactMessages } from '@/lib/contacts'

// Public endpoint for the website contact form. Saves to MongoDB; admins read it at /admin/contacts.

const LIMITS = { name: 100, email: 120, phone: 40, company: 120, service: 120, message: 5000 } as const
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/
const RATE_WINDOW_MS = 10 * 60 * 1000
const RATE_MAX = 5

const bad = (error: string, status = 400) => NextResponse.json({ success: false, error }, { status })

function clientIpHash(req: NextRequest): string {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0].trim() || req.headers.get('x-real-ip') || 'unknown'
  return createHash('sha256').update(`${process.env.BETTER_AUTH_SECRET ?? ''}:${ip}`).digest('hex')
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null)
  if (!body || typeof body !== 'object') return bad('Invalid request')

  // Honeypot: real visitors never see or fill the "website" field; bots usually do. Pretend success.
  if (typeof body.website === 'string' && body.website.trim()) {
    return NextResponse.json({ success: true }, { status: 201 })
  }

  const fields = {} as Record<keyof typeof LIMITS, string>
  for (const [key, max] of Object.entries(LIMITS) as [keyof typeof LIMITS, number][]) {
    const value = typeof body[key] === 'string' ? body[key].trim() : ''
    if (value.length > max) return bad(`${key} is too long (max ${max} characters)`)
    fields[key] = value
  }
  if (!fields.name) return bad('Please enter your name')
  if (!EMAIL.test(fields.email)) return bad('Please enter a valid email address')
  if (!fields.message) return bad('Please enter a message')

  try {
    const messages = contactMessages()
    const ip_hash = clientIpHash(req)
    const recent = await messages.countDocuments({ ip_hash, created_at: { $gt: new Date(Date.now() - RATE_WINDOW_MS) } })
    if (recent >= RATE_MAX) return bad('Too many messages. Please try again in a few minutes.', 429)

    const now = new Date()
    await messages.insertOne({ ...fields, status: 'new', created_at: now, updated_at: now, ip_hash })
    return NextResponse.json({ success: true }, { status: 201 })
  } catch (error) {
    console.error('POST /api/contact failed:', error instanceof Error ? error.name : error)
    return bad('We could not send your message right now. Please try again or email us directly.', 500)
  }
}
