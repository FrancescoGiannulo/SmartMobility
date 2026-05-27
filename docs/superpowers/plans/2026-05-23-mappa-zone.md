# Mappa Zone — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare la visualizzazione mappa con mezzi e zone per Utente (CS-01) e Operatore (CS-02/CS-03), incluso il disegno di zone via Google Maps Drawing Manager.

**Architecture:** Backend approccio B — endpoint distribuiti nei controller esistenti; `ServizioGIS` nella BLL gestisce logica geografica; `ZonaRepository` nel DAL accede a PostGIS. Frontend: `MapService.ts` per letture, `ZonaService.ts` per scritture, viste React separate per UT e OP.

**Tech Stack:** FastAPI + GeoAlchemy2 + PostGIS (backend), React 19 + @vis.gl/react-google-maps + Google Maps Drawing Manager (frontend)

---

## File Map

| File | Azione | Responsabilità |
|---|---|---|
| `backend/dal/zona_repository.py` | Modifica | CRUD zone su PostGIS |
| `backend/dal/mezzo_repository.py` | Modifica | Lista mezzi per mappa |
| `backend/bll/servizio_gis.py` | Modifica | Logica geografica: serializzazione, validazione poligoni |
| `backend/controllers/schemas.py` | Modifica | Schemi Pydantic per mappa |
| `backend/controllers/zona_operatore_controller.py` | Modifica | GET/POST/DELETE zone (OP) |
| `backend/controllers/mezzo_operatore_controller.py` | Modifica | GET mezzi per mappa (OP) |
| `backend/controllers/utente_controller.py` | Modifica | GET mezzi + zone per mappa (UT) — nuovo router `/utente` |
| `backend/main.py` | Modifica | Registra nuovi router |
| `backend/tests/test_mappa.py` | Crea | Test unitari mappa |
| `frontend/src/services/MapService.ts` | Crea | Chiamate GET mappa |
| `frontend/src/services/ZonaService.ts` | Crea | Chiamate POST/DELETE zone |
| `frontend/src/views/utente/VistaMappa.tsx` | Crea | Mappa UT con pin mezzi e zone |
| `frontend/src/views/utente/VistaMappa.css` | Crea | Stili mappa UT |
| `frontend/src/views/operatore/VistaMappaOperatore.tsx` | Crea | Dashboard OP split 70/30 |
| `frontend/src/views/operatore/VistaMappaOperatore.css` | Crea | Stili dashboard OP |
| `frontend/src/App.tsx` | Modifica | Sostituisce PlaceholderView con viste reali |

---

## Task 1: ZonaRepository (DAL)

**Files:**
- Modify: `backend/dal/zona_repository.py`

- [ ] **Step 1: Scrivi il test fallente**

Crea `backend/tests/test_mappa.py`:

```python
import pytest
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session


def _pulisci_zone(db):
    with Session(db) as s:
        s.execute(text("DELETE FROM zone WHERE nome LIKE 'test_%'"))
        s.commit()


@pytest.fixture(autouse=True)
def cleanup_zone(db):
    _pulisci_zone(db)
    yield
    _pulisci_zone(db)


def test_crea_e_lista_zona(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    coordinate = [
        [16.85, 41.11],
        [16.86, 41.11],
        [16.86, 41.12],
        [16.85, 41.12],
        [16.85, 41.11],
    ]
    zona = repo.crea("test_vietata", "vietata", coordinate, None)
    assert zona.id is not None
    assert zona.nome == "test_vietata"
    assert zona.tipo.value == "vietata"

    lista = repo.lista_zone(solo_attive=True)
    ids = [str(z["id"]) for z in lista]
    assert str(zona.id) in ids


def test_elimina_zona(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = repo.crea("test_elimina", "parcheggio", coordinate, None)
    repo.elimina(zona.id)
    lista = repo.lista_zone(solo_attive=True)
    assert str(zona.id) not in [str(z["id"]) for z in lista]
```

- [ ] **Step 2: Verifica che il test fallisca**

```bash
cd backend && uv run pytest tests/test_mappa.py -v -m "not integration"
```

Atteso: `ImportError` — `ZonaRepository` non implementato.

- [ ] **Step 3: Implementa ZonaRepository**

Sostituisci `backend/dal/zona_repository.py`:

```python
import json
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from model.zona import Zona, TipoZona


class ZonaNonTrovataException(Exception):
    pass


class ZonaRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    def lista_zone(self, solo_attive: bool = True) -> list[dict]:
        filtro = "WHERE attiva = true" if solo_attive else ""
        rows = self._db.execute(text(f"""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone {filtro}
            ORDER BY created_at DESC
        """)).fetchall()
        return [
            {
                "id": row.id,
                "nome": row.nome,
                "tipo": row.tipo,
                "limite_velocita": row.limite_velocita,
                "attiva": row.attiva,
                "perimetro": row.perimetro,
            }
            for row in rows
        ]

    def trova_per_id(self, id: UUID) -> dict:
        row = self._db.execute(text("""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone WHERE id = :id
        """), {"id": str(id)}).fetchone()
        if not row:
            raise ZonaNonTrovataException(f"Zona {id} non trovata")
        return {
            "id": row.id,
            "nome": row.nome,
            "tipo": row.tipo,
            "limite_velocita": row.limite_velocita,
            "attiva": row.attiva,
            "perimetro": row.perimetro,
        }

    def crea(self, nome: str, tipo: str, coordinate: list[list[float]], limite_velocita: int | None) -> Zona:
        geojson = json.dumps({
            "type": "Polygon",
            "coordinates": [coordinate],
        })
        row = self._db.execute(text("""
            INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
            VALUES (:nome, :tipo, ST_GeomFromGeoJSON(:geojson), :limite)
            RETURNING id, nome, tipo, limite_velocita, attiva
        """), {
            "nome": nome,
            "tipo": tipo,
            "geojson": geojson,
            "limite": limite_velocita,
        }).fetchone()
        self._db.commit()
        zona = Zona()
        zona.id = row.id
        zona.nome = row.nome
        zona.tipo = TipoZona(row.tipo)
        zona.limite_velocita = row.limite_velocita
        zona.attiva = row.attiva
        return zona

    def elimina(self, id: UUID) -> None:
        result = self._db.execute(
            text("DELETE FROM zone WHERE id = :id"), {"id": str(id)}
        )
        self._db.commit()
        if result.rowcount == 0:
            raise ZonaNonTrovataException(f"Zona {id} non trovata")
```

- [ ] **Step 4: Verifica che i test passino**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_crea_e_lista_zona tests/test_mappa.py::test_elimina_zona -v
```

Atteso: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/dal/zona_repository.py backend/tests/test_mappa.py
git commit -m "feat(mappa): ZonaRepository CRUD PostGIS [OP.03/OP.15/OP.16]"
```

---

## Task 2: MezzoRepository — metodi per mappa

**Files:**
- Modify: `backend/dal/mezzo_repository.py`

- [ ] **Step 1: Scrivi il test fallente**

Aggiungi in `backend/tests/test_mappa.py`:

```python
def test_lista_mezzi_disponibili(db):
    from dal.mezzo_repository import MezzoRepository
    from sqlalchemy.orm import Session
    # Inserisci un mezzo disponibile con posizione
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES ('TEST-001', 'monopattino', 'Disponibile', 41.11, 16.85, 80)
        """))
        s.commit()
    repo = MezzoRepository(db)
    mezzi = repo.lista_per_mappa(solo_disponibili=True)
    codici = [m["codice"] for m in mezzi]
    assert "TEST-001" in codici
    # Cleanup
    with Session(db) as s:
        s.execute(text("DELETE FROM mezzi WHERE codice = 'TEST-001'"))
        s.commit()


def test_lista_mezzi_tutti(db):
    from dal.mezzo_repository import MezzoRepository
    from sqlalchemy.orm import Session
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES ('TEST-002', 'bicicletta', 'In manutenzione', 41.12, 16.86, 20)
        """))
        s.commit()
    repo = MezzoRepository(db)
    tutti = repo.lista_per_mappa(solo_disponibili=False)
    codici = [m["codice"] for m in tutti]
    assert "TEST-002" in codici
    # solo_disponibili=True non deve includerlo
    disponibili = repo.lista_per_mappa(solo_disponibili=True)
    assert "TEST-002" not in [m["codice"] for m in disponibili]
    with Session(db) as s:
        s.execute(text("DELETE FROM mezzi WHERE codice = 'TEST-002'"))
        s.commit()
```

- [ ] **Step 2: Verifica che i test falliscano**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_lista_mezzi_disponibili tests/test_mappa.py::test_lista_mezzi_tutti -v
```

Atteso: `ImportError` o `AttributeError`.

- [ ] **Step 3: Implementa MezzoRepository**

Sostituisci `backend/dal/mezzo_repository.py`:

```python
from sqlalchemy import text
from sqlalchemy.orm import Session


class MezzoRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    def lista_per_mappa(self, solo_disponibili: bool) -> list[dict]:
        filtro = "AND stato = 'Disponibile'" if solo_disponibili else ""
        rows = self._db.execute(text(f"""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE lat IS NOT NULL AND lng IS NOT NULL {filtro}
            ORDER BY created_at DESC
        """)).fetchall()
        return [
            {
                "id": row.id,
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]
```

- [ ] **Step 4: Verifica che i test passino**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_lista_mezzi_disponibili tests/test_mappa.py::test_lista_mezzi_tutti -v
```

Atteso: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/dal/mezzo_repository.py backend/tests/test_mappa.py
git commit -m "feat(mappa): MezzoRepository.lista_per_mappa [UT.01/OP.01]"
```

---

## Task 3: ServizioGIS (BLL)

**Files:**
- Modify: `backend/bll/servizio_gis.py`

- [ ] **Step 1: Scrivi i test fallenti**

Aggiungi in `backend/tests/test_mappa.py`:

```python
def test_servizio_gis_crea_zona_valida(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = svc.crea_zona("test_gis", "vietata", coordinate, None)
    assert zona["nome"] == "test_gis"
    assert zona["tipo"] == "vietata"
    assert zona["perimetro"]["type"] == "Polygon"


def test_servizio_gis_poligono_insufficiente(db):
    from bll.servizio_gis import ServizioGIS, PoligonoNonValidoException
    svc = ServizioGIS(db)
    with pytest.raises(PoligonoNonValidoException):
        svc.crea_zona("test_err", "vietata", [[16.85, 41.11], [16.86, 41.11]], None)


def test_servizio_gis_lista_zone(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    svc.crea_zona("test_lista", "parcheggio", coordinate, None)
    zone = svc.ottieni_zone()
    nomi = [z["nome"] for z in zone]
    assert "test_lista" in nomi
```

- [ ] **Step 2: Verifica che i test falliscano**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_servizio_gis_crea_zona_valida tests/test_mappa.py::test_servizio_gis_poligono_insufficiente tests/test_mappa.py::test_servizio_gis_lista_zone -v
```

Atteso: `ImportError`.

- [ ] **Step 3: Implementa ServizioGIS**

Sostituisci `backend/bll/servizio_gis.py`:

```python
from uuid import UUID
from sqlalchemy.orm import Session
from dal.zona_repository import ZonaRepository, ZonaNonTrovataException
from dal.mezzo_repository import MezzoRepository


class PoligonoNonValidoException(Exception):
    pass


class ServizioGIS:

    def __init__(self, db: Session) -> None:
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
        # Un poligono valido richiede almeno 3 vertici distinti + punto di chiusura
        vertici_distinti = {tuple(c) for c in coordinate}
        if len(vertici_distinti) < 3:
            raise PoligonoNonValidoException("Il poligono deve avere almeno 3 vertici distinti")
        # Assicura chiusura del poligono
        if coordinate[0] != coordinate[-1]:
            coordinate = coordinate + [coordinate[0]]
        zona = self._zone_repo.crea(nome, tipo, coordinate, limite_velocita)
        return self._zone_repo.trova_per_id(zona.id)

    def elimina_zona(self, id: UUID) -> None:
        self._zone_repo.elimina(id)
```

- [ ] **Step 4: Verifica che i test passino**

```bash
cd backend && uv run pytest tests/test_mappa.py::test_servizio_gis_crea_zona_valida tests/test_mappa.py::test_servizio_gis_poligono_insufficiente tests/test_mappa.py::test_servizio_gis_lista_zone -v
```

Atteso: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_gis.py backend/tests/test_mappa.py
git commit -m "feat(mappa): ServizioGIS — validazione poligoni, CRUD zone, lettura mezzi"
```

---

## Task 4: Schemi Pydantic + Endpoint Backend

**Files:**
- Modify: `backend/controllers/schemas.py`
- Modify: `backend/controllers/zona_operatore_controller.py`
- Modify: `backend/controllers/mezzo_operatore_controller.py`
- Modify: `backend/controllers/utente_controller.py`
- Modify: `backend/main.py`

- [ ] **Step 1: Aggiungi schemi Pydantic**

Aggiungi in fondo a `backend/controllers/schemas.py`:

```python
from uuid import UUID
from typing import Any


class MezzoMappaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float
    lng: float
    batteria: int | None


class ZonaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    perimetro: dict[str, Any]
    limite_velocita: int | None
    attiva: bool


class ZonaCreate(BaseModel):
    nome: str
    tipo: str
    coordinate: list[list[float]]
    limite_velocita: int | None = None
```

- [ ] **Step 2: Implementa endpoint zona_operatore_controller**

Sostituisci `backend/controllers/zona_operatore_controller.py`:

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS, PoligonoNonValidoException
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
    except PoligonoNonValidoException as e:
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

- [ ] **Step 3: Implementa endpoint mezzo_operatore_controller**

Sostituisci `backend/controllers/mezzo_operatore_controller.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()
```

- [ ] **Step 4: Aggiungi endpoint mappa a utente_controller**

Aggiungi in fondo a `backend/controllers/utente_controller.py`:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut, ZonaOut

mappa_router = APIRouter(prefix="/utente", tags=["Mappa Utente"])


@mappa_router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Mezzi disponibili per la Mappa Utente."""
    return ServizioGIS(db).ottieni_mezzi_utente()


@mappa_router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Zone attive per la Mappa Utente."""
    return ServizioGIS(db).ottieni_zone()
```

- [ ] **Step 5: Registra i router in main.py**

Sostituisci `backend/main.py`:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as auth_router
from controllers.utente_controller import mappa_router
from controllers.mezzo_operatore_controller import router as mezzo_op_router
from controllers.zona_operatore_controller import router as zona_op_router

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


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
```

- [ ] **Step 6: Avvia il backend e verifica gli endpoint su Swagger**

```bash
cd backend && uv run uvicorn main:app --reload
```

Apri http://localhost:8000/docs e verifica che esistano:
- `GET /utente/mappa/mezzi`
- `GET /utente/mappa/zone`
- `GET /operatore/mappa/mezzi`
- `GET /operatore/zone`
- `POST /operatore/zone`
- `DELETE /operatore/zone/{zona_id}`

- [ ] **Step 7: Commit**

```bash
git add backend/controllers/schemas.py backend/controllers/zona_operatore_controller.py backend/controllers/mezzo_operatore_controller.py backend/controllers/utente_controller.py backend/main.py
git commit -m "feat(mappa): endpoint mappa UT/OP e CRUD zone [CS-01/CS-02/CS-03]"
```

---

## Task 5: Test endpoint HTTP

**Files:**
- Modify: `backend/tests/test_mappa.py`

- [ ] **Step 1: Aggiungi test HTTP**

Aggiungi in fondo a `backend/tests/test_mappa.py`:

```python
import httpx


def _login(email: str, password: str) -> str:
    r = httpx.post("http://localhost:8000/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]


def test_mappa_mezzi_utente_autenticato(utente_test):
    token = _login(utente_test["email"], utente_test["password"])
    r = httpx.get(
        "http://localhost:8000/utente/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_mappa_mezzi_utente_non_autenticato():
    r = httpx.get("http://localhost:8000/utente/mappa/mezzi")
    assert r.status_code == 401


def test_crea_zona_via_http(operatore_test, db):
    token = _login(operatore_test["email"], operatore_test["password"])
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
    # Cleanup
    zona_id = data["id"]
    httpx.delete(
        f"http://localhost:8000/operatore/zone/{zona_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


def test_crea_zona_poligono_invalido(operatore_test):
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "test_invalido",
        "tipo": "vietata",
        "coordinate": [[16.85, 41.11], [16.86, 41.11]],
        "limite_velocita": None,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 422
```

- [ ] **Step 2: Esegui i test HTTP (richiede backend avviato)**

Con il backend attivo in un altro terminale:

```bash
cd backend && uv run pytest tests/test_mappa.py::test_mappa_mezzi_utente_autenticato tests/test_mappa.py::test_mappa_mezzi_utente_non_autenticato tests/test_mappa.py::test_crea_zona_via_http tests/test_mappa.py::test_crea_zona_poligono_invalido -v
```

Atteso: PASS (tutti e 4).

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_mappa.py
git commit -m "test(mappa): test HTTP endpoint mappa UT/OP e CRUD zone"
```

---

## Task 6: MapService.ts e ZonaService.ts

**Files:**
- Create: `frontend/src/services/MapService.ts`
- Create: `frontend/src/services/ZonaService.ts`

- [ ] **Step 1: Crea MapService.ts**

Crea `frontend/src/services/MapService.ts`:

```typescript
import { api } from './ApiService'

export interface MezzoMappa {
  id: string
  codice: string
  tipo: 'monopattino' | 'bicicletta' | 'automobile'
  stato: string
  lat: number
  lng: number
  batteria: number | null
}

export interface ZonaMappa {
  id: string
  nome: string
  tipo: 'operativa' | 'parcheggio' | 'limitata' | 'vietata'
  perimetro: {
    type: 'Polygon'
    coordinates: number[][][]
  }
  limite_velocita: number | null
  attiva: boolean
}

export const getMezziUtente = async (): Promise<MezzoMappa[]> => {
  const r = await api.get<MezzoMappa[]>('/utente/mappa/mezzi')
  return r.data
}

export const getZoneUtente = async (): Promise<ZonaMappa[]> => {
  const r = await api.get<ZonaMappa[]>('/utente/mappa/zone')
  return r.data
}

export const getMezziOperatore = async (): Promise<MezzoMappa[]> => {
  const r = await api.get<MezzoMappa[]>('/operatore/mappa/mezzi')
  return r.data
}

export const getZoneOperatore = async (): Promise<ZonaMappa[]> => {
  const r = await api.get<ZonaMappa[]>('/operatore/zone')
  return r.data
}
```

- [ ] **Step 2: Crea ZonaService.ts**

Crea `frontend/src/services/ZonaService.ts`:

```typescript
import { api } from './ApiService'
import type { ZonaMappa } from './MapService'

export interface ZonaCreate {
  nome: string
  tipo: string
  coordinate: number[][]
  limite_velocita: number | null
}

export const creaZona = async (dati: ZonaCreate): Promise<ZonaMappa> => {
  const r = await api.post<ZonaMappa>('/operatore/zone', dati)
  return r.data
}

export const eliminaZona = async (id: string): Promise<void> => {
  await api.delete(`/operatore/zone/${id}`)
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/MapService.ts frontend/src/services/ZonaService.ts
git commit -m "feat(mappa): MapService e ZonaService [CS-01/CS-02/CS-03]"
```

---

## Task 7: VistaMappa (Utente — CS-01 / IUI-2)

**Files:**
- Create: `frontend/src/views/utente/VistaMappa.tsx`
- Create: `frontend/src/views/utente/VistaMappa.css`

- [ ] **Step 1: Crea VistaMappa.css**

Crea `frontend/src/views/utente/VistaMappa.css`:

```css
.vista-mappa {
  width: 100%;
  height: 100vh;
  position: relative;
}

.mappa-container {
  width: 100%;
  height: 100%;
}

.mappa-errore {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  font-size: 14px;
  color: #d32f2f;
  text-align: center;
  max-width: 300px;
}

.mappa-nessun-mezzo {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  font-size: 14px;
  color: #555;
  white-space: nowrap;
}

.mappa-topbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 10;
  gap: 12px;
}

.mappa-topbar h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #222;
  flex: 1;
}

.btn-logout-mappa {
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

- [ ] **Step 2: Crea VistaMappa.tsx**

Crea `frontend/src/views/utente/VistaMappa.tsx`:

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  APIProvider,
  Map,
  AdvancedMarker,
  Polygon,
} from '@vis.gl/react-google-maps'
import { getMezziUtente, getZoneUtente, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import './VistaMappa.css'

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string

// Coordinate centro di default (Bari — da aggiornare con Zootropolis reale)
const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_ZONA: Record<string, { fill: string; stroke: string }> = {
  vietata:   { fill: 'rgba(244,67,54,0.25)',  stroke: '#f44336' },
  limitata:  { fill: 'rgba(255,152,0,0.25)',  stroke: '#ff9800' },
  parcheggio:{ fill: 'rgba(76,175,80,0.25)',  stroke: '#4caf50' },
  operativa: { fill: 'rgba(33,150,243,0.25)', stroke: '#2196f3' },
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

export default function VistaMappa() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [centro, setCentro] = useState(CENTRO_DEFAULT)
  const [errore, setErrore] = useState('')

  useEffect(() => {
    // Geolocalizzazione utente
    navigator.geolocation?.getCurrentPosition(
      pos => setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => {} // fallback su CENTRO_DEFAULT già impostato
    )
    // Carica dati mappa
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

      <APIProvider apiKey={API_KEY}>
        <Map
          className="mappa-container"
          defaultCenter={centro}
          defaultZoom={14}
          mapId="mappa-utente"
          gestureHandling="greedy"
          disableDefaultUI={false}
          style={{ paddingTop: 56 }}
        >
          {/* Pin mezzi */}
          {mezzi.map(m => (
            <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
              <PinMezzo tipo={m.tipo} />
            </AdvancedMarker>
          ))}

          {/* Poligoni zone */}
          {zone.map(z => {
            const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
            // GeoJSON coordinate: [[[lng, lat], ...]] → inverti per Google Maps
            const paths = z.perimetro.coordinates[0].map(([lng, lat]) => ({ lat, lng }))
            return (
              <Polygon
                key={z.id}
                paths={paths}
                strokeColor={colori.stroke}
                strokeOpacity={1}
                strokeWeight={2}
                fillColor={colori.fill}
                fillOpacity={1}
              />
            )
          })}
        </Map>
      </APIProvider>

      {errore && <div className="mappa-errore">{errore}</div>}
      {!errore && mezzi.length === 0 && (
        <div className="mappa-nessun-mezzo">Nessun mezzo disponibile nelle vicinanze</div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/utente/VistaMappa.tsx frontend/src/views/utente/VistaMappa.css
git commit -m "feat(mappa): VistaMappa utente con pin mezzi e zone [CS-01/UT.01]"
```

---

## Task 8: VistaMappaOperatore (Operatore — CS-02/CS-03 / IUI-16)

**Files:**
- Create: `frontend/src/views/operatore/VistaMappaOperatore.tsx`
- Create: `frontend/src/views/operatore/VistaMappaOperatore.css`

- [ ] **Step 1: Crea VistaMappaOperatore.css**

Crea `frontend/src/views/operatore/VistaMappaOperatore.css`:

```css
.vista-mappa-op {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.mappa-op-topbar {
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

.mappa-op-topbar h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #222;
  flex: 1;
}

.mappa-op-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.mappa-op-mappa {
  flex: 70%;
  height: 100%;
}

.mappa-op-pannello {
  flex: 30%;
  background: #f9f9f9;
  border-left: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  gap: 10px;
  overflow-y: auto;
}

.mappa-op-pannello .logo {
  font-size: 13px;
  font-weight: 700;
  color: #4caf9a;
  text-align: center;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.btn-pannello {
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

.btn-pannello:hover {
  background: #3d9e8a;
}

.btn-pannello.secondario {
  background: transparent;
  color: #4caf9a;
  border: 2px solid #4caf9a;
}

.btn-pannello.secondario:hover {
  background: #e8f5e9;
}

.btn-pannello.danger {
  background: transparent;
  color: #d32f2f;
  border: 2px solid #d32f2f;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-card {
  background: #fff;
  border-radius: 16px;
  padding: 28px 24px;
  width: 340px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}

.modal-card h3 {
  margin: 0;
  font-size: 18px;
  color: #222;
}

.modal-card input,
.modal-card select {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
  box-sizing: border-box;
}

.modal-errore {
  color: #d32f2f;
  font-size: 13px;
}

.btn-logout-mappa {
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

- [ ] **Step 2: Crea VistaMappaOperatore.tsx**

Crea `frontend/src/views/operatore/VistaMappaOperatore.tsx`:

```tsx
import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  APIProvider,
  Map,
  AdvancedMarker,
  Polygon,
  useMap,
} from '@vis.gl/react-google-maps'
import { getMezziOperatore, getZoneOperatore, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { creaZona } from '../../services/ZonaService'
import { logout } from '../../services/AuthService'
import './VistaMappaOperatore.css'

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string
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

type TipoZona = 'vietata' | 'limitata' | 'parcheggio' | 'operativa'

interface ModalZona {
  tipo: TipoZona
  coordinate: google.maps.LatLngLiteral[]
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
    return () => {
      dm.setMap(null)
    }
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
    } catch {
      setErroreModal('Errore durante il salvataggio. Riprova.')
    } finally {
      setCaricamento(false)
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
          <APIProvider
            apiKey={API_KEY}
            libraries={['drawing']}
          >
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
                const paths = z.perimetro.coordinates[0].map(([lng, lat]) => ({ lat, lng }))
                return (
                  <Polygon
                    key={z.id}
                    paths={paths}
                    strokeColor={colori.stroke}
                    strokeOpacity={1}
                    strokeWeight={2}
                    fillColor={colori.fill}
                    fillOpacity={1}
                  />
                )
              })}
            </Map>
          </APIProvider>
        </div>

        <div className="mappa-op-pannello">
          <div className="logo">SMART MOBILITY</div>

          <button className="btn-pannello" onClick={() => avviaDisegno('vietata')}>
            🚫 DEFINISCI ZONA VIETATA
          </button>
          <button className="btn-pannello" style={{ background: '#ff9800' }} onClick={() => avviaDisegno('limitata')}>
            ⚠️ DEFINISCI ZONA LIMITATA
          </button>
          <button className="btn-pannello" style={{ background: '#4caf50' }} onClick={() => avviaDisegno('parcheggio')}>
            🅿️ DEFINISCI ZONA PARCHEGGIO
          </button>
          <button className="btn-pannello" style={{ background: '#2196f3' }} onClick={() => avviaDisegno('operativa')}>
            📍 DEFINISCI CONFINE OPERATIVO
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
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/operatore/VistaMappaOperatore.tsx frontend/src/views/operatore/VistaMappaOperatore.css
git commit -m "feat(mappa): VistaMappaOperatore split 70/30 con DrawingManager [CS-02/CS-03/OP.01/OP.03/OP.15/OP.16]"
```

---

## Task 9: Routing — collega le viste in App.tsx

**Files:**
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Aggiorna App.tsx**

Sostituisci `frontend/src/App.tsx`:

```tsx
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import VistaLogin from './views/auth/VistaLogin'
import CallbackOAuth from './views/auth/CallbackOAuth'
import RoutaProtetta from './components/RoutaProtetta'
import VistaMappa from './views/utente/VistaMappa'
import VistaMappaOperatore from './views/operatore/VistaMappaOperatore'
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

- [ ] **Step 2: Avvia frontend e verifica visivamente**

```bash
cd frontend && npm run dev
```

- Login come UT (`ut_test@example.com` / `TestPass123!` se disponibile, oppure crea un account da UI) → deve aprirsi la mappa con Google Maps
- Login come OP (`operatore@smartmobility.test` / `Operatore123!`) → deve aprirsi la dashboard split 70/30
- Clicca "DEFINISCI ZONA VIETATA" → deve apparire il banner in basso con istruzioni
- Disegna un poligono → deve aprirsi il modal con campo nome
- Inserisci nome e salva → la zona deve apparire sulla mappa in rosso

- [ ] **Step 3: Commit finale**

```bash
git add frontend/src/App.tsx
git commit -m "feat(mappa): collega VistaMappa e VistaMappaOperatore al routing [CS-01/CS-02]"
```

---

## Self-Review

**Spec coverage:**
- ✅ CS-01 (UT.01) — VistaMappa con pin mezzi, poligoni zone, geolocalizzazione
- ✅ CS-02 (OP.01) — VistaMappaOperatore con tutta la flotta
- ✅ CS-03 (OP.03/OP.15/OP.16) — Drawing Manager + modal + POST /operatore/zone
- ✅ Test: 6 scenari (unitari + HTTP)
- ✅ Errori: poligono invalido 422, no auth 401, fallback geolocalizzazione

**Tipo consistency:** `MezzoMappaOut`, `ZonaOut`, `ZonaCreate` definiti in Task 4 e usati identici nei Task 6-8. Metodi `ServizioGIS` definiti in Task 3 e chiamati identici in Task 4.

**Placeholder:** nessuno.
