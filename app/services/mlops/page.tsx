import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function MLOpsPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="🚀"
        subtitle="ML Lifecycle Management"
        title="MLOps & Deployment"
        description="Streamline ML lifecycle with robust MLOps—automate deployment, monitoring, and scaling for reliable, production-ready AI systems."
        gradient="bg-gradient-to-br from-orange-900 via-red-800 to-pink-700"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                MLOps Services
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">⚙️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">CI/CD for ML</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Automated pipelines for continuous integration and deployment of ML models.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">📊</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Model Monitoring</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Track model performance, data drift, and system health in production.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">📦</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Model Versioning</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Manage and track different versions of models for reproducibility.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">☁️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Cloud Deployment</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Deploy ML models on AWS, Azure, GCP with auto-scaling capabilities.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['Docker', 'Kubernetes', 'MLflow', 'Kubeflow', 'Azure ML', 'SageMaker', 'GitHub Actions', 'Jenkins'].map((tech) => (
                  <span key={tech} className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why MLOps?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">⚡</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Faster Deployment</h3>
                  <p className="text-secondary/80">Reduce time-to-production</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🔄</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Automation</h3>
                  <p className="text-secondary/80">Streamlined workflows</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">📈</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Scalability</h3>
                  <p className="text-secondary/80">Handle growing demands</p>
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

