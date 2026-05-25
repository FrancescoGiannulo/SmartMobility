import { useState, useEffect, useCallback } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { sbloccaMezzo, type CorsaAttiva } from '../../services/CorsaService'
import type { MezzoMappa } from '../../services/MapService'
import './VistaCorsa.css'

type Fase = 'pre_sblocco' | 'attiva'

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60).toString().padStart(2, '0')
  const s = (sec % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

function emojiMezzo(tipo?: string): string {
  if (tipo === 'monopattino') return '🛴'
  if (tipo === 'bicicletta') return '🚲'
  if (tipo === 'automobile') return '🚗'
  return '🚲'
}

// [IF-UT.04] CS-10 — Sblocca Mezzo / IUI-8
export default function VistaCorsa() {
  const { idMezzo } = useParams<{ idMezzo: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const mezzo = location.state?.mezzo as MezzoMappa | undefined

  const [fase, setFase] = useState<Fase>('pre_sblocco')
  const [corsa, setCorsa] = useState<CorsaAttiva | null>(null)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    if (fase !== 'attiva') return
    const t = setInterval(() => setElapsed(e => e + 1), 1000)
    return () => clearInterval(t)
  }, [fase])

  const handleSblocca = useCallback(async () => {
    if (!idMezzo) return
    setCaricamento(true)
    setErrore('')
    try {
      const c = await sbloccaMezzo(idMezzo)
      setCorsa(c)
      setFase('attiva')
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErrore('Mezzo non più disponibile. Torna alla mappa.')
      } else if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Mezzo non trovato.')
      } else {
        setErrore('Errore durante lo sblocco. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }, [idMezzo])

  if (fase === 'pre_sblocco') {
    return (
      <div className="vista-corsa">
        <button className="btn-back" onClick={() => navigate(-1)}>
          ← Torna alla mappa
        </button>
        <div className="corsa-card">
          <div className="corsa-emoji">{emojiMezzo(mezzo?.tipo)}</div>
          <h2>{mezzo?.tipo ?? 'Mezzo'}</h2>
          <p className="corsa-codice">ID: {mezzo?.codice ?? idMezzo}</p>
          {mezzo?.batteria != null && (
            <p className="corsa-batteria">🔋 {mezzo.batteria}%</p>
          )}
          {errore && <p className="corsa-errore">{errore}</p>}
          <button
            className="btn-sblocca"
            onClick={handleSblocca}
            disabled={caricamento}
          >
            {caricamento ? 'Sblocco in corso...' : 'SBLOCCA'}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="vista-corsa attiva">
      <div className="corsa-card">
        <div className="corsa-emoji">{emojiMezzo(mezzo?.tipo)}</div>
        <table className="corsa-info">
          <tbody>
            <tr>
              <td>ID mezzo</td>
              <td>{mezzo?.codice ?? corsa?.mezzo_id}</td>
            </tr>
            <tr>
              <td>Batteria</td>
              <td>{mezzo?.batteria != null ? `${mezzo.batteria}%` : '—'}</td>
            </tr>
            <tr>
              <td>Tempo</td>
              <td>{formatTime(elapsed)}</td>
            </tr>
            <tr>
              <td>Km</td>
              <td>0.0</td>
            </tr>
          </tbody>
        </table>
        <div className="corsa-azioni">
          <button className="btn-pausa" disabled>PAUSA CORSA</button>
          <button className="btn-termina" disabled>TERMINA E PAGA</button>
        </div>
      </div>
    </div>
  )
}
