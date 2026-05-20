import { NextResponse } from 'next/server'
import pool from '@/lib/db'
import { contactInfo } from '@/data/contact.data'

// Public GET - used by the website Contact component
export async function GET() {
  try {
    const [rows] = await pool.execute('SELECT * FROM contact_info ORDER BY sort_order ASC, id ASC')
    const items = rows as unknown[]
    if (!items.length) throw new Error('empty')
    return NextResponse.json({ success: true, data: items })
  } catch {
    // Fallback to static data
    return NextResponse.json({ success: true, data: contactInfo })
  }
}
