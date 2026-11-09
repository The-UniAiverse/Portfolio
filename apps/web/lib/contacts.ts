// Contact-form messages, stored in MongoDB (collection `contact_messages`).
// Written by the public /api/contact route; read and updated by the admin panel (/api/admin/contacts).
import { ObjectId, type WithId } from 'mongodb'
import { mongoDb } from './mongo'

export const CONTACT_STATUSES = ['new', 'in-progress', 'resolved'] as const
export type ContactStatus = (typeof CONTACT_STATUSES)[number]

export interface ContactMessage {
  name: string
  email: string
  phone: string
  company: string
  service: string
  message: string
  status: ContactStatus
  created_at: Date
  updated_at: Date
  ip_hash: string // salted hash of the sender's IP, only for rate limiting
}

export const contactMessages = () => mongoDb().collection<ContactMessage>('contact_messages')

/** The shape the admin panel expects (string id, ISO dates, no IP hash). */
export function toInquiry({ _id, ip_hash: _ip, ...m }: WithId<ContactMessage>) {
  void _ip
  return { ...m, id: _id.toHexString(), created_at: m.created_at.toISOString(), updated_at: m.updated_at.toISOString() }
}

export function parseId(id: string): ObjectId | null {
  return ObjectId.isValid(id) && /^[0-9a-f]{24}$/i.test(id) ? new ObjectId(id) : null
}
