'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { pillars } from '@/data/pillars.data'

const CYCLE_MS = 4500

/** Hero panel: the four core pillars as a deck-style console that cycles until the visitor takes over. */
export default function PillarConsole() {
  const [active, setActive] = useState(0)
  const [paused, setPaused] = useState(false)

  useEffect(() => {
    if (paused || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const id = window.setTimeout(() => setActive((a) => (a + 1) % pillars.length), CYCLE_MS)
    return () => window.clearTimeout(id)
  }, [active, paused])

  const p = pillars[active]

  return (
    <div
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
      className="relative w-full max-w-xl mx-auto lg:ml-auto rounded-3xl border border-white/10 bg-[#0b1020]/80 backdrop-blur-md shadow-2xl shadow-cyan-500/5 overflow-hidden"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_90%_0%,rgba(34,211,238,0.14),transparent_45%),radial-gradient(circle_at_0%_100%,rgba(251,191,36,0.10),transparent_50%)]" aria-hidden="true" />

      {/* title bar */}
      <div className="relative flex items-center justify-between px-6 pt-5 pb-4 border-b border-white/10 font-mono text-xs text-white/45">
        <span className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-300 animate-pulse" aria-hidden="true" />
          uniaiverse / core-pillars
        </span>
        <span>{p.number} / 0{pillars.length}</span>
      </div>

      {/* pillar list */}
      <ul className="relative p-3" role="tablist" aria-label="Our four core pillars">
        {pillars.map((x, i) => {
          const on = i === active
          return (
            <li key={x.id}>
              <button
                type="button" role="tab" aria-selected={on} onClick={() => setActive(i)}
                className={`w-full text-left rounded-2xl px-4 py-3 flex items-center gap-4 transition-all duration-300 ${on ? 'bg-white/[0.07]' : 'hover:bg-white/[0.04]'}`}
              >
                <span className={`font-mono text-sm ${on ? 'text-amber-300' : 'text-white/35'}`}>{x.number}</span>
                <span className={`flex-1 font-semibold ${on ? 'text-white' : 'text-white/60'}`}>{x.title}</span>
                <span className={`text-xl transition-transform duration-300 ${on ? 'scale-110' : 'opacity-50 grayscale'}`} aria-hidden="true">{x.icon}</span>
              </button>
              {/* progress line for the active pillar */}
              <div className="mx-4 h-px bg-white/5 overflow-hidden" aria-hidden="true">
                {on && <div key={`${active}-${paused}`} className={`h-px bg-gradient-to-r from-cyan-300 to-amber-300 ${paused ? 'w-full' : 'animate-pillar-progress'}`} />}
              </div>
            </li>
          )
        })}
      </ul>

      {/* detail */}
      <div key={p.id} role="tabpanel" className="relative px-7 pb-7 pt-3 animate-slide-in">
        <p className="kicker mb-3">{p.verbs.join(' · ')}</p>
        <p className="text-white/80 leading-relaxed mb-5 min-h-[4.5rem]">{p.scope}</p>
        <Link href={p.href} className="inline-flex items-center gap-2 font-semibold text-cyan-200 hover:text-amber-200 transition-colors">
          {p.cta} <span aria-hidden="true">→</span>
        </Link>
      </div>
    </div>
  )
}
