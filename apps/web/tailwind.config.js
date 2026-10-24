/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
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
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-blue': 'linear-gradient(135deg, #0F172A 0%, #1E40AF 50%, #3B82F6 100%)',
      },
      fontFamily: {
        outfit: ['var(--font-outfit)', 'sans-serif'],
        inter: ['var(--font-inter)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

