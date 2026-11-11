import { aboutData } from '@/data/about.data'

/** Compact "about" block for the homepage (anchor #about is used by the header nav). */
export default function WhyUs() {
  const { purpose, identity, differentiators } = aboutData
  return (
    <section id="about" className="py-24 bg-secondary scroll-mt-20">
      <div className="container mx-auto px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[2fr_3fr] gap-12 items-center">
          <div>
            <p className="kicker mb-3">Why uniAiverse</p>
            <h2 className="text-4xl md:text-5xl font-bold text-primary-dark leading-tight mb-5">{identity.tagline}</h2>
            <p className="text-lg text-primary-dark/70 leading-relaxed mb-6">{purpose.description}</p>
            <ul className="space-y-3">
              {purpose.corePrinciples.map((p) => (
                <li key={p} className="flex items-start gap-3 text-primary-dark/80">
                  <span className="mt-1 w-5 h-5 rounded-full bg-primary text-secondary text-xs flex items-center justify-center shrink-0" aria-hidden="true">✓</span>{p}
                </li>
              ))}
            </ul>
          </div>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {differentiators.map((d, i) => (
              <li key={d.title} className={`rounded-3xl p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${i === 0 ? 'bg-gradient-blue text-secondary' : 'bg-secondary-light'}`}>
                <span className="text-4xl block mb-4" aria-hidden="true">{d.icon}</span>
                <h3 className={`text-xl font-bold mb-2 ${i === 0 ? 'text-secondary' : 'text-primary-dark'}`}>{d.title}</h3>
                <p className={i === 0 ? 'text-secondary/80' : 'text-primary-dark/70'}>{d.description}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
