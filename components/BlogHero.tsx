const BlogHero = () => {
  return (
    <section className="relative min-h-[70vh] flex items-center justify-center overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-dark via-primary to-primary-light">
        {/* Animated mesh gradient overlay */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-0 -left-4 w-96 h-96 bg-primary-lighter rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
          <div className="absolute top-0 -right-4 w-96 h-96 bg-accent-blue rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-20 w-96 h-96 bg-primary-light rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
        </div>

        {/* Floating particles */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-secondary rounded-full opacity-60 animate-float"></div>
          <div className="absolute top-1/3 right-1/4 w-3 h-3 bg-secondary rounded-full opacity-40 animate-float animation-delay-1000"></div>
          <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-secondary rounded-full opacity-50 animate-float animation-delay-2000"></div>
          <div className="absolute bottom-1/3 right-1/3 w-3 h-3 bg-secondary rounded-full opacity-40 animate-float animation-delay-3000"></div>
          <div className="absolute top-1/2 left-1/2 w-2 h-2 bg-secondary rounded-full opacity-60 animate-float animation-delay-1500"></div>
        </div>

        {/* Grid pattern overlay */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)`,
            backgroundSize: '50px 50px'
          }}></div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 pt-32 pb-24 relative z-10">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-block animate-fade-in">
            <span className="bg-secondary/20 text-secondary px-6 py-3 rounded-full text-sm font-semibold backdrop-blur-sm border border-secondary/30 shadow-lg hover:scale-105 transition-transform duration-300 inline-block">
              📝 Insights & Innovation
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-secondary leading-tight">
            Explore the{' '}
            <span className="bg-gradient-to-r from-secondary via-primary-lighter to-secondary bg-clip-text text-transparent animate-pulse">
              Future of AI
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-secondary/90 leading-relaxed max-w-3xl mx-auto">
            Dive into cutting-edge AI trends, expert insights, and real-world case studies 
            that are shaping the future of technology and business.
          </p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-6 pt-8 max-w-2xl mx-auto">
            <div className="bg-secondary/10 backdrop-blur-sm p-6 rounded-2xl border border-secondary/20 hover:scale-105 transition-transform duration-300">
              <p className="text-3xl md:text-4xl font-bold text-secondary">50+</p>
              <p className="text-sm text-secondary/80">Articles</p>
            </div>
            <div className="bg-secondary/10 backdrop-blur-sm p-6 rounded-2xl border border-secondary/20 hover:scale-105 transition-transform duration-300">
              <p className="text-3xl md:text-4xl font-bold text-secondary">10K+</p>
              <p className="text-sm text-secondary/80">Readers</p>
            </div>
            <div className="bg-secondary/10 backdrop-blur-sm p-6 rounded-2xl border border-secondary/20 hover:scale-105 transition-transform duration-300">
              <p className="text-3xl md:text-4xl font-bold text-secondary">Weekly</p>
              <p className="text-sm text-secondary/80">Updates</p>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
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
      </div>
    </section>
  )
}

export default BlogHero

