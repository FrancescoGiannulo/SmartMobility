import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import VistaLogin from './views/auth/VistaLogin'
import CallbackOAuth from './views/auth/CallbackOAuth'
import RoutaProtetta from './components/RoutaProtetta'
import { utenteCorrente, logout } from './services/AuthService'

function PlaceholderView({ titolo }: { titolo: string }) {
  const navigate = useNavigate()
  const utente = utenteCorrente()
  const handleLogout = async () => {
    await logout()
    navigate('/', { replace: true })
  }
  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>{titolo}</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {utente && <span style={{ fontSize: 14, color: '#555' }}>{utente.profilo.email}</span>}
          <button
            onClick={handleLogout}
            style={{
              padding: '8px 20px',
              background: 'transparent',
              color: '#4caf9a',
              border: '2px solid #4caf9a',
              borderRadius: 24,
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            LOGOUT
          </button>
        </div>
      </div>
    </div>
  )
}

function App() {
  const utente = utenteCorrente()

  const homePerRuolo =
    utente?.ruolo === 'UT' ? '/utente/home' :
    utente?.ruolo === 'OP' ? '/operatore/dashboard' :
    utente?.ruolo === 'AP' ? '/ap/dashboard' : '/'

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={utente ? <Navigate to={homePerRuolo} replace /> : <VistaLogin />}
        />
        <Route
          path="/utente/*"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <PlaceholderView titolo="Homepage Utente" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/*"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <PlaceholderView titolo="Dashboard Operatore" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/ap/*"
          element={
            <RoutaProtetta ruoloRichiesto="AP">
              <PlaceholderView titolo="Dashboard AP" />
            </RoutaProtetta>
          }
        />
        <Route path="/auth/callback" element={<CallbackOAuth />} />
        <Route path="/non-autorizzato" element={<PlaceholderView titolo="Accesso non autorizzato" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
