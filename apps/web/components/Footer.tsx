import Link from 'next/link'
import Image from 'next/image'
import { footerServices, footerCompany, footerSocialLinks, footerAddress } from '@/data/footer.data'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-primary-dark text-secondary">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3 mb-2">
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
            </div>
            <p className="text-secondary/80 text-sm leading-relaxed">
              {footerAddress.line1}<br />
              {footerAddress.line2}<br />
              {footerAddress.line3}<br />
              {footerAddress.line4}
            </p>
            <p className="text-primary-light font-semibold">
              {footerAddress.phone}
            </p>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-lg font-bold mb-4 text-primary-light">Services</h3>
            <ul className="space-y-2">
              {footerServices.map((service) => (
                <li key={service}>
                  <Link
                    href="#services"
                    className="text-secondary/80 hover:text-primary-light transition-colors duration-300 text-sm"
                  >
                    {service}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-lg font-bold mb-4 text-primary-light">Company</h3>
            <ul className="space-y-2">
              {footerCompany.map((item) => (
                <li key={item}>
                  <Link
                    href="#"
                    className="text-secondary/80 hover:text-primary-light transition-colors duration-300 text-sm"
                  >
                    {item}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h3 className="text-lg font-bold mb-4 text-primary-light">Connect With Us</h3>
            <div className="flex space-x-4">
              {footerSocialLinks.map((social) => (
                <Link
                  key={social.name}
                  href={social.href}
                  className="w-10 h-10 bg-primary hover:bg-primary-light text-secondary rounded-full flex items-center justify-center font-bold text-xs transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50"
                  aria-label={social.name}
                >
                  {social.icon}
                </Link>
              ))}
            </div>
            <div className="mt-6">
              <Link
                href="#contact"
                className="inline-block bg-primary hover:bg-primary-light text-secondary px-6 py-3 rounded-full font-semibold transition-all duration-300 hover:shadow-lg hover:shadow-primary-light/50"
              >
                Get in Touch
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-primary-light/20">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-2">
              <Image 
                src="/logo.png" 
                alt="uniAiverse Logo" 
                width={24} 
                height={24}
                className="object-contain"
              />
              <p className="text-secondary/70 text-sm">
                © {currentYear} uniAiverse. All rights reserved.
              </p>
            </div>
            <div className="flex space-x-6">
              <Link
                href="#"
                className="text-secondary/70 hover:text-primary-light text-sm transition-colors duration-300"
              >
                Privacy Policy
              </Link>
              <Link
                href="#"
                className="text-secondary/70 hover:text-primary-light text-sm transition-colors duration-300"
              >
                Terms of Service
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

