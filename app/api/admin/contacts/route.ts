import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

async function ensureTable() {
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS contacts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      company VARCHAR(255) DEFAULT '',
      service VARCHAR(255) DEFAULT '',
      message TEXT,
      status ENUM('new', 'in-progress', 'resolved') DEFAULT 'new',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `)
}

// GET - fetch all contacts
export async function GET(req: NextRequest) {
  try {
    await ensureTable()
    const { searchParams } = new URL(req.url)
    const status = searchParams.get('status')
    const search = searchParams.get('search')

    let query = 'SELECT * FROM contacts WHERE 1=1'
    const params: (string | number)[] = []

    if (status && status !== 'all') {
      query += ' AND status = ?'
      params.push(status)
    }
    if (search) {
      query += ' AND (name LIKE ? OR email LIKE ? OR company LIKE ? OR service LIKE ?)'
      params.push(`%${search}%`, `%${search}%`, `%${search}%`, `%${search}%`)
    }

    query += ' ORDER BY created_at DESC'

    const [rows] = await pool.execute(query, params)
    return NextResponse.json({ success: true, data: rows })
  } catch (error) {
    console.error('GET /api/admin/contacts error:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch contacts' }, { status: 500 })
  }
}

// POST - create a contact (from website contact form)
export async function POST(req: NextRequest) {
  try {
    await ensureTable()
    const body = await req.json()
    const { name, email, company, service, message } = body

    if (!name || !email) {
      return NextResponse.json({ success: false, error: 'Name and email are required' }, { status: 400 })
    }

    const [result] = await pool.execute(
      'INSERT INTO contacts (name, email, company, service, message, status) VALUES (?, ?, ?, ?, ?, ?)',
      [name, email, company || '', service || '', message || '', 'new']
    )

    const insertResult = result as { insertId: number }
    return NextResponse.json({ success: true, data: { id: insertResult.insertId } }, { status: 201 })
  } catch (error) {
    console.error('POST /api/admin/contacts error:', error)
    return NextResponse.json({ success: false, error: 'Failed to submit contact' }, { status: 500 })
  }
}
