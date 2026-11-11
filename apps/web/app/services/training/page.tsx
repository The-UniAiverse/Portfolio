import type { Metadata } from 'next'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import CourseFinder from '@/components/training/CourseFinder'
import WorkshopDeck from '@/components/training/WorkshopDeck'
import {
  brochure, corporateTracks, individualTrack, levels, WORKSHOP_COURSE_ID, workshop,
  type Course, type Level,
} from '@/data/training.data'

export const metadata: Metadata = {
  title: 'Corporate AI Training | uniAiverse',
  description:
    'Corporate AI Training Catalogue: 25 courses in 10 tracks, from AI for every employee to GenAI and agentic AI engineering, MLOps and AI governance. Onsite in Pune or virtual.',
}

const levelStyle: Record<Level, string> = {
  1: 'bg-sky-400/15 text-sky-300',
  2: 'bg-blue-400/15 text-blue-300',
  3: 'bg-indigo-400/15 text-indigo-300',
  4: 'bg-purple-400/15 text-purple-300',
}

function LevelPill({ level }: { level: Level }) {
  return (
    <span className={`inline-flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full whitespace-nowrap ${levelStyle[level]}`}>
      {levels[level].short}<span className="font-semibold opacity-80">{levels[level].label}</span>
    </span>
  )
}

function CourseRow({ c }: { c: Course }) {
  return (
    <li id={`course-${c.id}`}
      className="scroll-mt-40 group flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6 px-5 py-4 rounded-2xl transition-colors duration-300 hover:bg-primary/5 target:bg-primary/10 target:ring-2 target:ring-primary-light">
      <div className="sm:w-36 shrink-0"><LevelPill level={c.level} /></div>
      <div className="flex-1 min-w-0">
        <p className="font-bold text-primary-dark text-lg leading-snug">{c.title}</p>
        {c.detail && <p className="text-sm text-primary-dark/60">{c.detail}</p>}
      </div>
      <div className="flex items-center gap-4 sm:justify-end shrink-0">
        {c.id === WORKSHOP_COURSE_ID && (
          <Link href="#workshop" className="text-sm font-semibold text-primary hover:text-primary-light whitespace-nowrap">Preview the deck ↓</Link>
        )}
        <span className="font-mono font-semibold text-primary-dark/70 whitespace-nowrap">{c.duration}</span>
      </div>
    </li>
  )
}

export default function TrainingPage() {
  const cohort = individualTrack.courses[0]
  return (
    <main className="min-h-screen">
      <Header />

      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden bg-deck pt-36 pb-20">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob" />
          <div className="absolute -top-20 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob animation-delay-2000" />
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:48px_48px]" />
        </div>
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            <span className="kicker inline-block mb-8">
              {brochure.title}
            </span>
            <h1 className="text-4xl md:text-6xl font-bold text-secondary leading-tight mb-6">
              AI training for{' '}
              <span className="bg-gradient-to-r from-cyan-300 via-blue-200 to-purple-300 bg-clip-text text-transparent">every role in your company</span>
            </h1>
            <p className="text-xl text-secondary/85 leading-relaxed max-w-3xl mx-auto mb-3">{brochure.intro}</p>
            <p className="text-secondary/70 max-w-3xl mx-auto mb-10">{brochure.aiModes}</p>

            <dl className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-3xl mx-auto mb-10">
              {[['25', 'courses'], ['10', 'tracks'], ['L1–L4', 'levels'], ['Onsite', 'Pune or virtual']].map(([v, l]) => (
                <div key={l} className="bg-white/10 backdrop-blur-sm border border-secondary/20 rounded-2xl py-4">
                  <dt className="sr-only">{l}</dt>
                  <dd className="text-3xl font-bold text-secondary">{v}</dd>
                  <dd className="text-sm text-secondary/70">{l}</dd>
                </div>
              ))}
            </dl>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10">
              <Link href="#courses" className="bg-amber-300 text-slate-900 px-8 py-4 rounded-full font-bold text-lg hover:bg-amber-200 transition-all duration-300 hover:shadow-2xl hover:scale-105">
                Browse the catalogue ↓
              </Link>
              <CourseFinder label="Not sure? Find your course" variant="outline" />
            </div>

            <ul className="flex flex-wrap justify-center gap-2">
              {brochure.chips.map((c) => (
                <li key={c.text} className="bg-white/10 border border-secondary/20 text-secondary/90 text-sm px-4 py-2 rounded-full">
                  <span aria-hidden="true">{c.icon}</span> {c.text}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* ── Catalogue ────────────────────────────────────────────────────── */}
      <section id="courses" className="bg-secondary scroll-mt-20">
        {/* track jump bar */}
        <div className="sticky top-[72px] z-30 bg-secondary-light/85 backdrop-blur border-b border-white/10">
          <nav aria-label="Tracks" className="container mx-auto px-6">
            <ul className="flex gap-2 overflow-x-auto no-scrollbar py-3 max-w-7xl mx-auto">
              {[...corporateTracks, individualTrack].map((t) => (
                <li key={t.id} className="shrink-0">
                  <a href={`#track-${t.id}`} className="block text-sm font-semibold text-primary-dark/70 bg-secondary-light hover:bg-primary hover:text-secondary px-4 py-2 rounded-full transition-colors duration-200 whitespace-nowrap">
                    <span aria-hidden="true">{t.icon}</span> {t.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        <div className="container mx-auto px-6 py-20">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-12">
              <div>
                <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-3">The catalogue</h2>
                <p className="text-lg text-primary-dark/60 max-w-2xl">{brochure.legend}</p>
              </div>
              <div className="flex flex-wrap gap-2" aria-label="Levels">
                {([1, 2, 3, 4] as Level[]).map((l) => <LevelPill key={l} level={l} />)}
              </div>
            </div>

            <div className="space-y-6">
              {corporateTracks.map((t) => (
                <article key={t.id} id={`track-${t.id}`}
                  className="scroll-mt-40 grid grid-cols-1 lg:grid-cols-[300px_minmax(0,1fr)] gap-4 lg:gap-8 bg-secondary-light rounded-3xl p-6 md:p-8 shadow-sm hover:shadow-lg transition-shadow duration-300">
                  <header>
                    <span className="text-4xl" aria-hidden="true">{t.icon}</span>
                    <h3 className="text-2xl font-bold text-primary-dark mt-3">{t.label}</h3>
                    <p className="text-primary-dark/60 mt-1">{t.audience}</p>
                    <p className="text-sm font-semibold text-primary mt-3">{t.courses.length} {t.courses.length === 1 ? 'course' : 'courses'}</p>
                  </header>
                  <ul className="bg-secondary rounded-2xl divide-y divide-primary/5 p-1 self-start">
                    {t.courses.map((c) => <CourseRow key={c.id} c={c} />)}
                  </ul>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Individual professionals ─────────────────────────────────────── */}
      <section id={`track-${individualTrack.id}`} className="pb-24 bg-secondary scroll-mt-40">
        <div className="container mx-auto px-6">
          <div id={`course-${cohort.id}`}
            className="max-w-7xl mx-auto bg-gradient-blue rounded-3xl p-8 md:p-14 shadow-2xl relative overflow-hidden scroll-mt-40 target:ring-4 target:ring-primary-lighter">
            <div className="absolute -right-24 -top-24 w-80 h-80 rounded-full bg-primary-lighter/30 blur-3xl" aria-hidden="true" />
            <div className="relative grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-10 items-center">
              <div>
                <span className="inline-block bg-white/15 text-secondary px-4 py-1.5 rounded-full text-sm font-bold mb-5">
                  {individualTrack.icon} {individualTrack.label} · {individualTrack.audience}
                </span>
                <h2 className="text-3xl md:text-5xl font-bold text-secondary mb-4">{cohort.title}</h2>
                <p className="text-xl text-secondary/85 mb-6">{cohort.detail}</p>
                <div className="flex flex-wrap gap-3">
                  <span className="bg-amber-300 text-slate-900 font-bold px-4 py-2 rounded-full">{levels[cohort.level].short} {levels[cohort.level].label}</span>
                  <span className="bg-white/15 text-secondary font-mono font-semibold px-4 py-2 rounded-full">{cohort.duration}</span>
                </div>
              </div>
              <div className="flex flex-col gap-3">
                <Link href="#contact" className="text-center bg-amber-300 text-slate-900 px-8 py-4 rounded-full font-bold hover:bg-amber-200 transition-all duration-300 hover:scale-105">
                  Join the next cohort →
                </Link>
                <CourseFinder label="Compare with other courses" variant="outline" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Workshop preview ─────────────────────────────────────────────── */}
      <section id="workshop" className="py-24 bg-slate-950 scroll-mt-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(251,191,36,0.08),transparent_55%)]" aria-hidden="true" />
        <div className="container mx-auto px-6 relative">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-10">
              <div>
                <p className="font-mono text-sm uppercase tracking-[0.25em] text-amber-300 mb-3">Workshop preview · slides 1–5 of {workshop.totalSlides}</p>
                <h2 className="text-4xl md:text-5xl font-bold text-white">{workshop.title}</h2>
                <p className="text-lg text-white/65 mt-3 max-w-2xl">Step through the opening of the deck. The full workshop runs 1 or 2 days, onsite or virtual.</p>
              </div>
              <Link href="#contact" className="self-start lg:self-auto border border-amber-300/60 text-amber-200 px-6 py-3 rounded-full font-semibold hover:bg-amber-300 hover:text-slate-900 transition-all duration-300">
                Book the workshop
              </Link>
            </div>
            <WorkshopDeck />
          </div>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-4 text-center">How it works</h2>
            <p className="text-xl text-primary-dark/70 max-w-2xl mx-auto mb-14 text-center">{brochure.legend.split('; ')[1]}</p>
            <ol className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              {brochure.process.map((p, i) => (
                <li key={p.title} className="relative bg-secondary rounded-2xl p-7 shadow-md">
                  <span className="font-mono text-sm font-bold text-primary">0{i + 1}</span>
                  <h3 className="text-2xl font-bold text-primary-dark mt-2 mb-2">{p.title}</h3>
                  <p className="text-primary-dark/70 leading-relaxed">{p.description}</p>
                </li>
              ))}
            </ol>

            <div className="bg-primary-dark rounded-3xl p-8 md:p-12 grid grid-cols-1 lg:grid-cols-[2fr_3fr] gap-8 items-center">
              <div>
                <h3 className="text-3xl font-bold text-secondary mb-3">Every course ships as a delivery kit</h3>
                <p className="text-secondary/70">{brochure.aiModes}</p>
              </div>
              <ul className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {brochure.kit.map((k) => (
                  <li key={k.text} className="bg-white/5 border border-secondary/10 rounded-2xl p-4 text-secondary">
                    <span className="text-2xl block mb-2" aria-hidden="true">{k.icon}</span>
                    <span className="font-semibold text-sm">{k.text}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ── Finder + booking ─────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-5xl mx-auto bg-deck rounded-3xl p-10 md:p-14 text-center relative overflow-hidden shadow-2xl">
            <div className="text-5xl mb-4" aria-hidden="true">🧭</div>
            <h2 className="text-3xl md:text-4xl font-bold text-secondary mb-3">{brochure.cta}</h2>
            <p className="text-lg text-secondary/75 max-w-2xl mx-auto mb-8">
              Not sure which one? Answer two questions and we’ll point you to the right course, or write to{' '}
              <a href={`mailto:${brochure.email}`} className="underline underline-offset-4 hover:text-secondary">{brochure.email}</a>.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <CourseFinder label="Try our course finder" variant="light" />
              <Link href="#contact" className="border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold text-lg hover:bg-white/10 hover:border-white/60 transition-all duration-300">
                Talk to us
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </main>
  )
}
