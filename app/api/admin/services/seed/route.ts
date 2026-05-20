import { NextResponse } from 'next/server'
import pool from '@/lib/db'
import { serviceCategories } from '@/data/services.data'

export async function POST() {
  try {
    // Ensure table exists
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

    let inserted = 0
    let skipped = 0
    let sortOrder = 0

    for (const category of serviceCategories) {
      for (const svc of category.services) {
        // Skip if a service with same title already exists
        const [existing] = await pool.execute('SELECT id FROM services WHERE title = ?', [svc.title])
        const rows = existing as unknown[]
        if (rows.length > 0) {
          skipped++
          continue
        }

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
        inserted++
      }
    }

    return NextResponse.json({
      success: true,
      message: `Seeded ${inserted} services (${skipped} already existed).`,
      inserted,
      skipped,
    })
  } catch (error) {
    console.error('POST /api/admin/services/seed error:', error)
    return NextResponse.json({ success: false, error: 'Failed to seed services' }, { status: 500 })
  }
}
