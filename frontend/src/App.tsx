import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import VistaLogin from './views/auth/VistaLogin'
import RoutaProtetta from './components/RoutaProtetta'
import { utenteCorrente } from './services/AuthService'

function PlaceholderView({ titolo }: { titolo: string }) {
  return <div style={{ padding: 32 }}><h1>{titolo}</h1></div>
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
        <Route path="/non-autorizzato" element={<PlaceholderView titolo="Accesso non autorizzato" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
