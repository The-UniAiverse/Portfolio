export interface ContactInfo {
  icon: string
  title: string
  details: string[]
  link?: string
}

export const contactServices = [
  'Generative AI Development',
  'AI & Machine Learning',
  'Agentic AI & Context-Aware Systems',
  'Natural Language Processing',
  'MLOps & Deployment',
  'Data Science',
  'Computer Vision',
  'Training and Workshops',
  'General Inquiry',
]

export const contactInfo: ContactInfo[] = [
  {
    icon: '📍',
    title: 'Address',
    details: [
      'F/N. 5. First Floor, F building,',
      'Monika Garden View,',
      'Near Ropalas Company,',
      'Pimpri, Pune, 411018.',
    ],
  },
  {
    icon: '📞',
    title: 'Phone',
    details: ['+91 8956837601'],
    link: 'tel:+918956837601',
  },
  {
    icon: '✉️',
    title: 'Email',
    details: ['uniaiverse@outlook.in'],
    link: 'mailto:uniaiverse@outlook.in',
  },
  {
    icon: '🕐',
    title: 'Business Hours',
    details: ['Monday - Friday: 9:00 AM - 6:00 PM', 'Saturday: 10:00 AM - 4:00 PM'],
  },
]

export const contactPageData = {
  heading: {
    prefix: 'Let\'s Start Your',
    highlight: 'AI Journey',
  },
  subheading:
    'Get in touch with our team of AI experts. We\'re here to help transform your business with intelligent solutions.',
  whyChooseUs: [
    {
      title: 'Expert Team',
      description: 'Decades of combined AI/ML experience',
    },
    {
      title: 'Proven Results',
      description: '10-40% ROI gains across use cases',
    },
    {
      title: 'Responsible AI',
      description: 'Ethical, transparent, and fair solutions',
    },
    {
      title: 'End-to-End Support',
      description: 'From strategy to deployment and beyond',
    },
  ],
  socialLinks: [
    { name: 'Facebook', icon: 'FB', href: '#' },
    { name: 'X', icon: 'X', href: '#' },
    { name: 'Instagram', icon: 'IG', href: '#' },
    { name: 'YouTube', icon: 'YT', href: '#' },
  ],
  calendlyUrl: "https://calendly.com/uniaiverse2025/30min",
  calendlyEventTypeUri: "https://api.calendly.com/event_types/PLACEHOLDER",
}

