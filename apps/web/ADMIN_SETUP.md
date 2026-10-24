# uniAiverse Admin Panel Setup Guide

## Overview
The admin panel is fully implemented with the following features:

- **Dashboard** - Real-time statistics from all modules
- **Services** - Manage AI services (CRUD operations)
- **Blog** - Create and manage blog posts
- **Testimonials** - Manage client testimonials
- **Contacts** - View inquiries and manage contact info

## Quick Start

### 1. Install Dependencies
```bash
cd uniaiverse-website-main
npm install
```

### 2. Set Up Environment Variables
Copy the example file and fill in your database details:
```bash
cp .env.example .env.local
```

Edit `.env.local` with your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=5240
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=uniaiverse
```

### 3. Set Up Database
**Option A: Manual SQL Setup**
Run the SQL schema file in your MySQL database:
```bash
mysql -u root -p uniaiverse < database/schema.sql
```

**Option B: Auto-Create Tables (Default)**
The API routes will automatically create tables on first request. No manual setup needed!

### 4. Start the Development Server
```bash
npm run dev
```

### 5. Access Admin Panel
1. Visit: `http://localhost:3000/admin`
2. Login with default credentials:
   - **Email:** `admin@uniaiverse.com`
   - **Password:** `admin@123`

## Admin Panel Routes

| Route | Description |
|-------|-------------|
| `/admin` | Redirects to login or dashboard |
| `/admin/login` | Admin login page |
| `/admin/dashboard` | Overview with live statistics |
| `/admin/services` | Manage services |
| `/admin/blog` | Manage blog posts |
| `/admin/testimonials` | Manage testimonials |
| `/admin/contacts` | View inquiries & contact info |

## Database Schema

### Tables Auto-Created by APIs:
1. `services` - AI services data
2. `blog_posts` - Blog articles
3. `testimonials` - Client testimonials
4. `contacts` - Contact form submissions
5. `contact_info` - Website contact details

## API Endpoints

All API routes are in `app/api/admin/`:

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/admin/services` | GET, POST | List/create services |
| `/api/admin/services/[id]` | PUT, PATCH, DELETE | Update/delete service |
| `/api/admin/blog` | GET, POST | List/create blog posts |
| `/api/admin/blog/[id]` | PUT, PATCH, DELETE | Update/delete post |
| `/api/admin/testimonials` | GET, POST | List/create testimonials |
| `/api/admin/testimonials/[id]` | PUT, DELETE | Update/delete testimonial |
| `/api/admin/contacts` | GET, POST | List inquiries / submit contact |
| `/api/admin/contacts/[id]` | PATCH, DELETE | Update status / delete |
| `/api/admin/contact-info` | GET, POST | List/create contact info |
| `/api/admin/contact-info/[id]` | PUT, DELETE | Update/delete contact info |
| `/api/contact-info` | GET | Public contact info for website |

## Features

### Dashboard
- Live statistics from all modules
- Recent activity feed
- Quick action buttons
- Database connection status

### Services Management
- Add/edit/delete services
- Category filtering
- Active/inactive toggle
- Import from static data
- Rich service details (included items, use cases, capabilities)

### Blog Management
- Create/edit blog posts
- Category and tag support
- Draft/published status
- Slug auto-generation
- Search and filter

### Testimonials
- Add client testimonials
- Star rating system
- Avatar selection
- Average rating calculation

### Contacts
- View contact inquiries
- Status management (new/in-progress/resolved)
- Search and filter
- Manage website contact information
- Direct email reply button

## Security

- AuthGuard component protects all admin pages
- localStorage-based session (simple auth)
- Login redirect for unauthenticated users
- Credentials stored in login page (change in production!)

## Customization

### Change Admin Password
Edit `app/admin/login/page.tsx`:
```typescript
const ADMIN_CREDENTIALS = {
  email: 'your-email@example.com',
  password: 'your-secure-password',
  name: 'Your Name',
}
```

### Add New Admin Menu Item
Edit `components/admin/AdminSidebar.tsx`:
```typescript
const navItems = [
  // ... existing items
  { href: '/admin/your-page', label: 'Your Page', icon: (...) },
]
```

## Production Deployment

1. Set up production database
2. Update environment variables
3. Change default admin credentials
4. Build the project:
   ```bash
   npm run build
   ```
5. Start production server:
   ```bash
   npm start
   ```

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `.env.local`
- Ensure database exists

### Tables Not Found
- Tables auto-create on first API request
- Or manually run `database/schema.sql`

### Admin Panel Not Loading
- Check if `npm run dev` is running
- Verify no build errors
- Clear browser cache

## Support

For issues or questions, check:
- API logs in terminal
- Browser console for errors
- Database connection status on dashboard
