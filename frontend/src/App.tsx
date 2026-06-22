import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { APIProvider } from '@vis.gl/react-google-maps'
import VistaLogin from './views/auth/VistaLogin'
import CallbackOAuth from './views/auth/CallbackOAuth'
import RoutaProtetta from './components/RoutaProtetta'
import VistaHomePageUtente from './views/utente/VistaHomePageUtente'
import VistaMappaOperatore from './views/operatore/VistaMappaOperatore'
import VistaImpostazioniRegole from './views/operatore/VistaImpostazioniRegole'
import VistaCorsa from './views/utente/VistaCorsa'
import VistaDashboardAP from './views/amministrazione/VistaDashboardAP'
import VistaSegnalazione from './views/utente/VistaSegnalazione'
import VistaSegnalazioniOperatore from './views/operatore/VistaSegnalazioniOperatore'
import VistaPagamenti from './views/utente/VistaPagamenti'
import VistaTariffe from './views/operatore/VistaTariffe'
import VistaOfferte from './views/operatore/VistaOfferte'
import VistaMezziOperatore from './views/operatore/VistaMezziOperatore'
import VistaParametriSistema from './views/operatore/VistaParametriSistema'
import VistaAbbonamenti from './views/utente/VistaAbbonamenti'
import { utenteCorrente, logout } from './services/AuthService'
import VistaProfiloUtente from './views/utente/VistaProfiloUtente'
import VistaStoricoCorse from './views/utente/VistaStoricoCorse'
import VistaRecensione from './views/utente/VistaRecensione'
import VistaGestioneUtentiOperatore from './views/operatore/VistaGestioneUtentiOperatore'
import VistaRecensioniOperatore from './views/operatore/VistaRecensioniOperatore'
import PrivacyPolicy from './views/PrivacyPolicy'
import { TourProvider } from './tour/TourProvider'
import { TourOverlay } from './tour/TourOverlay'
import { tourHomepageUtente } from './tour/tours/tourHomepageUtente'

const MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string

const TOURS = {
  [tourHomepageUtente.id]: tourHomepageUtente,
}

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
            type="button"
            onClick={handleLogout}
            style={{
              padding: '8px 20px',
              background: 'transparent',
              color: '#155e52',
              border: '2px solid #155e52',
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

// Componente separato: chiama utenteCorrente() fresco ad ogni mount,
// evitando stale closure quando App non si ri-renderizza dopo logout.
function RoutaIniziale() {
  const utente = utenteCorrente()
  const homePerRuolo =
    utente?.ruolo === 'UT' ? '/utente/home' :
    utente?.ruolo === 'OP' ? '/operatore/dashboard' :
    utente?.ruolo === 'AP' ? '/ap/dashboard' : '/'
  return utente ? <Navigate to={homePerRuolo} replace /> : <VistaLogin />
}

function App() {
  return (
    <APIProvider apiKey={MAPS_API_KEY} version="quarterly" libraries={['drawing']}>
    {/* [IIN-3 / WCAG 1.3.1 + 2.4.1] Landmark main + destinazione skip-link */}
    <BrowserRouter>
    <TourProvider tours={TOURS}>
    <main id="main-content" tabIndex={-1} style={{ outline: 'none' }}>
      <Routes>
        <Route path="/" element={<RoutaIniziale />} />
        <Route
          path="/utente/home"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaHomePageUtente />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/corsa/:idMezzo"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaCorsa />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/segnalazione"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaSegnalazione />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/recensione"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaRecensione />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/pagamenti"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaPagamenti />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/abbonamenti"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaAbbonamenti />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/profilo"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaProfiloUtente />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/storico"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaStoricoCorse />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/*"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <PlaceholderView titolo="Utente" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/dashboard"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaMappaOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/segnalazioni"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaSegnalazioniOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/utenti"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaGestioneUtentiOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/tariffe"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaTariffe />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/offerte"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaOfferte />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/impostazioni-regole"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaImpostazioniRegole />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/mezzi"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaMezziOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/parametri-sistema"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaParametriSistema />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/recensioni"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaRecensioniOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/*"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <PlaceholderView titolo="Operatore" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/ap/dashboard"
          element={
            <RoutaProtetta ruoloRichiesto="AP">
              <VistaDashboardAP />
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
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/non-autorizzato" element={<PlaceholderView titolo="Accesso non autorizzato" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </main>
    <TourOverlay tours={TOURS} />
    </TourProvider>
    </BrowserRouter>
    </APIProvider>
  )
}

export default App
