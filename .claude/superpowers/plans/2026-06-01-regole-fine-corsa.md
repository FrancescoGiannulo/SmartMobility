# Definisce Regole Fine Corsa — Implementation Plan (IF-OP.13 / CS-13)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permettere all'Operatore autenticato di configurare le regole di fine corsa: politica sanzionatoria (penale/blocco/avviso), importo penale, e bonus opzionale per parcheggi corretti.

**Architecture:** Layer standard Controller → BLL → DAL → DB. La tabella `regole_fine_corsa` esiste già; va estesa con bonus fields e `zona_parcheggio_id` reso nullable per config globale. Una sola riga attiva (upsert pattern): `GET` legge la config corrente, `PUT` la aggiorna o crea.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 + PostgreSQL (Supabase), React 19 + TypeScript + Axios.

---

## Contesto codebase

- **Tabella esistente** `regole_fine_corsa`: campi `id`, `zona_parcheggio_id` (NOT NULL FK), `batteria_minima`, `penale_fuori_zona`, `tipo_vincolo` (enum `penale`/`divieto`/`avviso`), `created_at`
- **Model esistente** `backend/model/regola_fine_corsa.py`: class `RegolaFinecorsa` + enum `TipoVincoloFinecorsa`
- **Mancanti**: colonne `bonus_parcheggi_corretti`, `bonus_valore`; `zona_parcheggio_id` va reso nullable
- **Enum `tipo_vincolo_fine_corsa`** già in DB: `'penale'` = penale, `'divieto'` = blocco fine corsa, `'avviso'` = avviso

## File Structure

| File | Azione | Responsabilità |
|------|--------|----------------|
| `backend/migrations/005_regole_fine_corsa_bonus.sql` | Crea | ALTER TABLE: zona nullable + add bonus columns |
| `backend/model/regola_fine_corsa.py` | Modifica | Aggiunge bonus fields, rende zona_parcheggio_id Optional |
| `backend/dal/regola_fine_corsa_repository.py` | Crea | `get_corrente()` + `salva()` (upsert) |
| `backend/bll/servizio_regole_fine_corsa.py` | Crea | Validazione + orchestrazione |
| `backend/controllers/schemas.py` | Modifica | Aggiunge `RegolaFinecorsaRequest`, `RegolaFinecorsaOut` |
| `backend/controllers/regola_fine_corsa_controller.py` | Crea | `GET` + `PUT /operatore/regole-fine-corsa` |
| `backend/main.py` | Modifica | Registra `regola_fine_corsa_router` |
| `backend/tests/test_regole_fine_corsa.py` | Crea | Test integrazione scenari base + alternativi |
| `frontend/src/services/RegolaFinecorsaService.ts` | Crea | API calls |
| `frontend/src/views/operatore/VistaImpostazioniRegole.tsx` | Crea | Form configurazione regole |
| `frontend/src/views/operatore/VistaImpostazioniRegole.css` | Crea | Stili |
| `frontend/src/App.tsx` | Modifica | Rotta `/operatore/impostazioni-regole` |
| `frontend/src/views/operatore/VistaMappaOperatore.tsx` | Modifica | onClick su "Impostazioni regole" |

---

## Task 1: Migrazione DB

**Files:**
- Crea: `backend/migrations/005_regole_fine_corsa_bonus.sql`

- [ ] **Step 1: Scrivi la migrazione**

```sql
-- backend/migrations/005_regole_fine_corsa_bonus.sql

-- Rende zona_parcheggio_id opzionale (config globale senza zona specifica)
ALTER TABLE regole_fine_corsa
  ALTER COLUMN zona_parcheggio_id DROP NOT NULL;

-- Aggiunge campi bonus
ALTER TABLE regole_fine_corsa
  ADD COLUMN IF NOT EXISTS bonus_parcheggi_corretti INTEGER,
  ADD COLUMN IF NOT EXISTS bonus_valore NUMERIC(10, 2);

ALTER TABLE regole_fine_corsa
  ADD CONSTRAINT IF NOT EXISTS bonus_parcheggi_check
    CHECK (bonus_parcheggi_corretti IS NULL OR bonus_parcheggi_corretti > 0),
  ADD CONSTRAINT IF NOT EXISTS bonus_valore_check
    CHECK (bonus_valore IS NULL OR bonus_valore > 0);
```

- [ ] **Step 2: Esegui su Supabase**

Copia il contenuto nel SQL Editor di Supabase → Run.
Verifica: `SELECT column_name FROM information_schema.columns WHERE table_name = 'regole_fine_corsa';`
Output atteso include: `bonus_parcheggi_corretti`, `bonus_valore`.

- [ ] **Step 3: Commit**

```bash
git add backend/migrations/005_regole_fine_corsa_bonus.sql
git commit -m "feat(db): aggiungi campi bonus e zona nullable a regole_fine_corsa [IF-OP.13]"
```

---

## Task 2: Aggiorna ORM Model

**Files:**
- Modifica: `backend/model/regola_fine_corsa.py`

- [ ] **Step 1: Riscrivi il file**

```python
# backend/model/regola_fine_corsa.py
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlalchemy import Integer, Numeric, DateTime, text, ForeignKey, CheckConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoVincoloFinecorsa(str, Enum):
    penale = "penale"
    divieto = "divieto"
    avviso = "avviso"


class RegolaFinecorsa(Base):
    __tablename__ = "regole_fine_corsa"
    __table_args__ = (
        CheckConstraint("batteria_minima BETWEEN 0 AND 100", name="batteria_minima_check"),
        CheckConstraint(
            "bonus_parcheggi_corretti IS NULL OR bonus_parcheggi_corretti > 0",
            name="bonus_parcheggi_check",
        ),
        CheckConstraint(
            "bonus_valore IS NULL OR bonus_valore > 0",
            name="bonus_valore_check",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zona_parcheggio_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="CASCADE"),
        nullable=True,
    )
    batteria_minima: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    penale_fuori_zona: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00")
    )
    tipo_vincolo: Mapped[TipoVincoloFinecorsa] = mapped_column(
        SAEnum(TipoVincoloFinecorsa, name="tipo_vincolo_fine_corsa", create_type=False),
        nullable=False,
        default=TipoVincoloFinecorsa.avviso,
    )
    bonus_parcheggi_corretti: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bonus_valore: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 2: Verifica import**

```bash
cd backend && uv run python -c "from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa; print('OK', list(TipoVincoloFinecorsa))"
```

Output atteso: `OK [<TipoVincoloFinecorsa.penale: 'penale'>, ...]`

- [ ] **Step 3: Commit**

```bash
git add backend/model/regola_fine_corsa.py
git commit -m "feat(model): aggiorna RegolaFinecorsa con bonus fields e zona nullable [IF-OP.13]"
```

---

## Task 3: DAL RegolaFinecorsaRepository

**Files:**
- Crea: `backend/dal/regola_fine_corsa_repository.py`

- [ ] **Step 1: Scrivi il repository**

```python
# backend/dal/regola_fine_corsa_repository.py
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa


class RegolaFinecorsaRepository:

    def get_corrente(self, db: Session) -> Optional[RegolaFinecorsa]:
        """Restituisce l'unica configurazione globale, o None se non esiste."""
        return (
            db.query(RegolaFinecorsa)
            .filter(RegolaFinecorsa.zona_parcheggio_id.is_(None))
            .order_by(RegolaFinecorsa.created_at.desc())
            .first()
        )

    def salva(
        self,
        tipo_vincolo: TipoVincoloFinecorsa,
        penale_fuori_zona: Decimal,
        batteria_minima: Optional[int],
        bonus_parcheggi_corretti: Optional[int],
        bonus_valore: Optional[Decimal],
        db: Session,
    ) -> RegolaFinecorsa:
        """Upsert: aggiorna la config esistente o ne crea una nuova."""
        regola = self.get_corrente(db)
        if regola is None:
            regola = RegolaFinecorsa(zona_parcheggio_id=None)
            db.add(regola)
        regola.tipo_vincolo = tipo_vincolo
        regola.penale_fuori_zona = penale_fuori_zona
        regola.batteria_minima = batteria_minima
        regola.bonus_parcheggi_corretti = bonus_parcheggi_corretti
        regola.bonus_valore = bonus_valore
        db.commit()
        db.refresh(regola)
        return regola
```

- [ ] **Step 2: Verifica import**

```bash
cd backend && uv run python -c "from dal.regola_fine_corsa_repository import RegolaFinecorsaRepository; print('OK')"
```

- [ ] **Step 3: Commit**

```bash
git add backend/dal/regola_fine_corsa_repository.py
git commit -m "feat(dal): RegolaFinecorsaRepository per IF-OP.13"
```

---

## Task 4: BLL ServizioRegolaFinecorsa

**Files:**
- Crea: `backend/bll/servizio_regole_fine_corsa.py`

- [ ] **Step 1: Scrivi il servizio**

```python
# backend/bll/servizio_regole_fine_corsa.py
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from dal.regola_fine_corsa_repository import RegolaFinecorsaRepository
from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa


class RegolaFinecorsaValidazioneException(Exception):
    pass


class ServizioRegolaFinecorsa:

    def __init__(self) -> None:
        self._repo = RegolaFinecorsaRepository()

    def get_corrente(self, db: Session) -> Optional[RegolaFinecorsa]:
        return self._repo.get_corrente(db)

    def salva(
        self,
        tipo_vincolo: str,
        penale_fuori_zona: Decimal,
        batteria_minima: Optional[int],
        bonus_parcheggi_corretti: Optional[int],
        bonus_valore: Optional[Decimal],
        db: Session,
    ) -> RegolaFinecorsa:
        self._valida(
            tipo_vincolo=tipo_vincolo,
            penale_fuori_zona=penale_fuori_zona,
            batteria_minima=batteria_minima,
            bonus_parcheggi_corretti=bonus_parcheggi_corretti,
            bonus_valore=bonus_valore,
        )
        try:
            vincolo = TipoVincoloFinecorsa(tipo_vincolo)
        except ValueError:
            raise RegolaFinecorsaValidazioneException(
                f"Tipo vincolo non valido: usa 'penale', 'divieto' o 'avviso'"
            )
        return self._repo.salva(
            tipo_vincolo=vincolo,
            penale_fuori_zona=penale_fuori_zona,
            batteria_minima=batteria_minima,
            bonus_parcheggi_corretti=bonus_parcheggi_corretti,
            bonus_valore=bonus_valore,
            db=db,
        )

    def _valida(
        self,
        tipo_vincolo: str,
        penale_fuori_zona: Decimal,
        batteria_minima: Optional[int],
        bonus_parcheggi_corretti: Optional[int],
        bonus_valore: Optional[Decimal],
    ) -> None:
        if tipo_vincolo not in ("penale", "divieto", "avviso"):
            raise RegolaFinecorsaValidazioneException(
                "Tipo vincolo non valido: usa 'penale', 'divieto' o 'avviso'"
            )
        if tipo_vincolo == "penale" and penale_fuori_zona <= 0:
            raise RegolaFinecorsaValidazioneException(
                "L'importo della penale deve essere maggiore di zero"
            )
        if tipo_vincolo != "penale" and penale_fuori_zona < 0:
            raise RegolaFinecorsaValidazioneException(
                "L'importo penale non può essere negativo"
            )
        if batteria_minima is not None and not (0 <= batteria_minima <= 100):
            raise RegolaFinecorsaValidazioneException(
                "La batteria minima deve essere compresa tra 0 e 100"
            )
        bonus_attivo = bonus_parcheggi_corretti is not None or bonus_valore is not None
        if bonus_attivo:
            if bonus_parcheggi_corretti is None:
                raise RegolaFinecorsaValidazioneException(
                    "Il numero di parcheggi corretti è obbligatorio per attivare il bonus"
                )
            if bonus_parcheggi_corretti <= 0:
                raise RegolaFinecorsaValidazioneException(
                    "Il numero di parcheggi corretti deve essere maggiore di zero"
                )
            if bonus_valore is None:
                raise RegolaFinecorsaValidazioneException(
                    "Il valore del bonus è obbligatorio quando si configura il bonus"
                )
            if bonus_valore <= 0:
                raise RegolaFinecorsaValidazioneException(
                    "Il valore del bonus deve essere maggiore di zero"
                )
```

- [ ] **Step 2: Verifica import**

```bash
cd backend && uv run python -c "from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa; print('OK')"
```

- [ ] **Step 3: Commit**

```bash
git add backend/bll/servizio_regole_fine_corsa.py
git commit -m "feat(bll): ServizioRegolaFinecorsa con validazione [IF-OP.13]"
```

---

## Task 5: Controller + Schemas + main.py

**Files:**
- Modifica: `backend/controllers/schemas.py`
- Crea: `backend/controllers/regola_fine_corsa_controller.py`
- Modifica: `backend/main.py`

- [ ] **Step 1: Aggiungi in fondo a `schemas.py`**

```python
class RegolaFinecorsaRequest(BaseModel):
    tipo_vincolo: str  # 'penale' | 'divieto' | 'avviso'
    penale_fuori_zona: Decimal = Decimal("0.00")
    batteria_minima: int | None = None
    bonus_parcheggi_corretti: int | None = None
    bonus_valore: Decimal | None = None


class RegolaFinecorsaOut(BaseModel):
    id: UUID
    tipo_vincolo: str
    penale_fuori_zona: Decimal
    batteria_minima: int | None
    bonus_parcheggi_corretti: int | None
    bonus_valore: Decimal | None
    created_at: datetime

    model_config = {"from_attributes": True}
```

Nota: `datetime`, `Decimal`, `UUID` sono già importati nel file dopo Task 5 di IF-OP.06.

- [ ] **Step 2: Crea il controller**

```python
# backend/controllers/regola_fine_corsa_controller.py
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import RegolaFinecorsaRequest, RegolaFinecorsaOut
from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa, RegolaFinecorsaValidazioneException

router = APIRouter(prefix="/operatore", tags=["Operatore - Regole Fine Corsa"])
_servizio = ServizioRegolaFinecorsa()


# [IF-OP.13] — leggi config corrente
@router.get("/regole-fine-corsa", response_model=RegolaFinecorsaOut | None)
def get_regole(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.get_corrente(db)


# [IF-OP.13] — salva (upsert) config
@router.put("/regole-fine-corsa", response_model=RegolaFinecorsaOut)
def salva_regole(
    body: RegolaFinecorsaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.salva(
            tipo_vincolo=body.tipo_vincolo,
            penale_fuori_zona=body.penale_fuori_zona,
            batteria_minima=body.batteria_minima,
            bonus_parcheggi_corretti=body.bonus_parcheggi_corretti,
            bonus_valore=body.bonus_valore,
            db=db,
        )
    except RegolaFinecorsaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))
```

- [ ] **Step 3: Aggiungi a `main.py`**

```python
from controllers.regola_fine_corsa_controller import router as regola_fine_corsa_router
# ...
app.include_router(regola_fine_corsa_router)
```

- [ ] **Step 4: Verifica route**

```bash
cd backend && uv run python -c "from main import app; routes=[r.path for r in app.routes if 'regole' in r.path]; print(routes)"
```

Output atteso: `['/operatore/regole-fine-corsa', '/operatore/regole-fine-corsa']`

- [ ] **Step 5: Commit**

```bash
git add backend/controllers/schemas.py backend/controllers/regola_fine_corsa_controller.py backend/main.py
git commit -m "feat(api): endpoint regole-fine-corsa [IF-OP.13]"
```

---

## Task 6: Test Backend

**Files:**
- Crea: `backend/tests/test_regole_fine_corsa.py`

- [ ] **Step 1: Crea il file di test (NON eseguire, richiedono DB)**

```python
"""[IF-OP.13] Test Definisce Regole Fine Corsa — scenari base e alternativi."""
import pytest
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── GET corrente ──────────────────────────────────────────────────────────────

def test_get_regole_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/operatore/regole-fine-corsa")
    assert resp.status_code == 401


def test_get_regole_autenticato(operatore_test):
    """[IF-OP.13] GET ritorna None o configurazione corrente."""
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/regole-fine-corsa", headers=_auth(token))
    assert resp.status_code == 200
    # può essere null se non c'è config salvata
    assert resp.json() is None or isinstance(resp.json(), dict)


# ── PUT scenario base: avviso ─────────────────────────────────────────────────

def test_salva_regole_avviso(operatore_test):
    """[IF-OP.13] Salva config con vincolo 'avviso' → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "tipo_vincolo": "avviso",
        "penale_fuori_zona": "0.00",
    }
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["tipo_vincolo"] == "avviso"
    assert float(body["penale_fuori_zona"]) == 0.0


# ── PUT scenario base: penale con importo ─────────────────────────────────────

def test_salva_regole_penale(operatore_test):
    """[IF-OP.13] Salva config penale con importo positivo → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "tipo_vincolo": "penale",
        "penale_fuori_zona": "5.00",
    }
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["tipo_vincolo"] == "penale"
    assert float(body["penale_fuori_zona"]) == 5.0


# ── PUT scenario base: bonus attivo ──────────────────────────────────────────

def test_salva_regole_con_bonus(operatore_test):
    """[IF-OP.13] Salva config con bonus → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "tipo_vincolo": "avviso",
        "penale_fuori_zona": "0.00",
        "bonus_parcheggi_corretti": 5,
        "bonus_valore": "2.50",
    }
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["bonus_parcheggi_corretti"] == 5
    assert float(body["bonus_valore"]) == 2.50


# ── PUT upsert: seconda chiamata aggiorna ─────────────────────────────────────

def test_salva_regole_upsert(operatore_test):
    """[IF-OP.13] Seconda PUT aggiorna la config (non ne crea una nuova)."""
    token = _login(operatore_test["email"], operatore_test["password"])
    http.put("/operatore/regole-fine-corsa", json={"tipo_vincolo": "avviso", "penale_fuori_zona": "0.00"}, headers=_auth(token))
    http.put("/operatore/regole-fine-corsa", json={"tipo_vincolo": "divieto", "penale_fuori_zona": "0.00"}, headers=_auth(token))
    resp = http.get("/operatore/regole-fine-corsa", headers=_auth(token))
    assert resp.json()["tipo_vincolo"] == "divieto"


# ── Scenari alternativi: validazione ─────────────────────────────────────────

def test_penale_importo_zero(operatore_test):
    """[IF-OP.13] Penale con importo = 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "penale", "penale_fuori_zona": "0.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_batteria_fuori_range(operatore_test):
    """[IF-OP.13] Batteria minima > 100 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "avviso", "penale_fuori_zona": "0.00", "batteria_minima": 150}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_bonus_incompleto(operatore_test):
    """[IF-OP.13] Bonus con solo parcheggi_corretti (senza valore) → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "tipo_vincolo": "avviso",
        "penale_fuori_zona": "0.00",
        "bonus_parcheggi_corretti": 5,
    }
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_tipo_vincolo_non_valido(operatore_test):
    """[IF-OP.13] Tipo vincolo non riconosciuto → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "multa", "penale_fuori_zona": "0.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422
```

- [ ] **Step 2: Commit**

```bash
git add backend/tests/test_regole_fine_corsa.py
git commit -m "test(regole_fine_corsa): test integrazione IF-OP.13"
```

---

## Task 7: Frontend — RegolaFinecorsaService.ts

**Files:**
- Crea: `frontend/src/services/RegolaFinecorsaService.ts`

- [ ] **Step 1: Scrivi il service**

```typescript
// frontend/src/services/RegolaFinecorsaService.ts
import { api } from './ApiService'

export interface RegolaFinecorsa {
  id: string
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  penale_fuori_zona: number
  batteria_minima: number | null
  bonus_parcheggi_corretti: number | null
  bonus_valore: number | null
  created_at: string
}

export interface SalvaRegolaPayload {
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  penale_fuori_zona: number
  batteria_minima?: number
  bonus_parcheggi_corretti?: number
  bonus_valore?: number
}

export const getRegolaFinecorsa = async (): Promise<RegolaFinecorsa | null> => {
  const r = await api.get<RegolaFinecorsa | null>('/operatore/regole-fine-corsa')
  return r.data
}

export const salvaRegolaFinecorsa = async (payload: SalvaRegolaPayload): Promise<RegolaFinecorsa> => {
  const r = await api.put<RegolaFinecorsa>('/operatore/regole-fine-corsa', payload)
  return r.data
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/services/RegolaFinecorsaService.ts
git commit -m "feat(fe): RegolaFinecorsaService per IF-OP.13"
```

---

## Task 8: Frontend — VistaImpostazioniRegole

**Files:**
- Crea: `frontend/src/views/operatore/VistaImpostazioniRegole.css`
- Crea: `frontend/src/views/operatore/VistaImpostazioniRegole.tsx`

- [ ] **Step 1: Scrivi il CSS**

```css
/* frontend/src/views/operatore/VistaImpostazioniRegole.css */
.vista-regole {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

.regole-topbar {
  height: 64px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 14px;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}

.regole-topbar h2 {
  margin: 0;
  flex: 1;
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
}

.regole-topbar .btn-indietro {
  padding: 8px 16px;
  background: transparent;
  color: #4caf9a;
  border: 2px solid #4caf9a;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
}

.regole-body {
  max-width: 640px;
  margin: 0 auto;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.regole-card {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.06);
  border: 1px solid rgba(15, 23, 42, 0.06);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.regole-card h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 800;
  color: #0f172a;
}

.regole-campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.regole-campo label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.regole-campo input,
.regole-campo select {
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  background: #f8fafc;
  color: #0f172a;
  outline: none;
  transition: border-color 160ms;
}
.regole-campo input:focus,
.regole-campo select:focus {
  border-color: #4caf9a;
  background: #fff;
}

.bonus-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
  user-select: none;
}

.bonus-toggle input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #4caf9a;
  cursor: pointer;
}

.regole-errore {
  font-size: 13px;
  color: #f43f5e;
  margin: 0;
  padding: 10px 14px;
  background: rgba(244, 63, 94, 0.06);
  border-radius: 10px;
  border: 1px solid rgba(244, 63, 94, 0.2);
}

.regole-conferma {
  font-size: 13px;
  color: #16a34a;
  margin: 0;
  padding: 10px 14px;
  background: rgba(22, 163, 74, 0.06);
  border-radius: 10px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

.btn-salva-regole {
  width: 100%;
  padding: 14px;
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: background 160ms;
}
.btn-salva-regole:hover { background: #3a9a86; }
.btn-salva-regole:disabled { opacity: 0.6; cursor: not-allowed; }
```

- [ ] **Step 2: Scrivi la vista**

```tsx
// frontend/src/views/operatore/VistaImpostazioniRegole.tsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getRegolaFinecorsa,
  salvaRegolaFinecorsa,
  type SalvaRegolaPayload,
} from '../../services/RegolaFinecorsaService'
import './VistaImpostazioniRegole.css'

const LABEL_VINCOLO: Record<string, string> = {
  penale: 'Penale (addebito importo)',
  divieto: 'Blocco fine corsa',
  avviso: 'Avviso (nessun addebito)',
}

export default function VistaImpostazioniRegole() {
  const navigate = useNavigate()
  const [tipoVincolo, setTipoVincolo] = useState<'penale' | 'divieto' | 'avviso'>('avviso')
  const [penale, setPenale] = useState('')
  const [batteria, setBatteria] = useState('')
  const [bonusAttivo, setBonusAttivo] = useState(false)
  const [bonusParcheggi, setBonusParcheggi] = useState('')
  const [bonusValore, setBonusValore] = useState('')
  const [errore, setErrore] = useState('')
  const [conferma, setConferma] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  useEffect(() => {
    getRegolaFinecorsa().then(regola => {
      if (!regola) return
      setTipoVincolo(regola.tipo_vincolo)
      setPenale(regola.penale_fuori_zona > 0 ? String(regola.penale_fuori_zona) : '')
      setBatteria(regola.batteria_minima != null ? String(regola.batteria_minima) : '')
      if (regola.bonus_parcheggi_corretti != null) {
        setBonusAttivo(true)
        setBonusParcheggi(String(regola.bonus_parcheggi_corretti))
        setBonusValore(regola.bonus_valore != null ? String(regola.bonus_valore) : '')
      }
    }).catch(() => {})
  }, [])

  const handleSalva = async () => {
    setErrore('')
    setConferma('')
    setCaricamento(true)
    try {
      const payload: SalvaRegolaPayload = {
        tipo_vincolo: tipoVincolo,
        penale_fuori_zona: penale ? parseFloat(penale) : 0,
        batteria_minima: batteria ? parseInt(batteria) : undefined,
        bonus_parcheggi_corretti: bonusAttivo && bonusParcheggi ? parseInt(bonusParcheggi) : undefined,
        bonus_valore: bonusAttivo && bonusValore ? parseFloat(bonusValore) : undefined,
      }
      await salvaRegolaFinecorsa(payload)
      setConferma('✅ Regole di fine corsa salvate correttamente.')
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail
        setErrore(typeof detail === 'string' ? detail : 'Dati non validi. Controlla i campi.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  return (
    <div className="vista-regole">
      <div className="regole-topbar">
        <h2>Impostazioni Regole Fine Corsa</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="regole-body">

        {/* Card politica sanzionatoria */}
        <div className="regole-card">
          <h3>Politica sanzionatoria</h3>
          <div className="regole-campo">
            <label>Vincolo rilascio fuori zona parcheggio</label>
            <select value={tipoVincolo} onChange={e => setTipoVincolo(e.target.value as typeof tipoVincolo)}>
              {Object.entries(LABEL_VINCOLO).map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
          </div>

          {tipoVincolo === 'penale' && (
            <div className="regole-campo">
              <label>Importo penale (€)</label>
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={penale}
                onChange={e => setPenale(e.target.value)}
                placeholder="es. 5.00"
              />
            </div>
          )}
        </div>

        {/* Card vincoli aggiuntivi */}
        <div className="regole-card">
          <h3>Vincoli aggiuntivi</h3>
          <div className="regole-campo">
            <label>Batteria minima richiesta (%)</label>
            <input
              type="number"
              min="0"
              max="100"
              value={batteria}
              onChange={e => setBatteria(e.target.value)}
              placeholder="Lascia vuoto per nessun vincolo"
            />
          </div>
        </div>

        {/* Card bonus */}
        <div className="regole-card">
          <h3>Incentivo parcheggio corretto</h3>
          <label className="bonus-toggle">
            <input type="checkbox" checked={bonusAttivo} onChange={e => setBonusAttivo(e.target.checked)} />
            Attiva bonus per parcheggi corretti
          </label>

          {bonusAttivo && (
            <>
              <div className="regole-campo">
                <label>Numero parcheggi corretti necessari</label>
                <input
                  type="number"
                  min="1"
                  value={bonusParcheggi}
                  onChange={e => setBonusParcheggi(e.target.value)}
                  placeholder="es. 5"
                />
              </div>
              <div className="regole-campo">
                <label>Valore bonus (€)</label>
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={bonusValore}
                  onChange={e => setBonusValore(e.target.value)}
                  placeholder="es. 2.50"
                />
              </div>
            </>
          )}
        </div>

        {errore && <p className="regole-errore">{errore}</p>}
        {conferma && <p className="regole-conferma">{conferma}</p>}

        <button className="btn-salva-regole" onClick={handleSalva} disabled={caricamento}>
          {caricamento ? '...' : 'Salva regole'}
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | head -20
```

Output atteso: nessun output (zero errori).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/operatore/VistaImpostazioniRegole.tsx frontend/src/views/operatore/VistaImpostazioniRegole.css
git commit -m "feat(fe): VistaImpostazioniRegole per IF-OP.13"
```

---

## Task 9: Routing App.tsx + navigazione dalla mappa

**Files:**
- Modifica: `frontend/src/App.tsx`
- Modifica: `frontend/src/views/operatore/VistaMappaOperatore.tsx`

- [ ] **Step 1: Aggiorna `App.tsx`**

Aggiungi import:
```tsx
import VistaImpostazioniRegole from './views/operatore/VistaImpostazioniRegole'
```

Aggiungi rotta PRIMA di `/operatore/*`:
```tsx
<Route
  path="/operatore/impostazioni-regole"
  element={
    <RoutaProtetta ruoloRichiesto="OP">
      <VistaImpostazioniRegole />
    </RoutaProtetta>
  }
/>
```

- [ ] **Step 2: Aggiorna `VistaMappaOperatore.tsx`**

Cerca il pulsante "Impostazioni regole" (o "IMPOSTAZIONI REGOLE") nel pannello laterale e aggiungi onClick:
```tsx
<button className="btn-pannello secondario" onClick={() => navigate('/operatore/impostazioni-regole')}>
  Impostazioni regole
</button>
```

- [ ] **Step 3: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | head -20
```

Output atteso: nessun output.

- [ ] **Step 4: Commit e push**

```bash
git add frontend/src/App.tsx frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(fe): routing VistaImpostazioniRegole + navigazione [IF-OP.13]"
git push origin feature/auth
```

---

## Checklist finale

- [ ] Migration 005 eseguita su Supabase
- [ ] `GET /operatore/regole-fine-corsa` → 200 (null o config)
- [ ] `PUT /operatore/regole-fine-corsa` avviso → 200
- [ ] `PUT /operatore/regole-fine-corsa` penale con importo → 200
- [ ] `PUT /operatore/regole-fine-corsa` penale con importo=0 → 422
- [ ] Bonus completo → 200
- [ ] Bonus incompleto → 422
- [ ] Batteria > 100 → 422
- [ ] Senza token → 401
- [ ] Frontend: pulsante "Impostazioni regole" naviga correttamente
- [ ] Frontend: form carica config esistente al mount
- [ ] Frontend: penale mostra campo importo solo se selezionata
- [ ] Frontend: bonus mostra campi solo se checkbox attivato
- [ ] Frontend: messaggio conferma dopo salvataggio
- [ ] TypeScript: zero errori di build
