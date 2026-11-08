import type { ReactNode } from 'react'
import Header from '@/components/Header'
import ServiceHero from '@/components/ServiceHero'
import Footer from '@/components/Footer'
import Contact from '@/components/Contact'

interface ToolPageProps {
  icon: string
  subtitle: string
  title: string
  description: string
  gradient: string
  children: ReactNode
}

/** Page shell for the AI tools, matching the layout of the service pages. */
export default function ToolPage({ icon, subtitle, title, description, gradient, children }: ToolPageProps) {
  return (
    <main className="min-h-screen">
      <Header />
      <ServiceHero icon={icon} subtitle={subtitle} title={title} description={description} gradient={gradient} />
      <section id="details" className="py-20 bg-secondary scroll-mt-20">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">{children}</div>
        </div>
      </section>
      <Contact />
      <Footer />
    </main>
  )
}
