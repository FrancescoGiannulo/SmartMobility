import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/ApiService'
import { logout, utenteCorrente } from '../../services/AuthService'
import './VistaProfiloUtente.css'

export default function VistaProfiloUtente() {
  const navigate = useNavigate()
  const utente = utenteCorrente()
  const [statoExport, setStatoExport] = useState<'idle' | 'loading' | 'done' | 'error'>('idle')
  const [statoElimina, setStatoElimina] = useState<'idle' | 'confirm' | 'loading' | 'error'>('idle')
  const [errore, setErrore] = useState('')

  const handleExport = async () => {
    setStatoExport('loading')
    setErrore('')
    try {
      const resp = await api.get('/utente/dati-personali')
      const blob = new Blob([JSON.stringify(resp.data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `smartmobility-dati-personali.json`
      a.click()
      URL.revokeObjectURL(url)
      setStatoExport('done')
    } catch {
      setStatoExport('error')
      setErrore('Impossibile scaricare i dati. Riprova.')
    }
  }

  const handleElimina = async () => {
    setStatoElimina('loading')
    setErrore('')
    try {
      await api.delete('/utente/account')
      await logout()
      navigate('/', { replace: true })
    } catch {
      setStatoElimina('error')
      setErrore('Impossibile eliminare l\'account. Riprova o contatta il supporto.')
    }
  }

  return (
    <div className="profilo-container">
      <div className="profilo-card">
        <button className="profilo-back" onClick={() => navigate(-1)} aria-label="Torna indietro">
          ← Indietro
        </button>

        <h1 className="profilo-titolo">Il mio profilo</h1>

        {utente && (
          <div className="profilo-info">
            <div className="profilo-info-row">
              <span className="profilo-label">Nome</span>
              <span className="profilo-valore">{utente.profilo.nome} {utente.profilo.cognome}</span>
            </div>
            <div className="profilo-info-row">
              <span className="profilo-label">Email</span>
              <span className="profilo-valore">{utente.profilo.email}</span>
            </div>
            <div className="profilo-info-row">
              <span className="profilo-label">Ruolo</span>
              <span className="profilo-badge">{utente.ruolo}</span>
            </div>
          </div>
        )}

        {/* ── GDPR ───────────────────────────────────────────── */}
        <section className="profilo-sezione">
          <h2 className="profilo-sezione-titolo">Privacy e dati personali</h2>
          <p className="profilo-sezione-desc">
            In conformità al{' '}
            <a href="/privacy-policy" target="_blank" rel="noopener noreferrer" className="profilo-link">
              Regolamento UE 2016/679 (GDPR)
            </a>
            , puoi scaricare una copia dei tuoi dati o richiedere la cancellazione del tuo account.
          </p>

          <div className="profilo-azioni">
            {/* Export dati — art. 20 */}
            <div className="profilo-azione-card">
              <div className="profilo-azione-icon">📥</div>
              <div>
                <h3>Scarica i tuoi dati</h3>
                <p>Ricevi un file JSON con profilo e storico corse (art. 20 GDPR — portabilità).</p>
              </div>
              <button
                className="profilo-btn-export"
                onClick={handleExport}
                disabled={statoExport === 'loading'}
              >
                {statoExport === 'loading' ? 'Scaricamento…' :
                 statoExport === 'done' ? '✓ Scaricato' : 'Scarica'}
              </button>
            </div>

            {/* Cancellazione account — art. 17 */}
            <div className="profilo-azione-card profilo-azione-danger">
              <div className="profilo-azione-icon">🗑️</div>
              <div>
                <h3>Elimina account</h3>
                <p>Cancella definitivamente il tuo account e tutti i dati personali (art. 17 GDPR — diritto all'oblio). Questa azione è irreversibile.</p>
              </div>
              {statoElimina === 'idle' && (
                <button
                  className="profilo-btn-danger"
                  onClick={() => setStatoElimina('confirm')}
                >
                  Elimina
                </button>
              )}
              {statoElimina === 'confirm' && (
                <div className="profilo-confirm">
                  <p className="profilo-confirm-testo">Sei sicuro? L'operazione è irreversibile.</p>
                  <div className="profilo-confirm-azioni">
                    <button className="profilo-btn-danger" onClick={handleElimina}>
                      Sì, elimina
                    </button>
                    <button className="profilo-btn-annulla" onClick={() => setStatoElimina('idle')}>
                      Annulla
                    </button>
                  </div>
                </div>
              )}
              {statoElimina === 'loading' && (
                <button className="profilo-btn-danger" disabled>Eliminazione…</button>
              )}
            </div>
          </div>

          {errore && <p className="profilo-errore" role="alert">{errore}</p>}
        </section>
      </div>
    </div>
  )
}
