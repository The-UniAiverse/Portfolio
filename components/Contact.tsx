'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { contactServices, contactInfo as staticContactInfo, contactPageData } from '@/data/contact.data'

interface ContactInfoItem {
  id?: number
  icon: string
  title: string
  details: string[] | string
  link?: string | null
}

function parseDetails(val: string[] | string | null | undefined): string[] {
  if (!val) return []
  if (Array.isArray(val)) return val
  try { return JSON.parse(val) } catch { return [String(val)] }
}

const Contact = () => {
  const [contactInfo, setContactInfo] = useState<ContactInfoItem[]>(staticContactInfo)

  useEffect(() => {
    fetch('/api/contact-info')
      .then((r) => r.json())
      .then((json) => { if (json.success && json.data?.length) setContactInfo(json.data) })
      .catch(() => {})
  }, [])

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    service: '',
    message: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const res = await fetch('/api/admin/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data = await res.json()
      if (data.success) {
        setSubmitted(true)
        setFormData({ name: '', email: '', phone: '', company: '', service: '', message: '' })
        setTimeout(() => setSubmitted(false), 5000)
      } else {
        setError('Something went wrong. Please try again.')
      }
    } catch {
      setError('Network error. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }



  return (
    <section id="contact" className="py-20 bg-secondary-light">
      <div className="container mx-auto px-6">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-primary-dark">
            {contactPageData.heading.prefix}{' '}
            <span className="text-primary">{contactPageData.heading.highlight}</span>
          </h2>
          <p className="text-lg text-primary-dark/70">
            {contactPageData.subheading}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <div className="bg-secondary p-8 rounded-2xl shadow-lg">
            <h3 className="text-2xl font-bold text-primary-dark mb-6">
              Send us a Message
            </h3>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    htmlFor="name"
                    className="block text-sm font-semibold text-primary-dark mb-2"
                  >
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300"
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-semibold text-primary-dark mb-2"
                  >
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300"
                    placeholder="john@example.com"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    htmlFor="phone"
                    className="block text-sm font-semibold text-primary-dark mb-2"
                  >
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300"
                    placeholder="+91 1234567890"
                  />
                </div>
                <div>
                  <label
                    htmlFor="company"
                    className="block text-sm font-semibold text-primary-dark mb-2"
                  >
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300"
                    placeholder="Your Company"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="service"
                  className="block text-sm font-semibold text-primary-dark mb-2"
                >
                  Service Interested In *
                </label>
                <select
                  id="service"
                  name="service"
                  value={formData.service}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300"
                >
                  <option value="">Select a service</option>
                  {contactServices.map((service, index) => (
                    <option key={index} value={service}>
                      {service}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label
                  htmlFor="message"
                  className="block text-sm font-semibold text-primary-dark mb-2"
                >
                  Message *
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="w-full px-4 py-3 rounded-lg border border-primary-light/30 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all duration-300 resize-none"
                  placeholder="Tell us about your project and how we can help..."
                ></textarea>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {submitted && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm flex items-center space-x-2">
                  <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Thank you! Your message has been received. We&apos;ll get back to you soon.</span>
                </div>
              )}

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-primary hover:bg-primary-light disabled:opacity-70 disabled:cursor-not-allowed text-secondary px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 hover:shadow-2xl hover:shadow-primary/50 hover:scale-105 flex items-center justify-center space-x-2"
              >
                {submitting ? (
                  <>
                    <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    <span>Sending...</span>
                  </>
                ) : (
                  <>
                    <span>Send Message</span>
                    <span>→</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Contact Information */}
          <div className="space-y-8">
            <div className="bg-gradient-blue p-8 rounded-2xl shadow-lg text-secondary">
              <h3 className="text-2xl font-bold mb-6">Contact Information</h3>
              <div className="space-y-6">
                {contactInfo.map((info, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="text-3xl">{info.icon}</div>
                    <div>
                      <h4 className="font-bold text-lg mb-2">{info.title}</h4>
                      {info.link ? (
                        <a
                          href={info.link}
                          className="text-secondary/90 hover:text-primary-lighter transition-colors duration-300"
                        >
                          {parseDetails(info.details)[0]}
                        </a>
                      ) : (
                        parseDetails(info.details).map((detail, i) => (
                          <p key={i} className="text-secondary/90 text-sm">
                            {detail}
                          </p>
                        ))
                      )}
                    </div>
                  </div>
                ))}
              </div>


            </div>

            {/* Why Choose Us */}
            <div className="bg-secondary p-8 rounded-2xl shadow-lg">
              <h3 className="text-2xl font-bold text-primary-dark mb-6">
                Why Choose uniAiverse?
              </h3>
              <ul className="space-y-4">
                {contactPageData.whyChooseUs.map((item, index) => (
                  <li key={index} className="flex items-start space-x-3">
                    <span className="text-primary text-xl mt-1">✓</span>
                    <span className="text-primary-dark/80">
                      <strong className="text-primary-dark">{item.title}:</strong>{' '}
                      {item.description}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Social Links */}
            <div className="bg-secondary p-8 rounded-2xl shadow-lg">
              <h3 className="text-2xl font-bold text-primary-dark mb-6">
                Follow Us
              </h3>
              <div className="flex space-x-4">
                {contactPageData.socialLinks.map((social, index) => (
                  <a
                    key={index}
                    href={social.href}
                    className="w-12 h-12 bg-primary hover:bg-primary-light text-secondary rounded-full flex items-center justify-center font-bold transition-all duration-300 hover:shadow-lg hover:shadow-primary/50 hover:scale-110"
                  >
                    {social.icon}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Contact

