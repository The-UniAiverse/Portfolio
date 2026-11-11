/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './data/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E40AF', // Primary Blue (blue-800)
          dark: '#0F172A', // Dark Blue (slate-900)
          light: '#3B82F6', // Light Blue (blue-500)
          lighter: '#60A5FA', // Lighter Blue (blue-400)
        },
        secondary: {
          DEFAULT: '#FFFFFF', // White
          light: '#F8FAFC', // Off-white (slate-50)
        },
        accent: {
          blue: '#2563EB', // Accent Blue (blue-600)
          darkBlue: '#1E3A8A', // Dark Blue (blue-900)
        }
      },
      // Deck theme: surfaces and text colours come from CSS variables (app/globals.css), so the same
      // class names render the dark "deck" look. Text-on-dark (text-secondary) stays white.
      backgroundColor: {
        secondary: { DEFAULT: 'rgb(var(--c-surface) / <alpha-value>)', light: 'rgb(var(--c-canvas) / <alpha-value>)' },
        primary: { DEFAULT: 'rgb(var(--c-action) / <alpha-value>)', dark: 'rgb(var(--c-deep) / <alpha-value>)' },
      },
      textColor: {
        primary: {
          DEFAULT: 'rgb(var(--c-link) / <alpha-value>)',
          light: 'rgb(var(--c-link-hover) / <alpha-value>)',
          lighter: 'rgb(var(--c-glow) / <alpha-value>)',
          dark: 'rgb(var(--c-ink) / <alpha-value>)',
        },
      },
      borderColor: {
        primary: { DEFAULT: 'rgb(var(--c-line) / <alpha-value>)' },
      },
      placeholderColor: {
        primary: { dark: 'rgb(var(--c-ink) / <alpha-value>)' },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-blue': 'radial-gradient(circle at 85% 10%, rgba(34,211,238,0.16), transparent 45%), radial-gradient(circle at 10% 90%, rgba(251,191,36,0.12), transparent 50%), linear-gradient(135deg, #0b1020 0%, #111a3a 100%)',
      },
      fontFamily: {
        outfit: ['var(--font-outfit)', 'sans-serif'],
        inter: ['var(--font-inter)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

