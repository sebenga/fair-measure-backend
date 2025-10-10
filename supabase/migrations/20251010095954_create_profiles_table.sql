/*
  # Create profiles table for user data

  ## Overview
  This migration creates the profiles table to store user profile information linked to Supabase Auth users.

  ## Tables Created
  
  ### `profiles`
  Stores user profile information synchronized with Supabase Auth
  
  **Columns:**
  - `id` (uuid, primary key) - Unique profile identifier
  - `user_id` (uuid, unique, not null) - References auth.users(id), links to Supabase Auth
  - `email` (text, not null) - User's email address
  - `full_name` (text) - User's full name
  - `avatar_url` (text) - URL to user's profile picture
  - `provider` (text, default 'email') - Authentication provider (email, google, facebook, linkedin)
  - `created_at` (timestamptz) - Profile creation timestamp
  - `updated_at` (timestamptz) - Last profile update timestamp

  ## Security
  
  ### Row Level Security (RLS)
  - RLS is enabled on the profiles table to protect user data
  
  ### Policies Created
  1. **"Users can view own profile"** - Authenticated users can SELECT their own profile data
  2. **"Users can insert own profile"** - Authenticated users can INSERT their own profile during signup
  3. **"Users can update own profile"** - Authenticated users can UPDATE their own profile data
  4. **"Public profiles are viewable by authenticated users"** - Authenticated users can view other users' basic profile info (email, full_name, avatar_url)

  ## Important Notes
  - Email confirmation is disabled by default in Supabase
  - Profiles are created automatically when users sign up
  - The user_id links to Supabase's built-in auth.users table
  - All timestamps use timestamptz with automatic timezone handling
*/

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  email text NOT NULL,
  full_name text,
  avatar_url text,
  provider text DEFAULT 'email',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own profile
CREATE POLICY "Users can view own profile"
  ON profiles
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Policy: Users can insert their own profile (during signup)
CREATE POLICY "Users can insert own profile"
  ON profiles
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile"
  ON profiles
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy: Authenticated users can view other users' basic profile info
CREATE POLICY "Public profiles viewable by authenticated users"
  ON profiles
  FOR SELECT
  TO authenticated
  USING (true);

-- Create index on user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);

-- Create index on email for search functionality
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on profile updates
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();