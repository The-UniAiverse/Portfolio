# Calendly Integration Setup Guide

This guide will help you set up Calendly integration for meeting bookings on your website.

## 📋 Prerequisites

1. A Calendly account (Free or Paid)
2. Your Calendly scheduling link

## 🚀 Quick Setup

### Step 1: Get Your Calendly Link

1. Go to [Calendly.com](https://calendly.com) and sign in
2. Create an event type (e.g., "30 Minute Meeting", "Free Consultation")
3. Copy your Calendly scheduling link (e.g., `https://calendly.com/your-username/30min`)

### Step 2: Update Your Website

Replace the placeholder Calendly URL in the Contact component:

#### Contact Page (`components/Contact.tsx`)

Find the `openCalendly` function (around line 45) and replace the URL:

```tsx
const openCalendly = () => {
	if (window.Calendly) {
		window.Calendly.initPopupWidget({
			url: "YOUR_CALENDLY_LINK_HERE", // Replace this with your actual Calendly link
		});
	}
	return false;
};
```

#### Book Meeting Page (Optional - `/app/book-meeting/page.tsx`)

If you want to use the dedicated booking page, update the URL in:

```tsx
<CalendlyBooking
	calendlyUrl="YOUR_CALENDLY_LINK_HERE" // Replace this
/>
```

### Step 3: Customize Your Calendly Settings

In your Calendly dashboard, configure:

1. **Event Duration**: Set to 30 minutes (or your preference)
2. **Event Name**: "Free AI Consultation" or similar
3. **Event Description**: Describe what the meeting will cover
4. **Location**: Zoom, Google Meet, or Phone
5. **Availability**: Set your available hours
6. **Notifications**: Enable email reminders for both parties

## 🎨 Customization Options

### Customize Popup Widget

In `components/Contact.tsx`, you can add options to the popup:

```tsx
const openCalendly = () => {
	if (window.Calendly) {
		window.Calendly.initPopupWidget({
			url: "https://calendly.com/your-username/30min",
			// Optional: Pre-fill user information
			prefill: {
				name: formData.name,
				email: formData.email,
			},
			// Optional: Add UTM parameters
			utm: {
				utmSource: "website",
				utmMedium: "contact_page",
				utmCampaign: "consultation",
			},
		});
	}
	return false;
};
```

### Change Button Text

Customize the button in `components/Contact.tsx`:

```tsx
<button onClick={openCalendly}>
	<span>📅</span>
	<span>Your Custom Text Here</span>
</button>
```

## 📍 Where Calendly Appears

Calendly is integrated as a popup widget:

1. **Contact Section** (`/#contact`) - "Schedule a Free Consultation" button opens Calendly popup
2. **Book Meeting Page** (`/book-meeting`) - Optional dedicated booking page with embedded widget

## 🎯 Advanced Features

### Calendly Premium Features

If you have a paid Calendly plan, you can:

- Remove Calendly branding
- Add custom questions
- Enable team scheduling
- Set up workflows and reminders
- Integrate with CRM systems

### Custom Styling

To match Calendly widget with your theme, add to `app/globals.css`:

```css
.calendly-inline-widget iframe {
	border-radius: 12px;
}
```

## 🔗 Useful Links

- [Calendly Help Center](https://help.calendly.com/)
- [Calendly Embed Options](https://help.calendly.com/hc/en-us/articles/223147027-Embed-options-overview)
- [Calendly API Documentation](https://developer.calendly.com/)

## 📧 Support

For Calendly-specific issues, contact [Calendly Support](https://help.calendly.com/hc/en-us)

For website integration help, contact your development team.

## ✅ Testing

After setup:

1. Visit your website and go to the Contact section
2. Click "Schedule a Free Consultation" button
3. Calendly popup should open
4. Try booking a test meeting
5. Verify you receive confirmation emails
6. Check the meeting appears in your calendar

## 🔧 Troubleshooting

### Button doesn't open popup

**Solution 1: Check Browser Console**

- Open browser DevTools (F12)
- Look for errors related to Calendly
- Make sure your Calendly URL is correct

**Solution 2: Script Loading Issue**

- The script loads automatically when the Contact component mounts
- Wait a few seconds after page load before clicking
- Check Network tab in DevTools to verify script loaded

**Solution 3: Fallback to New Tab**

- If popup fails, the button will open Calendly in a new tab
- This is built-in as a fallback mechanism

### 404 Error on Calendly Script

**Cause**: Script URL might be blocked or incorrect

**Solution**:

- Check your internet connection
- Verify firewall/ad-blocker isn't blocking Calendly
- The script URL is: `https://assets.calendly.com/assets/external/widget.js`

### Conflict with Other Widgets (Ada Embed Error)

**Cause**: Multiple chat/embed widgets competing

**Solution**: The code now checks if Calendly is already loaded to prevent conflicts

### TypeScript Errors

**Solution**: We've added proper type definitions in `types/calendly.d.ts`

---

**Note**: Replace all instances of `https://calendly.com/your-username/30min` with your actual Calendly link!
