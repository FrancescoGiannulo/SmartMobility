import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../../supabaseClient'
import { gestisciCallbackOAuth } from '../../services/AuthService'
import './CallbackOAuth.css'

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

  if (errore) return <div className="coauth__errore">{errore}</div>

  if (!tokenPendente) return <div className="coauth__loading">Accesso in corso…</div>

  return (
    <div className="coauth__wrap">
      <div className="coauth__card">
        <h2 className="coauth__titolo">Completa la registrazione</h2>
        <p className="coauth__desc">
          Per utilizzare Smart Mobility è necessario accettare il trattamento dei dati personali.
        </p>
        <form onSubmit={handleConsenso}>
          {/* [IIN-2 / GDPR art. 7] Consenso esplicito obbligatorio */}
          <label className="coauth__label">
            <input
              type="checkbox"
              className="coauth__checkbox"
              checked={consenso}
              onChange={e => setConsenso(e.target.checked)}
            />
            <span>
              Acconsento al trattamento dei miei dati personali ai sensi del{' '}
              <a href="/privacy-policy" target="_blank" rel="noopener noreferrer" className="coauth__link">
                Regolamento UE 2016/679 (GDPR)
              </a>.
              {' '}Il consenso è obbligatorio per la registrazione.
            </span>
          </label>
          <button
            type="submit"
            className="coauth__btn"
            disabled={!consenso || caricamento}
          >
            {caricamento ? '...' : 'ACCEDI'}
          </button>
        </form>
      </div>
    </div>
  )
}
