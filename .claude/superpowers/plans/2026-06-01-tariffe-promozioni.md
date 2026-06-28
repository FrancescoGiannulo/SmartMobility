# Tariffe & Promozioni Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementa IF-UT.05 (Consulta Tariffe) e IF-UT.13 (Visualizza Promozioni) secondo i diagrammi di sequenza: endpoint `GET /tariffe` e `GET /promozioni`, stack completo Controller→BLL→DAL, drawer tariffe/promozioni nella VistaMappa.

**Architecture:** Controller dedicato `pricing_controller.py` (path `/tariffe` e `/promozioni`) → `ServizioPricing` BLL → `TariffaRepository` / `PromozioneRepository` DAL. I repository restituiscono `dict` (pattern del codebase). Frontend: due bottoni flottanti nella `VistaMappa` esistente aprono un drawer laterale lazy-loaded.

**Tech Stack:** FastAPI, SQLAlchemy 2.0, Pydantic v2, pytest + unittest.mock, React 19 + TypeScript, Axios.

**Spec:** `docs/superpowers/specs/2026-06-01-tariffe-promozioni-design.md`

---

## File Map

### Backend — nuovi file
- `backend/migrations/002_promozioni.sql` — DDL per la tabella `promozioni`
- `backend/model/promozione.py` — ORM SQLAlchemy 2.0 per `Promozione`
- `backend/dal/tariffa_repository.py` — `TariffaRepository.findAll()`  restituisce `list[dict]`
- `backend/dal/promozione_repository.py` — `PromozioneRepository.getAttive()` restituisce `list[dict]`
- `backend/controllers/pricing_controller.py` — `GET /tariffe`, `GET /promozioni`
- `backend/tests/test_pricing.py` — unit test BLL e controller

### Backend — file modificati
- `backend/bll/servizio_pricing.py` — implementa `getTariffe()` e `getPromozioniAttive()`
- `backend/controllers/schemas.py` — aggiunge `TariffaOut`, `PromozioneOut`
- `backend/main.py` — registra `pricing_router`

### Frontend — file modificati
- `frontend/src/services/PaymentService.ts` — aggiunge interfacce + `getTariffe()`, `getPromozioni()`
- `frontend/src/views/utente/VistaMappa.tsx` — stato drawer + bottoni + render drawer
- `frontend/src/views/utente/VistaMappa.css` — stile drawer

---

## Task 1: Migrazione DB + Model Promozione

**Files:**
- Create: `backend/migrations/002_promozioni.sql`
- Create: `backend/model/promozione.py`

- [ ] **Step 1.1: Scrivi la migrazione SQL**

Crea `backend/migrations/002_promozioni.sql`:

```sql
-- [IF-UT.13] Tabella promozioni — Sprint 1
CREATE TABLE promozioni (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titolo              TEXT NOT NULL,
    descrizione         TEXT,
    sconto_percentuale  NUMERIC(5,2) NOT NULL
                            CHECK (sconto_percentuale > 0 AND sconto_percentuale <= 100),
    data_inizio         TIMESTAMPTZ NOT NULL DEFAULT now(),
    data_fine           TIMESTAMPTZ NOT NULL,
    attiva              BOOLEAN NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT promozione_date_valide CHECK (data_fine > data_inizio)
);
```

- [ ] **Step 1.2: Esegui la migrazione su Supabase**

Vai su Supabase → SQL Editor, incolla il contenuto di `002_promozioni.sql` ed esegui.

Verifica: nella sezione Table Editor compare la tabella `promozioni` con le colonne: `id`, `titolo`, `descrizione`, `sconto_percentuale`, `data_inizio`, `data_fine`, `attiva`, `created_at`.

- [ ] **Step 1.3: Scrivi il test del model**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
def test_promozione_tablename():
    from model.promozione import Promozione
    assert Promozione.__tablename__ == "promozioni"


def test_promozione_columns():
    from model.promozione import Promozione
    cols = {c.name for c in Promozione.__table__.columns}
    assert cols == {
        "id", "titolo", "descrizione", "sconto_percentuale",
        "data_inizio", "data_fine", "attiva", "created_at",
    }


def test_promozione_check_constraints():
    from model.promozione import Promozione
    nomi = {c.name for c in Promozione.__table__.constraints}
    assert "promozione_sconto_valido" in nomi
    assert "promozione_date_valide" in nomi
```

- [ ] **Step 1.4: Esegui il test — verificane il fallimento**

```bash
cd backend && uv run pytest tests/test_schema.py::test_promozione_tablename -v
```

Output atteso: `ImportError` — il model non esiste ancora.

- [ ] **Step 1.5: Crea il model ORM**

Crea `backend/model/promozione.py`:

```python
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Text, Boolean, Numeric, DateTime, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Promozione(Base):
    __tablename__ = "promozioni"
    __table_args__ = (
        CheckConstraint(
            "sconto_percentuale > 0 AND sconto_percentuale <= 100",
            name="promozione_sconto_valido",
        ),
        CheckConstraint(
            "data_fine > data_inizio",
            name="promozione_date_valide",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    titolo: Mapped[str] = mapped_column(Text, nullable=False)
    descrizione: Mapped[str | None] = mapped_column(Text, nullable=True)
    sconto_percentuale: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    data_inizio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    data_fine: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    attiva: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
```

- [ ] **Step 1.6: Esegui i test del model**

```bash
cd backend && uv run pytest tests/test_schema.py::test_promozione_tablename tests/test_schema.py::test_promozione_columns tests/test_schema.py::test_promozione_check_constraints -v
```

Output atteso: tutti e 3 `PASSED`.

- [ ] **Step 1.7: Commit**

```bash
git add backend/migrations/002_promozioni.sql backend/model/promozione.py backend/tests/test_schema.py
git commit -m "feat: model Promozione + migrazione 002 [IF-UT.13]"
```

---

## Task 2: TariffaRepository (DAL)

**Files:**
- Create: `backend/dal/tariffa_repository.py`
- Create: `backend/tests/test_pricing.py`

Il repository restituisce `list[dict]` — pattern usato in tutto il codebase (vedere `MezzoRepository`).

- [ ] **Step 2.1: Scrivi il test del repository**

Crea `backend/tests/test_pricing.py`:

```python
import pytest
import unittest.mock
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import uuid


# ── Task 2: TariffaRepository ─────────────────────────────────────────────────

class TestTariffaRepository:

    def test_findAll_importabile(self):
        from dal.tariffa_repository import TariffaRepository
        assert hasattr(TariffaRepository, "findAll")

    def test_findAll_restituisce_lista_di_dict(self):
        from dal.tariffa_repository import TariffaRepository
        from model.tariffa import Tariffa, TipoMezzo as TMezzo

        row = MagicMock(spec=Tariffa)
        row.id = uuid.uuid4()
        row.tipo_mezzo = TMezzo.monopattino
        row.costo_al_minuto = Decimal("0.05")
        row.costo_al_km = Decimal("0.10")

        db = MagicMock()
        db.query.return_value.all.return_value = [row]

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["tipo_mezzo"] == "monopattino"
        assert result[0]["costo_al_minuto"] == "0.0500"

    def test_findAll_lista_vuota(self):
        from dal.tariffa_repository import TariffaRepository

        db = MagicMock()
        db.query.return_value.all.return_value = []

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert result == []
```

- [ ] **Step 2.2: Esegui il test — verificane il fallimento**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestTariffaRepository -v
```

Output atteso: `ImportError: cannot import name 'TariffaRepository'`.

- [ ] **Step 2.3: Crea TariffaRepository**

Crea `backend/dal/tariffa_repository.py`:

```python
from sqlalchemy.orm import Session
from model.tariffa import Tariffa


class TariffaRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    # [IF-UT.05]
    def findAll(self) -> list[dict]:
        rows = self._db.query(Tariffa).all()
        return [
            {
                "id": str(r.id),
                "tipo_mezzo": r.tipo_mezzo.value,
                "costo_al_minuto": str(r.costo_al_minuto),
                "costo_al_km": str(r.costo_al_km),
            }
            for r in rows
        ]
```

- [ ] **Step 2.4: Esegui il test — verificane il passaggio**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestTariffaRepository -v
```

Output atteso: tutti e 3 `PASSED`.

- [ ] **Step 2.5: Commit**

```bash
git add backend/dal/tariffa_repository.py backend/tests/test_pricing.py
git commit -m "feat: TariffaRepository.findAll() [IF-UT.05]"
```

---

## Task 3: PromozioneRepository (DAL)

**Files:**
- Create: `backend/dal/promozione_repository.py`
- Modify: `backend/tests/test_pricing.py`

- [ ] **Step 3.1: Aggiungi i test del repository**

Aggiungi in fondo a `backend/tests/test_pricing.py`:

```python
# ── Task 3: PromozioneRepository ─────────────────────────────────────────────

class TestPromozioneRepository:

    def test_getAttive_importabile(self):
        from dal.promozione_repository import PromozioneRepository
        assert hasattr(PromozioneRepository, "getAttive")

    def test_getAttive_restituisce_lista_di_dict(self):
        from dal.promozione_repository import PromozioneRepository
        from model.promozione import Promozione

        scadenza = datetime.now(tz=timezone.utc) + timedelta(days=7)

        row = MagicMock(spec=Promozione)
        row.id = uuid.uuid4()
        row.titolo = "Prima corsa gratis"
        row.descrizione = "Solo nuovi utenti"
        row.sconto_percentuale = Decimal("100")
        row.data_fine = scadenza

        db = MagicMock()
        db.query.return_value.filter.return_value.all.return_value = [row]

        repo = PromozioneRepository(db)
        result = repo.getAttive()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["titolo"] == "Prima corsa gratis"
        assert result[0]["sconto_percentuale"] == "100.00"

    def test_getAttive_lista_vuota(self):
        from dal.promozione_repository import PromozioneRepository

        db = MagicMock()
        db.query.return_value.filter.return_value.all.return_value = []

        repo = PromozioneRepository(db)
        result = repo.getAttive()

        assert result == []
```

- [ ] **Step 3.2: Esegui il test — verificane il fallimento**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestPromozioneRepository -v
```

Output atteso: `ImportError: cannot import name 'PromozioneRepository'`.

- [ ] **Step 3.3: Crea PromozioneRepository**

Crea `backend/dal/promozione_repository.py`:

```python
from sqlalchemy import func
from sqlalchemy.orm import Session
from model.promozione import Promozione


class PromozioneRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    # [IF-UT.13] — promozioni con attiva=True e data_fine >= adesso
    def getAttive(self) -> list[dict]:
        rows = (
            self._db.query(Promozione)
            .filter(
                Promozione.attiva.is_(True),
                Promozione.data_fine >= func.now(),
            )
            .all()
        )
        return [
            {
                "id": str(r.id),
                "titolo": r.titolo,
                "descrizione": r.descrizione,
                "sconto_percentuale": str(r.sconto_percentuale),
                "data_fine": r.data_fine.isoformat(),
            }
            for r in rows
        ]
```

- [ ] **Step 3.4: Esegui il test — verificane il passaggio**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestPromozioneRepository -v
```

Output atteso: tutti e 3 `PASSED`.

- [ ] **Step 3.5: Commit**

```bash
git add backend/dal/promozione_repository.py backend/tests/test_pricing.py
git commit -m "feat: PromozioneRepository.getAttive() [IF-UT.13]"
```

---

## Task 4: ServizioPricing (BLL)

**Files:**
- Modify: `backend/bll/servizio_pricing.py`
- Modify: `backend/tests/test_pricing.py`

- [ ] **Step 4.1: Aggiungi i test del servizio**

Aggiungi in fondo a `backend/tests/test_pricing.py`:

```python
# ── Task 4: ServizioPricing ──────────────────────────────────────────────────

class TestServizioPricing:

    def test_getTariffe_delega_al_repository(self):
        from bll.servizio_pricing import ServizioPricing

        tariffa_dict = {
            "id": str(uuid.uuid4()),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": "0.0500",
            "costo_al_km": "0.1000",
        }
        db = MagicMock()

        with patch("bll.servizio_pricing.TariffaRepository") as MockRepo:
            MockRepo.return_value.findAll.return_value = [tariffa_dict]
            svc = ServizioPricing(db)
            result = svc.getTariffe()

        MockRepo.assert_called_once_with(db)
        MockRepo.return_value.findAll.assert_called_once()
        assert result == [tariffa_dict]

    def test_getTariffe_lista_vuota(self):
        from bll.servizio_pricing import ServizioPricing

        db = MagicMock()
        with patch("bll.servizio_pricing.TariffaRepository") as MockRepo:
            MockRepo.return_value.findAll.return_value = []
            result = ServizioPricing(db).getTariffe()

        assert result == []

    def test_getPromozioniAttive_delega_al_repository(self):
        from bll.servizio_pricing import ServizioPricing

        promo_dict = {
            "id": str(uuid.uuid4()),
            "titolo": "Prima corsa gratis",
            "descrizione": None,
            "sconto_percentuale": "100.00",
            "data_fine": (datetime.now(tz=timezone.utc) + timedelta(days=7)).isoformat(),
        }
        db = MagicMock()

        with patch("bll.servizio_pricing.PromozioneRepository") as MockRepo:
            MockRepo.return_value.getAttive.return_value = [promo_dict]
            svc = ServizioPricing(db)
            result = svc.getPromozioniAttive()

        MockRepo.assert_called_once_with(db)
        MockRepo.return_value.getAttive.assert_called_once()
        assert result == [promo_dict]

    def test_getPromozioniAttive_lista_vuota(self):
        from bll.servizio_pricing import ServizioPricing

        db = MagicMock()
        with patch("bll.servizio_pricing.PromozioneRepository") as MockRepo:
            MockRepo.return_value.getAttive.return_value = []
            result = ServizioPricing(db).getPromozioniAttive()

        assert result == []
```

- [ ] **Step 4.2: Esegui il test — verificane il fallimento**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestServizioPricing -v
```

Output atteso: test falliscono — `ServizioPricing` non ha ancora `getTariffe`/`getPromozioniAttive`.

- [ ] **Step 4.3: Implementa ServizioPricing**

Sovrascrivi `backend/bll/servizio_pricing.py`:

```python
from sqlalchemy.orm import Session
from dal.tariffa_repository import TariffaRepository
from dal.promozione_repository import PromozioneRepository


class ServizioPricing:
    """Calcolo tariffe, promozioni e addebiti a fine corsa."""

    def __init__(self, db: Session) -> None:
        self._tariffa_repo = TariffaRepository(db)
        self._promozione_repo = PromozioneRepository(db)

    # [IF-UT.05]
    def getTariffe(self) -> list[dict]:
        return self._tariffa_repo.findAll()

    # [IF-UT.13]
    def getPromozioniAttive(self) -> list[dict]:
        return self._promozione_repo.getAttive()
```

- [ ] **Step 4.4: Esegui il test — verificane il passaggio**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestServizioPricing -v
```

Output atteso: tutti e 4 `PASSED`.

- [ ] **Step 4.5: Commit**

```bash
git add backend/bll/servizio_pricing.py backend/tests/test_pricing.py
git commit -m "feat: ServizioPricing getTariffe + getPromozioniAttive [IF-UT.05, IF-UT.13]"
```

---

## Task 5: Schemas Pydantic + pricing_controller

**Files:**
- Modify: `backend/controllers/schemas.py`
- Create: `backend/controllers/pricing_controller.py`
- Modify: `backend/tests/test_pricing.py`

**Nota sugli auth test**: `verify_token(["UT"])` è una factory che ritorna una nuova closure ad ogni chiamata. Per poter usare `app.dependency_overrides` nei test, il controller definisce `_auth_utente = verify_token(["UT"])` a livello di modulo — così i test importano esattamente lo stesso oggetto callable usato nelle route.

- [ ] **Step 5.1: Aggiungi gli schemas Pydantic**

Apri `backend/controllers/schemas.py`. Aggiungi questi import in testa (se non già presenti):

```python
from decimal import Decimal
from datetime import datetime
```

Aggiungi in fondo al file:

```python
class TariffaOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    costo_al_minuto: str
    costo_al_km: str


class PromozioneOut(BaseModel):
    id: UUID
    titolo: str
    descrizione: str | None
    sconto_percentuale: str
    data_fine: str
```

Nota: i campi `Decimal` sono serializzati come `str` dai repository — il frontend li riceve come stringhe e li converte con `parseFloat()`.

- [ ] **Step 5.2: Scrivi i test del controller**

Aggiungi in fondo a `backend/tests/test_pricing.py`:

```python
# ── Task 5: PricingController ────────────────────────────────────────────────

class TestPricingController:
    """
    Usa dependency_overrides con _auth_utente importata dal controller.
    Vedere nota in Task 5 del piano.
    """

    def _make_client(self, tariffe=None, promozioni=None):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from controllers.pricing_controller import router, _auth_utente
        from database import get_db

        app = FastAPI()
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[_auth_utente] = lambda: {
            "id": str(uuid.uuid4()), "ruolo": "UT"
        }
        app.include_router(router)
        return TestClient(app)

    def test_get_tariffe_200(self):
        from controllers.pricing_controller import router, _auth_utente
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from database import get_db

        tariffa = {
            "id": str(uuid.uuid4()),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": "0.0500",
            "costo_al_km": "0.1000",
        }

        app = FastAPI()
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[_auth_utente] = lambda: {"id": str(uuid.uuid4()), "ruolo": "UT"}
        app.include_router(router)

        with patch("controllers.pricing_controller.ServizioPricing") as MockSvc:
            MockSvc.return_value.getTariffe.return_value = [tariffa]
            r = TestClient(app).get("/tariffe")

        assert r.status_code == 200
        body = r.json()
        assert len(body) == 1
        assert body[0]["tipo_mezzo"] == "monopattino"

    def test_get_tariffe_404_quando_vuoto(self):
        from controllers.pricing_controller import router, _auth_utente
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from database import get_db

        app = FastAPI()
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[_auth_utente] = lambda: {"id": str(uuid.uuid4()), "ruolo": "UT"}
        app.include_router(router)

        with patch("controllers.pricing_controller.ServizioPricing") as MockSvc:
            MockSvc.return_value.getTariffe.return_value = []
            r = TestClient(app).get("/tariffe")

        assert r.status_code == 404

    def test_get_promozioni_200(self):
        from controllers.pricing_controller import router, _auth_utente
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from database import get_db

        promo = {
            "id": str(uuid.uuid4()),
            "titolo": "Prova gratis",
            "descrizione": "Prima corsa gratis",
            "sconto_percentuale": "100.00",
            "data_fine": (datetime.now(tz=timezone.utc) + timedelta(days=30)).isoformat(),
        }

        app = FastAPI()
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[_auth_utente] = lambda: {"id": str(uuid.uuid4()), "ruolo": "UT"}
        app.include_router(router)

        with patch("controllers.pricing_controller.ServizioPricing") as MockSvc:
            MockSvc.return_value.getPromozioniAttive.return_value = [promo]
            r = TestClient(app).get("/promozioni")

        assert r.status_code == 200
        body = r.json()
        assert len(body) == 1
        assert body[0]["titolo"] == "Prova gratis"

    def test_get_promozioni_204_quando_vuoto(self):
        from controllers.pricing_controller import router, _auth_utente
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from database import get_db

        app = FastAPI()
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[_auth_utente] = lambda: {"id": str(uuid.uuid4()), "ruolo": "UT"}
        app.include_router(router)

        with patch("controllers.pricing_controller.ServizioPricing") as MockSvc:
            MockSvc.return_value.getPromozioniAttive.return_value = []
            r = TestClient(app).get("/promozioni")

        assert r.status_code == 204
```

- [ ] **Step 5.3: Esegui il test — verificane il fallimento**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestPricingController -v
```

Output atteso: `ImportError: cannot import name 'router' from 'controllers.pricing_controller'`.

- [ ] **Step 5.4: Crea pricing_controller.py**

Crea `backend/controllers/pricing_controller.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, Response
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_pricing import ServizioPricing
from controllers.schemas import TariffaOut, PromozioneOut

router = APIRouter(tags=["Pricing"])

# Variabile a livello modulo: permette dependency_overrides nei test
_auth_utente = verify_token(["UT"])


# [IF-UT.05] Consulta Tariffe
@router.get("/tariffe", response_model=list[TariffaOut])
def get_tariffe(
    utente=Depends(_auth_utente),
    db=Depends(get_db),
):
    tariffe = ServizioPricing(db).getTariffe()
    if not tariffe:
        raise HTTPException(status_code=404, detail="Nessuna tariffa disponibile.")
    return tariffe


# [IF-UT.13] Visualizza Promozioni
@router.get("/promozioni", status_code=200)
def get_promozioni(
    response: Response,
    utente=Depends(_auth_utente),
    db=Depends(get_db),
):
    promozioni = ServizioPricing(db).getPromozioniAttive()
    if not promozioni:
        response.status_code = 204
        return None
    return promozioni
```

- [ ] **Step 5.5: Esegui il test — verificane il passaggio**

```bash
cd backend && uv run pytest tests/test_pricing.py::TestPricingController -v
```

Output atteso: tutti e 4 `PASSED`.

- [ ] **Step 5.6: Commit**

```bash
git add backend/controllers/schemas.py backend/controllers/pricing_controller.py backend/tests/test_pricing.py
git commit -m "feat: pricing_controller GET /tariffe GET /promozioni + schemas [IF-UT.05, IF-UT.13]"
```

---

## Task 6: Registra router in main.py

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 6.1: Aggiungi l'import e la registrazione**

Apri `backend/main.py`. Aggiungi dopo l'ultima riga di import:

```python
from controllers.pricing_controller import router as pricing_router
```

Aggiungi dopo l'ultima riga `app.include_router(...)`:

```python
app.include_router(pricing_router)
```

- [ ] **Step 6.2: Avvia il backend e verifica gli endpoint**

```bash
cd backend && uv run uvicorn main:app --reload
```

Apri `http://localhost:8000/docs`. Verifica che compaiano:
- `GET /tariffe` nel gruppo "Pricing"
- `GET /promozioni` nel gruppo "Pricing"

- [ ] **Step 6.3: Esegui tutti i test unitari**

```bash
cd backend && uv run pytest tests/ -v -m "not integration"
```

Output atteso: zero `FAILED`.

- [ ] **Step 6.4: Commit**

```bash
git add backend/main.py
git commit -m "feat: registra pricing_router in main.py [IF-UT.05, IF-UT.13]"
```

---

## Task 7: Frontend — PaymentService.ts

**Files:**
- Modify: `frontend/src/services/PaymentService.ts`

- [ ] **Step 7.1: Aggiungi interfacce e funzioni**

Apri `frontend/src/services/PaymentService.ts`. Aggiungi prima delle esportazioni esistenti:

```typescript
// [IF-UT.05]
export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: string
  costo_al_km: string
}

// [IF-UT.13]
export interface Promozione {
  id: string
  titolo: string
  descrizione: string | null
  sconto_percentuale: string
  data_fine: string
}
```

Aggiungi in fondo al file:

```typescript
// [IF-UT.05] Consulta Tariffe
export const getTariffe = () => api.get<Tariffa[]>('/tariffe')

// [IF-UT.13] Visualizza Promozioni — 204 No Content se nessuna promozione attiva
export const getPromozioni = () => api.get<Promozione[]>('/promozioni')
```

- [ ] **Step 7.2: Verifica la build TypeScript**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

Output atteso: build completata senza errori TypeScript.

- [ ] **Step 7.3: Commit**

```bash
git add frontend/src/services/PaymentService.ts
git commit -m "feat: getTariffe + getPromozioni in PaymentService [IF-UT.05, IF-UT.13]"
```

---

## Task 8: Frontend — Drawer tariffe/promozioni in VistaMappa

**Files:**
- Modify: `frontend/src/views/utente/VistaMappa.tsx`
- Modify: `frontend/src/views/utente/VistaMappa.css`

- [ ] **Step 8.1: Aggiungi gli import**

Apri `frontend/src/views/utente/VistaMappa.tsx`. Nella sezione import, aggiungi:

```typescript
import { getTariffe, getPromozioni, type Tariffa, type Promozione } from '../../services/PaymentService'
```

- [ ] **Step 8.2: Aggiungi lo stato del drawer**

Nella funzione `VistaMappa()`, dopo la riga `const zoneAttive = useRef(...)` (attorno alla riga 96), aggiungi:

```typescript
  // [IF-UT.05] [IF-UT.13] Stato drawer tariffe/promozioni
  const [drawerAperto, setDrawerAperto] = useState<'tariffe' | 'promozioni' | null>(null)
  const [tariffe, setTariffe] = useState<Tariffa[] | null>(null)
  const [promozioni, setPromozioni] = useState<Promozione[] | null>(null)
  const [loadingDrawer, setLoadingDrawer] = useState(false)
  const [erroreDrawer, setErroreDrawer] = useState('')
```

- [ ] **Step 8.3: Aggiungi gli handler del drawer**

Dopo `const handleLogout = useCallback(...)`, aggiungi:

```typescript
  // [IF-UT.05] — fetch lazy, apre drawer tariffe
  const apriTariffe = useCallback(async () => {
    setDrawerAperto('tariffe')
    if (tariffe !== null) return
    setLoadingDrawer(true)
    setErroreDrawer('')
    try {
      const r = await getTariffe()
      setTariffe(r.data)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 404) {
        setTariffe([])
      } else {
        setErroreDrawer('Impossibile caricare le tariffe.')
      }
    } finally {
      setLoadingDrawer(false)
    }
  }, [tariffe])

  // [IF-UT.13] — fetch lazy, apre drawer promozioni
  const apriPromozioni = useCallback(async () => {
    setDrawerAperto('promozioni')
    if (promozioni !== null) return
    setLoadingDrawer(true)
    setErroreDrawer('')
    try {
      const r = await getPromozioni()
      setPromozioni(r.data ?? [])
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 204) {
        setPromozioni([])
      } else {
        setErroreDrawer('Impossibile caricare le promozioni.')
      }
    } finally {
      setLoadingDrawer(false)
    }
  }, [promozioni])

  const chiudiDrawer = useCallback(() => {
    setDrawerAperto(null)
    setErroreDrawer('')
  }, [])
```

- [ ] **Step 8.4: Aggiungi il render del drawer nel JSX**

Nel blocco `return`, immediatamente prima di `{errore && <div className="mappa-errore">...}` (ultima riga del JSX, prima di `</div>`), aggiungi:

```tsx
      {/* [IF-UT.05][IF-UT.13] Bottoni flottanti tariffe/promozioni */}
      <div className="pricing-fab-gruppo">
        <button type="button" className="pricing-fab" onClick={apriTariffe}>
          Tariffe
        </button>
        <button type="button" className="pricing-fab pricing-fab--promo" onClick={apriPromozioni}>
          Promo
        </button>
      </div>

      {/* Drawer laterale tariffe/promozioni */}
      {drawerAperto && (
        <div className="pricing-drawer" role="dialog" aria-modal="true">
          <div className="pricing-drawer__header">
            <span className="pricing-drawer__titolo">
              {drawerAperto === 'tariffe' ? 'Tariffe del servizio' : 'Promozioni attive'}
            </span>
            <button
              type="button"
              className="pricing-drawer__chiudi"
              onClick={chiudiDrawer}
              aria-label="Chiudi pannello"
            >
              ✕
            </button>
          </div>

          <div className="pricing-drawer__body">
            {loadingDrawer && <p className="pricing-stato">Caricamento...</p>}
            {erroreDrawer && <p className="pricing-stato pricing-stato--errore">{erroreDrawer}</p>}

            {!loadingDrawer && !erroreDrawer && drawerAperto === 'tariffe' && (
              tariffe && tariffe.length > 0 ? (
                <ul className="pricing-lista">
                  {tariffe.map(t => (
                    <li key={t.id} className="pricing-card">
                      <span className="pricing-card__tipo">
                        {t.tipo_mezzo === 'monopattino' ? '🛴'
                          : t.tipo_mezzo === 'bicicletta' ? '🚲' : '🚗'}{' '}
                        {t.tipo_mezzo.charAt(0).toUpperCase() + t.tipo_mezzo.slice(1)}
                      </span>
                      <span className="pricing-card__riga">
                        {parseFloat(t.costo_al_minuto).toFixed(2)} €/min
                      </span>
                      <span className="pricing-card__riga">
                        {parseFloat(t.costo_al_km).toFixed(2)} €/km
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="pricing-stato">Nessuna tariffa disponibile.</p>
              )
            )}

            {!loadingDrawer && !erroreDrawer && drawerAperto === 'promozioni' && (
              promozioni && promozioni.length > 0 ? (
                <ul className="pricing-lista">
                  {promozioni.map(p => (
                    <li key={p.id} className="pricing-card pricing-card--promo">
                      <span className="pricing-card__tipo">{p.titolo}</span>
                      {p.descrizione && (
                        <span className="pricing-card__riga">{p.descrizione}</span>
                      )}
                      <span className="pricing-card__riga pricing-card__sconto">
                        -{parseFloat(p.sconto_percentuale).toFixed(0)}%
                      </span>
                      <span className="pricing-card__riga pricing-card__scadenza">
                        Fino al {new Date(p.data_fine).toLocaleDateString('it-IT')}
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="pricing-stato">Nessuna promozione attiva al momento.</p>
              )
            )}
          </div>
        </div>
      )}
```

- [ ] **Step 8.5: Aggiungi gli stili CSS**

Apri `frontend/src/views/utente/VistaMappa.css`. Aggiungi in fondo al file:

```css
/* ---------- [IF-UT.05][IF-UT.13] Pricing FAB (bottoni flottanti) ---------- */
.pricing-fab-gruppo {
  position: absolute;
  bottom: 32px;
  left: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 10;
}

.pricing-fab {
  padding: 10px 20px;
  background: white;
  color: var(--sm-primary);
  border: 2px solid var(--sm-primary);
  border-radius: var(--sm-radius);
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  box-shadow: var(--sm-shadow-md);
  transition: background 0.15s, color 0.15s;
}

.pricing-fab:hover {
  background: var(--sm-primary);
  color: white;
}

.pricing-fab--promo {
  border-color: var(--sm-accent);
  color: var(--sm-primary-700);
}

.pricing-fab--promo:hover {
  background: var(--sm-accent);
  color: white;
  border-color: var(--sm-accent);
}

/* ---------- Pricing Drawer ---------- */
.pricing-drawer {
  position: absolute;
  top: 88px;
  left: 0;
  bottom: 0;
  width: 320px;
  max-width: 90vw;
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(8px);
  box-shadow: var(--sm-shadow-lg);
  display: flex;
  flex-direction: column;
  z-index: 20;
  border-right: 1px solid var(--sm-line);
}

.pricing-drawer__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--sm-line);
}

.pricing-drawer__titolo {
  font-weight: 700;
  font-size: 15px;
  color: var(--sm-dark);
}

.pricing-drawer__chiudi {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--sm-muted);
  line-height: 1;
  padding: 0 4px;
}

.pricing-drawer__chiudi:hover { color: var(--sm-dark); }

.pricing-drawer__body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* ---------- Pricing Lista card ---------- */
.pricing-lista {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pricing-card {
  background: #f8fafc;
  border: 1px solid var(--sm-line);
  border-radius: var(--sm-radius);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pricing-card--promo {
  border-color: rgba(6, 214, 160, 0.4);
  background: rgba(6, 214, 160, 0.05);
}

.pricing-card__tipo {
  font-weight: 700;
  font-size: 14px;
  color: var(--sm-dark);
}

.pricing-card__riga {
  font-size: 13px;
  color: var(--sm-muted);
}

.pricing-card__sconto {
  font-weight: 700;
  font-size: 16px;
  color: var(--sm-primary);
}

.pricing-card__scadenza {
  font-size: 12px;
  color: var(--sm-muted);
}

/* ---------- Stato (loading / errore / vuoto) ---------- */
.pricing-stato {
  font-size: 14px;
  color: var(--sm-muted);
  padding: 8px 0;
}

.pricing-stato--errore { color: var(--sm-error); }
```

- [ ] **Step 8.6: Verifica la build TypeScript**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

Output atteso: build completata senza errori TypeScript.

- [ ] **Step 8.7: Test manuale**

```bash
# Terminale 1
cd backend && uv run uvicorn main:app --reload

# Terminale 2
cd frontend && npm run dev
```

Apri `http://localhost:5173`, fai login come utente (UT). Verifica:
1. Compaiono i bottoni "Tariffe" e "Promo" in basso a sinistra della mappa
2. Click su "Tariffe" → drawer si apre con la lista tariffe (oppure "Nessuna tariffa disponibile.")
3. Click su "Promo" → drawer mostra promozioni attive (oppure "Nessuna promozione attiva al momento.")
4. Il bottone ✕ chiude il drawer
5. Un secondo click su "Tariffe" non genera una nuova chiamata HTTP (la lista è già in stato)

- [ ] **Step 8.8: Commit**

```bash
git add frontend/src/views/utente/VistaMappa.tsx frontend/src/views/utente/VistaMappa.css
git commit -m "feat: drawer tariffe/promozioni in VistaMappa [IF-UT.05, IF-UT.13]"
```

---

## Task 9: Esegui tutti i test + verifica finale

- [ ] **Step 9.1: Esegui tutti i test unitari backend**

```bash
cd backend && uv run pytest tests/ -v -m "not integration"
```

Output atteso: zero `FAILED`. Se ci sono fallimenti, correggerli prima di procedere.

- [ ] **Step 9.2: Verifica TypeScript frontend**

```bash
cd frontend && npm run build
```

Output atteso: build senza errori TypeScript.

- [ ] **Step 9.3: Commit finale se ci sono modifiche**

```bash
git status
```

Se ci sono file non committati relativi a questi item:

```bash
git add <file rilevanti>
git commit -m "chore: pulizia finale tariffe/promozioni [IF-UT.05, IF-UT.13]"
```

---

## Note tecniche

- **`_auth_utente` a livello modulo**: `verify_token(["UT"])` restituisce una nuova closure ad ogni invocazione. Definirla a livello modulo garantisce che `app.dependency_overrides[_auth_utente]` nei test faccia match con esattamente lo stesso oggetto callable usato nelle route.
- **204 No Content**: FastAPI non serializza il body quando `response.status_code = 204` e si ritorna `None`. Il frontend gestisce il 204 impostando `promozioni = []`.
- **Repr Decimal come str**: sia `TariffaRepository` che `PromozioneRepository` serializzano `Decimal` come `str` (es. `"0.0500"`). Il frontend usa `parseFloat()` per la visualizzazione.
- **Fetch lazy nel frontend**: `if (tariffe !== null) return` garantisce che la chiamata HTTP avvenga una sola volta per sessione utente — nessun refetch ogni volta che si apre il drawer.
