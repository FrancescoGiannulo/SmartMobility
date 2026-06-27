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

function tempoResiduo(fine: string): string {
  const ms = new Date(fine).getTime() - Date.now()
  if (ms <= 0) return 'meno di un minuto'
  const minutiTot = Math.floor(ms / 60000)
  const giorni = Math.floor(minutiTot / 1440)
  const ore = Math.floor((minutiTot % 1440) / 60)
  const minuti = minutiTot % 60
  const parti: string[] = []
  if (giorni) parti.push(giorni === 1 ? '1 giorno' : `${giorni} giorni`)
  if (ore) parti.push(ore === 1 ? '1 ora' : `${ore} ore`)
  if (minuti && !giorni) parti.push(minuti === 1 ? '1 minuto' : `${minuti} minuti`)
  return parti.length ? parti.join(' e ') : 'meno di un minuto'
}

// [IF-OP.09] Sospende Account Utente
export default function VistaGestioneUtentiOperatore() {
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
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vgest__body">
          <h1 className="vgest__titolo">Gestione Utenti</h1>

          {messaggio && <div className="vgest__messaggio">{messaggio}</div>}
          {errore && <p className="vgest__errore">{errore}</p>}

          <div className="vgest__lista">
            {caricamento ? (
              <p className="vgest__vuoto">Caricamento...</p>
            ) : utenti.length === 0 ? (
              <p className="vgest__vuoto">Nessun utente registrato.</p>
            ) : (
              utenti.map(u => (
                <div
                  key={u.id}
                  className="vgest__card"
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
        </div>

        {/* Popup 1 — dettaglio utente */}
        {dialogoAperto && selezionato && (
          <div className="vgest__overlay" onClick={chiudiDialogo}>
            <div className="vgest__modale" onClick={e => e.stopPropagation()}>
              <div className="vgest__modale-header">
                <h2 className="vgest__det-titolo">{selezionato.nome} {selezionato.cognome}</h2>
                <button type="button" className="vgest__modale-chiudi" onClick={chiudiDialogo}>✕</button>
              </div>
              <div className="vgest__modale-body">
                <div className="vgest__det-row">
                  <span className="vgest__det-label">Email</span>
                  <span>{selezionato.email}</span>
                </div>
                <div className="vgest__det-row">
                  <span className="vgest__det-label">Stato</span>
                  <span>{selezionato.sospeso ? '🔴 Sospeso' : 'Attivo'}</span>
                </div>

                <div className="vgest__modale-divider" />

                {selezionato.sospeso ? (
                  <div className="vgest__sospeso-info">
                    <p className="vgest__sospeso-msg">⚠️ Account sospeso</p>
                    {(selezionato as UtenteListItem & { sospensione_fine?: string }).sospensione_fine ? (
                      <>
                        <p className="vgest__scadenza">
                          Tempo rimanente: <strong>{tempoResiduo((selezionato as UtenteListItem & { sospensione_fine?: string }).sospensione_fine!)}</strong>
                        </p>
                        <p className="vgest__scadenza">
                          Riattivazione: {new Date((selezionato as UtenteListItem & { sospensione_fine?: string }).sospensione_fine!).toLocaleDateString('it-IT', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </>
                    ) : (
                      <p className="vgest__scadenza">Durata: indeterminata</p>
                    )}
                  </div>
                ) : (
                  <button
                    type="button"
                    className="sm-btn vgest__btn-danger"
                    onClick={apriSospensione}
                  >
                    Sospendi account
                  </button>
                )}
                <button
                  type="button"
                  className="sm-btn sm-btn--ghost vgest__btn-secondario"
                  onClick={chiudiDialogo}
                >
                  Chiudi
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Popup 2 — form sospensione */}
        {sospensioneAperta && selezionato && (
          <div className="vgest__overlay" onClick={chiudiSospensione}>
            <div className="vgest__modale" onClick={e => e.stopPropagation()}>
              <div className="vgest__modale-header">
                <h2 className="vgest__det-titolo">Sospendi account</h2>
                <button type="button" className="vgest__modale-chiudi" onClick={chiudiSospensione}>✕</button>
              </div>
              <div className="vgest__modale-body">
                <p className="vgest__modal-sub">{selezionato.nome} {selezionato.cognome}</p>
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
                  <label className="vgest__det-label" htmlFor="durata-sospensione">
                    Durata (giorni)
                  </label>
                  <select
                    id="durata-sospensione"
                    className="vgest__select"
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
                    className="sm-btn vgest__btn-danger"
                    onClick={confermaSospensione}
                    disabled={azioneInCorso || !motivazione.trim()}
                  >
                    {azioneInCorso ? 'Sospensione...' : 'Conferma sospensione'}
                  </button>
                  <button
                    type="button"
                    className="sm-btn sm-btn--ghost vgest__btn-secondario"
                    onClick={chiudiSospensione}
                    disabled={azioneInCorso}
                  >
                    Annulla
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
