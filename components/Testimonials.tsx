import { testimonialsPageData } from '@/data/testimonials.data'
import pool from '@/lib/db'

interface Testimonial {
  id: number
  quote: string
  author: string
  role: string
  company: string
  avatar: string
  rating: number
}

async function getTestimonials(): Promise<Testimonial[]> {
  try {
    const [rows] = await pool.execute('SELECT * FROM testimonials ORDER BY created_at ASC')
    return rows as Testimonial[]
  } catch {
    return []
  }
}

const Testimonials = async () => {
  const testimonialsData = await getTestimonials()

  return (
    <section className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-primary-dark">
            {testimonialsPageData.heading.prefix}{' '}
            <span className="text-primary">{testimonialsPageData.heading.highlight}</span>
          </h2>
          <p className="text-lg text-primary-dark/70">
            {testimonialsPageData.subheading}
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonialsData.map((testimonial, index) => (
            <div
              key={index}
              className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-primary-light/20 hover:border-primary relative"
            >
              {/* Quote Icon */}
              <div className="absolute -top-4 -left-4 text-6xl text-primary/20">
                "
              </div>

              {/* Rating Stars */}
              <div className="flex space-x-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <svg
                    key={i}
                    className="w-5 h-5 text-primary"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>

              {/* Quote */}
              <p className="text-primary-dark/80 italic leading-relaxed mb-6 relative z-10">
                {testimonial.quote}
              </p>

              {/* Author Info */}
              <div className="flex items-center space-x-4 pt-6 border-t border-primary-light/20">
                <div className="text-4xl">{testimonial.avatar}</div>
                <div>
                  <h4 className="font-bold text-primary-dark">
                    {testimonial.author}
                  </h4>
                  <p className="text-sm text-primary-dark/70">
                    {testimonial.role}
                  </p>
                  <p className="text-xs text-primary font-semibold">
                    {testimonial.company}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats Section */}
        <div className="mt-20 bg-gradient-blue p-12 rounded-3xl shadow-2xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {testimonialsPageData.stats.map((stat, index) => (
              <div key={index} className="text-center">
                <p className="text-5xl font-bold text-secondary mb-2">{stat.value}</p>
                <p className="text-secondary/80">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default Testimonials

