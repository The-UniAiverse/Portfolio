'use client'

import { useState } from 'react'
import { techCategories, filterCategories, techStackPageData } from '@/data/techstack.data'

const TechStack = () => {
  const [activeCategory, setActiveCategory] = useState('all')

  const filteredCategories =
    activeCategory === 'all'
      ? techCategories
      : techCategories.filter((cat) => cat.id === activeCategory)

  return (
    <section className="py-20 bg-secondary-light">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-primary-dark">
            {techStackPageData.heading.prefix}{' '}
            <span className="text-primary">{techStackPageData.heading.highlight}</span>
          </h2>
          <p className="text-lg text-primary-dark/70">
            {techStackPageData.subheading}
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {filterCategories.map((filter) => (
            <button
              key={filter.id}
              onClick={() => setActiveCategory(filter.id)}
              className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                activeCategory === filter.id
                  ? 'bg-primary text-secondary shadow-lg scale-105'
                  : 'bg-secondary text-primary-dark hover:bg-primary-light hover:text-secondary'
              }`}
            >
              {filter.label}
            </button>
          ))}
        </div>

        {/* Tech Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredCategories.map((category, index) => (
            <div
              key={index}
              className="bg-secondary p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-primary-light/20"
            >
              {/* Category Header */}
              <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-primary-light/20">
                <span className="text-4xl">{category.icon}</span>
                <h3 className="text-xl font-bold text-primary-dark">
                  {category.category}
                </h3>
              </div>

              {/* Tech Tags */}
              <div className="flex flex-wrap gap-2">
                {category.techs.map((tech, techIndex) => (
                  <span
                    key={techIndex}
                    className="px-4 py-2 bg-primary-dark/5 hover:bg-primary hover:text-secondary text-primary-dark rounded-lg text-sm font-medium transition-all duration-300 cursor-default hover:scale-105"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center bg-gradient-blue p-12 rounded-3xl shadow-2xl">
          <h3 className="text-3xl md:text-4xl font-bold text-secondary mb-4">
            {techStackPageData.cta.heading}
          </h3>
          <p className="text-xl text-secondary/90 mb-6">
            {techStackPageData.cta.subheading}
          </p>
          <a
            href={techStackPageData.cta.buttonHref}
            className="inline-block bg-secondary text-primary-dark px-10 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105"
          >
            {techStackPageData.cta.buttonText}
            <span className="inline-block ml-2">→</span>
          </a>
        </div>
      </div>
    </section>
  )
}

export default TechStack

