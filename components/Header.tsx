'use client'

import { useState, useRef } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { navLinks, serviceLinks } from '@/data/navigation.data'

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isServicesOpen, setIsServicesOpen] = useState(false)
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const handleMouseEnter = () => {
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current)
    }
    setIsServicesOpen(true)
  }

  const handleMouseLeave = () => {
    closeTimeoutRef.current = setTimeout(() => {
      setIsServicesOpen(false)
    }, 300) // 300ms delay before closing
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-primary-dark/95 backdrop-blur-sm border-b border-primary-light/20">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3">
            <Image
              src="/logo.png"
              alt="uniAiverse Logo"
              width={40}
              height={40}
              className="object-contain"
            />
            <div className="text-2xl font-bold">
              <span className="text-secondary">uni</span>
              <span className="text-primary-light">Ai</span>
              <span className="text-secondary">verse</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-secondary hover:text-primary-light transition-colors duration-300 font-medium"
              >
                {link.label}
              </Link>
            ))}

            {/* Services Dropdown */}
            <div
              className="relative"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              <button
                className="text-secondary hover:text-primary-light transition-colors duration-300 font-medium flex items-center space-x-1"
              >
                <span>Services</span>
                <svg
                  className={`w-4 h-4 transition-transform duration-300 ${isServicesOpen ? 'rotate-180' : ''}`}
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              {/* Dropdown Menu - 2 Column Layout */}
              {isServicesOpen && (
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-[680px] bg-primary-dark/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-primary-light/30 overflow-hidden animate-fade-in">
                  <div className="p-4">
                    <div className="grid grid-cols-2 gap-2">
                      {serviceLinks.map((service, index) => (
                        <Link
                          key={index}
                          href={service.href}
                          className="flex items-center space-x-3 px-4 py-3 hover:bg-primary/50 rounded-xl transition-all duration-300 group"
                          onClick={() => setIsServicesOpen(false)}
                        >
                          <span className="text-2xl group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                            {service.icon}
                          </span>
                          <span className="text-secondary text-sm font-medium group-hover:text-primary-light transition-colors duration-300">
                            {service.title}
                          </span>
                        </Link>
                      ))}
                    </div>
                    {/* View All Services Link */}
                    <div className="mt-3 pt-3 border-t border-primary-light/20">
                      <Link
                        href="/services"
                        className="flex items-center justify-center space-x-2 px-4 py-3 bg-primary hover:bg-primary-light rounded-xl transition-all duration-300 group"
                        onClick={() => setIsServicesOpen(false)}
                      >
                        <span className="text-secondary font-semibold">View All Services</span>
                        <svg
                          className="w-4 h-4 text-secondary group-hover:translate-x-1 transition-transform duration-300"
                          fill="none"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path d="M9 5l7 7-7 7"></path>
                        </svg>
                      </Link>
                    </div>
                  </div>
                </div>
              )}
            </div>



            <Link
              href="/#contact"
              className="bg-primary hover:bg-primary-light text-secondary px-6 py-2 rounded-full font-semibold transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50"
            >
              Get Started
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-secondary focus:outline-none"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMenuOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4">
            <div className="flex flex-col space-y-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-secondary hover:text-primary-light transition-colors duration-300 font-medium"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}

              {/* Mobile Services Dropdown */}
              <div>
                <button
                  onClick={() => setIsServicesOpen(!isServicesOpen)}
                  className="text-secondary hover:text-primary-light transition-colors duration-300 font-medium flex items-center space-x-1 w-full"
                >
                  <span>Services</span>
                  <svg
                    className={`w-4 h-4 transition-transform duration-300 ${isServicesOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>

                {isServicesOpen && (
                  <div className="mt-3 ml-4 space-y-2 bg-primary/30 rounded-xl p-3 max-h-96 overflow-y-auto">
                    {serviceLinks.map((service, index) => (
                      <Link
                        key={index}
                        href={service.href}
                        className="flex items-center space-x-2 text-secondary hover:text-primary-light transition-colors duration-300 py-2"
                        onClick={() => {
                          setIsMenuOpen(false)
                          setIsServicesOpen(false)
                        }}
                      >
                        <span className="text-xl">{service.icon}</span>
                        <span className="text-sm">{service.title}</span>
                      </Link>
                    ))}
                    {/* View All Services Link */}
                    <Link
                      href="/services"
                      className="flex items-center justify-center space-x-2 bg-primary hover:bg-primary-light rounded-lg py-3 mt-3 transition-all duration-300"
                      onClick={() => {
                        setIsMenuOpen(false)
                        setIsServicesOpen(false)
                      }}
                    >
                      <span className="text-secondary font-semibold text-sm">View All Services</span>
                      <svg
                        className="w-4 h-4 text-secondary"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path d="M9 5l7 7-7 7"></path>
                      </svg>
                    </Link>
                  </div>
                )}
              </div>

              <Link
                href="/#contact"
                className="bg-primary hover:bg-primary-light text-secondary px-6 py-2 rounded-full font-semibold transition-all duration-300 text-center"
                onClick={() => setIsMenuOpen(false)}
              >
                Get Started
              </Link>
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}

export default Header

