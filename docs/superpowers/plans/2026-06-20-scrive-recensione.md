# UT-15 Scrive Recensione — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the "Scrive Recensione" (UT-15) use case end-to-end (DB → DAL → BLL → Controller → frontend service → frontend view), exactly matching `docs/Diagrammi/Diagramma Classi.drawio` and `docs/Diagrammi/Diagrammi di Sequenza/camilla/sprint2/sequence_scrive_recensione.drawio`.

**Architecture:** Mirrors the existing `Segnalazione` feature (closest analog: simple write-once entity owned by an authenticated Utente, no edit/delete). Engine-based repository (`with Session(engine)`), BLL returning dicts to the controller, FastAPI router under `/utente` prefix protected by `verify_token(["UT"])`.

**Tech Stack:** FastAPI, SQLAlchemy 2.0 (Mapped/mapped_column), raw SQL migration file, React 19 + TypeScript, Axios via `ApiService`.

## Global Constraints

- Class names and method names must match the class diagram exactly: `Recensione`, `RecensioneRepository`, `ServizioRecensione`, `RecensioneController`, `RecensioneService`, `VistaRecensione`.
- `voto` is an integer 1–5; `commento` is optional free text (no length limit specified).
- Do NOT enforce the "at least one completed corsa" precondition in code — neither diagram models this check (see design doc note). Do not add a `CorsaRepository` dependency to `ServizioRecensione`.
- No edit/delete endpoints — out of scope per the use case and both diagrams.
- `CheckConstraint` for `voto` goes in `__table_args__`, not as a `mapped_column` argument (per project CLAUDE.md rule).
- Traceability comments `# [IF-UT.15]` on BLL/controller/repository methods, matching the existing convention used for `Segnalazione`.

---

## File Structure

- Create: `backend/migrations/014_recensioni.sql` — table `recensioni`
- Create: `backend/model/recensione.py` — ORM `Recensione`
- Create: `backend/dal/recensione_repository.py` — `RecensioneRepository`
- Create: `backend/bll/servizio_recensione.py` — `ServizioRecensione`
- Create: `backend/controllers/recensione_controller.py` — FastAPI router
- Modify: `backend/controllers/schemas.py` — add `ScriviRecensioneRequest`, `RecensioneOut`
- Modify: `backend/main.py` — register router
- Create: `backend/tests/test_recensione.py`
- Create: `frontend/src/services/RecensioneService.ts`
- Create: `frontend/src/views/utente/VistaRecensione.tsx`
- Create: `frontend/src/views/utente/VistaRecensione.css`
- Modify: `frontend/src/App.tsx` — add route
- Modify: `frontend/src/views/utente/VistaHomePageUtente.tsx` — add sidebar entry

---

## Task 1: Database migration + ORM model

**Files:**
- Create: `backend/migrations/014_recensioni.sql`
- Create: `backend/model/recensione.py`
- Test: `backend/tests/test_recensione.py` (schema-level check, added in this task; extended in Task 4)

**Interfaces:**
- Produces: `model.recensione.Recensione` ORM class with columns `id: uuid.UUID`, `utente_id: uuid.UUID`, `voto: int`, `commento: str | None`, `created_at: datetime`.

- [ ] **Step 1: Write the migration file**

```sql
-- backend/migrations/014_recensioni.sql
-- [IF-UT.15] Recensioni utenti
CREATE TABLE recensioni (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id       UUID NOT NULL,
    voto            INTEGER NOT NULL CHECK (voto BETWEEN 1 AND 5),
    commento        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX recensioni_utente_id_idx ON recensioni (utente_id);
CREATE INDEX recensioni_created_at_idx ON recensioni (created_at DESC);
```

- [ ] **Step 2: Run the migration against the dev DB**

Run (from `backend/`, with `DATABASE_URL` set in `.env`):
```bash
uv run python -c "
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()
e = create_engine(os.environ['DATABASE_URL'])
with e.begin() as c:
    c.execute(text(open('migrations/014_recensioni.sql').read()))
print('OK')
"
```
Expected: `OK` (or a clear error if the table already exists — in that case skip, it means a teammate already ran it).

- [ ] **Step 3: Write the ORM model**

```python
# backend/model/recensione.py
import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, String, Text, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Recensione(Base):
    __tablename__ = "recensioni"
    __table_args__ = (
        CheckConstraint("voto BETWEEN 1 AND 5", name="recensioni_voto_check"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    voto: Mapped[int] = mapped_column(Integer, nullable=False)
    commento: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Verify the model imports cleanly**

Run: `cd backend && uv run python -c "from model.recensione import Recensione; print(Recensione.__tablename__)"`
Expected: `recensioni`

- [ ] **Step 5: Commit**

```bash
git add backend/migrations/014_recensioni.sql backend/model/recensione.py
git commit -m "feat(recensione): aggiunge tabella recensioni e modello ORM [IF-UT.15]"
```

---

## Task 2: Repository (DAL)

**Files:**
- Create: `backend/dal/recensione_repository.py`
- Test: `backend/tests/test_recensione.py`

**Interfaces:**
- Consumes: `model.recensione.Recensione` (Task 1)
- Produces: `RecensioneRepository.save(utente_id: uuid.UUID, voto: int, commento: str | None) -> Recensione`, `RecensioneRepository.find_by_utente_id(utente_id: uuid.UUID) -> list[Recensione]`, `RecensioneRepository.find_all() -> list[Recensione]`

- [ ] **Step 1: Write the repository**

```python
# backend/dal/recensione_repository.py
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.recensione import Recensione


class RecensioneRepository:

    # [IF-UT.15] Scrive Recensione
    def save(self, utente_id: uuid.UUID, voto: int, commento: str | None) -> Recensione:
        with Session(engine) as session:
            recensione = Recensione(utente_id=utente_id, voto=voto, commento=commento)
            session.add(recensione)
            session.commit()
            session.refresh(recensione)
            return recensione

    def find_by_utente_id(self, utente_id: uuid.UUID) -> list[Recensione]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, voto, commento, created_at "
                    "FROM recensioni WHERE utente_id = :uid ORDER BY created_at DESC"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
        return [
            Recensione(
                id=r.id, utente_id=r.utente_id, voto=r.voto,
                commento=r.commento, created_at=r.created_at,
            )
            for r in rows
        ]

    def find_all(self) -> list[Recensione]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, voto, commento, created_at "
                    "FROM recensioni ORDER BY created_at DESC"
                )
            ).fetchall()
        return [
            Recensione(
                id=r.id, utente_id=r.utente_id, voto=r.voto,
                commento=r.commento, created_at=r.created_at,
            )
            for r in rows
        ]
```

- [ ] **Step 2: Verify import**

Run: `cd backend && uv run python -c "from dal.recensione_repository import RecensioneRepository; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/dal/recensione_repository.py
git commit -m "feat(recensione): aggiunge RecensioneRepository [IF-UT.15]"
```

---

## Task 3: BLL — ServizioRecensione

**Files:**
- Create: `backend/bll/servizio_recensione.py`

**Interfaces:**
- Consumes: `RecensioneRepository.save(utente_id, voto, commento)` (Task 2)
- Produces: `ServizioRecensione.scrivi_recensione(utente_id: uuid.UUID, voto: int, commento: str | None) -> dict`, `ServizioRecensione.valida_voto(voto: int) -> bool`. Raises `VotoNonValidoException` if `voto` is not in 1..5.

- [ ] **Step 1: Write the service**

```python
# backend/bll/servizio_recensione.py
from uuid import UUID
from dal.recensione_repository import RecensioneRepository


class VotoNonValidoException(Exception):
    pass


class ServizioRecensione:
    """[IF-UT.15] BLL per la scrittura di recensioni utente."""

    def __init__(self) -> None:
        self._repo = RecensioneRepository()

    # [IF-UT.15] Scrive Recensione
    def valida_voto(self, voto: int) -> bool:
        return 1 <= voto <= 5

    # [IF-UT.15] Scrive Recensione
    def scrivi_recensione(self, utente_id: UUID, voto: int, commento: str | None) -> dict:
        if not self.valida_voto(voto):
            raise VotoNonValidoException("Il voto deve essere compreso tra 1 e 5")
        recensione = self._repo.save(utente_id, voto, commento)
        return {
            "id": str(recensione.id),
            "voto": recensione.voto,
            "commento": recensione.commento,
            "created_at": recensione.created_at.isoformat(),
        }
```

- [ ] **Step 2: Verify import**

Run: `cd backend && uv run python -c "from bll.servizio_recensione import ServizioRecensione; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/bll/servizio_recensione.py
git commit -m "feat(recensione): aggiunge ServizioRecensione con validazione voto [IF-UT.15]"
```

---

## Task 4: Controller + schemas + router registration + tests

**Files:**
- Create: `backend/controllers/recensione_controller.py`
- Modify: `backend/controllers/schemas.py`
- Modify: `backend/main.py`
- Create: `backend/tests/test_recensione.py`

**Interfaces:**
- Consumes: `ServizioRecensione.scrivi_recensione` (Task 3), `middleware.auth_middleware.verify_token`
- Produces: `POST /utente/recensioni` → 201 with `RecensioneOut`

- [ ] **Step 1: Add Pydantic schemas**

In `backend/controllers/schemas.py`, add near the `SegnalazioneOut`/`InviaSegnalazioneRequest` block:

```python
class ScriviRecensioneRequest(BaseModel):
    voto: int
    commento: str | None = None


class RecensioneOut(BaseModel):
    id: str
    voto: int
    commento: str | None = None
    created_at: str
```

- [ ] **Step 2: Write the controller**

```python
# backend/controllers/recensione_controller.py
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from bll.servizio_recensione import ServizioRecensione, VotoNonValidoException
from middleware.auth_middleware import verify_token
from controllers.schemas import ScriviRecensioneRequest, RecensioneOut

# [IF-UT.15] RecensioneController
router = APIRouter(prefix="/utente", tags=["Recensioni"])
_servizio = ServizioRecensione()


@router.post("/recensioni", response_model=RecensioneOut, status_code=201)
def scrivi_recensione(
    body: ScriviRecensioneRequest,
    utente: dict = Depends(verify_token(["UT"])),
):
    """[IF-UT.15] Scrive Recensione."""
    try:
        return _servizio.scrivi_recensione(UUID(str(utente["id"])), body.voto, body.commento)
    except VotoNonValidoException as e:
        raise HTTPException(status_code=422, detail=str(e))
```

- [ ] **Step 3: Register the router in main.py**

In `backend/main.py`, add the import next to the other controller imports:

```python
from controllers.recensione_controller import router as recensione_router
```

And add the registration next to the other `app.include_router(...)` calls:

```python
app.include_router(recensione_router)
```

- [ ] **Step 4: Write the integration tests**

```python
# backend/tests/test_recensione.py
import pytest
import httpx

BASE_URL = "http://localhost:8000"


def _login(email: str, password: str) -> str:
    r = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()["access_token"]


class TestScriviRecensione:

    @pytest.mark.integration
    def test_scrive_recensione_scenario_base(self, utente_test):
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"{BASE_URL}/utente/recensioni",
            json={"voto": 5, "commento": "Servizio ottimo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201
        body = r.json()
        assert body["voto"] == 5
        assert body["commento"] == "Servizio ottimo"
        assert "id" in body
        assert "created_at" in body

    @pytest.mark.integration
    def test_scrive_recensione_senza_commento(self, utente_test):
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"{BASE_URL}/utente/recensioni",
            json={"voto": 3},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201
        assert r.json()["commento"] is None

    @pytest.mark.integration
    def test_scrive_recensione_voto_fuori_range(self, utente_test):
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"{BASE_URL}/utente/recensioni",
            json={"voto": 6, "commento": "x"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 422

    @pytest.mark.integration
    def test_scrive_recensione_non_autenticato(self):
        r = httpx.post(f"{BASE_URL}/utente/recensioni", json={"voto": 4})
        assert r.status_code == 401
```

- [ ] **Step 5: Run the tests against a running local backend**

Start the backend in one terminal: `cd backend && uv run uvicorn main:app --reload`
Run in another terminal: `cd backend && uv run pytest tests/test_recensione.py -v -m integration`
Expected: all 4 tests PASS

- [ ] **Step 6: Run the full unit test suite to check for regressions**

Run: `cd backend && uv run pytest tests/ -v -m "not integration"`
Expected: no new failures compared to before this change

- [ ] **Step 7: Commit**

```bash
git add backend/controllers/recensione_controller.py backend/controllers/schemas.py backend/main.py backend/tests/test_recensione.py
git commit -m "feat(recensione): endpoint POST /utente/recensioni con test [IF-UT.15]"
```

---

## Task 5: Frontend service

**Files:**
- Create: `frontend/src/services/RecensioneService.ts`

**Interfaces:**
- Consumes: `api` from `./ApiService` (axios instance, pattern identical to `SegnalazioneService.ts`)
- Produces: `scriviRecensione(voto: number, commento?: string): Promise<{ data: Recensione }>`

- [ ] **Step 1: Write the service**

```typescript
// frontend/src/services/RecensioneService.ts
import { api } from './ApiService'

export interface Recensione {
  id: string
  voto: number
  commento: string | null
  created_at: string
}

// [IF-UT.15] Scrive Recensione
export const scriviRecensione = (
  voto: number,
  commento?: string,
): Promise<{ data: Recensione }> =>
  api.post('/utente/recensioni', { voto, commento: commento || null })
```

- [ ] **Step 2: Type-check**

Run: `cd frontend && npx tsc -b --noEmit`
Expected: no new errors

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/RecensioneService.ts
git commit -m "feat(recensione): aggiunge RecensioneService [IF-UT.15]"
```

---

## Task 6: Frontend view — VistaRecensione

**Files:**
- Create: `frontend/src/views/utente/VistaRecensione.tsx`
- Create: `frontend/src/views/utente/VistaRecensione.css`

**Interfaces:**
- Consumes: `scriviRecensione` from `../../services/RecensioneService` (Task 5)
- Produces: default-exported React component `VistaRecensione` with no props (mounted at a route, like `VistaSegnalazione`)

- [ ] **Step 1: Write the CSS (mirrors VistaSegnalazione.css structure)**

```css
/* frontend/src/views/utente/VistaRecensione.css */
.vista-recensione-wrap {
  max-width: 480px;
  margin: 0 auto;
  padding: 24px 16px 80px;
}

.btn-back-rec {
  background: none;
  border: none;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 16px;
}

.rec-titolo {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 4px;
}

.rec-sottotitolo {
  color: #666;
  margin: 0 0 24px;
}

.rec-stelle {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.rec-stella {
  font-size: 36px;
  cursor: pointer;
  background: none;
  border: none;
  color: #ccc;
  padding: 0;
  line-height: 1;
}

.rec-stella--attiva {
  color: #f5a623;
}

.rec-label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
}

.rec-textarea {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  font-size: 14px;
  resize: vertical;
  box-sizing: border-box;
}

.rec-contatore {
  display: block;
  text-align: right;
  font-size: 12px;
  color: #888;
  margin-top: 4px;
}

.rec-errore {
  color: #e53935;
  font-size: 14px;
}

.btn-rec-primario {
  width: 100%;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 14px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 16px;
}

.btn-rec-primario:disabled {
  opacity: 0.6;
  cursor: default;
}

.btn-rec-secondario {
  width: 100%;
  background: none;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px;
  margin-top: 10px;
  cursor: pointer;
}

.rec-conferma {
  text-align: center;
  padding: 40px 0;
}

.rec-conferma-icona {
  font-size: 48px;
}

.rec-conferma-titolo {
  font-size: 20px;
  font-weight: 700;
  margin: 12px 0 4px;
}

.rec-conferma-testo {
  color: #666;
  margin-bottom: 24px;
}
```

- [ ] **Step 2: Write the component**

```tsx
// frontend/src/views/utente/VistaRecensione.tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { scriviRecensione } from '../../services/RecensioneService'
import './VistaRecensione.css'

// [IF-UT.15] Scrive Recensione
export default function VistaRecensione() {
  const navigate = useNavigate()

  const [voto, setVoto] = useState(0)
  const [commento, setCommento] = useState('')
  const [invioInCorso, setInvioInCorso] = useState(false)
  const [confermato, setConfermato] = useState(false)
  const [errore, setErrore] = useState('')

  const confermaScrivi = async (e: React.FormEvent) => {
    e.preventDefault()
    if (voto < 1 || voto > 5) {
      setErrore('Seleziona un voto da 1 a 5 stelle.')
      return
    }
    setInvioInCorso(true)
    setErrore('')
    try {
      await scriviRecensione(voto, commento.trim() || undefined)
      setConfermato(true)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore('Dati non validi. Controlla il voto e riprova.')
      } else {
        setErrore("Errore durante l'invio. Riprova.")
      }
    } finally {
      setInvioInCorso(false)
    }
  }

  return (
    <div className="vista-recensione-wrap">
      <button type="button" className="btn-back-rec" onClick={() => navigate(-1)}>
        ← Torna indietro
      </button>

      {confermato ? (
        <div className="rec-conferma">
          <span className="rec-conferma-icona">✅</span>
          <h2 className="rec-conferma-titolo">Recensione inviata</h2>
          <p className="rec-conferma-testo">
            Grazie per il tuo feedback, ci aiuta a migliorare il servizio.
          </p>
          <button
            type="button"
            className="btn-rec-secondario"
            onClick={() => navigate('/utente/home')}
          >
            Torna alla mappa
          </button>
        </div>
      ) : (
        <>
          <h1 className="rec-titolo">Lascia una recensione</h1>
          <p className="rec-sottotitolo">Aiutaci a migliorare il servizio.</p>

          <form onSubmit={confermaScrivi}>
            <span className="rec-label">Voto</span>
            <div className="rec-stelle">
              {[1, 2, 3, 4, 5].map(n => (
                <button
                  key={n}
                  type="button"
                  className={`rec-stella${n <= voto ? ' rec-stella--attiva' : ''}`}
                  onClick={() => setVoto(n)}
                  aria-label={`${n} stelle`}
                >
                  ★
                </button>
              ))}
            </div>

            <label className="rec-label" htmlFor="commento">Commento (facoltativo)</label>
            <textarea
              id="commento"
              className="rec-textarea"
              placeholder="Racconta la tua esperienza..."
              rows={5}
              maxLength={500}
              value={commento}
              onChange={e => setCommento(e.target.value)}
            />
            <span className="rec-contatore">{commento.length}/500</span>

            {errore && <p className="rec-errore">{errore}</p>}

            <button type="submit" className="btn-rec-primario" disabled={invioInCorso}>
              {invioInCorso ? 'Invio in corso...' : 'INVIA RECENSIONE'}
            </button>
          </form>
        </>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Type-check**

Run: `cd frontend && npx tsc -b --noEmit`
Expected: no new errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/utente/VistaRecensione.tsx frontend/src/views/utente/VistaRecensione.css
git commit -m "feat(recensione): aggiunge VistaRecensione [IF-UT.15]"
```

---

## Task 7: Wire up route and sidebar entry

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/views/utente/VistaHomePageUtente.tsx`

**Interfaces:**
- Consumes: `VistaRecensione` (Task 6)
- Produces: route `/utente/recensione`, sidebar menu entry navigating to it

- [ ] **Step 1: Add the import and route in App.tsx**

In `frontend/src/App.tsx`, add the import next to `import VistaSegnalazione from './views/utente/VistaSegnalazione'`:

```tsx
import VistaRecensione from './views/utente/VistaRecensione'
```

Add the route right after the `/utente/segnalazione` route block (around line 101, after its closing `/>`):

```tsx
        <Route
          path="/utente/recensione"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaRecensione />
            </RoutaProtetta>
          }
        />
```

- [ ] **Step 2: Add the sidebar menu entry in VistaHomePageUtente.tsx**

In `frontend/src/views/utente/VistaHomePageUtente.tsx`, add this button right after the "Invia segnalazione" sidebar voce block (around line 647, after its closing `</button>`):

```tsx
              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/recensione') }}
              >
                <span className="sidebar-voce__testo">Lascia recensione</span>
                <span className="sidebar-voce__icona">⭐</span>
              </button>
```

- [ ] **Step 3: Type-check and build**

Run: `cd frontend && npm run build`
Expected: build succeeds with no TypeScript errors

- [ ] **Step 4: Manual smoke test**

Run: `cd frontend && npm run dev` (and `cd backend && uv run uvicorn main:app --reload` in another terminal)
Open `http://localhost:5173`, log in as a UT user, open the sidebar menu, click "Lascia recensione", select a star rating, submit, and confirm the success screen appears.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/App.tsx frontend/src/views/utente/VistaHomePageUtente.tsx
git commit -m "feat(recensione): collega route e voce sidebar Lascia recensione [IF-UT.15]"
```

---

## Task 8: Update sprint documentation

**Files:**
- Modify: `docs/Sprint3_SMART_Mobility.md` (or wherever the implementation-status notes for Sprint items live — check the file for an existing "Note di implementazione" section per item)
- Modify: `c:\Users\camil_53qael0\SmartMobility\.claude\CLAUDE.md` — remove/update the line stating Recensione is "non ancora presente nel codice"

**Interfaces:** None (documentation only).

- [ ] **Step 1: Update CLAUDE.md**

In `.claude\CLAUDE.md`, find the paragraph under "Feature pianificate (progettate ma non ancora implementate)" about `Recensione` and update it to reflect that UT-15 (Scrive Recensione) is now implemented; OP-13 (Visualizza Recensioni, operator-side) remains pending.

- [ ] **Step 2: Add an implementation note to Sprint3_SMART_Mobility.md**

Find the UT-15 use case section (around line 2938) and add a short "Note di implementazione" line underneath the spec table noting: implemented in Sprint 3 via `POST /utente/recensioni`; files: `model/recensione.py`, `dal/recensione_repository.py`, `bll/servizio_recensione.py`, `controllers/recensione_controller.py`, `frontend/src/views/utente/VistaRecensione.tsx`.

- [ ] **Step 3: Commit**

```bash
git add docs/Sprint3_SMART_Mobility.md .claude/CLAUDE.md
git commit -m "docs: aggiorna stato implementazione UT-15 Scrive Recensione"
```

---

## Final Step: Push and open PR (only if user confirms)

After all tasks pass, do NOT push or open a PR automatically — ask the user first, per the project's git workflow (`Nessun commit diretto su main — ogni item passa da PR con review`).
