import { useState, useEffect, useCallback, useMemo } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { terminaCorsa } from '../../services/CorsaService'
import type { MezzoMappa } from '../../services/MapService'
import { effettuaPagamento } from '../../services/PaymentService'
import './VistaCorsa.css'

interface DatiCorsa {
  corsa_id: string
  mezzo: MezzoMappa
  inizio_at: string
}

type FasePagamento = 'idle' | 'termina' | 'paga' | 'ok' | 'rifiutato' | 'no-metodo' | 'errore'

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60).toString().padStart(2, '0')
  const s = (sec % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

function Batteria({ valore }: { valore: number | null | undefined }) {
  if (valore == null) return <span>N/D</span>
  const barre = Math.min(4, Math.ceil(valore / 25))
  const colore = valore > 50 ? '#4caf9a' : valore > 20 ? '#f59e0b' : '#ef4444'
  return (
    <span style={{ display: 'inline-flex', alignItems: 'flex-end', gap: 3 }}>
      {[1, 2, 3, 4].map(i => (
        <span key={i} style={{
          display: 'inline-block', width: 7, height: 6 + i * 4,
          background: i <= barre ? colore : '#e0e0e0', borderRadius: 2,
        }} />
      ))}
    </span>
  )
}

const GLYPH: Record<string, string> = {
  monopattino: '🛴', bicicletta: '🚲', automobile: '🚗',
}

// Posizione dei satelliti: n=4 → posizioni diagonali come nel mockup
function posSatellite(i: number, n: number, cx: number, cy: number, raggio: number, w: number, h: number) {
  const offset = n === 4 ? -Math.PI / 4 : 0
  const angolo = (i * 2 * Math.PI / n) - Math.PI / 2 + offset
  return {
    left: cx + raggio * Math.cos(angolo) - w / 2,
    top:  cy + raggio * Math.sin(angolo) - h / 2,
  }
}

// [IF-UT.04/IF-UT.06] CS-05/CS-06/CS-07
export default function VistaCorsa() {
  const location = useLocation()
  const navigate = useNavigate()

  // corse è uno stato: i mezzi terminati vengono rimossi dopo il pagamento
  const corseInit = useMemo<DatiCorsa[]>(() => {
    const s = location.state as Record<string, unknown> | null
    if (s?.corse) return s.corse as DatiCorsa[]
    if (s?.mezzo && s?.corsa) {
      const c = s.corsa as { id: string; inizio_at?: string }
      return [{ corsa_id: c.id, mezzo: s.mezzo as MezzoMappa, inizio_at: c.inizio_at ?? new Date().toISOString() }]
    }
    return []
  }, [location.state])

  const [corse, setCorse] = useState<DatiCorsa[]>(corseInit)
  const [selId, setSelId] = useState<string>(() => corseInit[0]?.mezzo.id ?? '')
  const [elapsed, setElapsed] = useState(0)
  const [fase, setFase] = useState<FasePagamento>('idle')
  const [schermataTermina, setSchermataTermina] = useState(false)
  const [daTerminare, setDaTerminare] = useState<Set<string>>(() => new Set(corseInit.map(c => c.corsa_id)))
  const [importoPagato, setImportoPagato] = useState<number | null>(null)
  const [errore, setErrore] = useState('')

  const selCorsa = corse.find(c => c.mezzo.id === selId) ?? corse[0]

  useEffect(() => {
    if (!corse[0]) return
    const inizio = new Date(corse[0].inizio_at).getTime()
    const tick = () => setElapsed(Math.floor((Date.now() - inizio) / 1000))
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [corse])

  const toggleTermina = (corsaId: string) => {
    setDaTerminare(prev => {
      const next = new Set(prev)
      if (next.has(corsaId)) next.delete(corsaId)
      else next.add(corsaId)
      return next
    })
  }

  const handleTermina = useCallback(async () => {
    const da = corse.filter(c => daTerminare.has(c.corsa_id))
    if (da.length === 0) return
    setFase('termina')
    setErrore('')
    try {
      for (const c of da) await terminaCorsa(c.corsa_id)
    } catch {
      setErrore('Errore durante la chiusura. Riprova.')
      setFase('idle')
      return
    }
    setFase('paga')
    try {
      const res = await effettuaPagamento(da[0].corsa_id, da[0].mezzo?.tipo ?? '', elapsed / 60, 0)
      setImportoPagato(res.importo)
      setFase('ok')

      // Rimuovi i mezzi terminati — rimangono solo quelli non selezionati
      const idTerminati = new Set(da.map(c => c.corsa_id))
      const rimanenti = corse.filter(c => !idTerminati.has(c.corsa_id))

      setTimeout(() => {
        if (rimanenti.length > 0) {
          // Torna all'Info Corsa con i mezzi rimasti attivi
          setCorse(rimanenti)
          setDaTerminare(new Set(rimanenti.map(c => c.corsa_id)))
          setSelId(rimanenti[0].mezzo.id)
          setSchermataTermina(false)
          setFase('idle')
          setImportoPagato(null)
        } else {
          navigate('/utente/home', { replace: true })
        }
      }, 2000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 400) setFase('no-metodo')
      else if (axios.isAxiosError(err) && err.response?.status === 402) setFase('rifiutato')
      else setFase('errore')
    }
  }, [corse, daTerminare, elapsed, navigate])

  if (!corse.length) return (
    <div className="vista-corsa-wrap">
      <button type="button" className="btn-back-corsa" onClick={() => navigate(-1)}>← Torna alla mappa</button>
      <p style={{ color: '#888', marginTop: 32, textAlign: 'center' }}>Nessuna corsa attiva.</p>
    </div>
  )

  // Costanti geometria cerchi
  const CONTAINER = 300
  const CX = CONTAINER / 2
  const CY = CONTAINER / 2
  const CENT = 124
  const SAT = 76
  const SAT_H = 90   // cerchio + testo codice
  const RAG = 104

  const satellites = corse.filter(c => c.mezzo.id !== selId)

  return (
    <div className="vista-corsa-wrap">
      {/* ── Info corsa ── */}
      <h1 className="corsa-titolo">Info corsa</h1>

      {/* Cerchi */}
      <div className="cerchi-container" style={{ width: CONTAINER, height: CONTAINER }}>
        {/* Satelliti */}
        {satellites.map((c, i) => {
          const pos = posSatellite(i, Math.max(satellites.length, 1), CX, CY, RAG, SAT, SAT_H)
          return (
            <button
              key={c.corsa_id}
              className="cerchio-sat-wrap"
              style={{ left: pos.left, top: pos.top }}
              onClick={() => setSelId(c.mezzo.id)}
            >
              <div className="cerchio cerchio--satellite" style={{ width: SAT, height: SAT }}>
                <span className="cerchio-glyph" style={{ fontSize: 28 }}>{GLYPH[c.mezzo.tipo] ?? '●'}</span>
              </div>
              <span className="cerchio-codice">{c.mezzo.codice}</span>
            </button>
          )
        })}

        {/* Cerchio centrale */}
        <div
          className="cerchio cerchio--centrale"
          style={{ width: CENT, height: CENT, left: (CONTAINER - CENT) / 2, top: (CONTAINER - CENT) / 2 }}
        >
          <span className="cerchio-glyph" style={{ fontSize: 48 }}>{GLYPH[selCorsa?.mezzo.tipo ?? ''] ?? '●'}</span>
          <span className="cerchio-codice-cent">{selCorsa?.mezzo.codice}</span>
        </div>
      </div>

      {/* Tabella info */}
      <table className="corsa-tabella">
        <tbody>
          <tr><td>ID Mezzo:</td><td>{selCorsa?.mezzo.codice}</td></tr>
          <tr><td>Carica rimanente:</td><td><Batteria valore={selCorsa?.mezzo.batteria} /></td></tr>
          <tr><td>Tempo trascorso:</td><td>{formatTime(elapsed)}</td></tr>
          <tr><td>Km percorsi:</td><td>0,0</td></tr>
        </tbody>
      </table>

      <div className="corsa-logo">
        <span className="corsa-logo-icona">🔄</span>
        <span className="corsa-logo-testo"><strong>SMART</strong> MOBILITY</span>
      </div>

      {/* Esiti */}
      {fase === 'ok' && (
        <div className="corsa-esito corsa-esito--ok">
          <span className="corsa-esito-icona">✅</span>
          <p className="corsa-esito-testo">Pagamento di <strong>€{importoPagato?.toFixed(2)}</strong> completato.</p>
          <p className="corsa-esito-sub">Torno alla mappa...</p>
        </div>
      )}
      {(fase === 'rifiutato' || fase === 'no-metodo' || fase === 'errore') && (
        <div className="corsa-esito corsa-esito--errore">
          <span className="corsa-esito-icona">{fase === 'rifiutato' ? '❌' : '⚠️'}</span>
          <p className="corsa-esito-testo">
            {fase === 'no-metodo' ? 'Metodo di pagamento non configurato.'
             : fase === 'rifiutato' ? 'Pagamento rifiutato.'
             : 'Errore nel servizio di pagamento.'}
          </p>
          {fase === 'no-metodo'
            ? <button type="button" className="btn-corsa btn-termina" onClick={() => navigate('/utente/pagamenti')}>Gestisci pagamenti</button>
            : <button type="button" className="btn-corsa btn-termina" onClick={() => setFase('idle')}>Riprova</button>
          }
        </div>
      )}

      {(fase === 'idle' || fase === 'termina' || fase === 'paga') && (
        <div className="corsa-bottoni">
          <button type="button" className="btn-corsa btn-termina" onClick={() => setSchermataTermina(true)}>
            TERMINA E PAGA
          </button>
          <button type="button" className="btn-corsa btn-pausa" disabled>PAUSA CORSA</button>
        </div>
      )}

      {/* ── Modal Termina Corsa — overlay sfocato ── */}
      {schermataTermina && (
        <div className="termina-overlay">
          <div className="termina-card">
            <p className="termina-counter">{daTerminare.size}/{corse.length}</p>

            <ul className="termina-lista">
              {corse.map(c => (
                <li key={c.corsa_id} className="termina-item">
                  <span className="termina-icona-mezzo">{GLYPH[c.mezzo.tipo] ?? '●'}</span>
                  <span className="termina-codice">{c.mezzo.codice}</span>
                  <button
                    className={`termina-btn termina-btn--ok${daTerminare.has(c.corsa_id) ? ' termina-btn--attivo' : ''}`}
                    onClick={() => !daTerminare.has(c.corsa_id) && toggleTermina(c.corsa_id)}
                    title="Termina"
                  >✓</button>
                  <button
                    className={`termina-btn termina-btn--no${!daTerminare.has(c.corsa_id) ? ' termina-btn--attivo' : ''}`}
                    onClick={() => daTerminare.has(c.corsa_id) && toggleTermina(c.corsa_id)}
                    title="Salta"
                  >✕</button>
                </li>
              ))}
            </ul>

            {errore && <p className="corsa-errore">{errore}</p>}

            <div className="termina-bottoni">
              <button
                type="button"
                className="btn-corsa btn-termina btn-termina-tutti"
                onClick={handleTermina}
                disabled={daTerminare.size === 0 || fase !== 'idle'}
              >
                {fase === 'termina' ? 'Chiusura...'
                  : fase === 'paga' ? 'Addebito...'
                  : daTerminare.size === corse.length ? 'TERMINA TUTTI' : 'TERMINA'}
              </button>
              <button
                type="button"
                className="btn-corsa btn-annulla-termina"
                onClick={() => { setSchermataTermina(false); setFase('idle'); setErrore('') }}
              >
                ANNULLA
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}