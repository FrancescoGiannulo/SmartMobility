# DB Schema Sprint 1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Creare lo schema logico del database su Supabase e i corrispondenti modelli SQLAlchemy 2.0 per i 23 item dello Sprint 1.

**Architecture:** La migrazione SQL definisce lo schema autoritativo su PostgreSQL/Supabase con PostGIS. I modelli SQLAlchemy nel layer `model/` rispecchiano fedelmente questo schema e sono usati dal DAL per l'accesso ai dati. I test verificano la struttura dei modelli senza richiedere una connessione live, con test di integrazione separati (marcati `@pytest.mark.integration`) che richiedono il DB.

**Tech Stack:** Python 3.11, SQLAlchemy 2.0, GeoAlchemy2, psycopg2-binary, PostgreSQL 15 + PostGIS (Supabase), pytest, uv

---

## File Structure

| File | Azione | Responsabilità |
|------|--------|----------------|
| `backend/pyproject.toml` | Modifica | Aggiunge `geoalchemy2`, `psycopg2-binary` |
| `backend/database.py` | Crea | Engine SQLAlchemy, SessionLocal, DeclarativeBase, `get_db()` |
| `backend/migrations/001_init_schema.sql` | Crea | Migrazione SQL completa: estensione, enum, tabelle, indice |
| `backend/model/utente.py` | Sostituisce | ORM: `Utente`, `Operatore`, `AmministrazionePubblica` |
| `backend/model/mezzo.py` | Sostituisce | ORM + enum: `TipoMezzo`, `StatoMezzo`, `Mezzo` |
| `backend/model/zona.py` | Sostituisce | ORM + enum: `TipoZona`, `Zona` |
| `backend/model/prenotazione.py` | Crea | ORM + enum: `StatoPrenotazione`, `Prenotazione` |
| `backend/model/corsa.py` | Sostituisce | ORM + enum: `StatoCorsa`, `Corsa` (rimuove `Prenotazione`) |
| `backend/model/pagamento.py` | Sostituisce | ORM + enum: `TipoMetodoPagamento`, `StatoPagamento`, `MetodoPagamento`, `Pagamento` |
| `backend/model/tariffa.py` | Crea | ORM: `Tariffa` |
| `backend/model/regola_fine_corsa.py` | Crea | ORM + enum: `TipoVincoloFinecorsa`, `RegolaFinecorsa` |
| `backend/tests/__init__.py` | Crea | Package marker |
| `backend/tests/test_schema.py` | Crea | Test struttura modelli + test integrazione schema DB |

---

## Task 1: Dipendenze e `database.py`

**Files:**
- Modify: `backend/pyproject.toml`
- Create: `backend/database.py`

- [ ] **Step 1: Aggiungi dipendenze mancanti**

Apri `backend/pyproject.toml` e aggiungi al blocco `dependencies`:

```toml
[project]
name = "smartmobility-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.136.1",
    "uvicorn[standard]>=0.47.0",
    "sqlalchemy>=2.0.49",
    "geoalchemy2>=0.14",
    "psycopg2-binary>=2.9",
    "supabase>=2.30.0",
    "python-dotenv>=1.2.2",
    "pydantic>=2.13.4",
    "pytest>=8.0",
    "pytest-dotenv>=0.5",
]

[tool.pyright]
venvPath = "."
venv = ".venv"
```

- [ ] **Step 2: Installa le nuove dipendenze**

```bash
cd backend && uv sync
```

Output atteso: `Resolved N packages` senza errori.

- [ ] **Step 3: Crea `backend/database.py`**

```python
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 4: Verifica che l'import funzioni**

```bash
cd backend && uv run python -c "from database import Base, engine, get_db; print('OK')"
```

Output atteso: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/pyproject.toml backend/uv.lock backend/database.py
git commit -m "feat: add SQLAlchemy database setup and GeoAlchemy2 dependency"
```

---

## Task 2: Migrazione SQL

**Files:**
- Create: `backend/migrations/001_init_schema.sql`

- [ ] **Step 1: Crea la directory e il file di migrazione**

```bash
mkdir -p backend/migrations
```

Crea `backend/migrations/001_init_schema.sql`:

```sql
-- ============================================================
-- 001_init_schema.sql — Smart Mobility Sprint 1
-- Eseguire su Supabase SQL Editor (o psql)
-- ============================================================

-- 1. Estensione PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- ============================================================
-- 2. Enum Types
-- ============================================================

CREATE TYPE tipo_mezzo AS ENUM ('monopattino', 'bicicletta', 'automobile');

CREATE TYPE stato_mezzo AS ENUM (
    'Disponibile', 'Prenotato', 'In uso', 'In pausa',
    'In manutenzione', 'Fuori servizio', 'Dismesso'
);

CREATE TYPE tipo_zona AS ENUM ('operativa', 'parcheggio', 'limitata', 'vietata');

CREATE TYPE stato_prenotazione AS ENUM ('attiva', 'scaduta', 'annullata', 'convertita');

CREATE TYPE stato_corsa AS ENUM ('in_uso', 'in_pausa', 'terminata');

CREATE TYPE stato_pagamento AS ENUM ('completato', 'rifiutato', 'in_attesa');

CREATE TYPE tipo_metodo_pagamento AS ENUM ('google_pay', 'apple_pay', 'paypal', 'carta');

CREATE TYPE tipo_vincolo_fine_corsa AS ENUM ('penale', 'divieto', 'avviso');

-- ============================================================
-- 3. Tabelle — Profili Utente (FK → auth.users)
-- ============================================================

CREATE TABLE utenti (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome        TEXT NOT NULL,
    cognome     TEXT NOT NULL,
    telefono    TEXT,
    sospeso     BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE operatori (
    id                              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome                            TEXT NOT NULL,
    durata_max_prenotazione_min     INTEGER NOT NULL DEFAULT 15,
    durata_periodo_grazia_min       INTEGER NOT NULL DEFAULT 5,
    max_mezzi_per_utente            INTEGER NOT NULL DEFAULT 1,
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE amministratori (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 4. Flotta
-- ============================================================

CREATE TABLE mezzi (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codice      TEXT NOT NULL UNIQUE,
    tipo        tipo_mezzo NOT NULL,
    stato       stato_mezzo NOT NULL DEFAULT 'Disponibile',
    lat         DOUBLE PRECISION,
    lng         DOUBLE PRECISION,
    batteria    INTEGER CHECK (batteria BETWEEN 0 AND 100),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 5. Zone Geografiche
-- ============================================================

CREATE TABLE zone (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome             TEXT NOT NULL,
    tipo             tipo_zona NOT NULL,
    perimetro        GEOMETRY(POLYGON, 4326) NOT NULL,
    limite_velocita  INTEGER,
    attiva           BOOLEAN NOT NULL DEFAULT true,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indice spaziale obbligatorio per ST_Contains / ST_Intersects
CREATE INDEX zone_perimetro_gist ON zone USING GIST (perimetro);

-- ============================================================
-- 6. Tariffe
-- ============================================================

CREATE TABLE tariffe (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_mezzo       tipo_mezzo NOT NULL UNIQUE,
    costo_al_minuto  NUMERIC(10, 4) NOT NULL CHECK (costo_al_minuto > 0),
    costo_al_km      NUMERIC(10, 4) NOT NULL CHECK (costo_al_km > 0),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    aggiornata_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 7. Metodi di Pagamento
-- ============================================================

CREATE TABLE metodi_pagamento (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id       UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    tipo            tipo_metodo_pagamento NOT NULL,
    token_esterno   TEXT NOT NULL,
    last_four       TEXT,
    predefinito     BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 8. Prenotazioni
-- ============================================================

CREATE TABLE prenotazioni (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    mezzo_id    UUID NOT NULL REFERENCES mezzi(id) ON DELETE RESTRICT,
    stato       stato_prenotazione NOT NULL DEFAULT 'attiva',
    scade_at    TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 9. Regole Fine Corsa
-- ============================================================

CREATE TABLE regole_fine_corsa (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zona_parcheggio_id  UUID NOT NULL REFERENCES zone(id) ON DELETE CASCADE,
    batteria_minima     INTEGER CHECK (batteria_minima BETWEEN 0 AND 100),
    penale_fuori_zona   NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    tipo_vincolo        tipo_vincolo_fine_corsa NOT NULL DEFAULT 'avviso',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 10. Corse
-- ============================================================

CREATE TABLE corse (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id        UUID NOT NULL REFERENCES utenti(id) ON DELETE RESTRICT,
    mezzo_id         UUID NOT NULL REFERENCES mezzi(id) ON DELETE RESTRICT,
    prenotazione_id  UUID REFERENCES prenotazioni(id) ON DELETE SET NULL,
    stato            stato_corsa NOT NULL DEFAULT 'in_uso',
    inizio_at        TIMESTAMPTZ NOT NULL,
    fine_at          TIMESTAMPTZ,
    distanza_km      NUMERIC(10, 3),
    inizio_lat       DOUBLE PRECISION,
    inizio_lng       DOUBLE PRECISION,
    fine_lat         DOUBLE PRECISION,
    fine_lng         DOUBLE PRECISION,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 11. Pagamenti
-- ============================================================

CREATE TABLE pagamenti (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    corsa_id              UUID NOT NULL REFERENCES corse(id) ON DELETE RESTRICT,
    utente_id             UUID NOT NULL REFERENCES utenti(id) ON DELETE RESTRICT,
    metodo_pagamento_id   UUID REFERENCES metodi_pagamento(id) ON DELETE SET NULL,
    importo               NUMERIC(10, 2) NOT NULL CHECK (importo >= 0),
    stato                 stato_pagamento NOT NULL DEFAULT 'in_attesa',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

- [ ] **Step 2: Esegui la migrazione su Supabase**

Apri il progetto Supabase → SQL Editor → incolla e lancia `001_init_schema.sql`.

Verifica nel Table Editor che compaiano le tabelle: `utenti`, `operatori`, `amministratori`, `mezzi`, `zone`, `tariffe`, `metodi_pagamento`, `prenotazioni`, `regole_fine_corsa`, `corse`, `pagamenti`.

- [ ] **Step 3: Commit**

```bash
git add backend/migrations/001_init_schema.sql
git commit -m "feat: add SQL migration 001 — full Sprint 1 schema with PostGIS"
```

---

## Task 3: Modelli — `utente.py`

**Files:**
- Modify: `backend/model/utente.py`

- [ ] **Step 1: Scrivi il test**

Crea `backend/tests/__init__.py` (file vuoto), poi `backend/tests/test_schema.py`:

```python
import uuid
from sqlalchemy import inspect


def test_utente_tablename():
    from model.utente import Utente
    assert Utente.__tablename__ == "utenti"


def test_utente_columns():
    from model.utente import Utente
    cols = {c.name for c in Utente.__table__.columns}
    assert cols == {"id", "nome", "cognome", "telefono", "sospeso", "created_at"}


def test_operatore_tablename():
    from model.utente import Operatore
    assert Operatore.__tablename__ == "operatori"


def test_operatore_columns():
    from model.utente import Operatore
    cols = {c.name for c in Operatore.__table__.columns}
    assert cols == {
        "id", "nome",
        "durata_max_prenotazione_min",
        "durata_periodo_grazia_min",
        "max_mezzi_per_utente",
        "created_at",
    }


def test_amministratore_tablename():
    from model.utente import AmministrazionePubblica
    assert AmministrazionePubblica.__tablename__ == "amministratori"
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py::test_utente_tablename -v
```

Output atteso: `FAILED` con `AttributeError: type object 'Utente' has no attribute '__tablename__'`

- [ ] **Step 3: Implementa `backend/model/utente.py`**

```python
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Utente(Base):
    __tablename__ = "utenti"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    cognome: Mapped[str] = mapped_column(String, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    sospeso: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class Operatore(Base):
    __tablename__ = "operatori"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    durata_max_prenotazione_min: Mapped[int] = mapped_column(
        nullable=False, default=15
    )
    durata_periodo_grazia_min: Mapped[int] = mapped_column(
        nullable=False, default=5
    )
    max_mezzi_per_utente: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class AmministrazionePubblica(Base):
    __tablename__ = "amministratori"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "utente or operatore or amministratore" -v
```

Output atteso: `5 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/model/utente.py backend/tests/__init__.py backend/tests/test_schema.py
git commit -m "feat: add SQLAlchemy ORM models for Utente, Operatore, AmministrazionePubblica"
```

---

## Task 4: Modelli — `mezzo.py`

**Files:**
- Modify: `backend/model/mezzo.py`

- [ ] **Step 1: Aggiungi test in `backend/tests/test_schema.py`**

Aggiungi in fondo al file:

```python
def test_tipo_mezzo_values():
    from model.mezzo import TipoMezzo
    assert set(TipoMezzo) == {
        TipoMezzo.monopattino,
        TipoMezzo.bicicletta,
        TipoMezzo.automobile,
    }


def test_stato_mezzo_values():
    from model.mezzo import StatoMezzo
    assert len(list(StatoMezzo)) == 7


def test_mezzo_columns():
    from model.mezzo import Mezzo
    cols = {c.name for c in Mezzo.__table__.columns}
    assert cols == {"id", "codice", "tipo", "stato", "lat", "lng", "batteria", "created_at"}
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py::test_mezzo_columns -v
```

Output atteso: `FAILED`

- [ ] **Step 3: Implementa `backend/model/mezzo.py`**

```python
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, Float, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoMezzo(str, Enum):
    monopattino = "monopattino"
    bicicletta = "bicicletta"
    automobile = "automobile"


class StatoMezzo(str, Enum):
    disponibile = "Disponibile"
    prenotato = "Prenotato"
    in_uso = "In uso"
    in_pausa = "In pausa"
    in_manutenzione = "In manutenzione"
    fuori_servizio = "Fuori servizio"
    dismesso = "Dismesso"


class Mezzo(Base):
    __tablename__ = "mezzi"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    codice: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    tipo: Mapped[TipoMezzo] = mapped_column(
        SAEnum(TipoMezzo, name="tipo_mezzo", create_type=False), nullable=False
    )
    stato: Mapped[StatoMezzo] = mapped_column(
        SAEnum(StatoMezzo, name="stato_mezzo", create_type=False),
        nullable=False,
        default=StatoMezzo.disponibile,
    )
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    batteria: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "mezzo" -v
```

Output atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/model/mezzo.py backend/tests/test_schema.py
git commit -m "feat: add SQLAlchemy ORM model for Mezzo with TipoMezzo and StatoMezzo enums"
```

---

## Task 5: Modelli — `zona.py`

**Files:**
- Modify: `backend/model/zona.py`

- [ ] **Step 1: Aggiungi test**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
def test_tipo_zona_values():
    from model.zona import TipoZona
    assert set(e.value for e in TipoZona) == {"operativa", "parcheggio", "limitata", "vietata"}


def test_zona_columns():
    from model.zona import Zona
    cols = {c.name for c in Zona.__table__.columns}
    assert cols == {"id", "nome", "tipo", "perimetro", "limite_velocita", "attiva", "created_at"}


def test_zona_perimetro_is_geometry():
    from model.zona import Zona
    from geoalchemy2 import Geometry
    col = Zona.__table__.columns["perimetro"]
    assert isinstance(col.type, Geometry)
    assert col.type.geometry_type == "POLYGON"
    assert col.type.srid == 4326
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py::test_zona_columns -v
```

Output atteso: `FAILED`

- [ ] **Step 3: Implementa `backend/model/zona.py`**

```python
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Boolean, Integer, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from geoalchemy2 import Geometry
from database import Base


class TipoZona(str, Enum):
    operativa = "operativa"
    parcheggio = "parcheggio"
    limitata = "limitata"
    vietata = "vietata"


class Zona(Base):
    __tablename__ = "zone"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    tipo: Mapped[TipoZona] = mapped_column(
        SAEnum(TipoZona, name="tipo_zona", create_type=False), nullable=False
    )
    perimetro: Mapped[bytes] = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=False
    )
    limite_velocita: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attiva: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "zona" -v
```

Output atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/model/zona.py backend/tests/test_schema.py
git commit -m "feat: add SQLAlchemy ORM model for Zona with PostGIS geometry"
```

---

## Task 6: Modelli — `prenotazione.py` e `corsa.py`

**Files:**
- Create: `backend/model/prenotazione.py`
- Modify: `backend/model/corsa.py`

- [ ] **Step 1: Aggiungi test**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
def test_prenotazione_columns():
    from model.prenotazione import Prenotazione
    cols = {c.name for c in Prenotazione.__table__.columns}
    assert cols == {"id", "utente_id", "mezzo_id", "stato", "scade_at", "created_at"}


def test_stato_prenotazione_values():
    from model.prenotazione import StatoPrenotazione
    assert set(e.value for e in StatoPrenotazione) == {
        "attiva", "scaduta", "annullata", "convertita"
    }


def test_corsa_columns():
    from model.corsa import Corsa
    cols = {c.name for c in Corsa.__table__.columns}
    assert cols == {
        "id", "utente_id", "mezzo_id", "prenotazione_id",
        "stato", "inizio_at", "fine_at", "distanza_km",
        "inizio_lat", "inizio_lng", "fine_lat", "fine_lng", "created_at",
    }


def test_corsa_prenotazione_id_is_nullable():
    from model.corsa import Corsa
    col = Corsa.__table__.columns["prenotazione_id"]
    assert col.nullable is True
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py -k "prenotazione or corsa" -v
```

Output atteso: `FAILED`

- [ ] **Step 3: Crea `backend/model/prenotazione.py`**

```python
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class StatoPrenotazione(str, Enum):
    attiva = "attiva"
    scaduta = "scaduta"
    annullata = "annullata"
    convertita = "convertita"


class Prenotazione(Base):
    __tablename__ = "prenotazioni"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="CASCADE"),
        nullable=False,
    )
    mezzo_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("mezzi.id", ondelete="RESTRICT"),
        nullable=False,
    )
    stato: Mapped[StatoPrenotazione] = mapped_column(
        SAEnum(StatoPrenotazione, name="stato_prenotazione", create_type=False),
        nullable=False,
        default=StatoPrenotazione.attiva,
    )
    scade_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Sostituisci `backend/model/corsa.py`**

```python
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import DateTime, Numeric, Float, text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class StatoCorsa(str, Enum):
    in_uso = "in_uso"
    in_pausa = "in_pausa"
    terminata = "terminata"


class Corsa(Base):
    __tablename__ = "corse"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="RESTRICT"),
        nullable=False,
    )
    mezzo_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("mezzi.id", ondelete="RESTRICT"),
        nullable=False,
    )
    # [IF-UT.04] nullable: CS-10 permette sblocco diretto senza prenotazione
    prenotazione_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("prenotazioni.id", ondelete="SET NULL"),
        nullable=True,
    )
    stato: Mapped[StatoCorsa] = mapped_column(
        SAEnum(StatoCorsa, name="stato_corsa", create_type=False),
        nullable=False,
        default=StatoCorsa.in_uso,
    )
    inizio_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fine_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    distanza_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 3), nullable=True)
    inizio_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    inizio_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    fine_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    fine_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 5: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "prenotazione or corsa" -v
```

Output atteso: `4 passed`

- [ ] **Step 6: Commit**

```bash
git add backend/model/prenotazione.py backend/model/corsa.py backend/tests/test_schema.py
git commit -m "feat: add ORM models for Prenotazione and Corsa (prenotazione_id nullable — CS-10)"
```

---

## Task 7: Modelli — `pagamento.py`

**Files:**
- Modify: `backend/model/pagamento.py`

- [ ] **Step 1: Aggiungi test**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
def test_metodo_pagamento_columns():
    from model.pagamento import MetodoPagamento
    cols = {c.name for c in MetodoPagamento.__table__.columns}
    assert cols == {
        "id", "utente_id", "tipo", "token_esterno", "last_four", "predefinito", "created_at"
    }


def test_pagamento_columns():
    from model.pagamento import Pagamento
    cols = {c.name for c in Pagamento.__table__.columns}
    assert cols == {
        "id", "corsa_id", "utente_id", "metodo_pagamento_id", "importo", "stato", "created_at"
    }


def test_pagamento_metodo_id_is_nullable():
    from model.pagamento import Pagamento
    col = Pagamento.__table__.columns["metodo_pagamento_id"]
    assert col.nullable is True
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py -k "metodo_pagamento or pagamento" -v
```

Output atteso: `FAILED`

- [ ] **Step 3: Sostituisci `backend/model/pagamento.py`**

```python
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Boolean, Numeric, DateTime, text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoMetodoPagamento(str, Enum):
    google_pay = "google_pay"
    apple_pay = "apple_pay"
    paypal = "paypal"
    carta = "carta"


class StatoPagamento(str, Enum):
    completato = "completato"
    rifiutato = "rifiutato"
    in_attesa = "in_attesa"


class MetodoPagamento(Base):
    __tablename__ = "metodi_pagamento"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="CASCADE"),
        nullable=False,
    )
    tipo: Mapped[TipoMetodoPagamento] = mapped_column(
        SAEnum(TipoMetodoPagamento, name="tipo_metodo_pagamento", create_type=False),
        nullable=False,
    )
    token_esterno: Mapped[str] = mapped_column(String, nullable=False)
    last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    predefinito: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class Pagamento(Base):
    __tablename__ = "pagamenti"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    corsa_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("corse.id", ondelete="RESTRICT"),
        nullable=False,
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="RESTRICT"),
        nullable=False,
    )
    # [IF-UT.20] nullable: CS-12.1 il metodo potrebbe essere rimosso dopo un pagamento rifiutato
    metodo_pagamento_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("metodi_pagamento.id", ondelete="SET NULL"),
        nullable=True,
    )
    importo: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    stato: Mapped[StatoPagamento] = mapped_column(
        SAEnum(StatoPagamento, name="stato_pagamento", create_type=False),
        nullable=False,
        default=StatoPagamento.in_attesa,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "pagamento" -v
```

Output atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/model/pagamento.py backend/tests/test_schema.py
git commit -m "feat: add ORM models for MetodoPagamento and Pagamento"
```

---

## Task 8: Modelli — `tariffa.py` e `regola_fine_corsa.py`

**Files:**
- Create: `backend/model/tariffa.py`
- Create: `backend/model/regola_fine_corsa.py`

- [ ] **Step 1: Aggiungi test**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
def test_tariffa_columns():
    from model.tariffa import Tariffa
    cols = {c.name for c in Tariffa.__table__.columns}
    assert cols == {
        "id", "tipo_mezzo", "costo_al_minuto", "costo_al_km", "created_at", "aggiornata_at"
    }


def test_tariffa_tipo_mezzo_unique():
    from model.tariffa import Tariffa
    col = Tariffa.__table__.columns["tipo_mezzo"]
    assert col.unique is True


def test_regola_fine_corsa_columns():
    from model.regola_fine_corsa import RegolaFinecorsa
    cols = {c.name for c in RegolaFinecorsa.__table__.columns}
    assert cols == {
        "id", "zona_parcheggio_id", "batteria_minima",
        "penale_fuori_zona", "tipo_vincolo", "created_at",
    }
```

- [ ] **Step 2: Esegui il test — deve fallire**

```bash
cd backend && uv run pytest tests/test_schema.py -k "tariffa or regola" -v
```

Output atteso: `FAILED`

- [ ] **Step 3: Crea `backend/model/tariffa.py`**

```python
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from model.mezzo import TipoMezzo
from database import Base


class Tariffa(Base):
    __tablename__ = "tariffe"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tipo_mezzo: Mapped[TipoMezzo] = mapped_column(
        SAEnum(TipoMezzo, name="tipo_mezzo", create_type=False),
        unique=True,
        nullable=False,
    )
    costo_al_minuto: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    costo_al_km: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    aggiornata_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 4: Crea `backend/model/regola_fine_corsa.py`**

```python
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import Integer, Numeric, DateTime, text, ForeignKey
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

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # zona referenziata deve avere tipo='parcheggio' — verificato in ServizioMobilità
    zona_parcheggio_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="CASCADE"),
        nullable=False,
    )
    batteria_minima: Mapped[int | None] = mapped_column(Integer, nullable=True)
    penale_fuori_zona: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00")
    )
    tipo_vincolo: Mapped[TipoVincoloFinecorsa] = mapped_column(
        SAEnum(TipoVincoloFinecorsa, name="tipo_vincolo_fine_corsa", create_type=False),
        nullable=False,
        default=TipoVincoloFinecorsa.avviso,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
```

- [ ] **Step 5: Esegui i test — devono passare**

```bash
cd backend && uv run pytest tests/test_schema.py -k "tariffa or regola" -v
```

Output atteso: `3 passed`

- [ ] **Step 6: Esegui tutti i test**

```bash
cd backend && uv run pytest tests/test_schema.py -v
```

Output atteso: tutti i test passano, nessun `FAILED`.

- [ ] **Step 7: Commit**

```bash
git add backend/model/tariffa.py backend/model/regola_fine_corsa.py backend/tests/test_schema.py
git commit -m "feat: add ORM models for Tariffa and RegolaFinecorsa — completes Sprint 1 schema"
```

---

## Task 9: Test di integrazione (opzionale — richiede DB)

**Files:**
- Modify: `backend/tests/test_schema.py`

Questi test verificano che lo schema sia effettivamente applicato su Supabase. Richiede `DATABASE_URL` in `backend/.env`.

- [ ] **Step 1: Aggiungi test di integrazione**

Aggiungi in fondo a `backend/tests/test_schema.py`:

```python
import pytest
import os


@pytest.mark.integration
def test_all_tables_exist():
    """Verifica che la migrazione SQL abbia creato tutte le tabelle attese."""
    from sqlalchemy import inspect as sa_inspect
    from database import engine

    inspector = sa_inspect(engine)
    existing = set(inspector.get_table_names(schema="public"))
    expected = {
        "utenti", "operatori", "amministratori",
        "mezzi", "zone", "tariffe",
        "metodi_pagamento", "prenotazioni",
        "regole_fine_corsa", "corse", "pagamenti",
    }
    assert expected.issubset(existing), f"Tabelle mancanti: {expected - existing}"


@pytest.mark.integration
def test_zone_gist_index_exists():
    """Verifica che l'indice GIST su zone.perimetro sia presente."""
    from sqlalchemy import text
    from database import engine

    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'zone' AND indexdef LIKE '%USING gist%'"
        ))
        indexes = [row[0] for row in result]
    assert len(indexes) >= 1, "Indice GIST su zone.perimetro non trovato"
```

- [ ] **Step 2: Configura pytest per saltare i test di integrazione senza DB**

Crea `backend/pytest.ini`:

```ini
[pytest]
markers =
    integration: test che richiedono connessione al database reale
```

- [ ] **Step 3: Esegui solo unit test (default)**

```bash
cd backend && uv run pytest tests/test_schema.py -v -m "not integration"
```

Output atteso: tutti i test unitari passano.

- [ ] **Step 4: Esegui i test di integrazione (con DB attivo)**

```bash
cd backend && uv run pytest tests/test_schema.py -v -m integration
```

Output atteso: `2 passed` — richiede `DATABASE_URL` in `.env` e migrazione già eseguita.

- [ ] **Step 5: Commit**

```bash
git add backend/tests/test_schema.py backend/pytest.ini
git commit -m "test: add integration tests for DB schema verification"
```

---

## Checklist di completamento

- [ ] `uv sync` senza errori
- [ ] `uv run pytest tests/test_schema.py -m "not integration"` — tutti i test unitari passano
- [ ] SQL migration applicata su Supabase senza errori
- [ ] `uv run pytest tests/test_schema.py -m integration` — test di integrazione passano
- [ ] Tutti i commit presenti sul branch corrente
