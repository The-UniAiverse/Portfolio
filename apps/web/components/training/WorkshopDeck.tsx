'use client'

import { useRef, useState, type KeyboardEvent, type ReactNode } from 'react'
import Link from 'next/link'
import { workshop, type WorkshopSlide } from '@/data/training.data'

const usd = (n: number) => `$${n.toLocaleString('en-US')}`
const pad = (n: number) => String(n).padStart(2, '0')

function Kicker({ children }: { children: ReactNode }) {
  return <p className="font-mono text-xs md:text-sm uppercase tracking-[0.2em] text-amber-300/90 mb-4">{children}</p>
}

function Slide({ s }: { s: WorkshopSlide }) {
  switch (s.kind) {
    case 'cover':
      return (
        <div className="flex flex-col justify-center h-full">
          <Kicker>{s.kicker}</Kicker>
          <h3 className="text-4xl md:text-6xl font-bold leading-[1.05] bg-gradient-to-r from-white via-cyan-200 to-amber-200 bg-clip-text text-transparent mb-4">{s.title}</h3>
          <p className="text-white/60 font-medium mb-6">{s.meta}</p>
          <p className="text-lg md:text-xl text-white/85 leading-relaxed max-w-3xl mb-8">{s.lead}</p>
          <div className="flex flex-wrap gap-2">
            {s.chips.map((c) => <span key={c} className="border border-white/20 bg-white/5 text-white/85 text-sm px-3 py-1.5 rounded-full">{c}</span>)}
          </div>
        </div>
      )
    case 'analogy':
      return (
        <div className="grid grid-cols-1 lg:grid-cols-[1.3fr_1fr] gap-8 lg:gap-12 items-center h-full">
          <div>
            <Kicker>{s.kicker}</Kicker>
            <h3 className="text-3xl md:text-5xl font-bold text-white mb-6">{s.title}</h3>
            <ol className="space-y-4">
              {s.story.map((line, i) => (
                <li key={line} className="flex gap-4 text-white/85 md:text-lg leading-relaxed">
                  <span className="font-mono text-amber-300/80 pt-0.5">{pad(i + 1)}</span>{line}
                </li>
              ))}
            </ol>
          </div>
          <div className="rounded-2xl border border-white/15 bg-white/[0.04] p-6">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-white/50 mb-4">The mapping</p>
            <dl className="divide-y divide-white/10">
              {s.mapping.map((m) => (
                <div key={m.thing} className="flex items-center justify-between gap-4 py-3">
                  <dt className="text-white/70">{m.thing}</dt>
                  <dd className="font-bold text-cyan-200 text-right"><span className="text-white/40 font-normal mr-2" aria-hidden="true">→</span>{m.is}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      )
    case 'lab':
      return (
        <div className="flex flex-col justify-center h-full">
          <div className="flex items-start justify-between gap-6">
            <div>
              <Kicker>{s.kicker}</Kicker>
              <h3 className="text-3xl md:text-5xl font-bold text-white mb-8">{s.title}</h3>
            </div>
            <span className="hidden sm:block font-mono text-4xl md:text-6xl font-bold text-amber-300/90 shrink-0">{s.badge}</span>
          </div>
          <ol className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
            {s.steps.map((step, i) => (
              <li key={step} className="rounded-2xl bg-white/[0.06] border border-white/10 p-5">
                <span className="block font-mono text-sm text-cyan-300 mb-2">Step {i + 1}</span>
                <span className="text-white/90 font-semibold leading-snug">{step}</span>
              </li>
            ))}
          </ol>
          <div className="border-l-4 border-amber-300/80 pl-5 space-y-1">
            {s.note.map((n) => <p key={n} className="text-white/75 md:text-lg leading-relaxed">{n}</p>)}
          </div>
        </div>
      )
    case 'concept':
      return (
        <div className="flex flex-col justify-center h-full">
          <Kicker>{s.kicker}</Kicker>
          <h3 className="text-3xl md:text-5xl font-bold text-white mb-8">{s.title}</h3>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-3 mb-8">
            {s.points.map((p, i) => (
              <li key={p} className={`flex gap-3 md:text-lg ${i === s.points.length - 1 ? 'text-amber-200 font-semibold' : 'text-white/85'}`}>
                <span className="text-cyan-300" aria-hidden="true">→</span>{p}
              </li>
            ))}
          </ul>
          <blockquote className="text-xl md:text-2xl font-semibold text-white leading-snug max-w-4xl">“{s.quote}”</blockquote>
        </div>
      )
    case 'tokens': {
      const share = Math.max((s.example.fetched / s.example.pasted) * 100, 1.5)
      return (
        <div className="flex flex-col justify-center h-full">
          <Kicker>{s.kicker}</Kicker>
          <h3 className="text-3xl md:text-5xl font-bold text-white mb-8">{s.title}</h3>
          <dl className="grid grid-cols-2 lg:grid-cols-3 gap-3 mb-8">
            {s.facts.map((f) => (
              <div key={f.value} className="rounded-2xl bg-white/[0.06] border border-white/10 p-4">
                <dt className="font-bold text-cyan-200 md:text-lg">{f.value}</dt>
                <dd className="text-white/70 text-sm leading-snug">{f.label}</dd>
              </div>
            ))}
          </dl>
          <p className="text-white/60 text-sm mb-3">{s.example.label}</p>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1"><span className="text-white/80">Pasted into every prompt</span><span className="font-mono text-amber-200">~{usd(s.example.pasted)}/month</span></div>
              <div className="h-3 rounded-full bg-gradient-to-r from-amber-400 to-rose-500" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1"><span className="text-white/80">Fetched with retrieval</span><span className="font-mono text-cyan-200">~{usd(s.example.fetched)}/month</span></div>
              <div className="h-3 rounded-full bg-white/10"><div className="h-3 rounded-full bg-cyan-300" style={{ width: `${share}%` }} /></div>
            </div>
          </div>
        </div>
      )
    }
  }
}

/** Slide-by-slide preview of the workshop deck, rebuilt as web content (the PDF is not embedded). */
export default function WorkshopDeck() {
  const slides = workshop.slides
  const last = slides.length // index of the closing "rest of the deck" panel
  const [i, setI] = useState(0)
  const touchX = useRef<number | null>(null)
  const go = (n: number) => setI(Math.min(Math.max(n, 0), last))

  const onKey = (e: KeyboardEvent) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1) }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1) }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[240px_minmax(0,1fr)] gap-6">
      {/* chapter rail */}
      <nav aria-label="Workshop slides" className="flex lg:flex-col gap-2 overflow-x-auto no-scrollbar -mx-6 px-6 lg:mx-0 lg:px-0">
        {[...slides.map((s) => s.title), 'The rest of the deck'].map((title, n) => (
          <button key={title} type="button" onClick={() => go(n)} aria-current={n === i ? 'step' : undefined}
            className={`shrink-0 text-left rounded-xl px-4 py-3 transition-all duration-200 border ${
              n === i ? 'bg-white/10 border-amber-300/60 text-white' : 'border-white/10 text-white/55 hover:text-white hover:bg-white/5'
            }`}>
            <span className="block font-mono text-xs text-amber-300/80">{n < last ? pad(n + 1) : '06–41'}</span>
            <span className="block text-sm font-semibold whitespace-nowrap lg:whitespace-normal">{title}</span>
          </button>
        ))}
      </nav>

      {/* stage */}
      <div>
        <div
          role="region" aria-roledescription="slide deck" aria-label={`${workshop.title} preview`} tabIndex={0} onKeyDown={onKey}
          onTouchStart={(e) => { touchX.current = e.touches[0].clientX }}
          onTouchEnd={(e) => {
            if (touchX.current === null) return
            const dx = e.changedTouches[0].clientX - touchX.current
            if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1))
            touchX.current = null
          }}
          className="relative rounded-3xl bg-[#0b1020] border border-white/10 shadow-2xl overflow-hidden focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-300/70"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_85%_10%,rgba(34,211,238,0.14),transparent_40%),radial-gradient(circle_at_10%_90%,rgba(251,191,36,0.10),transparent_45%)]" aria-hidden="true" />
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:32px_32px]" aria-hidden="true" />

          <div className="relative flex items-center justify-between px-6 md:px-10 pt-6 font-mono text-xs text-white/45">
            <span>{workshop.title}</span>
            <span aria-live="polite">{i < last ? `${pad(i + 1)} / ${workshop.totalSlides}` : `06–${workshop.totalSlides} / ${workshop.totalSlides}`}</span>
          </div>

          <div key={i} className="relative px-6 md:px-10 py-8 md:py-10 min-h-[480px] md:min-h-[520px] grid content-center animate-slide-in">
            {i < last ? <Slide s={slides[i]} /> : (
              <div className="flex flex-col items-center justify-center text-center h-full min-h-[400px]">
                <div className="relative w-56 h-36 mb-8" aria-hidden="true">
                  {[2, 1, 0].map((k) => (
                    <div key={k} className="absolute inset-0 rounded-xl border border-white/15 bg-white/[0.05] backdrop-blur"
                      style={{ transform: `translate(${k * 14}px, ${-k * 14}px) rotate(${k * 3}deg)` }} />
                  ))}
                  <span className="absolute inset-0 flex items-center justify-center text-5xl">🔒</span>
                </div>
                <p className="font-mono text-xs uppercase tracking-[0.2em] text-amber-300/90 mb-3">Preview ends here</p>
                <h3 className="text-3xl md:text-4xl font-bold text-white mb-3">{workshop.more}</h3>
                <p className="text-white/70 mb-8 max-w-lg">Run the full workshop with your team, on your own documents, onsite or virtual.</p>
                <Link href="#contact" className="bg-amber-300 text-slate-900 px-8 py-4 rounded-full font-bold hover:bg-amber-200 transition-all duration-300 hover:scale-105">
                  Book the workshop →
                </Link>
              </div>
            )}
          </div>

          {/* progress */}
          <div className="relative h-1 bg-white/10" aria-hidden="true">
            <div className="h-1 bg-gradient-to-r from-cyan-300 to-amber-300 transition-all duration-500" style={{ width: `${((i + 1) / (last + 1)) * 100}%` }} />
          </div>
        </div>

        <div className="flex items-center justify-between mt-4">
          <p className="text-white/45 text-sm hidden sm:block">Use ← → keys or swipe</p>
          <div className="flex gap-3 ml-auto">
            <button type="button" onClick={() => go(i - 1)} disabled={i === 0} aria-label="Previous slide"
              className="w-12 h-12 rounded-full border border-white/20 text-white text-xl hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-transparent transition">←</button>
            <button type="button" onClick={() => go(i + 1)} disabled={i === last} aria-label="Next slide"
              className="w-12 h-12 rounded-full bg-white text-slate-900 text-xl font-bold hover:bg-amber-200 disabled:opacity-30 transition">→</button>
          </div>
        </div>
      </div>
    </div>
  )
}
