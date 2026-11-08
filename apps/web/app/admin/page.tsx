import { redirect } from 'next/navigation'

export default function AdminRoot() {
  // The dashboard's AuthGuard sends signed-out or non-admin users to the right place.
  redirect('/admin/dashboard')
}
