'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { paths, programById, programs, tracks, type Program, type TrackId } from '@/data/training.data'

function ProgramCard({ p, active, recommended, onOpen }: { p: Program; active: boolean; recommended: boolean; onOpen: () => void }) {
  const flagship = p.track === 'flagship'
  return (
    <button
      type="button"
      onClick={onOpen}
      aria-pressed={active}
      className={`group relative text-left rounded-2xl p-7 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl ${
        flagship ? 'bg-gradient-blue text-secondary shadow-xl md:col-span-2 xl:col-span-1' : 'bg-secondary-light shadow-lg'
      } ${active ? 'ring-4 ring-primary-light' : ''} ${recommended ? 'ring-2 ring-primary-light/70' : ''}`}
    >
      {recommended && (
        <span className="absolute -top-3 left-6 bg-primary-light text-secondary text-xs font-bold px-3 py-1 rounded-full shadow">Recommended for you</span>
      )}
      <div className="flex items-start justify-between gap-3 mb-5">
        <span className="text-4xl transition-transform duration-300 group-hover:scale-110">{p.icon}</span>
        {p.badge && (
          <span className={`text-xs font-bold px-3 py-1 rounded-full ${flagship ? 'bg-secondary/20 text-secondary' : 'bg-primary text-secondary'}`}>{p.badge}</span>
        )}
      </div>
      <h3 className={`text-2xl font-bold mb-2 ${flagship ? 'text-secondary' : 'text-primary-dark'}`}>{p.title}</h3>
      <p className={`mb-5 leading-relaxed ${flagship ? 'text-secondary/85' : 'text-primary-dark/70'}`}>{p.tagline}</p>
      <div className="flex flex-wrap gap-2 mb-6">
        {(p.track === 'flagship' ? ['DSA', 'Full Stack', 'ML & DL', 'AI Engineering', 'GenAI', 'Agents'] : p.tools.slice(0, 4)).map((t) => (
          <span key={t} className={`text-xs font-semibold px-3 py-1 rounded-full ${flagship ? 'bg-secondary/15 text-secondary' : 'bg-secondary text-primary-dark/70 border border-primary/10'}`}>{t}</span>
        ))}
      </div>
      <div className="flex items-center justify-between gap-3">
        <span className={`text-sm font-medium ${flagship ? 'text-secondary/80' : 'text-primary-dark/50'}`}>{p.level}</span>
        <span className={`shrink-0 whitespace-nowrap font-semibold ${flagship ? 'text-secondary' : 'text-primary group-hover:text-primary-light'}`}>
          View syllabus <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
        </span>
      </div>
    </button>
  )
}

function Syllabus({ p }: { p: Program }) {
  const [open, setOpen] = useState<number | null>(0)
  const block = (title: string, items: string[], marker = '✓') => (
    <div>
      <h4 className="text-sm font-bold uppercase tracking-wider text-primary mb-3">{title}</h4>
      <ul className="space-y-2">
        {items.map((i) => (
          <li key={i} className="flex items-start text-primary-dark/80 leading-relaxed">
            <span className="text-primary mr-3 mt-0.5 shrink-0">{marker}</span>{i}
          </li>
        ))}
      </ul>
    </div>
  )

  return (
    <div className="bg-secondary rounded-3xl shadow-2xl overflow-hidden border border-primary/10">
      <div className="bg-gradient-blue p-8 md:p-10 text-secondary">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className="text-5xl">{p.icon}</span>
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-secondary/15">{tracks.find((t) => t.id === p.track)?.label}</span>
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-secondary/15">{p.level}</span>
        </div>
        <h3 className="text-3xl md:text-4xl font-bold mb-3">{p.title}</h3>
        <p className="text-lg text-secondary/85 max-w-3xl leading-relaxed">{p.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,2fr)_minmax(0,3fr)] gap-10 p-8 md:p-10">
        <div className="space-y-8">
          {block('Who it’s for', p.forWho, '→')}
          {block('Prerequisites', p.prerequisites, '•')}
          {block('What you’ll be able to do', p.outcomes)}
          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-primary mb-3">Tools & technologies</h4>
            <div className="flex flex-wrap gap-2">
              {p.tools.map((t) => (
                <span key={t} className="bg-primary/10 text-primary px-3 py-1.5 rounded-full text-sm font-semibold">{t}</span>
              ))}
            </div>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-bold uppercase tracking-wider text-primary mb-4">Syllabus · {p.modules.length} modules</h4>
          <ol className="space-y-3">
            {p.modules.map((m, i) => {
              const isOpen = open === i
              return (
                <li key={m.title} className={`rounded-2xl border transition-all duration-300 ${isOpen ? 'border-primary-light bg-secondary-light shadow-md' : 'border-primary/10 hover:border-primary-light/60'}`}>
                  <button type="button" onClick={() => setOpen(isOpen ? null : i)} aria-expanded={isOpen}
                    className="w-full flex items-center gap-4 p-5 text-left">
                    <span className={`w-10 h-10 shrink-0 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${isOpen ? 'bg-primary text-secondary' : 'bg-primary/10 text-primary'}`}>
                      {String(i + 1).padStart(2, '0')}
                    </span>
                    <span className="flex-1 font-semibold text-primary-dark">{m.title}</span>
                    <span className={`text-primary transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} aria-hidden="true">⌄</span>
                  </button>
                  {isOpen && (
                    <div className="px-5 pb-5 pl-[4.75rem] space-y-4">
                      <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
                        {m.topics.map((t) => (
                          <li key={t} className="flex items-start text-sm text-primary-dark/75"><span className="text-primary-light mr-2">•</span>{t}</li>
                        ))}
                      </ul>
                      <p className="text-sm bg-primary/5 border border-primary/10 rounded-xl px-4 py-3 text-primary-dark/80">
                        <span className="font-bold text-primary">Hands-on lab: </span>{m.lab}
                      </p>
                    </div>
                  )}
                </li>
              )
            })}
          </ol>

          <div className="mt-8 bg-primary-dark rounded-2xl p-6 text-secondary">
            <h4 className="text-sm font-bold uppercase tracking-wider text-primary-lighter mb-3">Portfolio projects</h4>
            <ul className="space-y-2">
              {p.projects.map((pr) => <li key={pr} className="flex items-start"><span className="mr-3">🏗️</span>{pr}</li>)}
            </ul>
          </div>

          <div className="mt-8 flex flex-col sm:flex-row gap-3">
            <Link href="#contact" className="text-center bg-primary hover:bg-primary-light text-secondary px-8 py-4 rounded-full font-bold transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50">
              {p.id === 'corporate' ? 'Plan a program for your team →' : 'Talk to a mentor about this program →'}
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ProgramExplorer() {
  const [track, setTrack] = useState<TrackId | 'all'>('all')
  const [pathId, setPathId] = useState<string | null>(null)
  const [selected, setSelected] = useState<string>(programs[0].id)
  const detailRef = useRef<HTMLDivElement>(null)

  // Deep links like #program-generative-ai (used by the roadmap) open that syllabus.
  useEffect(() => {
    const fromHash = () => {
      const id = window.location.hash.replace('#program-', '')
      if (window.location.hash.startsWith('#program-') && programById(id)) {
        setSelected(id)
        setTrack('all')
        requestAnimationFrame(() => detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
      }
    }
    const initial = setTimeout(fromHash, 0) // after hydration, so server and client HTML match
    window.addEventListener('hashchange', fromHash)
    return () => {
      clearTimeout(initial)
      window.removeEventListener('hashchange', fromHash)
    }
  }, [])

  const path = paths.find((x) => x.id === pathId)
  const shown = programs.filter((p) => track === 'all' || p.track === track)
  const current = programById(selected) ?? programs[0]

  function open(id: string) {
    setSelected(id)
    requestAnimationFrame(() => detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
  }

  return (
    <div className="space-y-16">
      {/* Find your path */}
      <div className="bg-secondary-light rounded-3xl p-8 md:p-10 shadow-lg">
        <div className="text-center mb-8">
          <h3 className="text-2xl md:text-3xl font-bold text-primary-dark mb-2">Find your path</h3>
          <p className="text-primary-dark/60">Tell us where you are today and we’ll show you where to start.</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {paths.map((x) => (
            <button key={x.id} type="button" onClick={() => setPathId(pathId === x.id ? null : x.id)} aria-pressed={pathId === x.id}
              className={`rounded-2xl p-4 text-center border-2 transition-all duration-300 ${pathId === x.id ? 'border-primary bg-primary text-secondary shadow-lg -translate-y-1' : 'border-primary/10 bg-secondary hover:border-primary-light'}`}>
              <div className="text-3xl mb-2">{x.icon}</div>
              <div className={`text-sm font-semibold ${pathId === x.id ? 'text-secondary' : 'text-primary-dark'}`}>{x.label}</div>
            </button>
          ))}
        </div>
        {path && (
          <div className="mt-8 flex flex-col md:flex-row md:items-center gap-4 bg-secondary rounded-2xl p-6 border border-primary/10">
            <p className="text-primary-dark/80 md:w-1/3"><span className="font-bold text-primary-dark">{path.summary}</span></p>
            <ol className="flex flex-wrap items-center gap-2">
              {path.programs.map((id, i) => {
                const p = programById(id)!
                return (
                  <li key={id} className="flex items-center gap-2">
                    <button type="button" onClick={() => open(id)} className="flex items-center gap-2 bg-primary/10 hover:bg-primary hover:text-secondary text-primary px-4 py-2 rounded-full font-semibold text-sm transition-all duration-300">
                      <span className="w-5 h-5 rounded-full bg-primary text-secondary text-xs flex items-center justify-center">{i + 1}</span>
                      {p.title}
                    </button>
                    {i < path.programs.length - 1 && <span className="text-primary-light font-bold">→</span>}
                  </li>
                )
              })}
            </ol>
          </div>
        )}
      </div>

      {/* Programs */}
      <div>
        <div className="flex flex-wrap justify-center gap-3 mb-10">
          {([{ id: 'all', label: 'All programs' }, ...tracks] as { id: TrackId | 'all'; label: string }[]).map((t) => (
            <button key={t.id} type="button" onClick={() => setTrack(t.id)} aria-pressed={track === t.id}
              className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${track === t.id ? 'bg-primary text-secondary shadow-lg' : 'bg-secondary-light text-primary-dark hover:bg-primary/10'}`}>
              {t.label}
            </button>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
          {shown.map((p) => (
            <ProgramCard key={p.id} p={p} active={selected === p.id} recommended={!!path?.programs.includes(p.id)} onOpen={() => open(p.id)} />
          ))}
        </div>
      </div>

      {/* Syllabus */}
      <div id="syllabus" ref={detailRef} className="scroll-mt-28">
        <div className="text-center mb-8">
          <span className="inline-block bg-primary/10 text-primary px-4 py-1.5 rounded-full text-sm font-bold mb-3">Syllabus</span>
          <div className="flex flex-wrap justify-center gap-2">
            {programs.map((p) => (
              <button key={p.id} type="button" onClick={() => setSelected(p.id)} aria-pressed={selected === p.id}
                className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${selected === p.id ? 'bg-primary text-secondary' : 'bg-secondary-light text-primary-dark/70 hover:text-primary'}`}>
                {p.icon} {p.title}
              </button>
            ))}
          </div>
        </div>
        <Syllabus key={current.id} p={current} />
      </div>
    </div>
  )
}
