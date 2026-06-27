import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { autentica, registra, autenticaGoogle } from '../../services/AuthService'
import './VistaLogin.css'

const ERRORI: Record<number, string> = {
  401: 'Email o password non corretti',
  422: 'Password non valida. Deve contenere almeno 8 caratteri',
  423: 'Account bloccato per troppi tentativi falliti. Riprova più tardi.',
  403: 'Account sospeso. Contatta il supporto',
  409: 'Email già registrata',
}

type Modalita = 'login' | 'registrazione'

export default function VistaLogin() {
  const navigate = useNavigate()
  const [modalita, setModalita] = useState<Modalita>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nome, setNome] = useState('')
  const [cognome, setCognome] = useState('')
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)
  const [consensoPrivacy, setConsensoPrivacy] = useState(false)
  const [mostraPassword, setMostraPassword] = useState(false)

  const redirectDopoLogin = (ruolo: string) => {
    if (ruolo === 'UT') navigate('/utente/home')
    else if (ruolo === 'OP') navigate('/operatore/dashboard')
    else navigate('/ap/dashboard')
  }

  const handleSubmit = async (e: { preventDefault(): void }) => {
    e.preventDefault()
    setErrore('')
    if (modalita === 'registrazione' && password.length < 8) {
      setErrore('Password non idonea: deve contenere almeno 8 caratteri')
      return
    }
    setCaricamento(true)
    try {
      if (modalita === 'login') {
        const result = await autentica({ email, password })
        redirectDopoLogin(result.ruolo)
      } else {
        const result = await registra({ email, password, nome, cognome, consenso_privacy: consensoPrivacy })
        redirectDopoLogin(result.ruolo)
      }
    } catch (err: unknown) {
      const response = (err as { response?: { status?: number; data?: { detail?: string } } })?.response
      const status = response?.status ?? 0
      if (status === 403) {
        // [IF-OP.09] Il backend include la motivazione della sospensione nel detail
        // come "Account sospeso: <motivazione>" — la estraiamo per mostrarla all'utente.
        const detail = response?.data?.detail ?? ''
        const motivazione = detail.startsWith('Account sospeso: ')
          ? detail.slice('Account sospeso: '.length)
          : null
        setErrore(
          motivazione
            ? `Account sospeso. Motivo: ${motivazione}. Contatta il supporto.`
            : ERRORI[403],
        )
      } else {
        setErrore(ERRORI[status] ?? 'Servizio temporaneamente non disponibile')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const handleGoogle = async () => {
    try {
      await autenticaGoogle()
    } catch {
      setErrore('Accesso con Google non disponibile')
    }
  }

  return (
    <div className="vista-login">
      <div className="login-card">
        <div className="login-logo">
          <div className="logo-wrapper">
            <img src="/logo.png" alt="Smart Mobility" style={{ width: 180, height: 'auto' }} />
          </div>
        </div>

        <h1 className="login-heading">
          {modalita === 'login' ? 'Bentornato.' : 'Registrati.'}
        </h1>

        <form onSubmit={handleSubmit}>
          {modalita === 'registrazione' && (
            <>
              <input
                className="login-input"
                type="text"
                placeholder="Nome"
                value={nome}
                onChange={e => setNome(e.target.value)}
                required
                aria-label="Nome"
              />
              <input
                className="login-input"
                type="text"
                placeholder="Cognome"
                value={cognome}
                onChange={e => setCognome(e.target.value)}
                required
                aria-label="Cognome"
              />
            </>
          )}

          <input
            className="login-input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            autoComplete="email"
            aria-label="Email"
          />
          <div className="login-password-wrap">
            <input
              className="login-input"
              type={mostraPassword ? 'text' : 'password'}
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              autoComplete={modalita === 'login' ? 'current-password' : 'new-password'}
              aria-label="Password"
            />
            <button
              type="button"
              className="btn-mostra-password"
              onClick={() => setMostraPassword(p => !p)}
              aria-label={mostraPassword ? 'Nascondi password' : 'Mostra password'}
            >
              {mostraPassword ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              )}
            </button>
          </div>

          {modalita === 'login' && (
            <button type="button" className="link-recupero" onClick={() => {}}>
              Password dimenticata?
            </button>
          )}

          {/* [IIN-2 / GDPR art. 7] Consenso esplicito al trattamento dati */}
          {modalita === 'registrazione' && (
            <label
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 10,
                fontSize: 13,
                color: 'var(--text-dim)',
                cursor: 'pointer',
                marginTop: 4,
              }}
            >
              <input
                type="checkbox"
                id="consenso-privacy"
                checked={consensoPrivacy}
                onChange={e => setConsensoPrivacy(e.target.checked)}
                style={{ marginTop: 2, flexShrink: 0, accentColor: 'var(--accent)' }}
              />
              <span>
                Acconsento al trattamento dei miei dati personali ai sensi del{' '}
                <a
                  href="/privacy-policy"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--accent)', fontWeight: 600 }}
                >
                  Regolamento UE 2016/679 (GDPR)
                </a>.
                {' '}Il consenso è obbligatorio per la registrazione.
              </span>
            </label>
          )}

          {errore && (
            <p className="login-errore" role="alert">
              {errore}
            </p>
          )}

          <button
            className="btn-primario"
            type="submit"
            disabled={caricamento || (modalita === 'registrazione' && !consensoPrivacy)}
          >
            {caricamento ? '...' : modalita === 'login' ? 'LOGIN' : 'REGISTRATI'}
          </button>
        </form>

        {/* SIGN UP — visibile solo su mobile (nascosto via CSS su desktop) */}
        <div className="signup-section">
          <p>Non sei ancora registrato?</p>
          <button
            className="btn-secondario"
            type="button"
            onClick={() => { setModalita('registrazione'); setErrore(''); setConsensoPrivacy(false) }}
          >
            SIGN UP
          </button>
        </div>

        {modalita === 'registrazione' && (
          <button
            className="btn-link"
            type="button"
            onClick={() => { setModalita('login'); setErrore(''); setConsensoPrivacy(false) }}
          >
            Hai già un account? LOGIN
          </button>
        )}

        <div className="social-login">
          <button
            className="btn-google"
            type="button"
            onClick={handleGoogle}
            aria-label="Accedi con Google"
          >
            <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
              <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
              <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
              <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
              <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
            </svg>
            Accedi con Google
          </button>
        </div>
      </div>
    </div>
  )
}
