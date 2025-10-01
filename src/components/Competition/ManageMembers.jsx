import { useState, useEffect } from 'react'

const API_URL = 'http://localhost:8000'

export default function ManageMembers({ competition, onClose, onUpdate }) {
  const [members, setMembers] = useState([])
  const [searchEmail, setSearchEmail] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchMembers()
  }, [competition.id])

  const fetchMembers = async () => {
    try {
      const response = await fetch(`${API_URL}/members/competition/${competition.id}`)
      if (!response.ok) throw new Error('Failed to fetch members')

      const data = await response.json()
      setMembers(data || [])
    } catch (err) {
      console.error('Error fetching members:', err)
    }
  }

  const searchUsers = async (email) => {
    if (!email || email.length < 3) {
      setSearchResults([])
      return
    }

    try {
      const response = await fetch(`${API_URL}/profiles/?email=${encodeURIComponent(email)}`)
      if (!response.ok) throw new Error('Failed to search users')

      const data = await response.json()
      const currentMemberIds = members.map(m => m.user.user_id)
      const filteredResults = (data || []).filter(
        user => !currentMemberIds.includes(user.user_id)
      )
      setSearchResults(filteredResults)
    } catch (err) {
      console.error('Error searching users:', err)
    }
  }

  const addMember = async (userId) => {
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/members/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          competition_id: competition.id,
          user_id: userId,
          role: 'member'
        })
      })

      if (!response.ok) throw new Error('Failed to add member')

      setSearchEmail('')
      setSearchResults([])
      await fetchMembers()
      onUpdate()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const removeMember = async (memberId) => {
    if (!confirm('Are you sure you want to remove this member?')) return

    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/members/${memberId}`, {
        method: 'DELETE'
      })

      if (!response.ok) throw new Error('Failed to remove member')

      await fetchMembers()
      onUpdate()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Manage Members - {competition.name}</h2>
          <button onClick={onClose} className="close-button">&times;</button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="modal-body">
          <div className="add-member-section">
            <h3>Add Member</h3>
            <div className="search-container">
              <input
                type="email"
                value={searchEmail}
                onChange={(e) => {
                  setSearchEmail(e.target.value)
                  searchUsers(e.target.value)
                }}
                placeholder="Search by email"
                className="search-input"
              />
              {searchResults.length > 0 && (
                <div className="search-results">
                  {searchResults.map((user) => (
                    <div key={user.id} className="search-result-item">
                      <div className="user-info">
                        <strong>{user.full_name || 'User'}</strong>
                        <span>{user.email}</span>
                      </div>
                      <button
                        onClick={() => addMember(user.id)}
                        className="btn btn-sm btn-primary"
                        disabled={loading}
                      >
                        Add
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="members-section">
            <h3>Current Members ({members.length})</h3>
            <div className="members-list">
              {members.map((member) => (
                <div key={member.id} className="member-item">
                  <div className="member-avatar">
                    {member.user.avatar_url ? (
                      <img src={member.user.avatar_url} alt={member.user.full_name || 'User'} />
                    ) : (
                      <div className="avatar-placeholder-sm">
                        {(member.user.full_name || member.user.email || 'U')[0].toUpperCase()}
                      </div>
                    )}
                  </div>
                  <div className="member-info">
                    <strong>{member.user.full_name || 'User'}</strong>
                    <span>{member.user.email}</span>
                  </div>
                  <span className={`role-badge ${member.role}`}>{member.role}</span>
                  {member.role !== 'owner' && (
                    <button
                      onClick={() => removeMember(member.id)}
                      className="btn btn-sm btn-danger"
                      disabled={loading}
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
