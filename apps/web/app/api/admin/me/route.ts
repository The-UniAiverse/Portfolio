import { NextResponse } from 'next/server'
import { getAdmin, requireAdmin } from '@/lib/admin'

// Lets the admin UI know whether the current session is an admin.
export async function GET() {
  const denied = await requireAdmin()
  if (denied) return denied
  const admin = await getAdmin()
  return NextResponse.json({ email: admin!.email, name: admin!.name })
}
