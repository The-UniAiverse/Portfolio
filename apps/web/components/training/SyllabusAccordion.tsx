'use client'

import { useState } from 'react'
import type { SyllabusModule } from '@/data/training.data'

export default function SyllabusAccordion({ modules }: { modules: SyllabusModule[] }) {
  const [open, setOpen] = useState<Set<number>>(() => new Set([0]))
  const allOpen = open.size === modules.length
  const toggle = (i: number) =>
    setOpen((prev) => {
      const next = new Set(prev)
      if (next.has(i)) next.delete(i)
      else next.add(i)
      return next
    })

  return (
    <div>
      <div className="flex justify-end mb-4">
        <button type="button" onClick={() => setOpen(allOpen ? new Set() : new Set(modules.map((_, i) => i)))}
          className="text-sm font-semibold text-primary hover:text-primary-light">
          {allOpen ? 'Collapse all' : 'Expand all'}
        </button>
      </div>
      <ol className="space-y-3">
        {modules.map((m, i) => {
          const isOpen = open.has(i)
          return (
            <li key={m.title} className={`rounded-2xl border bg-secondary transition-all duration-300 ${isOpen ? 'border-primary-light shadow-md' : 'border-primary/10 hover:border-primary-light/60'}`}>
              <button type="button" onClick={() => toggle(i)} aria-expanded={isOpen} className="w-full flex items-center gap-4 p-5 text-left">
                <span className={`w-11 h-11 shrink-0 rounded-xl flex items-center justify-center font-bold text-sm transition-colors ${isOpen ? 'bg-primary text-secondary' : 'bg-primary/10 text-primary'}`}>
                  {String(i + 1).padStart(2, '0')}
                </span>
                <span className="flex-1">
                  <span className="block font-semibold text-primary-dark">{m.title}</span>
                  {!isOpen && <span className="block text-sm text-primary-dark/50 mt-0.5">{m.topics.length} topics · hands-on lab</span>}
                </span>
                <span className={`text-primary text-xl transition-transform duration-300 ${isOpen ? 'rotate-45' : ''}`} aria-hidden="true">+</span>
              </button>
              {isOpen && (
                <div className="px-5 pb-5 sm:pl-20 space-y-4">
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
                    {m.topics.map((t) => (
                      <li key={t} className="flex items-start text-sm text-primary-dark/75"><span className="text-primary-light mr-2">•</span>{t}</li>
                    ))}
                  </ul>
                  <p className="text-sm bg-primary/5 border border-primary/10 rounded-xl px-4 py-3 text-primary-dark/80">
                    <span className="font-bold text-primary">🛠️ Hands-on lab: </span>{m.lab}
                  </p>
                </div>
              )}
            </li>
          )
        })}
      </ol>
    </div>
  )
}
