export interface Testimonial {
  quote: string
  author: string
  role: string
  company: string
  avatar: string
  rating: number
}

export const testimonialsData: Testimonial[] = [
  {
    quote:
      'UniAiverse\'s expertise helped us seamlessly integrate AI, boosting our productivity beyond expectations.',
    author: 'Maria Chen',
    role: 'Chief Technology Officer',
    company: 'TechCorp Inc.',
    avatar: '👩‍💼',
    rating: 5,
  },
  {
    quote:
      'The team delivered beyond our vision, providing AI solutions that truly elevated our operational efficiency.',
    author: 'David Alvarez',
    role: 'Head of Innovation',
    company: 'InnovateLabs',
    avatar: '👨‍💼',
    rating: 5,
  },
  {
    quote:
      'Outstanding AI consulting services. They transformed our data into actionable insights that drove real business value.',
    author: 'Sarah Johnson',
    role: 'VP of Engineering',
    company: 'DataFlow Systems',
    avatar: '👩‍💻',
    rating: 5,
  },
]

export const testimonialsPageData = {
  heading: {
    prefix: 'Empowering Growth with',
    highlight: 'Tailored AI Solutions',
  },
  subheading:
    'Hear from our clients about how uniAiverse transformed their businesses with innovative AI strategies and measurable success.',
  stats: [
    {
      value: '100+',
      label: 'Projects Completed',
    },
    {
      value: '50+',
      label: 'Happy Clients',
    },
    {
      value: '98%',
      label: 'Satisfaction Rate',
    },
    {
      value: '24/7',
      label: 'Support Available',
    },
  ],
}

