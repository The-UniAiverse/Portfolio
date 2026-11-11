'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { serviceShowcase } from '@/data/services.data'
import { pillars } from '@/data/pillars.data'

const AUTOPLAY_MS = 4500
const pad = (n: number) => String(n).padStart(2, '0')

/**
 * Homepage sneak peek of the services, grouped under the four core pillars: a snap-scrolling carousel
 * that auto-advances until the visitor takes over. The pillar bar follows the scroll and jumps to a pillar.
 */
const Services = () => {
  const trackRef = useRef<HTMLDivElement>(null)
  const [index, setIndex] = useState(0)
  const [paused, setPaused] = useState(false)
  const [visible, setVisible] = useState(false)
  // Card we are scrolling to. Cards near the end can't reach the left edge, so the scroll position alone
  // can't tell which one was chosen; this keeps the chosen card active.
  const pending = useRef<number | null>(null)
  const last = serviceShowcase.length - 1

  const cards = () => Array.from(trackRef.current?.children ?? []) as HTMLElement[]
  const atEnd = useCallback(() => {
    const t = trackRef.current
    return !!t && t.scrollLeft >= t.scrollWidth - t.clientWidth - 4
  }, [])

  const goTo = useCallback((n: number) => {
    const t = trackRef.current
    const list = Array.from(t?.children ?? []) as HTMLElement[]
    if (!t || !list.length) return
    const target = (n + list.length) % list.length
    const left = Math.min(list[target].offsetLeft - list[0].offsetLeft, t.scrollWidth - t.clientWidth)
    pending.current = Math.abs(t.scrollLeft - left) > 2 ? target : null
    setIndex(target)
    t.scrollTo({ left, behavior: 'smooth' })
  }, [])

  const onScroll = () => {
    const t = trackRef.current
    const list = cards()
    if (!t || !list.length) return
    if (pending.current !== null) {
      const left = list[pending.current].offsetLeft - list[0].offsetLeft
      if (Math.abs(t.scrollLeft - left) < 4 || atEnd()) pending.current = null
      return
    }
    if (atEnd()) {
      // Several cards are fully visible at the end; keep the active one if it is among them.
      const firstVisible = list.findIndex((c) => c.offsetLeft - list[0].offsetLeft >= t.scrollLeft - 4)
      return setIndex((cur) => (cur >= firstVisible ? cur : last))
    }
    let best = 0
    list.forEach((c, i) => {
      const d = Math.abs(c.offsetLeft - list[0].offsetLeft - t.scrollLeft)
      if (d < Math.abs(list[best].offsetLeft - list[0].offsetLeft - t.scrollLeft)) best = i
    })
    setIndex(best)
  }

  const next = () => goTo(index >= last ? 0 : index + 1)
  const prev = () => goTo(Math.max(index - 1, 0))

  // Only auto-advance while the carousel is on screen.
  useEffect(() => {
    const t = trackRef.current
    if (!t) return
    const io = new IntersectionObserver(([e]) => setVisible(e.isIntersecting), { threshold: 0.4 })
    io.observe(t)
    return () => io.disconnect()
  }, [])

  useEffect(() => {
    if (paused || !visible || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const id = window.setTimeout(() => goTo(index >= last ? 0 : index + 1), AUTOPLAY_MS)
    return () => window.clearTimeout(id)
  }, [index, paused, visible, goTo, last])

  const activePillar = serviceShowcase[index]?.pillar
  const pillarOf = (id: string) => pillars.find((p) => p.id === id)!

  return (
    <section id="services" className="py-24 bg-secondary-light overflow-hidden scroll-mt-20">
      <div className="container mx-auto px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-end md:justify-between gap-8 mb-12">
          <div className="max-w-2xl">
            <p className="kicker mb-3">What we do</p>
            <h2 className="text-4xl md:text-5xl font-bold text-primary-dark leading-tight">
              Four pillars. <span className="text-primary">One AI partner.</span>
            </h2>
            <p className="text-lg text-primary-dark/70 mt-4">From the first strategy session to production systems and trained teams: pick where you are, we take it from there.</p>
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <span className="font-mono text-primary-dark/60 tabular-nums" aria-live="polite">
              <span className="text-primary-dark font-bold">{pad(index + 1)}</span> / {pad(serviceShowcase.length)}
            </span>
            <button type="button" onClick={prev} disabled={index === 0} aria-label="Previous service"
              className="w-12 h-12 rounded-full border-2 border-primary/20 text-primary-dark text-xl hover:border-primary hover:text-primary disabled:opacity-30 disabled:hover:border-primary/20 transition">←</button>
            <button type="button" onClick={next} aria-label="Next service"
              className="w-12 h-12 rounded-full bg-primary text-secondary text-xl hover:bg-primary-light hover:shadow-lg hover:shadow-primary-light/40 transition">→</button>
          </div>
        </div>
      </div>

      {/* pillar bar */}
      <div className="container mx-auto px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-3 mb-10" role="group" aria-label="Jump to a pillar">
          {pillars.map((p) => {
            const on = p.id === activePillar
            const count = serviceShowcase.filter((s) => s.pillar === p.id).length
            return (
              <button key={p.id} type="button" aria-pressed={on}
                onClick={() => goTo(serviceShowcase.findIndex((s) => s.pillar === p.id))}
                className={`text-left rounded-2xl border px-5 py-4 transition-all duration-300 ${
                  on ? 'border-amber-300/60 bg-white/[0.06]' : 'border-white/10 hover:border-white/25 hover:bg-white/[0.03]'
                }`}>
                <span className={`block font-mono text-xs mb-1 ${on ? 'text-amber-300' : 'text-white/40'}`}>{p.number} · {count} {count === 1 ? 'offering' : 'offerings'}</span>
                <span className={`block font-semibold leading-snug ${on ? 'text-white' : 'text-white/65'}`}>{p.title}</span>
                <span className={`hidden md:block font-mono text-[11px] uppercase tracking-[0.15em] mt-2 ${on ? 'text-cyan-200' : 'text-white/30'}`}>{p.verbs.join(' · ')}</span>
              </button>
            )
          })}
        </div>
      </div>

      <div
        ref={trackRef}
        onScroll={onScroll}
        onMouseEnter={() => setPaused(true)}
        onMouseLeave={() => setPaused(false)}
        onFocus={() => setPaused(true)}
        onBlur={() => setPaused(false)}
        onTouchStart={() => { pending.current = null; setPaused(true) }}
        onWheel={() => { pending.current = null }}
        role="region"
        aria-roledescription="carousel"
        aria-label="Our services"
        className="relative flex gap-6 overflow-x-auto snap-x snap-mandatory no-scrollbar pb-8 px-6 scroll-px-6 md:px-[max(1.5rem,calc((100vw-80rem)/2+1.5rem))] md:scroll-px-[max(1.5rem,calc((100vw-80rem)/2+1.5rem))]"
      >
        {serviceShowcase.map((s, i) => (
          <Link key={s.href} href={s.href} aria-label={`${s.title}: ${s.blurb}`}
            className={`group snap-start shrink-0 w-[85vw] sm:w-[380px] flex flex-col bg-secondary rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 ${
              i === index ? 'ring-1 ring-amber-300/50' : ''
            }`}>
            <div className={`relative h-44 bg-gradient-to-br ${s.gradient} p-7 flex items-end justify-between overflow-hidden`}>
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.07)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.07)_1px,transparent_1px)] bg-[size:28px_28px]" aria-hidden="true" />
              <div className="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-white/10 blur-2xl transition-transform duration-500 group-hover:scale-150" aria-hidden="true" />
              <span className="relative text-6xl drop-shadow-lg transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-6" aria-hidden="true">{s.icon}</span>
              <span className="relative font-mono text-secondary/70 text-xs text-right leading-relaxed">
                Pillar {pillarOf(s.pillar).number}<br />{pad(i + 1)}
              </span>
            </div>
            <div className="flex-1 flex flex-col p-7">
              <h3 className="text-2xl font-bold text-primary-dark mb-2 group-hover:text-primary transition-colors">{s.title}</h3>
              <p className="text-primary-dark/70 leading-relaxed mb-5">{s.blurb}</p>
              <ul className="space-y-2 mb-6 flex-1">
                {s.points.map((p) => (
                  <li key={p} className="flex items-start gap-2 text-sm text-primary-dark/80"><span className="text-primary" aria-hidden="true">✓</span>{p}</li>
                ))}
              </ul>
              <span className="font-semibold text-primary group-hover:text-primary-light">
                Explore <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </span>
            </div>
          </Link>
        ))}
      </div>

      <div className="container mx-auto px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          <div className="flex gap-2" role="group" aria-label="Choose a service">
            {serviceShowcase.map((s, i) => (
              <button key={s.href} type="button" onClick={() => goTo(i)} aria-label={`Show ${s.title}`} aria-current={i === index}
                className={`h-2 rounded-full transition-all duration-500 ${i === index ? 'w-10 bg-primary' : 'w-2 bg-primary/20 hover:bg-primary/40'}`} />
            ))}
          </div>
          <Link href="/services" className="font-semibold text-primary hover:text-primary-light">See all services →</Link>
        </div>
      </div>
    </section>
  )
}

export default Services
