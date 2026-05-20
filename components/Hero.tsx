import Link from 'next/link'
import { heroData } from '@/data/hero.data'

const Hero = () => {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Video Background */}
      <div className="absolute inset-0 w-full h-full overflow-hidden">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover"
        >
          <source src={heroData.video.src} type={heroData.video.type} />
        </video>

        {/* Dark Overlay for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-dark/80 via-primary/70 to-primary-dark/80"></div>

        {/* Additional gradient for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-primary-dark/60 via-transparent to-transparent"></div>

        {/* Animated accent elements on top of video */}
        <div className="absolute inset-0 overflow-hidden">
          {/* Subtle floating particles */}
          <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-primary-lighter rounded-full opacity-40 animate-float"></div>
          <div className="absolute top-1/3 right-1/4 w-2 h-2 bg-primary-lighter rounded-full opacity-30 animate-float animation-delay-1000"></div>
          <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-primary-light rounded-full opacity-40 animate-float animation-delay-2000"></div>
          <div className="absolute bottom-1/3 right-1/3 w-3 h-3 bg-primary-lighter rounded-full opacity-35 animate-float animation-delay-3000"></div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-24 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center max-w-7xl mx-auto">
          {/* Left Side - Text Content */}
          <div className="space-y-8">
            {/* Badge */}
            <div className="inline-block animate-fade-in">
              <span className="bg-primary/80 text-secondary px-6 py-3 rounded-full text-sm font-semibold backdrop-blur-sm border border-primary-light/30 shadow-lg hover:scale-105 transition-transform duration-300 inline-block">
                {heroData.badge.emoji} {heroData.badge.text}
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
            <div className="space-y-3 bg-secondary/10 backdrop-blur-sm p-6 rounded-2xl border border-secondary/20">
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
                className="group bg-secondary text-primary-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-primary-lighter hover:text-secondary transition-all duration-300 hover:shadow-2xl hover:shadow-primary-light/50 hover:scale-105 text-center"
              >
                {heroData.cta.primary.text}
                <span className="inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300">
                  →
                </span>
              </Link>
              <Link
                href={heroData.cta.secondary.href}
                className="group bg-transparent border-2 border-secondary text-secondary px-8 py-4 rounded-full font-bold text-lg hover:bg-secondary hover:text-primary-dark transition-all duration-300 hover:shadow-2xl hover:shadow-secondary/50 hover:scale-105 text-center"
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
                <div key={index} className="bg-secondary/10 backdrop-blur-sm p-4 rounded-xl border border-secondary/20 hover:scale-105 transition-transform duration-300 hover:bg-secondary/20">
                  <p className="text-3xl md:text-4xl font-bold text-primary-lighter">{stat.value}</p>
                  <p className="text-xs md:text-sm text-secondary/80">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Side - Image Container with Corner Images */}
          <div className="relative hidden lg:flex items-center justify-center">
            <div className="relative group w-full">
              {/* Decorative background element */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary-light/20 to-accent-blue/20 rounded-3xl blur-2xl opacity-60 group-hover:opacity-80 transition-all duration-500"></div>

              {/* Main Central Image Container with Gradient Border */}
              <div className="relative bg-gradient-to-br from-primary-light/30 to-accent-blue/30 backdrop-blur-sm rounded-3xl p-1 shadow-2xl hover:shadow-primary-light/50 transition-all duration-500 hover:scale-[1.02] overflow-visible">

                {/* Inner container */}
                <div className="relative bg-primary-dark/40 rounded-3xl p-4 backdrop-blur-sm">
                  {/* Main Image Element */}
                  <div className="relative w-full h-[400px] rounded-2xl overflow-hidden">
                    <img
                      src={heroData.images.main}
                      alt="AI Technology"
                      className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
                    />

                    {/* Gradient overlay for better integration */}
                    <div className="absolute inset-0 bg-gradient-to-t from-primary-dark/60 via-transparent to-transparent"></div>

                    {/* Subtle overlay on hover */}
                    <div className="absolute inset-0 bg-gradient-to-br from-primary-light/10 to-accent-blue/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  </div>

                  {/* Top Right Corner Image */}
                  <div className="absolute -top-16 -right-16 w-64 h-64 animate-float">
                    <div className="relative group/corner">
                      <div className="absolute inset-0 bg-gradient-to-br from-primary-lighter/50 to-accent-blue/50 rounded-3xl blur-xl"></div>
                      <div className="relative bg-gradient-to-br from-primary-light/40 to-accent-blue/40 backdrop-blur-sm rounded-3xl p-1 shadow-2xl hover:shadow-primary-lighter/60 transition-all duration-500">
                        <div className="relative bg-primary-dark/60 rounded-3xl p-3 backdrop-blur-sm">
                          <div className="relative w-full h-full rounded-2xl overflow-hidden">
                            <img
                              src={heroData.images.topRight}
                              alt="AI Innovation"
                              className="w-full h-full object-cover transform group-hover/corner:scale-110 transition-transform duration-500"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Bottom Right Corner Image */}
                  <div className="absolute -bottom-16 -right-16 w-64 h-64 animate-float animation-delay-2000">
                    <div className="relative group/corner">
                      <div className="absolute inset-0 bg-gradient-to-br from-accent-blue/50 to-primary-lighter/50 rounded-3xl blur-xl"></div>
                      <div className="relative bg-gradient-to-br from-accent-blue/40 to-primary-light/40 backdrop-blur-sm rounded-3xl p-1 shadow-2xl hover:shadow-accent-blue/60 transition-all duration-500">
                        <div className="relative bg-primary-dark/60 rounded-3xl p-3 backdrop-blur-sm">
                          <div className="relative w-full h-full rounded-2xl overflow-hidden">
                            <img
                              src={heroData.images.bottomRight}
                              alt="Future of AI"
                              className="w-full h-full object-cover transform group-hover/corner:scale-110 transition-transform duration-500"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating particles around image */}
              <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary-lighter/30 rounded-full blur-2xl animate-pulse"></div>
              <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-accent-blue/30 rounded-full blur-2xl animate-pulse animation-delay-1000"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <Link href="#about" aria-label="Scroll down">
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

