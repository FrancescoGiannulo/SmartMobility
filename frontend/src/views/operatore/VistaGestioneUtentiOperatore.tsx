import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getUtenti,
  getDettaglioUtente,
  sospendiAccount,
  type UtenteListItem,
} from '../../services/GestioneUtentiService'
import './VistaGestioneUtentiOperatore.css'

// [IF-OP.09] Sospende Account Utente
export default function VistaGestioneUtentiOperatore() {
  const navigate = useNavigate()

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
    <div className="vista-gest-ut-wrap">
      <button type="button" className="btn-back-gest-ut" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="gest-ut-titolo">Gestione Utenti</h1>

      {messaggio && <div className="gest-ut-messaggio">{messaggio}</div>}
      {errore && <p className="gest-ut-errore">{errore}</p>}

      <div className="gest-ut-layout">
        <div className="gest-ut-lista">
          {caricamento ? (
            <p className="gest-ut-vuoto">Caricamento...</p>
          ) : utenti.length === 0 ? (
            <p className="gest-ut-vuoto">Nessun utente registrato.</p>
          ) : (
            utenti.map(u => (
              <div
                key={u.id}
                className={`gest-ut-card${selezionato?.id === u.id ? ' gest-ut-card--attiva' : ''}`}
                onClick={() => selezionaUtente(u.id)}
              >
                <div className="gest-ut-card-header">
                  <span className="gest-ut-nome">{u.nome} {u.cognome}</span>
                  {u.sospeso && <span className="gest-ut-badge">Sospeso</span>}
                </div>
                <span className="gest-ut-email">{u.email}</span>
              </div>
            ))
          )}
        </div>

        {selezionato && (
          <div className="gest-ut-dettaglio">
            <h2 className="gest-ut-det-titolo">Dettaglio</h2>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Nome</span>
              <span>{selezionato.nome} {selezionato.cognome}</span>
            </div>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Email</span>
              <span>{selezionato.email}</span>
            </div>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Stato</span>
              <span>{selezionato.sospeso ? 'Sospeso' : 'Attivo'}</span>
            </div>

            {selezionato.sospeso ? (
              <p className="gest-ut-sospeso-msg">⚠️ Account già sospeso</p>
            ) : !dialogoAperto ? (
              <button
                type="button"
                className="btn-gest-ut-danger"
                onClick={() => setDialogoAperto(true)}
              >
                Sospendi account
              </button>
            ) : (
              <div className="gest-ut-conferma">
                <label className="gest-ut-det-label" htmlFor="motivazione-sospensione">
                  Motivazione della sospensione
                </label>
                <textarea
                  id="motivazione-sospensione"
                  className="gest-ut-textarea"
                  value={motivazione}
                  onChange={e => setMotivazione(e.target.value)}
                  placeholder="Descrivi il motivo della sospensione"
                  rows={4}
                />
                <button
                  type="button"
                  className="btn-gest-ut-danger"
                  onClick={confermaSospensione}
                  disabled={azioneInCorso || !motivazione.trim()}
                >
                  {azioneInCorso ? 'Sospensione...' : 'Conferma sospensione'}
                </button>
                <button
                  type="button"
                  className="btn-gest-ut-secondario"
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
  )
}
