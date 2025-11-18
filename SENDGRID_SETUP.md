# SendGrid Email Setup Guide

## Why SendGrid?

When deploying to cloud platforms like Render.com, **SMTP ports (25, 465, 587) are blocked** to prevent spam. This means traditional SMTP email services (like Gmail SMTP) won't work.

**SendGrid** is a cloud-based email delivery service that works reliably on cloud platforms without requiring SMTP ports.

## Setup Steps

### 1. Create a SendGrid Account

1. Go to [SendGrid](https://sendgrid.com/) and sign up for a free account
2. Free tier includes 100 emails/day, which is sufficient for most assessment use cases

### 2. Verify Your Sender Email

**CRITICAL**: SendGrid requires you to verify the email address you'll send from.

1. Go to [Sender Authentication](https://app.sendgrid.com/settings/sender_auth)
2. Click "Verify a Single Sender"
3. Fill in the form with your email address (this will be your `EMAIL_DEFAULT_SENDER`)
4. Check your email and click the verification link
5. Wait for verification to complete (usually instant)

### 3. Create an API Key

1. Go to [API Keys](https://app.sendgrid.com/settings/api_keys)
2. Click "Create API Key"
3. Name it something like "Foreign Language Assessment"
4. Choose "Full Access" or at minimum "Mail Send" permissions
5. Click "Create & View"
6. **IMPORTANT**: Copy the API key immediately - you won't be able to see it again!

### 4. Configure Environment Variables

In your Render dashboard, add these environment variables:

```bash
# Required
SENDGRID_API_KEY=SG.your-api-key-here
EMAIL_DEFAULT_SENDER=your-verified-email@example.com
TARGET_EMAIL=recipient@example.com

# Optional - SMTP (won't work on Render but can be used locally)
EMAIL_PROVIDER=smtp
```

### 5. Verify Configuration

After deploying with the new environment variables:

1. The application will automatically use SendGrid for email delivery
2. Check the logs for:
   ```
   [EMAILER] SendGrid configured: True
   [EMAILER] Using SendGrid fallback for email delivery
   ```

## Troubleshooting

### Error: "HTTP Error 403: Forbidden"

**Causes:**
1. Invalid or expired API key
2. Sender email not verified in SendGrid
3. API key lacks "Mail Send" permissions

**Solutions:**
1. Verify `SENDGRID_API_KEY` is correct (starts with `SG.`)
2. Check that your `EMAIL_DEFAULT_SENDER` is verified in the [SendGrid dashboard](https://app.sendgrid.com/settings/sender_auth)
3. Recreate API key with "Full Access" or "Mail Send" permissions

### Error: "Network is unreachable" (SMTP)

This is expected on Render. The application will automatically fallback to SendGrid if configured.

### Emails not arriving

1. Check SendGrid Activity Feed: [https://app.sendgrid.com/email_activity](https://app.sendgrid.com/email_activity)
2. Verify the recipient email is correct
3. Check spam/junk folders
4. Ensure you haven't exceeded SendGrid's daily limit (100 for free tier)

## Testing Locally

If testing locally, you can use SMTP:

```bash
# .env file for local development
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_DEFAULT_SENDER=your-email@gmail.com
SENDGRID_API_KEY=SG.your-key-here  # Optional fallback
```

## Configuration Check

Use the `/api/config/email` endpoint to check your configuration:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-app.onrender.com/api/config/email
```

Response includes:
- `smtp_configured`: Whether SMTP is fully configured
- `sendgrid_configured`: Whether SendGrid is configured
- `diagnosis`: Helpful diagnostic messages
- `missing_fields`: What's missing from your configuration

## Additional Resources

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [SendGrid Sender Verification](https://docs.sendgrid.com/ui/sending-email/sender-verification)
- [SendGrid API Keys](https://docs.sendgrid.com/ui/account-and-settings/api-keys)
