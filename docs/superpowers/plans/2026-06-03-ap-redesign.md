# AP Section Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernise the AP dashboard and report views: left icon sidebar navigation (Mappa/Report), inline KPI pills in topbar, redesigned right panel, and a proper analytics report page with 4 KPI cards + charts.

**Architecture:** Pure CSS/TSX rewrite of 2 view files. The two "pages" (Mappa and Report) stay as a `vista` state switch inside `VistaDashboardAP`. `VistaReportAP` loses its `onIndietro` prop and its own topbar — the parent handles navigation via the sidebar and export buttons via the ap-topbar. No new routes, no backend changes.

**Tech Stack:** React 19 + TypeScript, CSS class names, existing Recharts for charts.

**Spec:** `docs/superpowers/specs/2026-06-03-ap-redesign-design.md`

---

## File Structure

| File | Change |
|------|--------|
| `frontend/src/views/amministrazione/VistaDashboardAP.css` | Full rewrite — new shell, sidebar, topbar, panel classes |
| `frontend/src/views/amministrazione/VistaReportAP.css` | Full rewrite — new report layout classes |
| `frontend/src/views/amministrazione/VistaReportAP.tsx` | Rewrite — remove onIndietro, add KPI cards, fix chart widths |
| `frontend/src/views/amministrazione/VistaDashboardAP.tsx` | Full rewrite — sidebar + ap-main structure, KPI pills |

**Task order matters:** `VistaReportAP.tsx` (Task 3) must be done before `VistaDashboardAP.tsx` (Task 4), because Task 4 calls `<VistaReportAP />` with no props. If `VistaReportAP` still requires `onIndietro`, the build fails.

No other files are modified. All components (`HeatmapLayerAP`, `ClusterLayerAP`, `PopupStatsZona`, `ZonaPoligono`) are unchanged.

---

### Task 1: VistaDashboardAP.css — new shell styles

**Files:**
- Modify: `frontend/src/views/amministrazione/VistaDashboardAP.css`

- [ ] **Step 1: Replace the entire CSS file with the new stylesheet**

```css
/* ── Shell ───────────────────────────────────────────────── */
.vista-dashboard-ap {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: row;
  overflow: hidden;
}

/* ── Left sidebar ────────────────────────────────────────── */
.ap-sidebar {
  width: 52px;
  background: #ffffff;
  border-right: 1px solid #f1f5f9;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0 12px;
  gap: 8px;
  flex-shrink: 0;
  z-index: 5;
}

.ap-sidebar-logo {
  width: 28px;
  height: 28px;
  background: #4caf9a;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  margin-bottom: 4px;
  flex-shrink: 0;
}

.ap-nav-item {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1.5px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  flex-shrink: 0;
}

.ap-nav-item .ap-nav-icon {
  font-size: 14px;
  line-height: 1;
}

.ap-nav-item .ap-nav-label {
  font-size: 9px;
  font-weight: 700;
  color: #94a3b8;
  margin-top: 1px;
  line-height: 1;
}

.ap-nav-item.attivo {
  background: #ecfdf5;
  border-color: #4caf9a;
}

.ap-nav-item.attivo .ap-nav-label {
  color: #4caf9a;
}

.ap-nav-item:not(.attivo):hover {
  background: #f1f5f9;
}

.ap-nav-bottom {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
}

.ap-nav-badge {
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
}

.ap-nav-logout {
  background: transparent;
  border: none;
  font-size: 9px;
  font-weight: 600;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
}

.ap-nav-logout:hover {
  color: #4caf9a;
}

/* ── Main area ───────────────────────────────────────────── */
.ap-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── Topbar ──────────────────────────────────────────────── */
.ap-topbar {
  height: 40px;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  padding: 0 14px;
  gap: 10px;
  flex-shrink: 0;
}

.ap-topbar-title {
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
}

.ap-kpi-pills {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ap-kpi-pill {
  font-size: 11px;
  font-weight: 800;
}

.ap-kpi-pill span {
  font-size: 9px;
  font-weight: 500;
  color: #94a3b8;
  margin-left: 2px;
}

.ap-kpi-divider {
  color: #e2e8f0;
  font-size: 11px;
}

.ap-topbar-actions {
  margin-left: auto;
  display: flex;
  gap: 6px;
}

.btn-export-csv,
.btn-export-pdf {
  border: none;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 700;
  padding: 4px 12px;
  cursor: pointer;
}

.btn-export-csv {
  background: #4caf9a;
  color: #fff;
}

.btn-export-pdf {
  background: #3b82f6;
  color: #fff;
}

/* ── Body (mappa + pannello) ─────────────────────────────── */
.ap-body {
  flex: 1;
  display: flex;
  overflow: hidden;
  position: relative;
}

.ap-mappa {
  flex: 1;
  height: 100%;
}

.ap-pannello {
  width: 180px;
  background: #ffffff;
  border-left: 1px solid #f1f5f9;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  padding: 12px 10px;
  gap: 10px;
  overflow-y: auto;
  flex-shrink: 0;
}

/* ── Gauge ───────────────────────────────────────────────── */
.ap-gauge-container {
  display: flex;
  justify-content: center;
}

/* ── Panel sections ──────────────────────────────────────── */
.ap-pannello-sezione {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.ap-pannello-label {
  font-size: 9px;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ── Vista toggle ────────────────────────────────────────── */
.ap-vista-btn {
  width: 100%;
  padding: 5px 8px;
  border: none;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s, color 0.15s;
}

.ap-vista-btn.attivo {
  background: #4caf9a;
  color: #ffffff;
}

.ap-vista-btn:not(.attivo) {
  background: #f1f5f9;
  color: #64748b;
}

.ap-vista-btn:not(.attivo):hover {
  background: #e2e8f0;
}

/* ── Vehicle chips ───────────────────────────────────────── */
.ap-chip-mezzo {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 8px;
  border: 1.5px solid transparent;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s, background 0.15s, border-color 0.15s;
  width: 100%;
  text-align: left;
}

.ap-chip-mezzo:not(.attivo) {
  background: #f1f5f9;
  color: #94a3b8;
  opacity: 0.55;
}

.ap-chip-mezzo-count {
  margin-left: auto;
  font-size: 10px;
  font-weight: 800;
}

/* ── Error banner ────────────────────────────────────────── */
.ap-errore {
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

- [ ] **Step 2: Verify the build passes**

```bash
cd frontend && npm run build
```

Expected: `✓ built in Xs` — CSS-only change, build always passes if there are no pre-existing TS errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.css
git commit -m "style: rewrite VistaDashboardAP.css — B2 shell layout"
```

---

### Task 2: VistaReportAP.css — new report styles

**Files:**
- Modify: `frontend/src/views/amministrazione/VistaReportAP.css`

- [ ] **Step 1: Replace the entire CSS file**

```css
/* ── Shell ───────────────────────────────────────────────── */
.vista-report-ap {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
}

/* ── Body ────────────────────────────────────────────────── */
.report-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 14px 16px;
  overflow-y: auto;
}

/* ── KPI row ─────────────────────────────────────────────── */
.report-kpi-row {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.report-kpi-card {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.report-kpi-valore {
  font-size: 24px;
  font-weight: 900;
  line-height: 1;
  display: block;
}

.report-kpi-label {
  font-size: 9px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 4px;
  display: block;
}

/* ── Charts row ──────────────────────────────────────────── */
.report-charts-row {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.report-chart-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.report-chart-card.grande {
  flex: 2;
}

.report-chart-card.piccola {
  flex: 1;
}

.report-chart-titolo {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

/* ── Print ───────────────────────────────────────────────── */
@media print {
  .ap-sidebar,
  .ap-topbar {
    display: none !important;
  }
  .vista-report-ap {
    background: #fff;
  }
  .report-chart-card,
  .report-kpi-card {
    box-shadow: none;
    border: 1px solid #e2e8f0;
  }
}
```

- [ ] **Step 2: Verify build**

```bash
cd frontend && npm run build
```

Expected: `✓ built in Xs`.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaReportAP.css
git commit -m "style: rewrite VistaReportAP.css — KPI cards, chart layout"
```

---

### Task 3: VistaReportAP.tsx — analytics content

**Files:**
- Modify: `frontend/src/views/amministrazione/VistaReportAP.tsx`

**Context:**
- Remove `onIndietro` prop — navigation is handled by the parent's sidebar
- Remove the `report-topbar` div with back button and export buttons — the parent renders those
- Add 4 KPI summary cards computed from mock data at module level (constants, not state)
- Switch `ResponsiveContainer` from hardcoded pixel widths to `width="100%"` with `height={240}`
- `esportaCsv` moves to `VistaDashboardAP.tsx` in Task 4 — remove it here

The two module-level constants:
- `corseTotali` = sum of all entries in `DATI_SETTIMANALI` (monopattino + bicicletta + automobile per row)
- `quotaDominante` = entry in `DATI_TORTA` with the highest `value`

- [ ] **Step 1: Replace the entire TSX file**

```tsx
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts'
import { DATI_SETTIMANALI, DATI_TORTA, type DatoTorta } from './datiReportMock'
import './VistaReportAP.css'

function LabelTorta({ cx, cy, midAngle, outerRadius, name, value }: {
  cx: number; cy: number; midAngle: number; outerRadius: number; name: string; value: number
}) {
  const RAD = Math.PI / 180
  const r = outerRadius + 24
  const x = cx + r * Math.cos(-midAngle * RAD)
  const y = cy + r * Math.sin(-midAngle * RAD)
  return (
    <text x={x} y={y} textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={12} fill="#444">
      {name} {value}%
    </text>
  )
}

const corseTotali = DATI_SETTIMANALI.reduce(
  (acc, d) => acc + d.monopattino + d.bicicletta + d.automobile,
  0
)

const quotaDominante = DATI_TORTA.reduce(
  (max, d) => d.value > max.value ? d : max,
  DATI_TORTA[0]
)

export default function VistaReportAP() {
  return (
    <div className="vista-report-ap">
      <div className="report-body">

        <div className="report-kpi-row">
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#4caf9a' }}>{corseTotali}</span>
            <span className="report-kpi-label">Corse totali</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#3b82f6' }}>26.4h</span>
            <span className="report-kpi-label">Durata media</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#8b5cf6' }}>142 km</span>
            <span className="report-kpi-label">Distanza totale</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#f59e0b' }}>{quotaDominante.value}%</span>
            <span className="report-kpi-label">{quotaDominante.name}</span>
          </div>
        </div>

        <div className="report-charts-row">
          <div className="report-chart-card grande">
            <div className="report-chart-titolo">Corse settimanali per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={DATI_SETTIMANALI} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="giorno" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="monopattino" name="Monopattino" stackId="a" fill="#4caf9a" />
                <Bar dataKey="bicicletta"  name="Bicicletta"  stackId="a" fill="#2196f3" />
                <Bar dataKey="automobile"  name="Automobile"  stackId="a" fill="#e91e8c" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="report-chart-card piccola">
            <div className="report-chart-titolo">Quota per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={DATI_TORTA}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  labelLine={false}
                  label={(props) => <LabelTorta {...(props as Parameters<typeof LabelTorta>[0])} />}
                >
                  {DATI_TORTA.map((d: DatoTorta) => (
                    <Cell key={d.name} fill={d.colore} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verify the build passes**

```bash
cd frontend && npm run build
```

Expected: `✓ built in Xs`. The build will still see the old `VistaDashboardAP.tsx` calling `<VistaReportAP onIndietro={...} />` — TypeScript will error here (`onIndietro` no longer exists). This is expected; it resolves in Task 4.

If the build errors only on `VistaDashboardAP.tsx` line referencing `onIndietro`, continue to Task 4 immediately.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaReportAP.tsx
git commit -m "feat: rewrite VistaReportAP — KPI cards, responsive charts, no onIndietro"
```

---

### Task 4: VistaDashboardAP.tsx — new shell structure

**Files:**
- Modify: `frontend/src/views/amministrazione/VistaDashboardAP.tsx`

**Context:** This is the final task. It rewrites the shell component with the sidebar-nav + ap-main structure. Key differences from the current file:
- `esportaCsv` moves here from `VistaReportAP.tsx` — it uses `DATI_SETTIMANALI` (add import)
- `VistaReportAP` is called with no props: `<VistaReportAP />`
- `kpi.totale` card removed — only disponibili/inUso/manutenzione as inline pills
- `CHIP_CONFIG` constant replaces the inline array in JSX
- Old `dashboard-ap-topbar`, `dashboard-ap-kpi`, `dashboard-ap-pannello` divs are gone — replaced by `ap-sidebar`, `ap-main`, `ap-topbar`, `ap-body`, `ap-pannello`

- [ ] **Step 1: Replace the entire TSX file**

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
import { DATI_SETTIMANALI } from './datiReportMock'
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta:  '#2196f3',
  automobile:  '#e91e8c',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta:  '🚲',
  automobile:  '🚗',
}

type VistaMode = 'pin' | 'cluster' | 'heatmap'

const CHIP_CONFIG = [
  { tipo: 'monopattino', emoji: '🛴', colore: '#4caf9a', bg: '#ecfdf5' },
  { tipo: 'bicicletta',  emoji: '🚲', colore: '#3b82f6', bg: '#eff6ff' },
  { tipo: 'automobile',  emoji: '🚗', colore: '#e91e8c', bg: '#fdf2f8' },
] as const

function esportaCsv(): void {
  const intestazione = 'Giorno,Monopattino,Bicicletta,Automobile'
  const righe = DATI_SETTIMANALI.map(
    d => `${d.giorno},${d.monopattino},${d.bicicletta},${d.automobile}`
  )
  const contenuto = [intestazione, ...righe].join('\n')
  const blob = new Blob(['﻿' + contenuto], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report_smartmobility.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const RAGGIO = 38
const STROKE = 8
const CIRCONFERENZA = 2 * Math.PI * RAGGIO

function GaugeMezzi({ perc }: { perc: number }) {
  const offset = CIRCONFERENZA - (perc / 100) * CIRCONFERENZA
  const colore = perc >= 60 ? '#4caf9a' : perc >= 30 ? '#ff9800' : '#f44336'
  return (
    <div className="ap-gauge-container">
      <svg width={84} height={84} viewBox="0 0 96 96">
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
  const emoji  = EMOJI_MEZZO[tipo]  ?? '●'
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
  const [mezzi, setMezzi]   = useState<MezzoMappa[]>([])
  const [zone, setZone]     = useState<ZonaMappa[]>([])
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
    disponibili:  mezzi.filter(m => m.stato === 'Disponibile').length,
    inUso:        mezzi.filter(m => m.stato === 'In uso').length,
    manutenzione: mezzi.filter(
      m => ['In manutenzione', 'Fuori servizio', 'In pausa'].includes(m.stato)
    ).length,
  }), [mezzi])

  const percDisponibili = mezzi.length > 0
    ? Math.round((kpi.disponibili / mezzi.length) * 100)
    : 0

  const conteggiPerTipo = useMemo(() => ({
    monopattino: mezzi.filter(m => m.tipo === 'monopattino').length,
    bicicletta:  mezzi.filter(m => m.tipo === 'bicicletta').length,
    automobile:  mezzi.filter(m => m.tipo === 'automobile').length,
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

  const errVal = errore ? '—' : undefined

  return (
    <div className="vista-dashboard-ap">

      {/* ── Left sidebar ── */}
      <div className="ap-sidebar">
        <div className="ap-sidebar-logo">🚲</div>

        <div
          className={`ap-nav-item${vista === 'mappa' ? ' attivo' : ''}`}
          role="button"
          tabIndex={0}
          onClick={() => setVista('mappa')}
          onKeyDown={e => e.key === 'Enter' && setVista('mappa')}
        >
          <span className="ap-nav-icon">🗺️</span>
          <span className="ap-nav-label">Mappa</span>
        </div>

        <div
          className={`ap-nav-item${vista === 'report' ? ' attivo' : ''}`}
          role="button"
          tabIndex={0}
          onClick={() => setVista('report')}
          onKeyDown={e => e.key === 'Enter' && setVista('report')}
        >
          <span className="ap-nav-icon">📊</span>
          <span className="ap-nav-label">Report</span>
        </div>

        <div className="ap-nav-bottom">
          <span className="ap-nav-badge">AP</span>
          <button type="button" className="ap-nav-logout" onClick={handleLogout}>Esci</button>
        </div>
      </div>

      {/* ── Main area ── */}
      <div className="ap-main">

        {/* Topbar */}
        <div className="ap-topbar">
          <span className="ap-topbar-title">
            {vista === 'mappa' ? 'Dashboard Mappa' : 'Report Settimanale'}
          </span>

          {vista === 'mappa' && (
            <div className="ap-kpi-pills">
              <span className="ap-kpi-pill" style={{ color: '#4caf9a' }}>
                <strong>{errVal ?? kpi.disponibili}</strong>{' '}
                <span>disp</span>
              </span>
              <span className="ap-kpi-divider">|</span>
              <span className="ap-kpi-pill" style={{ color: '#3b82f6' }}>
                <strong>{errVal ?? kpi.inUso}</strong>{' '}
                <span>uso</span>
              </span>
              <span className="ap-kpi-divider">|</span>
              <span className="ap-kpi-pill" style={{ color: '#f59e0b' }}>
                <strong>{errVal ?? kpi.manutenzione}</strong>{' '}
                <span>man</span>
              </span>
            </div>
          )}

          {vista === 'report' && (
            <div className="ap-topbar-actions">
              <button type="button" className="btn-export-csv" onClick={esportaCsv}>CSV</button>
              <button type="button" className="btn-export-pdf" onClick={() => window.print()}>PDF</button>
            </div>
          )}
        </div>

        {/* Content: Mappa or Report */}
        {vista === 'mappa' ? (
          <div className="ap-body">
            {errore && <div className="ap-errore">{errore}</div>}

            <div className="ap-mappa">
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

            <div className="ap-pannello">
              <GaugeMezzi perc={percDisponibili} />

              <div className="ap-pannello-sezione">
                <div className="ap-pannello-label">Vista</div>
                {(['pin', 'cluster', 'heatmap'] as VistaMode[]).map(mode => (
                  <button
                    key={mode}
                    type="button"
                    className={`ap-vista-btn${vistaMode === mode ? ' attivo' : ''}`}
                    onClick={() => setVistaMode(mode)}
                  >
                    {mode === 'pin' ? '📍 Pin' : mode === 'cluster' ? '⬤ Cluster' : '🔥 Heatmap'}
                  </button>
                ))}
              </div>

              <div className="ap-pannello-sezione">
                <div className="ap-pannello-label">Mezzi</div>
                {CHIP_CONFIG.map(({ tipo, emoji, colore, bg }) => {
                  const attivo = layerAttivi.has(tipo)
                  return (
                    <button
                      key={tipo}
                      type="button"
                      className={`ap-chip-mezzo${attivo ? ' attivo' : ''}`}
                      style={attivo ? { background: bg, borderColor: colore, color: colore } : undefined}
                      onClick={() => toggleLayer(tipo)}
                    >
                      <span>{emoji}</span>
                      <span style={{ flex: 1, textTransform: 'capitalize' }}>{tipo}</span>
                      <span className="ap-chip-mezzo-count">
                        {conteggiPerTipo[tipo as keyof typeof conteggiPerTipo]}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        ) : (
          <VistaReportAP />
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verify the build passes**

```bash
cd frontend && npm run build
```

Expected: `✓ built in Xs` with zero TypeScript errors. Both `VistaDashboardAP.tsx` and `VistaReportAP.tsx` are now consistent (no `onIndietro` prop anywhere).

- [ ] **Step 3: Run backend unit tests**

```bash
cd backend && uv run pytest tests/ -v -m "not integration"
```

Expected: all tests pass (frontend-only change; sanity check).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.tsx
git commit -m "feat: rewrite VistaDashboardAP — sidebar nav, KPI pills, B2 layout"
```

---

## Visual Verification Checklist

After all 4 tasks, start the dev server:

```bash
cd frontend && npm run dev
```

Open `http://localhost:5173`, log in as AP role.

**Dashboard Mappa:**
- [ ] Left sidebar: logo 🚲, Mappa tile active (teal border + bg), Report tile inactive, "AP" badge, "Esci" button
- [ ] Topbar: "Dashboard Mappa" on left + KPI pills (disp/uso/man coloured values) on right
- [ ] Map fills area with zone polygons and vehicle markers
- [ ] Right panel: gauge showing %, Vista buttons stacked (Pin active green), chip filters with counts
- [ ] Clicking Cluster → cluster view; Heatmap → heat overlay
- [ ] Clicking a chip → vehicle type disappears from map (chip fades)
- [ ] Clicking a zone polygon → popup stats appear

**Dashboard Report (click 📊 in sidebar):**
- [ ] Report tile becomes active (teal border); Mappa tile becomes inactive
- [ ] Topbar: "Report Settimanale" + CSV (green) and PDF (blue) buttons on right
- [ ] 4 KPI cards with large coloured numbers (corse/durata/distanza/quota)
- [ ] Bar chart and pie chart rendered below, filling card width
- [ ] CSV button downloads `report_smartmobility.csv`
- [ ] PDF button opens browser print dialog
