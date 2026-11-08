import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function NLPPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="💬"
        subtitle="Language Understanding"
        title="Natural Language Processing"
        description="Unlock NLP with sentiment analysis, chatbots, and multilingual AI—designed for accurate, inclusive, and bias-minimized communication."
        gradient="bg-gradient-to-br from-cyan-900 via-blue-800 to-teal-600"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Natural Language Processing Services
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Tap into the power of language with AI systems that understand, interpret, and respond like humans—only faster and smarter.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">📝</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Text Intelligence Solutions</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Automating classification, summarization, and sentiment analysis for efficient content processing.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">💬</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Conversational AI & QnA Systems</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Enabling real-time engagement through intelligent, context-aware chatbots and assistants.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🌍</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Multilingual AI & Accessibility</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Breaking barriers with translation, transcription, and inclusive NLP solutions built on ethical AI models.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['BERT', 'GPT', 'Transformers', 'spaCy', 'NLTK', 'Hugging Face', 'Word2Vec', 'FastText'].map((tech) => (
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
                Why Choose Our NLP Services?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">🎯</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">High Accuracy</h3>
                  <p className="text-secondary/80">State-of-the-art models</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🌐</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Multilingual</h3>
                  <p className="text-secondary/80">Support for 100+ languages</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">⚖️</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Bias-Free</h3>
                  <p className="text-secondary/80">Fair and inclusive AI</p>
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

