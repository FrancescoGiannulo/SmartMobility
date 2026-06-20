import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { salvaSegnalazione, getMieSegnalazioni, TIPOLOGIE, type Segnalazione } from '../../services/SegnalazioneService'
import './VistaSegnalazione.css'

const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'segn-badge--aperta',
  in_carico: 'segn-badge--in-carico',
}

function formatData(iso: string) {
  return new Date(iso).toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

// [IF-UT.12] Invia Segnalazione
export default function VistaSegnalazione() {
  const navigate = useNavigate()

  const [tipologia, setTipologia] = useState<string>(TIPOLOGIE[0])
  const [descrizione, setDescrizione] = useState('')
  const [invioInCorso, setInvioInCorso] = useState(false)
  const [confermato, setConfermato] = useState(false)
  const [errore, setErrore] = useState('')

  const [storico, setStorico] = useState<Segnalazione[]>([])

  const caricaStorico = useCallback(async () => {
    try {
      const res = await getMieSegnalazioni()
      setStorico(res.data)
    } catch {
      // storico non bloccante
    }
  }, [])

  useEffect(() => { caricaStorico() }, [caricaStorico])

  const inviaForm = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!descrizione.trim()) {
      setErrore('Inserisci una descrizione.')
      return
    }
    setInvioInCorso(true)
    setErrore('')
    try {
      await salvaSegnalazione(tipologia, descrizione.trim())
      setConfermato(true)
      await caricaStorico()
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore('Dati non validi. Controlla i campi e riprova.')
      } else {
        setErrore("Errore durante l'invio. Riprova.")
      }
    } finally {
      setInvioInCorso(false)
    }
  }

  return (
    <div className="vista-segn-wrap">
      <button type="button" className="btn-back-segn" onClick={() => navigate(-1)}>
        ← Torna indietro
      </button>

      {confermato ? (
        <div className="segn-conferma">
          <span className="segn-conferma-icona">✅</span>
          <h2 className="segn-conferma-titolo">Segnalazione inviata</h2>
          <p className="segn-conferma-testo">
            La tua segnalazione è stata registrata e sarà presa in carico dall'operatore.
          </p>
          <button
            type="button"
            className="btn-segn-primario"
            onClick={() => { setConfermato(false); setDescrizione(''); setTipologia(TIPOLOGIE[0]) }}
          >
            Invia un'altra
          </button>
          <button type="button" className="btn-segn-secondario" onClick={() => navigate('/utente/home')}>
            Torna alla mappa
          </button>
        </div>
      ) : (
        <>
          <h1 className="segn-titolo">Invia segnalazione</h1>
          <p className="segn-sottotitolo">Segnala un problema relativo a un mezzo o al servizio.</p>

          <form className="segn-form" onSubmit={inviaForm}>
            <label className="segn-label" htmlFor="tipologia">Tipologia</label>
            <select
              id="tipologia"
              className="segn-select"
              value={tipologia}
              onChange={e => setTipologia(e.target.value)}
            >
              {TIPOLOGIE.map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>

            <label className="segn-label" htmlFor="descrizione">Descrizione</label>
            <textarea
              id="descrizione"
              className="segn-textarea"
              placeholder="Descrivi il problema in dettaglio..."
              rows={5}
              maxLength={500}
              value={descrizione}
              onChange={e => setDescrizione(e.target.value)}
              required
            />
            <span className="segn-contatore">{descrizione.length}/500</span>

            {errore && <p className="segn-errore">{errore}</p>}

            <button type="submit" className="btn-segn-primario" disabled={invioInCorso}>
              {invioInCorso ? 'Invio in corso...' : 'INVIA SEGNALAZIONE'}
            </button>
          </form>
        </>
      )}

      {storico.length > 0 && (
        <div className="segn-storico">
          <h2 className="segn-storico-titolo">Le mie segnalazioni</h2>
          <div className="segn-storico-lista">
            {storico.map(s => (
              <div key={s.id} className="segn-storico-card">
                <div className="segn-storico-header">
                  <span className="segn-storico-tipologia">{s.tipologia}</span>
                  <span className={`segn-badge ${STATO_CLASS[s.stato] ?? ''}`}>
                    {STATO_LABEL[s.stato] ?? s.stato}
                  </span>
                </div>
                <p className="segn-storico-desc">
                  {s.descrizione.length > 100 ? s.descrizione.slice(0, 100) + '…' : s.descrizione}
                </p>
                <span className="segn-storico-data">{formatData(s.created_at)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
