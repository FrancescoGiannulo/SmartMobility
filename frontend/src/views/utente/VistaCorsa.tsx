import { useState, useEffect, useCallback } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { terminaCorsa, type CorsaAttiva } from '../../services/CorsaService'
import type { MezzoMappa } from '../../services/MapService'
import { effettuaPagamento } from '../../services/PaymentService'
import './VistaCorsa.css'

type FasePagamento = 'idle' | 'termina' | 'paga' | 'ok' | 'rifiutato' | 'no-metodo'

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60).toString().padStart(2, '0')
  const s = (sec % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

function IconaMezzo({ tipo }: { tipo?: string }) {
  const emoji = tipo === 'monopattino' ? '🛴' : tipo === 'bicicletta' ? '🚲' : '🚗'
  return <div className="corsa-icona-mezzo">{emoji}</div>
}

function Batteria({ valore }: { valore: number | null | undefined }) {
  if (valore == null) return <span>N/D</span>
  const barre = Math.min(4, Math.ceil(valore / 25))
  const colore = valore > 50 ? '#4caf9a' : valore > 20 ? '#f59e0b' : '#ef4444'
  return (
    <span style={{ display: 'inline-flex', alignItems: 'flex-end', gap: 3 }}>
      {[1, 2, 3, 4].map(i => (
        <span key={i} style={{
          display: 'inline-block',
          width: 7,
          height: 6 + i * 4,
          background: i <= barre ? colore : '#e0e0e0',
          borderRadius: 2,
        }} />
      ))}
    </span>
  )
}

// [IF-UT.04/IF-UT.06] CS-10/CS-11 — Info Corsa / IUI-8
export default function VistaCorsa() {
  const { idMezzo } = useParams<{ idMezzo: string }>()
  const location = useLocation()
  const navigate = useNavigate()

  const mezzo = location.state?.mezzo as MezzoMappa | undefined
  const corsaPassata = location.state?.corsa as CorsaAttiva | undefined

  const [corsa] = useState<CorsaAttiva | null>(corsaPassata ?? null)
  const [elapsed, setElapsed] = useState(0)
  const [fase, setFase] = useState<FasePagamento>('idle')
  const [importoPagato, setImportoPagato] = useState<number | null>(null)
  const [errore, setErrore] = useState('')

  useEffect(() => {
    if (!corsa) return
    const inizio = new Date(corsa.inizio_at).getTime()
    const tick = () => setElapsed(Math.floor((Date.now() - inizio) / 1000))
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [corsa])

  // [IF-UT.06 + IF-UT.17] CS-06 termina corsa → CS-07 effettua pagamento
  const handleTermina = useCallback(async () => {
    if (!corsa) return
    setErrore('')

    setFase('termina')
    try {
      await terminaCorsa(corsa.id)
    } catch {
      setErrore('Errore durante la chiusura della corsa. Riprova.')
      setFase('idle')
      return
    }

    setFase('paga')
    try {
      const durata_min = elapsed / 60
      const risultato = await effettuaPagamento(corsa.id, mezzo?.tipo ?? '', durata_min, 0)
      setImportoPagato(risultato.importo)
      setFase('ok')
      setTimeout(() => navigate('/utente/home', { replace: true }), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 400) {
        setFase('no-metodo')
      } else {
        setFase('rifiutato')
      }
    }
  }, [corsa, mezzo, elapsed, navigate])

  if (!corsa) {
    return (
      <div className="vista-corsa-wrap">
        <button type="button" className="btn-back-corsa" onClick={() => navigate(-1)}>← Torna alla mappa</button>
        <p style={{ color: '#888', marginTop: 32, textAlign: 'center' }}>
          Nessuna corsa attiva. Torna alla mappa e clicca su un mezzo.
        </p>
      </div>
    )
  }

  return (
    <div className="vista-corsa-wrap">
      <h1 className="corsa-titolo">Info corsa</h1>

      <IconaMezzo tipo={mezzo?.tipo} />

      <table className="corsa-tabella">
        <tbody>
          <tr>
            <td>ID Mezzo:</td>
            <td>{mezzo?.codice ?? idMezzo}</td>
          </tr>
          <tr>
            <td>Carica rimanente:</td>
            <td><Batteria valore={mezzo?.batteria} /></td>
          </tr>
          <tr>
            <td>Tempo trascorso:</td>
            <td>{formatTime(elapsed)}</td>
          </tr>
          <tr>
            <td>Km percorsi:</td>
            <td>0,0</td>
          </tr>
        </tbody>
      </table>

      <div className="corsa-logo">
        <span className="corsa-logo-icona">🔄</span>
        <span className="corsa-logo-testo"><strong>SMART</strong> MOBILITY</span>
      </div>

      {errore && <p className="corsa-errore">{errore}</p>}

      {fase === 'ok' && (
        <div className="corsa-esito corsa-esito--ok">
          <span className="corsa-esito-icona">✅</span>
          <p className="corsa-esito-testo">
            Pagamento di <strong>€{importoPagato?.toFixed(2)}</strong> completato.
          </p>
          <p className="corsa-esito-sub">Torno alla mappa...</p>
        </div>
      )}

      {fase === 'rifiutato' && (
        <div className="corsa-esito corsa-esito--errore">
          <span className="corsa-esito-icona">❌</span>
          <p className="corsa-esito-testo">Pagamento rifiutato.</p>
          <button type="button" className="btn-corsa btn-termina" onClick={() => navigate('/utente/pagamenti')}>
            Aggiorna metodo di pagamento
          </button>
        </div>
      )}

      {fase === 'no-metodo' && (
        <div className="corsa-esito corsa-esito--errore">
          <span className="corsa-esito-icona">⚠️</span>
          <p className="corsa-esito-testo">Nessun metodo di pagamento predefinito.</p>
          <button type="button" className="btn-corsa btn-termina" onClick={() => navigate('/utente/pagamenti')}>
            Aggiungi metodo di pagamento
          </button>
        </div>
      )}

      {(fase === 'idle' || fase === 'termina' || fase === 'paga') && (
        <div className="corsa-bottoni">
          <button
            type="button"
            className="btn-corsa btn-termina"
            onClick={handleTermina}
            disabled={fase !== 'idle'}
          >
            {fase === 'termina' ? 'Chiusura...' : fase === 'paga' ? 'Addebito...' : 'TERMINA E PAGA'}
          </button>
          <button type="button" className="btn-corsa btn-pausa" disabled>PAUSA CORSA</button>
        </div>
      )}
    </div>
  )
}
