import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'
import nextTs from 'eslint-config-next/typescript'

// Pages written before linting was added to CI. Their existing findings are warnings so they stay
// visible without blocking deploys; fix a file, then remove it from this list. New files get the full rules.
const LEGACY_FILES = [
  'app/admin/contacts/page.tsx',
  'app/admin/dashboard/page.tsx',
  'app/admin/services/page.tsx',
  'app/admin/testimonials/page.tsx',
  'app/services/ai-chatbots/page.tsx',
  'app/services/ai-strategy/page.tsx',
  'app/services/training/page.tsx',
  'components/Services.tsx',
  'components/Testimonials.tsx',
  'components/admin/AdminHeader.tsx',
  'components/admin/AuthGuard.tsx',
]

export default defineConfig([
  ...nextVitals,
  ...nextTs,
  {
    files: LEGACY_FILES,
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      'react-hooks/set-state-in-effect': 'warn',
      'react-hooks/immutability': 'warn',
      'react/no-unescaped-entities': 'warn',
    },
  },
  globalIgnores(['.next/**', 'out/**', 'next-env.d.ts']),
])
