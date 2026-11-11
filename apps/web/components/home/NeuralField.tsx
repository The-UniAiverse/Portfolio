'use client'

import { useEffect, useRef } from 'react'

type Node = { x: number; y: number; vx: number; vy: number; r: number; amber: boolean; phase: number }
type Pulse = { a: number; b: number; t: number; speed: number }

const LINK = 165 // max link distance (px)
const CYAN = '103, 232, 249'
const AMBER = '252, 211, 77'

/**
 * Live network backdrop for the homepage hero: drifting nodes, links between neighbours,
 * signal pulses travelling along links, and a soft pull towards the cursor.
 * Pauses off-screen; draws a single still frame for reduced-motion users.
 */
export default function NeuralField({ className = '' }: { className?: string }) {
  const ref = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = ref.current
    const ctx = canvas?.getContext('2d')
    if (!canvas || !ctx) return

    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let w = 0, h = 0, raf = 0, running = false
    let nodes: Node[] = []
    let pulses: Pulse[] = []
    const mouse = { x: -9999, y: -9999 }

    const seed = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      w = canvas.clientWidth
      h = canvas.clientHeight
      canvas.width = w * dpr
      canvas.height = h * dpr
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      const count = Math.min(140, Math.round((w * h) / 10000))
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: 1 + Math.random() * 1.6,
        amber: Math.random() < 0.08,
        phase: Math.random() * Math.PI * 2,
      }))
      pulses = []
    }

    const frame = (time: number) => {
      ctx.clearRect(0, 0, w, h)

      // move
      for (const n of nodes) {
        const dx = mouse.x - n.x, dy = mouse.y - n.y
        const d2 = dx * dx + dy * dy
        if (d2 < 180 * 180) { n.vx += dx * 0.000025; n.vy += dy * 0.000025 }
        n.vx *= 0.995; n.vy *= 0.995
        n.x += n.vx; n.y += n.vy
        if (n.x < 0 || n.x > w) n.vx *= -1
        if (n.y < 0 || n.y > h) n.vy *= -1
      }

      // links
      const links: [number, number][] = []
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j]
          const d = Math.hypot(a.x - b.x, a.y - b.y)
          if (d > LINK) continue
          links.push([i, j])
          ctx.strokeStyle = `rgba(${CYAN}, ${(1 - d / LINK) * 0.38})`
          ctx.lineWidth = 0.8
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke()
        }
        // cursor links
        const n = nodes[i]
        const dm = Math.hypot(n.x - mouse.x, n.y - mouse.y)
        if (dm < 180) {
          ctx.strokeStyle = `rgba(${AMBER}, ${(1 - dm / 180) * 0.35})`
          ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke()
        }
      }

      // pulses: spawn a few signals on random links
      if (!still && links.length && pulses.length < 14 && Math.random() < 0.08) {
        const [a, b] = links[Math.floor(Math.random() * links.length)]
        pulses.push({ a, b, t: 0, speed: 0.008 + Math.random() * 0.012 })
      }
      pulses = pulses.filter((p) => {
        p.t += p.speed
        const a = nodes[p.a], b = nodes[p.b]
        if (p.t >= 1 || Math.hypot(a.x - b.x, a.y - b.y) > LINK) return false
        const x = a.x + (b.x - a.x) * p.t, y = a.y + (b.y - a.y) * p.t
        const g = ctx.createRadialGradient(x, y, 0, x, y, 6)
        g.addColorStop(0, `rgba(${AMBER}, 0.95)`); g.addColorStop(1, `rgba(${AMBER}, 0)`)
        ctx.fillStyle = g
        ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2); ctx.fill()
        return true
      })

      // nodes
      for (const n of nodes) {
        const glow = 0.55 + 0.45 * Math.sin(time / 900 + n.phase)
        ctx.fillStyle = `rgba(${n.amber ? AMBER : CYAN}, ${0.35 + glow * 0.5})`
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r + (n.amber ? 0.8 : 0), 0, Math.PI * 2); ctx.fill()
      }

      if (running) raf = requestAnimationFrame(frame)
    }

    const start = () => { if (!running && !still) { running = true; raf = requestAnimationFrame(frame) } }
    const stop = () => { running = false; cancelAnimationFrame(raf) }

    seed()
    frame(0)

    const ro = new ResizeObserver(() => { seed(); frame(performance.now()) })
    ro.observe(canvas)
    const io = new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop()))
    io.observe(canvas)
    // The canvas sits behind the hero content, so track the pointer on the window.
    const onMove = (e: PointerEvent) => {
      const r = canvas.getBoundingClientRect()
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top
    }
    window.addEventListener('pointermove', onMove, { passive: true })

    return () => {
      stop(); ro.disconnect(); io.disconnect()
      window.removeEventListener('pointermove', onMove)
    }
  }, [])

  return <canvas ref={ref} aria-hidden="true" className={className} />
}
