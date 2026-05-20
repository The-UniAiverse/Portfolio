import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function ComputerVisionPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="👁️"
        subtitle="Visual Intelligence"
        title="Computer Vision"
        description="Enable AI to interpret visuals—build Computer Vision systems for detection, recognition, and automation that enhance safety and user experience."
        gradient="bg-gradient-to-br from-violet-900 via-purple-800 to-fuchsia-700"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Computer Vision Services
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Leverage the power of sight with AI-powered visual systems that automate, detect, and analyze with unmatched precision.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">👁️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Visual Recognition & Detection</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Implementing cutting-edge object detection, facial recognition, and segmentation models.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">⚙️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Operational Automation with Vision</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Enabling real-time surveillance, quality control, and inventory tracking using smart cameras.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🛡️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">AI-Powered Compliance & Safety</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Ensuring safety and regulatory standards through automated visual inspections and anomaly detection.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['OpenCV', 'YOLO', 'TensorFlow', 'PyTorch', 'ResNet', 'CNN', 'Mask R-CNN', 'Vision Transformers'].map((tech) => (
                  <span key={tech} className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why Computer Vision?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">🎯</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">High Accuracy</h3>
                  <p className="text-secondary/80">Precision detection</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">⚡</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Real-Time</h3>
                  <p className="text-secondary/80">Instant processing</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🔒</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Secure</h3>
                  <p className="text-secondary/80">Privacy-focused solutions</p>
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

