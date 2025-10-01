import { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import CompetitionCard from './CompetitionCard'
import CreateCompetition from './CreateCompetition'
import './Competition.css'

const API_URL = 'http://localhost:8000'

export default function CompetitionList() {
  const [competitions, setCompetitions] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [filter, setFilter] = useState('all')
  const { user, profile } = useAuth()

  useEffect(() => {
    if (user && profile) {
      fetchCompetitions()
    }
  }, [filter, user, profile])

  const fetchCompetitions = async () => {
    try {
      setLoading(true)
      let url = `${API_URL}/competitions/`

      if (filter === 'owned') {
        url += `?owner_id=${user.id}`
      } else if (filter === 'member') {
        url += `?member_id=${user.id}`
      }

      const response = await fetch(url)
      if (!response.ok) throw new Error('Failed to fetch competitions')

      const data = await response.json()

      const enrichedData = await Promise.all(
        data.map(async (comp) => {
          const membersResponse = await fetch(`${API_URL}/members/competition/${comp.id}`)
          const members = membersResponse.ok ? await membersResponse.json() : []
          return { ...comp, competition_members: members }
        })
      )

      setCompetitions(enrichedData)
    } catch (error) {
      console.error('Error fetching competitions:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="competition-list-container">
      <div className="competition-header">
        <h1>Competitions</h1>
        <button onClick={() => setShowCreate(true)} className="btn btn-primary">
          Create Competition
        </button>
      </div>

      <div className="filter-tabs">
        <button
          className={`filter-tab ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={`filter-tab ${filter === 'owned' ? 'active' : ''}`}
          onClick={() => setFilter('owned')}
        >
          My Competitions
        </button>
        <button
          className={`filter-tab ${filter === 'member' ? 'active' : ''}`}
          onClick={() => setFilter('member')}
        >
          Member Of
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading competitions...</div>
      ) : competitions.length === 0 ? (
        <div className="empty-state">
          <p>No competitions found</p>
          <button onClick={() => setShowCreate(true)} className="btn btn-primary">
            Create Your First Competition
          </button>
        </div>
      ) : (
        <div className="competition-grid">
          {competitions.map((competition) => (
            <CompetitionCard
              key={competition.id}
              competition={competition}
              onUpdate={fetchCompetitions}
            />
          ))}
        </div>
      )}

      {showCreate && (
        <CreateCompetition
          onClose={() => setShowCreate(false)}
          onSuccess={() => {
            setShowCreate(false)
            fetchCompetitions()
          }}
        />
      )}
    </div>
  )
}
