# Data Services Documentation

This directory contains all static data used throughout the uniAiverse website. All data has been centralized here to make content management easier and more maintainable.

## File Structure

```
data/
├── about.data.ts          # About page content (purpose, principles, achievements)
├── aijourney.data.ts      # AI Journey phases and content
├── contact.data.ts        # Contact page information and services list
├── footer.data.ts         # Footer links, services, company info
├── hero.data.ts           # Hero section content, stats, and CTAs
├── navigation.data.ts     # Header navigation links and service menu
├── services.data.ts       # Services list and page content
├── techstack.data.ts      # Technology categories and filters
├── testimonials.data.ts   # Client testimonials and stats
└── index.ts               # Central export file for all data
```

## Usage

Import data from the specific file you need:

```typescript
import { heroData } from '@/data/hero.data'
import { servicesData } from '@/data/services.data'
import { aboutData } from '@/data/about.data'
```

Or import from the central index:

```typescript
import { heroData, servicesData, aboutData } from '@/data'
```

## Data Files Overview

### `hero.data.ts`
Contains hero section content including:
- Badge text and emoji
- Main heading (prefix, highlight, suffix)
- Subheading and tagline
- CTA buttons (primary and secondary)
- Stats (ROI, Projects, Clients, Support)
- Images and video sources

### `services.data.ts`
Contains:
- Array of service objects with title, description, icon, and href
- Services page heading and subheading
- CTA section content

### `about.data.ts`
Contains:
- Purpose section (heading, description, core principles)
- Company identity (heading, tagline, brand name)
- Vision, Mission, Drive principles
- Differentiators (4 key points)
- Achievements list

### `testimonials.data.ts`
Contains:
- Array of testimonial objects (quote, author, role, company, avatar, rating)
- Page heading and subheading
- Stats section (Projects, Clients, Satisfaction, Support)

### `techstack.data.ts`
Contains:
- Tech categories array (8 categories with technologies)
- Filter categories for the tech stack
- Page heading, subheading, and CTA

### `aijourney.data.ts`
Contains:
- Array of 4 phases (Strategy, Build, Deploy, Upskill)
- Page heading and subheading
- CTA text and button

### `contact.data.ts`
Contains:
- Contact services list (for dropdown)
- Contact information (address, phone, email, hours)
- Page heading and subheading
- "Why Choose Us" section
- Social media links

### `navigation.data.ts`
Contains:
- Main navigation links (Home, About, Blog, etc.)
- Service links for dropdown menu

### `footer.data.ts`
Contains:
- Footer services list
- Company links
- Social media links
- Address information

## Modifying Content

To update any content on the website:

1. Locate the appropriate data file
2. Edit the content directly in the TypeScript object
3. Save the file
4. The changes will be reflected across all components using that data

## TypeScript Interfaces

Most data files include TypeScript interfaces for type safety:

- `Service` - Service object structure
- `Testimonial` - Testimonial object structure
- `TechCategory` - Technology category structure
- `Phase` - AI Journey phase structure
- `ContactInfo` - Contact information structure
- etc.

## Benefits of This Structure

✅ **Centralized Management** - All content in one place  
✅ **Type Safety** - TypeScript interfaces ensure data consistency  
✅ **Easy Updates** - Change content without touching component logic  
✅ **Reusability** - Same data can be used across multiple components  
✅ **Maintainability** - Easier to track and update content  
✅ **Scalability** - Easy to add new data sources or migrate to CMS  

## Future Enhancements

This structure makes it easy to:
- Connect to a headless CMS (Contentful, Sanity, etc.)
- Add internationalization (i18n)
- Implement A/B testing
- Create admin panels for content management

