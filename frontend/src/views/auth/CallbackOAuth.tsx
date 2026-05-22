import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { gestisciCallbackOAuth } from '../../services/AuthService'

export default function CallbackOAuth() {
  const navigate = useNavigate()
  const [errore, setErrore] = useState('')

  useEffect(() => {
    gestisciCallbackOAuth()
      .then(result => {
        if (!result) { navigate('/'); return }
        if (result.ruolo === 'UT') navigate('/utente/home')
        else if (result.ruolo === 'OP') navigate('/operatore/dashboard')
        else navigate('/ap/dashboard')
      })
      .catch(() => {
        setErrore('Autenticazione Google fallita. Riprova.')
        setTimeout(() => navigate('/'), 3000)
      })
  }, [navigate])

  if (errore) return <div style={{ padding: 32, textAlign: 'center', color: '#d32f2f' }}>{errore}</div>
  return <div style={{ padding: 32, textAlign: 'center' }}>Accesso in corso...</div>
}
