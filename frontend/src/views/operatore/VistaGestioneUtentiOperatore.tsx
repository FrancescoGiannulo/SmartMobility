import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import {
  getUtenti,
  getDettaglioUtente,
  sospendiAccount,
  type UtenteListItem,
} from '../../services/GestioneUtentiService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import './VistaGestioneUtentiOperatore.css'

// [IF-OP.09] Sospende Account Utente
export default function VistaGestioneUtentiOperatore() {
  const [utenti, setUtenti] = useState<UtenteListItem[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [selezionato, setSelezionato] = useState<UtenteListItem | null>(null)
  const [motivazione, setMotivazione] = useState('')
  const [dialogoAperto, setDialogoAperto] = useState(false)
  const [azioneInCorso, setAzioneInCorso] = useState(false)
  const [messaggio, setMessaggio] = useState('')

  const caricaUtenti = useCallback(async () => {
    setErrore('')
    try {
      const res = await getUtenti()
      setUtenti(res.data)
    } catch {
      setErrore('Impossibile caricare gli utenti.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaUtenti() }, [caricaUtenti])

  const selezionaUtente = async (id: string) => {
    setErrore('')
    setDialogoAperto(false)
    setMotivazione('')
    try {
      const res = await getDettaglioUtente(id)
      setSelezionato(res.data)
    } catch {
      setErrore('Errore nel caricamento del dettaglio.')
    }
  }

  const confermaSospensione = async () => {
    if (!selezionato || !motivazione.trim()) return
    setErrore('')
    setAzioneInCorso(true)
    try {
      const res = await sospendiAccount(selezionato.id, motivazione.trim())
      setSelezionato(res.data)
      setUtenti(prev => prev.map(u => (u.id === res.data.id ? res.data : u)))
      setDialogoAperto(false)
      setMessaggio('Account sospeso con successo.')
      setTimeout(() => setMessaggio(''), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErrore('L\'account è già sospeso.')
      } else if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Utente non trovato.')
      } else {
        setErrore('Errore durante la sospensione dell\'account.')
      }
    } finally {
      setAzioneInCorso(false)
    }
  }

  return (
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vgest__body">
          <h1 className="vgest__titolo">Gestione Utenti</h1>

          {messaggio && <div className="vgest__messaggio">{messaggio}</div>}
          {errore && <p className="vgest__errore">{errore}</p>}

          <div className="vgest__layout">
            <div className="vgest__lista">
              {caricamento ? (
                <p className="vgest__vuoto">Caricamento...</p>
              ) : utenti.length === 0 ? (
                <p className="vgest__vuoto">Nessun utente registrato.</p>
              ) : (
                utenti.map(u => (
                  <div
                    key={u.id}
                    className={`vgest__card${selezionato?.id === u.id ? ' vgest__card--attiva' : ''}`}
                    onClick={() => selezionaUtente(u.id)}
                  >
                    <div className="vgest__card-header">
                      <span className="vgest__nome">{u.nome} {u.cognome}</span>
                      {u.sospeso && <span className="vgest__badge">Sospeso</span>}
                    </div>
                    <span className="vgest__email">{u.email}</span>
                  </div>
                ))
              )}
            </div>

            {selezionato && (
              <div className="vgest__dettaglio">
                <h2 className="vgest__det-titolo">Dettaglio</h2>
                <div className="vgest__det-row">
                  <span className="vgest__det-label">Nome</span>
                  <span>{selezionato.nome} {selezionato.cognome}</span>
                </div>
                <div className="vgest__det-row">
                  <span className="vgest__det-label">Email</span>
                  <span>{selezionato.email}</span>
                </div>
                <div className="vgest__det-row">
                  <span className="vgest__det-label">Stato</span>
                  <span>{selezionato.sospeso ? 'Sospeso' : 'Attivo'}</span>
                </div>

                {selezionato.sospeso ? (
                  <p className="vgest__sospeso-msg">⚠️ Account già sospeso</p>
                ) : !dialogoAperto ? (
                  <button
                    type="button"
                    className="sm-btn vgest__btn-danger"
                    onClick={() => setDialogoAperto(true)}
                  >
                    Sospendi account
                  </button>
                ) : (
                  <div className="vgest__conferma">
                    <label className="vgest__det-label" htmlFor="motivazione-sospensione">
                      Motivazione della sospensione
                    </label>
                    <textarea
                      id="motivazione-sospensione"
                      className="vgest__textarea"
                      value={motivazione}
                      onChange={e => setMotivazione(e.target.value)}
                      placeholder="Descrivi il motivo della sospensione"
                      rows={4}
                    />
                    <button
                      type="button"
                      className="sm-btn vgest__btn-danger"
                      onClick={confermaSospensione}
                      disabled={azioneInCorso || !motivazione.trim()}
                    >
                      {azioneInCorso ? 'Sospensione...' : 'Conferma sospensione'}
                    </button>
                    <button
                      type="button"
                      className="sm-btn sm-btn--ghost vgest__btn-secondario"
                      onClick={() => { setDialogoAperto(false); setMotivazione('') }}
                      disabled={azioneInCorso}
                    >
                      Annulla
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
