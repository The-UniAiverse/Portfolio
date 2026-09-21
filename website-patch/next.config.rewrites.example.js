// Optional: serve the tools under uniaiverse.ai/tools/* instead of api.uniaiverse.ai
/** @type {import('next').NextConfig} */
module.exports = {
  async rewrites() {
    const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    return [
      { source: '/tools/audit', destination: `${api}/` },
      { source: '/tools/course-finder', destination: `${api}/course-finder` },
      { source: '/tools/quest', destination: `${api}/quest` },
      { source: '/tools/pay', destination: `${api}/pay` },
      { source: '/tools/delivery', destination: `${api}/delivery` },
      { source: '/tools/demos', destination: `${api}/demos` },
      { source: '/api/:path*', destination: `${api}/api/:path*` },
      { source: '/static/:path*', destination: `${api}/static/:path*` },
    ]
  },
}
