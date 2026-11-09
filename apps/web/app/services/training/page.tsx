import type { Metadata } from 'next'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import ProgramExplorer from '@/components/training/ProgramExplorer'
import { faqs, learningSteps, mentorship, programById, programs } from '@/data/training.data'

export const metadata: Metadata = {
  title: 'Training & Mentorship | uniAiverse',
  description:
    'Mentor-led programs in AI Engineering, Generative AI, Agentic AI, Machine Learning & Deep Learning, Full Stack Development and DSA, plus AI for Everyone and corporate AI training.',
}

const ROADMAP = ['dsa', 'full-stack', 'ml-dl', 'ai-engineering', 'generative-ai', 'agentic-ai']

export default function TrainingPage() {
  const flagship = programById('ai-mastery')!
  return (
    <main className="min-h-screen">
      <Header />

      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600 pt-36 pb-24">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob" />
          <div className="absolute -top-20 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-60 animate-blob animation-delay-2000" />
          <div className="absolute -bottom-40 left-1/3 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-4000" />
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:48px_48px]" />
          <div className="absolute inset-0 bg-gradient-to-t from-primary-dark/60 via-transparent to-transparent" />
        </div>

        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            <span className="inline-block bg-primary/80 text-secondary px-6 py-2.5 rounded-full text-sm font-semibold backdrop-blur-sm border border-primary-light/30 shadow-lg mb-8">
              🎓 Training & Mentorship
            </span>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-secondary leading-tight mb-6">
              Learn to build AI the way{' '}
              <span className="bg-gradient-to-r from-cyan-300 via-blue-200 to-purple-300 bg-clip-text text-transparent">industry builds it</span>
            </h1>
            <p className="text-xl md:text-2xl text-secondary/85 leading-relaxed max-w-3xl mx-auto mb-10">
              Mentor-led programs from DSA and full stack to generative and agentic AI, plus AI for every business and team.
              Learn at your pace, build real projects and get reviewed by engineers who ship AI every day.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-14">
              <Link href="#programs" className="bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:scale-105">
                Explore programs →
              </Link>
              <Link href="#contact" className="border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold text-lg hover:bg-secondary hover:text-primary-dark transition-all duration-300 hover:scale-105">
                Talk to a mentor
              </Link>
            </div>

            {/* program chips */}
            <div className="flex flex-wrap justify-center gap-3">
              {programs.map((p) => (
                <Link key={p.id} href={`#program-${p.id}`}
                  className="bg-secondary/10 hover:bg-secondary/20 backdrop-blur-sm border border-secondary/20 text-secondary px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:-translate-y-0.5">
                  {p.icon} {p.title}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Highlights ───────────────────────────────────────────────────── */}
      <section className="bg-primary-dark border-b border-primary-light/20">
        <div className="container mx-auto px-6 py-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-5xl mx-auto text-center">
            {[
              { value: String(programs.length), label: 'Programs' },
              { value: '1:1', label: 'Mentorship' },
              { value: '100%', label: 'Project-based' },
              { value: 'Live', label: 'Sessions + labs' },
            ].map((s) => (
              <div key={s.label}>
                <div className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">{s.value}</div>
                <div className="text-secondary/60 text-sm font-semibold uppercase tracking-widest mt-2">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Programs + syllabus ──────────────────────────────────────────── */}
      <section id="programs" className="py-24 bg-secondary scroll-mt-20">
        <div className="container mx-auto px-6">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-14">
              <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-4">Choose your program</h2>
              <p className="text-xl text-primary-dark/70 max-w-3xl mx-auto">
                Six deep engineering tracks, one flagship program that combines them, and AI training for businesses and teams.
              </p>
            </div>
            <ProgramExplorer />
          </div>
        </div>
      </section>

      {/* ── Flagship roadmap ─────────────────────────────────────────────── */}
      <section className="py-24 bg-primary-dark relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.25),transparent_45%),radial-gradient(circle_at_80%_80%,rgba(168,85,247,0.2),transparent_45%)]" aria-hidden="true" />
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-14">
              <span className="inline-block bg-purple-500/20 text-purple-200 border border-purple-400/30 px-4 py-1.5 rounded-full text-sm font-bold mb-4">
                {flagship.icon} {flagship.badge}
              </span>
              <h2 className="text-4xl md:text-5xl font-bold text-secondary mb-4">{flagship.title}</h2>
              <p className="text-xl text-secondary/75 max-w-3xl mx-auto">{flagship.tagline} Six tracks and one mentor, in the order that makes each step easier.</p>
            </div>

            <div className="relative">
            <div className="hidden lg:block absolute top-8 left-[8%] right-[8%] h-0.5 bg-gradient-to-r from-blue-500 via-cyan-400 to-purple-500" aria-hidden="true" />
            <ol className="relative grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6">
              {ROADMAP.map((id, i) => {
                const p = programById(id)!
                return (
                  <li key={id} className="relative">
                    <Link href={`#program-${id}`} className="group block text-center">
                      <span className="relative z-10 mx-auto w-16 h-16 rounded-2xl bg-gradient-blue border border-primary-light/40 flex items-center justify-center text-3xl shadow-lg shadow-primary/30 transition-transform duration-300 group-hover:scale-110 group-hover:-translate-y-1">
                        {p.icon}
                      </span>
                      <span className="block text-xs font-bold text-primary-lighter uppercase tracking-widest mt-4">Stage {i + 1}</span>
                      <span className="block text-secondary font-semibold mt-1 group-hover:text-primary-lighter transition-colors">{p.title}</span>
                    </Link>
                  </li>
                )
              })}
            </ol>
            </div>

            <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6">
              {flagship.outcomes.slice(1).map((o) => (
                <div key={o} className="bg-secondary/5 border border-secondary/10 rounded-2xl p-6 text-secondary/85 backdrop-blur-sm">
                  <span className="text-primary-lighter text-xl mr-2">✓</span>{o}
                </div>
              ))}
            </div>
            <div className="text-center mt-10">
              <Link href="#program-ai-mastery" className="inline-block bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:scale-105">
                See the full AI Mastery syllabus →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── Mentorship ───────────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-14">
              <h2 className="text-4xl md:text-5xl font-bold text-primary-dark mb-4">Mentorship, not just lessons</h2>
              <p className="text-xl text-primary-dark/70 max-w-3xl mx-auto">Every program pairs structured learning with people who have done the work.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {mentorship.map((m) => (
                <div key={m.title} className="bg-secondary p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">{m.icon}</div>
                  <h3 className="text-xl font-bold text-primary-dark mb-3">{m.title}</h3>
                  <p className="text-primary-dark/70 leading-relaxed">{m.description}</p>
                </div>
              ))}
            </div>

            {/* how it works */}
            <ol className="mt-20 grid grid-cols-1 md:grid-cols-4 gap-6">
              {learningSteps.map((s, i) => (
                <li key={s.title} className="relative bg-gradient-blue rounded-2xl p-7 text-secondary shadow-xl">
                  <span className="text-5xl font-bold text-secondary/20 absolute top-4 right-5">{i + 1}</span>
                  <h3 className="text-xl font-bold mb-2">{s.title}</h3>
                  <p className="text-secondary/80">{s.description}</p>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </section>

      {/* ── Corporate ────────────────────────────────────────────────────── */}
      <section className="py-24 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-700 rounded-3xl p-10 md:p-16 shadow-2xl relative overflow-hidden">
            <div className="absolute -right-20 -top-20 w-80 h-80 bg-cyan-400/20 rounded-full blur-3xl" aria-hidden="true" />
            <div className="relative grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
              <div>
                <span className="inline-block bg-secondary/15 text-secondary px-4 py-1.5 rounded-full text-sm font-bold mb-5">🏢 For organisations</span>
                <h2 className="text-3xl md:text-5xl font-bold text-secondary mb-5">Upskill your whole company</h2>
                <p className="text-lg text-secondary/80 leading-relaxed mb-8">
                  Leadership strategy workshops, AI productivity for every employee, hands-on engineering tracks on your own stack
                  and an internal AI champions network, designed around your goals and measured on real adoption.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link href="#contact" className="text-center bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:scale-105">
                    Plan a corporate program →
                  </Link>
                  <Link href="/tools/readiness-audit" className="text-center border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold hover:bg-secondary hover:text-primary-dark transition-all duration-300">
                    Take the AI readiness audit
                  </Link>
                </div>
              </div>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {['Leadership AI strategy', 'AI for every employee', 'Engineering team tracks', 'AI champions program', 'On-site, virtual or hybrid', 'Built on your tools and data'].map((x) => (
                  <li key={x} className="bg-secondary/10 border border-secondary/15 rounded-2xl px-5 py-4 text-secondary font-semibold backdrop-blur-sm">
                    <span className="text-primary-lighter mr-2">✓</span>{x}
                  </li>
                ))}
              </ul>
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
                <details key={f.q} className="group bg-secondary rounded-2xl shadow-md open:shadow-lg transition-all">
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
