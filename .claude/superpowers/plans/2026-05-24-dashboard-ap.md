# Dashboard Amministrazione Pubblica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare la dashboard AP con mappa read-only (IF-AP.03) e schermata report con grafici mock (IF-AP.01).

**Architecture:** Backend — nuovo `ap_controller.py` con 2 endpoint GET (ruolo AP) che delegano a `ServizioGIS` già esistente. Frontend — `VistaDashboardAP` (split 70/30, mappa + pulsante report) e `VistaReportAP` (schermata intera con Recharts), navigati tramite stato interno `vista`. `APIProvider` è già al top-level in `App.tsx`, non va duplicato.

**Tech Stack:** FastAPI + PyJWT (backend), React 19 + Recharts + @vis.gl/react-google-maps (frontend)

---

## File Map

| File | Azione | Responsabilità |
|---|---|---|
| `backend/controllers/ap_controller.py` | Crea | Endpoint GET /ap/mappa/mezzi e /ap/mappa/zone |
| `backend/main.py` | Modifica | Registra ap_router |
| `backend/tests/test_ap.py` | Crea | Test autenticazione endpoint AP |
| `frontend/src/services/MapService.ts` | Modifica | Aggiunge getMezziAP, getZoneAP |
| `frontend/src/views/amministrazione/datiReportMock.ts` | Crea | Dati mock per grafici |
| `frontend/src/views/amministrazione/VistaReportAP.tsx` | Crea | Schermata report con grafici Recharts |
| `frontend/src/views/amministrazione/VistaReportAP.css` | Crea | Stili report |
| `frontend/src/views/amministrazione/VistaDashboardAP.tsx` | Crea | Mappa read-only + navigazione a report |
| `frontend/src/views/amministrazione/VistaDashboardAP.css` | Crea | Stili dashboard AP |
| `frontend/src/App.tsx` | Modifica | Collega /ap/dashboard a VistaDashboardAP |

---

## Task 1: Backend — ap_controller + test

**Files:**
- Create: `backend/controllers/ap_controller.py`
- Modify: `backend/main.py`
- Create: `backend/tests/test_ap.py`

- [ ] **Step 1: Scrivi i test fallenti**

Crea `backend/tests/test_ap.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def test_ap_mappa_mezzi_autenticato(ap_test):
    """[IF-AP.03] AP autenticata riceve lista mezzi."""
    token = _login(ap_test["email"], ap_test["password"])
    resp = http.get(
        "/ap/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_ap_mappa_mezzi_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/ap/mappa/mezzi")
    assert resp.status_code == 401


def test_ap_mappa_mezzi_ruolo_errato(utente_test):
    """[IIN-2] Token UT su endpoint AP → 403."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.get(
        "/ap/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_ap_mappa_zone_autenticato(ap_test):
    """[IF-AP.03] AP autenticata riceve lista zone."""
    token = _login(ap_test["email"], ap_test["password"])
    resp = http.get(
        "/ap/mappa/zone",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
```

- [ ] **Step 2: Verifica che i test falliscano**

```bash
cd backend && uv run pytest tests/test_ap.py -v -m "not integration"
```

Atteso: 4 errori `404 Not Found` (gli endpoint non esistono ancora).

- [ ] **Step 3: Crea ap_controller.py**

Crea `backend/controllers/ap_controller.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut, ZonaOut

router = APIRouter(prefix="/ap", tags=["Mappa AP"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Tutti i mezzi con posizione per la Mappa AP."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


@router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Zone attive per la Mappa AP."""
    return ServizioGIS(db).ottieni_zone()
```

- [ ] **Step 4: Registra il router in main.py**

In `backend/main.py`, aggiungi l'import e `include_router`:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as auth_router, mappa_router
from controllers.mezzo_operatore_controller import router as mezzo_op_router
from controllers.zona_operatore_controller import router as zona_op_router
from controllers.ap_controller import router as ap_router

app = FastAPI(title="SmartMobility API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(auth_router)
app.include_router(mappa_router)
app.include_router(mezzo_op_router)
app.include_router(zona_op_router)
app.include_router(ap_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
```

- [ ] **Step 5: Verifica che i test passino**

```bash
cd backend && uv run pytest tests/test_ap.py -v -m "not integration"
```

Atteso: 4 PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/controllers/ap_controller.py backend/main.py backend/tests/test_ap.py
git commit -m "feat(ap): endpoint GET /ap/mappa/mezzi e /ap/mappa/zone [IF-AP.03]"
```

---

## Task 2: Frontend — installa Recharts

**Files:**
- Modify: `frontend/package.json` (automatico via npm)

- [ ] **Step 1: Installa Recharts**

```bash
cd frontend && npm install recharts
```

Atteso: `recharts` aggiunto in `dependencies` di `package.json`.

- [ ] **Step 2: Verifica che TypeScript trovi i tipi**

Recharts include i tipi nativamente — nessun `@types/recharts` necessario.

```bash
cd frontend && npm run build 2>&1 | head -5
```

Atteso: nessun errore relativo a recharts (possono esserci altri warning pre-esistenti).

- [ ] **Step 3: Commit**

```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "chore: installa recharts per grafici dashboard AP"
```

---

## Task 3: Frontend — MapService.ts (getMezziAP, getZoneAP)

**Files:**
- Modify: `frontend/src/services/MapService.ts`

- [ ] **Step 1: Aggiungi le due funzioni in fondo a MapService.ts**

Il file attuale termina a riga 43. Aggiungi dopo `getZoneOperatore`:

```typescript
export const getMezziAP = async (): Promise<MezzoMappa[]> => {
  const r = await api.get<MezzoMappa[]>('/ap/mappa/mezzi')
  return r.data
}

export const getZoneAP = async (): Promise<ZonaMappa[]> => {
  const r = await api.get<ZonaMappa[]>('/ap/mappa/zone')
  return r.data
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npm run build 2>&1 | grep -i "mapservice"
```

Atteso: nessun errore su MapService.ts.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/MapService.ts
git commit -m "feat(ap): getMezziAP e getZoneAP in MapService [IF-AP.03]"
```

---

## Task 4: Frontend — datiReportMock.ts

**Files:**
- Create: `frontend/src/views/amministrazione/datiReportMock.ts`

- [ ] **Step 1: Crea il file mock**

Crea `frontend/src/views/amministrazione/datiReportMock.ts`:

```typescript
export interface DatoSettimanale {
  giorno: string
  monopattino: number
  bicicletta: number
  automobile: number
}

export interface DatoTorta {
  name: string
  value: number
  colore: string
}

export const DATI_SETTIMANALI: DatoSettimanale[] = [
  { giorno: 'Lun', monopattino: 42, bicicletta: 18, automobile: 12 },
  { giorno: 'Mar', monopattino: 38, bicicletta: 22, automobile: 10 },
  { giorno: 'Mer', monopattino: 35, bicicletta: 20, automobile: 14 },
  { giorno: 'Gio', monopattino: 28, bicicletta: 15, automobile: 8  },
  { giorno: 'Ven', monopattino: 20, bicicletta: 12, automobile: 6  },
  { giorno: 'Sab', monopattino: 15, bicicletta: 10, automobile: 5  },
  { giorno: 'Dom', monopattino: 10, bicicletta: 8,  automobile: 4  },
]

export const DATI_TORTA: DatoTorta[] = [
  { name: 'Monopattino', value: 70.9, colore: '#4caf9a' },
  { name: 'Bicicletta',  value: 13.3, colore: '#2196f3' },
  { name: 'Automobile',  value: 15.8, colore: '#e91e8c' },
]
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/amministrazione/datiReportMock.ts
git commit -m "feat(ap): dati mock report [IF-AP.01]"
```

---

## Task 5: Frontend — VistaReportAP

**Files:**
- Create: `frontend/src/views/amministrazione/VistaReportAP.tsx`
- Create: `frontend/src/views/amministrazione/VistaReportAP.css`

- [ ] **Step 1: Crea VistaReportAP.css**

Crea `frontend/src/views/amministrazione/VistaReportAP.css`:

```css
.vista-report-ap {
  width: 100%;
  min-height: 100vh;
  background: #f5f6fa;
  display: flex;
  flex-direction: column;
}

.report-topbar {
  height: 56px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  flex-shrink: 0;
  gap: 16px;
}

.report-topbar h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #222;
  flex: 1;
}

.btn-indietro {
  padding: 6px 18px;
  background: transparent;
  color: #4caf9a;
  border: 2px solid #4caf9a;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.report-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 24px;
  gap: 32px;
}

.report-grafici {
  display: flex;
  gap: 32px;
  width: 100%;
  max-width: 960px;
  justify-content: center;
  flex-wrap: wrap;
}

.report-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.report-card h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.report-azioni {
  display: flex;
  gap: 16px;
}

.btn-export {
  padding: 12px 28px;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.5px;
}

.btn-export.csv {
  background: #4caf9a;
  color: #fff;
}

.btn-export.pdf {
  background: #2196f3;
  color: #fff;
}

@media print {
  .report-topbar,
  .report-azioni {
    display: none;
  }
  .vista-report-ap {
    background: #fff;
  }
}
```

- [ ] **Step 2: Crea VistaReportAP.tsx**

Crea `frontend/src/views/amministrazione/VistaReportAP.tsx`:

```tsx
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts'
import { DATI_SETTIMANALI, DATI_TORTA, type DatoSettimanale, type DatoTorta } from './datiReportMock'
import './VistaReportAP.css'

interface VistaReportAPProps {
  onIndietro: () => void
}

function esportaCsv(dati: DatoSettimanale[]): void {
  const intestazione = 'Giorno,Monopattino,Bicicletta,Automobile'
  const righe = dati.map(d => `${d.giorno},${d.monopattino},${d.bicicletta},${d.automobile}`)
  const contenuto = [intestazione, ...righe].join('\n')
  const blob = new Blob([contenuto], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report_smartmobility.csv'
  a.click()
  URL.revokeObjectURL(url)
}

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

export default function VistaReportAP({ onIndietro }: VistaReportAPProps) {
  return (
    <div className="vista-report-ap">
      <div className="report-topbar">
        <button className="btn-indietro" onClick={onIndietro}>← Indietro</button>
        <h2>REPORT</h2>
      </div>

      <div className="report-body">
        <div className="report-grafici">
          <div className="report-card">
            <h3>Corse settimanali per tipologia</h3>
            <ResponsiveContainer width={480} height={260}>
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

          <div className="report-card">
            <h3>Quota per tipologia</h3>
            <ResponsiveContainer width={340} height={260}>
              <PieChart>
                <Pie
                  data={DATI_TORTA}
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  dataKey="value"
                  labelLine={false}
                  label={(props) => <LabelTorta {...props} />}
                >
                  {DATI_TORTA.map((d: DatoTorta) => (
                    <Cell key={d.name} fill={d.colore} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="report-azioni">
          <button className="btn-export csv" onClick={() => esportaCsv(DATI_SETTIMANALI)}>
            ESPORTA CSV
          </button>
          <button className="btn-export pdf" onClick={() => window.print()}>
            ESPORTA PDF
          </button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaReportAP.tsx frontend/src/views/amministrazione/VistaReportAP.css
git commit -m "feat(ap): VistaReportAP con grafici Recharts e export [IF-AP.01]"
```

---

## Task 6: Frontend — VistaDashboardAP

**Files:**
- Create: `frontend/src/views/amministrazione/VistaDashboardAP.tsx`
- Create: `frontend/src/views/amministrazione/VistaDashboardAP.css`

- [ ] **Step 1: Crea VistaDashboardAP.css**

Crea `frontend/src/views/amministrazione/VistaDashboardAP.css`:

```css
.vista-dashboard-ap {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-ap-topbar {
  height: 56px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 10;
  gap: 12px;
  flex-shrink: 0;
}

.dashboard-ap-topbar h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #222;
  flex: 1;
}

.dashboard-ap-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.dashboard-ap-mappa {
  flex: 70%;
  height: 100%;
}

.dashboard-ap-pannello {
  flex: 30%;
  background: #f9f9f9;
  border-left: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  gap: 10px;
  overflow-y: auto;
}

.dashboard-ap-pannello .logo {
  font-size: 13px;
  font-weight: 700;
  color: #4caf9a;
  text-align: center;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.btn-pannello-ap {
  width: 100%;
  padding: 12px 16px;
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 24px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: background 0.2s;
  text-align: center;
}

.btn-pannello-ap:hover {
  background: #3d9e8a;
}

.btn-logout-ap {
  padding: 6px 16px;
  background: transparent;
  color: #4caf9a;
  border: 2px solid #4caf9a;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}
```

- [ ] **Step 2: Crea VistaDashboardAP.tsx**

Crea `frontend/src/views/amministrazione/VistaDashboardAP.tsx`:

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Map, AdvancedMarker } from '@vis.gl/react-google-maps'
import { getMezziAP, getZoneAP, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import TooltipZona from '../../components/TooltipZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import VistaReportAP from './VistaReportAP'
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta:  '#2196f3',
  automobile:  '#e91e8c',
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = tipo === 'monopattino' ? '🛴' : tipo === 'bicicletta' ? '🚲' : '🚗'
  const opacita = stato === 'Disponibile' ? 1 : 0.45
  return (
    <div style={{
      background: colore,
      opacity: opacita,
      borderRadius: '50%',
      width: 32,
      height: 32,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
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
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [tooltipZona, setTooltipZona] = useState<{ zona: ZonaMappa; pos: google.maps.LatLngLiteral } | null>(null)

  useEffect(() => {
    Promise.all([getMezziAP(), getZoneAP()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => {})
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  if (vista === 'report') {
    return <VistaReportAP onIndietro={() => setVista('mappa')} />
  }

  return (
    <div className="vista-dashboard-ap">
      <div className="dashboard-ap-topbar">
        <h2>🚲 SMART MOBILITY — Amministrazione Pubblica</h2>
        <button className="btn-logout-ap" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="dashboard-ap-body">
        <div className="dashboard-ap-mappa">
          <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={CENTRO_DEFAULT}
            defaultZoom={14}
            mapId="mappa-ap"
            gestureHandling="greedy"
          >
            {mezzi.map(m => (
              <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
                <PinMezzo tipo={m.tipo} stato={m.stato} />
              </AdvancedMarker>
            ))}

            {zone.map(z => {
              const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
              return (
                <ZonaPoligono
                  key={z.id}
                  zona={z}
                  fillColor={colori.fill}
                  strokeColor={colori.stroke}
                  onHover={(zona, pos) => setTooltipZona({ zona, pos })}
                  onHoverEnd={() => setTooltipZona(null)}
                />
              )
            })}

            {tooltipZona && (
              <TooltipZona zona={tooltipZona.zona} posizione={tooltipZona.pos} />
            )}
          </Map>
        </div>

        <div className="dashboard-ap-pannello">
          <div className="logo">SMART MOBILITY</div>
          <button className="btn-pannello-ap" onClick={() => setVista('report')}>
            📊 VISUALIZZA REPORT
          </button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.tsx frontend/src/views/amministrazione/VistaDashboardAP.css
git commit -m "feat(ap): VistaDashboardAP mappa read-only + navigazione report [IF-AP.03]"
```

---

## Task 7: Frontend — collega App.tsx

**Files:**
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Aggiorna App.tsx**

Sostituisci l'intero contenuto di `frontend/src/App.tsx`:

```tsx
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import VistaLogin from './views/auth/VistaLogin'
import CallbackOAuth from './views/auth/CallbackOAuth'
import RoutaProtetta from './components/RoutaProtetta'
import VistaMappa from './views/utente/VistaMappa'
import VistaMappaOperatore from './views/operatore/VistaMappaOperatore'
import VistaDashboardAP from './views/amministrazione/VistaDashboardAP'
import { utenteCorrente, logout } from './services/AuthService'

function PlaceholderView({ titolo }: { titolo: string }) {
  const navigate = useNavigate()
  const utente = utenteCorrente()
  const handleLogout = async () => {
    await logout()
    navigate('/', { replace: true })
  }
  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>{titolo}</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {utente && <span style={{ fontSize: 14, color: '#555' }}>{utente.profilo.email}</span>}
          <button
            onClick={handleLogout}
            style={{
              padding: '8px 20px',
              background: 'transparent',
              color: '#4caf9a',
              border: '2px solid #4caf9a',
              borderRadius: 24,
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            LOGOUT
          </button>
        </div>
      </div>
    </div>
  )
}

function App() {
  const utente = utenteCorrente()

  const homePerRuolo =
    utente?.ruolo === 'UT' ? '/utente/home' :
    utente?.ruolo === 'OP' ? '/operatore/dashboard' :
    utente?.ruolo === 'AP' ? '/ap/dashboard' : '/'

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={utente ? <Navigate to={homePerRuolo} replace /> : <VistaLogin />}
        />
        <Route
          path="/utente/home"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaMappa />
            </RoutaProtetta>
          }
        />
        <Route
          path="/utente/*"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <PlaceholderView titolo="Utente" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/dashboard"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaMappaOperatore />
            </RoutaProtetta>
          }
        />
        <Route
          path="/operatore/*"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <PlaceholderView titolo="Operatore" />
            </RoutaProtetta>
          }
        />
        <Route
          path="/ap/dashboard"
          element={
            <RoutaProtetta ruoloRichiesto="AP">
              <VistaDashboardAP />
            </RoutaProtetta>
          }
        />
        <Route
          path="/ap/*"
          element={
            <RoutaProtetta ruoloRichiesto="AP">
              <PlaceholderView titolo="Dashboard AP" />
            </RoutaProtetta>
          }
        />
        <Route path="/auth/callback" element={<CallbackOAuth />} />
        <Route path="/non-autorizzato" element={<PlaceholderView titolo="Accesso non autorizzato" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

Nota: `APIProvider` rimosso da `App.tsx` — era già lì nel branch corrente ma va spostato dentro `VistaMappa` e `VistaMappaOperatore` (che già lo gestiscono internamente), oppure mantenuto se le viste lo usano. Verifica: se `VistaMappa` e `VistaMappaOperatore` wrappano già il loro `Map` con un proprio `APIProvider`, rimuovilo da App.tsx. Se invece lo usano dal contesto globale, mantienilo.

**Azione concreta:** Apri `frontend/src/views/utente/VistaMappa.tsx` e `frontend/src/views/operatore/VistaMappaOperatore.tsx`. Se nessuno dei due ha `<APIProvider>` al loro interno, aggiungi `APIProvider` intorno a `BrowserRouter` in `App.tsx`:

```tsx
import { APIProvider } from '@vis.gl/react-google-maps'
const MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string

// Wrappa BrowserRouter:
return (
  <APIProvider apiKey={MAPS_API_KEY} version="quarterly" libraries={['drawing']}>
    <BrowserRouter>
      ...
    </BrowserRouter>
  </APIProvider>
)
```

- [ ] **Step 2: Avvia frontend e verifica**

```bash
cd frontend && npm run dev
```

Verifica:
- Login come AP (`ap_test@example.com` / `TestPass123!`) → si apre `VistaDashboardAP` con mappa e pannello destro con "VISUALIZZA REPORT"
- Click "VISUALIZZA REPORT" → si apre `VistaReportAP` con istogramma + torta
- Click "← Indietro" → si torna alla mappa
- Click "ESPORTA CSV" → scarica `report_smartmobility.csv`
- Click "ESPORTA PDF" → apre la finestra di stampa del browser

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "feat(ap): collega VistaDashboardAP al routing /ap/dashboard [IF-AP.03/IF-AP.01]"
```

---

## Self-Review

**Spec coverage:**
- ✅ IF-AP.03 (Visualizza Mappa AP) — VistaDashboardAP con Map, pin mezzi, ZonaPoligono
- ✅ IF-AP.01 (Accede Report) — VistaReportAP con BarChart + PieChart + export CSV/PDF
- ✅ IIN-2 (Sicurezza) — endpoint AP verificano ruolo AP; UT → 403, no token → 401
- ✅ Dati mock in file separato sostituibile in futuro senza toccare i componenti grafici

**Placeholder scan:** nessun TBD, ogni step ha codice completo.

**Type consistency:**
- `getMezziAP` → `MezzoMappa[]` (Task 3) → usato in `VistaDashboardAP` (Task 6) ✓
- `getZoneAP` → `ZonaMappa[]` (Task 3) → usato in `VistaDashboardAP` (Task 6) ✓
- `onIndietro: () => void` definito in `VistaReportAP` props (Task 5) → chiamato in `VistaDashboardAP` (Task 6) ✓
- `DATI_SETTIMANALI: DatoSettimanale[]` e `DATI_TORTA: DatoTorta[]` definiti in Task 4, importati in Task 5 ✓
- `esportaCsv(dati: DatoSettimanale[])` riceve `DATI_SETTIMANALI` ✓
