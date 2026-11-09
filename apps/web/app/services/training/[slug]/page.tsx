import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import CourseCard from '@/components/training/CourseCard'
import CourseFinder from '@/components/training/CourseFinder'
import SyllabusAccordion from '@/components/training/SyllabusAccordion'
import { programById, programs, tracks } from '@/data/training.data'

// Stage order of the flagship program; each stage is a full course.
const MASTERY_STAGES = ['dsa', 'full-stack', 'ml-dl', 'ai-engineering', 'generative-ai', 'agentic-ai']

type Params = { params: Promise<{ slug: string }> }

export function generateStaticParams() {
  return programs.map((p) => ({ slug: p.id }))
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const p = programById((await params).slug)
  if (!p) return { title: 'Course not found | uniAiverse' }
  return { title: `${p.title} | Training & Mentorship | uniAiverse`, description: p.description }
}

function CheckList({ items }: { items: string[] }) {
  return (
    <ul className="space-y-2">
      {items.map((i) => (
        <li key={i} className="flex items-start text-primary-dark/80 leading-relaxed"><span className="text-primary mr-3 mt-0.5 shrink-0">✓</span>{i}</li>
      ))}
    </ul>
  )
}

export default async function CoursePage({ params }: Params) {
  const p = programById((await params).slug)
  if (!p) notFound()

  const track = tracks.find((t) => t.id === p.track)!
  const related = [
    ...programs.filter((x) => x.track === p.track && x.id !== p.id),
    ...programs.filter((x) => x.track !== p.track && x.id !== p.id),
  ].slice(0, 3)

  return (
    <main className="min-h-screen">
      <Header />

      {/* ── Course hero ──────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600 pt-32 pb-16">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob" />
          <div className="absolute -bottom-40 -left-20 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob animation-delay-2000" />
        </div>
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-6xl mx-auto">
            <nav aria-label="Breadcrumb" className="text-sm text-secondary/70 mb-8">
              <Link href="/services/training" className="hover:text-secondary">Training & Mentorship</Link>
              <span className="mx-2">/</span>
              <span className="text-secondary">{p.title}</span>
            </nav>
            <div className="flex flex-wrap items-center gap-3 mb-5">
              <span className="text-6xl" aria-hidden="true">{p.icon}</span>
              <span className="bg-secondary/15 text-secondary text-sm font-semibold px-4 py-1.5 rounded-full">{track.label}</span>
              {p.badge && <span className="bg-secondary text-primary-dark text-sm font-bold px-4 py-1.5 rounded-full">{p.badge}</span>}
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-secondary leading-tight mb-4">{p.title}</h1>
            <p className="text-2xl text-secondary/90 mb-4">{p.tagline}</p>
            <p className="text-lg text-secondary/75 leading-relaxed max-w-3xl mb-10">{p.description}</p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="#contact" className="text-center bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:scale-105">
                {p.id === 'corporate' ? 'Plan a program with us' : 'Talk to a mentor'}
              </Link>
              <CourseFinder label="Not sure this is for you?" variant="outline" />
            </div>
          </div>
        </div>
      </section>

      {/* ── Course body ──────────────────────────────────────────────────── */}
      <section className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_340px] gap-12 items-start">
            <div className="space-y-16 min-w-0">
              <div>
                <h2 className="text-3xl font-bold text-primary-dark mb-6">What you’ll be able to do</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {p.outcomes.map((o) => (
                    <div key={o} className="flex items-start gap-3 bg-secondary-light rounded-2xl p-5">
                      <span className="w-7 h-7 rounded-full bg-primary text-secondary flex items-center justify-center text-sm shrink-0">✓</span>
                      <span className="text-primary-dark/80 leading-relaxed">{o}</span>
                    </div>
                  ))}
                </div>
              </div>

              {p.id === 'ai-mastery' && (
                <div>
                  <h2 className="text-3xl font-bold text-primary-dark mb-2">Your roadmap</h2>
                  <p className="text-primary-dark/60 mb-6">Six full courses in order, each one building on the last. Open any stage to see its full syllabus.</p>
                  <ol className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {MASTERY_STAGES.map((id, i) => {
                      const s = programById(id)!
                      return (
                        <li key={id}>
                          <Link href={`/services/training/${id}`} className="group block bg-gradient-blue rounded-2xl p-5 text-secondary h-full hover:-translate-y-1 transition-all duration-300 hover:shadow-xl">
                            <span className="text-xs font-bold uppercase tracking-widest text-primary-lighter">Stage {i + 1}</span>
                            <span className="flex items-center gap-2 mt-2 font-semibold"><span className="text-2xl" aria-hidden="true">{s.icon}</span>{s.title}</span>
                          </Link>
                        </li>
                      )
                    })}
                  </ol>
                </div>
              )}

              <div>
                <div className="flex items-end justify-between gap-4 mb-2">
                  <h2 className="text-3xl font-bold text-primary-dark">Syllabus</h2>
                  <span className="text-primary-dark/50 font-semibold">{p.modules.length} modules</span>
                </div>
                <p className="text-primary-dark/60 mb-4">Every module ends with a hands-on lab reviewed by your mentor.</p>
                <SyllabusAccordion modules={p.modules} />
              </div>

              <div className="bg-primary-dark rounded-3xl p-8 text-secondary">
                <h2 className="text-2xl font-bold mb-5">Portfolio projects</h2>
                <ul className="space-y-3">
                  {p.projects.map((x) => <li key={x} className="flex items-start gap-3"><span aria-hidden="true">🏗️</span><span className="text-secondary/90">{x}</span></li>)}
                </ul>
              </div>

              <div>
                <h2 className="text-3xl font-bold text-primary-dark mb-6">Tools & technologies</h2>
                <div className="flex flex-wrap gap-3">
                  {p.tools.map((t) => (
                    <span key={t} className="bg-primary/10 text-primary px-4 py-2 rounded-full font-semibold">{t}</span>
                  ))}
                </div>
              </div>
            </div>

            {/* sticky side card */}
            <aside className="lg:sticky lg:top-28 space-y-6">
              <div className="bg-secondary-light rounded-3xl p-7 shadow-lg">
                <h2 className="text-lg font-bold text-primary-dark mb-4">At a glance</h2>
                <dl className="space-y-3 text-sm">
                  {[
                    ['Level', p.level],
                    ['Syllabus', `${p.modules.length} modules + projects`],
                    ['Format', 'Live sessions + self-paced labs'],
                    ['Mentorship', '1:1 mentor and code reviews'],
                    ['Pace', 'Learn at your own pace'],
                    ['Certificate', 'Yes, on completion'],
                  ].map(([k, v]) => (
                    <div key={k} className="flex justify-between gap-4 border-b border-primary/10 pb-3 last:border-0 last:pb-0">
                      <dt className="text-primary-dark/50">{k}</dt>
                      <dd className="font-semibold text-primary-dark text-right">{v}</dd>
                    </div>
                  ))}
                </dl>
                <Link href="#contact" className="mt-6 block text-center bg-primary hover:bg-primary-light text-secondary px-6 py-3.5 rounded-full font-bold transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50">
                  {p.id === 'corporate' ? 'Plan a program →' : 'Talk to a mentor →'}
                </Link>
              </div>
              <div className="bg-secondary-light rounded-3xl p-7 shadow-lg space-y-6">
                <div>
                  <h2 className="text-lg font-bold text-primary-dark mb-3">Who it’s for</h2>
                  <CheckList items={p.forWho} />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-primary-dark mb-3">Prerequisites</h2>
                  <CheckList items={p.prerequisites} />
                </div>
              </div>
            </aside>
          </div>
        </div>
      </section>

      {/* ── Related ──────────────────────────────────────────────────────── */}
      <section className="py-20 bg-secondary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
              <h2 className="text-3xl md:text-4xl font-bold text-primary-dark">You might also like</h2>
              <Link href="/services/training#courses" className="text-primary font-semibold hover:text-primary-light">All courses →</Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {related.map((r) => <CourseCard key={r.id} p={r} featured={r.track === 'flagship'} />)}
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </main>
  )
}
