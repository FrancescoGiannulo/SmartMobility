import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/ApiService'
import { logout, utenteCorrente, modificaDatiAccount } from '../../services/AuthService'
import './VistaProfiloUtente.css'

export default function VistaProfiloUtente() {
  const navigate = useNavigate()
  const utente = utenteCorrente()
  const [statoExport, setStatoExport] = useState<'idle' | 'loading' | 'done' | 'error'>('idle')
  const [statoElimina, setStatoElimina] = useState<'idle' | 'confirm' | 'loading' | 'error'>('idle')
  const [errore, setErrore] = useState('')

  // Modifica dati account
  const [modificaAttiva, setModificaAttiva] = useState(false)
  const [nome, setNome] = useState(utente?.profilo.nome ?? '')
  const [cognome, setCognome] = useState(utente?.profilo.cognome ?? '')
  const [statoModifica, setStatoModifica] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [erroreModifica, setErroreModifica] = useState('')

  const handleModifica = async () => {
    if (!nome.trim() || !cognome.trim()) {
      setErroreModifica('Nome e cognome sono obbligatori.')
      return
    }
    setStatoModifica('loading')
    setErroreModifica('')
    try {
      await modificaDatiAccount({ nome: nome.trim(), cognome: cognome.trim() })
      setStatoModifica('success')
      setModificaAttiva(false)
      setTimeout(() => setStatoModifica('idle'), 2000)
    } catch {
      setStatoModifica('error')
      setErroreModifica('Impossibile aggiornare i dati. Riprova.')
    }
  }

  const handleAnnullaModifica = () => {
    setNome(utente?.profilo.nome ?? '')
    setCognome(utente?.profilo.cognome ?? '')
    setModificaAttiva(false)
    setErroreModifica('')
    setStatoModifica('idle')
  }

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

  const profiloAggiornato = utenteCorrente()

  return (
    <div className="profilo-container">
      <div className="profilo-card">
        <button className="profilo-back" onClick={() => navigate(-1)} aria-label="Torna indietro">
          ← Indietro
        </button>

        <h1 className="profilo-titolo">Il mio profilo</h1>

        {/* Avatar */}
        {profiloAggiornato && (
          <div className="profilo-avatar-sezione">
            <div className="profilo-avatar-grande">
              {(profiloAggiornato.profilo.nome?.[0] ?? '?').toUpperCase()}
            </div>
          </div>
        )}

        {/* Dati account */}
        {profiloAggiornato && (
          <div className="profilo-info">
            {modificaAttiva ? (
              <>
                <div className="profilo-campo">
                  <label className="profilo-label" htmlFor="profilo-nome">Nome</label>
                  <input
                    id="profilo-nome"
                    className="profilo-input"
                    type="text"
                    value={nome}
                    onChange={e => setNome(e.target.value)}
                    disabled={statoModifica === 'loading'}
                  />
                </div>
                <div className="profilo-campo">
                  <label className="profilo-label" htmlFor="profilo-cognome">Cognome</label>
                  <input
                    id="profilo-cognome"
                    className="profilo-input"
                    type="text"
                    value={cognome}
                    onChange={e => setCognome(e.target.value)}
                    disabled={statoModifica === 'loading'}
                  />
                </div>
                {erroreModifica && <p className="profilo-errore" role="alert">{erroreModifica}</p>}
                <div className="profilo-modifica-azioni">
                  <button
                    className="profilo-btn-salva"
                    onClick={handleModifica}
                    disabled={statoModifica === 'loading'}
                  >
                    {statoModifica === 'loading' ? 'Salvataggio...' : 'Salva'}
                  </button>
                  <button
                    className="profilo-btn-annulla"
                    onClick={handleAnnullaModifica}
                    disabled={statoModifica === 'loading'}
                  >
                    Annulla
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="profilo-info-row">
                  <span className="profilo-label">Nome</span>
                  <span className="profilo-valore">{profiloAggiornato.profilo.nome} {profiloAggiornato.profilo.cognome}</span>
                </div>
                <div className="profilo-info-row">
                  <span className="profilo-label">Email</span>
                  <span className="profilo-valore">{profiloAggiornato.profilo.email}</span>
                </div>
                <div className="profilo-info-row">
                  <span className="profilo-label">Ruolo</span>
                  <span className="profilo-badge">{profiloAggiornato.ruolo}</span>
                </div>
                {statoModifica === 'success' && (
                  <p className="profilo-successo" role="status">Dati aggiornati con successo.</p>
                )}
                <button
                  className="profilo-btn-modifica"
                  onClick={() => {
                    setNome(profiloAggiornato.profilo.nome)
                    setCognome(profiloAggiornato.profilo.cognome ?? '')
                    setModificaAttiva(true)
                  }}
                >
                  Modifica dati
                </button>
              </>
            )}
          </div>
        )}

        {/* GDPR */}
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
                {statoExport === 'loading' ? 'Scaricamento...' :
                 statoExport === 'done' ? 'Scaricato' : 'Scarica'}
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
                <button className="profilo-btn-danger" disabled>Eliminazione...</button>
              )}
            </div>
          </div>

          {errore && <p className="profilo-errore" role="alert">{errore}</p>}
        </section>
      </div>
    </div>
  )
}
