import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../../supabaseClient'
import { gestisciCallbackOAuth } from '../../services/AuthService'

export default function CallbackOAuth() {
  const navigate = useNavigate()
  const [errore, setErrore] = useState('')
  const gestito = useRef(false)

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (gestito.current || event !== 'SIGNED_IN' || !session) return
      gestito.current = true

      try {
        const result = await gestisciCallbackOAuth(session.access_token)
        if (result.ruolo === 'UT') navigate('/utente/home')
        else if (result.ruolo === 'OP') navigate('/operatore/dashboard')
        else navigate('/ap/dashboard')
      } catch {
        setErrore('Autenticazione Google fallita. Riprova.')
        setTimeout(() => navigate('/'), 3000)
      }
    })

    return () => subscription.unsubscribe()
  }, [navigate])

  if (errore) return <div style={{ padding: 32, textAlign: 'center', color: '#d32f2f' }}>{errore}</div>
  return <div style={{ padding: 32, textAlign: 'center' }}>Accesso in corso...</div>
}
