// Server-side authentication (Better Auth). Users sign in with Google or GitHub; the first sign-in
// creates the account. Users and sessions live in MongoDB.
// The JWT plugin issues short-lived tokens (GET /api/auth/token) that the AI Services API (apps/api)
// verifies against the public keys at /api/auth/jwks, so the API enforces login itself.
import { betterAuth } from 'better-auth'
import { mongodbAdapter } from 'better-auth/adapters/mongodb'
import { nextCookies } from 'better-auth/next-js'
import { jwt } from 'better-auth/plugins'
import { mongoClient, mongoDb } from './mongo'

const socialProviders = {
  ...(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
    ? { google: { clientId: process.env.GOOGLE_CLIENT_ID, clientSecret: process.env.GOOGLE_CLIENT_SECRET } }
    : {}),
  ...(process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET
    ? { github: { clientId: process.env.GITHUB_CLIENT_ID, clientSecret: process.env.GITHUB_CLIENT_SECRET } }
    : {}),
}

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  database: mongodbAdapter(mongoDb(), {
    client: mongoClient,
    // Atlas supports transactions; a standalone local mongod does not (set MONGODB_TRANSACTIONS=false).
    transaction: process.env.MONGODB_TRANSACTIONS !== 'false',
  }),
  socialProviders,
  account: {
    // Same verified email via Google and GitHub = one account.
    accountLinking: { enabled: true, trustedProviders: ['google', 'github'] },
  },
  plugins: [
    jwt({
      jwt: {
        expirationTime: '15m',
        // Keep the token small: only what the API needs to identify the user.
        definePayload: ({ user }) => ({ email: user.email, name: user.name }),
      },
    }),
    nextCookies(),
  ],
})

/** Which sign-in buttons to show (providers without credentials are hidden). */
export const enabledProviders = Object.keys(socialProviders) as ('google' | 'github')[]
