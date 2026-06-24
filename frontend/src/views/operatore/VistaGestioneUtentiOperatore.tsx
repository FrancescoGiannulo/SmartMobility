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
  const [durataGiorni, setDurataGiorni] = useState(7)
  const [dialogoAperto, setDialogoAperto] = useState(false)
  const [sospensioneAperta, setSospensioneAperta] = useState(false)
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
    setMotivazione('')
    setDurataGiorni(7)
    try {
      const res = await getDettaglioUtente(id)
      setSelezionato(res.data)
      setDialogoAperto(true)
    } catch {
      setErrore('Errore nel caricamento del dettaglio.')
    }
  }

  const chiudiDialogo = () => {
    if (azioneInCorso) return
    setDialogoAperto(false)
    setSospensioneAperta(false)
    setSelezionato(null)
    setMotivazione('')
    setDurataGiorni(7)
  }

  const apriSospensione = () => {
    setMotivazione('')
    setDurataGiorni(7)
    setSospensioneAperta(true)
  }

  const chiudiSospensione = () => {
    if (azioneInCorso) return
    setSospensioneAperta(false)
    setMotivazione('')
    setDurataGiorni(7)
  }

  const confermaSospensione = async () => {
    if (!selezionato || !motivazione.trim()) return
    setErrore('')
    setAzioneInCorso(true)
    try {
      const res = await sospendiAccount(selezionato.id, motivazione.trim(), durataGiorni)
      setSelezionato(res.data)
      setUtenti(prev => prev.map(u => (u.id === res.data.id ? res.data : u)))
      setSospensioneAperta(false)
      setDialogoAperto(false)
      setSelezionato(null)
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

      </div>

      {/* Popup 1 — dettaglio utente (come Riepilogo Corsa) */}
      {dialogoAperto && selezionato && (
        <div className="gest-ut-overlay" onClick={chiudiDialogo}>
          <div className="gest-ut-modal" onClick={e => e.stopPropagation()}>
            <h2 className="gest-ut-modal-titolo">{selezionato.nome} {selezionato.cognome}</h2>
            <p className="gest-ut-modal-sub">{selezionato.email}</p>

            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Stato</span>
              <span>{selezionato.sospeso ? 'Sospeso' : 'Attivo'}</span>
            </div>

            {selezionato.sospeso ? (
              <div className="gest-ut-sospeso-info">
                <p className="gest-ut-sospeso-msg">⚠️ Account sospeso</p>
                {selezionato.sospensione_fine && (
                  <p className="gest-ut-scadenza">
                    Riattivazione: {new Date(selezionato.sospensione_fine).toLocaleDateString('it-IT', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                )}
              </div>
            ) : (
              <button
                type="button"
                className="btn-gest-ut-danger"
                onClick={apriSospensione}
              >
                Sospendi account
              </button>
            )}
            <button
              type="button"
              className="btn-gest-ut-secondario"
              onClick={chiudiDialogo}
            >
              Chiudi
            </button>
          </div>
        </div>
      )}

      {/* Popup 2 — form di sospensione, sopra il dettaglio */}
      {sospensioneAperta && selezionato && (
        <div className="gest-ut-overlay" onClick={chiudiSospensione}>
          <div className="gest-ut-modal" onClick={e => e.stopPropagation()}>
            <h2 className="gest-ut-modal-titolo">Sospendi account</h2>
            <p className="gest-ut-modal-sub">{selezionato.nome} {selezionato.cognome}</p>

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
            <label className="gest-ut-det-label" htmlFor="durata-sospensione">
              Durata (giorni)
            </label>
            <select
              id="durata-sospensione"
              className="gest-ut-select"
              value={durataGiorni}
              onChange={e => setDurataGiorni(Number(e.target.value))}
            >
              <option value={1}>1 giorno</option>
              <option value={3}>3 giorni</option>
              <option value={7}>7 giorni</option>
              <option value={14}>14 giorni</option>
              <option value={30}>30 giorni</option>
              <option value={90}>90 giorni</option>
            </select>
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
              onClick={chiudiSospensione}
              disabled={azioneInCorso}
            >
              Annulla
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
