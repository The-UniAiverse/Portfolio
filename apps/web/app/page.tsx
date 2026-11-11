import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Services from '@/components/Services'
import WhyUs from '@/components/home/WhyUs'
import AIJourney from '@/components/AIJourney'
import Spotlight from '@/components/home/Spotlight'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <Services />
      <WhyUs />
      <AIJourney />
      <Spotlight />
      <Contact />
      <Footer />
    </main>
  )
}
