import Header from '@/components/Header'
import BlogHero from '@/components/BlogHero'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'
import Link from 'next/link'
import pool from '@/lib/db'

interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  category: string
  read_time: string
  date: string
  tags: string[] | string
  status: string
}

const categoryImages: Record<string, string> = {
  'AI Trends': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
  'Technical': 'https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=800&h=600&fit=crop',
  'MLOps': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&h=600&fit=crop',
  'Case Study': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop',
  'News': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=600&fit=crop',
  'General': 'https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=800&h=600&fit=crop',
}

function getImage(category: string) {
  return categoryImages[category] || categoryImages['General']
}

function parseTags(tags: string[] | string): string[] {
  if (Array.isArray(tags)) return tags
  try { return JSON.parse(tags) } catch { return [] }
}

async function getBlogPosts(): Promise<BlogPost[]> {
  try {
    const [rows] = await pool.execute(
      "SELECT * FROM blog_posts WHERE status = 'published' ORDER BY date DESC, created_at DESC"
    )
    return rows as BlogPost[]
  } catch {
    return []
  }
}

const BlogPage = async () => {
  const blogPosts = await getBlogPosts()

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <BlogHero />

      {/* Blog Posts Section - Zigzag Layout */}
      <section className="py-20 bg-secondary">
        <div className="container mx-auto px-6">
          {blogPosts.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-primary-dark/50 text-xl">No published posts yet. Check back soon!</p>
            </div>
          ) : (
            <div className="max-w-7xl mx-auto space-y-32">
              {blogPosts.map((post, index) => {
                const isEven = index % 2 === 0
                const tags = parseTags(post.tags)
                const image = getImage(post.category)
                const formattedDate = post.date
                  ? new Date(post.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                  : ''

                return (
                  <article
                    key={post.id}
                    className={`flex flex-col ${isEven ? 'lg:flex-row' : 'lg:flex-row-reverse'} gap-12 items-center group`}
                  >
                    {/* Image Container */}
                    <div className="lg:w-1/2 relative">
                      <div className="relative overflow-hidden rounded-3xl shadow-2xl group-hover:shadow-primary-light/30 transition-all duration-500">
                        <div className="relative h-80 lg:h-96">
                          <img
                            src={image}
                            alt={post.title}
                            className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-primary-dark/80 via-primary-dark/40 to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-500" />
                          <div className="absolute top-6 left-6">
                            <span className="bg-primary-light/90 backdrop-blur-sm text-secondary px-4 py-2 rounded-full text-sm font-semibold shadow-lg">
                              {post.category}
                            </span>
                          </div>
                        </div>
                        <div className={`absolute -z-10 top-8 ${isEven ? '-right-8' : '-left-8'} w-full h-full bg-gradient-to-br from-primary-light/20 to-accent-blue/20 rounded-3xl transform group-hover:scale-105 transition-transform duration-500`} />
                      </div>
                    </div>

                    {/* Content Container */}
                    <div className="lg:w-1/2 space-y-6">
                      <div className="flex items-center gap-4 text-sm text-primary-dark/60">
                        {formattedDate && (
                          <span className="flex items-center gap-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {formattedDate}
                          </span>
                        )}
                        <span className="flex items-center gap-2">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          {post.read_time}
                        </span>
                        <span className="flex items-center gap-2">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          uniAiverse Team
                        </span>
                      </div>

                      <h2 className="text-3xl lg:text-4xl font-bold text-primary-dark leading-tight group-hover:text-primary transition-colors duration-300">
                        {post.title}
                      </h2>

                      <p className="text-lg text-primary-dark/70 leading-relaxed">
                        {post.excerpt}
                      </p>

                      {tags.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {tags.map((tag, tagIndex) => (
                            <span
                              key={tagIndex}
                              className="bg-primary-light/10 text-primary-dark px-4 py-2 rounded-full text-sm font-medium hover:bg-primary-light/20 transition-colors duration-300"
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}

                      <div className="pt-4">
                        <Link
                          href={`/blog/${post.slug}`}
                          className="group/btn inline-flex items-center gap-2 bg-primary hover:bg-primary-light text-secondary px-8 py-4 rounded-full font-semibold text-lg transition-all duration-300 hover:shadow-xl hover:shadow-primary-light/50 hover:scale-105"
                        >
                          Read Full Article
                          <svg
                            className="w-5 h-5 group-hover/btn:translate-x-2 transition-transform duration-300"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                          </svg>
                        </Link>
                      </div>
                    </div>
                  </article>
                )
              })}
            </div>
          )}

          {/* Load More */}
          {blogPosts.length > 0 && (
            <div className="text-center mt-20">
              <button className="group bg-transparent border-2 border-primary text-primary px-10 py-4 rounded-full font-bold text-lg hover:bg-primary hover:text-secondary transition-all duration-300 hover:shadow-xl hover:shadow-primary/50 hover:scale-105">
                Load More Articles
                <span className="inline-block ml-2 group-hover:translate-y-1 transition-transform duration-300">↓</span>
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-20 bg-gradient-to-r from-primary-dark via-primary to-primary-light">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h2 className="text-4xl md:text-5xl font-bold text-secondary">
              Stay Updated with AI Insights
            </h2>
            <p className="text-xl text-secondary/90">
              Subscribe to our newsletter and get the latest AI trends, tutorials, and case studies delivered to your inbox.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-2xl mx-auto">
              <input
                type="email"
                placeholder="Enter your email address"
                className="flex-1 px-6 py-4 rounded-full text-primary-dark focus:outline-none focus:ring-4 focus:ring-primary-lighter/50 shadow-lg"
              />
              <button className="bg-secondary hover:bg-primary-lighter text-primary-dark px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 hover:shadow-2xl hover:scale-105 whitespace-nowrap">
                Subscribe Now
              </button>
            </div>
            <p className="text-sm text-secondary/70">
              🔒 We respect your privacy. Unsubscribe at any time.
            </p>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </div>
  )
}

export default BlogPage
