import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { autentica, registra, autenticaGoogle } from '../../services/AuthService'
import './VistaLogin.css'

const ERRORI: Record<number, string> = {
  401: 'Email o password non corretti',
  422: 'Password non valida. Deve contenere almeno 8 caratteri',
  423: 'Account bloccato. Riprova tra 15 minuti',
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

  const redirectDopoLogin = (ruolo: string) => {
    if (ruolo === 'UT') navigate('/utente/home')
    else if (ruolo === 'OP') navigate('/operatore/dashboard')
    else navigate('/ap/dashboard')
  }

  const handleSubmit = async (e: React.FormEvent) => {
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
        const result = await registra({ email, password, nome, cognome })
        redirectDopoLogin(result.ruolo)
      }
    } catch (err: unknown) {
      const status: number = (err as { response?: { status?: number } })?.response?.status ?? 0
      setErrore(ERRORI[status] ?? 'Servizio temporaneamente non disponibile')
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
          <span style={{ fontSize: 64 }}>🚲</span>
          <h1>SMART MOBILITY</h1>
        </div>

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
          <input
            className="login-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            autoComplete={modalita === 'login' ? 'current-password' : 'new-password'}
            aria-label="Password"
          />

          {modalita === 'login' && (
            <button type="button" className="link-recupero" onClick={() => {}}>
              Password dimenticata?
            </button>
          )}

          {errore && (
            <p className="login-errore" role="alert">
              {errore}
            </p>
          )}

          <button className="btn-primario" type="submit" disabled={caricamento}>
            {caricamento ? '...' : modalita === 'login' ? 'LOGIN' : 'REGISTRATI'}
          </button>
        </form>

        {/* SIGN UP — visibile solo su mobile (nascosto via CSS su desktop) */}
        <div className="signup-section">
          <p>Non sei ancora registrato?</p>
          <button
            className="btn-secondario"
            type="button"
            onClick={() => { setModalita('registrazione'); setErrore('') }}
          >
            SIGN UP
          </button>
        </div>

        {modalita === 'registrazione' && (
          <button
            className="btn-link"
            type="button"
            onClick={() => { setModalita('login'); setErrore('') }}
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
