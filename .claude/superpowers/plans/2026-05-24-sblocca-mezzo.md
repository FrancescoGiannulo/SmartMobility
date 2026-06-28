# Sblocca Mezzo (IF-UT.04) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare il flusso completo Sblocca Mezzo (CS-10): backend DAL/BLL/Controller + frontend VistaCorsa + integrazione mappa, fedele al diagramma di sequenza `sequence_sblocca_mezzo.drawio`.

**Architecture:** `POST /utente/mezzi/{mezzo_id}/sblocca` → `PrenotazioneUtenteController` → `ServizioMobilita.sblocca_mezzo()` → `MezzoRepository` + `CorsaRepository` + `PrenotazioneRepository`. Frontend: click sul pin della mappa → `VistaCorsa` (pre-sblocco → corsa attiva).

**Tech Stack:** Python/FastAPI, SQLAlchemy raw SQL, Supabase PostgreSQL, React 19/TypeScript, @vis.gl/react-google-maps, React Router DOM.

---

## File Map

| File | Azione |
|------|--------|
| `backend/dal/mezzo_repository.py` | Modifica — aggiunge `trova_per_id`, `aggiorna_stato` |
| `backend/dal/corsa_repository.py` | Implementa (era stub vuoto) |
| `backend/dal/prenotazione_repository.py` | Implementa (era stub vuoto) |
| `backend/bll/servizio_mobilita.py` | Implementa (era stub vuoto) |
| `backend/controllers/prenotazione_utente_controller.py` | Implementa endpoint, cambia prefix a `/utente` |
| `backend/main.py` | Modifica — registra `corsa_router` |
| `backend/tests/test_sblocca_mezzo.py` | Crea — test integrazione su Supabase reale |
| `frontend/src/services/CorsaService.ts` | Crea — `sbloccaMezzo()` |
| `frontend/src/views/utente/VistaCorsa.tsx` | Crea — schermata pre-sblocco + corsa attiva |
| `frontend/src/views/utente/VistaCorsa.css` | Crea — stili IUI-8 |
| `frontend/src/views/utente/VistaMappa.tsx` | Modifica — aggiunge `onClick` su `AdvancedMarker` |
| `frontend/src/App.tsx` | Modifica — aggiunge rotta `/utente/corsa/:idMezzo` |

---

## Task 1: DAL — MezzoRepository: trova_per_id + aggiorna_stato

**Files:**
- Modify: `backend/dal/mezzo_repository.py`
- Test: `backend/tests/test_sblocca_mezzo.py` (sezione TestMezzoRepository)

- [ ] **Step 1: Crea il file di test con i test per MezzoRepository**

Crea `backend/tests/test_sblocca_mezzo.py`:

```python
import pytest
import uuid as _uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session


# ── Helpers ────────────────────────────────────────────────────────────────

def _login(email: str, password: str) -> str:
    import httpx
    r = httpx.post("http://localhost:8000/auth/login",
                   json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _inserisci_mezzo(db, codice: str, stato: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, 41.11, 16.85, 80)
        """), {"codice": codice, "stato": stato})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"),
                  {"id": mezzo_id})
        s.execute(text("DELETE FROM prenotazioni WHERE mezzo_id = :id"),
                  {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


# ── TestMezzoRepository ────────────────────────────────────────────────────

class TestMezzoRepository:

    def test_trova_per_id_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-TR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            mezzo = repo.trova_per_id(_uuid.UUID(mezzo_id))
            assert mezzo is not None
            assert mezzo["stato"] == "Disponibile"
            assert mezzo["codice"] == codice
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_trova_per_id_non_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        repo = MezzoRepository(db)
        risultato = repo.trova_per_id(_uuid.uuid4())
        assert risultato is None

    def test_aggiorna_stato(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-AS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            repo.aggiorna_stato(_uuid.UUID(mezzo_id), "In uso")
            mezzo = repo.trova_per_id(_uuid.UUID(mezzo_id))
            assert mezzo["stato"] == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Esegui i test — devono fallire (metodi non definiti)**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestMezzoRepository -v
```

Atteso: `FAILED` con `AttributeError: 'MezzoRepository' object has no attribute 'trova_per_id'`

- [ ] **Step 3: Implementa trova_per_id e aggiorna_stato in MezzoRepository**

Aggiungi in fondo a `backend/dal/mezzo_repository.py`, dopo il metodo `lista_per_mappa`:

```python
    def trova_per_id(self, mezzo_id: UUID) -> dict | None:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi WHERE id = :id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(mezzo_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "codice": row.codice,
            "tipo": row.tipo,
            "stato": row.stato,
            "lat": row.lat,
            "lng": row.lng,
            "batteria": row.batteria,
        }

    def aggiorna_stato(self, mezzo_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE mezzi SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"stato": nuovo_stato, "id": str(mezzo_id)})
            s.commit()
```

Aggiungi `from uuid import UUID` all'import esistente in cima al file (già presente `from sqlalchemy import Engine, text`):

```python
from uuid import UUID
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestMezzoRepository -v
```

Atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/dal/mezzo_repository.py backend/tests/test_sblocca_mezzo.py
git commit -m "feat(dal): MezzoRepository.trova_per_id e aggiorna_stato [IF-UT.04]"
```

---

## Task 2: DAL — CorsaRepository

**Files:**
- Implement: `backend/dal/corsa_repository.py`
- Test: `backend/tests/test_sblocca_mezzo.py` (sezione TestCorsaRepository)

- [ ] **Step 1: Aggiungi i test per CorsaRepository in test_sblocca_mezzo.py**

Aggiungi in fondo al file `backend/tests/test_sblocca_mezzo.py`:

```python
# ── TestCorsaRepository ────────────────────────────────────────────────────

class TestCorsaRepository:

    def test_crea_corsa_diretta(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-CR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = CorsaRepository(db)
            corsa = repo.crea(utente_test["id"], _uuid.UUID(mezzo_id), None)
            assert corsa["stato"] == "in_uso"
            assert str(corsa["utente_id"]) == str(utente_test["id"])
            assert str(corsa["mezzo_id"]) == mezzo_id
            assert corsa["prenotazione_id"] is None
            assert "inizio_at" in corsa
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestCorsaRepository -v
```

Atteso: `FAILED` — `CorsaRepository` non ha il metodo `crea`

- [ ] **Step 3: Implementa CorsaRepository**

Sostituisci il contenuto di `backend/dal/corsa_repository.py`:

```python
import uuid as _uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class CorsaRepository:

    def __init__(self, db: Session | Engine) -> None:
        self._engine = db if isinstance(db, Engine) else None
        self._session = db if not isinstance(db, Engine) else None

    @contextmanager
    def _sessione(self):
        if self._session is not None:
            yield self._session
        else:
            with Session(self._engine) as s:
                yield s

    # [IF-UT.04] CS-10 — crea corsa all'avvio del mezzo
    def crea(
        self,
        utente_id: UUID,
        mezzo_id: UUID,
        prenotazione_id: UUID | None,
    ) -> dict:
        sql = text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, prenotazione_id, stato, inizio_at)
            VALUES
                (:id, :utente_id, :mezzo_id, :prenotazione_id, 'in_uso', :inizio_at)
            RETURNING id, utente_id, mezzo_id, prenotazione_id, stato, inizio_at
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "id": str(_uuid.uuid4()),
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
                "prenotazione_id": str(prenotazione_id) if prenotazione_id else None,
                "inizio_at": datetime.now(timezone.utc),
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "prenotazione_id": str(row.prenotazione_id) if row.prenotazione_id else None,
            "stato": row.stato,
            "inizio_at": row.inizio_at.isoformat(),
        }
```

- [ ] **Step 4: Esegui il test — deve passare**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestCorsaRepository -v
```

Atteso: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/dal/corsa_repository.py backend/tests/test_sblocca_mezzo.py
git commit -m "feat(dal): CorsaRepository.crea [IF-UT.04]"
```

---

## Task 3: DAL — PrenotazioneRepository

**Files:**
- Implement: `backend/dal/prenotazione_repository.py`
- Test: `backend/tests/test_sblocca_mezzo.py` (sezione TestPrenotazioneRepository)

- [ ] **Step 1: Aggiungi i test per PrenotazioneRepository**

Aggiungi in fondo a `backend/tests/test_sblocca_mezzo.py`:

```python
# ── TestPrenotazioneRepository ─────────────────────────────────────────────

class TestPrenotazioneRepository:

    def test_trova_attiva_trovata(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        codice = f"TEST-PR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            repo = PrenotazioneRepository(db)
            pren = repo.trova_attiva_per_utente_e_mezzo(
                utente_test["id"], _uuid.UUID(mezzo_id)
            )
            assert pren is not None
            assert str(pren["utente_id"]) == str(utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_trova_attiva_non_trovata(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        repo = PrenotazioneRepository(db)
        risultato = repo.trova_attiva_per_utente_e_mezzo(
            utente_test["id"], _uuid.uuid4()
        )
        assert risultato is None

    def test_aggiorna_stato_prenotazione(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        codice = f"TEST-APR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
            pren_id = s.execute(text("""
                SELECT id FROM prenotazioni
                WHERE mezzo_id = :mid AND utente_id = :uid
            """), {"mid": mezzo_id, "uid": str(utente_test["id"])}).fetchone().id
        try:
            repo = PrenotazioneRepository(db)
            repo.aggiorna_stato(_uuid.UUID(str(pren_id)), "convertita")
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM prenotazioni WHERE id = :id"),
                    {"id": str(pren_id)}
                ).fetchone()
            assert row.stato == "convertita"
        finally:
            _elimina_mezzo(db, mezzo_id)
```

Aggiungi anche l'import mancante in cima al file (dopo gli import esistenti):

```python
from datetime import datetime, timezone, timedelta
```

- [ ] **Step 2: Esegui i test — devono fallire**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestPrenotazioneRepository -v
```

Atteso: `FAILED` — `PrenotazioneRepository` non ha i metodi richiesti

- [ ] **Step 3: Implementa PrenotazioneRepository**

Sostituisci il contenuto di `backend/dal/prenotazione_repository.py`:

```python
from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class PrenotazioneRepository:

    def __init__(self, db: Session | Engine) -> None:
        self._engine = db if isinstance(db, Engine) else None
        self._session = db if not isinstance(db, Engine) else None

    @contextmanager
    def _sessione(self):
        if self._session is not None:
            yield self._session
        else:
            with Session(self._engine) as s:
                yield s

    # [IF-UT.04] CS-10 — verifica prenotazione attiva per sblocco da prenotazione
    def trova_attiva_per_utente_e_mezzo(
        self, utente_id: UUID, mezzo_id: UUID
    ) -> dict | None:
        sql = text("""
            SELECT id, utente_id, mezzo_id, stato
            FROM prenotazioni
            WHERE utente_id = :utente_id
              AND mezzo_id = :mezzo_id
              AND stato = 'attiva'
              AND scade_at > now()
            LIMIT 1
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
            }).fetchone()
        if row is None:
            return None
        return {
            "id": row.id,
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
        }

    def aggiorna_stato(self, prenotazione_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE prenotazioni SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {
                "stato": nuovo_stato,
                "id": str(prenotazione_id),
            })
            s.commit()
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestPrenotazioneRepository -v
```

Atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/dal/prenotazione_repository.py backend/tests/test_sblocca_mezzo.py
git commit -m "feat(dal): PrenotazioneRepository [IF-UT.04]"
```

---

## Task 4: BLL — ServizioMobilita.sblocca_mezzo

**Files:**
- Implement: `backend/bll/servizio_mobilita.py`
- Test: `backend/tests/test_sblocca_mezzo.py` (sezione TestServizioMobilita)

- [ ] **Step 1: Aggiungi i test per ServizioMobilita**

Aggiungi in fondo a `backend/tests/test_sblocca_mezzo.py`:

```python
# ── TestServizioMobilita ───────────────────────────────────────────────────

class TestServizioMobilita:

    def test_sblocca_mezzo_disponibile(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SM-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            svc = ServizioMobilita(db)
            corsa = svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
            assert corsa["stato"] == "in_uso"
            assert corsa["prenotazione_id"] is None
            # Verifica stato mezzo aggiornato nel DB
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM mezzi WHERE id = :id"),
                    {"id": mezzo_id}
                ).fetchone()
            assert row.stato == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_prenotato_da_utente(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SMP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            svc = ServizioMobilita(db)
            corsa = svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
            assert corsa["stato"] == "in_uso"
            assert corsa["prenotazione_id"] is not None
            # Verifica prenotazione convertita
            with Session(db) as s:
                row = s.execute(text("""
                    SELECT stato FROM prenotazioni
                    WHERE mezzo_id = :mid AND utente_id = :uid
                """), {"mid": mezzo_id, "uid": str(utente_test["id"])}).fetchone()
            assert row.stato == "convertita"
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_non_trovato(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonTrovatoException
        svc = ServizioMobilita(db)
        with pytest.raises(MezzoNonTrovatoException):
            svc.sblocca_mezzo(_uuid.uuid4(), utente_test["id"])

    def test_sblocca_mezzo_non_disponibile(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonDisponibileException
        codice = f"TEST-SMN-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            svc = ServizioMobilita(db)
            with pytest.raises(MezzoNonDisponibileException):
                svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_prenotato_senza_prenotazione(self, db, utente_test):
        """Mezzo Prenotato ma l'utente non ha una prenotazione attiva per esso."""
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonDisponibileException
        codice = f"TEST-SMX-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        try:
            svc = ServizioMobilita(db)
            with pytest.raises(MezzoNonDisponibileException):
                svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Esegui i test — devono fallire**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestServizioMobilita -v
```

Atteso: `FAILED` — `ServizioMobilita` non ha il metodo `sblocca_mezzo`

- [ ] **Step 3: Implementa ServizioMobilita**

Sostituisci il contenuto di `backend/bll/servizio_mobilita.py`:

```python
from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.corsa_repository import CorsaRepository
from dal.prenotazione_repository import PrenotazioneRepository


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class ServizioMobilita:
    """Orchestrazione principale del ciclo di vita dei mezzi e delle corse."""

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._corsa_repo = CorsaRepository(db)
        self._pren_repo = PrenotazioneRepository(db)

    # [IF-UT.04] CS-10 — Sblocca Mezzo
    def sblocca_mezzo(self, mezzo_id: UUID, utente_id: UUID) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")

        stato = mezzo["stato"]
        prenotazione_id = None

        if stato == "Disponibile":
            pass  # sblocco diretto — CS-10 scenario base
        elif stato == "Prenotato":
            pren = self._pren_repo.trova_attiva_per_utente_e_mezzo(
                utente_id, mezzo_id
            )
            if pren is None:
                raise MezzoNonDisponibileException(
                    "Mezzo prenotato da un altro utente"
                )
            prenotazione_id = pren["id"]
        else:
            raise MezzoNonDisponibileException(
                f"Mezzo non disponibile (stato: {stato})"
            )

        corsa = self._corsa_repo.crea(utente_id, mezzo_id, prenotazione_id)

        if prenotazione_id:
            self._pren_repo.aggiorna_stato(prenotazione_id, "convertita")

        self._mezzo_repo.aggiorna_stato(mezzo_id, "In uso")

        return corsa
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestServizioMobilita -v
```

Atteso: `5 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_mobilita.py backend/tests/test_sblocca_mezzo.py
git commit -m "feat(bll): ServizioMobilita.sblocca_mezzo [IF-UT.04]"
```

---

## Task 5: Controller + registrazione in main.py

**Files:**
- Implement: `backend/controllers/prenotazione_utente_controller.py`
- Modify: `backend/main.py`

- [ ] **Step 1: Implementa il controller**

Sostituisci il contenuto di `backend/controllers/prenotazione_utente_controller.py`:

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_mobilita import (
    ServizioMobilita,
    MezzoNonTrovatoException,
    MezzoNonDisponibileException,
)

router = APIRouter(prefix="/utente", tags=["Utente - Corsa"])

# [IF-UT.02] Prenota Mezzo — da implementare
# [IF-UT.06] Termina Corsa — da implementare

# [IF-UT.04] CS-10 Sblocca Mezzo
@router.post("/mezzi/{mezzo_id}/sblocca", status_code=201)
def sblocca_mezzo(
    mezzo_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        corsa = ServizioMobilita(db).sblocca_mezzo(mezzo_id, utente["id"])
        return corsa
    except MezzoNonTrovatoException:
        raise HTTPException(status_code=404, detail="Mezzo non trovato")
    except MezzoNonDisponibileException as e:
        raise HTTPException(status_code=409, detail=str(e))
```

- [ ] **Step 2: Registra il router in main.py**

In `backend/main.py`, aggiungi l'import dopo gli altri router:

```python
from controllers.prenotazione_utente_controller import router as corsa_router
```

E aggiungi dopo `app.include_router(zona_op_router)`:

```python
app.include_router(corsa_router)
```

Il file `main.py` completo diventa:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as auth_router, mappa_router
from controllers.mezzo_operatore_controller import router as mezzo_op_router
from controllers.zona_operatore_controller import router as zona_op_router
from controllers.prenotazione_utente_controller import router as corsa_router

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
app.include_router(corsa_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
```

- [ ] **Step 3: Verifica che il server si avvii senza errori**

```bash
cd backend && uv run uvicorn main:app --reload
```

Atteso: nessun errore, server attivo su `http://localhost:8000`. Verifica che `/docs` mostri `POST /utente/mezzi/{mezzo_id}/sblocca`.

- [ ] **Step 4: Commit**

```bash
git add backend/controllers/prenotazione_utente_controller.py backend/main.py
git commit -m "feat(controller): POST /utente/mezzi/{id}/sblocca [IF-UT.04]"
```

---

## Task 6: Test di integrazione HTTP

**Files:**
- Test: `backend/tests/test_sblocca_mezzo.py` (sezione TestSbloccaMezzoHTTP)

> **Prerequisito:** il server deve essere in esecuzione su `http://localhost:8000` prima di eseguire questi test.

- [ ] **Step 1: Aggiungi i test HTTP in fondo a test_sblocca_mezzo.py**

```python
# ── TestSbloccaMezzoHTTP ───────────────────────────────────────────────────

class TestSbloccaMezzoHTTP:

    def test_sblocca_disponibile_201(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert data["stato"] == "in_uso"
            assert str(data["mezzo_id"]) == mezzo_id
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_da_prenotazione_201(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert data["stato"] == "in_uso"
            assert data["prenotazione_id"] is not None
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_in_uso_409(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_prenotato_da_altri_409(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_sblocca_mezzo_inesistente_404(self, utente_test):
        import httpx
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"http://localhost:8000/utente/mezzi/{_uuid.uuid4()}/sblocca",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    def test_sblocca_non_autenticato_401(self, db):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            import httpx
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca"
            )
            assert r.status_code == 401
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Avvia il server (in un terminale separato)**

```bash
cd backend && uv run uvicorn main:app --reload
```

- [ ] **Step 3: Esegui i test HTTP**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py::TestSbloccaMezzoHTTP -v
```

Atteso: `6 passed`

- [ ] **Step 4: Esegui tutti i test del file**

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py -v
```

Atteso: tutti i test passano

- [ ] **Step 5: Commit**

```bash
git add backend/tests/test_sblocca_mezzo.py
git commit -m "test: test integrazione HTTP sblocca mezzo [IF-UT.04]"
```

---

## Task 7: Frontend — CorsaService.ts

**Files:**
- Create: `frontend/src/services/CorsaService.ts`

- [ ] **Step 1: Crea CorsaService.ts**

Crea `frontend/src/services/CorsaService.ts`:

```typescript
import { api } from './ApiService'

export interface CorsaAttiva {
  id: string
  mezzo_id: string
  utente_id: string
  prenotazione_id: string | null
  stato: 'in_uso'
  inizio_at: string
}

// [IF-UT.04] CS-10 Sblocca Mezzo
export const sbloccaMezzo = async (mezzoId: string): Promise<CorsaAttiva> => {
  const r = await api.post<CorsaAttiva>(`/utente/mezzi/${mezzoId}/sblocca`)
  return r.data
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/services/CorsaService.ts
git commit -m "feat(fe): CorsaService.sbloccaMezzo [IF-UT.04]"
```

---

## Task 8: Frontend — VistaCorsa.tsx + CSS

**Files:**
- Create: `frontend/src/views/utente/VistaCorsa.tsx`
- Create: `frontend/src/views/utente/VistaCorsa.css`

- [ ] **Step 1: Crea VistaCorsa.css**

Crea `frontend/src/views/utente/VistaCorsa.css`:

```css
.vista-corsa {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
}

.btn-back {
  align-self: flex-start;
  background: none;
  border: none;
  color: #4caf9a;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 24px;
  padding: 0;
}

.corsa-card {
  background: #fff;
  border-radius: 20px;
  padding: 32px 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.corsa-emoji {
  font-size: 64px;
  line-height: 1;
}

.corsa-card h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  text-transform: capitalize;
  color: #222;
}

.corsa-codice,
.corsa-batteria {
  margin: 0;
  font-size: 15px;
  color: #666;
}

.corsa-errore {
  color: #e53935;
  font-size: 14px;
  text-align: center;
  margin: 0;
}

.btn-sblocca {
  margin-top: 12px;
  width: 100%;
  padding: 16px;
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-sblocca:disabled {
  background: #a5d6cc;
  cursor: not-allowed;
}

.btn-sblocca:hover:not(:disabled) {
  background: #3d9e8a;
}

/* Stato corsa attiva */
.vista-corsa.attiva .corsa-card {
  border-top: 6px solid #4caf9a;
}

.corsa-info {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}

.corsa-info td {
  padding: 10px 4px;
  border-bottom: 1px solid #f0f0f0;
}

.corsa-info td:first-child {
  color: #888;
  width: 50%;
}

.corsa-info td:last-child {
  font-weight: 600;
  color: #222;
  text-align: right;
}

.corsa-azioni {
  display: flex;
  gap: 12px;
  width: 100%;
  margin-top: 8px;
}

.btn-pausa,
.btn-termina {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-pausa {
  background: #fff3e0;
  color: #e65100;
  border: 2px solid #e65100;
}

.btn-termina {
  background: #4caf9a;
  color: #fff;
}

.btn-pausa:disabled,
.btn-termina:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
```

- [ ] **Step 2: Crea VistaCorsa.tsx**

Crea `frontend/src/views/utente/VistaCorsa.tsx`:

```tsx
import { useState, useEffect, useCallback } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import { sbloccaMezzo, type CorsaAttiva } from '../../services/CorsaService'
import type { MezzoMappa } from '../../services/MapService'
import './VistaCorsa.css'

type Fase = 'pre_sblocco' | 'attiva'

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60).toString().padStart(2, '0')
  const s = (sec % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

function emojiMezzo(tipo?: string): string {
  if (tipo === 'monopattino') return '🛴'
  if (tipo === 'bicicletta') return '🚲'
  if (tipo === 'automobile') return '🚗'
  return '🚲'
}

// [IF-UT.04] CS-10 — Sblocca Mezzo / IUI-8
export default function VistaCorsa() {
  const { idMezzo } = useParams<{ idMezzo: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const mezzo = location.state?.mezzo as MezzoMappa | undefined

  const [fase, setFase] = useState<Fase>('pre_sblocco')
  const [corsa, setCorsa] = useState<CorsaAttiva | null>(null)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    if (fase !== 'attiva') return
    const t = setInterval(() => setElapsed(e => e + 1), 1000)
    return () => clearInterval(t)
  }, [fase])

  const handleSblocca = useCallback(async () => {
    if (!idMezzo) return
    setCaricamento(true)
    setErrore('')
    try {
      const c = await sbloccaMezzo(idMezzo)
      setCorsa(c)
      setFase('attiva')
    } catch (err: any) {
      if (err?.response?.status === 409) {
        setErrore('Mezzo non più disponibile. Torna alla mappa.')
      } else if (err?.response?.status === 404) {
        setErrore('Mezzo non trovato.')
      } else {
        setErrore('Errore durante lo sblocco. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }, [idMezzo])

  if (fase === 'pre_sblocco') {
    return (
      <div className="vista-corsa">
        <button className="btn-back" onClick={() => navigate(-1)}>
          ← Torna alla mappa
        </button>
        <div className="corsa-card">
          <div className="corsa-emoji">{emojiMezzo(mezzo?.tipo)}</div>
          <h2>{mezzo?.tipo ?? 'Mezzo'}</h2>
          <p className="corsa-codice">ID: {mezzo?.codice ?? idMezzo}</p>
          {mezzo?.batteria != null && (
            <p className="corsa-batteria">🔋 {mezzo.batteria}%</p>
          )}
          {errore && <p className="corsa-errore">{errore}</p>}
          <button
            className="btn-sblocca"
            onClick={handleSblocca}
            disabled={caricamento}
          >
            {caricamento ? 'Sblocco in corso...' : 'SBLOCCA'}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="vista-corsa attiva">
      <div className="corsa-card">
        <div className="corsa-emoji">{emojiMezzo(mezzo?.tipo)}</div>
        <table className="corsa-info">
          <tbody>
            <tr>
              <td>ID mezzo</td>
              <td>{mezzo?.codice ?? corsa?.mezzo_id}</td>
            </tr>
            <tr>
              <td>Batteria</td>
              <td>{mezzo?.batteria != null ? `${mezzo.batteria}%` : '—'}</td>
            </tr>
            <tr>
              <td>Tempo</td>
              <td>{formatTime(elapsed)}</td>
            </tr>
            <tr>
              <td>Km</td>
              <td>0.0</td>
            </tr>
          </tbody>
        </table>
        <div className="corsa-azioni">
          <button className="btn-pausa" disabled>PAUSA CORSA</button>
          <button className="btn-termina" disabled>TERMINA E PAGA</button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/utente/VistaCorsa.tsx frontend/src/views/utente/VistaCorsa.css
git commit -m "feat(fe): VistaCorsa pre-sblocco e attiva [IF-UT.04] IUI-8"
```

---

## Task 9: Frontend — VistaMappa onClick + App.tsx rotta

**Files:**
- Modify: `frontend/src/views/utente/VistaMappa.tsx`
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Aggiungi onClick sui marker in VistaMappa.tsx**

In `frontend/src/views/utente/VistaMappa.tsx`, sostituisci il blocco dei marker (righe 88-92):

```tsx
        {mezzi.map(m => (
          <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
            <PinMezzo tipo={m.tipo} />
          </AdvancedMarker>
        ))}
```

Con:

```tsx
        {mezzi.map(m => (
          <AdvancedMarker
            key={m.id}
            position={{ lat: m.lat, lng: m.lng }}
            onClick={() => navigate(`/utente/corsa/${m.id}`, { state: { mezzo: m } })}
          >
            <PinMezzo tipo={m.tipo} />
          </AdvancedMarker>
        ))}
```

- [ ] **Step 2: Aggiungi la rotta /utente/corsa/:idMezzo in App.tsx**

In `frontend/src/App.tsx`, aggiungi l'import di `VistaCorsa` dopo l'import di `VistaMappaOperatore`:

```tsx
import VistaCorsa from './views/utente/VistaCorsa'
```

Aggiungi la rotta **prima** della rotta `/utente/*` (riga 69), altrimenti il catch-all la intercetterebbe:

```tsx
        <Route
          path="/utente/corsa/:idMezzo"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaCorsa />
            </RoutaProtetta>
          }
        />
```

- [ ] **Step 3: Verifica che il frontend si compili senza errori**

```bash
cd frontend && npm run build
```

Atteso: build completata senza errori TypeScript.

- [ ] **Step 4: Testa manualmente il flusso**

1. Avvia backend: `cd backend && uv run uvicorn main:app --reload`
2. Avvia frontend: `cd frontend && npm run dev`
3. Accedi come utente (UT) → homepage mappa
4. Clicca su un pin mezzo → naviga a `/utente/corsa/{id}` con schermata pre-sblocco
5. Clicca **SBLOCCA** → transizione a corsa attiva con timer
6. Verifica su Supabase che la tabella `corse` abbia una nuova riga con `stato = 'in_uso'`
7. Verifica che il mezzo abbia stato `In uso`

- [ ] **Step 5: Commit finale**

```bash
git add frontend/src/views/utente/VistaMappa.tsx frontend/src/App.tsx
git commit -m "feat(fe): VistaMappa onClick + rotta VistaCorsa [IF-UT.04]"
```

---

## Verifica finale

```bash
cd backend && uv run pytest tests/test_sblocca_mezzo.py -v
```

Atteso: tutti i test passano (DAL + BLL + HTTP).
