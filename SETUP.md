# Authentication & Competition Platform Setup

This application now uses **Supabase for authentication** and **MongoDB for data storage**.

## Architecture

- **Authentication**: Supabase Auth (email/password, Google, Facebook, LinkedIn)
- **Database**: MongoDB (existing Fair Measure DB)
- **Backend**: FastAPI with Motor (async MongoDB driver)
- **Frontend**: React with Vite

## Database Schema

### Collections

1. **profiles** - User profiles linked to Supabase auth users
   - `user_id` (Supabase auth user ID)
   - `email`
   - `full_name`
   - `avatar_url`
   - `provider` (email, google, facebook, linkedin)

2. **competitions** - Existing schema enhanced with:
   - `owner_id` (user_id from profiles)
   - All existing fields (name, type, rules, etc.)

3. **competition_members** - New collection for membership tracking
   - `competition_id`
   - `user_id`
   - `role` (owner or member)
   - `joined_at`

## Setup Instructions

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Configure Social Authentication (Optional)

To enable Google, Facebook, and LinkedIn login:

1. Go to your Supabase Dashboard
2. Navigate to Authentication > Providers
3. Enable and configure each provider with OAuth credentials

## Features

✅ Email/password registration and login
✅ Social authentication (Google, Facebook, LinkedIn)
✅ Automatic profile creation in MongoDB
✅ Competition creation with ownership
✅ Member management (add/remove members)
✅ Role-based access (owner vs member)
✅ Competition filtering (All, Owned, Member Of)
✅ Search users by email to add as members

## API Endpoints

### Profiles
- `POST /profiles/` - Create/sync profile
- `GET /profiles/` - List profiles (with email filter)
- `GET /profiles/user/{user_id}` - Get profile by Supabase user ID
- `PUT /profiles/{profile_id}` - Update profile

### Competitions
- `GET /competitions/` - List competitions (filter by owner_id or member_id)
- `POST /competitions/` - Create competition (auto-adds owner as member)
- `GET /competitions/{id}` - Get competition details

### Members
- `GET /members/competition/{competition_id}` - Get competition members with user details
- `POST /members/` - Add member to competition
- `DELETE /members/{member_id}` - Remove member from competition

## Environment Variables

Ensure `.env` file contains:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Notes

- Profiles are automatically created in MongoDB when users sign up via Supabase
- Competition owners are automatically added as members with 'owner' role
- Only competition owners can manage members
- Social login profiles are synced with MongoDB on first login
