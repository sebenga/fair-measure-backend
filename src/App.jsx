import { useState } from 'react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Login from './components/Auth/Login'
import Register from './components/Auth/Register'
import ProfileCard from './components/Profile/ProfileCard'
import CompetitionList from './components/Competition/CompetitionList'
import './App.css'

function AppContent() {
  const [showLogin, setShowLogin] = useState(true)
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  if (!user) {
    return showLogin ? (
      <Login onToggle={() => setShowLogin(false)} />
    ) : (
      <Register onToggle={() => setShowLogin(true)} />
    )
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Competition Platform</h1>
          <ProfileCard />
        </div>
      </header>
      <main className="app-main">
        <CompetitionList />
      </main>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}
