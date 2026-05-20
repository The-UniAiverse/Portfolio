import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function AIMLPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="🤖"
        subtitle="Intelligent Automation"
        title="Artificial Intelligence & Machine Learning"
        description="Build ROI-driven AI/ML to automate decisions and optimize operations—scalable, predictive, and rooted in Responsible AI for transparency."
        gradient="bg-gradient-to-br from-blue-900 via-indigo-800 to-blue-600"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Artificial Intelligence and Machine Learning Services
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Explore our comprehensive AI development services, crafted to automate processes, uncover insights, and scale innovation responsibly.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🤖</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">AI Development & Deployment</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Delivering custom AI models built to solve real business problems with precision and scale.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🎯</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">LLM Fine-Tuning & Solutions</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Creating optimized language models and RAG systems for enterprise needs.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">⚖️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Responsible AI Implementation</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Integrating fairness, transparency, and compliance into AI pipelines for responsible and future-ready outcomes.
                  </p>
                </div>
              </div>
            </div>

            {/* Case Studies/Projects */}
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Featured AI & ML Projects
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">📈</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Predictive Analytics</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Forecast trends, customer behavior, and business outcomes with advanced predictive models.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🎯</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Recommendation Systems</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Personalized recommendations to enhance user experience and drive engagement.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🔍</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Anomaly Detection</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Identify unusual patterns and outliers in data for fraud detection and quality control.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">⚙️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Process Automation</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Automate repetitive tasks and optimize workflows with intelligent automation.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'XGBoost', 'Random Forest', 'Neural Networks', 'Deep Learning'].map((tech) => (
                  <span
                    key={tech}
                    className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why Choose Our AI & ML Services?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">💰</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">ROI Driven</h3>
                  <p className="text-secondary/80">Measurable business impact</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">📊</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Data-Driven Insights</h3>
                  <p className="text-secondary/80">Make informed decisions</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🚀</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Scalable Solutions</h3>
                  <p className="text-secondary/80">Grow with your business</p>
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

