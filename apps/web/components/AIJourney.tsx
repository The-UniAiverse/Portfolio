import { aiJourneyPhases, aiJourneyPageData } from '@/data/aijourney.data'

const AIJourney = () => {

  return (
    <section className="py-20 bg-gradient-blue">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-secondary">
            {aiJourneyPageData.heading.prefix}{' '}
            <span className="text-primary-lighter">{aiJourneyPageData.heading.highlight}</span>
          </h2>
          <p className="text-lg text-secondary/80">
            {aiJourneyPageData.subheading}
          </p>
        </div>

        {/* Journey Timeline */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
          {/* Connection Line (Desktop) */}
          <div className="hidden lg:block absolute top-24 left-0 right-0 h-1 bg-primary-lighter/30">
            <div className="absolute inset-0 bg-gradient-to-r from-primary via-primary-light to-primary-lighter animate-pulse"></div>
          </div>

          {aiJourneyPhases.map((phase, index) => (
            <div key={index} className="relative">
              {/* Phase Card */}
              <div className="bg-secondary p-8 rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-300 hover:-translate-y-2 border-2 border-primary-light/30 hover:border-primary-lighter relative z-10">
                {/* Phase Number */}
                <div
                  className={`absolute -top-6 -right-6 w-16 h-16 bg-gradient-to-br ${phase.color} rounded-full flex items-center justify-center text-secondary font-bold text-xl shadow-lg`}
                >
                  {phase.phase}
                </div>

                {/* Icon */}
                <div className="text-6xl mb-6">{phase.icon}</div>

                {/* Title */}
                <h3 className="text-2xl font-bold text-primary-dark mb-3">
                  {phase.title}
                </h3>

                {/* Description */}
                <p className="text-primary-dark/70 leading-relaxed">
                  {phase.description}
                </p>

                {/* Progress Indicator */}
                <div className="mt-6 pt-6 border-t border-primary-light/20">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-primary font-semibold">Phase {phase.phase}</span>
                    <div className="flex space-x-1">
                      {[...Array(4)].map((_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full ${
                            i <= index ? 'bg-primary' : 'bg-primary-light/30'
                          }`}
                        ></div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Arrow (Mobile) */}
              {index < aiJourneyPhases.length - 1 && (
                <div className="lg:hidden flex justify-center py-4">
                  <svg
                    className="w-6 h-6 text-primary-lighter animate-bounce"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <p className="text-xl text-secondary/90 mb-6">
            {aiJourneyPageData.cta.text}
          </p>
          <a
            href={aiJourneyPageData.cta.buttonHref}
            className="inline-block bg-secondary text-primary-dark px-10 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105"
          >
            {aiJourneyPageData.cta.buttonText}
            <span className="inline-block ml-2">→</span>
          </a>
        </div>
      </div>
    </section>
  )
}

export default AIJourney

