import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getParametriSistema,
  aggiornaParametriSistema,
} from '../../services/ConfigurazioneService'
import './VistaParametriSistema.css'

export default function VistaParametriSistema() {
  const navigate = useNavigate()

  const [durataPrenotazione, setDurataPrenotazione] = useState('')
  const [durataGrazia, setDurataGrazia] = useState('')
  const [maxMezzi, setMaxMezzi] = useState('')
  const [addebitoPausa, setAddebitoPausa] = useState('')
  const [errore, setErrore] = useState('')
  const [conferma, setConferma] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  useEffect(() => {
    getParametriSistema()
      .then(p => {
        setDurataPrenotazione(String(p.durata_max_prenotazione_min))
        setDurataGrazia(String(p.durata_periodo_grazia_min))
        setMaxMezzi(String(p.max_mezzi_per_utente))
        setAddebitoPausa(String(p.addebito_pausa_min))
      })
      .catch(() => {})
  }, [])

  const handleSalva = async () => {
    setErrore('')
    setConferma('')
    setCaricamento(true)
    try {
      await aggiornaParametriSistema({
        durata_max_prenotazione_min: parseInt(durataPrenotazione),
        durata_periodo_grazia_min: parseInt(durataGrazia),
        max_mezzi_per_utente: parseInt(maxMezzi),
        addebito_pausa_min: parseFloat(addebitoPausa),
      })
      setConferma('Parametri di sistema salvati correttamente.')
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail
        setErrore(typeof detail === 'string' ? detail : 'Dati non validi. Controlla i campi.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  return (
    <div className="vista-params">
      <div className="params-topbar">
        <h2>Parametri Numerici di Sistema</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="params-body">
        <div className="params-card">
          <h3>Prenotazione</h3>
          <div className="params-campo">
            <label>Durata massima prenotazione (minuti)</label>
            <input
              type="number"
              min="0"
              value={durataPrenotazione}
              onChange={e => setDurataPrenotazione(e.target.value)}
              placeholder="es. 15"
            />
          </div>
          <div className="params-campo">
            <label>Numero massimo mezzi per utente</label>
            <input
              type="number"
              min="1"
              value={maxMezzi}
              onChange={e => setMaxMezzi(e.target.value)}
              placeholder="es. 1"
            />
          </div>
        </div>

        <div className="params-card">
          <h3>Pausa corsa</h3>
          <div className="params-campo">
            <label>Durata periodo di grazia (minuti — 0 = pausa gratuita disabilitata)</label>
            <input
              type="number"
              min="0"
              value={durataGrazia}
              onChange={e => setDurataGrazia(e.target.value)}
              placeholder="es. 5"
            />
          </div>
          <div className="params-campo">
            <label>Addebito pausa al minuto €/min (0 = nessun addebito)</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={addebitoPausa}
              onChange={e => setAddebitoPausa(e.target.value)}
              placeholder="es. 0.50"
            />
          </div>
        </div>

        {errore && <p className="params-errore">{errore}</p>}
        {conferma && <p className="params-conferma">{conferma}</p>}

        <button className="btn-salva-params" onClick={handleSalva} disabled={caricamento}>
          {caricamento ? '...' : 'Salva parametri'}
        </button>
      </div>
    </div>
  )
}
