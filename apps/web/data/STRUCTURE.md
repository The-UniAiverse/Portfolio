# Data Structure Visualization

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│                         (app/page.tsx)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Components Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Hero    │  │ Services │  │  About   │  │Testimonial│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │              │          │
│  ┌────┴─────┐  ┌───┴──────┐  ┌───┴──────┐  ┌───┴──────┐   │
│  │TechStack │  │AIJourney │  │ Contact  │  │  Header  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │              │          │
└───────┼─────────────┼──────────────┼──────────────┼─────────┘
        │             │              │              │
        ▼             ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ hero.data.ts │  │services.data │  │ about.data   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │testimonials  │  │techstack.data│  │aijourney.data│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │contact.data  │  │navigation.data│  │ footer.data  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Page      │────▶│  Component  │────▶│    Data     │
│  (app/)     │     │(components/)│     │   (data/)   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────┐
│              Rendered HTML to User                   │
└─────────────────────────────────────────────────────┘
```

## Component-Data Mapping

| Component | Data File | Purpose |
|-----------|-----------|---------|
| `Hero.tsx` | `hero.data.ts` | Hero section content, stats, CTAs |
| `Services.tsx` | `services.data.ts` | Services list and descriptions |
| `About.tsx` | `about.data.ts` | Company info, principles, achievements |
| `Testimonials.tsx` | `testimonials.data.ts` | Client testimonials and stats |
| `TechStack.tsx` | `techstack.data.ts` | Technology categories and filters |
| `AIJourney.tsx` | `aijourney.data.ts` | AI journey phases |
| `Contact.tsx` | `contact.data.ts` | Contact information and form options |
| `Header.tsx` | `navigation.data.ts` | Navigation links and menu |
| `Footer.tsx` | `footer.data.ts` | Footer links and company info |

## Data File Contents

### 📄 hero.data.ts
```typescript
{
  badge: { emoji, text },
  heading: { prefix, highlight, suffix },
  subheading: string,
  tagline: { main, sub },
  cta: { primary, secondary },
  stats: [{ value, label }],
  images: { main, topRight, bottomRight },
  video: { src, type }
}
```

### 📄 services.data.ts
```typescript
{
  servicesData: [
    { title, description, icon, href }
  ],
  servicesPageData: {
    heading: { prefix, highlight, suffix },
    subheading,
    cta: { heading, buttonText, buttonHref }
  }
}
```

### 📄 about.data.ts
```typescript
{
  purpose: { heading, description, corePrinciples[] },
  identity: { heading, description, tagline, brandName },
  principles: [{ icon, title, description }],
  differentiators: [{ title, description, icon }],
  achievements: { heading, items[] }
}
```

### 📄 testimonials.data.ts
```typescript
{
  testimonialsData: [
    { quote, author, role, company, avatar, rating }
  ],
  testimonialsPageData: {
    heading: { prefix, highlight },
    subheading,
    stats: [{ value, label }]
  }
}
```

### 📄 techstack.data.ts
```typescript
{
  techCategories: [
    { category, id, icon, techs[] }
  ],
  filterCategories: [{ id, label }],
  techStackPageData: {
    heading: { prefix, highlight },
    subheading,
    cta: { heading, subheading, buttonText, buttonHref }
  }
}
```

### 📄 aijourney.data.ts
```typescript
{
  aiJourneyPhases: [
    { phase, title, description, icon, color }
  ],
  aiJourneyPageData: {
    heading: { prefix, highlight },
    subheading,
    cta: { text, buttonText, buttonHref }
  }
}
```

### 📄 contact.data.ts
```typescript
{
  contactServices: string[],
  contactInfo: [
    { icon, title, details[], link? }
  ],
  contactPageData: {
    heading: { prefix, highlight },
    subheading,
    whyChooseUs: [{ title, description }],
    socialLinks: [{ name, icon, href }]
  }
}
```

### 📄 navigation.data.ts
```typescript
{
  navLinks: [{ href, label }],
  serviceLinks: [{ icon, title, href }]
}
```

### 📄 footer.data.ts
```typescript
{
  footerServices: string[],
  footerCompany: string[],
  footerSocialLinks: [{ name, href, icon }],
  footerAddress: { line1, line2, line3, line4, phone }
}
```

## Import Examples

### Single Import
```typescript
import { heroData } from '@/data/hero.data'
```

### Multiple Imports
```typescript
import { servicesData, servicesPageData } from '@/data/services.data'
```

### From Index
```typescript
import { heroData, servicesData, aboutData } from '@/data'
```

## Maintenance Workflow

```
┌─────────────────┐
│  Need to Update │
│    Content?     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Identify the   │
│  Data File      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Edit Data in   │
│  TypeScript     │
│  Object         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save File      │
│  (Auto-reload)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Changes Live   │
│  Everywhere!    │
└─────────────────┘
```

## Benefits Summary

```
┌──────────────────────────────────────────────────────┐
│                   BEFORE                              │
├──────────────────────────────────────────────────────┤
│  • Data scattered across components                  │
│  • Hard to find and update content                   │
│  • Duplicate data in multiple places                 │
│  • Component files cluttered                         │
│  • No single source of truth                         │
└──────────────────────────────────────────────────────┘
                        ↓
                  REFACTORED
                        ↓
┌──────────────────────────────────────────────────────┐
│                    AFTER                              │
├──────────────────────────────────────────────────────┤
│  ✅ All data centralized in data/ directory          │
│  ✅ Easy to find and update content                  │
│  ✅ Single source of truth                           │
│  ✅ Clean, focused component files                   │
│  ✅ Type-safe with TypeScript                        │
│  ✅ Ready for CMS integration                        │
│  ✅ Scalable and maintainable                        │
└──────────────────────────────────────────────────────┘
```

