import Link from 'next/link'

interface ServiceHeroProps {
  title: string
  subtitle: string
  description: string
  icon: string
  gradient: string
}

const ServiceHero = ({ title, subtitle, description, icon, gradient }: ServiceHeroProps) => {
  return (
    <section className={`relative min-h-[70vh] flex items-center justify-center overflow-hidden ${gradient}`}>
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Large Animated Orbs */}
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 left-20 w-80 h-80 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-4000"></div>
        
        {/* Floating Particles */}
        <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-white rounded-full opacity-60 animate-float"></div>
        <div className="absolute top-1/3 right-1/4 w-3 h-3 bg-white rounded-full opacity-50 animate-float animation-delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-white rounded-full opacity-70 animate-float animation-delay-2000"></div>
        
        {/* Grid Pattern Overlay */}
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:50px_50px]"></div>
        
        {/* Gradient Overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-primary-dark/60 via-transparent to-transparent"></div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-24 relative z-10">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Icon */}
          <div className="inline-block">
            <div className="text-8xl mb-6 animate-float">
              {icon}
            </div>
          </div>

          {/* Subtitle */}
          <div className="inline-block">
            <span className="bg-primary/80 text-secondary px-6 py-3 rounded-full text-sm font-semibold backdrop-blur-sm border border-primary-light/30 shadow-lg">
              {subtitle}
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-secondary leading-tight">
            {title}
          </h1>

          {/* Description */}
          <p className="text-xl md:text-2xl text-secondary/90 leading-relaxed max-w-3xl mx-auto">
            {description}
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Link
              href="#details"
              className="group bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-primary-light/50 hover:scale-105"
            >
              Learn More
              <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300">
                →
              </span>
            </Link>
            <Link
              href="#contact"
              className="group bg-transparent border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold text-lg hover:bg-secondary hover:text-primary-dark transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105"
            >
              Get Started
              <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300">
                →
              </span>
            </Link>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <a href="#details" aria-label="Scroll down">
          <svg
            className="w-6 h-6 text-secondary hover:text-primary-lighter transition-colors duration-300"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
          </svg>
        </a>
      </div>
    </section>
  )
}

export default ServiceHero

