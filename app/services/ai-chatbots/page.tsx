import type { Metadata } from 'next'
import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import { getServiceBySlug } from '@/data/service-pages.data'

const serviceData = getServiceBySlug('ai-chatbots')!

export const metadata: Metadata = {
  title: `${serviceData.title} | uniAiverse`,
  description: serviceData.description,
}

export default function AIChatbotsPage() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <ServiceHero
        icon={serviceData.icon}
        subtitle={serviceData.subtitle}
        title={serviceData.title}
        description={serviceData.description}
        gradient={serviceData.gradient}
      />

      {/* Service Details */}
      <section id="details" className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            {/* Main Service Description */}
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                {serviceData.title}
              </h2>
              <p className="text-xl text-primary-dark/80 text-center max-w-4xl mx-auto mb-12">
                {serviceData.mainDescription}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {serviceData.features.map((feature, index) => (
                  <div key={index} className="bg-secondary-light p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                    <div className="text-4xl mb-4">{feature.icon}</div>
                    <h3 className="text-2xl font-bold text-primary-dark mb-4">{feature.title}</h3>
                    <p className="text-primary-dark/70 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Deliverables */}
            {serviceData.deliverables && (
              <div className="mb-16">
                <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                  What You'll Get
                </h2>
                <div className="bg-secondary-light p-10 rounded-2xl shadow-lg max-w-3xl mx-auto">
                  <ul className="space-y-4">
                    {serviceData.deliverables.map((item, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-primary text-2xl mr-4">✓</span>
                        <span className="text-lg text-primary-dark/80">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Technologies We Use */}
            <div className="mb-16">
              <h2 className="text-4xl font-bold text-primary-dark mb-8 text-center">
                Technologies & Platforms
              </h2>
              <div className="flex flex-wrap gap-4 justify-center">
                {serviceData.technologies.map((tech) => (
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
                Why Choose This Service?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {serviceData.benefits.map((benefit, index) => (
                  <div key={index} className="text-center">
                    <div className="text-5xl mb-4">{benefit.icon}</div>
                    <h3 className="text-xl font-bold text-secondary mb-2">{benefit.title}</h3>
                    <p className="text-secondary/80">{benefit.description}</p>
                  </div>
                ))}
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

