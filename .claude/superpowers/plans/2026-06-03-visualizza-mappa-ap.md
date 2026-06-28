# IF-AP.03 – Visualizza Mappa Amministrazione Pubblica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Completare la dashboard AP con layer filtering per tipo mezzo, modalità Pin/Cluster/Heatmap, KPI bar, gauge disponibilità e popup stats per zona cliccata.

**Architecture:** Il backend (`/ap/mappa/mezzi`, `/ap/mappa/zone`) è già implementato e testato. Il lavoro è interamente frontend: nuovi componenti riutilizzabili in `frontend/src/components/`, utility `geoUtils.ts`, e riscrittura di `VistaDashboardAP.tsx`. Nessuna modifica al backend.

**Tech Stack:** React 19, TypeScript, `@vis.gl/react-google-maps` v1.8.3, `@googlemaps/markerclusterer` (nuova dipendenza), Google Maps Visualization Library (heatmap, caricata via `useMapsLibrary`).

---

## File map

| Azione | File |
|---|---|
| Crea | `frontend/src/utils/geoUtils.ts` |
| Crea | `frontend/src/components/HeatmapLayerAP.tsx` |
| Crea | `frontend/src/components/ClusterLayerAP.tsx` |
| Crea | `frontend/src/components/PopupStatsZona.tsx` |
| Modifica | `frontend/src/views/amministrazione/VistaDashboardAP.tsx` |
| Modifica | `frontend/src/views/amministrazione/VistaDashboardAP.css` |
| Modifica | `docs/Sprint1_definitivo.md` |

---

## Task 1 — Setup branch git

**Files:** nessun file modificato

- [ ] **Step 1: Checkout branch feature/mappa-zone da main aggiornato**

```bash
git checkout main
git pull origin main
git checkout feature/mappa-zone
git merge main
```

Expected: nessun conflitto. Se ci sono conflitti, risolverli prima di procedere.

- [ ] **Step 2: Installa dipendenza**

```bash
cd frontend && npm install @googlemaps/markerclusterer
```

Expected output (ultima riga): `added 1 package` o simile, senza errori.

- [ ] **Step 3: Verifica build pulita**

```bash
npm run build 2>&1 | tail -5
```

Expected: `✓ built in` senza errori TypeScript.

---

## Task 2 — Utility `geoUtils.ts`

**Files:**
- Crea: `frontend/src/utils/geoUtils.ts`

Algoritmo ray casting: un punto è dentro un poligono se un raggio orizzontale dal punto interseca un numero dispari di lati del poligono.

> ⚠️ GeoJSON usa convenzione `[lng, lat]` (longitudine prima, latitudine dopo). L'algoritmo usa `ring[i][0]` = lng e `ring[i][1]` = lat.

- [ ] **Step 1: Crea il file**

```typescript
// frontend/src/utils/geoUtils.ts
export function puntoInPoligono(
  lat: number,
  lng: number,
  perimetro: { type: 'Polygon'; coordinates: number[][][] }
): boolean {
  const ring = perimetro.coordinates[0]
  let inside = false
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0]; const yi = ring[i][1] // [lng, lat]
    const xj = ring[j][0]; const yj = ring[j][1]
    const intersect = yi > lat !== yj > lat &&
      lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi
    if (intersect) inside = !inside
  }
  return inside
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep geoUtils
```

Expected: nessun output (nessun errore).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/utils/geoUtils.ts frontend/package.json frontend/package-lock.json
git commit -m "feat(ap): utility puntoInPoligono + installa @googlemaps/markerclusterer [IF-AP.03]"
```

---

## Task 3 — `HeatmapLayerAP.tsx`

**Files:**
- Crea: `frontend/src/components/HeatmapLayerAP.tsx`

Usa `useMapsLibrary('visualization')` per caricare la libreria heatmap di Google Maps. Due `useEffect` separati: uno per creare/distruggere il layer (dipende da `map` e `visualization`), uno per aggiornare i punti (dipende da `mezzi`).

- [ ] **Step 1: Crea il componente**

```tsx
// frontend/src/components/HeatmapLayerAP.tsx
import { useEffect, useRef } from 'react'
import { useMap, useMapsLibrary } from '@vis.gl/react-google-maps'
import type { MezzoMappa } from '../services/MapService'

export default function HeatmapLayerAP({ mezzi }: { mezzi: MezzoMappa[] }) {
  const map = useMap()
  const visualization = useMapsLibrary('visualization')
  const layerRef = useRef<google.maps.visualization.HeatmapLayer | null>(null)

  useEffect(() => {
    if (!map || !visualization) return
    const layer = new google.maps.visualization.HeatmapLayer({
      data: [],
      map,
      radius: 35,
      opacity: 0.7,
    })
    layerRef.current = layer
    return () => {
      layer.setMap(null)
      layerRef.current = null
    }
  }, [map, visualization])

  useEffect(() => {
    if (!layerRef.current) return
    const points = mezzi.map(m => new google.maps.LatLng(m.lat, m.lng))
    layerRef.current.setData(points)
  }, [mezzi])

  return null
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep HeatmapLayerAP
```

Expected: nessun output.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/HeatmapLayerAP.tsx
git commit -m "feat(ap): HeatmapLayerAP con Google Maps visualization library [IF-AP.03]"
```

---

## Task 4 — `ClusterLayerAP.tsx`

**Files:**
- Crea: `frontend/src/components/ClusterLayerAP.tsx`

Usa `MarkerClusterer` da `@googlemaps/markerclusterer`. Crea marker nativi `AdvancedMarkerElement` per ogni mezzo visibile, li aggiunge al clusterer. Al cambio di `mezzi` rimuove i vecchi marker e ne crea di nuovi.

- [ ] **Step 1: Crea il componente**

```tsx
// frontend/src/components/ClusterLayerAP.tsx
import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import { MarkerClusterer } from '@googlemaps/markerclusterer'
import type { MezzoMappa } from '../services/MapService'

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta: '#2196f3',
  automobile: '#e91e8c',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

export default function ClusterLayerAP({ mezzi }: { mezzi: MezzoMappa[] }) {
  const map = useMap()
  const clustererRef = useRef<MarkerClusterer | null>(null)
  const markersRef = useRef<google.maps.marker.AdvancedMarkerElement[]>([])

  useEffect(() => {
    if (!map) return
    clustererRef.current = new MarkerClusterer({ map })
    return () => {
      clustererRef.current?.clearMarkers()
      clustererRef.current = null
    }
  }, [map])

  useEffect(() => {
    if (!clustererRef.current || !window.google) return
    clustererRef.current.clearMarkers()
    markersRef.current.forEach(m => { m.map = null })
    markersRef.current = []

    const nuoviMarker = mezzi.map(m => {
      const el = document.createElement('div')
      el.style.cssText = [
        `background:${COLORI_MEZZO[m.tipo] ?? '#888'}`,
        'border-radius:50%',
        'width:32px',
        'height:32px',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'font-size:16px',
        'box-shadow:0 2px 6px rgba(0,0,0,0.3)',
        'border:2px solid #fff',
        `opacity:${m.stato === 'Disponibile' ? 1 : 0.45}`,
      ].join(';')
      el.textContent = EMOJI_MEZZO[m.tipo] ?? '●'
      return new google.maps.marker.AdvancedMarkerElement({
        position: { lat: m.lat, lng: m.lng },
        content: el,
      })
    })
    markersRef.current = nuoviMarker
    clustererRef.current.addMarkers(nuoviMarker)
  }, [mezzi])

  return null
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep ClusterLayerAP
```

Expected: nessun output.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/ClusterLayerAP.tsx
git commit -m "feat(ap): ClusterLayerAP con MarkerClusterer [IF-AP.03]"
```

---

## Task 5 — `PopupStatsZona.tsx`

**Files:**
- Crea: `frontend/src/components/PopupStatsZona.tsx`

Usa `InfoWindow` da `@vis.gl/react-google-maps`. Posizionato al centroide della zona (media lat/lng dei vertici). Calcola mezzi interni con `puntoInPoligono`. Mostra breakdown per tipo e per stato.

- [ ] **Step 1: Crea il componente**

```tsx
// frontend/src/components/PopupStatsZona.tsx
import { InfoWindow } from '@vis.gl/react-google-maps'
import { puntoInPoligono } from '../utils/geoUtils'
import { COLORI_ZONA } from '../utils/coloriZona'
import type { ZonaMappa, MezzoMappa } from '../services/MapService'

const LABEL_TIPO: Record<string, string> = {
  operativa: 'Operativa',
  parcheggio: 'Parcheggio',
  limitata: 'Limitata',
  vietata: 'Vietata',
}
const ICONA_TIPO: Record<string, string> = {
  operativa: '◉',
  parcheggio: 'P',
  limitata: '!',
  vietata: '×',
}

function calcolaCentroide(zona: ZonaMappa): google.maps.LatLngLiteral {
  const ring = zona.perimetro.coordinates[0]
  // GeoJSON: [lng, lat]
  const lat = ring.reduce((s, c) => s + c[1], 0) / ring.length
  const lng = ring.reduce((s, c) => s + c[0], 0) / ring.length
  return { lat, lng }
}

interface Props {
  zona: ZonaMappa
  mezziVisibili: MezzoMappa[]
  onChiudi: () => void
}

export default function PopupStatsZona({ zona, mezziVisibili, onChiudi }: Props) {
  const centroide = calcolaCentroide(zona)
  const mezziInterni = mezziVisibili.filter(m =>
    puntoInPoligono(m.lat, m.lng, zona.perimetro)
  )
  const perTipo = {
    monopattino: mezziInterni.filter(m => m.tipo === 'monopattino').length,
    bicicletta: mezziInterni.filter(m => m.tipo === 'bicicletta').length,
    automobile: mezziInterni.filter(m => m.tipo === 'automobile').length,
  }
  const disponibili = mezziInterni.filter(m => m.stato === 'Disponibile').length
  const accent = COLORI_ZONA[zona.tipo]?.stroke ?? '#2196f3'

  return (
    <InfoWindow position={centroide} onCloseClick={onChiudi}>
      <div style={{ fontFamily: 'system-ui, sans-serif', minWidth: 200, color: '#0f172a', padding: '2px 4px' }}>
        {/* Header zona */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: accent, color: '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 800, fontSize: 16, flexShrink: 0,
          }}>
            {ICONA_TIPO[zona.tipo] ?? '●'}
          </div>
          <div>
            <div style={{ fontSize: 10, fontWeight: 700, color: accent, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              {LABEL_TIPO[zona.tipo]}
            </div>
            <div style={{ fontSize: 14, fontWeight: 800 }}>{zona.nome}</div>
          </div>
        </div>

        {/* Totale mezzi */}
        <div style={{ background: '#f8fafc', borderRadius: 8, padding: '7px 10px', marginBottom: 8 }}>
          <div style={{ fontSize: 11, color: '#64748b', fontWeight: 600, marginBottom: 2 }}>Mezzi nella zona</div>
          <div style={{ fontSize: 22, fontWeight: 800 }}>{mezziInterni.length}</div>
        </div>

        {/* Breakdown per tipo */}
        <div style={{ display: 'flex', gap: 5, marginBottom: 8 }}>
          {[
            { emoji: '🛴', count: perTipo.monopattino, colore: '#4caf9a' },
            { emoji: '🚲', count: perTipo.bicicletta, colore: '#2196f3' },
            { emoji: '🚗', count: perTipo.automobile, colore: '#e91e8c' },
          ].map(({ emoji, count, colore }) => (
            <div key={emoji} style={{
              flex: 1, textAlign: 'center', background: '#f8fafc',
              borderRadius: 8, padding: '5px 4px',
              borderTop: `3px solid ${colore}`,
            }}>
              <div style={{ fontSize: 15 }}>{emoji}</div>
              <div style={{ fontWeight: 800, fontSize: 13 }}>{count}</div>
            </div>
          ))}
        </div>

        {/* Stato */}
        <div style={{ fontSize: 11, color: '#64748b' }}>
          <span style={{ color: '#4caf9a', fontWeight: 700 }}>{disponibili} disponibili</span>
          {' · '}
          <span>{mezziInterni.length - disponibili} non disponibili</span>
        </div>
      </div>
    </InfoWindow>
  )
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep PopupStatsZona
```

Expected: nessun output.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/PopupStatsZona.tsx
git commit -m "feat(ap): PopupStatsZona con stats mezzi interni per zona [IF-AP.03]"
```

---

## Task 6 — Aggiorna `VistaDashboardAP.tsx`

**Files:**
- Modifica: `frontend/src/views/amministrazione/VistaDashboardAP.tsx`

Riscrittura completa del componente. Aggiunge: stato `vistaMode`/`layerAttivi`/`zonaSelezionata`, computed `mezziVisibili`/`kpi`/`percDisponibili`, componenti inline `GaugeMezzi` e `KpiCard`, integrazione dei nuovi componenti `HeatmapLayerAP`/`ClusterLayerAP`/`PopupStatsZona`, sezione filtri e toggle nel pannello.

- [ ] **Step 1: Sostituisci l'intero file**

```tsx
// frontend/src/views/amministrazione/VistaDashboardAP.tsx
// [IF-AP.03] Dashboard mappa Amministrazione Pubblica
import { useEffect, useState, useCallback, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { Map, AdvancedMarker } from '@vis.gl/react-google-maps'
import { getMezziAP, getZoneAP, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import HeatmapLayerAP from '../../components/HeatmapLayerAP'
import ClusterLayerAP from '../../components/ClusterLayerAP'
import PopupStatsZona from '../../components/PopupStatsZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import VistaReportAP from './VistaReportAP'
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta: '#2196f3',
  automobile: '#e91e8c',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

type VistaMode = 'pin' | 'cluster' | 'heatmap'

function KpiCard({ label, valore, colore }: { label: string; valore: number | string; colore: string }) {
  return (
    <div className="kpi-card">
      <span className="kpi-valore" style={{ color: colore }}>{valore}</span>
      <span className="kpi-label">{label}</span>
    </div>
  )
}

const RAGGIO = 38
const STROKE = 8
const CIRCONFERENZA = 2 * Math.PI * RAGGIO

function GaugeMezzi({ perc }: { perc: number }) {
  const offset = CIRCONFERENZA - (perc / 100) * CIRCONFERENZA
  const colore = perc >= 60 ? '#4caf9a' : perc >= 30 ? '#ff9800' : '#f44336'
  return (
    <div className="gauge-container">
      <svg width={96} height={96} viewBox="0 0 96 96">
        <circle cx={48} cy={48} r={RAGGIO} fill="none" stroke="#e8ecef" strokeWidth={STROKE} />
        <circle
          cx={48} cy={48} r={RAGGIO} fill="none"
          stroke={colore} strokeWidth={STROKE}
          strokeDasharray={CIRCONFERENZA}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          style={{ transition: 'stroke-dashoffset 0.5s ease, stroke 0.5s ease' }}
        />
        <text x={48} y={45} textAnchor="middle" fontSize={15} fontWeight={800} fill="#0f172a">{perc}%</text>
        <text x={48} y={61} textAnchor="middle" fontSize={8} fontWeight={600} fill="#94a3b8">DISPONIBILI</text>
      </svg>
    </div>
  )
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = EMOJI_MEZZO[tipo] ?? '●'
  return (
    <div style={{
      background: colore,
      opacity: stato === 'Disponibile' ? 1 : 0.45,
      borderRadius: '50%',
      width: 32, height: 32,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 16,
      boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
      border: '2px solid #fff',
    }}>
      {emoji}
    </div>
  )
}

export default function VistaDashboardAP() {
  const navigate = useNavigate()
  const [vista, setVista] = useState<'mappa' | 'report'>('mappa')
  const [vistaMode, setVistaMode] = useState<VistaMode>('pin')
  const [layerAttivi, setLayerAttivi] = useState<Set<string>>(
    new Set(['monopattino', 'bicicletta', 'automobile'])
  )
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [errore, setErrore] = useState('')

  useEffect(() => {
    Promise.all([getMezziAP(), getZoneAP()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => setErrore('Impossibile caricare i dati della mappa. Riprova.'))
  }, [])

  const mezziVisibili = useMemo(
    () => mezzi.filter(m => layerAttivi.has(m.tipo)),
    [mezzi, layerAttivi]
  )

  const kpi = useMemo(() => ({
    totale: mezzi.length,
    disponibili: mezzi.filter(m => m.stato === 'Disponibile').length,
    inUso: mezzi.filter(m => m.stato === 'In uso').length,
    manutenzione: mezzi.filter(
      m => ['In manutenzione', 'Fuori servizio', 'In pausa'].includes(m.stato)
    ).length,
  }), [mezzi])

  const percDisponibili = kpi.totale > 0
    ? Math.round((kpi.disponibili / kpi.totale) * 100)
    : 0

  const conteggiPerTipo = useMemo(() => ({
    monopattino: mezzi.filter(m => m.tipo === 'monopattino').length,
    bicicletta: mezzi.filter(m => m.tipo === 'bicicletta').length,
    automobile: mezzi.filter(m => m.tipo === 'automobile').length,
  }), [mezzi])

  const toggleLayer = useCallback((tipo: string) => {
    setLayerAttivi(prev => {
      const next = new Set(prev)
      next.has(tipo) ? next.delete(tipo) : next.add(tipo)
      return next
    })
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  if (vista === 'report') {
    return <VistaReportAP onIndietro={() => setVista('mappa')} />
  }

  const errVal = errore ? '—' : undefined

  return (
    <div className="vista-dashboard-ap">
      <div className="dashboard-ap-topbar">
        <h2>🚲 SMART MOBILITY: Amministrazione Pubblica</h2>
        <button type="button" className="btn-logout-ap" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="dashboard-ap-kpi">
        <KpiCard label="Totale" valore={errVal ?? kpi.totale} colore="#64748b" />
        <KpiCard label="Disponibili" valore={errVal ?? kpi.disponibili} colore="#4caf9a" />
        <KpiCard label="In uso" valore={errVal ?? kpi.inUso} colore="#2196f3" />
        <KpiCard label="Non disponibili" valore={errVal ?? kpi.manutenzione} colore="#ff9800" />
      </div>

      <div className="dashboard-ap-body">
        {errore && <div className="dashboard-ap-errore">{errore}</div>}

        <div className="dashboard-ap-mappa">
          <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={CENTRO_DEFAULT}
            defaultZoom={14}
            mapId="mappa-ap"
            gestureHandling="greedy"
          >
            {zone.map(z => {
              const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
              return (
                <ZonaPoligono
                  key={z.id}
                  zona={z}
                  fillColor={colori.fill}
                  strokeColor={colori.stroke}
                  onClick={zona => setZonaSelezionata(
                    prev => prev?.id === zona.id ? null : zona
                  )}
                />
              )
            })}

            {zonaSelezionata && (
              <PopupStatsZona
                zona={zonaSelezionata}
                mezziVisibili={mezziVisibili}
                onChiudi={() => setZonaSelezionata(null)}
              />
            )}

            {vistaMode === 'pin' && mezziVisibili.map(m => (
              <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
                <PinMezzo tipo={m.tipo} stato={m.stato} />
              </AdvancedMarker>
            ))}

            {vistaMode === 'heatmap' && <HeatmapLayerAP mezzi={mezziVisibili} />}
            {vistaMode === 'cluster' && <ClusterLayerAP mezzi={mezziVisibili} />}
          </Map>
        </div>

        <div className="dashboard-ap-pannello">
          <div className="logo">SMART MOBILITY</div>

          <GaugeMezzi perc={percDisponibili} />

          <div className="pannello-sezione">
            <div className="pannello-sezione-titolo">Vista mappa</div>
            <div className="vista-toggle">
              {(['pin', 'cluster', 'heatmap'] as VistaMode[]).map(mode => (
                <button
                  key={mode}
                  type="button"
                  className={`btn-vista${vistaMode === mode ? ' attivo' : ''}`}
                  onClick={() => setVistaMode(mode)}
                >
                  {mode === 'pin' ? '📍 Pin' : mode === 'cluster' ? '⬤ Cluster' : '🔥 Heatmap'}
                </button>
              ))}
            </div>
          </div>

          <div className="pannello-sezione">
            <div className="pannello-sezione-titolo">Filtra tipo mezzo</div>
            <div className="chips-tipo">
              {[
                { tipo: 'monopattino', emoji: '🛴', colore: '#4caf9a' },
                { tipo: 'bicicletta', emoji: '🚲', colore: '#2196f3' },
                { tipo: 'automobile', emoji: '🚗', colore: '#e91e8c' },
              ].map(({ tipo, emoji, colore }) => {
                const attivo = layerAttivi.has(tipo)
                return (
                  <button
                    key={tipo}
                    type="button"
                    className={`chip-tipo${attivo ? ' attivo' : ''}`}
                    style={attivo ? { background: colore, borderColor: colore } : undefined}
                    onClick={() => toggleLayer(tipo)}
                  >
                    <span className="chip-emoji">{emoji}</span>
                    <span className="chip-label">{tipo}</span>
                    <span className="chip-badge">
                      {conteggiPerTipo[tipo as keyof typeof conteggiPerTipo]}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          <button type="button" className="btn-pannello-ap" onClick={() => setVista('report')}>
            📊 VISUALIZZA REPORT
          </button>
        </div>
      </div>
    </div>
  )
}
```

> ⚠️ Nota: `setZonaSelezionata(prev => prev?.id === zona.id ? null : zona)` — cliccando la stessa zona due volte la chiude (toggle). Questo pattern richiede la form funzionale di setState.

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep -v "node_modules"
```

Expected: nessun output (nessun errore nei file del progetto).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.tsx
git commit -m "feat(ap): dashboard AP con KPI bar, gauge, layer filter, heatmap/cluster/pin [IF-AP.03]"
```

---

## Task 7 — Aggiorna `VistaDashboardAP.css`

**Files:**
- Modifica: `frontend/src/views/amministrazione/VistaDashboardAP.css`

Aggiunge stili per KPI bar, gauge, pannello sezione, toggle vista, chips tipo mezzo, banner errore. **Mantieni tutti gli stili esistenti**, aggiungi in fondo.

- [ ] **Step 1: Aggiungi in fondo al file CSS esistente**

Apri `frontend/src/views/amministrazione/VistaDashboardAP.css` e aggiungi alla fine:

```css
/* ── KPI bar ─────────────────────────────────────────────── */
.dashboard-ap-kpi {
  height: 52px;
  background: #fff;
  border-bottom: 1px solid #e8ecef;
  display: flex;
  align-items: stretch;
  flex-shrink: 0;
  z-index: 5;
}

.kpi-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e8ecef;
  padding: 0 8px;
}

.kpi-card:last-child {
  border-right: none;
}

.kpi-valore {
  font-size: 18px;
  font-weight: 800;
  line-height: 1;
}

.kpi-label {
  font-size: 10px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 2px;
}

/* ── Gauge ───────────────────────────────────────────────── */
.gauge-container {
  display: flex;
  justify-content: center;
  padding: 4px 0 8px;
}

/* ── Pannello sezioni ────────────────────────────────────── */
.pannello-sezione {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pannello-sezione-titolo {
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ── Toggle vista (Pin / Cluster / Heatmap) ──────────────── */
.vista-toggle {
  display: flex;
  border: 1.5px solid #e0e0e0;
  border-radius: 20px;
  overflow: hidden;
}

.btn-vista {
  flex: 1;
  padding: 7px 4px;
  background: transparent;
  border: none;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}

.btn-vista.attivo {
  background: #4caf9a;
  color: #fff;
}

.btn-vista:not(.attivo):hover {
  background: #f1f5f9;
}

/* ── Chips tipo mezzo ────────────────────────────────────── */
.chips-tipo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chip-tipo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  background: #f8fafc;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s, background 0.15s, border-color 0.15s, color 0.15s;
  width: 100%;
  text-align: left;
}

.chip-tipo.attivo {
  color: #fff;
}

.chip-tipo:not(.attivo) {
  opacity: 0.65;
}

.chip-emoji {
  font-size: 15px;
}

.chip-label {
  flex: 1;
  text-transform: capitalize;
}

.chip-badge {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  padding: 2px 7px;
  font-size: 11px;
  font-weight: 800;
  min-width: 22px;
  text-align: center;
}

.chip-tipo:not(.attivo) .chip-badge {
  background: #e0e0e0;
  color: #64748b;
}

/* ── Banner errore ───────────────────────────────────────── */
.dashboard-ap-errore {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  border-radius: 12px;
  padding: 10px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  color: #d32f2f;
  z-index: 20;
  white-space: nowrap;
}
```

- [ ] **Step 2: Verifica build**

```bash
cd frontend && npm run build 2>&1 | tail -5
```

Expected: `✓ built in` senza errori.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.css
git commit -m "feat(ap): stili KPI bar, gauge, toggle vista, chips tipo mezzo [IF-AP.03]"
```

---

## Task 8 — Aggiorna `Sprint1_definitivo.md`

**Files:**
- Modifica: `docs/Sprint1_definitivo.md`

Due modifiche:
1. Aggiungere `AP.03` alla tabella Sprint Backlog (riga 800, dopo `AP.01`)
2. Aggiungere tabella use case CS-04bis (IF-AP.03) prima di "Visualizza Mappa Operatore" (riga 831)

- [ ] **Step 1: Aggiungi AP.03 nel backlog (dopo la riga `| AP.01 | Sprint 1 | Accede report |`)**

Trova la riga: `| AP.01 | Sprint 1 | Accede report |`
Inserisci subito dopo:

```markdown
| AP.03 | Sprint 1 | Visualizza Mappa AP |
```

- [ ] **Step 2: Aggiungi tabella use case (prima di "Visualizza Mappa Operatore")**

Trova il testo: `Visualizza Mappa Operatore` (il titolo h3 a riga ~831).
Inserisci il blocco seguente **prima** di quel titolo:

```markdown
Visualizza Mappa Amministrazione Pubblica

|  |  |
| --- | --- |
| **Nome** | **Visualizza Mappa Amministrazione Pubblica** |
| **ID** | CS-02bis (AP.03) |
| **Breve descrizione** | Il sistema mostra all'Amministratore autenticato la mappa interattiva con tutti i mezzi della flotta, le zone attive e funzionalità analitiche avanzate (heatmap densità, clustering, KPI flotta, statistiche per zona), così da monitorare il servizio sul territorio. |
| **Attori Primari** | Amministrazione Pubblica |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L'AP è autenticata alla piattaforma con ruolo AP |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'AP accede alla schermata `/ap/dashboard`. 2. Il sistema carica mezzi e zone tramite `GET /ap/mappa/mezzi` e `GET /ap/mappa/zone`. 3. Il sistema visualizza la KPI bar (Totale / Disponibili / In uso / Non disponibili) e il gauge di disponibilità flotta. 4. Il sistema visualizza la mappa in modalità Pin con tutti i mezzi e le zone. 5. L'AP può filtrare i mezzi per tipo (monopattino / bicicletta / automobile) tramite i chip nel pannello. 6. L'AP può cambiare la modalità di visualizzazione: Pin, Cluster (raggruppamento geografico), Heatmap (densità). 7. L'AP può cliccare una zona per visualizzare il popup statistiche con numero di mezzi interni, breakdown per tipo e stato. |
| **Post-condizioni** | La mappa è visualizzata con i dati aggiornati; l'AP può monitorare distribuzione, densità e copertura della flotta sul territorio. |
| **Sequenza alternativa degli eventi** | **SA-1 (Errore GIS):** Se il backend restituisce un errore, il sistema mostra il banner "Impossibile caricare i dati della mappa. Riprova." La KPI bar mostra "—" e la gauge rimane vuota. |

```

- [ ] **Step 3: Commit**

```bash
git add docs/Sprint1_definitivo.md
git commit -m "docs: aggiunge IF-AP.03 nel backlog Sprint 1 e tabella use case CS-02bis [IF-AP.03]"
```

---

## Task 9 — Verifica finale e PR

**Files:** nessun nuovo file

- [ ] **Step 1: Build finale pulita**

```bash
cd frontend && npm run build 2>&1 | tail -8
```

Expected: `✓ built in X.Xs` senza errori TypeScript o di bundling.

- [ ] **Step 2: Test backend invariati**

```bash
cd backend && uv run pytest tests/test_ap.py -v 2>&1 | tail -12
```

Expected: `6 passed`.

- [ ] **Step 3: Push branch**

```bash
git push origin feature/mappa-zone
```

- [ ] **Step 4: Apri PR**

```bash
gh pr create \
  --title "feat(ap): IF-AP.03 Visualizza Mappa AP — heatmap, cluster, KPI, stats zona" \
  --base main \
  --body "$(cat <<'EOF'
## Summary

- Aggiunge layer filtering per tipo mezzo (🛴/🚲/🚗) con chip e badge conteggio
- Aggiunge tre modalità mappa: **Pin** (default), **Cluster** (raggruppamento geografico), **Heatmap** (densità)
- Aggiunge KPI bar con 4 counter live (Totale / Disponibili / In uso / Non disponibili)
- Aggiunge gauge SVG % disponibilità flotta nel pannello
- Aggiunge popup statistiche al click zona (mezzi interni, breakdown tipo/stato)
- Documenta IF-AP.03 in Sprint1_definitivo.md (backlog + tabella use case CS-02bis)

## Componenti nuovi
- `frontend/src/utils/geoUtils.ts` — ray casting point-in-polygon
- `frontend/src/components/HeatmapLayerAP.tsx` — Google Maps visualization
- `frontend/src/components/ClusterLayerAP.tsx` — MarkerClusterer
- `frontend/src/components/PopupStatsZona.tsx` — InfoWindow con stats

## Test plan
- [ ] Build `npm run build` senza errori
- [ ] 6/6 test backend passano (`pytest tests/test_ap.py`)
- [ ] Login AP → dashboard mostra KPI bar e gauge
- [ ] Toggle chip monopattino → i monopattini scompaiono dalla mappa
- [ ] Cambio vista Heatmap → appare gradiente densità, pin spariscono
- [ ] Cambio vista Cluster → marker raggruppati, zoom espande
- [ ] Click su zona → popup con conteggio mezzi interni
- [ ] Click stessa zona di nuovo → popup si chiude
- [ ] Errore API simulato → banner errore e KPI "—"

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: URL della PR stampato a terminale.

---

## Note implementative

- `@googlemaps/markerclusterer` richiede che `mapId` sia impostato sulla `<Map>` per `AdvancedMarkerElement` — il `mapId="mappa-ap"` è già presente nel componente.
- La libreria `visualization` (heatmap) viene caricata lazy da `useMapsLibrary`: il componente `HeatmapLayerAP` renderizza `null` finché la libreria non è disponibile, senza errori.
- Il `puntoInPoligono` usa coordinate GeoJSON `[lng, lat]`: accede a `ring[i][0]` per longitudine e `ring[i][1]` per latitudine, allineato con la struttura `ZonaMappa.perimetro.coordinates`.
- `setZonaSelezionata` usa la forma funzionale per il toggle (chiude se stessa zona viene riclickata).
