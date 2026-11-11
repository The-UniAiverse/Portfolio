import Link from 'next/link'
import { corporateTracks, levels, type Level } from '@/data/training.data'
import { tools } from '@/data/tools.data'

/** Two doors from the homepage: the training catalogue and the free AI tools. */
export default function Spotlight() {
  const shown = corporateTracks.slice(0, 5)
  return (
    <section className="py-24 bg-secondary-light">
      <div className="container mx-auto px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Link href="/services/training" className="group relative overflow-hidden rounded-3xl bg-deck p-8 md:p-12 text-secondary shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <div className="absolute -right-20 -bottom-20 w-72 h-72 rounded-full bg-purple-400/30 blur-3xl transition-transform duration-500 group-hover:scale-125" aria-hidden="true" />
            <div className="relative">
              <p className="kicker mb-3">Corporate AI training</p>
              <h2 className="text-3xl md:text-4xl font-bold mb-3">25 courses. 10 tracks. Every role.</h2>
              <p className="text-secondary/80 text-lg mb-8">From AI for every employee to agentic AI engineering, customised to your context before delivery.</p>
              <ul className="flex flex-wrap gap-2 mb-10">
                {shown.map((t) => (
                  <li key={t.id} className="bg-white/10 border border-secondary/20 text-sm px-3 py-1.5 rounded-full">{t.icon} {t.label}</li>
                ))}
                <li className="bg-white/10 border border-secondary/20 text-sm px-3 py-1.5 rounded-full">+{corporateTracks.length - shown.length + 1} more</li>
              </ul>
              <ol className="grid grid-cols-4 gap-2 mb-10" aria-label="Levels">
                {([1, 2, 3, 4] as Level[]).map((l) => (
                  <li key={l} className="rounded-xl bg-white/10 px-3 py-3" style={{ opacity: 0.55 + l * 0.11 }}>
                    <span className="block font-bold">{levels[l].short}</span>
                    <span className="block text-xs text-secondary/75">{levels[l].label}</span>
                  </li>
                ))}
              </ol>
              <span className="inline-block bg-amber-300 text-slate-900 px-7 py-3.5 rounded-full font-bold group-hover:bg-amber-200 transition-colors duration-300">
                Explore the catalogue →
              </span>
            </div>
          </Link>

          <Link href="/tools" className="group relative overflow-hidden rounded-3xl bg-primary-dark p-8 md:p-12 text-secondary shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <div className="absolute -right-20 -top-20 w-72 h-72 rounded-full bg-primary-light/25 blur-3xl transition-transform duration-500 group-hover:scale-125" aria-hidden="true" />
            <div className="relative">
              <p className="kicker mb-3">AI tools</p>
              <h2 className="text-3xl md:text-4xl font-bold mb-3">Try our AI tools</h2>
              <p className="text-secondary/80 text-lg mb-8">Free tools built on the same engine we use with clients. Sign in to run them.</p>
              <ul className="space-y-3 mb-10">
                {tools.map((t) => (
                  <li key={t.slug} className="flex items-center gap-3">
                    <span className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-xl shrink-0" aria-hidden="true">{t.icon}</span>
                    <span><span className="font-semibold block leading-tight">{t.title}</span><span className="text-sm text-secondary/60">{t.subtitle}</span></span>
                  </li>
                ))}
              </ul>
              <span className="inline-block bg-primary text-secondary px-7 py-3.5 rounded-full font-bold group-hover:bg-primary-light transition-colors duration-300">
                Open the tools →
              </span>
            </div>
          </Link>
        </div>
      </div>
    </section>
  )
}
