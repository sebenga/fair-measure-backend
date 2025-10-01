import { useAuth } from '../../contexts/AuthContext'
import './Profile.css'

export default function ProfileCard() {
  const { profile, user, signOut } = useAuth()

  const handleSignOut = async () => {
    await signOut()
  }

  if (!profile) return null

  return (
    <div className="profile-card">
      <div className="profile-header">
        <div className="profile-avatar">
          {profile.avatar_url ? (
            <img src={profile.avatar_url} alt={profile.full_name || 'User'} />
          ) : (
            <div className="avatar-placeholder">
              {(profile.full_name || profile.email || 'U')[0].toUpperCase()}
            </div>
          )}
        </div>
        <div className="profile-info">
          <h3>{profile.full_name || 'User'}</h3>
          <p>{profile.email}</p>
          <span className="provider-badge">{profile.provider}</span>
        </div>
      </div>
      <button onClick={handleSignOut} className="btn btn-secondary">
        Sign Out
      </button>
    </div>
  )
}
