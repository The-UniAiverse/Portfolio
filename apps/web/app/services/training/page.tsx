import type { Metadata } from 'next'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import CourseCard from '@/components/training/CourseCard'
import CourseFinder from '@/components/training/CourseFinder'
import { faqs, mentorship, programs, tracks } from '@/data/training.data'

export const metadata: Metadata = {
  title: 'Training & Mentorship | uniAiverse',
  description:
    'Mentor-led courses in AI Engineering, Generative AI, Agentic AI, Machine Learning & Deep Learning, Full Stack Development and DSA, plus AI for Everyone and corporate AI training.',
}

export default function TrainingPage() {
  return (
    <main className="min-h-screen">
      <Header />

      {/* ── Hero: short, so the courses are the first thing people see ─────── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600 pt-36 pb-20">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob" />
          <div className="absolute -top-20 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob animation-delay-2000" />
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:48px_48px]" />
        </div>
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <span className="inline-block bg-primary/80 text-secondary px-6 py-2.5 rounded-full text-sm font-semibold backdrop-blur-sm border border-primary-light/30 shadow-lg mb-8">
              🎓 Training & Mentorship
            </span>
            <h1 className="text-4xl md:text-6xl font-bold text-secondary leading-tight mb-6">
              Courses that take you from{' '}
              <span className="bg-gradient-to-r from-cyan-300 via-blue-200 to-purple-300 bg-clip-text text-transparent">learning to building</span>
            </h1>
            <p className="text-xl text-secondary/85 leading-relaxed max-w-2xl mx-auto mb-10">
              Mentor-led, project-first courses in AI, software engineering and AI for business, for individuals and whole teams.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#courses" className="bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:scale-105">
                Browse courses ↓
              </Link>
              <CourseFinder label="Not sure? Find your course" variant="outline" />
            </div>
          </div>
        </div>
      </section>

      {/* ── Course catalogue ─────────────────────────────────────────────── */}
      <section id="courses" className="py-20 bg-secondary scroll-mt-20">
        <div className="container mx-auto px-6">
          <div className="max-w-7xl mx-auto space-y-20">
            {tracks.map((t) => {
              const list = programs.filter((p) => p.track === t.id)
              const flagship = t.id === 'flagship'
              return (
                <div key={t.id}>
                  <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-2 mb-8">
                    <div>
                      <h2 className="text-3xl md:text-4xl font-bold text-primary-dark">{t.label}</h2>
                      <p className="text-lg text-primary-dark/60 mt-1">{t.description}</p>
                    </div>
                    <span className="text-primary-dark/40 font-semibold">{list.length} {list.length === 1 ? 'course' : 'courses'}</span>
                  </div>
                  {flagship ? (
                    <div className="grid grid-cols-1">
                      {list.map((p) => <CourseCard key={p.id} p={p} featured />)}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                      {list.map((p) => <CourseCard key={p.id} p={p} />)}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* ── Course finder banner ─────────────────────────────────────────── */}
      <section className="pb-24 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-5xl mx-auto bg-primary-dark rounded-3xl p-10 md:p-14 text-center relative overflow-hidden shadow-2xl">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_20%,rgba(59,130,246,0.35),transparent_45%),radial-gradient(circle_at_85%_80%,rgba(168,85,247,0.3),transparent_45%)]" aria-hidden="true" />
            <div className="relative">
              <div className="text-5xl mb-4" aria-hidden="true">🧭</div>
              <h2 className="text-3xl md:text-4xl font-bold text-secondary mb-3">Still confused about where to start?</h2>
              <p className="text-lg text-secondary/75 max-w-2xl mx-auto mb-8">
                Answer three quick questions and we’ll recommend the course that fits your background and goals.
              </p>
              <CourseFinder label="Try our course finder" variant="light" />
            </div>
          </div>
        </div>
      </section>

      {/* ── Every course includes ────────────────────────────────────────── */}
      <section className="py-24 bg-secondary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-4 text-center">Every course includes</h2>
            <p className="text-xl text-primary-dark/70 max-w-2xl mx-auto mb-14 text-center">Structured learning, paired with people who have done the work.</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {mentorship.map((m) => (
                <div key={m.title} className="flex gap-4 bg-secondary p-6 rounded-2xl shadow-md">
                  <span className="text-3xl shrink-0" aria-hidden="true">{m.icon}</span>
                  <div>
                    <h3 className="font-bold text-primary-dark mb-1">{m.title}</h3>
                    <p className="text-sm text-primary-dark/70 leading-relaxed">{m.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Corporate ────────────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-700 rounded-3xl p-10 md:p-14 shadow-2xl grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-10 items-center">
            <div>
              <span className="inline-block bg-secondary/15 text-secondary px-4 py-1.5 rounded-full text-sm font-bold mb-5">🏢 For organisations</span>
              <h2 className="text-3xl md:text-4xl font-bold text-secondary mb-4">Training a team or the whole company?</h2>
              <p className="text-lg text-secondary/80 leading-relaxed">
                We tailor any of these courses to your stack, data and goals, from leadership strategy to hands-on engineering and AI for every employee.
              </p>
            </div>
            <div className="flex flex-col gap-3">
              <Link href="/services/training/corporate" className="text-center bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:scale-105">
                See corporate training →
              </Link>
              <Link href="#contact" className="text-center border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold hover:bg-secondary hover:text-primary-dark transition-all duration-300">
                Plan a program with us
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── FAQ ──────────────────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-12 text-center">Questions, answered</h2>
            <div className="space-y-4">
              {faqs.map((f) => (
                <details key={f.q} className="group bg-secondary rounded-2xl shadow-md">
                  <summary className="flex items-center justify-between gap-4 cursor-pointer list-none p-6 font-semibold text-primary-dark">
                    {f.q}
                    <span className="text-primary text-2xl transition-transform duration-300 group-open:rotate-45" aria-hidden="true">+</span>
                  </summary>
                  <p className="px-6 pb-6 text-primary-dark/75 leading-relaxed">{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </main>
  )
}
