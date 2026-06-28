# Miglioramenti Mappa Zone — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare 3 miglioramenti alla feature mappa-zone: (1) vincolo zona operativa per tipi non-operativi, (2) eliminazione zone dalla mappa, (3) tooltip hover sulle zone per entrambe le viste.

**Architecture:** Backend aggiunge controllo PostGIS ST_Within in `ServizioGIS.crea_zona()`; frontend estrae un componente `ZonaPoligono` che usa poligoni Google Maps nativi con event listener per hover e click; entrambe le viste ottengono un `InfoWindow` tooltip; `VistaMappaOperatore` ottiene un dialog di conferma eliminazione e gestione errore 422 specifico.

**Tech Stack:** FastAPI + PostGIS (ST_Within), SQLAlchemy raw SQL, React 19 + `@vis.gl/react-google-maps` (InfoWindow, useMap), TypeScript. Branch di lavoro: `feature/mappa-zone`.

---

## File interessati

**Backend:**
- Modify: `backend/dal/zona_repository.py` — aggiunge `esiste_zona_operativa_contenente()`
- Modify: `backend/bll/servizio_gis.py` — aggiunge `PoligonoFuoriZonaOperativaException` + check in `crea_zona()`
- Modify: `backend/controllers/zona_operatore_controller.py` — cattura la nuova eccezione → HTTP 422
- Modify: `backend/tests/test_mappa.py` — nuovi test + aggiornamento test esistenti che rompono

**Frontend:**
- Create: `frontend/src/components/ZonaPoligono.tsx` — poligono nativo con hover/click
- Modify: `frontend/src/views/utente/VistaMappa.tsx` — usa ZonaPoligono + InfoWindow tooltip
- Modify: `frontend/src/views/operatore/VistaMappaOperatore.tsx` — usa ZonaPoligono + tooltip + dialog eliminazione + errore 422

---

## Task 1: DAL — `esiste_zona_operativa_contenente` in ZonaRepository

**Files:**
- Modify: `backend/dal/zona_repository.py`
- Test: `backend/tests/test_mappa.py`

- [ ] **Step 1.1: Scrivi il test fallente**

Aggiungi in fondo a `backend/tests/test_mappa.py`:

```python
def test_repo_esiste_zona_operativa_contenente_true(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    # Crea zona operativa grande
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    repo.crea("test_op_outer", "operativa", operativa, None)
    # Poligono piccolo interno
    interno = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    assert repo.esiste_zona_operativa_contenente(interno) is True


def test_repo_esiste_zona_operativa_contenente_false(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    # Nessuna zona operativa → False
    esterno = [
        [16.90, 41.15], [16.91, 41.15],
        [16.91, 41.16], [16.90, 41.16], [16.90, 41.15],
    ]
    assert repo.esiste_zona_operativa_contenente(esterno) is False
```

- [ ] **Step 1.2: Esegui per verificare il fallimento**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_repo_esiste_zona_operativa_contenente_true tests/test_mappa.py::test_repo_esiste_zona_operativa_contenente_false -v -m integration
```

Atteso: `FAILED` con `AttributeError: 'ZonaRepository' object has no attribute 'esiste_zona_operativa_contenente'`

- [ ] **Step 1.3: Implementa il metodo in `backend/dal/zona_repository.py`**

Aggiungi dopo il metodo `elimina`:

```python
def esiste_zona_operativa_contenente(self, coordinate: list[list[float]]) -> bool:
    """True se esiste almeno una zona operativa attiva che contiene ST_Within il poligono dato."""
    if coordinate[0] != coordinate[-1]:
        coordinate = coordinate + [coordinate[0]]
    geojson = json.dumps({"type": "Polygon", "coordinates": [coordinate]})
    sql = text("""
        SELECT EXISTS(
            SELECT 1 FROM zone
            WHERE tipo = 'operativa'
              AND attiva = true
              AND ST_Within(ST_GeomFromGeoJSON(:geojson), perimetro)
        )
    """)
    with self._sessione() as s:
        row = s.execute(sql, {"geojson": geojson}).fetchone()
    return bool(row[0]) if row else False
```

- [ ] **Step 1.4: Esegui per verificare il passaggio**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_repo_esiste_zona_operativa_contenente_true tests/test_mappa.py::test_repo_esiste_zona_operativa_contenente_false -v -m integration
```

Atteso: entrambi `PASSED`

- [ ] **Step 1.5: Commit**

```bash
git add backend/dal/zona_repository.py backend/tests/test_mappa.py
git commit -m "feat(gis): ZonaRepository.esiste_zona_operativa_contenente via ST_Within [IF-OP.02]"
```

---

## Task 2: BLL + Controller — vincolo zona operativa

**Files:**
- Modify: `backend/bll/servizio_gis.py`
- Modify: `backend/controllers/zona_operatore_controller.py`
- Modify: `backend/tests/test_mappa.py`

- [ ] **Step 2.1: Scrivi i test BLL e HTTP fallenti**

Aggiungi in `backend/tests/test_mappa.py`:

```python
def test_servizio_gis_vincolo_zona_operativa_ok(db):
    """Zona non-operativa dentro una zona operativa → crea correttamente."""
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_vincolo", "operativa", operativa, None)
    interno = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = svc.crea_zona("test_vietata_interna", "vietata", interno, None)
    assert zona["nome"] == "test_vietata_interna"


def test_servizio_gis_vincolo_zona_operativa_fuori(db):
    """Zona non-operativa fuori da qualsiasi zona operativa → PoligonoFuoriZonaOperativaException."""
    from bll.servizio_gis import ServizioGIS, PoligonoFuoriZonaOperativaException
    svc = ServizioGIS(db)
    esterno = [
        [16.90, 41.15], [16.91, 41.15],
        [16.91, 41.16], [16.90, 41.16], [16.90, 41.15],
    ]
    with pytest.raises(PoligonoFuoriZonaOperativaException):
        svc.crea_zona("test_fuori", "vietata", esterno, None)


def test_crea_zona_fuori_operativa_http(operatore_test):
    """POST /operatore/zone con zona non-operativa fuori confine → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "test_fuori_http",
        "tipo": "limitata",
        "coordinate": [
            [16.90, 41.15], [16.91, 41.15],
            [16.91, 41.16], [16.90, 41.16],
        ],
        "limite_velocita": 30,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 422
```

- [ ] **Step 2.2: Esegui per verificare il fallimento dei nuovi test**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_servizio_gis_vincolo_zona_operativa_ok tests/test_mappa.py::test_servizio_gis_vincolo_zona_operativa_fuori tests/test_mappa.py::test_crea_zona_fuori_operativa_http -v -m integration
```

Atteso: tutti `FAILED` (PoligonoFuoriZonaOperativaException non esiste ancora)

- [ ] **Step 2.3: Aggiorna `test_servizio_gis_crea_zona_valida` che romperà dopo il cambio**

Il test esistente crea una zona "vietata" senza zona operativa. Aggiornalo creando prima una zona operativa:

```python
def test_servizio_gis_crea_zona_valida(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    # Zona operativa contenitore
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_valida", "operativa", operativa, None)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = svc.crea_zona("test_gis", "vietata", coordinate, None)
    assert zona["nome"] == "test_gis"
    assert zona["tipo"] == "vietata"
    assert zona["perimetro"]["type"] == "Polygon"
```

Aggiorna anche `test_crea_zona_via_http` (aggiunge zona operativa HTTP prima della zona vietata):

```python
def test_crea_zona_via_http(operatore_test):
    token = _login(operatore_test["email"], operatore_test["password"])
    # Crea zona operativa contenitore
    r_op = httpx.post(
        "http://localhost:8000/operatore/zone",
        json={
            "nome": "test_op_http",
            "tipo": "operativa",
            "coordinate": [
                [16.84, 41.10], [16.88, 41.10],
                [16.88, 41.14], [16.84, 41.14],
            ],
            "limite_velocita": None,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r_op.status_code == 201
    op_id = r_op.json()["id"]

    payload = {
        "nome": "test_http_zona",
        "tipo": "vietata",
        "coordinate": [
            [16.85, 41.11], [16.86, 41.11],
            [16.86, 41.12], [16.85, 41.12],
        ],
        "limite_velocita": None,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["nome"] == "test_http_zona"
    assert data["tipo"] == "vietata"
    assert data["perimetro"]["type"] == "Polygon"
    zona_id = data["id"]
    httpx.delete(
        f"http://localhost:8000/operatore/zone/{zona_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    httpx.delete(
        f"http://localhost:8000/operatore/zone/{op_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
```

Aggiorna anche `test_servizio_gis_lista_zone`:

```python
def test_servizio_gis_lista_zone(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_lista", "operativa", operativa, None)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    svc.crea_zona("test_lista", "parcheggio", coordinate, None)
    zone = svc.ottieni_zone()
    nomi = [z["nome"] for z in zone]
    assert "test_lista" in nomi
```

- [ ] **Step 2.4: Implementa `PoligonoFuoriZonaOperativaException` e il check in `backend/bll/servizio_gis.py`**

```python
from uuid import UUID
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from dal.zona_repository import ZonaRepository
from dal.mezzo_repository import MezzoRepository


class PoligonoNonValidoException(Exception):
    pass


class PoligonoFuoriZonaOperativaException(Exception):
    pass


class ServizioGIS:
    """Funzionalità geografiche: zone, posizioni, validazione perimetri."""

    def __init__(self, db: Session | Engine) -> None:
        self._zone_repo = ZonaRepository(db)
        self._mezzo_repo = MezzoRepository(db)

    def ottieni_zone(self) -> list[dict]:
        return self._zone_repo.lista_zone(solo_attive=True)

    def ottieni_mezzi_utente(self) -> list[dict]:
        return self._mezzo_repo.lista_per_mappa(solo_disponibili=True)

    def ottieni_mezzi_operatore(self) -> list[dict]:
        return self._mezzo_repo.lista_per_mappa(solo_disponibili=False)

    def crea_zona(
        self,
        nome: str,
        tipo: str,
        coordinate: list[list[float]],
        limite_velocita: int | None,
    ) -> dict:
        vertici_distinti = {tuple(c) for c in coordinate}
        if len(vertici_distinti) < 3:
            raise PoligonoNonValidoException("Il poligono deve avere almeno 3 vertici distinti")
        if coordinate[0] != coordinate[-1]:
            coordinate = coordinate + [coordinate[0]]
        # [IF-OP.02] Zone non-operative devono essere contenute in una zona operativa
        if tipo != "operativa":
            if not self._zone_repo.esiste_zona_operativa_contenente(coordinate):
                raise PoligonoFuoriZonaOperativaException(
                    "La zona deve essere disegnata all'interno del confine operativo"
                )
        zona = self._zone_repo.crea(nome, tipo, coordinate, limite_velocita)
        return self._zone_repo.trova_per_id(zona.id)

    def elimina_zona(self, zona_id: UUID) -> None:
        self._zone_repo.elimina(zona_id)
```

- [ ] **Step 2.5: Aggiorna `backend/controllers/zona_operatore_controller.py` per catturare la nuova eccezione**

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS, PoligonoNonValidoException, PoligonoFuoriZonaOperativaException
from dal.zona_repository import ZonaNonTrovataException
from controllers.schemas import ZonaOut, ZonaCreate

router = APIRouter(prefix="/operatore/zone", tags=["Zone Operatore"])


@router.get("", response_model=list[ZonaOut])
def lista_zone(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Lista zone attive."""
    return ServizioGIS(db).ottieni_zone()


@router.post("", response_model=ZonaOut, status_code=201)
def crea_zona(
    body: ZonaCreate,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Crea una nuova zona."""
    try:
        return ServizioGIS(db).crea_zona(
            body.nome, body.tipo, body.coordinate, body.limite_velocita
        )
    except (PoligonoNonValidoException, PoligonoFuoriZonaOperativaException) as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{zona_id}", status_code=204)
def elimina_zona(
    zona_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03] Elimina zona."""
    try:
        ServizioGIS(db).elimina_zona(zona_id)
    except ZonaNonTrovataException as e:
        raise HTTPException(status_code=404, detail=str(e))
```

- [ ] **Step 2.6: Esegui tutti i test mappa**

```bash
cd backend && uv run pytest tests/test_mappa.py -v -m integration
```

Atteso: tutti `PASSED`

- [ ] **Step 2.7: Commit**

```bash
git add backend/bll/servizio_gis.py backend/controllers/zona_operatore_controller.py backend/tests/test_mappa.py
git commit -m "feat(gis): vincolo ST_Within per zone non-operative [IF-OP.02]"
```

---

## Task 3: Frontend — componente `ZonaPoligono`

**Files:**
- Create: `frontend/src/components/ZonaPoligono.tsx`

Il componente crea un `google.maps.Polygon` nativo tramite `useMap()` e vi attacca listener `mouseover`, `mouseout`, `click`. Usa refs per i callback così da non ricreare il poligono ad ogni re-render del padre.

- [ ] **Step 3.1: Crea `frontend/src/components/ZonaPoligono.tsx`**

```tsx
import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { ZonaMappa } from '../services/MapService'

interface ZonaPoligonoProps {
  zona: ZonaMappa
  fillColor: string
  strokeColor: string
  onHover?: (zona: ZonaMappa, pos: google.maps.LatLngLiteral) => void
  onHoverEnd?: () => void
  onClick?: (zona: ZonaMappa) => void
}

export default function ZonaPoligono({
  zona, fillColor, strokeColor, onHover, onHoverEnd, onClick,
}: ZonaPoligonoProps) {
  const mappa = useMap()

  // Ref pattern: i callback e i dati della zona vengono aggiornati ad ogni render
  // senza ricaricare l'effect e ricreare il poligono
  const zonaRef = useRef(zona)
  zonaRef.current = zona
  const onHoverRef = useRef(onHover)
  onHoverRef.current = onHover
  const onHoverEndRef = useRef(onHoverEnd)
  onHoverEndRef.current = onHoverEnd
  const onClickRef = useRef(onClick)
  onClickRef.current = onClick

  useEffect(() => {
    if (!mappa || !window.google) return
    const paths = zonaRef.current.perimetro.coordinates[0].map(
      ([lng, lat]) => ({ lat, lng })
    )
    const poly = new window.google.maps.Polygon({
      paths,
      strokeColor,
      strokeOpacity: 1,
      strokeWeight: 2,
      fillColor,
      fillOpacity: 1,
      map: mappa,
    })
    window.google.maps.event.addListener(
      poly,
      'mouseover',
      (e: google.maps.MapMouseEvent) => {
        if (e.latLng) {
          onHoverRef.current?.(zonaRef.current, {
            lat: e.latLng.lat(),
            lng: e.latLng.lng(),
          })
        }
      }
    )
    window.google.maps.event.addListener(poly, 'mouseout', () => {
      onHoverEndRef.current?.()
    })
    window.google.maps.event.addListener(poly, 'click', () => {
      onClickRef.current?.(zonaRef.current)
    })
    return () => {
      window.google.maps.event.clearInstanceListeners(poly)
      poly.setMap(null)
    }
  }, [mappa, zona.id, fillColor, strokeColor]) // eslint-disable-line react-hooks/exhaustive-deps

  return null
}
```

- [ ] **Step 3.2: Commit**

```bash
git add frontend/src/components/ZonaPoligono.tsx
git commit -m "feat(mappa): componente ZonaPoligono con hover e click nativi [IF-UT.01/IF-OP.01]"
```

---

## Task 4: Frontend — tooltip hover in `VistaMappa` (utente)

**Files:**
- Modify: `frontend/src/views/utente/VistaMappa.tsx`

- [ ] **Step 4.1: Aggiorna `frontend/src/views/utente/VistaMappa.tsx`**

Sostituisci l'intero file con:

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map,
  AdvancedMarker,
  InfoWindow,
} from '@vis.gl/react-google-maps'
import { getMezziUtente, getZoneUtente, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import './VistaMappa.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_ZONA: Record<string, { fill: string; stroke: string }> = {
  vietata:    { fill: 'rgba(244,67,54,0.25)',  stroke: '#f44336' },
  limitata:   { fill: 'rgba(255,152,0,0.25)',  stroke: '#ff9800' },
  parcheggio: { fill: 'rgba(76,175,80,0.25)',  stroke: '#4caf50' },
  operativa:  { fill: 'rgba(33,150,243,0.25)', stroke: '#2196f3' },
}

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta:  '#2196f3',
  automobile:  '#e91e8c',
}

function PinMezzo({ tipo }: { tipo: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = tipo === 'monopattino' ? '🛴' : tipo === 'bicicletta' ? '🚲' : '🚗'
  return (
    <div style={{
      background: colore,
      borderRadius: '50%',
      width: 36,
      height: 36,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 18,
      boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
      border: '2px solid #fff',
    }}>
      {emoji}
    </div>
  )
}

interface ZonaHover {
  zona: ZonaMappa
  pos: google.maps.LatLngLiteral
}

export default function VistaMappa() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [centro, setCentro] = useState(CENTRO_DEFAULT)
  const [errore, setErrore] = useState('')
  const [zonaHover, setZonaHover] = useState<ZonaHover | null>(null)

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      pos => setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => {}
    )
    Promise.all([getMezziUtente(), getZoneUtente()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => setErrore('Impossibile caricare la mappa. Riprova.'))
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  return (
    <div className="vista-mappa">
      <div className="mappa-topbar">
        <h2>🚲 SMART MOBILITY</h2>
        <button className="btn-logout-mappa" onClick={handleLogout}>LOGOUT</button>
      </div>

      <Map
        className="mappa-container"
        defaultCenter={centro}
        defaultZoom={14}
        mapId="mappa-utente"
        gestureHandling="greedy"
        disableDefaultUI={false}
        style={{ paddingTop: 56 }}
      >
        {mezzi.map(m => (
          <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
            <PinMezzo tipo={m.tipo} />
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
              onHover={(zona, pos) => setZonaHover({ zona, pos })}
              onHoverEnd={() => setZonaHover(null)}
            />
          )
        })}

        {zonaHover && (
          <InfoWindow
            position={zonaHover.pos}
            onCloseClick={() => setZonaHover(null)}
          >
            <TooltipZona zona={zonaHover.zona} />
          </InfoWindow>
        )}
      </Map>

      {errore && <div className="mappa-errore">{errore}</div>}
      {!errore && mezzi.length === 0 && (
        <div className="mappa-nessun-mezzo">Nessun mezzo disponibile nelle vicinanze</div>
      )}
    </div>
  )
}

function TooltipZona({ zona }: { zona: ZonaMappa }) {
  const colori = COLORI_ZONA[zona.tipo] ?? COLORI_ZONA.operativa
  return (
    <div style={{ padding: '4px 2px', minWidth: 120 }}>
      <strong style={{ display: 'block', marginBottom: 4 }}>{zona.nome}</strong>
      <span style={{
        display: 'inline-block', padding: '2px 8px', borderRadius: 12, fontSize: 12,
        background: colori.stroke, color: '#fff',
      }}>
        {zona.tipo}
      </span>
      {zona.limite_velocita && (
        <span style={{ display: 'block', marginTop: 4, fontSize: 12 }}>
          Max {zona.limite_velocita} km/h
        </span>
      )}
    </div>
  )
}
```

- [ ] **Step 4.2: Commit**

```bash
git add frontend/src/views/utente/VistaMappa.tsx
git commit -m "feat(mappa): tooltip hover zone in VistaMappa utente [IF-UT.01]"
```

---

## Task 5: Frontend — tooltip + eliminazione + errore 422 in `VistaMappaOperatore`

**Files:**
- Modify: `frontend/src/views/operatore/VistaMappaOperatore.tsx`

- [ ] **Step 5.1: Aggiorna `frontend/src/views/operatore/VistaMappaOperatore.tsx`**

Sostituisci l'intero file con:

```tsx
import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map,
  AdvancedMarker,
  InfoWindow,
  useMap,
} from '@vis.gl/react-google-maps'
import { getMezziOperatore, getZoneOperatore, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { creaZona, eliminaZona } from '../../services/ZonaService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import './VistaMappaOperatore.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_ZONA: Record<string, { fill: string; stroke: string }> = {
  vietata:    { fill: 'rgba(244,67,54,0.25)',  stroke: '#f44336' },
  limitata:   { fill: 'rgba(255,152,0,0.25)',  stroke: '#ff9800' },
  parcheggio: { fill: 'rgba(76,175,80,0.25)',  stroke: '#4caf50' },
  operativa:  { fill: 'rgba(33,150,243,0.25)', stroke: '#2196f3' },
}

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

function TooltipZona({ zona }: { zona: ZonaMappa }) {
  const colori = COLORI_ZONA[zona.tipo] ?? COLORI_ZONA.operativa
  return (
    <div style={{ padding: '4px 2px', minWidth: 120 }}>
      <strong style={{ display: 'block', marginBottom: 4 }}>{zona.nome}</strong>
      <span style={{
        display: 'inline-block', padding: '2px 8px', borderRadius: 12, fontSize: 12,
        background: colori.stroke, color: '#fff',
      }}>
        {zona.tipo}
      </span>
      {zona.limite_velocita && (
        <span style={{ display: 'block', marginTop: 4, fontSize: 12 }}>
          Max {zona.limite_velocita} km/h
        </span>
      )}
    </div>
  )
}

type TipoZona = 'vietata' | 'limitata' | 'parcheggio' | 'operativa'

interface ModalZona {
  tipo: TipoZona
  coordinate: google.maps.LatLngLiteral[]
}

interface ZonaHover {
  zona: ZonaMappa
  pos: google.maps.LatLngLiteral
}

function DrawingManager({
  tipoAttivo,
  onCompletato,
}: {
  tipoAttivo: TipoZona | null
  onCompletato: (coords: google.maps.LatLngLiteral[]) => void
}) {
  const mappa = useMap()
  const managerRef = useRef<google.maps.drawing.DrawingManager | null>(null)

  useEffect(() => {
    if (!mappa || !window.google) return
    if (managerRef.current) {
      managerRef.current.setMap(null)
      managerRef.current = null
    }
    if (!tipoAttivo) return

    const colori = COLORI_ZONA[tipoAttivo]
    const dm = new window.google.maps.drawing.DrawingManager({
      drawingMode: window.google.maps.drawing.OverlayType.POLYGON,
      drawingControl: false,
      polygonOptions: {
        fillColor: colori.fill,
        strokeColor: colori.stroke,
        strokeWeight: 2,
        editable: false,
      },
    })
    dm.setMap(mappa)

    window.google.maps.event.addListener(dm, 'polygoncomplete', (polygon: google.maps.Polygon) => {
      const coords = polygon.getPath().getArray().map(p => ({ lat: p.lat(), lng: p.lng() }))
      polygon.setMap(null)
      dm.setMap(null)
      managerRef.current = null
      onCompletato(coords)
    })

    managerRef.current = dm
    return () => { dm.setMap(null) }
  }, [mappa, tipoAttivo, onCompletato])

  return null
}

export default function VistaMappaOperatore() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [tipoDisegno, setTipoDisegno] = useState<TipoZona | null>(null)
  const [modalZona, setModalZona] = useState<ModalZona | null>(null)
  const [nomeZona, setNomeZona] = useState('')
  const [limiteVelocita, setLimiteVelocita] = useState('')
  const [erroreModal, setErroreModal] = useState('')
  const [caricamento, setCaricamento] = useState(false)
  const [zonaHover, setZonaHover] = useState<ZonaHover | null>(null)
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const [eliminazione, setEliminazione] = useState(false)

  const ricaricaDati = useCallback(() => {
    Promise.all([getMezziOperatore(), getZoneOperatore()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => {})
  }, [])

  useEffect(() => { ricaricaDati() }, [ricaricaDati])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  const avviaDisegno = (tipo: TipoZona) => {
    setTipoDisegno(tipo)
    setModalZona(null)
  }

  const handlePoligonoCompletato = useCallback((coords: google.maps.LatLngLiteral[]) => {
    if (!tipoDisegno) return
    setModalZona({ tipo: tipoDisegno, coordinate: coords })
    setTipoDisegno(null)
    setNomeZona('')
    setLimiteVelocita('')
    setErroreModal('')
  }, [tipoDisegno])

  const handleConfermaZona = async () => {
    if (!modalZona) return
    if (!nomeZona.trim()) { setErroreModal('Inserisci un nome per la zona'); return }
    setCaricamento(true)
    setErroreModal('')
    try {
      const coordinate = modalZona.coordinate.map(p => [p.lng, p.lat])
      await creaZona({
        nome: nomeZona.trim(),
        tipo: modalZona.tipo,
        coordinate,
        limite_velocita: limiteVelocita ? parseInt(limiteVelocita) : null,
      })
      setModalZona(null)
      ricaricaDati()
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number } })?.response?.status
      if (status === 422) {
        setErroreModal("La zona deve essere disegnata all'interno del confine operativo.")
      } else {
        setErroreModal('Errore durante il salvataggio. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const handleEliminaZona = async () => {
    if (!zonaSelezionata) return
    setEliminazione(true)
    try {
      await eliminaZona(zonaSelezionata.id)
    } finally {
      setZonaSelezionata(null)
      setEliminazione(false)
      ricaricaDati()
    }
  }

  return (
    <div className="vista-mappa-op">
      <div className="mappa-op-topbar">
        <h2>🚲 SMART MOBILITY — Operatore</h2>
        <button className="btn-logout-mappa" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="mappa-op-body">
        <div className="mappa-op-mappa">
          <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={CENTRO_DEFAULT}
            defaultZoom={14}
            mapId="mappa-operatore"
            gestureHandling="greedy"
          >
            <DrawingManager
              tipoAttivo={tipoDisegno}
              onCompletato={handlePoligonoCompletato}
            />

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
                  onHover={(zona, pos) => setZonaHover({ zona, pos })}
                  onHoverEnd={() => setZonaHover(null)}
                  onClick={zona => {
                    setZonaHover(null)
                    setZonaSelezionata(zona)
                  }}
                />
              )
            })}

            {zonaHover && (
              <InfoWindow
                position={zonaHover.pos}
                onCloseClick={() => setZonaHover(null)}
              >
                <TooltipZona zona={zonaHover.zona} />
              </InfoWindow>
            )}
          </Map>
        </div>

        <div className="mappa-op-pannello">
          <div className="logo">SMART MOBILITY</div>

          <button className="btn-pannello" onClick={() => avviaDisegno('vietata')}>
            DEFINISCI ZONA VIETATA
          </button>
          <button className="btn-pannello" style={{ background: '#ff9800' }} onClick={() => avviaDisegno('limitata')}>
            DEFINISCI ZONA LIMITATA
          </button>
          <button className="btn-pannello" style={{ background: '#4caf50' }} onClick={() => avviaDisegno('parcheggio')}>
            DEFINISCI ZONA PARCHEGGIO
          </button>
          <button className="btn-pannello" style={{ background: '#2196f3' }} onClick={() => avviaDisegno('operativa')}>
            DEFINISCI CONFINE OPERATIVO
          </button>

          <hr style={{ border: 'none', borderTop: '1px solid #e0e0e0', margin: '4px 0' }} />

          <button className="btn-pannello secondario">GESTISCI SEGNALAZIONI</button>
          <button className="btn-pannello secondario">GESTISCI UTENTI</button>
          <button className="btn-pannello secondario">IMPOSTAZIONI REGOLE</button>
          <button className="btn-pannello secondario">TARIFFE E PROMOZIONI</button>
          <button className="btn-pannello secondario">VISUALIZZA REPORT</button>
          <button className="btn-pannello secondario">GESTISCI MEZZI</button>
        </div>
      </div>

      {tipoDisegno && (
        <div style={{
          position: 'fixed', bottom: 24, left: '35%', transform: 'translateX(-50%)',
          background: '#333', color: '#fff', borderRadius: 12, padding: '12px 20px',
          fontSize: 14, zIndex: 50, boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
        }}>
          Disegna il poligono sulla mappa — doppio click per chiudere
          <button
            onClick={() => setTipoDisegno(null)}
            style={{ marginLeft: 12, background: 'transparent', border: '1px solid #fff', color: '#fff', borderRadius: 8, padding: '2px 10px', cursor: 'pointer' }}
          >
            Annulla
          </button>
        </div>
      )}

      {modalZona && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Nuova zona {modalZona.tipo}</h3>
            <input
              placeholder="Nome zona"
              value={nomeZona}
              onChange={e => setNomeZona(e.target.value)}
              autoFocus
            />
            {modalZona.tipo === 'limitata' && (
              <input
                type="number"
                placeholder="Limite velocità (km/h)"
                value={limiteVelocita}
                onChange={e => setLimiteVelocita(e.target.value)}
                min={1}
              />
            )}
            {erroreModal && <p className="modal-errore">{erroreModal}</p>}
            <button className="btn-pannello" onClick={handleConfermaZona} disabled={caricamento}>
              {caricamento ? '...' : 'SALVA ZONA'}
            </button>
            <button className="btn-pannello secondario" onClick={() => setModalZona(null)}>
              Annulla
            </button>
          </div>
        </div>
      )}

      {zonaSelezionata && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Elimina zona</h3>
            <p style={{ marginBottom: 16 }}>
              Vuoi eliminare la zona <strong>{zonaSelezionata.nome}</strong>?
            </p>
            <button
              className="btn-pannello"
              style={{ background: '#f44336' }}
              onClick={handleEliminaZona}
              disabled={eliminazione}
            >
              {eliminazione ? '...' : 'ELIMINA'}
            </button>
            <button
              className="btn-pannello secondario"
              onClick={() => setZonaSelezionata(null)}
            >
              Annulla
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 5.2: Verifica che il progetto TypeScript compili senza errori**

```bash
cd frontend && npx tsc --noEmit
```

Atteso: nessun output (zero errori)

- [ ] **Step 5.3: Commit**

```bash
git add frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(mappa): tooltip hover, eliminazione zone e errore 422 in VistaMappaOperatore [IF-OP.01/IF-OP.03/IF-OP.02]"
```

---

## Task 6: Cleanup — rimuovi il file TODO

Il file `docs/TODO_mappa_zone.md` contiene l'istruzione "ELIMINARE QUESTO FILE al merge su main". Le feature sono ora implementate.

- [ ] **Step 6.1: Elimina il file**

```bash
git rm docs/TODO_mappa_zone.md
git commit -m "chore: rimuovi TODO_mappa_zone.md — feature implementate"
```

---

## Checklist finale

- [ ] `cd backend && uv run pytest tests/test_mappa.py -v -m integration` → tutti PASSED
- [ ] Frontend parte senza errori TypeScript (`npx tsc --noEmit`)
- [ ] Hover su una zona mostra tooltip con nome, tipo, limite velocità
- [ ] Click su una zona in VistaMappaOperatore apre dialog di conferma eliminazione
- [ ] Creazione zona non-operativa fuori dal confine operativo → errore specifico nel modal
- [ ] La zona operativa può sempre essere creata senza vincoli
