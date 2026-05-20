import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'
import { serviceCategories } from '@/data/services.data'

async function ensureTableAndSeed() {
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS services (
      id INT AUTO_INCREMENT PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      description TEXT NOT NULL,
      icon VARCHAR(20) DEFAULT '🔧',
      category VARCHAR(100) NOT NULL,
      category_icon VARCHAR(20) DEFAULT '🚀',
      whats_included JSON,
      use_cases JSON,
      deliverables TEXT,
      capabilities JSON,
      examples JSON,
      ideal_for TEXT,
      powered_by TEXT,
      tools TEXT,
      duration VARCHAR(100),
      is_active TINYINT(1) DEFAULT 1,
      sort_order INT DEFAULT 0,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `)

  // Auto-seed from static data if the table is empty
  const [countRows] = await pool.execute('SELECT COUNT(*) as total FROM services')
  const total = (countRows as { total: number }[])[0]?.total ?? 0

  if (total === 0) {
    let sortOrder = 0
    for (const category of serviceCategories) {
      for (const svc of category.services) {
        await pool.execute(
          `INSERT INTO services
            (title, description, icon, category, category_icon, whats_included, use_cases, deliverables, capabilities, examples, ideal_for, powered_by, tools, duration, is_active, sort_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            svc.title,
            svc.description,
            svc.icon || '🔧',
            category.categoryTitle,
            category.categoryIcon,
            JSON.stringify(Array.isArray(svc.whatsIncluded) ? svc.whatsIncluded : []),
            JSON.stringify(Array.isArray(svc.useCases) ? svc.useCases : []),
            Array.isArray(svc.deliverables) ? svc.deliverables.join(', ') : (svc.deliverables || ''),
            JSON.stringify(Array.isArray(svc.capabilities) ? svc.capabilities : []),
            JSON.stringify(Array.isArray(svc.examples) ? svc.examples : []),
            svc.idealFor || '',
            svc.poweredBy || '',
            svc.tools || '',
            svc.duration || '',
            1,
            sortOrder++,
          ]
        )
      }
    }
  }
}

// GET - fetch all services
export async function GET(req: NextRequest) {
  try {
    await ensureTableAndSeed()

    const { searchParams } = new URL(req.url)
    const category = searchParams.get('category')
    const search = searchParams.get('search')
    const status = searchParams.get('status')

    let query = 'SELECT * FROM services WHERE 1=1'
    const params: (string | number)[] = []

    if (category && category !== 'All') {
      query += ' AND category = ?'
      params.push(category)
    }
    if (search) {
      query += ' AND (title LIKE ? OR description LIKE ?)'
      params.push(`%${search}%`, `%${search}%`)
    }
    if (status === 'active') {
      query += ' AND is_active = 1'
    } else if (status === 'inactive') {
      query += ' AND is_active = 0'
    }

    query += ' ORDER BY sort_order ASC, category ASC, id ASC'

    const [rows] = await pool.execute(query, params)
    return NextResponse.json({ success: true, data: rows })
  } catch (error) {
    console.error('GET /api/admin/services error:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch services' }, { status: 500 })
  }
}

// POST - create a new service
export async function POST(req: NextRequest) {
  try {
    await ensureTableAndSeed()

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

    const [result] = await pool.execute(
      `INSERT INTO services 
        (title, description, icon, category, category_icon, whats_included, use_cases, deliverables, capabilities, examples, ideal_for, powered_by, tools, duration, is_active, sort_order)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
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
        is_active !== undefined ? (is_active ? 1 : 0) : 1,
        sort_order || 0,
      ]
    )

    const insertResult = result as { insertId: number }
    const [rows] = await pool.execute('SELECT * FROM services WHERE id = ?', [insertResult.insertId])
    const services = rows as unknown[]
    return NextResponse.json({ success: true, data: services[0] }, { status: 201 })
  } catch (error) {
    console.error('POST /api/admin/services error:', error)
    return NextResponse.json({ success: false, error: 'Failed to create service' }, { status: 500 })
  }
}
