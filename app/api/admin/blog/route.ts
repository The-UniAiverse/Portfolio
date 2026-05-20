import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

async function ensureTable() {
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS blog_posts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      slug VARCHAR(255) NOT NULL UNIQUE,
      excerpt TEXT,
      content LONGTEXT,
      category VARCHAR(100) DEFAULT 'General',
      tags JSON,
      status ENUM('draft', 'published') DEFAULT 'draft',
      read_time VARCHAR(50) DEFAULT '5 min read',
      date DATE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `)
}

// GET - fetch all blog posts
export async function GET(req: NextRequest) {
  try {
    await ensureTable()
    const { searchParams } = new URL(req.url)
    const status = searchParams.get('status')
    const category = searchParams.get('category')
    const search = searchParams.get('search')

    let query = 'SELECT * FROM blog_posts WHERE 1=1'
    const params: (string | number)[] = []

    if (status && status !== 'all') {
      query += ' AND status = ?'
      params.push(status)
    }
    if (category && category !== 'All') {
      query += ' AND category = ?'
      params.push(category)
    }
    if (search) {
      query += ' AND (title LIKE ? OR excerpt LIKE ?)'
      params.push(`%${search}%`, `%${search}%`)
    }

    query += ' ORDER BY created_at DESC'

    const [rows] = await pool.execute(query, params)
    return NextResponse.json({ success: true, data: rows })
  } catch (error) {
    console.error('GET /api/admin/blog error:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch blog posts' }, { status: 500 })
  }
}

// POST - create a new blog post
export async function POST(req: NextRequest) {
  try {
    await ensureTable()
    const body = await req.json()
    const { title, slug, excerpt, content, category, tags, status, read_time, date } = body

    if (!title) {
      return NextResponse.json({ success: false, error: 'Title is required' }, { status: 400 })
    }

    const finalSlug = slug || title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
    const tagsJson = JSON.stringify(Array.isArray(tags) ? tags : (tags ? tags.split(',').map((t: string) => t.trim()).filter(Boolean) : []))

    const [result] = await pool.execute(
      'INSERT INTO blog_posts (title, slug, excerpt, content, category, tags, status, read_time, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [title, finalSlug, excerpt || '', content || '', category || 'General', tagsJson, status || 'draft', read_time || '5 min read', date || new Date().toISOString().split('T')[0]]
    )

    const insertResult = result as { insertId: number }
    const [rows] = await pool.execute('SELECT * FROM blog_posts WHERE id = ?', [insertResult.insertId])
    const posts = rows as unknown[]
    return NextResponse.json({ success: true, data: posts[0] }, { status: 201 })
  } catch (error) {
    console.error('POST /api/admin/blog error:', error)
    return NextResponse.json({ success: false, error: 'Failed to create blog post' }, { status: 500 })
  }
}
