# Authentication Setup Guide

This application now uses **Supabase Authentication** with support for email/password and social logins.

## Supported Authentication Methods

- Email/Password (enabled by default)
- Google OAuth
- Facebook OAuth
- LinkedIn OAuth

## What's Already Configured

### Database
- `profiles` table created in Supabase
- Row Level Security (RLS) enabled with secure policies
- Automatic profile creation on signup
- User profile sync for social logins

### Frontend
- Login and Registration components with social login buttons
- AuthContext for managing authentication state
- Automatic session management
- Profile management functions

## Setup Social Login Providers

To enable social login, you need to configure OAuth providers in your Supabase dashboard:

### 1. Go to Supabase Dashboard
Navigate to: https://supabase.com/dashboard/project/pzyerpyvtmadzpdxrcxm

### 2. Configure Authentication Providers
Go to: **Authentication** → **Providers**

### 3. Enable and Configure Each Provider

#### Google OAuth
1. Click on Google provider
2. Enable the provider
3. Add your Google OAuth credentials:
   - Client ID
   - Client Secret
4. Add authorized redirect URL: `https://pzyerpyvtmadzpdxrcxm.supabase.co/auth/v1/callback`

[Get Google OAuth credentials](https://console.cloud.google.com/apis/credentials)

#### Facebook OAuth
1. Click on Facebook provider
2. Enable the provider
3. Add your Facebook App credentials:
   - App ID
   - App Secret
4. Add authorized redirect URL: `https://pzyerpyvtmadzpdxrcxm.supabase.co/auth/v1/callback`

[Get Facebook App credentials](https://developers.facebook.com/apps)

#### LinkedIn OAuth
1. Click on LinkedIn (OIDC) provider
2. Enable the provider
3. Add your LinkedIn App credentials:
   - Client ID
   - Client Secret
4. Add authorized redirect URL: `https://pzyerpyvtmadzpdxrcxm.supabase.co/auth/v1/callback`

[Get LinkedIn App credentials](https://www.linkedin.com/developers/apps)

## How Authentication Works

### Email/Password Registration
1. User fills registration form with name, email, and password
2. Account is created in Supabase Auth
3. Profile is automatically created in `profiles` table
4. User is logged in automatically

### Email/Password Login
1. User enters email and password
2. Supabase validates credentials
3. Session is created and user profile is loaded

### Social Login (Google/Facebook/LinkedIn)
1. User clicks social login button
2. Redirects to OAuth provider
3. User authorizes the app
4. Redirects back to application
5. Profile is automatically created in `profiles` table if it doesn't exist
6. User is logged in with session

## API Protection

All API endpoints can now be protected using Supabase authentication:

### Get Current User
```javascript
const { data: { user } } = await supabase.auth.getUser()
```

### Get User's Session Token
```javascript
const { data: { session } } = await supabase.auth.getSession()
const token = session?.access_token
```

### Protect API Calls
Send the token in API requests:
```javascript
fetch('your-api-endpoint', {
  headers: {
    'Authorization': `Bearer ${session.access_token}`
  }
})
```

## Testing Authentication

1. Start the frontend: `npm run dev`
2. Visit the application
3. Try registering with email/password
4. Try logging in with existing credentials
5. After configuring OAuth providers, test social logins

## Security Notes

- Email confirmation is disabled by default in Supabase
- All passwords are securely hashed by Supabase
- Sessions are managed automatically
- Row Level Security ensures users can only access their own data
- Social login profiles are synced automatically

## Database Schema

### profiles table
- `id` - Unique profile identifier
- `user_id` - Links to Supabase auth.users
- `email` - User's email
- `full_name` - User's display name
- `avatar_url` - Profile picture URL
- `provider` - Authentication provider (email, google, facebook, linkedin)
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp
