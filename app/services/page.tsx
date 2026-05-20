import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'
import { serviceCategories, servicesPageData } from '@/data/services.data'
import pool from '@/lib/db'

export const metadata: Metadata = {
  title: 'AI Services - Strategy, Automation & Custom Solutions | uniAiverse',
  description: 'Comprehensive AI services including strategy & roadmap, automation, chatbots, LLM integrations, data analytics, RAG systems, MLOps, and enterprise solutions.',
  keywords: 'AI strategy, AI automation, AI chatbots, LLM integration, RAG systems, MLOps, AI consulting, enterprise AI',
}

// Always fetch fresh from DB on every request
export const revalidate = 0

interface DbService {
  id: number
  title: string
  description: string
  icon: string
  category: string
  category_icon: string
  whats_included: string
  use_cases: string
  deliverables: string
  capabilities: string
  examples: string
  ideal_for: string
  powered_by: string
  tools: string
  duration: string
  is_active: number
  sort_order: number
}

interface ServiceForDisplay {
  title: string
  description: string
  icon: string
  whatsIncluded?: string[]
  useCases?: string[]
  deliverables?: string
  capabilities?: string[]
  examples?: string[]
  idealFor?: string
  poweredBy?: string
  tools?: string
  duration?: string
}

interface CategoryForDisplay {
  categoryTitle: string
  categoryIcon: string
  services: ServiceForDisplay[]
}

function parseJson(val: string | null | undefined): string[] {
  if (!val) return []
  try {
    const parsed = JSON.parse(val)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

async function getActiveServicesGrouped(): Promise<CategoryForDisplay[]> {
  try {
    const [rows] = await pool.execute(
      'SELECT * FROM services WHERE is_active = 1 ORDER BY sort_order ASC, category ASC, id ASC'
    )
    const services = rows as DbService[]

    if (!services.length) return []

    // Group by category, preserving order of first appearance
    const categoryMap = new Map<string, CategoryForDisplay>()

    for (const svc of services) {
      if (!categoryMap.has(svc.category)) {
        categoryMap.set(svc.category, {
          categoryTitle: svc.category,
          categoryIcon: svc.category_icon,
          services: [],
        })
      }
      categoryMap.get(svc.category)!.services.push({
        title: svc.title,
        description: svc.description,
        icon: svc.icon,
        whatsIncluded: parseJson(svc.whats_included),
        useCases: parseJson(svc.use_cases),
        capabilities: parseJson(svc.capabilities),
        examples: parseJson(svc.examples),
        deliverables: svc.deliverables || undefined,
        idealFor: svc.ideal_for || undefined,
        poweredBy: svc.powered_by || undefined,
        tools: svc.tools || undefined,
        duration: svc.duration || undefined,
      })
    }

    return Array.from(categoryMap.values())
  } catch {
    // Fallback to static data if DB is unavailable
    return serviceCategories.map((cat) => ({
      categoryTitle: cat.categoryTitle,
      categoryIcon: cat.categoryIcon,
      services: cat.services.map((svc) => ({
        title: svc.title,
        description: svc.description,
        icon: svc.icon,
        whatsIncluded: svc.whatsIncluded,
        useCases: svc.useCases,
        capabilities: svc.capabilities,
        examples: svc.examples,
        deliverables: Array.isArray(svc.deliverables) ? svc.deliverables.join(', ') : svc.deliverables,
        idealFor: svc.idealFor,
        poweredBy: svc.poweredBy,
        tools: svc.tools,
        duration: svc.duration,
      })),
    }))
  }
}

export default async function ServicesPage() {
  const categories = await getActiveServicesGrouped()

  return (
    <main className="min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-blue py-32 pt-40 overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary-lighter rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary rounded-full blur-3xl"></div>
        </div>
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="text-center max-w-4xl mx-auto space-y-6">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-secondary leading-tight">
              {servicesPageData.heading.prefix}{' '}
              <span className="text-primary-lighter">{servicesPageData.heading.highlight}</span>
            </h1>
            <p className="text-xl md:text-2xl text-secondary/90 leading-relaxed">
              {servicesPageData.subheading}
            </p>
            <div className="pt-6">
              <a
                href="#services"
                className="inline-block bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105"
              >
                Explore Services
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Service Categories */}
      <section id="services" className="py-20 bg-secondary-light">
        <div className="container mx-auto px-6">
          {categories.length === 0 ? (
            <div className="text-center py-20 text-primary-dark/50">
              <p className="text-xl">No services available at the moment. Please check back soon.</p>
            </div>
          ) : (
            categories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="mb-24 last:mb-0">
                {/* Category Title */}
                <div className="text-center mb-12">
                  <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-primary-dark mb-4">
                    {category.categoryTitle}
                  </h2>
                  <div className="h-1 w-24 bg-primary mx-auto rounded-full"></div>
                </div>

                {/* Services Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                  {category.services.map((service, index) => (
                    <div
                      key={index}
                      className="group bg-secondary p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-primary-light/20 hover:border-primary"
                    >
                      {/* Icon and Duration */}
                      <div className="flex justify-between items-start mb-4">
                        <div className="text-5xl group-hover:scale-110 transition-transform duration-300">
                          {service.icon}
                        </div>
                        {service.duration && (
                          <span className="text-xs font-semibold text-primary bg-primary/10 px-3 py-1 rounded-full">
                            {service.duration}
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h3 className="text-xl font-bold text-primary-dark mb-3 group-hover:text-primary transition-colors duration-300">
                        {service.title}
                      </h3>

                      {/* Description */}
                      <p className="text-primary-dark/70 leading-relaxed text-sm mb-4">
                        {service.description}
                      </p>

                      {/* What's Included */}
                      {service.whatsIncluded && service.whatsIncluded.length > 0 && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">What&apos;s included:</p>
                          <ul className="text-sm text-primary-dark/70 space-y-1">
                            {service.whatsIncluded.map((item, i) => (
                              <li key={i} className="flex items-start">
                                <span className="text-primary mr-2">•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Use Cases */}
                      {service.useCases && service.useCases.length > 0 && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Use cases:</p>
                          <ul className="text-sm text-primary-dark/70 space-y-1">
                            {service.useCases.map((item, i) => (
                              <li key={i} className="flex items-start">
                                <span className="text-primary mr-2">•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Capabilities */}
                      {service.capabilities && service.capabilities.length > 0 && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Capabilities:</p>
                          <ul className="text-sm text-primary-dark/70 space-y-1">
                            {service.capabilities.map((item, i) => (
                              <li key={i} className="flex items-start">
                                <span className="text-primary mr-2">•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Examples */}
                      {service.examples && service.examples.length > 0 && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Examples:</p>
                          <ul className="text-sm text-primary-dark/70 space-y-1">
                            {service.examples.map((item, i) => (
                              <li key={i} className="flex items-start">
                                <span className="text-primary mr-2">•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Deliverables */}
                      {service.deliverables && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Deliverables:</p>
                          <p className="text-sm text-primary-dark/70">{service.deliverables}</p>
                        </div>
                      )}

                      {/* Powered By */}
                      {service.poweredBy && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Powered by:</p>
                          <p className="text-sm text-primary-dark/70">{service.poweredBy}</p>
                        </div>
                      )}

                      {/* Tools */}
                      {service.tools && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Tools:</p>
                          <p className="text-sm text-primary-dark/70">{service.tools}</p>
                        </div>
                      )}

                      {/* Ideal For */}
                      {service.idealFor && (
                        <div className="mb-4">
                          <p className="text-xs font-semibold text-primary mb-2">Ideal for:</p>
                          <p className="text-sm text-primary-dark/70 italic">{service.idealFor}</p>
                        </div>
                      )}

                      {/* Get Started Link */}
                      <div className="mt-6 pt-4 border-t border-primary-light/20">
                        <a
                          href="#contact"
                          className="inline-flex items-center text-primary font-semibold group-hover:text-primary-light transition-colors duration-300"
                        >
                          Get Started
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
              </div>
            ))
          )}

          {/* Why Work With Us */}
          <div className="mb-16 max-w-7xl mx-auto">
            <div className="bg-secondary p-10 rounded-2xl shadow-lg border border-primary-light/20">
              <h3 className="text-3xl font-bold text-primary-dark mb-8 text-center">
                {servicesPageData.whyWorkWithUs.title}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                {servicesPageData.whyWorkWithUs.benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="flex-shrink-0 w-2 h-2 bg-primary rounded-full"></div>
                    <p className="text-primary-dark/80 font-medium">{benefit}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center max-w-4xl mx-auto">
            <div className="bg-gradient-blue p-12 rounded-3xl shadow-2xl">
              <h3 className="text-3xl md:text-4xl font-bold text-secondary mb-4">
                {servicesPageData.cta.heading}
              </h3>
              <p className="text-secondary/90 text-lg mb-6">
                Let&apos;s discuss how we can help you achieve your goals
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

      {/* Contact Section */}
      <Contact />
      
      {/* Footer */}
      <Footer />
    </main>
  )
}
