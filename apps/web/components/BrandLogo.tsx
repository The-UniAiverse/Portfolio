import { useId } from 'react'

interface BrandLogoProps {
  /** Mark size in px. */
  size?: number
  /** Show the "uniAiverse" wordmark next to the mark. */
  wordmark?: boolean
  /** Wordmark text size (Tailwind class). */
  textClassName?: string
  /** Orbit, glow and shimmer animations (always off for prefers-reduced-motion). */
  animated?: boolean
  /** Background the logo sits on: wordmark letters are white on dark, navy on light. */
  tone?: 'dark' | 'light'
  className?: string
}

/**
 * uniAiverse brand mark: the "Ai" ligature from the original logo, drawn as a gradient vector,
 * circled by an orbit (the "universe") with a travelling particle. Styles live in globals.css (.brand-*).
 */
export default function BrandLogo({
  size = 40,
  wordmark = true,
  textClassName = 'text-2xl',
  animated = true,
  tone = 'dark',
  className = '',
}: BrandLogoProps) {
  const id = useId().replace(/:/g, '')
  const grad = `brand-grad-${id}`
  const ring = `brand-ring-${id}`
  const glow = `brand-glow-${id}`
  const orbit = 'M -2 32 a 34 13 0 1 0 68 0 a 34 13 0 1 0 -68 0'

  return (
    <span className={`brand-logo inline-flex items-center gap-4 ${animated ? 'brand-animated' : ''} ${className}`}>
      <svg width={size} height={size} viewBox="6 6 52 52" aria-hidden="true" className="shrink-0 overflow-visible">
        <defs>
          <linearGradient id={grad} x1="12" y1="54" x2="52" y2="8" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#2563EB" />
            <stop offset="0.55" stopColor="#38BDF8" />
            <stop offset="1" stopColor="#A78BFA" />
          </linearGradient>
          <linearGradient id={ring} x1="0" y1="32" x2="64" y2="32" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#38BDF8" stopOpacity="0" />
            <stop offset="0.5" stopColor="#60A5FA" stopOpacity="0.9" />
            <stop offset="1" stopColor="#A78BFA" stopOpacity="0" />
          </linearGradient>
          <filter id={glow} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="6" />
          </filter>
        </defs>

        {/* soft halo behind the mark */}
        <circle className="brand-halo" cx="32" cy="32" r="20" fill={`url(#${grad})`} filter={`url(#${glow})`} opacity="0.45" />

        {/* orbit + travelling particle, tilted like a planetary ring */}
        <g transform="rotate(-24 32 32)">
          <path className="brand-orbit" d={orbit} fill="none" stroke={`url(#${ring})`} strokeWidth="2" />
          <circle className="brand-particle" r="2.8" fill="#E0F2FE">
            <animateMotion dur="5.5s" repeatCount="indefinite" path={orbit} />
          </circle>
        </g>

        {/* the "Ai" ligature */}
        <path
          className="brand-stroke"
          d="M33 15 L19.5 42 Q15.5 52.5 24.5 52.5 Q30.5 52.5 33.5 45.5 L40.5 24 L48.5 50"
          fill="none"
          stroke={`url(#${grad})`}
          strokeWidth="6.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={100}
        />
        <circle className="brand-dot" cx="43.5" cy="12.5" r="4.3" fill="#A78BFA" />
      </svg>

      {wordmark && (
        <span className={`font-bold tracking-tight leading-none ${textClassName}`}>
          <span className={tone === 'dark' ? 'text-white' : 'text-primary-dark'}>uni</span>
          <span className="brand-ai">Ai</span>
          <span className={tone === 'dark' ? 'text-white' : 'text-primary-dark'}>verse</span>
        </span>
      )}
    </span>
  )
}
