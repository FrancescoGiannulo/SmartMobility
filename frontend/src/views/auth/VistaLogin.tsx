import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { autentica, registra, autenticaGoogle } from '../../services/AuthService'
import './VistaLogin.css'

const ERRORI: Record<number, string> = {
  401: 'Email o password non corretti',
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
            <a className="link-recupero" href="/recupero-password">
              Forgot Password?
            </a>
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
            className="btn-social"
            type="button"
            onClick={handleGoogle}
            aria-label="Accedi con Google"
          >
            G
          </button>
          <button
            className="btn-social"
            type="button"
            disabled
            aria-label="Accedi con Apple (non disponibile)"
          >

          </button>
        </div>
      </div>
    </div>
  )
}
