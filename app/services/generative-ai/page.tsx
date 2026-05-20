import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function GenerativeAIPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="🎨"
        subtitle="Creative AI Solutions"
        title="Generative AI Development"
        description="Deliver custom Generative AI for content, images, and dynamic UX—enhancing creativity, control, and brand trust with powerful models."
        gradient="bg-gradient-to-br from-purple-900 via-blue-800 to-blue-600"
      />

      {/* Service Details */}
      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            {/* Main Service Description */}
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Generative AI Development Services
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Unleash creativity and intelligence with generative AI systems that simulate, synthesize, and innovate responsibly.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🎨</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Generative Model Development</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Building advanced models like GANs, VAEs, and Diffusion for imagery, data, and beyond.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🔄</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Synthetic Data & Personalization</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Producing high-quality data and content that adapts to user behavior and preferences.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🛡️</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Responsible Content Generation</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Embedding ethical guardrails and transparency in every generative application.
                  </p>
                </div>
              </div>
            </div>

            {/* Technologies We Use */}
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['GPT-4', 'DALL-E', 'Stable Diffusion', 'Midjourney', 'Claude', 'LangChain', 'HuggingFace', 'OpenAI API'].map((tech) => (
                  <span
                    key={tech}
                    className="bg-primary text-secondary px-6 py-3 rounded-full font-semibold hover:bg-primary-light transition-all duration-300 hover:scale-110 cursor-default"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            {/* Benefits */}
            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h2 className="text-4xl font-bold text-secondary mb-8 text-center">
                Why Choose Our Generative AI Services?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">⚡</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Fast Deployment</h3>
                  <p className="text-secondary/80">Rapid implementation and integration</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🎯</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Custom Solutions</h3>
                  <p className="text-secondary/80">Tailored to your business needs</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🔒</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Secure & Scalable</h3>
                  <p className="text-secondary/80">Enterprise-grade security and scalability</p>
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

