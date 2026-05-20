import { coreServices, servicesPageData } from '@/data/services.data'

const Services = () => {

  return (
    <section id="services" className="py-20 bg-secondary-light">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-primary-dark">
            🚀 Our Core Services
          </h2>
          <p className="text-lg text-primary-dark/70">
            From strategy to deployment, we deliver AI solutions that drive real business value
          </p>
        </div>

        {/* Services Grid - Clean & Simple */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {coreServices.map((service, index) => (
            <div
              key={index}
              className="group bg-secondary p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-primary-light/20 hover:border-primary"
            >
              {/* Icon */}
              <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">
                {service.icon}
              </div>

              {/* Title */}
              <h3 className="text-xl font-bold text-primary-dark mb-3 group-hover:text-primary transition-colors duration-300">
                {service.title}
              </h3>

              {/* Description */}
              <p className="text-primary-dark/70 leading-relaxed text-sm mb-6">
                {service.description}
              </p>

              {/* Learn More Link */}
              <div className="mt-auto">
                <a
                  href="#contact"
                  className="inline-flex items-center text-primary font-semibold group-hover:text-primary-light transition-colors duration-300"
                >
                  Learn More
                  <svg
                    className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M9 5l7 7-7 7"></path>
                  </svg>
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Services Teaser */}
        <div className="mt-16 text-center space-y-6">
          <div className="inline-flex flex-wrap justify-center items-center gap-6 md:gap-8 bg-secondary px-8 py-6 rounded-2xl shadow-lg border border-primary-light/20">
            <div className="flex items-center gap-3">
              <span className="text-2xl">⚡</span>
              <span className="text-primary-dark/80 font-medium">Advanced Services</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🏢</span>
              <span className="text-primary-dark/80 font-medium">Enterprise Solutions</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🎁</span>
              <span className="text-primary-dark/80 font-medium">Productized Packages</span>
            </div>
          </div>
          <a
            href="/services"
            className="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-light transition-colors duration-300 group"
          >
            View All Services
            <svg
              className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M9 5l7 7-7 7"></path>
            </svg>
          </a>
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
            <h3 className="text-3xl md:text-4xl font-bold text-secondary mb-4">
              Ready to transform your business with AI?
            </h3>
            <p className="text-secondary/90 text-lg mb-6">
              Let's discuss how we can help you achieve your goals
            </p>
            <a
              href={servicesPageData.cta.buttonHref}
              className="inline-block bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105"
            >
              {servicesPageData.cta.buttonText}
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Services

