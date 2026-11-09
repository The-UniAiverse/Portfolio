import Link from 'next/link'
import type { Program } from '@/data/training.data'

/** Catalogue card linking to the course page. The flagship variant uses the brand gradient. */
export default function CourseCard({ p, featured = false }: { p: Program; featured?: boolean }) {
  return (
    <Link
      href={`/services/training/${p.id}`}
      className={`group relative flex flex-col rounded-2xl p-7 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl ${
        featured ? 'bg-gradient-blue text-secondary shadow-xl' : 'bg-secondary-light shadow-lg'
      }`}
    >
      <div className="flex items-start justify-between gap-3 mb-5">
        <span className="text-4xl transition-transform duration-300 group-hover:scale-110" aria-hidden="true">{p.icon}</span>
        {p.badge && (
          <span className={`text-xs font-bold px-3 py-1 rounded-full ${featured ? 'bg-secondary/20 text-secondary' : 'bg-primary text-secondary'}`}>{p.badge}</span>
        )}
      </div>
      <h3 className={`text-2xl font-bold mb-2 ${featured ? 'text-secondary' : 'text-primary-dark'}`}>{p.title}</h3>
      <p className={`leading-relaxed mb-6 flex-1 ${featured ? 'text-secondary/85' : 'text-primary-dark/70'}`}>{p.tagline}</p>
      <div className={`flex items-center justify-between gap-3 pt-5 border-t ${featured ? 'border-secondary/20' : 'border-primary/10'}`}>
        <span className={`text-sm font-medium ${featured ? 'text-secondary/75' : 'text-primary-dark/50'}`}>{p.level}</span>
        <span className={`shrink-0 whitespace-nowrap font-semibold ${featured ? 'text-secondary' : 'text-primary group-hover:text-primary-light'}`}>
          Explore <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
        </span>
      </div>
    </Link>
  )
}
