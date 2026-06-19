import type { Metadata } from 'next'
import { Inter, Outfit } from 'next/font/google'
import Script from 'next/script'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const outfit = Outfit({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-outfit',
})

export const metadata: Metadata = {
  title: 'uniAiverse - AI Consulting & Development Services',
  description: 'Expert AI consulting, solution design, development, and long-term support. From Generative AI and NLP to MLOps, Data Science, and Computer Vision.',
  keywords: 'AI consulting, Machine Learning, Generative AI, NLP, MLOps, Data Science, Computer Vision',
  icons: {
    icon: '/logo.png',
    apple: '/logo.png',
  },
}

import CalendlyBadge from '@/components/CalendlyBadge'
import OrbiBot from '@/components/OrbiBot'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
      <body>
        {children}
        <CalendlyBadge />
        <OrbiBot />
        {/* Tawk.to chat widget - Commented out as HubSpot chat is being used */}
        {/* <Script
          id="tawk-to-init"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
            `,
          }}
        />
        <Script
          id="tawk-to-loader"
          src="https://embed.tawk.to/69a9c847684fb91c32f1e797/1jivjcmnc"
          strategy="afterInteractive"
          async
        /> */}
      </body>
    </html>
  )
}

