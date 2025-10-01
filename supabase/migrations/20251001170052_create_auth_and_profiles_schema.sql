/*
  # Authentication and Profile Management Schema

  ## Overview
  Sets up the complete authentication system with profiles, competitions, and membership management.

  ## 1. New Tables
  
  ### `profiles`
  - `id` (uuid, primary key) - Links to auth.users
  - `email` (text) - User email
  - `full_name` (text) - User's full name
  - `avatar_url` (text) - Profile picture URL
  - `provider` (text) - Auth provider (google, facebook, linkedin, email)
  - `created_at` (timestamptz) - Profile creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `competitions`
  - `id` (uuid, primary key)
  - `name` (text) - Competition name
  - `owner_id` (uuid, foreign key) - References profiles(id)
  - `date_created` (timestamptz) - Creation timestamp
  - `logo_location` (text) - Logo URL
  - `is_private` (boolean) - Privacy setting
  - `type` (text) - Competition type
  - `rules` (jsonb) - Competition rules
  - `scoring_categories` (jsonb) - Scoring categories
  - `point_accumulation` (jsonb) - Point system
  - `default_photo_repositories` (jsonb) - Photo repos
  - `default_video_repositories` (jsonb) - Video repos
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### `competition_members`
  - `id` (uuid, primary key)
  - `competition_id` (uuid, foreign key) - References competitions(id)
  - `user_id` (uuid, foreign key) - References profiles(id)
  - `role` (text) - 'owner' or 'member'
  - `joined_at` (timestamptz) - Membership timestamp
  - Unique constraint on (competition_id, user_id)

  ## 2. Security
  - Enable RLS on all tables
  - Profiles: Users can read all profiles, but only update their own
  - Competitions: Public competitions are readable by all, private only by members
  - Competition members: Members can view membership, owners can manage
  
  ## 3. Functions
  - Automatic profile creation trigger on user signup
  - Function to check competition membership
*/

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text UNIQUE NOT NULL,
  full_name text,
  avatar_url text,
  provider text DEFAULT 'email',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create competitions table
CREATE TABLE IF NOT EXISTS competitions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  owner_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  date_created timestamptz DEFAULT now(),
  logo_location text,
  is_private boolean DEFAULT false,
  type text NOT NULL,
  rules jsonb DEFAULT '[]'::jsonb,
  scoring_categories jsonb DEFAULT '[]'::jsonb,
  point_accumulation jsonb DEFAULT '{}'::jsonb,
  default_photo_repositories jsonb DEFAULT '[]'::jsonb,
  default_video_repositories jsonb DEFAULT '[]'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create competition_members table
CREATE TABLE IF NOT EXISTS competition_members (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  competition_id uuid NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('owner', 'member')),
  joined_at timestamptz DEFAULT now(),
  UNIQUE(competition_id, user_id)
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE competition_members ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

-- Competitions policies
CREATE POLICY "Public competitions are viewable by everyone"
  ON competitions FOR SELECT
  TO authenticated
  USING (
    is_private = false
    OR owner_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM competition_members
      WHERE competition_members.competition_id = competitions.id
      AND competition_members.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can create competitions"
  ON competitions FOR INSERT
  TO authenticated
  WITH CHECK (owner_id = auth.uid());

CREATE POLICY "Owners can update their competitions"
  ON competitions FOR UPDATE
  TO authenticated
  USING (owner_id = auth.uid())
  WITH CHECK (owner_id = auth.uid());

CREATE POLICY "Owners can delete their competitions"
  ON competitions FOR DELETE
  TO authenticated
  USING (owner_id = auth.uid());

-- Competition members policies
CREATE POLICY "Members can view competition memberships"
  ON competition_members FOR SELECT
  TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM competitions
      WHERE competitions.id = competition_members.competition_id
      AND competitions.owner_id = auth.uid()
    )
    OR EXISTS (
      SELECT 1 FROM competition_members cm
      WHERE cm.competition_id = competition_members.competition_id
      AND cm.user_id = auth.uid()
    )
  );

CREATE POLICY "Competition owners can add members"
  ON competition_members FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM competitions
      WHERE competitions.id = competition_members.competition_id
      AND competitions.owner_id = auth.uid()
    )
  );

CREATE POLICY "Competition owners can remove members"
  ON competition_members FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM competitions
      WHERE competitions.id = competition_members.competition_id
      AND competitions.owner_id = auth.uid()
    )
  );

CREATE POLICY "Members can leave competitions"
  ON competition_members FOR DELETE
  TO authenticated
  USING (user_id = auth.uid() AND role = 'member');

-- Function to automatically create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, avatar_url, provider)
  VALUES (
    NEW.id,
    NEW.email,
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url',
    COALESCE(NEW.raw_user_meta_data->>'provider', 'email')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
DROP TRIGGER IF EXISTS profiles_updated_at ON profiles;
CREATE TRIGGER profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS competitions_updated_at ON competitions;
CREATE TRIGGER competitions_updated_at
  BEFORE UPDATE ON competitions
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Function to automatically add owner as member
CREATE OR REPLACE FUNCTION public.add_owner_as_member()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.competition_members (competition_id, user_id, role)
  VALUES (NEW.id, NEW.owner_id, 'owner');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to add owner as member
DROP TRIGGER IF EXISTS on_competition_created ON competitions;
CREATE TRIGGER on_competition_created
  AFTER INSERT ON competitions
  FOR EACH ROW EXECUTE FUNCTION public.add_owner_as_member();

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);
CREATE INDEX IF NOT EXISTS idx_competitions_owner ON competitions(owner_id);
CREATE INDEX IF NOT EXISTS idx_competitions_private ON competitions(is_private);
CREATE INDEX IF NOT EXISTS idx_competition_members_competition ON competition_members(competition_id);
CREATE INDEX IF NOT EXISTS idx_competition_members_user ON competition_members(user_id);
