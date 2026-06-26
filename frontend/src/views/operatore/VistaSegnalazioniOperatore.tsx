import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getSegnalazioni,
  getDettaglioSegnalazione,
  aggiornaStatoSegnalazione,
  risolviSegnalazione,
  type Segnalazione,
} from '../../services/SegnalazioneService'
import './VistaSegnalazioniOperatore.css'

const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
  risolta: 'Risolta',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'badge-aperta',
  in_carico: 'badge-in-carico',
  risolta: 'badge-risolta',
}

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

// [IF-OP.08] Gestisce Segnalazione
export default function VistaSegnalazioniOperatore() {
  const navigate = useNavigate()

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

  const risolviSegnalazioneLocale = async () => {
    if (!selezionata) return
    setAzioneInCorso(true)
    try {
      const res = await risolviSegnalazione(selezionata.id)
      setSelezionata(res.data)
      setSegnalazioni(prev =>
        prev.map(s => s.id === res.data.id ? res.data : s)
      )
      setMessaggio('Segnalazione segnata come risolta.')
      setTimeout(() => setMessaggio(''), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Segnalazione non trovata.')
      } else if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore('La segnalazione deve essere prima presa in carico.')
      } else {
        setErrore('Errore durante l\'operazione.')
      }
    } finally {
      setAzioneInCorso(false)
    }
  }

  return (
    <div className="vista-segn-op-wrap">
      <button type="button" className="btn-back-segn-op" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="segn-op-titolo">Segnalazioni</h1>

      {messaggio && <div className="segn-op-messaggio">{messaggio}</div>}
      {errore && <p className="segn-op-errore">{errore}</p>}

      <div className="segn-op-layout">
        {/* Lista */}
        <div className="segn-op-lista">
          {caricamento ? (
            <p className="segn-op-vuoto">Caricamento...</p>
          ) : segnalazioni.length === 0 ? (
            <p className="segn-op-vuoto">Nessuna segnalazione ricevuta.</p>
          ) : (
            segnalazioni.map(s => (
              <div
                key={s.id}
                className={`segn-op-card${selezionata?.id === s.id ? ' segn-op-card--attiva' : ''}`}
                onClick={() => selezionaSegnalazione(s.id)}
              >
                <div className="segn-op-card-header">
                  <span className="segn-op-tipologia">{s.tipologia}</span>
                  <span className={`segn-badge ${STATO_CLASS[s.stato] ?? ''}`}>
                    {STATO_LABEL[s.stato] ?? s.stato}
                  </span>
                </div>
                {s.nome_utente && (
                  <span className="segn-op-utente">👤 {s.nome_utente}</span>
                )}
                <p className="segn-op-descrizione-anteprima">
                  {s.descrizione.length > 80 ? s.descrizione.slice(0, 80) + '…' : s.descrizione}
                </p>
                <span className="segn-op-data">{formatData(s.created_at)}</span>
              </div>
            ))
          )}
        </div>

        {/* Dettaglio */}
        {selezionata && (
          <div className="segn-op-dettaglio">
            <h2 className="segn-op-det-titolo">Dettaglio</h2>
            {selezionata.nome_utente && (
              <div className="segn-op-det-row">
                <span className="segn-op-det-label">Utente</span>
                <span>{selezionata.nome_utente}</span>
              </div>
            )}
            <div className="segn-op-det-row">
              <span className="segn-op-det-label">Tipologia</span>
              <span>{selezionata.tipologia}</span>
            </div>
            <div className="segn-op-det-row">
              <span className="segn-op-det-label">Stato</span>
              <span className={`segn-badge ${STATO_CLASS[selezionata.stato] ?? ''}`}>
                {STATO_LABEL[selezionata.stato] ?? selezionata.stato}
              </span>
            </div>
            <div className="segn-op-det-row">
              <span className="segn-op-det-label">Data</span>
              <span>{formatData(selezionata.created_at)}</span>
            </div>
            <div className="segn-op-det-descrizione">
              <span className="segn-op-det-label">Descrizione</span>
              <p>{selezionata.descrizione}</p>
            </div>
            {selezionata.stato === 'aperta' && (
              <button
                type="button"
                className="btn-segn-op-primario"
                onClick={prendiInCarico}
                disabled={azioneInCorso}
              >
                {azioneInCorso ? 'Aggiornamento...' : 'PRENDI IN CARICO'}
              </button>
            )}
            {selezionata.stato === 'in_carico' && (
              <button
                type="button"
                className="btn-segn-op-primario"
                onClick={risolviSegnalazioneLocale}
                disabled={azioneInCorso}
              >
                {azioneInCorso ? 'Aggiornamento...' : 'SEGNA COME RISOLTA'}
              </button>
            )}
            {selezionata.stato === 'risolta' && (
              <p className="segn-op-in-carico-msg">✅ Segnalazione risolta</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
