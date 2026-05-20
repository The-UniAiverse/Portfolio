import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

export default function AgenticAIPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon="🧠"
        subtitle="Autonomous Intelligence"
        title="Agentic AI & Context-Aware Systems"
        description="Deploy autonomous, context-aware AI agents that reason, adapt, and act—driving safe, responsible, outcome-based transformation."
        gradient="bg-gradient-to-br from-indigo-900 via-purple-800 to-blue-700"
      />

      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Agentic AI & Context-Aware Systems
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                Deploy next-gen agentic systems that handle complex business workflows with contextual awareness and autonomy.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🤖</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Autonomous AI Agent Development</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Creating self-operating agents capable of executing multi-step business tasks.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🔄</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">MCP-Based Workflow Orchestration</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Coordinating agent behavior through a Model Context Protocol for seamless collaboration.
                  </p>
                </div>
                <div className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                  <div className="text-4xl mb-4">🧠</div>
                  <h3 className="text-2xl font-bold text-primary-dark mb-4">Scalable, Memory-Retaining Systems</h3>
                  <p className="text-primary-dark/70 leading-relaxed">
                    Enabling agents with context recall, personalization, and multi-modal reasoning.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies We Use
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {['LangChain', 'AutoGPT', 'ReAct', 'Reinforcement Learning', 'Multi-Agent Systems', 'LangGraph', 'CrewAI', 'AgentGPT'].map((tech) => (
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
                Why Agentic AI?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-5xl mb-4">🤖</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Autonomous</h3>
                  <p className="text-secondary/80">Self-directed decision making</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🔄</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Adaptive</h3>
                  <p className="text-secondary/80">Learns and improves over time</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🛡️</div>
                  <h3 className="text-xl font-bold text-secondary mb-2">Responsible</h3>
                  <p className="text-secondary/80">Safe and ethical AI practices</p>
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

