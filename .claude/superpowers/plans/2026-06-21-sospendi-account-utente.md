# IF-OP.09 Sospende Account Utente — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement IF-OP.09 "Sospende Account Utente" end-to-end (DB → DAL → BLL → Controller → frontend), so an Operatore can suspend a Utente's account with a motivazione, persisting a notification record, blocking future logins (already partially wired).

**Architecture:** Follows the existing Client-Server + MVC + layered pattern of this repo. Backend: raw-SQL DAL methods on `AttoreRepository` (existing pattern, no ORM session queries for business data), a new `NotificaRepository`/`NotificaService` pair, new methods on `ServizioUtenti` (BLL), a new `UtentiOPController`. Frontend: a new `GestioneUtentiService.ts` (exact name from the sequence diagram) and `VistaGestioneUtentiOperatore.tsx`, wired into the existing placeholder button and router.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 (raw `text()` queries for this entity, matching `attore_repository.py`), pytest (`-m integration` for DB-touching tests, requires `backend/.env` with `DATABASE_URL`/`SUPABASE_*` and, for HTTP tests, a running `uv run uvicorn main:app` on `localhost:8000`), React 19 + TypeScript + Axios.

## Global Constraints

- Controller layer: solo validazione HTTP e smistamento, zero logica di business.
- BLL: tutta la logica applicativa, nessun accesso diretto al DB.
- DAL: solo accesso ai dati, nessuna logica di business.
- Nomi delle classi/metodi devono corrispondere esattamente al diagramma delle classi: `ServizioUtenti.sospendiAccount` → `sospendi_account`, `AttoreRepository.sospendi` → `sospendi`, `NotificaService.notifica` → `notifica`, frontend service si chiama `GestioneUtentiService` (lifeline esatta nel diagramma di sequenza).
- Non mockare il database nei test che verificano comportamento persistente — usare i fixture reali in `backend/tests/conftest.py` (`utente_test`, `utente_sospeso`, `operatore_test`) e marcare i test con `@pytest.mark.integration`.
- Ogni metodo/classe nuova deve riportare il commento di tracciabilità `# [IF-OP.09]` nel punto architetturalmente rilevante (non ovunque).
- Riattivazione account e invalidazione di sessioni JWT già attive sono esplicitamente fuori scope (vedi spec `docs/superpowers/specs/2026-06-21-sospendi-account-utente-design.md`).

---

### Task 1: Migrazione DB + modelli ORM/dataclass per `Notifica` e colonne di sospensione

**Files:**
- Create: `backend/migrations/015_sospensione_account.sql`
- Create: `backend/model/notifica.py`
- Modify: `backend/model/orm.py` (aggiunge colonne a `Utente`, aggiunge classe `Notifica`)
- Test: `backend/tests/test_schema.py` (aggiorna `test_utente_columns`, aggiunge `test_notifica_columns`, `test_notifica_tablename`)

**Interfaces:**
- Produces: `model.notifica.Notifica` dataclass (`id: UUID`, `id_utente: UUID`, `messaggio: str`, `letta: bool = False`, `data: datetime | None = None`) — usata da `NotificaRepository` (Task 2).
- Produces: `model.orm.Notifica` ORM class, tabella `notifiche`, colonne `id, utente_id, messaggio, letta, created_at`.
- Produces: colonne `utenti.motivazione_sospensione` (TEXT, nullable) e `utenti.sospeso_at` (TIMESTAMPTZ, nullable) — usate da `AttoreRepository.sospendi` (Task 4).

- [ ] **Step 1: Scrivi la migrazione SQL**

`backend/migrations/015_sospensione_account.sql`:
```sql
-- 015_sospensione_account.sql — IF-OP.09 Sospende Account Utente
ALTER TABLE utenti ADD COLUMN IF NOT EXISTS motivazione_sospensione TEXT;
ALTER TABLE utenti ADD COLUMN IF NOT EXISTS sospeso_at TIMESTAMPTZ;

CREATE TABLE IF NOT EXISTS notifiche (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
  messaggio   TEXT NOT NULL,
  letta       BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS notifiche_utente_idx ON notifiche (utente_id, created_at);
```

- [ ] **Step 2: Applica la migrazione su Supabase**

Esegui il contenuto del file SQL nell'SQL editor di Supabase (pattern già seguito per le migrazioni precedenti — non c'è un runner automatico in questo repo). Verifica manualmente che la tabella `notifiche` e le due colonne esistano prima di proseguire.

- [ ] **Step 3: Crea la dataclass `Notifica`**

`backend/model/notifica.py`:
```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Notifica:
    """[IF-OP.09] Notifica persistita per l'Utente (es. sospensione account)."""

    id: UUID
    id_utente: UUID
    messaggio: str
    letta: bool = False
    data: datetime | None = None
```

- [ ] **Step 4: Aggiungi le colonne a `Utente` e la classe ORM `Notifica` in `model/orm.py`**

Modifica `backend/model/orm.py`: aggiungi due righe alla classe `Utente` esistente (dopo `sospeso`) e una nuova classe `Notifica` in fondo al file:
```python
class Utente(Base):
    """[IF-UT.17] Profilo dell'utente finale."""

    __tablename__ = "utenti"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    cognome: Mapped[str] = mapped_column(Text, nullable=False)
    telefono: Mapped[str | None] = mapped_column(Text, nullable=True)
    sospeso: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    motivazione_sospensione: Mapped[str | None] = mapped_column(Text, nullable=True)
    sospeso_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
```

E in fondo al file (dopo `AmministrazionePubblica`):
```python
class Notifica(Base):
    """[IF-OP.09] Notifica persistita per l'Utente."""

    __tablename__ = "notifiche"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    utente_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    messaggio: Mapped[str] = mapped_column(Text, nullable=False)
    letta: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
```

- [ ] **Step 5: Aggiorna i test di schema**

Modifica `backend/tests/test_schema.py`, riga `test_utente_columns`:
```python
def test_utente_columns():
    from model.orm import Utente
    cols = {c.name for c in Utente.__table__.columns}
    assert cols == {
        "id", "nome", "cognome", "telefono", "sospeso",
        "motivazione_sospensione", "sospeso_at", "created_at",
    }
```

Aggiungi in fondo al file:
```python
def test_notifica_tablename():
    from model.orm import Notifica
    assert Notifica.__tablename__ == "notifiche"


def test_notifica_columns():
    from model.orm import Notifica
    cols = {c.name for c in Notifica.__table__.columns}
    assert cols == {"id", "utente_id", "messaggio", "letta", "created_at"}
```

- [ ] **Step 6: Esegui i test di schema**

Run: `cd backend && uv run pytest tests/test_schema.py -v -m "not integration"`
Expected: PASS su tutti i test (nessuno richiede DB live per queste assert, sono check sulle classi ORM Python).

- [ ] **Step 7: Commit**

```bash
git add backend/migrations/015_sospensione_account.sql backend/model/notifica.py backend/model/orm.py backend/tests/test_schema.py
git commit -m "feat(IF-OP.09): aggiunge schema DB per sospensione account e notifiche"
```

---

### Task 2: `NotificaRepository` (DAL)

**Files:**
- Create: `backend/dal/notifica_repository.py`
- Test: `backend/tests/test_notifica_repository.py`

**Interfaces:**
- Consumes: tabella `notifiche` creata in Task 1; fixture `utente_test` da `conftest.py` (`{"id": UUID, "email": str, "password": str}`).
- Produces: `NotificaRepository.crea(id_utente: UUID, messaggio: str) -> Notifica`, `NotificaRepository.find_by_utente(id_utente: UUID) -> list[Notifica]` — usati da `NotificaService` (Task 3).

- [ ] **Step 1: Scrivi il test (fallente) per `crea` e `find_by_utente`**

`backend/tests/test_notifica_repository.py`:
```python
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestNotificaRepository:

    def test_crea_e_find_by_utente(self, db, utente_test):
        repo = NotificaRepository()
        try:
            notifica = repo.crea(utente_test["id"], "Messaggio di test")
            assert notifica.id_utente == utente_test["id"]
            assert notifica.messaggio == "Messaggio di test"
            assert notifica.letta is False

            trovate = repo.find_by_utente(utente_test["id"])
            assert any(n.id == notifica.id for n in trovate)
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()

    def test_find_by_utente_vuoto_se_nessuna_notifica(self, db, utente_test):
        repo = NotificaRepository()
        assert repo.find_by_utente(utente_test["id"]) == []
```

- [ ] **Step 2: Esegui il test per verificarne il fallimento**

Run: `cd backend && uv run pytest tests/test_notifica_repository.py -v -m integration`
Expected: FAIL con `ModuleNotFoundError: No module named 'dal.notifica_repository'`

- [ ] **Step 3: Implementa `NotificaRepository`**

`backend/dal/notifica_repository.py`:
```python
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.notifica import Notifica


class NotificaRepository:
    """[IF-OP.09] Persistenza delle notifiche utente."""

    def crea(self, id_utente: UUID, messaggio: str) -> Notifica:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "INSERT INTO notifiche (utente_id, messaggio) "
                    "VALUES (:utente_id, :messaggio) "
                    "RETURNING id, utente_id, messaggio, letta, created_at"
                ),
                {"utente_id": str(id_utente), "messaggio": messaggio},
            ).fetchone()
            session.commit()
            return Notifica(
                id=row.id,
                id_utente=row.utente_id,
                messaggio=row.messaggio,
                letta=row.letta,
                data=row.created_at,
            )

    def find_by_utente(self, id_utente: UUID) -> list[Notifica]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, messaggio, letta, created_at "
                    "FROM notifiche WHERE utente_id = :id ORDER BY created_at DESC"
                ),
                {"id": str(id_utente)},
            ).fetchall()
            return [
                Notifica(
                    id=row.id,
                    id_utente=row.utente_id,
                    messaggio=row.messaggio,
                    letta=row.letta,
                    data=row.created_at,
                )
                for row in rows
            ]
```

- [ ] **Step 4: Esegui il test per verificarne il successo**

Run: `cd backend && uv run pytest tests/test_notifica_repository.py -v -m integration`
Expected: PASS su entrambi i test (richiede `backend/.env` con `DATABASE_URL` valido e migrazione Task 1 applicata).

- [ ] **Step 5: Commit**

```bash
git add backend/dal/notifica_repository.py backend/tests/test_notifica_repository.py
git commit -m "feat(IF-OP.09): aggiunge NotificaRepository"
```

---

### Task 3: `NotificaService` (BLL)

**Files:**
- Create: `backend/bll/notifica_service.py`
- Test: `backend/tests/test_notifica_service.py`

**Interfaces:**
- Consumes: `NotificaRepository.crea(id_utente: UUID, messaggio: str) -> Notifica` (Task 2).
- Produces: `NotificaService.notifica(id_utente: UUID, messaggio: str) -> None` — usato da `ServizioUtenti.sospendi_account` (Task 5).

- [ ] **Step 1: Scrivi il test (fallente)**

`backend/tests/test_notifica_service.py`:
```python
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from bll.notifica_service import NotificaService
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestNotificaService:

    def test_notifica_persiste_messaggio(self, db, utente_test):
        try:
            NotificaService().notifica(utente_test["id"], "Account sospeso: test")
            notifiche = NotificaRepository().find_by_utente(utente_test["id"])
            assert len(notifiche) == 1
            assert notifiche[0].messaggio == "Account sospeso: test"
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()
```

- [ ] **Step 2: Esegui il test per verificarne il fallimento**

Run: `cd backend && uv run pytest tests/test_notifica_service.py -v -m integration`
Expected: FAIL con `ModuleNotFoundError: No module named 'bll.notifica_service'`

- [ ] **Step 3: Implementa `NotificaService`**

`backend/bll/notifica_service.py`:
```python
from uuid import UUID
from dal.notifica_repository import NotificaRepository


class NotificaService:
    """[IF-OP.09 / IF-OP.08] Logica di invio (persistenza) notifiche all'Utente."""

    def __init__(self) -> None:
        self._repo = NotificaRepository()

    def notifica(self, id_utente: UUID, messaggio: str) -> None:
        self._repo.crea(id_utente, messaggio)
```

- [ ] **Step 4: Esegui il test per verificarne il successo**

Run: `cd backend && uv run pytest tests/test_notifica_service.py -v -m integration`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/bll/notifica_service.py backend/tests/test_notifica_service.py
git commit -m "feat(IF-OP.09): aggiunge NotificaService"
```

---

### Task 4: Estendi `AttoreRepository` con `lista_utenti`, `trova_utente_per_id`, `sospendi`

**Files:**
- Modify: `backend/dal/attore_repository.py`
- Test: `backend/tests/test_attore_repository_utenti.py`

**Interfaces:**
- Consumes: fixture `utente_test`, `utente_sospeso`, `operatore_test` da `conftest.py`; tabella `utenti` con le colonne aggiunte in Task 1.
- Produces:
  - `AttoreRepository.lista_utenti() -> list[dict]` — ogni dict: `{"id": str, "nome": str, "cognome": str, "email": str, "sospeso": bool}`.
  - `AttoreRepository.trova_utente_per_id(id: UUID) -> dict` — stesso shape del singolo elemento sopra; lancia `AttoreNonTrovatoException` se non esiste in `utenti`.
  - `AttoreRepository.sospendi(id: UUID, motivazione: str) -> None` — lancia `AttoreNonTrovatoException` se l'utente non esiste, `AccountGiaSospesoException` (nuova eccezione in questo file) se `sospeso` è già `true`.
  - Usati da `ServizioUtenti` (Task 5).

- [ ] **Step 1: Scrivi i test (fallenti)**

`backend/tests/test_attore_repository_utenti.py`:
```python
import pytest
from uuid import uuid4
from dal.attore_repository import (
    AttoreRepository,
    AttoreNonTrovatoException,
    AccountGiaSospesoException,
)


@pytest.mark.integration
class TestListaUtenti:

    def test_lista_utenti_contiene_utente_test(self, utente_test):
        utenti = AttoreRepository().lista_utenti()
        ids = {u["id"] for u in utenti}
        assert str(utente_test["id"]) in ids

    def test_lista_utenti_include_email(self, utente_test):
        utenti = AttoreRepository().lista_utenti()
        trovato = next(u for u in utenti if u["id"] == str(utente_test["id"]))
        assert trovato["email"] == utente_test["email"]
        assert trovato["sospeso"] is False


@pytest.mark.integration
class TestTrovaUtentePerId:

    def test_trova_utente_per_id_ok(self, utente_test):
        u = AttoreRepository().trova_utente_per_id(utente_test["id"])
        assert u["nome"] == "Test"
        assert u["email"] == utente_test["email"]

    def test_trova_utente_per_id_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            AttoreRepository().trova_utente_per_id(uuid4())


@pytest.mark.integration
class TestSospendi:

    def test_sospendi_account_attivo(self, utente_test):
        AttoreRepository().sospendi(utente_test["id"], "Comportamento scorretto")
        u = AttoreRepository().trova_utente_per_id(utente_test["id"])
        assert u["sospeso"] is True

    def test_sospendi_account_gia_sospeso(self, utente_sospeso):
        with pytest.raises(AccountGiaSospesoException):
            AttoreRepository().sospendi(utente_sospeso["id"], "Motivo")

    def test_sospendi_utente_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            AttoreRepository().sospendi(uuid4(), "Motivo")
```

- [ ] **Step 2: Esegui i test per verificarne il fallimento**

Run: `cd backend && uv run pytest tests/test_attore_repository_utenti.py -v -m integration`
Expected: FAIL — `lista_utenti`/`trova_utente_per_id`/`sospendi`/`AccountGiaSospesoException` non esistono ancora.

- [ ] **Step 3: Implementa i nuovi metodi**

Aggiungi in `backend/dal/attore_repository.py`, dopo la classe `AttoreNonTrovatoException`:
```python
class AccountGiaSospesoException(Exception):
    pass
```

Aggiungi questi metodi alla classe `AttoreRepository` (dopo `crea_utente`):
```python
    # [IF-OP.09] ──────────────────────────────────────────────────────────────

    def lista_utenti(self) -> list[dict]:
        """Elenco di tutti gli Utenti registrati, con email da auth.users."""
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT u.id, u.nome, u.cognome, u.sospeso, a.email "
                    "FROM utenti u JOIN auth.users a ON a.id = u.id "
                    "ORDER BY u.cognome, u.nome"
                )
            ).fetchall()
            return [
                {
                    "id": str(row.id),
                    "nome": row.nome,
                    "cognome": row.cognome,
                    "email": row.email,
                    "sospeso": row.sospeso,
                }
                for row in rows
            ]

    def trova_utente_per_id(self, id: UUID) -> dict:
        """Dettaglio di un singolo Utente, con email da auth.users."""
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT u.id, u.nome, u.cognome, u.sospeso, a.email "
                    "FROM utenti u JOIN auth.users a ON a.id = u.id "
                    "WHERE u.id = :id"
                ),
                {"id": str(id)},
            ).fetchone()
            if not row:
                raise AttoreNonTrovatoException(f"Utente {id} non trovato")
            return {
                "id": str(row.id),
                "nome": row.nome,
                "cognome": row.cognome,
                "email": row.email,
                "sospeso": row.sospeso,
            }

    def sospendi(self, id: UUID, motivazione: str) -> None:
        """[IF-OP.09] Sospende l'account di un Utente attivo."""
        with Session(engine) as session:
            row = session.execute(
                text("SELECT sospeso FROM utenti WHERE id = :id"),
                {"id": str(id)},
            ).fetchone()
            if not row:
                raise AttoreNonTrovatoException(f"Utente {id} non trovato")
            if row.sospeso:
                raise AccountGiaSospesoException(f"Utente {id} è già sospeso")

            session.execute(
                text(
                    "UPDATE utenti SET sospeso = true, "
                    "motivazione_sospensione = :motivazione, sospeso_at = NOW() "
                    "WHERE id = :id"
                ),
                {"id": str(id), "motivazione": motivazione},
            )
            session.commit()
```

- [ ] **Step 4: Esegui i test per verificarne il successo**

Run: `cd backend && uv run pytest tests/test_attore_repository_utenti.py -v -m integration`
Expected: PASS su tutti i test.

- [ ] **Step 5: Commit**

```bash
git add backend/dal/attore_repository.py backend/tests/test_attore_repository_utenti.py
git commit -m "feat(IF-OP.09): aggiunge lista_utenti, trova_utente_per_id, sospendi a AttoreRepository"
```

---

### Task 5: Estendi `ServizioUtenti` con `get_utenti`, `get_dettaglio_utente`, `sospendi_account`

**Files:**
- Modify: `backend/bll/servizio_utenti.py`
- Test: `backend/tests/test_servizio_utenti_sospensione.py`

**Interfaces:**
- Consumes: `AttoreRepository.lista_utenti/trova_utente_per_id/sospendi` (Task 4), `NotificaService.notifica` (Task 3), `AttoreNonTrovatoException`/`AccountGiaSospesoException` da `dal.attore_repository`.
- Produces:
  - `ServizioUtenti.get_utenti() -> list[dict]`
  - `ServizioUtenti.get_dettaglio_utente(id: UUID) -> dict`
  - `ServizioUtenti.sospendi_account(id: UUID, motivazione: str) -> None` — lancia `ValueError` se `motivazione` è vuota/whitespace, propaga `AttoreNonTrovatoException`/`AccountGiaSospesoException`, poi notifica l'utente.
  - Usati da `UtentiOPController` (Task 7).

- [ ] **Step 1: Scrivi i test (fallenti)**

`backend/tests/test_servizio_utenti_sospensione.py`:
```python
import pytest
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session
from bll.servizio_utenti import ServizioUtenti
from dal.attore_repository import AttoreNonTrovatoException, AccountGiaSospesoException
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestGetUtenti:

    def test_get_utenti_contiene_utente_test(self, utente_test):
        utenti = ServizioUtenti().get_utenti()
        assert any(u["id"] == str(utente_test["id"]) for u in utenti)


@pytest.mark.integration
class TestGetDettaglioUtente:

    def test_get_dettaglio_utente_ok(self, utente_test):
        u = ServizioUtenti().get_dettaglio_utente(utente_test["id"])
        assert u["email"] == utente_test["email"]

    def test_get_dettaglio_utente_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            ServizioUtenti().get_dettaglio_utente(uuid4())


@pytest.mark.integration
class TestSospendiAccount:

    def test_sospendi_account_crea_notifica(self, db, utente_test):
        try:
            ServizioUtenti().sospendi_account(utente_test["id"], "Comportamento scorretto")

            u = ServizioUtenti().get_dettaglio_utente(utente_test["id"])
            assert u["sospeso"] is True

            notifiche = NotificaRepository().find_by_utente(utente_test["id"])
            assert len(notifiche) == 1
            assert "Comportamento scorretto" in notifiche[0].messaggio
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()

    def test_sospendi_account_motivazione_vuota(self, utente_test):
        with pytest.raises(ValueError):
            ServizioUtenti().sospendi_account(utente_test["id"], "   ")

    def test_sospendi_account_gia_sospeso(self, utente_sospeso):
        with pytest.raises(AccountGiaSospesoException):
            ServizioUtenti().sospendi_account(utente_sospeso["id"], "Motivo")

    def test_sospendi_account_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            ServizioUtenti().sospendi_account(uuid4(), "Motivo")
```

- [ ] **Step 2: Esegui i test per verificarne il fallimento**

Run: `cd backend && uv run pytest tests/test_servizio_utenti_sospensione.py -v -m integration`
Expected: FAIL — `get_utenti`/`get_dettaglio_utente`/`sospendi_account` non esistono ancora su `ServizioUtenti`.

- [ ] **Step 3: Implementa i nuovi metodi**

Modifica `backend/bll/servizio_utenti.py`:
1. Aggiungi l'import di `NotificaService` in testa al file:
```python
from bll.notifica_service import NotificaService
```
2. Aggiungi i tre metodi alla classe `ServizioUtenti`, dopo `cancella_account`:
```python
    # [IF-OP.09] ──────────────────────────────────────────────────────────────

    def get_utenti(self) -> list[dict]:
        return self._repo.lista_utenti()

    def get_dettaglio_utente(self, utente_id: UUID) -> dict:
        return self._repo.trova_utente_per_id(utente_id)

    def sospendi_account(self, utente_id: UUID, motivazione: str) -> None:
        if not motivazione or not motivazione.strip():
            raise ValueError("La motivazione della sospensione è obbligatoria")
        self._repo.sospendi(utente_id, motivazione)
        NotificaService().notifica(
            utente_id, f"Il tuo account è stato sospeso. Motivo: {motivazione}"
        )
```

- [ ] **Step 4: Esegui i test per verificarne il successo**

Run: `cd backend && uv run pytest tests/test_servizio_utenti_sospensione.py -v -m integration`
Expected: PASS su tutti i test.

- [ ] **Step 5: Esegui la suite di autenticazione per verificare nessuna regressione**

Run: `cd backend && uv run pytest tests/test_auth.py -v -m integration`
Expected: PASS (in particolare `test_login_account_sospeso` continua a passare, confermando che il blocco login per utenti sospesi resta intatto).

- [ ] **Step 6: Commit**

```bash
git add backend/bll/servizio_utenti.py backend/tests/test_servizio_utenti_sospensione.py
git commit -m "feat(IF-OP.09): aggiunge get_utenti, get_dettaglio_utente, sospendi_account a ServizioUtenti"
```

---

### Task 6: Schemi Pydantic per richieste/risposte

**Files:**
- Modify: `backend/controllers/schemas.py`

**Interfaces:**
- Produces: `UtenteListItemOut`, `UtenteDettaglioOut`, `SospensioneRequest` — usati da `UtentiOPController` (Task 7).

- [ ] **Step 1: Aggiungi gli schemi**

Aggiungi in fondo a `backend/controllers/schemas.py`:
```python
# [IF-OP.09] Sospende Account Utente
class UtenteListItemOut(BaseModel):
    id: str
    nome: str
    cognome: str
    email: str
    sospeso: bool


class UtenteDettaglioOut(UtenteListItemOut):
    pass


class SospensioneRequest(BaseModel):
    motivazione: str
```

Non serve un test dedicato: questi schemi sono coperti dai test HTTP del Task 7 (FastAPI valida automaticamente request/response contro questi modelli).

- [ ] **Step 2: Verifica che il modulo importi correttamente**

Run: `cd backend && uv run python -c "from controllers.schemas import UtenteListItemOut, UtenteDettaglioOut, SospensioneRequest; print('ok')"`
Expected: stampa `ok` senza errori.

- [ ] **Step 3: Commit**

```bash
git add backend/controllers/schemas.py
git commit -m "feat(IF-OP.09): aggiunge schemi UtenteListItemOut, UtenteDettaglioOut, SospensioneRequest"
```

---

### Task 7: `UtentiOPController` + registrazione router + test HTTP

**Files:**
- Create: `backend/controllers/utenti_op_controller.py`
- Modify: `backend/main.py`
- Test: `backend/tests/test_sospendi_account_http.py`

**Interfaces:**
- Consumes: `ServizioUtenti.get_utenti/get_dettaglio_utente/sospendi_account` (Task 5), `AttoreNonTrovatoException`/`AccountGiaSospesoException` (Task 4), `UtenteListItemOut`/`UtenteDettaglioOut`/`SospensioneRequest` (Task 6), `verify_token(["OP"])` da `middleware.auth_middleware`.
- Produces: router montato su `GET /operatore/utenti`, `GET /operatore/utenti/{utente_id}`, `PATCH /operatore/utenti/{utente_id}/stato` — consumati dal frontend (Task 8).

- [ ] **Step 1: Scrivi i test HTTP (fallenti)**

`backend/tests/test_sospendi_account_http.py` (richiede il server avviato: `cd backend && uv run uvicorn main:app --reload`, in un altro terminale, prima di eseguire questi test — stesso pattern di `test_tariffa_http.py`):
```python
import pytest
import httpx
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8000"


def _login(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _pulisci_notifiche(db, utente_id) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM notifiche WHERE utente_id = :id"), {"id": str(utente_id)})
        s.commit()


@pytest.mark.integration
class TestUtentiOPControllerHTTP:

    def test_get_utenti_200(self, db, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/utenti", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert any(u["id"] == str(utente_test["id"]) for u in r.json())

    def test_get_utenti_403_per_ruolo_ut(self, utente_test):
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.get(f"{BASE}/operatore/utenti", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 403

    def test_get_dettaglio_utente_200(self, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(
            f"{BASE}/operatore/utenti/{utente_test['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        assert r.json()["email"] == utente_test["email"]

    def test_get_dettaglio_utente_404(self, operatore_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(
            f"{BASE}/operatore/utenti/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    def test_sospendi_account_200(self, db, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        try:
            r = httpx.patch(
                f"{BASE}/operatore/utenti/{utente_test['id']}/stato",
                json={"motivazione": "Comportamento scorretto"},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            assert r.json()["sospeso"] is True
        finally:
            _pulisci_notifiche(db, utente_test["id"])

    def test_sospendi_account_422_motivazione_vuota(self, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{utente_test['id']}/stato",
            json={"motivazione": "   "},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 422

    def test_sospendi_account_409_gia_sospeso(self, operatore_test, utente_sospeso):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{utente_sospeso['id']}/stato",
            json={"motivazione": "Motivo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 409

    def test_sospendi_account_404_non_trovato(self, operatore_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{uuid4()}/stato",
            json={"motivazione": "Motivo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404
```

- [ ] **Step 2: Esegui i test per verificarne il fallimento**

Run: `cd backend && uv run pytest tests/test_sospendi_account_http.py -v -m integration`
Expected: FAIL con `ConnectionError`/404 generico — il router non esiste ancora e non è montato.

- [ ] **Step 3: Implementa `UtentiOPController`**

`backend/controllers/utenti_op_controller.py`:
```python
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from bll.servizio_utenti import ServizioUtenti
from dal.attore_repository import AttoreNonTrovatoException, AccountGiaSospesoException
from middleware.auth_middleware import verify_token
from controllers.schemas import UtenteListItemOut, UtenteDettaglioOut, SospensioneRequest

# [IF-OP.09] UtentiOPController
router = APIRouter(prefix="/operatore", tags=["Gestione Utenti Operatore"])
_servizio = ServizioUtenti()


@router.get("/utenti", response_model=list[UtenteListItemOut])
def lista_utenti(_=Depends(verify_token(["OP"]))):
    """[IF-OP.09] Elenco di tutti gli Utenti registrati."""
    return _servizio.get_utenti()


@router.get("/utenti/{utente_id}", response_model=UtenteDettaglioOut)
def dettaglio_utente(utente_id: UUID, _=Depends(verify_token(["OP"]))):
    """[IF-OP.09] Dettaglio del profilo di un Utente."""
    try:
        return _servizio.get_dettaglio_utente(utente_id)
    except AttoreNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/utenti/{utente_id}/stato", response_model=UtenteDettaglioOut)
def sospendi_account(
    utente_id: UUID,
    body: SospensioneRequest,
    _=Depends(verify_token(["OP"])),
):
    """[IF-OP.09] Sospende l'account di un Utente, con motivazione."""
    try:
        _servizio.sospendi_account(utente_id, body.motivazione)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AccountGiaSospesoException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except AttoreNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _servizio.get_dettaglio_utente(utente_id)
```

- [ ] **Step 4: Registra il router in `main.py`**

Modifica `backend/main.py`: aggiungi l'import dopo `from controllers.recensione_controller import router as recensione_router`:
```python
from controllers.utenti_op_controller import router as utenti_op_router
```
E aggiungi la riga di registrazione dopo `app.include_router(recensione_router)`:
```python
app.include_router(utenti_op_router)
```

- [ ] **Step 5: Avvia il server e riesegui i test HTTP**

Run (in un terminale separato, lascialo in esecuzione): `cd backend && uv run uvicorn main:app --reload`
Run (in questo terminale): `cd backend && uv run pytest tests/test_sospendi_account_http.py -v -m integration`
Expected: PASS su tutti i test.

- [ ] **Step 6: Commit**

```bash
git add backend/controllers/utenti_op_controller.py backend/main.py backend/tests/test_sospendi_account_http.py
git commit -m "feat(IF-OP.09): aggiunge UtentiOPController con endpoint lista/dettaglio/sospendi"
```

---

### Task 8: `GestioneUtentiService.ts` (frontend service layer)

**Files:**
- Create: `frontend/src/services/GestioneUtentiService.ts`

**Interfaces:**
- Consumes: `api` da `./ApiService` (axios instance con interceptor JWT già configurato).
- Produces: `UtenteListItem` interface, `getUtenti()`, `getDettaglioUtente(id)`, `sospendiAccount(id, motivazione)` — usati da `VistaGestioneUtentiOperatore.tsx` (Task 9). Forma della risposta JSON corrisponde a `UtenteListItemOut`/`UtenteDettaglioOut` del backend (Task 6): `{ id, nome, cognome, email, sospeso }`.

- [ ] **Step 1: Crea il service**

`frontend/src/services/GestioneUtentiService.ts`:
```typescript
import { api } from './ApiService'

export interface UtenteListItem {
  id: string
  nome: string
  cognome: string
  email: string
  sospeso: boolean
}

// [IF-OP.09] Sospende Account Utente
export const getUtenti = (): Promise<{ data: UtenteListItem[] }> =>
  api.get('/operatore/utenti')

export const getDettaglioUtente = (id: string): Promise<{ data: UtenteListItem }> =>
  api.get(`/operatore/utenti/${id}`)

export const sospendiAccount = (
  id: string,
  motivazione: string,
): Promise<{ data: UtenteListItem }> =>
  api.patch(`/operatore/utenti/${id}/stato`, { motivazione })
```

- [ ] **Step 2: Verifica la compilazione TypeScript**

Run: `cd frontend && npm run build`
Expected: build completata senza errori TypeScript relativi a `GestioneUtentiService.ts` (potrebbero esserci altri file non ancora collegati — verrà completato nel Task 9-10; se il build fallisce solo per import non utilizzato, è atteso fino al Task 9).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/GestioneUtentiService.ts
git commit -m "feat(IF-OP.09): aggiunge GestioneUtentiService"
```

---

### Task 9: `VistaGestioneUtentiOperatore.tsx` + stile

**Files:**
- Create: `frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx`
- Create: `frontend/src/views/operatore/VistaGestioneUtentiOperatore.css`

**Interfaces:**
- Consumes: `getUtenti`, `getDettaglioUtente`, `sospendiAccount`, `UtenteListItem` da `../../services/GestioneUtentiService` (Task 8).
- Produces: componente React default-exportato `VistaGestioneUtentiOperatore` — usato da `App.tsx` (Task 10).

- [ ] **Step 1: Crea il componente**

`frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx`:
```tsx
import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getUtenti,
  getDettaglioUtente,
  sospendiAccount,
  type UtenteListItem,
} from '../../services/GestioneUtentiService'
import './VistaGestioneUtentiOperatore.css'

// [IF-OP.09] Sospende Account Utente
export default function VistaGestioneUtentiOperatore() {
  const navigate = useNavigate()

  const [utenti, setUtenti] = useState<UtenteListItem[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [selezionato, setSelezionato] = useState<UtenteListItem | null>(null)
  const [motivazione, setMotivazione] = useState('')
  const [dialogoAperto, setDialogoAperto] = useState(false)
  const [azioneInCorso, setAzioneInCorso] = useState(false)
  const [messaggio, setMessaggio] = useState('')

  const caricaUtenti = useCallback(async () => {
    try {
      const res = await getUtenti()
      setUtenti(res.data)
    } catch {
      setErrore('Impossibile caricare gli utenti.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaUtenti() }, [caricaUtenti])

  const selezionaUtente = async (id: string) => {
    setDialogoAperto(false)
    setMotivazione('')
    try {
      const res = await getDettaglioUtente(id)
      setSelezionato(res.data)
    } catch {
      setErrore('Errore nel caricamento del dettaglio.')
    }
  }

  const confermaSospensione = async () => {
    if (!selezionato || !motivazione.trim()) return
    setAzioneInCorso(true)
    try {
      const res = await sospendiAccount(selezionato.id, motivazione.trim())
      setSelezionato(res.data)
      setUtenti(prev => prev.map(u => (u.id === res.data.id ? res.data : u)))
      setDialogoAperto(false)
      setMessaggio('Account sospeso con successo.')
      setTimeout(() => setMessaggio(''), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErrore('L\'account è già sospeso.')
      } else if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Utente non trovato.')
      } else {
        setErrore('Errore durante la sospensione dell\'account.')
      }
    } finally {
      setAzioneInCorso(false)
    }
  }

  return (
    <div className="vista-gest-ut-wrap">
      <button type="button" className="btn-back-gest-ut" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="gest-ut-titolo">Gestione Utenti</h1>

      {messaggio && <div className="gest-ut-messaggio">{messaggio}</div>}
      {errore && <p className="gest-ut-errore">{errore}</p>}

      <div className="gest-ut-layout">
        <div className="gest-ut-lista">
          {caricamento ? (
            <p className="gest-ut-vuoto">Caricamento...</p>
          ) : utenti.length === 0 ? (
            <p className="gest-ut-vuoto">Nessun utente registrato.</p>
          ) : (
            utenti.map(u => (
              <div
                key={u.id}
                className={`gest-ut-card${selezionato?.id === u.id ? ' gest-ut-card--attiva' : ''}`}
                onClick={() => selezionaUtente(u.id)}
              >
                <div className="gest-ut-card-header">
                  <span className="gest-ut-nome">{u.nome} {u.cognome}</span>
                  {u.sospeso && <span className="gest-ut-badge">Sospeso</span>}
                </div>
                <span className="gest-ut-email">{u.email}</span>
              </div>
            ))
          )}
        </div>

        {selezionato && (
          <div className="gest-ut-dettaglio">
            <h2 className="gest-ut-det-titolo">Dettaglio</h2>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Nome</span>
              <span>{selezionato.nome} {selezionato.cognome}</span>
            </div>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Email</span>
              <span>{selezionato.email}</span>
            </div>
            <div className="gest-ut-det-row">
              <span className="gest-ut-det-label">Stato</span>
              <span>{selezionato.sospeso ? 'Sospeso' : 'Attivo'}</span>
            </div>

            {selezionato.sospeso ? (
              <p className="gest-ut-sospeso-msg">⚠️ Account già sospeso</p>
            ) : !dialogoAperto ? (
              <button
                type="button"
                className="btn-gest-ut-danger"
                onClick={() => setDialogoAperto(true)}
              >
                Sospendi account
              </button>
            ) : (
              <div className="gest-ut-conferma">
                <label className="gest-ut-det-label" htmlFor="motivazione-sospensione">
                  Motivazione della sospensione
                </label>
                <textarea
                  id="motivazione-sospensione"
                  className="gest-ut-textarea"
                  value={motivazione}
                  onChange={e => setMotivazione(e.target.value)}
                  placeholder="Descrivi il motivo della sospensione"
                  rows={4}
                />
                <button
                  type="button"
                  className="btn-gest-ut-danger"
                  onClick={confermaSospensione}
                  disabled={azioneInCorso || !motivazione.trim()}
                >
                  {azioneInCorso ? 'Sospensione...' : 'Conferma sospensione'}
                </button>
                <button
                  type="button"
                  className="btn-gest-ut-secondario"
                  onClick={() => { setDialogoAperto(false); setMotivazione('') }}
                  disabled={azioneInCorso}
                >
                  Annulla
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Crea il CSS riusando il pattern visivo esistente**

`frontend/src/views/operatore/VistaGestioneUtentiOperatore.css`:
```css
.vista-gest-ut-wrap {
  min-height: 100vh;
  background: #f5f6fa;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 24px 20px 48px;
}

.btn-back-gest-ut {
  background: none;
  border: none;
  color: #4caf9a;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-bottom: 20px;
}

.gest-ut-titolo {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 16px;
}

.gest-ut-messaggio {
  background: #e8f5e9;
  border: 1px solid #a5d6a7;
  border-radius: 8px;
  color: #2e7d32;
  font-size: 13px;
  padding: 10px 14px;
  margin-bottom: 12px;
  width: 100%;
  max-width: 860px;
}

.gest-ut-errore {
  color: #e53935;
  font-size: 13px;
  margin: 0 0 12px;
}

.gest-ut-vuoto {
  color: #888;
  font-size: 14px;
}

.gest-ut-layout {
  display: flex;
  gap: 20px;
  width: 100%;
  max-width: 920px;
  align-items: flex-start;
}

.gest-ut-lista {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
}

.gest-ut-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  padding: 14px 16px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.15s;
}

.gest-ut-card:hover {
  border-color: #4caf9a;
}

.gest-ut-card--attiva {
  border-color: #4caf9a;
}

.gest-ut-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.gest-ut-nome {
  font-size: 14px;
  font-weight: 700;
  color: #1a1a2e;
}

.gest-ut-email {
  font-size: 12px;
  color: #666;
}

.gest-ut-badge {
  font-size: 11px;
  font-weight: 700;
  border-radius: 20px;
  padding: 3px 10px;
  white-space: nowrap;
  background: #ffebee;
  color: #c62828;
}

.gest-ut-dettaglio {
  width: 320px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gest-ut-det-titolo {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}

.gest-ut-det-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #333;
}

.gest-ut-det-label {
  font-weight: 600;
  color: #666;
}

.btn-gest-ut-danger {
  background: #e53935;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
  margin-top: 4px;
}

.btn-gest-ut-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-gest-ut-secondario {
  background: transparent;
  color: #666;
  border: 1px solid #ccc;
  border-radius: 24px;
  padding: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
}

.gest-ut-conferma {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.gest-ut-textarea {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  font-size: 13px;
  font-family: inherit;
  resize: vertical;
}

.gest-ut-sospeso-msg {
  font-size: 13px;
  color: #c62828;
  text-align: center;
  margin: 0;
}
```

- [ ] **Step 3: Verifica la compilazione TypeScript**

Run: `cd frontend && npm run build`
Expected: build completata senza errori (a questo punto il componente non è ancora montato in nessuna rotta — il build verifica solo che il file compili).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx frontend/src/views/operatore/VistaGestioneUtentiOperatore.css
git commit -m "feat(IF-OP.09): aggiunge VistaGestioneUtentiOperatore"
```

---

### Task 10: Routing e collegamento del bottone "Gestisci utenti"

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/views/operatore/VistaMappaOperatore.tsx:327`

**Interfaces:**
- Consumes: `VistaGestioneUtentiOperatore` (Task 9), `RoutaProtetta` esistente (`ruoloRichiesto` prop).
- Produces: rotta `/operatore/utenti` raggiungibile dall'app e dal bottone "Gestisci utenti" già presente nel pannello operatore.

- [ ] **Step 1: Aggiungi l'import e la rotta in `App.tsx`**

In `frontend/src/App.tsx`, aggiungi l'import dopo `import VistaRecensione from './views/utente/VistaRecensione'`:
```tsx
import VistaGestioneUtentiOperatore from './views/operatore/VistaGestioneUtentiOperatore'
```

Aggiungi la rotta dopo il blocco `/operatore/segnalazioni` (circa riga 167, prima di `/operatore/tariffe`):
```tsx
        <Route
          path="/operatore/utenti"
          element={
            <RoutaProtetta ruoloRichiesto="OP">
              <VistaGestioneUtentiOperatore />
            </RoutaProtetta>
          }
        />
```

- [ ] **Step 2: Collega il bottone "Gestisci utenti"**

In `frontend/src/views/operatore/VistaMappaOperatore.tsx`, riga 327, sostituisci:
```tsx
          <button type="button" className="btn-pannello secondario">Gestisci utenti</button>
```
con:
```tsx
          <button type="button" className="btn-pannello secondario" onClick={() => navigate('/operatore/utenti')}>Gestisci utenti</button>
```

- [ ] **Step 3: Verifica la compilazione**

Run: `cd frontend && npm run build`
Expected: build completata senza errori.

- [ ] **Step 4: Verifica manuale nel browser**

Run: `cd backend && uv run uvicorn main:app --reload` (terminale 1)
Run: `cd frontend && npm run dev` (terminale 2)
Apri `http://localhost:5173`, accedi come Operatore, vai su Mappa Operatore → "Gestisci utenti", seleziona un Utente, inserisci una motivazione, conferma la sospensione, verifica:
- Il badge "Sospeso" appare nella lista.
- Tentando il login con le credenziali dell'Utente appena sospeso, il sistema risponde con errore 403 ("Account sospeso").

- [ ] **Step 5: Commit**

```bash
git add frontend/src/App.tsx frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(IF-OP.09): collega rotta e bottone Gestisci utenti a VistaGestioneUtentiOperatore"
```

---

### Task 11: Aggiornamento documentazione

**Files:**
- Modify: `docs/Sprintn3.md` (sezione OP-09, § 2.4.3.25)
- Modify: `docs/CoerenzaDiagrammaClassi.md`

**Interfaces:**
- Nessuna — solo testo di documentazione, nessun codice consumato/prodotto.

- [ ] **Step 1: Correggi le post-condizioni di OP-09 in `Sprintn3.md`**

Trova la riga (circa 3192-3194):
```
<td>Post-condizioni</td>
<td>La segnalazione è stata presa in carico dall'Operatore; l'Utente è informato dell'aggiornamento di stato.</td>
```
Sostituisci con:
```
<td>Post-condizioni</td>
<td>L'account dell'Utente è sospeso; l'Utente non può più accedere alla piattaforma; l'Utente è stato notificato dell'avvenuta sospensione.</td>
```

- [ ] **Step 2: Aggiorna `CoerenzaDiagrammaClassi.md`**

Nella tabella "FRONTEND — Views", cambia la riga `VistaGestioneUtentiOperatore` da:
```
| `VistaGestioneUtentiOperatore` | non trovata | ❌ | IF-OP.09 Sospende Account Utente — pianificata nel diagramma, non implementata (come `Recensione`) |
```
a:
```
| `VistaGestioneUtentiOperatore` | `views/operatore/VistaGestioneUtentiOperatore.tsx` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
```

Nella tabella "BACKEND — BLL (Servizi)", cambia la riga `NotificaService` da:
```
| `NotificaService` | non trovato | ❌ | Creato 2026-06-20 nel diagramma (IF-OP.08/IF-OP.09 richiedono notifica all'Utente); non implementato nel codice — nessun canale notifiche esiste oggi |
```
a:
```
| `NotificaService` | `bll/notifica_service.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) — solo persistenza, nessuna UI di lettura |
```

Nella tabella "BACKEND — Model (Entità ORM)", cambia la riga `Notifica` da:
```
| `Notifica` | non trovato | ❌ | Creato 2026-06-20 nel diagramma insieme a `NotificaService`/`NotificaRepository` — non implementato |
```
a:
```
| `Notifica` | `model/notifica.py` + `model/orm.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
```

Nella tabella "BACKEND — DAL (Repository)", cambia la riga `NotificaRepository` da:
```
| `NotificaRepository` | non trovato | ❌ | Creato 2026-06-20 nel diagramma — non implementato |
```
a:
```
| `NotificaRepository` | `dal/notifica_repository.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
```

Nella tabella "BACKEND — Controllers", cambia la riga `UtentiOPController` da:
```
| `UtentiOPController` | non trovato | ❌ | IF-OP.09 Sospende Account Utente — pianificato nel diagramma, non implementato |
```
a:
```
| `UtentiOPController` | `controllers/utenti_op_controller.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
```

Nella sezione "❌ Critiche (da risolvere)", rimuovi le righe `4 | VistaGestioneUtentiOperatore mancante | ...` e `7 | UtentiOPController mancante | ...`, rinumerando le righe rimanenti.

Aggiungi una riga in "Cronologia fix":
```
| 2026-06-21 | Implementato IF-OP.09 (Sospende Account Utente): `model/notifica.py`+`model/orm.py::Notifica`, `dal/notifica_repository.py`, `bll/notifica_service.py`, `AttoreRepository.lista_utenti/trova_utente_per_id/sospendi`, `ServizioUtenti.get_utenti/get_dettaglio_utente/sospendi_account`, `controllers/utenti_op_controller.py`, `GestioneUtentiService.ts`, `VistaGestioneUtentiOperatore.tsx`. Riattivazione e invalidazione sessione attiva escluse dallo scope (vedi spec). Corrette anche le post-condizioni errate di OP-09 in `Sprintn3.md` (testo copiato dal caso d'uso Segnalazione) | `backend/migrations/015_sospensione_account.sql`, `backend/model/notifica.py`, `backend/model/orm.py`, `backend/dal/notifica_repository.py`, `backend/bll/notifica_service.py`, `backend/dal/attore_repository.py`, `backend/bll/servizio_utenti.py`, `backend/controllers/utenti_op_controller.py`, `backend/controllers/schemas.py`, `backend/main.py`, `frontend/src/services/GestioneUtentiService.ts`, `frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx`, `App.tsx`, `VistaMappaOperatore.tsx`, `Sprintn3.md` |
```

- [ ] **Step 3: Commit**

```bash
git add docs/Sprintn3.md docs/CoerenzaDiagrammaClassi.md
git commit -m "docs(IF-OP.09): corregge post-condizioni OP-09 e aggiorna coerenza diagramma classi"
```

---

## Final Verification

- [ ] **Step 1: Esegui l'intera suite backend non-integration**

Run: `cd backend && uv run pytest tests/ -v -m "not integration"`
Expected: PASS, nessuna regressione.

- [ ] **Step 2: Esegui l'intera suite backend integration (richiede `backend/.env` e server avviato per i test HTTP)**

Run: `cd backend && uv run pytest tests/ -v -m integration`
Expected: PASS, nessuna regressione (in particolare `test_auth.py`, `test_schema.py`).

- [ ] **Step 3: Build frontend**

Run: `cd frontend && npm run build`
Expected: build completata senza errori.

- [ ] **Step 4: Verifica manuale end-to-end nel browser** (vedi Task 10 Step 4)
