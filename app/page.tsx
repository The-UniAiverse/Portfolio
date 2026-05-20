import Header from '@/components/Header'
import Hero from '@/components/Hero'
import About from '@/components/About'
import Services from '@/components/Services'
import AIJourney from '@/components/AIJourney'
import TechStack from '@/components/TechStack'
import Testimonials from '@/components/Testimonials'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <About />
      <Services />
      <AIJourney />
      <TechStack />
      <Testimonials />
      <Contact />
      <Footer />
    </main>
  )
}

