'use client'

import { useCallback, useEffect, useState, type FormEvent, type ReactNode } from 'react'
import { courseFileUrl, getCatalog, getCourse, recommendPath, type Catalog, type Course, errorText } from '@/lib/ai-services'

// Course catalogue + learning-path finder served by apps/api (training-materials/catalog.yaml).
// Styled to sit inside the Training page, which defines the `syne` and `track-card` classes.

const AUDIENCE_LABELS: Record<string, string> = {
  business: 'Business users',
  leadership: 'Leadership',
  sales: 'Sales',
  marketing: 'Marketing',
  engineer: 'Engineers',
  genai_engineer: 'GenAI engineers',
}

const pill = { background: 'linear-gradient(135deg,#92400e,#d97706)', color: '#fff', padding: '4px 18px', borderRadius: '100px', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase' as const }

// Minimal Markdown → React (headings, lists, tables, **bold**, `code`). No raw HTML is injected.
function inline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, i) =>
    part.startsWith('**') && part.endsWith('**') ? <strong key={i}>{part.slice(2, -2)}</strong>
      : part.startsWith('`') && part.endsWith('`') ? <code key={i} className="bg-amber-50 text-amber-800 px-1.5 py-0.5 rounded text-[0.9em]">{part.slice(1, -1)}</code>
      : part
  )
}

function Markdown({ source }: { source: string }) {
  const lines = source.split('\n')
  const out: ReactNode[] = []
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trimEnd()
    if (!line.trim()) continue
    if (line.startsWith('|')) {
      const rows: string[][] = []
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        const cells = lines[i].trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim())
        if (!cells.every((c) => /^-+$/.test(c))) rows.push(cells)
        i++
      }
      i--
      const [head, ...body] = rows
      out.push(
        <div key={i} className="overflow-x-auto my-4">
          <table className="w-full text-sm text-left">
            <thead><tr className="border-b border-amber-200">{head.map((c, j) => <th key={j} className="py-2 pr-3 font-semibold">{inline(c)}</th>)}</tr></thead>
            <tbody>{body.map((r, k) => <tr key={k} className="border-b border-amber-100">{r.map((c, j) => <td key={j} className="py-2 pr-3 align-top">{inline(c)}</td>)}</tr>)}</tbody>
          </table>
        </div>
      )
    } else if (line.startsWith('# ')) {
      out.push(<h3 key={i} className="syne text-2xl font-bold mt-2 mb-3">{inline(line.slice(2))}</h3>)
    } else if (line.startsWith('## ')) {
      out.push(<h4 key={i} className="syne text-lg font-bold mt-6 mb-2">{inline(line.slice(3))}</h4>)
    } else if (/^(\d+\.|[-*])\s/.test(line)) {
      out.push(<p key={i} className="pl-4 my-1">• {inline(line.replace(/^(\d+\.|[-*])\s/, ''))}</p>)
    } else {
      out.push(<p key={i} className="my-2">{inline(line)}</p>)
    }
  }
  return <div className="text-primary-dark/80 leading-relaxed">{out}</div>
}

function CourseModal({ course, onClose }: { course: Course; onClose: () => void }) {
  const [outline, setOutline] = useState<string | null | undefined>(undefined)

  useEffect(() => {
    getCourse(course.id).then((c) => setOutline(c.outline_markdown)).catch(() => setOutline(null))
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [course.id, onClose])

  // Only files inside the course's own folder are downloadable through the API.
  const files = (course.files ?? []).filter((f) => !f.includes('/'))

  return (
    <div className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm flex items-start justify-center p-4 overflow-y-auto" onClick={onClose}>
      <div role="dialog" aria-modal="true" aria-label={course.title}
        className="bg-secondary rounded-2xl shadow-2xl max-w-3xl w-full my-12 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div style={{ height: '4px', background: 'linear-gradient(90deg,#d97706,#f59e0b,transparent)' }} />
        <div className="p-8">
          <div className="flex justify-between items-start gap-4 mb-4">
            <div>
              <h3 className="syne text-2xl font-bold text-primary-dark">{course.title}</h3>
              <p className="text-primary-dark/60 text-sm mt-1">{course.hours} hours · {course.format}</p>
            </div>
            <button type="button" onClick={onClose} aria-label="Close" className="text-2xl text-primary-dark/50 hover:text-primary-dark">×</button>
          </div>
          {files.length > 0 && (
            <div className="flex flex-wrap gap-3 mb-6">
              {files.map((f) => (
                <a key={f} href={courseFileUrl(course.id, f)} target="_blank" rel="noopener noreferrer"
                  className="text-sm font-semibold px-4 py-2 rounded-full border-2 border-amber-600 text-amber-700 hover:bg-amber-600 hover:text-white transition-all duration-300">
                  ⬇ {f}
                </a>
              ))}
            </div>
          )}
          {outline === undefined && <p className="text-primary-dark/50">Loading outline…</p>}
          {outline === null && <p className="text-primary-dark/50">Detailed outline available on request.</p>}
          {outline && <Markdown source={outline} />}
        </div>
      </div>
    </div>
  )
}

export default function TrainingCatalog() {
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [audience, setAudience] = useState('')
  const [goal, setGoal] = useState('')
  const [path, setPath] = useState<string[] | null>(null)
  const [finding, setFinding] = useState(false)
  const [open, setOpen] = useState<Course | null>(null)
  const closeCourse = useCallback(() => setOpen(null), [])

  useEffect(() => {
    getCatalog()
      .then((c) => {
        setCatalog(c)
        setAudience(Object.keys(c.learning_paths)[0] ?? '')
      })
      .catch((e) => setError(errorText(e)))
  }, [])

  async function findPath(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setFinding(true)
    try {
      setPath((await recommendPath(audience, goal.trim())).path)
    } catch (e) {
      setError(errorText(e))
    } finally {
      setFinding(false)
    }
  }

  // The catalogue is supplementary: if the API is unreachable the rest of the page still works.
  if (!catalog) return null

  const byId = Object.fromEntries(catalog.courses.map((c) => [c.id, c]))

  return (
    <section className="py-24 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <span style={pill}>Short Courses & Workshops</span>
            <h2 className="syne text-primary-dark mt-5 mb-5" style={{ fontSize: 'clamp(2rem,4vw,2.75rem)', fontWeight: 800, letterSpacing: '-0.02em' }}>
              Course Catalogue
            </h2>
            <p className="text-primary-dark/70 text-xl max-w-3xl mx-auto leading-relaxed">
              Focused workshops for every team, plus a learning path matched to your role.
            </p>
          </div>

          {/* Learning-path finder */}
          <form onSubmit={findPath} className="bg-secondary-light rounded-2xl shadow-md p-8 mb-14">
            <h3 className="syne text-primary-dark text-xl font-bold mb-5">Find your learning path</h3>
            <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr_auto] gap-4 items-end">
              <div>
                <label htmlFor="lp-audience" className="block text-sm font-semibold text-primary-dark mb-2">I am in…</label>
                <select id="lp-audience" value={audience} onChange={(e) => setAudience(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-amber-300 bg-secondary text-primary-dark focus:outline-none focus:ring-2 focus:ring-amber-500">
                  {Object.keys(catalog.learning_paths).map((a) => <option key={a} value={a}>{AUDIENCE_LABELS[a] ?? a}</option>)}
                </select>
              </div>
              <div>
                <label htmlFor="lp-goal" className="block text-sm font-semibold text-primary-dark mb-2">My goal (optional)</label>
                <input id="lp-goal" value={goal} maxLength={200} onChange={(e) => setGoal(e.target.value)} placeholder="Use AI safely in day-to-day work"
                  className="w-full px-4 py-3 rounded-xl border border-amber-300 bg-secondary text-primary-dark focus:outline-none focus:ring-2 focus:ring-amber-500" />
              </div>
              <button type="submit" disabled={finding}
                className="text-white px-8 py-3 rounded-full font-bold transition-all duration-300 hover:shadow-lg disabled:opacity-60"
                style={{ background: 'linear-gradient(135deg,#b45309,#f59e0b)' }}>
                {finding ? 'Finding…' : 'Show my path →'}
              </button>
            </div>
            {error && <p role="alert" className="mt-4 text-red-700">{error}</p>}
            {path && (
              <ol className="mt-8 flex flex-col md:flex-row md:flex-wrap gap-3">
                {path.map((id, i) => byId[id] && (
                  <li key={id} className="flex items-center gap-3">
                    <button type="button" onClick={() => setOpen(byId[id])}
                      className="flex items-center gap-3 bg-secondary border border-amber-300 rounded-xl px-4 py-3 hover:border-amber-600 transition-all duration-300 text-left">
                      <span className="w-7 h-7 rounded-full text-white text-sm font-bold flex items-center justify-center shrink-0" style={{ background: '#d97706' }}>{i + 1}</span>
                      <span>
                        <span className="block font-semibold text-primary-dark text-sm">{byId[id].title}</span>
                        <span className="block text-xs text-primary-dark/60">{byId[id].hours} hrs</span>
                      </span>
                    </button>
                    {i < path.length - 1 && <span className="hidden md:inline text-amber-600 font-bold">→</span>}
                  </li>
                ))}
              </ol>
            )}
          </form>

          {/* Course grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
            {catalog.courses.map((c) => (
              <button key={c.id} type="button" onClick={() => setOpen(c)}
                className="bg-secondary-light rounded-2xl shadow-md overflow-hidden track-card text-left">
                <div style={{ height: '3px', background: 'linear-gradient(90deg, #d97706, transparent)' }} />
                <div className="p-7">
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span style={{ background: '#d9770614', color: '#b45309', border: '1px solid #d9770635', padding: '3px 11px', borderRadius: '100px', fontSize: '0.72rem', fontWeight: 700 }}>{c.hours} hrs</span>
                    <span style={{ background: '#d9770614', color: '#b45309', border: '1px solid #d9770635', padding: '3px 11px', borderRadius: '100px', fontSize: '0.72rem', fontWeight: 700 }}>{c.format}</span>
                  </div>
                  <h3 className="syne text-primary-dark mb-2" style={{ fontSize: '1.15rem', fontWeight: 700 }}>{c.title}</h3>
                  <p className="text-primary-dark/50 text-xs font-semibold uppercase tracking-wide mb-3">{c.audience}</p>
                  <p className="text-primary-dark/70 text-sm leading-relaxed">{c.outcome}</p>
                  <span className="inline-block mt-5 text-sm font-semibold" style={{ color: '#b45309' }}>View outline →</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
      {open && <CourseModal course={open} onClose={closeCourse} />}
    </section>
  )
}
