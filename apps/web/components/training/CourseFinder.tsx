'use client'

import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import Link from 'next/link'
import { courseHref, finderQuestions, levels, recommend } from '@/data/training.data'

/** "Still confused?" button plus the two-question course finder it opens. */
export default function CourseFinder({ label = 'Still confused? Try our course finder', variant = 'solid' }: {
  label?: string
  variant?: 'solid' | 'outline' | 'light'
}) {
  const [open, setOpen] = useState(false)
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false)
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('keydown', onKey)
    }
  }, [open])

  const start = () => {
    setAnswers({})
    setStep(0)
    setOpen(true)
  }
  // Course links are plain <a>: a native fragment jump updates :target, which highlights the row.
  const done = step >= finderQuestions.length
  const q = finderQuestions[Math.min(step, finderQuestions.length - 1)]
  const result = done ? recommend(answers) : null

  const buttonClass = {
    solid: 'bg-primary hover:bg-primary-light text-secondary hover:shadow-lg hover:shadow-primary-light/50',
    outline: 'border-2 border-secondary text-secondary hover:bg-white/10 hover:border-white/60',
    light: 'bg-amber-300 text-slate-900 hover:bg-amber-200 hover:shadow-2xl hover:shadow-amber-300/20',
  }[variant]

  return (
    <>
      <button type="button" onClick={start} className={`px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 hover:scale-105 ${buttonClass}`}>
        🧭 {label}
      </button>

      {/* Portalled to <body> so no parent stacking context (e.g. the hero) can put the header above it. */}
      {open && createPortal(
        <div className="fixed inset-0 z-[70] bg-primary-dark/70 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setOpen(false)}>
          <div role="dialog" aria-modal="true" aria-label="Course finder" onClick={(e) => e.stopPropagation()}
            className="bg-secondary w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl shadow-2xl text-left">
            {/* header */}
            <div className="bg-gradient-blue px-8 pt-7 pb-6 text-secondary">
              <div className="flex items-center justify-between mb-4">
                <span className="font-bold">🧭 Course finder</span>
                <button type="button" onClick={() => setOpen(false)} aria-label="Close" className="text-2xl text-secondary/70 hover:text-secondary">×</button>
              </div>
              <div className="flex gap-2" aria-hidden="true">
                {finderQuestions.map((x, i) => (
                  <span key={x.id} className={`h-1.5 flex-1 rounded-full transition-all duration-500 ${i < step || done ? 'bg-secondary' : i === step ? 'bg-white/60' : 'bg-white/20'}`} />
                ))}
              </div>
              <p className="text-secondary/70 text-sm mt-3">{done ? 'Your recommendation' : `Question ${step + 1} of ${finderQuestions.length}`}</p>
            </div>

            <div className="p-8">
              {!done && (
                <>
                  <h2 className="text-2xl md:text-3xl font-bold text-primary-dark mb-6">{q.question}</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {q.options.map((o) => (
                      <button key={o.id} type="button"
                        onClick={() => { setAnswers({ ...answers, [q.id]: o.id }); setStep(step + 1) }}
                        className={`flex items-center gap-3 text-left p-4 rounded-2xl border-2 transition-all duration-200 hover:-translate-y-0.5 ${
                          answers[q.id] === o.id ? 'border-primary bg-primary/5' : 'border-primary/10 hover:border-primary-light hover:bg-primary/5'
                        }`}>
                        <span className="text-2xl" aria-hidden="true">{o.icon}</span>
                        <span className="font-semibold text-primary-dark">{o.label}</span>
                      </button>
                    ))}
                  </div>
                  {step > 0 && (
                    <button type="button" onClick={() => setStep(step - 1)} className="mt-6 text-primary font-semibold hover:text-primary-light">← Back</button>
                  )}
                </>
              )}

              {result && (
                <div>
                  <p className="text-primary-dark/60 mb-3">We recommend</p>
                  <div className="bg-gradient-blue rounded-2xl p-6 text-secondary shadow-xl mb-6">
                    <div className="flex items-center gap-4 mb-3">
                      <span className="text-5xl" aria-hidden="true">{result.best.track.icon}</span>
                      <div>
                        <h2 className="text-2xl md:text-3xl font-bold">{result.best.title}</h2>
                        <p className="text-secondary/75 text-sm">
                          {result.best.track.label} · {levels[result.best.level].short} {levels[result.best.level].label} · {result.best.duration}
                        </p>
                      </div>
                    </div>
                    <p className="text-secondary/90 leading-relaxed">Because {result.reason}.</p>
                    <div className="flex flex-col sm:flex-row gap-3 mt-6">
                      <a href={courseHref(result.best.id)} onClick={() => setOpen(false)}
                        className="text-center bg-amber-300 text-slate-900 px-6 py-3 rounded-full font-bold hover:bg-amber-200 transition-all duration-300">
                        See it in the catalogue →
                      </a>
                      <Link href="#contact" onClick={() => setOpen(false)}
                        className="text-center border-2 border-secondary text-secondary px-6 py-3 rounded-full font-bold hover:bg-white/10 hover:border-white/60 transition-all duration-300">
                        Talk to us
                      </Link>
                    </div>
                  </div>

                  <p className="text-primary-dark/60 mb-3">Also worth a look</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {result.alternatives.map((p) => (
                      <a key={p.id} href={courseHref(p.id)} onClick={() => setOpen(false)}
                        className="flex items-center gap-3 p-4 rounded-2xl border-2 border-primary/10 hover:border-primary-light transition-all duration-200">
                        <span className="text-2xl" aria-hidden="true">{p.track.icon}</span>
                        <span>
                          <span className="block font-semibold text-primary-dark">{p.title}</span>
                          <span className="block text-sm text-primary-dark/60">{p.track.label} · {levels[p.level].short} · {p.duration}</span>
                        </span>
                      </a>
                    ))}
                  </div>
                  <button type="button" onClick={() => { setAnswers({}); setStep(0) }} className="mt-6 text-primary font-semibold hover:text-primary-light">
                    ↺ Start over
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>,
        document.body,
      )}
    </>
  )
}
