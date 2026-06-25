import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import {
  getSegnalazioni,
  getDettaglioSegnalazione,
  aggiornaStatoSegnalazione,
  type Segnalazione,
} from '../../services/SegnalazioneService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import './VistaSegnalazioniOperatore.css'

const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'vsegn__badge--aperta',
  in_carico: 'vsegn__badge--in-carico',
}

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

// [IF-OP.08] Gestisce Segnalazione
export default function VistaSegnalazioniOperatore() {
  const [segnalazioni, setSegnalazioni] = useState<Segnalazione[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [selezionata, setSelezionata] = useState<Segnalazione | null>(null)
  const [azioneInCorso, setAzioneInCorso] = useState(false)
  const [messaggio, setMessaggio] = useState('')

  const getSegnalazioniLocale = useCallback(async () => {
    try {
      const res = await getSegnalazioni()
      setSegnalazioni(res.data)
    } catch {
      setErrore('Impossibile caricare le segnalazioni.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { getSegnalazioniLocale() }, [getSegnalazioniLocale])

  const selezionaSegnalazione = async (id: string) => {
    try {
      const res = await getDettaglioSegnalazione(id)
      setSelezionata(res.data)
    } catch {
      setErrore('Errore nel caricamento del dettaglio.')
    }
  }

  const prendiInCarico = async () => {
    if (!selezionata) return
    setAzioneInCorso(true)
    try {
      const res = await aggiornaStatoSegnalazione(selezionata.id)
      setSelezionata(res.data)
      setSegnalazioni(prev =>
        prev.map(s => s.id === res.data.id ? res.data : s)
      )
      setMessaggio('Segnalazione presa in carico.')
      setTimeout(() => setMessaggio(''), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Segnalazione non trovata.')
      } else {
        setErrore('Errore durante l\'operazione.')
      }
    } finally {
      setAzioneInCorso(false)
    }
  }

  return (
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vsegn__body">
          <h1 className="vsegn__titolo">Segnalazioni</h1>

          {messaggio && <div className="vsegn__messaggio">{messaggio}</div>}
          {errore && <p className="vsegn__errore">{errore}</p>}

          <div className="vsegn__layout">
            {/* Lista */}
            <div className="vsegn__lista">
              {caricamento ? (
                <p className="vsegn__vuoto">Caricamento...</p>
              ) : segnalazioni.length === 0 ? (
                <p className="vsegn__vuoto">Nessuna segnalazione ricevuta.</p>
              ) : (
                segnalazioni.map(s => (
                  <div
                    key={s.id}
                    className={`vsegn__card${selezionata?.id === s.id ? ' vsegn__card--attiva' : ''}`}
                    onClick={() => selezionaSegnalazione(s.id)}
                  >
                    <div className="vsegn__card-header">
                      <span className="vsegn__tipologia">{s.tipologia}</span>
                      <span className={`vsegn__badge ${STATO_CLASS[s.stato] ?? ''}`}>
                        {STATO_LABEL[s.stato] ?? s.stato}
                      </span>
                    </div>
                    {s.nome_utente && (
                      <span className="vsegn__utente">👤 {s.nome_utente}</span>
                    )}
                    <p className="vsegn__descrizione-anteprima">
                      {s.descrizione.length > 80 ? s.descrizione.slice(0, 80) + '…' : s.descrizione}
                    </p>
                    <span className="vsegn__data">{formatData(s.created_at)}</span>
                  </div>
                ))
              )}
            </div>

            {/* Dettaglio */}
            {selezionata && (
              <div className="vsegn__dettaglio">
                <h2 className="vsegn__det-titolo">Dettaglio</h2>
                {selezionata.nome_utente && (
                  <div className="vsegn__det-row">
                    <span className="vsegn__det-label">Utente</span>
                    <span>{selezionata.nome_utente}</span>
                  </div>
                )}
                <div className="vsegn__det-row">
                  <span className="vsegn__det-label">Tipologia</span>
                  <span>{selezionata.tipologia}</span>
                </div>
                <div className="vsegn__det-row">
                  <span className="vsegn__det-label">Stato</span>
                  <span className={`vsegn__badge ${STATO_CLASS[selezionata.stato] ?? ''}`}>
                    {STATO_LABEL[selezionata.stato] ?? selezionata.stato}
                  </span>
                </div>
                <div className="vsegn__det-row">
                  <span className="vsegn__det-label">Data</span>
                  <span>{formatData(selezionata.created_at)}</span>
                </div>
                <div className="vsegn__det-descrizione">
                  <span className="vsegn__det-label">Descrizione</span>
                  <p>{selezionata.descrizione}</p>
                </div>
                {selezionata.stato === 'aperta' && (
                  <button
                    type="button"
                    className="sm-btn sm-btn--primary vsegn__btn-primario"
                    onClick={prendiInCarico}
                    disabled={azioneInCorso}
                  >
                    {azioneInCorso ? 'Aggiornamento...' : 'PRENDI IN CARICO'}
                  </button>
                )}
                {selezionata.stato === 'in_carico' && (
                  <p className="vsegn__in-carico-msg">✅ Già presa in carico</p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
