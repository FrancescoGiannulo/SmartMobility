# Definisci Offerta — Implementation Plan (IF-OP.06)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permettere all'Operatore autenticato di creare e pubblicare offerte commerciali (Promozione o Abbonamento) con validazione e stato visibile nella UI.

**Architecture:** Layer standard Controller → BLL → DAL → DB. Una singola tabella `offerte` con colonna `tipo` discriminante. Il frontend espone una nuova vista `/operatore/tariffe-promozioni` raggiungibile dal pannello laterale della mappa operatore.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 + PostgreSQL (Supabase), React 19 + TypeScript + Axios, pytest per i test backend.

---

## File Structure

| File | Azione | Responsabilità |
|------|--------|----------------|
| `backend/migrations/004_offerte.sql` | Crea | DDL tabella `offerte` |
| `backend/model/offerta.py` | Crea | ORM SQLAlchemy `Offerta` |
| `backend/dal/offerta_repository.py` | Crea | CRUD offerte su DB |
| `backend/bll/servizio_offerte.py` | Crea | Validazione e logica di business |
| `backend/controllers/schemas.py` | Modifica | Aggiunge `CreaOffertaRequest`, `OffertaOut` |
| `backend/controllers/offerta_controller.py` | Crea | Endpoint REST `/operatore/offerte` |
| `backend/main.py` | Modifica | Registra `offerta_router` |
| `backend/tests/test_offerte.py` | Crea | Test integrazione scenari base + alternativi |
| `frontend/src/services/OffertaService.ts` | Crea | Chiamate API offerte |
| `frontend/src/views/operatore/VistaTariffePromozioni.tsx` | Crea | Vista lista + form nuova offerta |
| `frontend/src/views/operatore/VistaTariffePromozioni.css` | Crea | Stili vista |
| `frontend/src/App.tsx` | Modifica | Aggiunge rotta `/operatore/tariffe-promozioni` |
| `frontend/src/views/operatore/VistaMappaOperatore.tsx` | Modifica | Naviga a `/operatore/tariffe-promozioni` dal pulsante "Tariffe e promozioni" |

---

## Task 1: Migrazione DB — tabella `offerte`

**Files:**
- Crea: `backend/migrations/004_offerte.sql`

- [ ] **Step 1: Scrivi la migrazione SQL**

```sql
-- backend/migrations/004_offerte.sql
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_offerta') THEN
    CREATE TYPE tipo_offerta AS ENUM ('promozione', 'abbonamento');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stato_offerta') THEN
    CREATE TYPE stato_offerta AS ENUM ('bozza', 'attiva', 'scaduta');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS offerte (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome            TEXT NOT NULL,
    tipo            tipo_offerta NOT NULL,
    stato           stato_offerta NOT NULL DEFAULT 'attiva',
    descrizione     TEXT,
    -- campi promozione
    sconto_percentuale NUMERIC(5,2),
    -- campi abbonamento
    prezzo          NUMERIC(10,2),
    durata_giorni   INTEGER,
    -- date
    data_inizio     TIMESTAMPTZ,
    data_scadenza   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT offerte_nome_unico UNIQUE (nome),
    CONSTRAINT sconto_valido CHECK (sconto_percentuale IS NULL OR (sconto_percentuale > 0 AND sconto_percentuale <= 100)),
    CONSTRAINT prezzo_valido CHECK (prezzo IS NULL OR prezzo > 0),
    CONSTRAINT durata_valida CHECK (durata_giorni IS NULL OR durata_giorni > 0)
);
```

- [ ] **Step 2: Esegui la migrazione su Supabase**

Copia il contenuto del file e incollalo nell'editor SQL di Supabase → Run.
Verifica: `SELECT table_name FROM information_schema.tables WHERE table_name = 'offerte';` → ritorna una riga.

- [ ] **Step 3: Commit**

```bash
git add backend/migrations/004_offerte.sql
git commit -m "feat(db): aggiungi tabella offerte per IF-OP.06"
```

---

## Task 2: ORM Model `Offerta`

**Files:**
- Crea: `backend/model/offerta.py`

- [ ] **Step 1: Scrivi il model**

```python
# backend/model/offerta.py
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import Text, Numeric, Integer, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Offerta(Base):
    __tablename__ = "offerte"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    tipo: Mapped[str] = mapped_column(
        SAEnum("promozione", "abbonamento", name="tipo_offerta", create_type=False),
        nullable=False,
    )
    stato: Mapped[str] = mapped_column(
        SAEnum("bozza", "attiva", "scaduta", name="stato_offerta", create_type=False),
        nullable=False,
        server_default="attiva",
    )
    descrizione: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sconto_percentuale: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)
    prezzo: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    durata_giorni: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    data_inizio: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    data_scadenza: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 2: Commit**

```bash
git add backend/model/offerta.py
git commit -m "feat(model): ORM Offerta per IF-OP.06"
```

---

## Task 3: DAL `OffertaRepository`

**Files:**
- Crea: `backend/dal/offerta_repository.py`

- [ ] **Step 1: Scrivi il repository**

```python
# backend/dal/offerta_repository.py
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from model.offerta import Offerta


class NomeDuplicatoException(Exception):
    pass


class OffertaNonTrovataException(Exception):
    pass


class OffertaRepository:

    def lista(self, db: Session) -> list[Offerta]:
        return db.query(Offerta).order_by(Offerta.created_at.desc()).all()

    def trova_per_id(self, offerta_id: uuid.UUID, db: Session) -> Offerta:
        offerta = db.query(Offerta).filter(Offerta.id == offerta_id).first()
        if not offerta:
            raise OffertaNonTrovataException(f"Offerta {offerta_id} non trovata")
        return offerta

    def nome_esiste(self, nome: str, db: Session) -> bool:
        return db.query(Offerta).filter(Offerta.nome == nome).first() is not None

    def crea(
        self,
        nome: str,
        tipo: str,
        descrizione: Optional[str],
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_inizio: Optional[datetime],
        data_scadenza: Optional[datetime],
        db: Session,
    ) -> Offerta:
        if self.nome_esiste(nome, db):
            raise NomeDuplicatoException(f"Offerta con nome '{nome}' già esistente")
        offerta = Offerta(
            nome=nome,
            tipo=tipo,
            stato="attiva",
            descrizione=descrizione,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_inizio=data_inizio,
            data_scadenza=data_scadenza,
        )
        db.add(offerta)
        db.commit()
        db.refresh(offerta)
        return offerta

    def elimina(self, offerta_id: uuid.UUID, db: Session) -> None:
        offerta = self.trova_per_id(offerta_id, db)
        db.delete(offerta)
        db.commit()
```

- [ ] **Step 2: Commit**

```bash
git add backend/dal/offerta_repository.py
git commit -m "feat(dal): OffertaRepository per IF-OP.06"
```

---

## Task 4: BLL `ServizioOfferte`

**Files:**
- Crea: `backend/bll/servizio_offerte.py`

- [ ] **Step 1: Scrivi il servizio**

```python
# backend/bll/servizio_offerte.py
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from dal.offerta_repository import OffertaRepository, NomeDuplicatoException, OffertaNonTrovataException
from model.offerta import Offerta


class OffertaValidazioneException(Exception):
    pass


class OffertaDuplicataException(Exception):
    pass


class ServizioOfferte:

    def __init__(self) -> None:
        self._repo = OffertaRepository()

    def lista_offerte(self, db: Session) -> list[Offerta]:
        return self._repo.lista(db)

    def crea_offerta(
        self,
        nome: str,
        tipo: str,
        descrizione: Optional[str],
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_inizio: Optional[datetime],
        data_scadenza: Optional[datetime],
        db: Session,
    ) -> Offerta:
        self._valida(
            nome=nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_scadenza=data_scadenza,
        )
        try:
            return self._repo.crea(
                nome=nome,
                tipo=tipo,
                descrizione=descrizione,
                sconto_percentuale=sconto_percentuale,
                prezzo=prezzo,
                durata_giorni=durata_giorni,
                data_inizio=data_inizio,
                data_scadenza=data_scadenza,
                db=db,
            )
        except NomeDuplicatoException:
            raise OffertaDuplicataException(f"Esiste già un'offerta con nome '{nome}'")

    def elimina_offerta(self, offerta_id: uuid.UUID, db: Session) -> None:
        try:
            self._repo.elimina(offerta_id, db)
        except OffertaNonTrovataException:
            raise OffertaValidazioneException(f"Offerta {offerta_id} non trovata")

    def _valida(
        self,
        nome: str,
        tipo: str,
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_scadenza: Optional[datetime],
    ) -> None:
        if not nome or not nome.strip():
            raise OffertaValidazioneException("Il nome è obbligatorio")
        if tipo not in ("promozione", "abbonamento"):
            raise OffertaValidazioneException("Tipo non valido: usa 'promozione' o 'abbonamento'")
        if tipo == "promozione":
            if sconto_percentuale is None:
                raise OffertaValidazioneException("Lo sconto percentuale è obbligatorio per una promozione")
            if sconto_percentuale <= 0 or sconto_percentuale > 100:
                raise OffertaValidazioneException("Lo sconto deve essere compreso tra 0 e 100")
            if data_scadenza is None:
                raise OffertaValidazioneException("La data di scadenza è obbligatoria per una promozione")
            if data_scadenza <= datetime.now(timezone.utc):
                raise OffertaValidazioneException("La data di scadenza deve essere nel futuro")
        if tipo == "abbonamento":
            if prezzo is None:
                raise OffertaValidazioneException("Il prezzo è obbligatorio per un abbonamento")
            if prezzo <= 0:
                raise OffertaValidazioneException("Il prezzo deve essere maggiore di zero")
            if durata_giorni is None:
                raise OffertaValidazioneException("La durata in giorni è obbligatoria per un abbonamento")
            if durata_giorni <= 0:
                raise OffertaValidazioneException("La durata deve essere maggiore di zero")
```

- [ ] **Step 2: Commit**

```bash
git add backend/bll/servizio_offerte.py
git commit -m "feat(bll): ServizioOfferte con validazione per IF-OP.06"
```

---

## Task 5: Controller + Schemas

**Files:**
- Modifica: `backend/controllers/schemas.py`
- Crea: `backend/controllers/offerta_controller.py`
- Modifica: `backend/main.py`

- [ ] **Step 1: Aggiungi schemas in `schemas.py`**

Apri `backend/controllers/schemas.py` e aggiungi in fondo:

```python
from datetime import datetime
from decimal import Decimal

class CreaOffertaRequest(BaseModel):
    nome: str
    tipo: str  # 'promozione' | 'abbonamento'
    descrizione: str | None = None
    sconto_percentuale: Decimal | None = None
    prezzo: Decimal | None = None
    durata_giorni: int | None = None
    data_inizio: datetime | None = None
    data_scadenza: datetime | None = None


class OffertaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    stato: str
    descrizione: str | None
    sconto_percentuale: Decimal | None
    prezzo: Decimal | None
    durata_giorni: int | None
    data_inizio: datetime | None
    data_scadenza: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: Scrivi il controller**

```python
# backend/controllers/offerta_controller.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import CreaOffertaRequest, OffertaOut
from bll.servizio_offerte import ServizioOfferte, OffertaValidazioneException, OffertaDuplicataException

router = APIRouter(prefix="/operatore", tags=["Operatore - Offerte"])
_servizio = ServizioOfferte()


# [IF-OP.06] — lista offerte
@router.get("/offerte", response_model=list[OffertaOut])
def lista_offerte(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.lista_offerte(db)


# [IF-OP.06] — crea offerta
@router.post("/offerte", response_model=OffertaOut, status_code=201)
def crea_offerta(
    body: CreaOffertaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.crea_offerta(
            nome=body.nome,
            tipo=body.tipo,
            descrizione=body.descrizione,
            sconto_percentuale=body.sconto_percentuale,
            prezzo=body.prezzo,
            durata_giorni=body.durata_giorni,
            data_inizio=body.data_inizio,
            data_scadenza=body.data_scadenza,
            db=db,
        )
    except OffertaDuplicataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.06] — elimina offerta
@router.delete("/offerte/{offerta_id}", status_code=204)
def elimina_offerta(
    offerta_id: uuid.UUID,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        _servizio.elimina_offerta(offerta_id, db)
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=404, detail=str(e))
```

- [ ] **Step 3: Registra il router in `main.py`**

Aggiungi in `backend/main.py`:
```python
from controllers.offerta_controller import router as offerta_router
# ...
app.include_router(offerta_router)
```

- [ ] **Step 4: Verifica che il backend si avvii e le route siano presenti**

```bash
cd backend && uv run python -c "from main import app; [print(r.path) for r in app.routes if 'offert' in r.path]"
```

Output atteso:
```
/operatore/offerte
/operatore/offerte
/operatore/offerte/{offerta_id}
```

- [ ] **Step 5: Commit**

```bash
git add backend/controllers/schemas.py backend/controllers/offerta_controller.py backend/main.py
git commit -m "feat(api): endpoint offerte operatore [IF-OP.06]"
```

---

## Task 6: Test Backend

**Files:**
- Crea: `backend/tests/test_offerte.py`

- [ ] **Step 1: Scrivi i test**

```python
# backend/tests/test_offerte.py
"""[IF-OP.06] Test Definisce Offerta — scenari base e alternativi."""
import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _domani() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()


def _ieri() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()


# ── Scenario base: lista offerte ─────────────────────────────────────────────

def test_lista_offerte_operatore_autenticato(operatore_test):
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/offerte", headers=_auth(token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_lista_offerte_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/operatore/offerte")
    assert resp.status_code == 401


# ── Scenario base: crea promozione ───────────────────────────────────────────

def test_crea_promozione_valida(operatore_test):
    """[IF-OP.06] Crea promozione con sconto e scadenza futura → 201."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Black Friday 2026",
        "tipo": "promozione",
        "descrizione": "Sconto del 20% su tutte le corse",
        "sconto_percentuale": 20.0,
        "data_scadenza": _domani(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == "Black Friday 2026"
    assert body["tipo"] == "promozione"
    assert body["stato"] == "attiva"
    assert float(body["sconto_percentuale"]) == 20.0
    # cleanup
    http.delete(f"/operatore/offerte/{body['id']}", headers=_auth(token))


# ── Scenario base: crea abbonamento ──────────────────────────────────────────

def test_crea_abbonamento_valido(operatore_test):
    """[IF-OP.06] Crea abbonamento con prezzo e durata → 201."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Abbonamento Mensile",
        "tipo": "abbonamento",
        "descrizione": "30 giorni illimitati",
        "prezzo": 29.99,
        "durata_giorni": 30,
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 201
    body = resp.json()
    assert body["tipo"] == "abbonamento"
    assert float(body["prezzo"]) == 29.99
    assert body["durata_giorni"] == 30
    # cleanup
    http.delete(f"/operatore/offerte/{body['id']}", headers=_auth(token))


# ── Scenario alternativo: nome duplicato → 409 ───────────────────────────────

def test_crea_offerta_nome_duplicato(operatore_test):
    """[IF-OP.06] Nome già esistente → 409."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Offerta Unica Dup Test",
        "tipo": "promozione",
        "sconto_percentuale": 10.0,
        "data_scadenza": _domani(),
    }
    resp1 = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp1.status_code == 201
    resp2 = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp2.status_code == 409
    # cleanup
    http.delete(f"/operatore/offerte/{resp1.json()['id']}", headers=_auth(token))


# ── Scenario alternativo: scadenza nel passato → 422 ─────────────────────────

def test_crea_promozione_scadenza_passata(operatore_test):
    """[IF-OP.06] Data scadenza nel passato → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Offerta Scaduta",
        "tipo": "promozione",
        "sconto_percentuale": 10.0,
        "data_scadenza": _ieri(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Scenario alternativo: sconto non valido → 422 ────────────────────────────

def test_crea_promozione_sconto_zero(operatore_test):
    """[IF-OP.06] Sconto = 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Sconto Zero",
        "tipo": "promozione",
        "sconto_percentuale": 0.0,
        "data_scadenza": _domani(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Scenario alternativo: abbonamento prezzo negativo → 422 ──────────────────

def test_crea_abbonamento_prezzo_negativo(operatore_test):
    """[IF-OP.06] Prezzo ≤ 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Abbonamento Gratis",
        "tipo": "abbonamento",
        "prezzo": -5.0,
        "durata_giorni": 30,
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Elimina offerta ───────────────────────────────────────────────────────────

def test_elimina_offerta(operatore_test):
    """[IF-OP.06] Crea poi elimina → 204, poi GET lista non contiene più."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Offerta Da Eliminare",
        "tipo": "promozione",
        "sconto_percentuale": 15.0,
        "data_scadenza": _domani(),
    }
    created = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert created.status_code == 201
    offerta_id = created.json()["id"]

    del_resp = http.delete(f"/operatore/offerte/{offerta_id}", headers=_auth(token))
    assert del_resp.status_code == 204

    lista = http.get("/operatore/offerte", headers=_auth(token)).json()
    ids = [o["id"] for o in lista]
    assert offerta_id not in ids
```

- [ ] **Step 2: Esegui i test (integration)**

```bash
cd backend && uv run pytest tests/test_offerte.py -v -m integration
```

Tutti i test devono passare. Se fallisce `test_lista_offerte_operatore_autenticato` per mancanza di DB, verifica `DATABASE_URL` in `backend/.env`.

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_offerte.py
git commit -m "test(offerte): test integrazione IF-OP.06"
```

---

## Task 7: Frontend — `OffertaService.ts`

**Files:**
- Crea: `frontend/src/services/OffertaService.ts`

- [ ] **Step 1: Scrivi il service**

```typescript
// frontend/src/services/OffertaService.ts
import { api } from './ApiService'

export interface Offerta {
  id: string
  nome: string
  tipo: 'promozione' | 'abbonamento'
  stato: 'bozza' | 'attiva' | 'scaduta'
  descrizione: string | null
  sconto_percentuale: number | null
  prezzo: number | null
  durata_giorni: number | null
  data_inizio: string | null
  data_scadenza: string | null
  created_at: string
}

export interface CreaOffertaPayload {
  nome: string
  tipo: 'promozione' | 'abbonamento'
  descrizione?: string
  sconto_percentuale?: number
  prezzo?: number
  durata_giorni?: number
  data_inizio?: string
  data_scadenza?: string
}

export const getOfferte = async (): Promise<Offerta[]> => {
  const r = await api.get<Offerta[]>('/operatore/offerte')
  return r.data
}

export const creaOfferta = async (payload: CreaOffertaPayload): Promise<Offerta> => {
  const r = await api.post<Offerta>('/operatore/offerte', payload)
  return r.data
}

export const eliminaOfferta = async (id: string): Promise<void> => {
  await api.delete(`/operatore/offerte/${id}`)
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/services/OffertaService.ts
git commit -m "feat(fe): OffertaService per IF-OP.06"
```

---

## Task 8: Frontend — `VistaTariffePromozioni`

**Files:**
- Crea: `frontend/src/views/operatore/VistaTariffePromozioni.tsx`
- Crea: `frontend/src/views/operatore/VistaTariffePromozioni.css`

- [ ] **Step 1: Scrivi il CSS**

```css
/* frontend/src/views/operatore/VistaTariffePromozioni.css */
.vista-tariffe {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

.tariffe-topbar {
  height: 64px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 14px;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}

.tariffe-topbar h2 {
  margin: 0;
  flex: 1;
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
}

.tariffe-body {
  max-width: 860px;
  margin: 0 auto;
  padding: 32px 24px;
}

.tariffe-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.tariffe-header-row h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
}

.btn-nuova-offerta {
  padding: 11px 22px;
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: background 160ms ease;
}
.btn-nuova-offerta:hover { background: #3a9a86; }

/* Lista offerte */
.offerte-lista {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.offerta-card {
  background: #fff;
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.06);
  border: 1px solid rgba(15, 23, 42, 0.06);
}

.offerta-tipo-badge {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.offerta-tipo-badge.promozione { background: #fef3c7; }
.offerta-tipo-badge.abbonamento { background: #dbeafe; }

.offerta-info { flex: 1; min-width: 0; }
.offerta-nome {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
}
.offerta-dettaglio {
  font-size: 12px;
  color: #64748b;
}

.offerta-stato {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 99px;
}
.offerta-stato.attiva  { background: #dcfce7; color: #16a34a; }
.offerta-stato.scaduta { background: #f1f5f9; color: #64748b; }
.offerta-stato.bozza   { background: #fef9c3; color: #a16207; }

.btn-elimina-offerta {
  background: none;
  border: none;
  color: #f43f5e;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 8px;
  transition: background 140ms;
}
.btn-elimina-offerta:hover { background: rgba(244, 63, 94, 0.08); }

.offerte-vuote {
  text-align: center;
  padding: 48px;
  color: #94a3b8;
  font-size: 15px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-offerta {
  background: #fff;
  border-radius: 20px;
  padding: 28px 26px;
  width: 420px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 32px 80px rgba(0,0,0,0.2);
}

.modal-offerta h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.modal-offerta label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.modal-offerta input,
.modal-offerta select,
.modal-offerta textarea {
  padding: 10px 12px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  background: #f8fafc;
  color: #0f172a;
  outline: none;
  transition: border-color 160ms;
}
.modal-offerta input:focus,
.modal-offerta select:focus,
.modal-offerta textarea:focus {
  border-color: #4caf9a;
  background: #fff;
}

.modal-errore {
  font-size: 12.5px;
  color: #f43f5e;
  margin: 0;
}

.modal-azioni {
  display: flex;
  gap: 10px;
  margin-top: 4px;
}

.btn-conferma {
  flex: 1;
  padding: 12px;
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
}
.btn-conferma:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-annulla {
  flex: 1;
  padding: 12px;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
}

.tariffe-topbar .btn-indietro {
  padding: 8px 16px;
  background: transparent;
  color: #4caf9a;
  border: 2px solid #4caf9a;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}
```

- [ ] **Step 2: Scrivi la vista**

```tsx
// frontend/src/views/operatore/VistaTariffePromozioni.tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getOfferte,
  creaOfferta,
  eliminaOfferta,
  type Offerta,
  type CreaOffertaPayload,
} from '../../services/OffertaService'
import './VistaTariffePromozioni.css'

const STATO_LABEL: Record<string, string> = {
  attiva: 'Attiva',
  scaduta: 'Scaduta',
  bozza: 'Bozza',
}

const TIPO_EMOJI: Record<string, string> = {
  promozione: '🏷️',
  abbonamento: '📅',
}

interface FormState {
  nome: string
  tipo: 'promozione' | 'abbonamento'
  descrizione: string
  sconto_percentuale: string
  prezzo: string
  durata_giorni: string
  data_inizio: string
  data_scadenza: string
}

const FORM_VUOTO: FormState = {
  nome: '',
  tipo: 'promozione',
  descrizione: '',
  sconto_percentuale: '',
  prezzo: '',
  durata_giorni: '',
  data_inizio: '',
  data_scadenza: '',
}

export default function VistaTariffePromozioni() {
  const navigate = useNavigate()
  const [offerte, setOfferte] = useState<Offerta[]>([])
  const [mostraModal, setMostraModal] = useState(false)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricarica = useCallback(() => {
    getOfferte().then(setOfferte).catch(() => {})
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriModal = () => {
    setForm(FORM_VUOTO)
    setErrore('')
    setMostraModal(true)
  }

  const chiudiModal = () => {
    setMostraModal(false)
    setErrore('')
  }

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    try {
      const payload: CreaOffertaPayload = {
        nome: form.nome.trim(),
        tipo: form.tipo,
        descrizione: form.descrizione.trim() || undefined,
        sconto_percentuale: form.sconto_percentuale ? parseFloat(form.sconto_percentuale) : undefined,
        prezzo: form.prezzo ? parseFloat(form.prezzo) : undefined,
        durata_giorni: form.durata_giorni ? parseInt(form.durata_giorni) : undefined,
        data_inizio: form.data_inizio || undefined,
        data_scadenza: form.data_scadenza || undefined,
      }
      await creaOfferta(payload)
      chiudiModal()
      ricarica()
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const status = err.response?.status
        const detail = err.response?.data?.detail
        if (status === 409) setErrore('Esiste già un\'offerta con questo nome.')
        else if (status === 422) setErrore(typeof detail === 'string' ? detail : 'Dati non validi. Controlla i campi.')
        else setErrore('Errore durante il salvataggio. Riprova.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const handleElimina = async (id: string) => {
    if (!confirm('Eliminare questa offerta?')) return
    await eliminaOfferta(id).catch(() => {})
    ricarica()
  }

  const set = (field: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setForm(prev => ({ ...prev, [field]: e.target.value }))

  return (
    <div className="vista-tariffe">
      <div className="tariffe-topbar">
        <h2>Tariffe e Promozioni</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="tariffe-body">
        <div className="tariffe-header-row">
          <h3>Offerte commerciali</h3>
          <button className="btn-nuova-offerta" onClick={apriModal}>
            + Nuova offerta
          </button>
        </div>

        <div className="offerte-lista">
          {offerte.length === 0 ? (
            <div className="offerte-vuote">Nessuna offerta definita. Crea la prima!</div>
          ) : (
            offerte.map(o => (
              <div className="offerta-card" key={o.id}>
                <div className={`offerta-tipo-badge ${o.tipo}`}>
                  {TIPO_EMOJI[o.tipo]}
                </div>
                <div className="offerta-info">
                  <div className="offerta-nome">{o.nome}</div>
                  <div className="offerta-dettaglio">
                    {o.tipo === 'promozione'
                      ? `Sconto ${o.sconto_percentuale}% — scade ${o.data_scadenza ? new Date(o.data_scadenza).toLocaleDateString('it-IT') : '—'}`
                      : `€${o.prezzo} · ${o.durata_giorni} giorni`}
                  </div>
                </div>
                <span className={`offerta-stato ${o.stato}`}>{STATO_LABEL[o.stato]}</span>
                <button className="btn-elimina-offerta" onClick={() => handleElimina(o.id)} title="Elimina">🗑</button>
              </div>
            ))
          )}
        </div>
      </div>

      {mostraModal && (
        <div className="modal-overlay" onClick={chiudiModal}>
          <div className="modal-offerta" onClick={e => e.stopPropagation()}>
            <h3>Nuova offerta</h3>

            <label>
              Nome *
              <input value={form.nome} onChange={set('nome')} placeholder="es. Estate 2026" />
            </label>

            <label>
              Tipo *
              <select value={form.tipo} onChange={set('tipo')}>
                <option value="promozione">Promozione</option>
                <option value="abbonamento">Abbonamento</option>
              </select>
            </label>

            <label>
              Descrizione
              <input value={form.descrizione} onChange={set('descrizione')} placeholder="Descrizione opzionale" />
            </label>

            {form.tipo === 'promozione' && (
              <>
                <label>
                  Sconto (%) *
                  <input type="number" min="1" max="100" value={form.sconto_percentuale} onChange={set('sconto_percentuale')} placeholder="es. 20" />
                </label>
                <label>
                  Data scadenza *
                  <input type="datetime-local" value={form.data_scadenza} onChange={set('data_scadenza')} />
                </label>
              </>
            )}

            {form.tipo === 'abbonamento' && (
              <>
                <label>
                  Prezzo (€) *
                  <input type="number" min="0.01" step="0.01" value={form.prezzo} onChange={set('prezzo')} placeholder="es. 29.99" />
                </label>
                <label>
                  Durata (giorni) *
                  <input type="number" min="1" value={form.durata_giorni} onChange={set('durata_giorni')} placeholder="es. 30" />
                </label>
                <label>
                  Data inizio
                  <input type="datetime-local" value={form.data_inizio} onChange={set('data_inizio')} />
                </label>
                <label>
                  Data scadenza
                  <input type="datetime-local" value={form.data_scadenza} onChange={set('data_scadenza')} />
                </label>
              </>
            )}

            {errore && <p className="modal-errore">{errore}</p>}

            <div className="modal-azioni">
              <button className="btn-annulla" onClick={chiudiModal}>Annulla</button>
              <button className="btn-conferma" onClick={handleConferma} disabled={caricamento}>
                {caricamento ? '...' : 'Salva offerta'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/operatore/VistaTariffePromozioni.tsx frontend/src/views/operatore/VistaTariffePromozioni.css
git commit -m "feat(fe): VistaTariffePromozioni per IF-OP.06"
```

---

## Task 9: Routing App.tsx + navigazione dalla mappa

**Files:**
- Modifica: `frontend/src/App.tsx`
- Modifica: `frontend/src/views/operatore/VistaMappaOperatore.tsx`

- [ ] **Step 1: Aggiungi la rotta in `App.tsx`**

Aggiungi l'import:
```tsx
import VistaTariffePromozioni from './views/operatore/VistaTariffePromozioni'
```

Aggiungi la rotta prima di `/operatore/*`:
```tsx
<Route
  path="/operatore/tariffe-promozioni"
  element={
    <RoutaProtetta ruoloRichiesto="OP">
      <VistaTariffePromozioni />
    </RoutaProtetta>
  }
/>
```

- [ ] **Step 2: Aggiungi navigazione in `VistaMappaOperatore.tsx`**

Il pulsante "Tariffe e promozioni" nel pannello laterale deve navigare alla nuova vista. Cerca il pulsante:
```tsx
<button className="btn-pannello secondario">Tariffe e promozioni</button>
```
E sostituiscilo con:
```tsx
<button className="btn-pannello secondario" onClick={() => navigate('/operatore/tariffe-promozioni')}>
  Tariffe e promozioni
</button>
```

- [ ] **Step 3: Verifica build TypeScript**

```bash
cd frontend && npm run build 2>&1 | tail -20
```

Output atteso: `✓ built in Xs` senza errori TypeScript.

- [ ] **Step 4: Commit finale**

```bash
git add frontend/src/App.tsx frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(fe): routing e navigazione VistaTariffePromozioni [IF-OP.06]"
```

- [ ] **Step 5: Push**

```bash
git push origin feature/auth
```

---

## Checklist finale

- [ ] Migration SQL eseguita su Supabase
- [ ] `GET /operatore/offerte` → 200 con lista
- [ ] `POST /operatore/offerte` promozione → 201
- [ ] `POST /operatore/offerte` abbonamento → 201
- [ ] Nome duplicato → 409
- [ ] Scadenza nel passato → 422
- [ ] Sconto = 0 → 422
- [ ] Senza token → 401
- [ ] Frontend: pulsante "Tariffe e promozioni" naviga a `/operatore/tariffe-promozioni`
- [ ] Frontend: lista offerte visibile
- [ ] Frontend: form promozione mostra campi sconto + scadenza
- [ ] Frontend: form abbonamento mostra campi prezzo + durata
- [ ] Frontend: errore nome duplicato mostrato in form
- [ ] Build TypeScript senza errori
