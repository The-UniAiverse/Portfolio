import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'
import { contactInfo } from '@/data/contact.data'

async function ensureTableAndSeed() {
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS contact_info (
      id INT AUTO_INCREMENT PRIMARY KEY,
      icon VARCHAR(20) DEFAULT '📍',
      title VARCHAR(100) NOT NULL,
      details JSON NOT NULL,
      link VARCHAR(500),
      sort_order INT DEFAULT 0,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `)

  const [countRows] = await pool.execute('SELECT COUNT(*) as total FROM contact_info')
  const total = (countRows as { total: number }[])[0]?.total ?? 0

  if (total === 0) {
    for (let i = 0; i < contactInfo.length; i++) {
      const info = contactInfo[i]
      await pool.execute(
        'INSERT INTO contact_info (icon, title, details, link, sort_order) VALUES (?, ?, ?, ?, ?)',
        [info.icon, info.title, JSON.stringify(info.details), info.link || null, i]
      )
    }
  }
}

// GET all contact info
export async function GET() {
  try {
    await ensureTableAndSeed()
    const [rows] = await pool.execute('SELECT * FROM contact_info ORDER BY sort_order ASC, id ASC')
    return NextResponse.json({ success: true, data: rows })
  } catch (error) {
    console.error('GET /api/admin/contact-info error:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch contact info' }, { status: 500 })
  }
}

// POST - add a new contact info entry
export async function POST(req: NextRequest) {
  try {
    await ensureTableAndSeed()
    const body = await req.json()
    const { icon, title, details, link, sort_order } = body

    if (!title) {
      return NextResponse.json({ success: false, error: 'Title is required' }, { status: 400 })
    }

    const detailsArr = Array.isArray(details)
      ? details
      : String(details).split('\n').map((s: string) => s.trim()).filter(Boolean)

    const [result] = await pool.execute(
      'INSERT INTO contact_info (icon, title, details, link, sort_order) VALUES (?, ?, ?, ?, ?)',
      [icon || '📍', title, JSON.stringify(detailsArr), link || null, sort_order || 0]
    )

    const insertResult = result as { insertId: number }
    const [rows] = await pool.execute('SELECT * FROM contact_info WHERE id = ?', [insertResult.insertId])
    const items = rows as unknown[]
    return NextResponse.json({ success: true, data: items[0] }, { status: 201 })
  } catch (error) {
    console.error('POST /api/admin/contact-info error:', error)
    return NextResponse.json({ success: false, error: 'Failed to create contact info' }, { status: 500 })
  }
}
