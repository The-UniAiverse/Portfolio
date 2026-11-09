import type { Metadata } from 'next'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import ProviderButtons from '@/components/auth/ProviderButtons'
import { enabledProviders } from '@/lib/auth'
import { safeNext } from '@/lib/safe-next'
import BrandLogo from '@/components/BrandLogo'

export const metadata: Metadata = {
  title: 'Sign in | uniAiverse',
  description: 'Sign in to use the uniAiverse AI tools.',
}

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string }> }) {
  const next = safeNext((await searchParams).next)
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <section className="flex-1 bg-gradient-to-br from-blue-900 via-indigo-800 to-purple-600 flex items-center justify-center px-6 pt-32 pb-20">
        <div className="bg-secondary rounded-3xl shadow-2xl p-10 w-full max-w-md text-center">
          <div className="flex justify-center mb-4"><BrandLogo size={72} wordmark={false} /></div>
          <h1 className="text-3xl font-bold text-primary-dark mb-2">Sign in to uniAiverse</h1>
          <p className="text-primary-dark/60 mb-8">New here? Signing in creates your free account. Use it to run our AI tools.</p>
          <ProviderButtons providers={enabledProviders} next={next} />
          <p className="text-xs text-primary-dark/40 mt-8">
            We only receive your name, email and profile picture from Google or GitHub.{' '}
            <Link href="/" className="underline">Back to home</Link>
          </p>
        </div>
      </section>
      <Footer />
    </main>
  )
}
