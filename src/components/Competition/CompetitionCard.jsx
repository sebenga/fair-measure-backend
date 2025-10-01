import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import ManageMembers from './ManageMembers'

export default function CompetitionCard({ competition, onUpdate }) {
  const [showMembers, setShowMembers] = useState(false)
  const { user } = useAuth()

  const isOwner = competition.owner_id === user?.id
  const memberCount = competition.competition_members?.length || 0

  return (
    <>
      <div className="competition-card">
        {competition.logo_location && (
          <div className="competition-logo">
            <img src={competition.logo_location} alt={competition.name} />
          </div>
        )}
        <div className="competition-content">
          <div className="competition-title-row">
            <h3>{competition.name}</h3>
            {competition.is_private && <span className="private-badge">Private</span>}
          </div>
          <p className="competition-type">{competition.type}</p>
          <p className="competition-owner">
            Owner: {competition.author || 'Unknown'}
          </p>
          <div className="competition-stats">
            <span>{memberCount} {memberCount === 1 ? 'member' : 'members'}</span>
          </div>
          {isOwner && (
            <button
              onClick={() => setShowMembers(true)}
              className="btn btn-secondary"
              style={{ marginTop: '12px', width: '100%' }}
            >
              Manage Members
            </button>
          )}
        </div>
      </div>

      {showMembers && (
        <ManageMembers
          competition={competition}
          onClose={() => setShowMembers(false)}
          onUpdate={onUpdate}
        />
      )}
    </>
  )
}
