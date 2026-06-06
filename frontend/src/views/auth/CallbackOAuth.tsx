import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../../supabaseClient'
import { gestisciCallbackOAuth } from '../../services/AuthService'

export default function CallbackOAuth() {
  const navigate = useNavigate()
  const [errore, setErrore] = useState('')
  const [tokenPendente, setTokenPendente] = useState<string | null>(null)
  const [consenso, setConsenso] = useState(false)
  const [caricamento, setCaricamento] = useState(false)
  const gestito = useRef(false)

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (gestito.current || event !== 'SIGNED_IN' || !session) return
      gestito.current = true
      // [IIN-2 / GDPR art. 7] Sospende il flusso per raccogliere il consenso esplicito
      setTokenPendente(session.access_token)
    })

    return () => subscription.unsubscribe()
  }, [])

  const handleConsenso = async (e: { preventDefault(): void }) => {
    e.preventDefault()
    if (!tokenPendente) return
    setCaricamento(true)
    try {
      const result = await gestisciCallbackOAuth(tokenPendente, consenso)
      if (result.ruolo === 'UT') navigate('/utente/home')
      else if (result.ruolo === 'OP') navigate('/operatore/dashboard')
      else navigate('/ap/dashboard')
    } catch {
      setErrore('Autenticazione Google fallita. Riprova.')
      setTimeout(() => navigate('/'), 3000)
    } finally {
      setCaricamento(false)
    }
  }

  if (errore) return <div style={{ padding: 32, textAlign: 'center', color: '#d32f2f' }}>{errore}</div>

  if (!tokenPendente) return <div style={{ padding: 32, textAlign: 'center' }}>Accesso in corso…</div>

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f5f5f5' }}>
      <div style={{ background: '#fff', borderRadius: 16, padding: '40px 32px', maxWidth: 420, width: '100%', boxShadow: '0 4px 24px rgba(0,0,0,0.10)' }}>
        <h2 style={{ marginBottom: 8, fontSize: 22, color: '#222' }}>Completa la registrazione</h2>
        <p style={{ color: '#555', fontSize: 14, marginBottom: 24 }}>
          Per utilizzare Smart Mobility è necessario accettare il trattamento dei dati personali.
        </p>
        <form onSubmit={handleConsenso}>
          {/* [IIN-2 / GDPR art. 7] Consenso esplicito obbligatorio */}
          <label style={{ display: 'flex', alignItems: 'flex-start', gap: 10, fontSize: 13, color: '#555', cursor: 'pointer', marginBottom: 24 }}>
            <input
              type="checkbox"
              checked={consenso}
              onChange={e => setConsenso(e.target.checked)}
              style={{ marginTop: 2, flexShrink: 0, accentColor: '#155e52' }}
            />
            <span>
              Acconsento al trattamento dei miei dati personali ai sensi del{' '}
              <a href="/privacy-policy" target="_blank" rel="noopener noreferrer" style={{ color: '#155e52', fontWeight: 600 }}>
                Regolamento UE 2016/679 (GDPR)
              </a>.
              {' '}Il consenso è obbligatorio per la registrazione.
            </span>
          </label>
          <button
            type="submit"
            disabled={!consenso || caricamento}
            style={{
              width: '100%',
              padding: '12px 0',
              background: consenso ? '#155e52' : '#ccc',
              color: '#fff',
              border: 'none',
              borderRadius: 24,
              fontWeight: 700,
              fontSize: 15,
              cursor: consenso ? 'pointer' : 'not-allowed',
              transition: 'background 0.2s',
            }}
          >
            {caricamento ? '...' : 'ACCEDI'}
          </button>
        </form>
      </div>
    </div>
  )
}
