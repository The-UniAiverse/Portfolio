import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

async function ensureTable() {
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS testimonials (
      id INT AUTO_INCREMENT PRIMARY KEY,
      quote TEXT NOT NULL,
      author VARCHAR(255) NOT NULL,
      role VARCHAR(255) DEFAULT '',
      company VARCHAR(255) DEFAULT '',
      avatar VARCHAR(20) DEFAULT '👤',
      rating INT DEFAULT 5,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `)
}

// GET - fetch all testimonials
export async function GET() {
  try {
    await ensureTable()
    const [rows] = await pool.execute('SELECT * FROM testimonials ORDER BY created_at DESC')
    return NextResponse.json({ success: true, data: rows })
  } catch (error) {
    console.error('GET /api/admin/testimonials error:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch testimonials' }, { status: 500 })
  }
}

// POST - create a testimonial
export async function POST(req: NextRequest) {
  try {
    await ensureTable()
    const body = await req.json()
    const { quote, author, role, company, avatar, rating } = body

    if (!quote || !author) {
      return NextResponse.json({ success: false, error: 'Quote and author are required' }, { status: 400 })
    }

    const [result] = await pool.execute(
      'INSERT INTO testimonials (quote, author, role, company, avatar, rating) VALUES (?, ?, ?, ?, ?, ?)',
      [quote, author, role || '', company || '', avatar || '👤', rating || 5]
    )

    const insertResult = result as { insertId: number }
    const [rows] = await pool.execute('SELECT * FROM testimonials WHERE id = ?', [insertResult.insertId])
    const items = rows as unknown[]
    return NextResponse.json({ success: true, data: items[0] }, { status: 201 })
  } catch (error) {
    console.error('POST /api/admin/testimonials error:', error)
    return NextResponse.json({ success: false, error: 'Failed to create testimonial' }, { status: 500 })
  }
}
