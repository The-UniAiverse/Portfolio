import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function DataSciencePage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="📊"
        subtitle="Data-Driven Insights"
        title="Data Science"
        description="Turn data into insights with advanced analytics—achieve measurable outcomes and smarter decisions with fair, accountable AI solutions."
        gradient="bg-gradient-to-br from-green-900 via-emerald-800 to-teal-700"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Data Science Services
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Explore how our data science solutions transform data into clarity, foresight, and performance.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">📈</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Advanced Analytics & Forecasting</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Delivering actionable insights through predictive modeling, anomaly detection, and trend analysis.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🔄</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">End-to-End Data Pipelines</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Designing robust systems for data acquisition, transformation, modeling, and visualization.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">💡</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Insight-Driven Optimization</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Using data to refine operations, enhance customer experiences, and increase ROI across the board.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['Python', 'R', 'SQL', 'Pandas', 'NumPy', 'Matplotlib', 'Tableau', 'Power BI'].map((tech) => (
                  <span key={tech} className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why Data Science?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">💡</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Actionable Insights</h3>
                  <p className="text-secondary/80">Make informed decisions</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">📊</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Data-Driven</h3>
                  <p className="text-secondary/80">Evidence-based strategies</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🎯</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Measurable ROI</h3>
                  <p className="text-secondary/80">Track business impact</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </main>
  )
}

