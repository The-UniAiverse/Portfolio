import { aboutData } from '@/data/about.data'

const About = () => {

  return (
    <section id="about" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        {/* Main Purpose Section */}
        <div className="max-w-4xl mx-auto text-center mb-20 space-y-6">
          <h2 className="text-4xl md:text-5xl font-bold text-primary-dark">
            {aboutData.purpose.heading}
          </h2>
          <div className="h-1 w-24 bg-primary mx-auto rounded-full"></div>
          <p className="text-lg md:text-xl text-primary-dark/80 leading-relaxed">
            {aboutData.purpose.description}
          </p>

          {/* Core Principles */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12">
            {aboutData.purpose.corePrinciples.map((principle, index) => (
              <div key={index} className="flex items-center justify-center space-x-2 text-primary-dark/80">
                <span className="text-xl">✓</span>
                <span className="font-medium">
                  {principle}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Company Identity */}
        <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl mb-20">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h3 className="text-3xl md:text-4xl font-bold text-secondary">
              {aboutData.identity.heading}
            </h3>
            <p className="text-xl text-secondary/90 leading-relaxed">
              {aboutData.identity.description}
            </p>
            <p className="text-2xl font-bold text-primary-lighter">
              {aboutData.identity.tagline}
            </p>
            <div className="text-4xl font-bold">
              <span className="text-secondary">{aboutData.identity.brandName.prefix}</span>
              {aboutData.identity.brandName.parts.map((part, index) => (
                <span key={index} className={`text-${part.color}`}>{part.text}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Vision, Mission, Drive Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {aboutData.principles.map((principle, index) => (
            <div
              key={index}
              className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-2 border-primary-light/20 hover:border-primary"
            >
              <div className="text-5xl mb-4">{principle.icon}</div>
              <h4 className="text-2xl font-bold text-primary mb-4">
                {principle.title}
              </h4>
              <p className="text-primary-dark/70 leading-relaxed">
                {principle.description}
              </p>
            </div>
          ))}
        </div>

        {/* What Sets Us Apart */}
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl md:text-4xl font-bold text-primary-dark text-center mb-12">
            What Sets Us Apart
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {aboutData.differentiators.map((item, index) => (
              <div
                key={index}
                className="bg-secondary-light p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 hover:-translate-y-1 text-center"
              >
                <div className="text-4xl mb-3">{item.icon}</div>
                <h4 className="text-lg font-bold text-primary-dark mb-2">
                  {item.title}
                </h4>
                <p className="text-sm text-primary-dark/70">{item.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Achievements */}
        <div className="mt-20 bg-primary-dark/5 p-8 rounded-2xl">
          <h3 className="text-2xl md:text-3xl font-bold text-primary-dark text-center mb-8">
            {aboutData.achievements.heading}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {aboutData.achievements.items.map((item, index) => (
              <div key={index} className="flex items-start space-x-3">
                <span className="text-primary text-2xl">✓</span>
                <span className="text-primary-dark/80 font-medium">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default About

