import type { Metadata } from 'next'
import ToolPage from '@/components/tools/ToolPage'
import PricingTool from '@/components/tools/PricingTool'

export const metadata: Metadata = {
  title: 'Pricing | uniAiverse',
  description: 'Bronze, Silver, Gold and Platinum packages for every uniAiverse service, with indicative pricing by company size.',
}

export default function PricingPage() {
  return (
    <ToolPage
      icon="💎"
      subtitle="Service Tiers & Pricing"
      title="Transparent Pricing"
      description="Four tiers for every service. Pick your company size to see an indicative quote."
      gradient="bg-deck"
    >
      <PricingTool />
    </ToolPage>
  )
}
