import { useState, useEffect, useCallback, useMemo, useRef } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useMapsLibrary } from '@vis.gl/react-google-maps'
import axios from 'axios'
import { terminaCorsa, sospendiCorsa, riprendiCorsa, getRiepilogoCorsa, aggiornaPosizioneDemo, type Corsa, type RispostaSospensione } from '../../services/CorsaService'
import type { MezzoMappa } from '../../services/MapService'
import { getZoneUtente, type ZonaMappa } from '../../services/MapService'
import { effettuaPagamento, getMetodiPagamento, getPromozioni, type Promozione } from '../../services/PaymentService'
import { getAbbonamentoCorrente } from '../../services/AbbonamentoService'
import { puntoInPoligono, distanzaDaPoligono, zonaCorrente, type TipoZonaCorrente } from '../../utils/geoUtils'
import { utenteCorrente } from '../../services/AuthService'
import './VistaCorsa.css'

interface DatiCorsa {
  corsa_id: string
  mezzo: MezzoMappa
  inizio_at: string
  gruppo_corsa_id?: string | null
}

type FasePagamento = 'idle' | 'termina' | 'scegli-promo' | 'paga' | 'ok' | 'rifiutato' | 'no-metodo' | 'errore'

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60).toString().padStart(2, '0')
  const s = (sec % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

// Distanza in km tra due punti (haversine) — usata per il contatore km durante la demo.
function distanzaKm(aLat: number, aLng: number, bLat: number, bLng: number): number {
  const R = 6371, toRad = Math.PI / 180
  const dLat = (bLat - aLat) * toRad, dLng = (bLng - aLng) * toRad
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(aLat * toRad) * Math.cos(bLat * toRad) * Math.sin(dLng / 2) ** 2
  return 2 * R * Math.asin(Math.sqrt(h))
}

type PuntoLL = { lat: number; lng: number }

// Lunghezze cumulative (in metri) lungo una polilinea, per muoversi a velocità costante.
function lunghezzeCumulativeM(path: PuntoLL[]): number[] {
  const cum = [0]
  for (let i = 1; i < path.length; i++) {
    cum[i] = cum[i - 1] + distanzaKm(path[i - 1].lat, path[i - 1].lng, path[i].lat, path[i].lng) * 1000
  }
  return cum
}

// Punto sulla polilinea a distanza `d` metri dall'inizio (interpolazione sul segmento).
function puntoADistanzaM(path: PuntoLL[], cum: number[], d: number): PuntoLL {
  const totale = cum[cum.length - 1]
  if (d <= 0) return path[0]
  if (d >= totale) return path[path.length - 1]
  let i = 1
  while (i < cum.length && cum[i] < d) i++
  const segLen = (cum[i] - cum[i - 1]) || 1
  const t = (d - cum[i - 1]) / segLen
  return {
    lat: path[i - 1].lat + (path[i].lat - path[i - 1].lat) * t,
    lng: path[i - 1].lng + (path[i].lng - path[i - 1].lng) * t,
  }
}

function Batteria({ valore }: { valore: number | null | undefined }) {
  if (valore == null) return <span>N/D</span>
  const barre = Math.min(4, Math.ceil(valore / 25))
  const colore = valore > 50 ? '#155e52' : valore > 20 ? '#f59e0b' : '#ef4444'
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

// Posizioni sempre sfalsate/diagonali (offset -π/4 fisso)
// n=1 → top-right; n=2 → top-left + bottom-right; n=4 → angoli
function posSatellite(i: number, n: number, cx: number, cy: number, raggio: number, w: number, h: number) {
  const angolo = (i * 2 * Math.PI / n) - Math.PI / 2 - Math.PI / 4
  return {
    left: cx + raggio * Math.cos(angolo) - w / 2,
    top:  cy + raggio * Math.sin(angolo) - h / 2,
  }
}

// [IF-UT.04/IF-UT.06] CS-05/UT-08/CS-07
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
  const [inPausa, setInPausa] = useState(false)
  const [pausaLoading, setPausaLoading] = useState(false)
  const [pausaInfo, setPausaInfo] = useState<RispostaSospensione | null>(null)
  const [graziaResiduaSec, setGraziaResiduaSec] = useState<number | null>(null)
  const [fase, setFase] = useState<FasePagamento>('idle')
  const [schermataTermina, setSchermataTermina] = useState(false)
  const [daTerminare, setDaTerminare] = useState<Set<string>>(() => new Set(corseInit.map(c => c.corsa_id)))
  const [importoPagato, setImportoPagato] = useState<number | null>(null)
  const [errore, setErrore] = useState('')
  const [promozioniDisp, setPromozioniDisp] = useState<Promozione[]>([])
  const [corsePerPagamento, setCorsePerPagamento] = useState<DatiCorsa[]>([])
  const [riepilogoData, setRiepilogoData] = useState<{
    riepilogo: Corsa
    daTerminate: DatiCorsa[]
  } | null>(null)

  const [zoneOperative, setZoneOperative] = useState<ZonaMappa[]>([])
  const [fuoriZona, setFuoriZona] = useState(false)
  const watchIdRef = useRef<number | null>(null)

  const [zoneTutte, setZoneTutte] = useState<ZonaMappa[]>([])
  const [statoZonaDemo, setStatoZonaDemo] = useState<{ tipo: TipoZonaCorrente; limiteVelocita?: number } | null>(null)
  const demoTimerRef = useRef<number | null>(null)
  const penaleRef = useRef(false)
  const inPausaRef = useRef(false)
  const terminatiRef = useRef<Set<string>>(new Set())
  const routesLib = useMapsLibrary('routes')
  const [kmDemo, setKmDemo] = useState(0)
  const demoAttivo = statoZonaDemo !== null
  const emailDemo = import.meta.env.VITE_DEMO_EMAIL as string | undefined
  const isAccountDemo = !!emailDemo && utenteCorrente()?.profilo.email === emailDemo

  const MARGINE_FUORI_ZONA_M = 200

  const selCorsa = corse.find(c => c.mezzo.id === selId) ?? corse[0]

  useEffect(() => {
    if (!corse[0]) return
    const inizio = new Date(corse[0].inizio_at).getTime()
    const tick = () => setElapsed(Math.floor((Date.now() - inizio) / 1000))
    tick()
    const t = setInterval(tick, 1000)
    return () => clearInterval(t)
  }, [corse])

  // [IF-UT.10] Countdown grace period durante la pausa (msg16: mostraSospensione)
  useEffect(() => {
    if (!inPausa || graziaResiduaSec === null || graziaResiduaSec <= 0) return
    const t = setInterval(() => setGraziaResiduaSec(prev => (prev !== null && prev > 0) ? prev - 1 : 0), 1000)
    return () => clearInterval(t)
  }, [inPausa, graziaResiduaSec])

  useEffect(() => {
    getZoneUtente()
      .then(zone => {
        setZoneOperative(zone.filter(z => z.tipo === 'operativa' && z.attiva))
        setZoneTutte(zone.filter(z => z.attiva))
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (zoneOperative.length === 0) return
    const onPosition = (pos: GeolocationPosition) => {
      const { latitude, longitude } = pos.coords
      const dentroAlmenoUna = zoneOperative.some(z => puntoInPoligono(latitude, longitude, z.perimetro))
      if (dentroAlmenoUna) {
        setFuoriZona(false)
        return
      }
      const distMin = Math.min(...zoneOperative.map(z => distanzaDaPoligono(latitude, longitude, z.perimetro)))
      setFuoriZona(distMin > MARGINE_FUORI_ZONA_M)
    }
    watchIdRef.current = navigator.geolocation.watchPosition(onPosition, () => {}, {
      enableHighAccuracy: true,
      maximumAge: 5000,
    })
    return () => {
      if (watchIdRef.current !== null) navigator.geolocation.clearWatch(watchIdRef.current)
    }
  }, [zoneOperative, MARGINE_FUORI_ZONA_M])

  const toggleTermina = (corsaId: string) => {
    setDaTerminare(prev => {
      const next = new Set(prev)
      if (next.has(corsaId)) next.delete(corsaId)
      else next.add(corsaId)
      return next
    })
  }

  const handlePaga = useCallback(async (da: DatiCorsa[], offertaId?: string) => {
    setFase('paga')
    try {
      // [IF-UT.20] Per corse di gruppo ogni mezzo ha il proprio pagamento; somma i totali
      let totaleImporto = 0
      for (const corsa of da) {
        const res = await effettuaPagamento(corsa.corsa_id, corsa.mezzo?.tipo ?? '', elapsed / 60, 0, offertaId, penaleRef.current)
        totaleImporto += res.importo
      }
      setImportoPagato(totaleImporto)
      // [IF-UT.07] Recupera riepilogo dal backend e mostralo all'utente
      try {
        const riepilogo = await getRiepilogoCorsa(da[0].corsa_id)
        // Per gruppo: costo_totale del riepilogo è la somma di tutti i pagamenti
        setRiepilogoData({
          riepilogo: da.length > 1 ? { ...riepilogo, costo_totale: totaleImporto } : riepilogo,
          daTerminate: da,
        })
      } catch {
        // fallback: costruisci riepilogo minimo da dati client
        setRiepilogoData({
          riepilogo: {
            id: da[0].corsa_id,
            inizio_at: da[0].inizio_at,
            fine_at: new Date().toISOString(),
            costo_totale: totaleImporto,
            stato: 'terminata',
            distanza_km: 0,
            gruppo_corsa_id: da[0].gruppo_corsa_id ?? null,
            importo_pieno: null,
            tipo_mezzo: da[0].mezzo?.tipo ?? null,
            codice_mezzo: da[0].mezzo?.codice ?? null,
            durata_min: null,
            nome_offerta_applicata: null,
          },
          daTerminate: da,
        })
      }
      setFase('ok')
    } catch (err) {
      setSchermataTermina(false)
      if (axios.isAxiosError(err) && err.response?.status === 400) setFase('no-metodo')
      else if (axios.isAxiosError(err) && err.response?.status === 402) setFase('rifiutato')
      else setFase('errore')
    }
  }, [elapsed, navigate])

  // [IF-UT.07] Torna alla mappa dopo aver visualizzato il riepilogo
  const handleTornaAllaMappa = useCallback(() => {
    if (!riepilogoData) return
    const idTerminati = new Set(riepilogoData.daTerminate.map(c => c.corsa_id))
    const rimanenti = corse.filter(c => !idTerminati.has(c.corsa_id))
    if (rimanenti.length > 0) {
      setCorse(rimanenti)
      setDaTerminare(new Set(rimanenti.map(c => c.corsa_id)))
      setSelId(rimanenti[0].mezzo.id)
      setSchermataTermina(false)
      setFase('idle')
      setImportoPagato(null)
      setRiepilogoData(null)
    } else {
      navigate('/utente/home', { replace: true })
    }
  }, [corse, navigate, riepilogoData])

  const handlePausa = useCallback(async () => {
    if (!selCorsa) return
    setPausaLoading(true)
    try {
      if (inPausa) {
        await riprendiCorsa(selCorsa.corsa_id)
        setInPausa(false)
        setPausaInfo(null)
        setGraziaResiduaSec(null)
      } else {
        // [IF-UT.10] msg2: sospendiCorsa(idCorsa) → msg16: mostraSospensione(tempoGratuitoResiduo, politicaAddebito)
        const risposta = await sospendiCorsa(selCorsa.corsa_id)
        setInPausa(true)
        setPausaInfo(risposta)
        setGraziaResiduaSec(risposta.tempo_gratuito_residuo_sec)
      }
    } catch {
      // Ignora errori di rete: lo stato si risincronizza al prossimo aggiornamento
    } finally {
      setPausaLoading(false)
    }
  }, [selCorsa, inPausa])

  const handleTermina = useCallback(async () => {
    const da = corse.filter(c => daTerminare.has(c.corsa_id))
    if (da.length === 0) return
    setFase('termina')
    setErrore('')
    // [CS-07 precondition] Verifica metodo predefinito PRIMA di terminare la corsa.
    // Se manca, la corsa rimane attiva e l'utente può aggiungere un metodo.
    try {
      const metodi = await getMetodiPagamento()
      if (!metodi.some(m => m.predefinito)) {
        setSchermataTermina(false)
        setFase('no-metodo')
        return
      }
    } catch { /* errore rete: il backend gestirà il 400 se necessario */ }
    try {
      for (const c of da) await terminaCorsa(c.corsa_id)
    } catch {
      setErrore('Errore durante la chiusura. Riprova.')
      setFase('idle')
      return
    }
    // Demo: i mezzi terminati si fermano subito (non vengono più mossi dal driver)
    da.forEach(c => terminatiRef.current.add(c.corsa_id))
    // [IF-UT.16] Abbonamento attivo → corsa gratuita (non si applica alle corse di gruppo)
    const isGruppo = da.some(c => c.gruppo_corsa_id)
    if (!isGruppo) {
      try {
        const abb = await getAbbonamentoCorrente()
        if (abb && new Date(abb.data_fine) > new Date()) {
          await handlePaga(da)
          return
        }
      } catch {
        // Errore di rete: saltiamo le promozioni per non mostrarle a chi ha l'abbonamento attivo
        await handlePaga(da)
        return
      }
    }
    // Dopo la chiusura controlla promozioni disponibili
    try {
      const r = await getPromozioni()
      const lista = Array.isArray(r.data) ? r.data : []
      if (lista.length > 0) {
        setPromozioniDisp(lista)
        setCorsePerPagamento(da)
        setFase('scegli-promo')
        return
      }
    } catch { /* nessuna promo o errore rete: prosegui senza */ }
    await handlePaga(da)
  }, [corse, daTerminare, handlePaga])

  // --- Demo movimento (helper di presentazione, solo account demo) ---
  // Giro su strada (Google Directions) a velocità realistica: attraversa zona limitata e
  // vietata, esce dalla zona operativa e rientra a parcheggiare dove il mezzo è stato preso.
  const avviaDemoMovimento = useCallback(async () => {
    if (corse.length === 0 || zoneTutte.length === 0 || demoTimerRef.current !== null) return

    const CAMPUS: PuntoLL = { lat: 41.1095, lng: 16.8806 }       // limitata (vmax 15)
    const POLITECNICO: PuntoLL = { lat: 41.1093, lng: 16.8791 }  // vietata (dentro Campus)
    const OPERATIVA_CENTRO: PuntoLL = { lat: 41.11033, lng: 16.86814 }
    const start: PuntoLL = { lat: corse[0].mezzo.lat, lng: corse[0].mezzo.lng }

    // Primo punto appena fuori dalla zona operativa, oltre il Politecnico (escursione minima).
    const dLat = POLITECNICO.lat - OPERATIVA_CENTRO.lat
    const dLng = POLITECNICO.lng - OPERATIVA_CENTRO.lng
    const norm = Math.hypot(dLat, dLng) || 1
    let fuori: PuntoLL = { ...POLITECNICO }
    for (let s = 0; s < 120; s++) {
      fuori = { lat: fuori.lat + (dLat / norm) * 0.0015, lng: fuori.lng + (dLng / norm) * 0.0015 }
      if (zonaCorrente(fuori.lat, fuori.lng, zoneTutte).tipo === 'fuori') break
    }

    // Percorso su strada (round trip). Fallback a linea retta se Directions non è disponibile.
    let path: PuntoLL[] = []
    if (routesLib) {
      try {
        const ds = new routesLib.DirectionsService()
        const res = await ds.route({
          origin: start,
          destination: start,
          waypoints: [CAMPUS, POLITECNICO, fuori].map(w => ({ location: w, stopover: false })),
          travelMode: google.maps.TravelMode.DRIVING,
        })
        const op = res.routes[0]?.overview_path
        if (op?.length) path = op.map(p => ({ lat: p.lat(), lng: p.lng() }))
      } catch { /* fallback sotto */ }
    }
    if (path.length < 2) {
      const interp = (a: PuntoLL, b: PuntoLL, n: number): PuntoLL[] =>
        Array.from({ length: n }, (_, k) => ({ lat: a.lat + (b.lat - a.lat) * (k + 1) / n, lng: a.lng + (b.lng - a.lng) * (k + 1) / n }))
      path = [start, ...interp(start, CAMPUS, 6), ...interp(CAMPUS, POLITECNICO, 3), ...interp(POLITECNICO, fuori, 6), ...interp(fuori, start, 10)]
    }

    const cum = lunghezzeCumulativeM(path)
    const totale = cum[cum.length - 1]
    const VEL_KMH = 22, TICK_SEC = 1.5, GAP_M = 25
    const passoM = (VEL_KMH / 3.6) * TICK_SEC
    const ordine: Record<TipoZonaCorrente, number> = { vietata: 0, fuori: 1, limitata: 2, operativa: 3 }
    const startBatt = corse.map(c => c.mezzo.batteria ?? 100)
    const CONSUMO_DEMO_PER_KM = 15  // calo batteria ben visibile durante la demo

    const avvioCorse = corse
    terminatiRef.current = new Set()
    penaleRef.current = false
    setKmDemo(0)
    let d = 0
    demoTimerRef.current = window.setInterval(() => {
      // Pausa: i mezzi si fermano finché la corsa è in pausa (come nell'app reale)
      if (inPausaRef.current) return
      let aggregato: { tipo: TipoZonaCorrente; limiteVelocita?: number } = { tipo: 'operativa' }
      const nuoveBatt: Record<string, number> = {}
      let qualcunoSiMuove = false
      avvioCorse.forEach((c, i) => {
        if (terminatiRef.current.has(c.corsa_id)) return  // mezzo terminato dall'utente: resta fermo
        const dm = Math.max(0, Math.min(totale, d - i * GAP_M))
        if (d - i * GAP_M < totale) qualcunoSiMuove = true
        const p = puntoADistanzaM(path, cum, dm)
        const z = zonaCorrente(p.lat, p.lng, zoneTutte)
        if (z.tipo === 'vietata' || z.tipo === 'fuori') penaleRef.current = true
        if (ordine[z.tipo] < ordine[aggregato.tipo]) aggregato = z
        const batt = Math.max(5, Math.round(startBatt[i] - CONSUMO_DEMO_PER_KM * (dm / 1000)))
        nuoveBatt[c.corsa_id] = batt
        aggiornaPosizioneDemo(c.corsa_id, p.lat, p.lng, batt).catch(() => {})
      })
      // Aggiorna la batteria mostrata (cala col movimento)
      setCorse(prev => prev.map(c => c.corsa_id in nuoveBatt
        ? { ...c, mezzo: { ...c.mezzo, batteria: nuoveBatt[c.corsa_id] } } : c))
      setStatoZonaDemo(aggregato)
      setKmDemo(Math.min(totale, d) / 1000)
      d += passoM
      // Fine quando nessun mezzo (non terminato) è più in movimento: tutti arrivati o terminati.
      if (!qualcunoSiMuove && demoTimerRef.current !== null) {
        clearInterval(demoTimerRef.current)
        demoTimerRef.current = null
        setStatoZonaDemo(null)
      }
    }, TICK_SEC * 1000)
  }, [corse, zoneTutte, routesLib])

  // Cleanup del timer demo allo smontaggio
  useEffect(() => () => {
    if (demoTimerRef.current !== null) clearInterval(demoTimerRef.current)
  }, [])

  // Sincronizza lo stato di pausa col driver demo (i mezzi si fermano in pausa)
  useEffect(() => { inPausaRef.current = inPausa }, [inPausa])

  if (!corse.length) return (
    <div className="vista-corsa-wrap">
      <button type="button" className="btn-back-corsa" onClick={() => navigate(-1)}>← Torna alla mappa</button>
      <p style={{ color: '#888', marginTop: 32, textAlign: 'center' }}>Nessuna corsa attiva.</p>
    </div>
  )

  // Costanti geometria cerchi
  const CONTAINER = 330
  const CX = CONTAINER / 2
  const CY = CONTAINER / 2
  const CENT = 126
  const SAT = 72
  const SAT_H = 86   // cerchio + testo codice
  const RAG = 122    // gap visibile ≈ 63-36=27px tra i bordi

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
              style={{ left: pos.left, top: pos.top, animationDelay: `${i * 0.55}s` }}
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
          <tr><td>Km percorsi:</td><td>{kmDemo.toFixed(2).replace('.', ',')}</td></tr>
        </tbody>
      </table>

      {demoAttivo && statoZonaDemo?.tipo === 'limitata' && (
        <div className="zona-warning-banner zona-warning-limitata">
          <span className="zona-warning-icona">🐢</span>
          <div className="zona-warning-testo">
            <strong>Zona a velocità limitata</strong>
            <span>Velocità massima consentita: {statoZonaDemo.limiteVelocita ?? '—'} km/h.</span>
          </div>
        </div>
      )}

      {demoAttivo && statoZonaDemo?.tipo === 'vietata' && (
        <div className="zona-warning-banner zona-warning-vietata">
          <span className="zona-warning-icona">⛔</span>
          <div className="zona-warning-testo">
            <strong>Zona vietata</strong>
            <span>Esci dall'area: a fine corsa verrà applicata una penale.</span>
          </div>
        </div>
      )}

      {((demoAttivo && statoZonaDemo?.tipo === 'fuori') || (!demoAttivo && fuoriZona)) && (
        <div className="zona-warning-banner">
          <span className="zona-warning-icona">⚠️</span>
          <div className="zona-warning-testo">
            <strong>Fuori dalla zona operativa</strong>
            <span>Torna indietro per continuare a usufruire del servizio.</span>
          </div>
        </div>
      )}

      {isAccountDemo && corse.length > 0 && fase === 'idle' && (
        <button type="button" className="btn-demo-movimento" onClick={avviaDemoMovimento} disabled={demoTimerRef.current !== null}>
          ▶ Avvia demo movimento
        </button>
      )}

      <div className="corsa-logo">
        <span className="corsa-logo-icona">🔄</span>
        <span className="corsa-logo-testo"><strong>SMART</strong> MOBILITY</span>
      </div>

      {/* [IF-UT.07] Riepilogo corsa */}
      {fase === 'ok' && riepilogoData && (
        <div className="riepilogo-overlay">
          <div className="riepilogo-card">
            <div className="riepilogo-header">
              <span className="riepilogo-check">✅</span>
              <h2 className="riepilogo-titolo">Riepilogo Corsa</h2>
            </div>

            {/* [IF-UT.07] mostraRiepilogo(Corsa) — dettaglio per ogni mezzo */}
            {(() => {
              const r = riepilogoData.riepilogo
              const durataMin = r.fine_at
                ? (new Date(r.fine_at).getTime() - new Date(r.inizio_at).getTime()) / 60000
                : elapsed / 60
              return (
                <>
                  <ul className="riepilogo-mezzi">
                    {riepilogoData.daTerminate.map(c => (
                      <li key={c.corsa_id} className="riepilogo-mezzo-item">
                        <span className="riepilogo-glyph">{GLYPH[c.mezzo.tipo] ?? '●'}</span>
                        <div className="riepilogo-mezzo-info">
                          <span className="riepilogo-codice">{c.mezzo.codice}</span>
                          <span className="riepilogo-dato">Durata: <strong>{formatTime(Math.round(durataMin * 60))}</strong></span>
                          <span className="riepilogo-dato">Km: <strong>{(r.distanza_km ?? 0).toFixed(1)}</strong></span>
                        </div>
                      </li>
                    ))}
                  </ul>

                  {/* CO2 risparmiata rispetto a mezzo a combustione (stima basata su durata) */}
                  {(() => {
                    const VEL_MEDIA_CITTA_KMH = 20
                    const CO2_COMBUSTIONE_G_KM = 120
                    const CO2_SHARING_G_KM: Record<string, number> = { bicicletta: 0, monopattino: 5, automobile: 40 }
                    const kmStimati = (durataMin / 60) * VEL_MEDIA_CITTA_KMH
                    const emissioneMedia = riepilogoData.daTerminate.length > 0
                      ? riepilogoData.daTerminate.reduce((acc, c) => acc + (CO2_SHARING_G_KM[c.mezzo.tipo] ?? 0), 0) / riepilogoData.daTerminate.length
                      : 0
                    const co2Grammi = Math.round((CO2_COMBUSTIONE_G_KM - emissioneMedia) * kmStimati)
                    return co2Grammi > 0 ? (
                      <div className="riepilogo-co2">
                        <span className="riepilogo-co2-label">CO₂ risparmiata</span>
                        <span className="riepilogo-co2-valore">
                          {co2Grammi >= 1000 ? `${(co2Grammi / 1000).toFixed(1)} kg` : `${co2Grammi} g`}
                        </span>
                      </div>
                    ) : null
                  })()}

                  {/* [IF-UT.07] mostraTotaleComplessivo(Corsa[]) */}
                  <div className="riepilogo-totale">
                    {r.importo_pieno !== null && r.costo_totale === 0 ? (
                      <>
                        <span className="riepilogo-badge riepilogo-badge--abb">Abbonamento</span>
                        <div className="riepilogo-prezzi">
                          <span className="riepilogo-gratis">Gratuita</span>
                          <span className="riepilogo-prezzo-barrato">€{r.importo_pieno!.toFixed(2)}</span>
                        </div>
                      </>
                    ) : r.importo_pieno !== null ? (
                      <>
                        <span className="riepilogo-badge riepilogo-badge--promo">Promozione</span>
                        <div className="riepilogo-prezzi">
                          <span className="riepilogo-prezzo-finale">€{(r.costo_totale ?? 0).toFixed(2)}</span>
                          <span className="riepilogo-prezzo-barrato">€{r.importo_pieno!.toFixed(2)}</span>
                        </div>
                      </>
                    ) : (
                      <div className="riepilogo-prezzi">
                        <span className="riepilogo-label-totale">Totale pagato</span>
                        <span className="riepilogo-prezzo-finale">€{(r.costo_totale ?? importoPagato ?? 0).toFixed(2)}</span>
                      </div>
                    )}
                  </div>
                </>
              )
            })()}

            <button type="button" className="btn-corsa btn-termina" onClick={handleTornaAllaMappa}>
              Torna alla mappa
            </button>
          </div>
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
          <button
            type="button"
            className={`btn-corsa ${inPausa ? 'btn-riprendi' : 'btn-pausa'}`}
            onClick={handlePausa}
            disabled={pausaLoading}
          >
            {pausaLoading ? '...' : inPausa ? 'RIPRENDI CORSA' : 'PAUSA CORSA'}
          </button>
        </div>
      )}

      {/* [IF-UT.10] msg16: mostraSospensione(tempoGratuitoResiduo, politicaAddebito) */}
      {inPausa && pausaInfo && (
        <div className={`pausa-banner ${pausaInfo.periodo_grazia_scaduto || graziaResiduaSec === 0 ? 'pausa-banner--addebito' : 'pausa-banner--gratis'}`}>
          {(pausaInfo.periodo_grazia_scaduto || graziaResiduaSec === 0) ? (
            /* A9: mostraAddebitoPausa() */
            <>
              <span className="pausa-banner-icona">⚠️</span>
              <div className="pausa-banner-testo">
                <strong>Periodo gratuito terminato</strong>
                <span>Addebito in corso: €{pausaInfo.addebito_pausa_min.toFixed(2)}/min</span>
              </div>
            </>
          ) : (
            /* Pausa gratuita: mostra countdown */
            <>
              <span className="pausa-banner-icona">⏸</span>
              <div className="pausa-banner-testo">
                <strong>Corsa in pausa</strong>
                <span>Tempo gratuito residuo: {formatTime(graziaResiduaSec ?? 0)}</span>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── Modal scegli promozione ── */}
      {schermataTermina && fase === 'scegli-promo' && (
        <div className="termina-overlay">
          <div className="termina-card">
            <p className="termina-titolo-promo">Vuoi applicare una promozione?</p>
            <ul className="promo-lista">
              {promozioniDisp.map(p => (
                <li key={p.id} className="promo-item">
                  <div className="promo-info">
                    <span className="promo-nome">{p.titolo}</span>
                    <span className="promo-sconto">-{parseFloat(p.sconto_percentuale).toFixed(0)}%</span>
                  </div>
                  <button
                    type="button"
                    className="btn-corsa btn-termina btn-applica-promo"
                    onClick={() => handlePaga(corsePerPagamento, p.id)}
                  >
                    Applica
                  </button>
                </li>
              ))}
            </ul>
            <button
              type="button"
              className="btn-corsa btn-salta-promo"
              onClick={() => handlePaga(corsePerPagamento)}
            >
              Salta, paga prezzo pieno
            </button>
          </div>
        </div>
      )}

      {/* ── Modal Termina Corsa — overlay sfocato ── */}
      {schermataTermina && fase !== 'scegli-promo' && (
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