import Link from 'next/link'
import { heroData } from '@/data/hero.data'
import NeuralField from '@/components/home/NeuralField'
import PillarConsole from '@/components/home/PillarConsole'

const Hero = () => {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Live network backdrop */}
      <div className="absolute inset-0 bg-deck">
        <NeuralField className="absolute inset-0 w-full h-full" />
        {/* keep the text side calm and readable */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#050816]/80 via-[#050816]/30 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#050816] to-transparent" />
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-24 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center max-w-7xl mx-auto">
          {/* Left Side - Text Content */}
          <div className="space-y-8">
            {/* Badge */}
            <div className="inline-block animate-fade-in">
              <span className="kicker">
                {heroData.badge.text}
              </span>
            </div>

            {/* Main Heading */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold text-secondary leading-tight">
              {heroData.heading.prefix}{' '}
              <span className="text-primary-lighter bg-gradient-to-r from-primary-lighter to-primary-light bg-clip-text text-transparent">
                {heroData.heading.highlight}
              </span>{' '}
              {heroData.heading.suffix}
            </h1>

            {/* Subheading */}
            <p className="text-lg md:text-xl text-secondary/90 leading-relaxed">
              {heroData.subheading}
            </p>

            {/* Tagline */}
            <div className="space-y-3 bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-secondary/20">
              <p className="text-2xl md:text-3xl font-bold text-primary-lighter">
                {heroData.tagline.main}
              </p>
              <p className="text-base text-secondary/80">
                {heroData.tagline.sub}
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link
                href={heroData.cta.primary.href}
                className="group bg-amber-300 text-slate-900 px-8 py-4 rounded-full font-bold text-lg hover:bg-amber-200 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-300/30 hover:scale-105 text-center"
              >
                {heroData.cta.primary.text}
                <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300">
                  →
                </span>
              </Link>
              <Link
                href={heroData.cta.secondary.href}
                className="group bg-transparent border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold text-lg hover:bg-white/10 hover:border-white/60 transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105 text-center"
              >
                {heroData.cta.secondary.text}
                <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300">
                  →
                </span>
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8">
              {heroData.stats.map((stat, index) => (
                <div key={index} className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-secondary/20 hover:scale-105 transition-transform duration-300 hover:bg-white/20">
                  <p className="text-3xl md:text-4xl font-bold text-primary-lighter">{stat.value}</p>
                  <p className="text-xs md:text-sm text-secondary/80">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Side - the four core pillars */}
          <PillarConsole />
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <Link href="#services" aria-label="Scroll down">
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
        </Link>
      </div>
    </section>
  )
}

export default Hero

