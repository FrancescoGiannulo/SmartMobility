import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { inviaSegnalazione, TIPOLOGIE } from '../../services/SegnalazioneService'
import './VistaSegnalazione.css'

// [IF-UT.15] Invia Segnalazione
export default function VistaSegnalazione() {
  const navigate = useNavigate()

  const [tipologia, setTipologia] = useState<string>(TIPOLOGIE[0])
  const [descrizione, setDescrizione] = useState('')
  const [invioInCorso, setInvioInCorso] = useState(false)
  const [confermato, setConfermato] = useState(false)
  const [errore, setErrore] = useState('')

  const handleInvia = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!descrizione.trim()) {
      setErrore('Inserisci una descrizione.')
      return
    }
    setInvioInCorso(true)
    setErrore('')
    try {
      await inviaSegnalazione(tipologia, descrizione.trim())
      setConfermato(true)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore('Dati non validi. Controlla i campi e riprova.')
      } else {
        setErrore('Errore durante l\'invio. Riprova.')
      }
    } finally {
      setInvioInCorso(false)
    }
  }

  if (confermato) {
    return (
      <div className="vista-segn-wrap">
        <div className="segn-conferma">
          <span className="segn-conferma-icona">✅</span>
          <h2 className="segn-conferma-titolo">Segnalazione inviata</h2>
          <p className="segn-conferma-testo">
            La tua segnalazione è stata registrata e sarà presa in carico dall'operatore.
          </p>
          <button
            type="button"
            className="btn-segn-primario"
            onClick={() => navigate('/utente/home')}
          >
            Torna alla mappa
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="vista-segn-wrap">
      <button type="button" className="btn-back-segn" onClick={() => navigate(-1)}>
        ← Torna indietro
      </button>

      <h1 className="segn-titolo">Invia segnalazione</h1>
      <p className="segn-sottotitolo">
        Segnala un problema relativo a un mezzo o al servizio.
      </p>

      <form className="segn-form" onSubmit={handleInvia}>
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
    </div>
  )
}
