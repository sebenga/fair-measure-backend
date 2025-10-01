import { useState, useEffect } from 'react'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../contexts/AuthContext'
import CompetitionCard from './CompetitionCard'
import CreateCompetition from './CreateCompetition'
import './Competition.css'

export default function CompetitionList() {
  const [competitions, setCompetitions] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [filter, setFilter] = useState('all')
  const { user } = useAuth()

  useEffect(() => {
    fetchCompetitions()
  }, [filter, user])

  const fetchCompetitions = async () => {
    try {
      setLoading(true)
      let query = supabase
        .from('competitions')
        .select(`
          *,
          owner:profiles!competitions_owner_id_fkey(id, full_name, email),
          competition_members(user_id, role)
        `)
        .order('created_at', { ascending: false })

      if (filter === 'owned') {
        query = query.eq('owner_id', user.id)
      } else if (filter === 'member') {
        query = query.in('id',
          supabase
            .from('competition_members')
            .select('competition_id')
            .eq('user_id', user.id)
            .neq('role', 'owner')
        )
      }

      const { data, error } = await query

      if (error) throw error
      setCompetitions(data || [])
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
