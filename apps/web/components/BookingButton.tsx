'use client'

import { useEffect, useState } from 'react'
import { contactPageData } from '@/data/contact.data'

// Google Calendar appointment schedules can be shown in a frame when the link is the
// ".../calendar/appointments/schedules/..." form (Calendar → schedule → Share → Website embed).
// Short "calendar.app.google" links open in a new tab instead.
function embedUrl(url: string): string | null {
  try {
    const u = new URL(url)
    if (u.hostname !== 'calendar.google.com' || !u.pathname.includes('/appointments/schedules/')) return null
    u.searchParams.set('gv', 'true')
    return u.toString()
  } catch {
    return null
  }
}

/** Floating "Book a call" button that opens the Google Calendar booking page. Hidden until a link is set. */
export default function BookingButton() {
  const url = contactPageData.bookingUrl
  const frame = url ? embedUrl(url) : null
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  if (!url) return null

  const buttonClass =
    'fixed bottom-5 left-5 z-50 flex items-center gap-2 bg-primary hover:bg-primary-light text-secondary px-5 py-3 rounded-full font-semibold shadow-lg hover:shadow-primary-light/50 transition-all duration-300'
  const icon = (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  )

  if (!frame) {
    return (
      <a href={url} target="_blank" rel="noopener noreferrer" className={buttonClass}>
        {icon}
        Book a call
      </a>
    )
  }

  return (
    <>
      <button type="button" onClick={() => setOpen(true)} className={buttonClass}>
        {icon}
        Book a call
      </button>
      {open && (
        <div className="fixed inset-0 z-[70] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setOpen(false)}>
          <div role="dialog" aria-modal="true" aria-label="Book a call"
            className="bg-secondary rounded-2xl shadow-2xl w-full max-w-4xl h-[85vh] flex flex-col overflow-hidden"
            onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between px-6 py-4 border-b border-primary/10">
              <h2 className="text-lg font-bold text-primary-dark">Book a call with uniAiverse</h2>
              <div className="flex items-center gap-4">
                <a href={url} target="_blank" rel="noopener noreferrer" className="text-sm text-primary hover:text-primary-light font-semibold">
                  Open in new tab ↗
                </a>
                <button type="button" onClick={() => setOpen(false)} aria-label="Close" className="text-2xl text-primary-dark/50 hover:text-primary-dark">×</button>
              </div>
            </div>
            <iframe src={frame} title="Book a call" className="flex-1 w-full border-0" />
          </div>
        </div>
      )}
    </>
  )
}
