// Calendly Widget Type Definitions

interface CalendlyPopupOptions {
  url: string
  prefill?: {
    name?: string
    email?: string
    firstName?: string
    lastName?: string
    customAnswers?: Record<string, string>
  }
  utm?: {
    utmCampaign?: string
    utmSource?: string
    utmMedium?: string
    utmContent?: string
    utmTerm?: string
  }
}

interface CalendlyWidget {
  initPopupWidget: (options: CalendlyPopupOptions) => void
  closePopupWidget: () => void
  initInlineWidget: (options: { url: string; parentElement: HTMLElement }) => void
  initBadgeWidget: (options: {
    url: string
    text: string
    color: string
    textColor: string
    branding?: boolean
  }) => void
}

interface Window {
  Calendly?: CalendlyWidget
}


