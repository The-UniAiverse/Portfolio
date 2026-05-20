'use client'

import Script from 'next/script'
import { contactPageData } from '@/data/contact.data'

const CalendlyBadge = () => {
    const initCalendly = () => {
        if (typeof window !== 'undefined' && window.Calendly) {
            // Clear any existing badge if it exists to avoid duplicates
            const existingBadge = document.querySelector('.calendly-badge-widget');
            if (existingBadge) {
                existingBadge.remove();
            }

            window.Calendly.initBadgeWidget({
                url: contactPageData.calendlyUrl,
                text: 'Schedule time with me',
                color: '#0069ff',
                textColor: '#ffffff',
                branding: true
            })
        }
    }

    return (
        <>
            <link
                href="https://assets.calendly.com/assets/external/widget.css"
                rel="stylesheet"
            />
            <Script
                src="https://assets.calendly.com/assets/external/widget.js"
                onLoad={initCalendly}
            />
        </>
    )
}

export default CalendlyBadge
