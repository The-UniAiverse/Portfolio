import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function TrainingPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="📚"
        subtitle="AI Education & Upskilling"
        title="Training and Workshops"
        description="Build AI fluency through interactive workshops—tailored to professionals for real-world innovation and confident tech leadership."
        gradient="bg-gradient-to-br from-amber-900 via-yellow-800 to-orange-700"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Training and Workshops
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Equip your teams with the skills and mindset to innovate, adapt, and lead in an AI-driven world.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">💻</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Hands-On Technical Workshops</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Delivering real-world training in ML, NLP, CV, and generative AI with expert-led sessions.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">💼</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Business-Focused AI Programs</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Enabling non-technical teams to understand, evaluate, and apply AI strategically.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">⚖️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Ethics & Responsible AI Training</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Fostering a culture of trust, safety, and accountability in every AI initiative.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Topics We Cover
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision', 'MLOps', 'Python', 'TensorFlow', 'PyTorch'].map((tech) => (
                  <span key={tech} className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why Our Training?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">👨‍💼</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Industry Experts</h3>
                  <p className="text-secondary/80">Learn from the best</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">💼</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Real-World Projects</h3>
                  <p className="text-secondary/80">Practical experience</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">📜</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Certification</h3>
                  <p className="text-secondary/80">Recognized credentials</p>
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

