# Demo movimento mezzi — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Durante una corsa di gruppo dell'account demo, un pulsante avvia il movimento simulato dei mezzi in convoglio lungo un percorso che attraversa zona limitata, vietata e uscita dall'operativa, visibile in tempo reale su mappa Operatore e info corsa Utente.

**Architecture:** Il backend espone solo l'aggiornamento posizione del mezzo (`ServizioMappa.aggiorna_posizione_mezzo` → `MezzoRepository.aggiorna_posizione` → DB). Il geofencing è calcolato lato client (`geoUtils.zonaCorrente`). Il frontend dell'account demo pilota il convoglio con un `setInterval` che, per ogni mezzo, avanza lungo una polilinea condivisa e chiama l'endpoint posizione; la mappa Operatore fa polling e mostra i mezzi muoversi.

**Tech Stack:** FastAPI + SQLAlchemy (PostGIS via SQL grezzo), React 19 + TypeScript + Vite, axios.

## Global Constraints

- Layer separation: Controller solo validazione/smistamento; logica in BLL (`ServizioMappa`); DB solo nel DAL. La posizione NON è uno stato del mezzo: non passa per `ServizioMobilità`.
- Gating: solo l'account con email == `DEMO_ACCOUNT_EMAIL` (backend) / `VITE_DEMO_EMAIL` (frontend) = `demo@smartmobility.it`.
- Nessuna nuova classe/entità. Unica aggiunta di dominio: `aggiornaPosizioneMezzo(idMezzo, lat, lng)` su `IServizioMappa`/`ServizioMappa`, da riflettere nel Diagramma Classi.
- Nessuna notifica frontend, nessuna persistenza `Notifica`. Solo un piccolo banner in info corsa.
- Glossario/precedenza zone: `vietata > limitata > operativa` (`docs/Sprintn3.md §4.2`).
- Test backend: integration (Supabase+DB reali), marcati `@pytest.mark.integration`, server su `http://localhost:8000`. Frontend: nessun test runner → verifica con `npx tsc -b` + controllo manuale.
- Tracciabilità: `IF-OP.01`, `IF-UT.01`, `IF-UT.08`. Endpoint demo marcato come helper di presentazione.

---

### Task 1: DAL — `MezzoRepository.aggiorna_posizione`

**Files:**
- Modify: `backend/dal/mezzo_repository.py` (aggiungere metodo dopo `aggiorna_stato`, ~riga 141)
- Test: `backend/tests/test_aggiorna_posizione.py` (create)

**Interfaces:**
- Produces: `MezzoRepository.aggiorna_posizione(mezzo_id: UUID, lat: float, lng: float) -> None`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_aggiorna_posizione.py
import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository


@pytest.mark.integration
def test_aggiorna_posizione_aggiorna_lat_lng(db):
    codice = f"POS-{_uuid.uuid4().hex[:6]}"
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:c, 'monopattino', 'Disponibile', 41.1100, 16.8680)
        """), {"c": codice})
        s.commit()
        mezzo_id = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).scalar()
    try:
        MezzoRepository(db).aggiorna_posizione(mezzo_id, 41.1093, 16.8791)
        m = MezzoRepository(db).trova_per_id(mezzo_id)
        assert round(m["lat"], 4) == 41.1093
        assert round(m["lng"], 4) == 16.8791
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = :c"), {"c": codice})
            s.commit()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && uv run pytest tests/test_aggiorna_posizione.py -v -m integration`
Expected: FAIL con `AttributeError: 'MezzoRepository' object has no attribute 'aggiorna_posizione'`

- [ ] **Step 3: Write minimal implementation**

In `backend/dal/mezzo_repository.py`, subito dopo il metodo `aggiorna_stato`:

```python
    def aggiorna_posizione(self, mezzo_id: UUID, lat: float, lng: float) -> None:
        sql = text("UPDATE mezzi SET lat = :lat, lng = :lng WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"lat": lat, "lng": lng, "id": str(mezzo_id)})
            s.commit()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && uv run pytest tests/test_aggiorna_posizione.py -v -m integration`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/dal/mezzo_repository.py backend/tests/test_aggiorna_posizione.py
git commit -m "feat(dal): MezzoRepository.aggiorna_posizione per movimento demo"
```

---

### Task 2: BLL — `ServizioMappa.aggiorna_posizione_mezzo`

**Files:**
- Modify: `backend/bll/servizio_mappa.py` (aggiungere metodo in fondo alla classe)
- Test: `backend/tests/test_aggiorna_posizione.py` (aggiungere test)

**Interfaces:**
- Consumes: `MezzoRepository.aggiorna_posizione` (Task 1)
- Produces: `ServizioMappa.aggiorna_posizione_mezzo(id_mezzo: UUID, lat: float, lng: float) -> None`

- [ ] **Step 1: Write the failing test** (aggiungi in coda a `test_aggiorna_posizione.py`)

```python
@pytest.mark.integration
def test_servizio_mappa_aggiorna_posizione_mezzo(db):
    import uuid as _uuid
    from bll.servizio_mappa import ServizioMappa
    codice = f"POS2-{_uuid.uuid4().hex[:6]}"
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:c, 'bicicletta', 'In uso', 41.1100, 16.8680)
        """), {"c": codice})
        s.commit()
        mezzo_id = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).scalar()
    try:
        ServizioMappa(db).aggiorna_posizione_mezzo(mezzo_id, 41.1095, 16.8806)
        m = MezzoRepository(db).trova_per_id(mezzo_id)
        assert round(m["lat"], 4) == 41.1095
        assert round(m["lng"], 4) == 16.8806
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = :c"), {"c": codice})
            s.commit()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && uv run pytest tests/test_aggiorna_posizione.py::test_servizio_mappa_aggiorna_posizione_mezzo -v -m integration`
Expected: FAIL con `AttributeError: ... has no attribute 'aggiorna_posizione_mezzo'`

- [ ] **Step 3: Write minimal implementation**

In `backend/bll/servizio_mappa.py`, in coda alla classe `ServizioMappa`:

```python
    # [IF-OP.01] Helper demo di presentazione: aggiorna la posizione di un mezzo.
    # La posizione non è uno stato del mezzo: resta in ServizioMappa (servizio geografico).
    def aggiorna_posizione_mezzo(self, id_mezzo: UUID, lat: float, lng: float) -> None:
        self._mezzo_repo.aggiorna_posizione(id_mezzo, lat, lng)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && uv run pytest tests/test_aggiorna_posizione.py -v -m integration`
Expected: PASS (entrambi i test)

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_mappa.py backend/tests/test_aggiorna_posizione.py
git commit -m "feat(bll): ServizioMappa.aggiorna_posizione_mezzo"
```

---

### Task 3: Controller + config — `PATCH /utente/corse/{corsa_id}/demo/posizione`

**Files:**
- Modify: `backend/config.py` (aggiungere `DEMO_ACCOUNT_EMAIL`)
- Modify: `backend/.env.example` (documentare `DEMO_ACCOUNT_EMAIL`)
- Modify: `backend/controllers/schemas.py` (aggiungere `PosizioneDemoRequest`)
- Modify: `backend/controllers/corsa_controller.py` (import + endpoint)
- Test: `backend/tests/test_demo_posizione_http.py` (create)

**Interfaces:**
- Consumes: `ServizioMappa.aggiorna_posizione_mezzo` (Task 2), `CorsaRepository.trova_per_id`, `verify_token(["UT"])` → `{id, ruolo, email}`
- Produces: `PATCH /utente/corse/{corsa_id}/demo/posizione` body `{lat: float, lng: float}` → `204`; `403` se non account demo o corsa non propria.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_demo_posizione_http.py
import pytest
import httpx

BASE = "http://localhost:8000"


def _login(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.mark.integration
def test_posizione_demo_403_se_non_account_demo(db, utente_test):
    # utente_test ha email ut_test@example.com != DEMO_ACCOUNT_EMAIL
    token = _login(utente_test["email"], utente_test["password"])
    import uuid as _uuid
    corsa_fittizia = str(_uuid.uuid4())
    r = httpx.patch(
        f"{BASE}/utente/corse/{corsa_fittizia}/demo/posizione",
        json={"lat": 41.1093, "lng": 16.8791},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403, r.text
```

- [ ] **Step 2: Run test to verify it fails**

Assicurarsi che il server giri (`cd backend && uv run uvicorn main:app --reload`).
Run: `cd backend && uv run pytest tests/test_demo_posizione_http.py -v -m integration`
Expected: FAIL con `404` (route inesistente) invece di `403`.

- [ ] **Step 3a: Aggiungi config**

In `backend/config.py`, dopo `DATABASE_URL`:

```python
DEMO_ACCOUNT_EMAIL: str = os.getenv("DEMO_ACCOUNT_EMAIL", "")
```

In `backend/.env.example`, aggiungi una riga:

```
DEMO_ACCOUNT_EMAIL=demo@smartmobility.it
```

In `backend/.env` (locale, non committato) aggiungi la stessa riga, poi **riavvia il server**.

- [ ] **Step 3b: Aggiungi lo schema**

In `backend/controllers/schemas.py`, dopo `LoginRequest`:

```python
class PosizioneDemoRequest(BaseModel):
    lat: float
    lng: float
```

- [ ] **Step 3c: Aggiungi l'endpoint**

In `backend/controllers/corsa_controller.py`:

In testa, estendere gli import:

```python
import config
from dal.corsa_repository import CorsaRepository
from bll.servizio_mappa import ServizioMappa
from controllers.schemas import PosizioneDemoRequest
```

In fondo al file:

```python
# [IF-OP.01 / IF-UT.08] Helper demo di presentazione (gated all'account demo):
# aggiorna la posizione del mezzo della corsa per simularne il movimento sulla mappa.
@router.patch("/corse/{corsa_id}/demo/posizione", status_code=204)
def aggiorna_posizione_demo(
    corsa_id: UUID,
    body: PosizioneDemoRequest,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    if not config.DEMO_ACCOUNT_EMAIL or utente["email"] != config.DEMO_ACCOUNT_EMAIL:
        raise HTTPException(status_code=403, detail="Funzione demo non disponibile per questo account")
    corsa = CorsaRepository(db).trova_per_id(corsa_id)
    if corsa is None or corsa["utente_id"] != str(utente["id"]):
        raise HTTPException(status_code=403, detail="Corsa non appartenente all'utente")
    ServizioMappa(db).aggiorna_posizione_mezzo(UUID(corsa["mezzo_id"]), body.lat, body.lng)
```

- [ ] **Step 4: Run test to verify it passes**

Riavviare il server (per caricare `DEMO_ACCOUNT_EMAIL` e la nuova route). Verificare con:
`curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/openapi.json` → 200.
Run: `cd backend && uv run pytest tests/test_demo_posizione_http.py -v -m integration`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/config.py backend/.env.example backend/controllers/schemas.py backend/controllers/corsa_controller.py backend/tests/test_demo_posizione_http.py
git commit -m "feat(api): endpoint demo posizione mezzo gated all'account demo"
```

---

### Task 4: Frontend — `geoUtils.zonaCorrente`

**Files:**
- Modify: `frontend/src/utils/geoUtils.ts`

**Interfaces:**
- Consumes: `puntoInPoligono`, `distanzaDaPoligono` (già presenti), `ZonaMappa` (type-only da `MapService`)
- Produces: `zonaCorrente(lat, lng, zone, margineFuoriM?) -> { tipo: TipoZonaCorrente; limiteVelocita?: number }`, type `TipoZonaCorrente = 'vietata' | 'limitata' | 'operativa' | 'fuori'`

- [ ] **Step 1: Implementa la funzione** (no test runner FE: si verifica con `tsc -b`)

In coda a `frontend/src/utils/geoUtils.ts`:

```ts
import type { ZonaMappa } from '../services/MapService'

export type TipoZonaCorrente = 'vietata' | 'limitata' | 'operativa' | 'fuori'

// Precedenza zone: vietata > limitata > operativa (docs/Sprintn3.md §4.2).
// Calcolo lato client riusando la logica già usata in VistaCorsa per la zona operativa.
export function zonaCorrente(
  lat: number,
  lng: number,
  zone: ZonaMappa[],
  margineFuoriM = 200,
): { tipo: TipoZonaCorrente; limiteVelocita?: number } {
  const attive = zone.filter(z => z.attiva)
  if (attive.some(z => z.tipo === 'vietata' && puntoInPoligono(lat, lng, z.perimetro))) {
    return { tipo: 'vietata' }
  }
  const limitata = attive.find(z => z.tipo === 'limitata' && puntoInPoligono(lat, lng, z.perimetro))
  if (limitata) return { tipo: 'limitata', limiteVelocita: limitata.limite_velocita ?? undefined }
  const operative = attive.filter(z => z.tipo === 'operativa')
  if (operative.length === 0) return { tipo: 'operativa' }
  if (operative.some(z => puntoInPoligono(lat, lng, z.perimetro))) return { tipo: 'operativa' }
  const distMin = Math.min(...operative.map(z => distanzaDaPoligono(lat, lng, z.perimetro)))
  return distMin > margineFuoriM ? { tipo: 'fuori' } : { tipo: 'operativa' }
}
```

- [ ] **Step 2: Verifica compilazione**

Run: `cd frontend && npx tsc -b`
Expected: exit 0, nessun errore.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/utils/geoUtils.ts
git commit -m "feat(fe): geoUtils.zonaCorrente con precedenza zone"
```

---

### Task 5: Frontend — `CorsaService.aggiornaPosizioneDemo`

**Files:**
- Modify: `frontend/src/services/CorsaService.ts`

**Interfaces:**
- Produces: `aggiornaPosizioneDemo(corsaId: string, lat: number, lng: number) -> Promise<void>`

- [ ] **Step 1: Implementa la funzione**

In `frontend/src/services/CorsaService.ts`, in coda (mantieni lo stile delle altre funzioni che usano `api`):

```ts
// Helper demo di presentazione: aggiorna la posizione del mezzo della corsa.
export const aggiornaPosizioneDemo = async (corsaId: string, lat: number, lng: number): Promise<void> => {
  await api.patch(`/utente/corse/${corsaId}/demo/posizione`, { lat, lng })
}
```

(Se `api` non è già importato in questo file, aggiungi `import { api } from './ApiService'` in testa — verifica prima per non duplicare.)

- [ ] **Step 2: Verifica compilazione**

Run: `cd frontend && npx tsc -b`
Expected: exit 0.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/CorsaService.ts
git commit -m "feat(fe): CorsaService.aggiornaPosizioneDemo"
```

---

### Task 6: Frontend — VistaCorsa: pulsante demo + convoglio + banner

**Files:**
- Modify: `frontend/src/views/utente/VistaCorsa.tsx`
- Modify: `frontend/src/views/utente/VistaCorsa.css` (stili banner limitata/vietata)
- Modify: `frontend/.env.example` (documentare `VITE_DEMO_EMAIL`)

**Interfaces:**
- Consumes: `zonaCorrente`/`TipoZonaCorrente` (Task 4), `aggiornaPosizioneDemo` (Task 5), `utenteCorrente` (AuthService), `getZoneUtente`/`ZonaMappa` (già importati)

- [ ] **Step 1: Aggiorna import e stato**

In `frontend/src/views/utente/VistaCorsa.tsx`:

Estendi gli import esistenti:

```ts
import { terminaCorsa, sospendiCorsa, riprendiCorsa, getRiepilogoCorsa, aggiornaPosizioneDemo, type Corsa, type RispostaSospensione } from '../../services/CorsaService'
import { puntoInPoligono, distanzaDaPoligono, zonaCorrente, type TipoZonaCorrente } from '../../utils/geoUtils'
import { utenteCorrente } from '../../services/AuthService'
```

Dopo lo stato `zoneOperative`/`fuoriZona` (~riga 93) aggiungi:

```ts
  const [zoneTutte, setZoneTutte] = useState<ZonaMappa[]>([])
  const [statoZonaDemo, setStatoZonaDemo] = useState<{ tipo: TipoZonaCorrente; limiteVelocita?: number } | null>(null)
  const demoTimerRef = useRef<number | null>(null)
  const demoAttivo = statoZonaDemo !== null
  const emailDemo = import.meta.env.VITE_DEMO_EMAIL as string | undefined
  const isAccountDemo = !!emailDemo && utenteCorrente()?.profilo.email === emailDemo
```

- [ ] **Step 2: Carica tutte le zone attive**

Modifica l'effect che chiama `getZoneUtente` (~riga 116) per popolare anche `zoneTutte`:

```ts
  useEffect(() => {
    getZoneUtente()
      .then(zone => {
        setZoneOperative(zone.filter(z => z.tipo === 'operativa' && z.attiva))
        setZoneTutte(zone.filter(z => z.attiva))
      })
      .catch(() => {})
  }, [])
```

- [ ] **Step 3: Aggiungi le funzioni del convoglio e il driver**

Prima del `return` del componente, aggiungi:

```ts
  // --- Demo movimento (helper di presentazione, solo account demo) ---
  const avviaDemoMovimento = useCallback(() => {
    if (corse.length === 0 || zoneTutte.length === 0 || demoTimerRef.current !== null) return

    type P = { lat: number; lng: number }
    const CAMPUS: P = { lat: 41.1095, lng: 16.8806 }       // "Campus universitario" (limitata, vmax 15)
    const POLITECNICO: P = { lat: 41.1093, lng: 16.8791 }  // "Politecnico" (vietata, dentro Campus)
    const OPERATIVA_CENTRO: P = { lat: 41.11033, lng: 16.86814 }
    const LAG = 2

    const interpola = (a: P, b: P, n: number): P[] => {
      const out: P[] = []
      for (let k = 1; k <= n; k++) out.push({ lat: a.lat + (b.lat - a.lat) * k / n, lng: a.lng + (b.lng - a.lng) * k / n })
      return out
    }

    const start: P = { lat: corse[0].mezzo.lat, lng: corse[0].mezzo.lng }
    const percorso: P[] = [start, ...interpola(start, CAMPUS, 6), ...interpola(CAMPUS, POLITECNICO, 4)]
    // Marcia oltre il Politecnico nella direzione centro→Politecnico finché si esce dall'operativa.
    const dLat = POLITECNICO.lat - OPERATIVA_CENTRO.lat
    const dLng = POLITECNICO.lng - OPERATIVA_CENTRO.lng
    const norm = Math.hypot(dLat, dLng) || 1
    const stepLat = (dLat / norm) * 0.0015
    const stepLng = (dLng / norm) * 0.0015
    let cur: P = POLITECNICO
    let fuoriContati = 0
    for (let s = 0; s < 50 && fuoriContati < 3; s++) {
      cur = { lat: cur.lat + stepLat, lng: cur.lng + stepLng }
      percorso.push(cur)
      if (zonaCorrente(cur.lat, cur.lng, zoneTutte).tipo === 'fuori') fuoriContati++
    }

    const ordine: Record<TipoZonaCorrente, number> = { vietata: 0, fuori: 1, limitata: 2, operativa: 3 }
    let tick = 0
    demoTimerRef.current = window.setInterval(() => {
      let tuttiFermi = true
      let aggregato: { tipo: TipoZonaCorrente; limiteVelocita?: number } = { tipo: 'operativa' }
      corse.forEach((c, i) => {
        const idxReale = tick - i * LAG
        if (idxReale < percorso.length - 1) tuttiFermi = false
        const idx = Math.min(percorso.length - 1, Math.max(0, idxReale))
        const p = percorso[idx]
        const z = zonaCorrente(p.lat, p.lng, zoneTutte)
        if (ordine[z.tipo] < ordine[aggregato.tipo]) aggregato = z
        aggiornaPosizioneDemo(c.corsa_id, p.lat, p.lng).catch(() => {})
      })
      setStatoZonaDemo(aggregato)
      tick += 1
      if (tuttiFermi && demoTimerRef.current !== null) {
        clearInterval(demoTimerRef.current)
        demoTimerRef.current = null
      }
    }, 2000)
  }, [corse, zoneTutte])

  // Cleanup del timer demo allo smontaggio
  useEffect(() => () => {
    if (demoTimerRef.current !== null) clearInterval(demoTimerRef.current)
  }, [])
```

- [ ] **Step 4: Aggiungi pulsante e banner nel JSX**

Sostituisci il blocco esistente del banner `fuoriZona` (~righe 354-362) con:

```tsx
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
```

- [ ] **Step 5: Aggiungi gli stili**

In `frontend/src/views/utente/VistaCorsa.css`, in coda:

```css
.zona-warning-limitata { background: #fef3c7; border-color: #f59e0b; }
.zona-warning-vietata { background: #fee2e2; border-color: #ef4444; }
.btn-demo-movimento {
  margin: 12px auto; display: block; padding: 10px 18px;
  background: #155e52; color: #fff; border: none; border-radius: 999px;
  font-weight: 600; cursor: pointer;
}
.btn-demo-movimento:disabled { opacity: .6; cursor: default; }
```

- [ ] **Step 6: Documenta la env var**

In `frontend/.env.example`, aggiungi:

```
VITE_DEMO_EMAIL=demo@smartmobility.it
```

In `frontend/.env.local` (locale, non committato) aggiungi la stessa riga e riavvia `npm run dev`.

- [ ] **Step 7: Verifica compilazione**

Run: `cd frontend && npx tsc -b`
Expected: exit 0.

- [ ] **Step 8: Commit**

```bash
git add frontend/src/views/utente/VistaCorsa.tsx frontend/src/views/utente/VistaCorsa.css frontend/.env.example
git commit -m "feat(fe): VistaCorsa pulsante demo, convoglio e banner zone"
```

---

### Task 7: Frontend — VistaMappaOperatore polling posizioni

**Files:**
- Modify: `frontend/src/views/operatore/VistaMappaOperatore.tsx` (~riga 126)

- [ ] **Step 1: Aggiungi il polling**

Sostituisci:

```ts
  useEffect(() => { ricaricaDati() }, [ricaricaDati])
```

con:

```ts
  useEffect(() => {
    ricaricaDati()
    const t = setInterval(ricaricaDati, 2000)  // [IF-OP.01] aggiornamento posizioni mezzi in tempo reale
    return () => clearInterval(t)
  }, [ricaricaDati])
```

- [ ] **Step 2: Verifica compilazione**

Run: `cd frontend && npx tsc -b`
Expected: exit 0.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(fe): mappa operatore polling posizioni mezzi"
```

---

### Task 8: Documentazione — Diagramma Classi + Sprintn3

**Files:**
- Modify: `docs/Diagrammi/DiagrammaClassi.md` (aggiungere il metodo a `IServizioMappa` e a `ServizioMappa`)
- Modify: `docs/Diagrammi/Diagramma Classi.drawio` (riflettere il metodo nel sorgente)
- Modify: `docs/Sprintn3.md` (nota di implementazione tracciabilità `IF-OP.01`)

- [ ] **Step 1: Aggiorna l'export `DiagrammaClassi.md`**

In `docs/Diagrammi/DiagrammaClassi.md`, sezione `### \`IServizioMappa\``, aggiungi alla lista metodi:

```
+ aggiornaPosizioneMezzo(idMezzo, lat, lng): void
```

Cerca la classe `### \`ServizioMappa\`` (implementazione) e aggiungi lo stesso metodo nella sua lista metodi. Se la classe concreta non è listata separatamente, aggiungere solo all'interfaccia è sufficiente per coerenza del contratto.

- [ ] **Step 2: Aggiorna il sorgente `.drawio`**

Apri `docs/Diagrammi/Diagramma Classi.drawio` in draw.io (o editor XML), individua il box `IServizioMappa` (e `ServizioMappa` se presente) e aggiungi una riga metodo `+ aggiornaPosizioneMezzo(idMezzo, lat, lng): void`. Salva. Verifica che `DiagrammaClassi.md` resti l'export coerente del `.drawio`.

- [ ] **Step 3: Nota in Sprintn3**

In `docs/Sprintn3.md`, nella sezione note di implementazione / tracciabilità, aggiungi:

```
- Demo movimento mezzi (helper di presentazione, account demo): `ServizioMappa.aggiornaPosizioneMezzo`
  + endpoint `PATCH /utente/corse/{id}/demo/posizione`, geofencing client-side (`geoUtils.zonaCorrente`),
  mappa operatore in polling. Tracciabilità IF-OP.01 / IF-UT.01 / IF-UT.08.
```

- [ ] **Step 4: Commit**

```bash
git add "docs/Diagrammi/DiagrammaClassi.md" "docs/Diagrammi/Diagramma Classi.drawio" docs/Sprintn3.md
git commit -m "docs: diagramma classi aggiornato con aggiornaPosizioneMezzo + nota demo"
```

---

### Task 9: Runbook demo per l'esame

**Files:**
- Create: `docs/RunbookDemo.md`

- [ ] **Step 1: Scrivi il runbook**

```markdown
# Runbook Demo Esame — Movimento mezzi e geofencing

## Prerequisiti
- Backend e frontend avviati (o ambiente di produzione raggiungibile).
- Env: `DEMO_ACCOUNT_EMAIL=demo@smartmobility.it` (backend), `VITE_DEMO_EMAIL=demo@smartmobility.it` (frontend).
- Account demo UT: `demo@smartmobility.it` / `DemoEsame2026!` (creato con `backend/scripts/seed_demo_account.py`).
- Account operatore: `operatore@smartmobility.test` / `Operatore123!`.

## Passi
1. Finestra A (browser): login come `demo@smartmobility.it`. Finestra B: login come operatore, apri la mappa.
2. Finestra A: dalla home prenota e **sblocca i mezzi** desiderati (es. 3) → corsa di gruppo, si apre Info Corsa.
3. In Info Corsa premi **▶ Avvia demo movimento**.
4. Racconta mentre il convoglio attraversa:
   - **Campus universitario** → banner giallo "Zona a velocità limitata — max 15 km/h";
   - **Politecnico** (dentro Campus) → banner rosso "Zona vietata" → spiega la **precedenza** vietata>limitata;
   - **uscita zona operativa** → banner ⚠️ "Fuori dalla zona operativa".
   In finestra B i mezzi si muovono in fila sulla mappa operatore.
5. Termina la corsa per mostrare la **penale** zona vietata a fine corsa (caso d'uso UT-04).

## Note
- La demo gira finché la tab demo resta aperta.
- Se i banner non cambiano: verifica che le zone "Campus universitario"/"Politecnico" esistano e siano attive nel DB.
```

- [ ] **Step 2: Commit**

```bash
git add docs/RunbookDemo.md
git commit -m "docs: runbook demo esame movimento mezzi"
```

---

## Verifica finale end-to-end (manuale)

- [ ] Backend: `cd backend && uv run pytest tests/test_aggiorna_posizione.py tests/test_demo_posizione_http.py -v -m integration` → tutti PASS (server attivo, `DEMO_ACCOUNT_EMAIL` impostato).
- [ ] Frontend: `cd frontend && npx tsc -b` → exit 0; `npm run build` → build ok.
- [ ] Manuale: seguire `docs/RunbookDemo.md` con due finestre; verificare convoglio in movimento sulla mappa operatore e sequenza banner limitata→vietata→fuori in info corsa.
