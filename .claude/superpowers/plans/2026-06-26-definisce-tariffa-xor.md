# OP-05 Definisce Tariffa — scelta minuto/km XOR — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allineare la creazione/modifica tariffa (OP-05) al vincolo del diagramma delle classi — esattamente uno tra `costo_al_minuto` e `costo_al_km` è impostato — e far emergere l'errore "tariffa già esistente" (OP-05.1) alla selezione del tipo mezzo invece di filtrare preventivamente le opzioni.

**Architecture:** Backend: colonne `costo_al_minuto`/`costo_al_km` diventano nullable con un `CHECK` XOR a livello DB più validazione Pydantic a livello API. Frontend: il form passa da "due campi sempre visibili" a "scelta del tipo di tariffa (radio) + un solo valore", e il dropdown tipo mezzo mostra sempre tutte le tipologie con validazione duplicato inline.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 + Pydantic (backend), React 19 + TypeScript + Axios (frontend), pytest (test).

## Global Constraints

- Glossario di progetto: usare sempre `Tariffa`, `Mezzo`, mai sinonimi inglesi (da `CLAUDE.md`).
- Controller = solo validazione HTTP, BLL = logica applicativa, DAL = solo accesso dati — non mescolare layer (da `CLAUDE.md`).
- Non inventare classi/campi non presenti nel diagramma delle classi (`docs/Diagrammi/DiagrammaClassi.md` è la fonte di verità) — qui il diagramma già specifica `costoPerMinuto: float?`, `costoPerKm: float?` con vincolo XOR, quindi il codice deve raggiungerlo, non il contrario.
- Test indipendenti, niente mock del DB per i test che verificano comportamento persistente (i test di integrazione in `test_tariffa_http.py` restano marcati `@pytest.mark.integration` e usano DB reale).
- Non eseguire `npm run build`/push su `main` con build rotta.

---

### Task 1: Migrazione DB e modello `Tariffa` nullable + vincolo XOR

**Files:**
- Create: `backend/migrations/021_tariffa_xor_costo.sql`
- Modify: `backend/model/tariffa.py`
- Test: `backend/tests/test_servizio_tariffa.py` (nessuna modifica in questo task, verificato solo che i test esistenti restino verdi dopo il cambio di modello — sono tutti mockati e non toccano il DB reale)

**Interfaces:**
- Produces: `Tariffa.costo_al_minuto: Decimal | None`, `Tariffa.costo_al_km: Decimal | None` — usati da Task 2, 3, 4, 5.

- [ ] **Step 1: Scrivere la migrazione SQL**

Crea `backend/migrations/021_tariffa_xor_costo.sql`:

```sql
-- ============================================================
-- OP-05: una tariffa ha esattamente un tipo di costo (minuto XOR km),
-- come specificato nel diagramma delle classi (Tariffa.costoPerMinuto/
-- costoPerKm: float?, vincolo: esattamente uno dei due non-null).
-- ============================================================

ALTER TABLE tariffe
    ALTER COLUMN costo_al_minuto DROP NOT NULL,
    ALTER COLUMN costo_al_km DROP NOT NULL;

-- Le righe esistenti avevano entrambi i valori popolati: si mantiene
-- costo_al_minuto e si azzera costo_al_km per rispettare il nuovo vincolo.
UPDATE tariffe SET costo_al_km = NULL WHERE costo_al_minuto IS NOT NULL;

ALTER TABLE tariffe
    DROP CONSTRAINT IF EXISTS tariffa_costo_minuto_positivo,
    DROP CONSTRAINT IF EXISTS tariffa_costo_km_positivo;

ALTER TABLE tariffe
    ADD CONSTRAINT tariffa_costo_xor CHECK (
        (costo_al_minuto IS NOT NULL AND costo_al_km IS NULL AND costo_al_minuto > 0)
        OR
        (costo_al_km IS NOT NULL AND costo_al_minuto IS NULL AND costo_al_km > 0)
    );
```

- [ ] **Step 2: Applicare la migrazione sul DB Supabase usato per i test di integrazione**

Apri Supabase → SQL Editor (o `psql $DATABASE_URL`) ed esegui il contenuto del file creato al passo 1. Verifica con:

```sql
SELECT tipo_mezzo, costo_al_minuto, costo_al_km FROM tariffe;
```

Expected: ogni riga ha `costo_al_minuto` popolato e `costo_al_km` `NULL` (o viceversa se erano già stati modificati manualmente).

- [ ] **Step 3: Aggiornare il modello SQLAlchemy**

In `backend/model/tariffa.py`, sostituisci il contenuto della classe:

```python
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric, DateTime, text, CheckConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from model.mezzo import TipoMezzo
from database import Base


class Tariffa(Base):
    __tablename__ = "tariffe"
    __table_args__ = (
        CheckConstraint(
            "(costo_al_minuto IS NOT NULL AND costo_al_km IS NULL AND costo_al_minuto > 0) "
            "OR (costo_al_km IS NOT NULL AND costo_al_minuto IS NULL AND costo_al_km > 0)",
            name="tariffa_costo_xor",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tipo_mezzo: Mapped[TipoMezzo] = mapped_column(
        SAEnum(TipoMezzo, name="tipo_mezzo", create_type=False),
        unique=True,
        nullable=False,
    )
    costo_al_minuto: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    costo_al_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    aggiornata_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=func.now(),
    )
```

- [ ] **Step 4: Eseguire i test unitari esistenti per verificare che nulla si rompa**

Run: `cd backend && uv run pytest tests/test_servizio_tariffa.py -v -m "not integration"`
Expected: PASS (questi test mockano `TariffaRepository`, non toccano il modello direttamente, quindi devono restare verdi).

- [ ] **Step 5: Commit**

```bash
git add backend/migrations/021_tariffa_xor_costo.sql backend/model/tariffa.py
git commit -m "feat(tariffa): rendi costo_al_minuto/costo_al_km nullable con vincolo XOR"
```

---

### Task 2: Schemi Pydantic con validazione XOR

**Files:**
- Modify: `backend/controllers/schemas.py:79-89`
- Test: `backend/tests/test_tariffa_schemas.py` (nuovo file)

**Interfaces:**
- Consumes: nessuna dipendenza da Task 1 a livello di import (Pydantic è indipendente dal modello SQLAlchemy).
- Produces: `CreaTariffaRequest(tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None)` che lancia `pydantic.ValidationError` se non esattamente uno dei due è popolato e > 0. `TariffaResponse` con gli stessi due campi opzionali. Usati da Task 3 (controller) e Task 4 (servizio).

- [ ] **Step 1: Scrivere il test che fallisce**

Crea `backend/tests/test_tariffa_schemas.py`:

```python
import pytest
from pydantic import ValidationError
from controllers.schemas import CreaTariffaRequest


class TestCreaTariffaRequestXor:

    def test_solo_costo_al_minuto_valido(self):
        req = CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0.15, costo_al_km=None)
        assert req.costo_al_minuto == 0.15
        assert req.costo_al_km is None

    def test_solo_costo_al_km_valido(self):
        req = CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=None, costo_al_km=0.20)
        assert req.costo_al_km == 0.20
        assert req.costo_al_minuto is None

    def test_entrambi_popolati_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0.15, costo_al_km=0.20)

    def test_nessuno_popolato_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=None, costo_al_km=None)

    def test_valore_zero_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0, costo_al_km=None)

    def test_valore_negativo_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=-0.05, costo_al_km=None)
```

- [ ] **Step 2: Eseguire i test per verificare che falliscano**

Run: `cd backend && uv run pytest tests/test_tariffa_schemas.py -v`
Expected: FAIL — `CreaTariffaRequest` accetta ancora `costo_al_minuto`/`costo_al_km` come `float` obbligatori (non `None`), quindi i test con `None` falliscono con `ValidationError` di tipo sbagliato o i test "rifiutato" non lanciano nulla.

- [ ] **Step 3: Aggiornare gli schemi**

In `backend/controllers/schemas.py`, sostituisci le righe 79-89:

```python
class CreaTariffaRequest(BaseModel):
    tipo_mezzo: str
    costo_al_minuto: float | None = None
    costo_al_km: float | None = None

    @model_validator(mode="after")
    def valida_xor_costo(self) -> "CreaTariffaRequest":
        minuto, km = self.costo_al_minuto, self.costo_al_km
        if (minuto is None) == (km is None):
            raise ValueError(
                "Specificare esattamente uno tra costo_al_minuto e costo_al_km"
            )
        valore = minuto if minuto is not None else km
        if valore is None or valore <= 0:
            raise ValueError("Il costo deve essere un numero maggiore di zero")
        return self


class TariffaResponse(BaseModel):
    id: str
    tipo_mezzo: str
    costo_al_minuto: float | None
    costo_al_km: float | None
```

Verifica l'import in testa al file: se `model_validator` non è già importato da `pydantic`, aggiungi `model_validator` all'import esistente (`from pydantic import BaseModel, ...`).

- [ ] **Step 4: Eseguire i test per verificare che passino**

Run: `cd backend && uv run pytest tests/test_tariffa_schemas.py -v`
Expected: PASS (6 test).

- [ ] **Step 5: Commit**

```bash
git add backend/controllers/schemas.py backend/tests/test_tariffa_schemas.py
git commit -m "feat(tariffa): valida XOR costo_al_minuto/costo_al_km negli schemi Pydantic"
```

---

### Task 3: `TariffaRepository` — propagare valori opzionali

**Files:**
- Modify: `backend/dal/tariffa_repository.py`
- Test: `backend/tests/test_tariffa_repository.py` (nuovo file)

**Interfaces:**
- Consumes: `Tariffa` model da Task 1 (`costo_al_minuto: Decimal | None`, `costo_al_km: Decimal | None`).
- Produces: `TariffaRepository.crea(tipo_mezzo: str, costo_al_minuto: Decimal | None, costo_al_km: Decimal | None) -> Tariffa`, `.aggiorna(tipo_mezzo, costo_al_minuto: Decimal | None, costo_al_km: Decimal | None) -> Tariffa | None`, `.findAll() -> list[dict]` con campi `costo_al_minuto`/`costo_al_km` come `str | None`. Usati da Task 4.

- [ ] **Step 1: Scrivere il test che fallisce**

Crea `backend/tests/test_tariffa_repository.py`:

```python
import uuid
from decimal import Decimal
from unittest.mock import MagicMock, patch


class TestTariffaRepositoryFindAll:

    def test_find_all_propaga_costo_km_none(self):
        from dal.tariffa_repository import TariffaRepository

        riga = MagicMock()
        riga.id = uuid.uuid4()
        riga.tipo_mezzo = "monopattino"
        riga.costo_al_minuto = Decimal("0.05")
        riga.costo_al_km = None

        mock_session = MagicMock()
        mock_session.execute.return_value.fetchall.return_value = [riga]

        with patch("dal.tariffa_repository.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = mock_session
            result = TariffaRepository().find_all()

        assert len(result) == 1
        assert result[0].costo_al_minuto == Decimal("0.05")
        assert result[0].costo_al_km is None

    def test_crea_con_solo_costo_al_km(self):
        from dal.tariffa_repository import TariffaRepository

        mock_session = MagicMock()

        with patch("dal.tariffa_repository.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = mock_session
            TariffaRepository().crea("automobile", None, Decimal("0.20"))

        added = mock_session.add.call_args[0][0]
        assert added.tipo_mezzo == "automobile"
        assert added.costo_al_minuto is None
        assert added.costo_al_km == Decimal("0.20")
```

- [ ] **Step 2: Eseguire i test per verificare che falliscano**

Run: `cd backend && uv run pytest tests/test_tariffa_repository.py -v`
Expected: FAIL — `find_all` oggi legge `costo_al_minuto`/`costo_al_km` dalla riga senza problemi (sono già passthrough), ma `crea`/`aggiorna` forzano `Decimal(str(...))` su entrambi i parametri nel chiamante (`servizio_tariffa.py`), non nel repository stesso: il repository di per sé già accetta `Decimal | None` come tipo perché Python non valida i tipi a runtime — il test `test_crea_con_solo_costo_al_km` fallisce perché l'attuale type hint dichiarato (`Decimal`) non genera errore Python ma la query INSERT con SQLAlchemy ORM funziona comunque. Esegui il test per confermare lo stato reale prima di modificare; se passa già, procedi comunque al passo 3 per allineare i type hint e l'SQL raw di `aggiorna`/`findAll` ai valori opzionali.

- [ ] **Step 3: Aggiornare il repository**

In `backend/dal/tariffa_repository.py`, sostituisci l'intero file:

```python
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.tariffa import Tariffa


class TariffaRepository:

    def __init__(self, db: Session | None = None) -> None:
        self._db = db

    # [IF-UT.05] — db injection pattern (pricing_controller)
    def findAll(self) -> list[dict]:
        if self._db is None:
            raise RuntimeError("TariffaRepository.findAll richiede db iniettato")
        rows = self._db.query(Tariffa).all()
        return [
            {
                "id": str(r.id),
                "tipo_mezzo": r.tipo_mezzo.value,
                "costo_al_minuto": f"{r.costo_al_minuto:.4f}" if r.costo_al_minuto is not None else None,
                "costo_al_km": f"{r.costo_al_km:.4f}" if r.costo_al_km is not None else None,
            }
            for r in rows
        ]

    # [IF-OP.07] — engine pattern (ServizioPricing pagamenti)
    def find_all(self) -> list[Tariffa]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, tipo_mezzo, costo_al_minuto, costo_al_km "
                    "FROM tariffe ORDER BY tipo_mezzo"
                )
            ).fetchall()
            return [
                Tariffa(
                    id=r.id,
                    tipo_mezzo=r.tipo_mezzo,
                    costo_al_minuto=r.costo_al_minuto,
                    costo_al_km=r.costo_al_km,
                )
                for r in rows
            ]

    def exists_by_tipologia(self, tipo_mezzo: str) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text("SELECT 1 FROM tariffe WHERE tipo_mezzo = :tipo LIMIT 1"),
                {"tipo": tipo_mezzo},
            ).fetchone()
        return result is not None

    def aggiorna(
        self, tipo_mezzo: str, costo_al_minuto: Decimal | None, costo_al_km: Decimal | None
    ) -> Tariffa | None:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "UPDATE tariffe SET costo_al_minuto = :minuto, costo_al_km = :km "
                    "WHERE tipo_mezzo = :tipo "
                    "RETURNING id, tipo_mezzo, costo_al_minuto, costo_al_km"
                ),
                {
                    "minuto": str(costo_al_minuto) if costo_al_minuto is not None else None,
                    "km": str(costo_al_km) if costo_al_km is not None else None,
                    "tipo": tipo_mezzo,
                },
            ).fetchone()
            session.commit()
        if not row:
            return None
        return Tariffa(id=row.id, tipo_mezzo=row.tipo_mezzo, costo_al_minuto=row.costo_al_minuto, costo_al_km=row.costo_al_km)

    def crea(
        self, tipo_mezzo: str, costo_al_minuto: Decimal | None, costo_al_km: Decimal | None
    ) -> Tariffa:
        with Session(engine) as session:
            tariffa = Tariffa(
                tipo_mezzo=tipo_mezzo,
                costo_al_minuto=costo_al_minuto,
                costo_al_km=costo_al_km,
            )
            session.add(tariffa)
            session.commit()
            session.refresh(tariffa)
            return tariffa
```

- [ ] **Step 4: Eseguire i test per verificare che passino**

Run: `cd backend && uv run pytest tests/test_tariffa_repository.py -v`
Expected: PASS (2 test).

- [ ] **Step 5: Commit**

```bash
git add backend/dal/tariffa_repository.py backend/tests/test_tariffa_repository.py
git commit -m "feat(tariffa): TariffaRepository propaga costo_al_minuto/costo_al_km opzionali"
```

---

### Task 4: `ServizioTariffa` — creare/aggiornare con un solo costo

**Files:**
- Modify: `backend/bll/servizio_tariffa.py`
- Modify: `backend/tests/test_servizio_tariffa.py`

**Interfaces:**
- Consumes: `TariffaRepository.crea/aggiorna(tipo_mezzo, costo_al_minuto: Decimal | None, costo_al_km: Decimal | None)` da Task 3.
- Produces: `ServizioTariffa.crea_tariffa(tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None, operatore_id: UUID) -> dict`, `.aggiorna_tariffa(...)` stessa firma. Usati da Task 5 (controller).

- [ ] **Step 1: Aggiornare i test esistenti per il nuovo formato (uno-dei-due)**

Sostituisci in `backend/tests/test_servizio_tariffa.py` il contenuto da `test_get_tariffe_delega_al_repository` a `test_crea_tariffa_delega_al_repository` (righe 9-61) con:

```python
    def test_get_tariffe_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        riga = MagicMock()
        riga.id = uuid.uuid4()
        riga.tipo_mezzo = "monopattino"
        riga.costo_al_minuto = Decimal("0.05")
        riga.costo_al_km = None

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = [riga]
            result = ServizioTariffa().get_tariffe()

        assert result == [{
            "id": str(riga.id),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": 0.05,
            "costo_al_km": None,
        }]

    def test_get_tariffe_lista_vuota(self):
        from bll.servizio_tariffa import ServizioTariffa

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = []
            result = ServizioTariffa().get_tariffe()

        assert result == []

    def test_crea_tariffa_solo_costo_al_km(self):
        from bll.servizio_tariffa import ServizioTariffa

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "bicicletta"
        tariffa.costo_al_minuto = None
        tariffa.costo_al_km = Decimal("0.08")
        operatore_id = uuid.uuid4()

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche") as MockStorico:
            MockRepo.return_value.exists_by_tipologia.return_value = False
            MockRepo.return_value.crea.return_value = tariffa
            result = ServizioTariffa().crea_tariffa("bicicletta", None, 0.08, operatore_id)

        MockRepo.return_value.crea.assert_called_once_with("bicicletta", None, Decimal("0.08"))
        assert result["tipo_mezzo"] == "bicicletta"
        assert result["costo_al_minuto"] is None
        assert result["costo_al_km"] == 0.08
        MockStorico.return_value.registra_modifica.assert_called_once()
        kwargs = MockStorico.return_value.registra_modifica.call_args.kwargs
        assert kwargs["tipo_configurazione"] == "tariffa_creata"
        assert kwargs["valore_precedente"] is None
        assert "tipo_mezzo=bicicletta" in kwargs["valore_nuovo"]
        assert kwargs["operatore_id"] == operatore_id
```

Aggiungi inoltre, dopo `test_crea_tariffa_gia_esistente`, un test per il caso minuto:

```python
    def test_crea_tariffa_solo_costo_al_minuto(self):
        from bll.servizio_tariffa import ServizioTariffa

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "automobile"
        tariffa.costo_al_minuto = Decimal("0.25")
        tariffa.costo_al_km = None
        operatore_id = uuid.uuid4()

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche"):
            MockRepo.return_value.exists_by_tipologia.return_value = False
            MockRepo.return_value.crea.return_value = tariffa
            result = ServizioTariffa().crea_tariffa("automobile", 0.25, None, operatore_id)

        MockRepo.return_value.crea.assert_called_once_with("automobile", Decimal("0.25"), None)
        assert result["costo_al_km"] is None
```

Aggiorna anche `test_aggiorna_tariffa_delega_al_repository` (righe 77-102 nel file originale) per usare un solo costo:

```python
    def test_aggiorna_tariffa_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        precedente = MagicMock()
        precedente.tipo_mezzo = "monopattino"
        precedente.costo_al_minuto = Decimal("0.05")
        precedente.costo_al_km = None

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "monopattino"
        tariffa.costo_al_minuto = Decimal("0.07")
        tariffa.costo_al_km = None
        operatore_id = uuid.uuid4()

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche") as MockStorico:
            MockRepo.return_value.find_all.return_value = [precedente]
            MockRepo.return_value.aggiorna.return_value = tariffa
            result = ServizioTariffa().aggiorna_tariffa("monopattino", 0.07, None, operatore_id)

        assert result["costo_al_minuto"] == 0.07
        assert result["costo_al_km"] is None
        kwargs = MockStorico.return_value.registra_modifica.call_args.kwargs
        assert kwargs["tipo_configurazione"] == "tariffa_modificata"
        assert "costo_al_minuto=0.05" in kwargs["valore_precedente"]
        assert "costo_al_minuto=0.07" in kwargs["valore_nuovo"]
```

- [ ] **Step 2: Eseguire i test per verificare che falliscano**

Run: `cd backend && uv run pytest tests/test_servizio_tariffa.py -v`
Expected: FAIL — `crea_tariffa`/`aggiorna_tariffa` chiamano `Decimal(str(costo_al_minuto))` incondizionatamente, quindi passare `None` lancia `decimal.InvalidOperation` o `TypeError`.

- [ ] **Step 3: Aggiornare il servizio**

Sostituisci `backend/bll/servizio_tariffa.py`:

```python
from decimal import Decimal
from uuid import UUID
from dal.tariffa_repository import TariffaRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
    pass


def _a_decimal(valore: float | None) -> Decimal | None:
    return Decimal(str(valore)) if valore is not None else None


def _tariffa_a_dict(tariffa) -> dict:
    return {
        "id": str(tariffa.id),
        "tipo_mezzo": tariffa.tipo_mezzo,
        "costo_al_minuto": float(tariffa.costo_al_minuto) if tariffa.costo_al_minuto is not None else None,
        "costo_al_km": float(tariffa.costo_al_km) if tariffa.costo_al_km is not None else None,
    }


def _descrivi(tariffa) -> str:
    return (
        f"tipo_mezzo={tariffa.tipo_mezzo}, "
        f"costo_al_minuto={tariffa.costo_al_minuto}, "
        f"costo_al_km={tariffa.costo_al_km}"
    )


class ServizioTariffa:
    """[IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa."""

    def __init__(self, tariffa_repo: TariffaRepository | None = None):
        self._tariffa_repo = tariffa_repo or TariffaRepository()
        self._storico = ServizioStoricoModifiche()

    def get_tariffe(self) -> list[dict]:
        tariffe = self._tariffa_repo.find_all()
        return [_tariffa_a_dict(t) for t in tariffe]

    def crea_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None, operatore_id: UUID
    ) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            _a_decimal(costo_al_minuto),
            _a_decimal(costo_al_km),
        )
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_creata",
            descrizione=f"Creazione tariffa '{tipo_mezzo}'",
            valore_precedente=None,
            valore_nuovo=_descrivi(tariffa),
            operatore_id=operatore_id,
        )
        return _tariffa_a_dict(tariffa)

    def aggiorna_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None, operatore_id: UUID
    ) -> dict:
        precedenti = [t for t in self._tariffa_repo.find_all() if t.tipo_mezzo == tipo_mezzo]
        precedente = precedenti[0] if precedenti else None
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            _a_decimal(costo_al_minuto),
            _a_decimal(costo_al_km),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_modificata",
            descrizione=f"Modifica tariffa '{tipo_mezzo}'",
            valore_precedente=_descrivi(precedente) if precedente is not None else None,
            valore_nuovo=_descrivi(tariffa),
            operatore_id=operatore_id,
        )
        return _tariffa_a_dict(tariffa)
```

- [ ] **Step 4: Eseguire i test per verificare che passino**

Run: `cd backend && uv run pytest tests/test_servizio_tariffa.py -v`
Expected: PASS (8 test: i 6 esistenti aggiornati + `test_crea_tariffa_solo_costo_al_km` + `test_crea_tariffa_solo_costo_al_minuto`).

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_tariffa.py backend/tests/test_servizio_tariffa.py
git commit -m "feat(tariffa): ServizioTariffa supporta costo_al_minuto XOR costo_al_km"
```

---

### Task 5: `ServizioPricing.calcola_importo` — gestire il costo nullo

**Files:**
- Modify: `backend/bll/servizio_pricing.py:63-73`
- Test: `backend/tests/test_calcola_importo.py` (nuovo file)

**Interfaces:**
- Consumes: tabella `tariffe` con `costo_al_minuto`/`costo_al_km` opzionali (Task 1).
- Produces: `ServizioPricing.calcola_importo(tipo_mezzo: str, durata_min: float, distanza_km: float) -> Decimal` — comportamento osservabile invariato per i chiamanti esistenti (`effettua_pagamento`), ma ora tollera uno dei due campi `None`.

- [ ] **Step 1: Scrivere il test che fallisce**

Crea `backend/tests/test_calcola_importo.py`:

```python
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from bll.servizio_pricing import ServizioPricing
from bll.servizio_tariffa import TariffaNonTrovata
import pytest


def _mock_session_con_riga(riga):
    mock_session = MagicMock()
    mock_session.execute.return_value.fetchone.return_value = riga
    return mock_session


class TestCalcolaImporto:

    def test_tariffa_solo_al_minuto(self):
        riga = SimpleNamespace(costo_al_minuto=Decimal("0.05"), costo_al_km=None)
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(riga)
            importo = ServizioPricing().calcola_importo("monopattino", 10.0, 999.0)

        assert importo == Decimal("0.5")

    def test_tariffa_solo_al_km(self):
        riga = SimpleNamespace(costo_al_minuto=None, costo_al_km=Decimal("0.20"))
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(riga)
            importo = ServizioPricing().calcola_importo("automobile", 999.0, 3.0)

        assert importo == Decimal("0.6")

    def test_tariffa_inesistente(self):
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(None)
            with pytest.raises(TariffaNonTrovata):
                ServizioPricing().calcola_importo("monopattino", 10.0, 1.0)
```

- [ ] **Step 2: Eseguire i test per verificare che falliscano**

Run: `cd backend && uv run pytest tests/test_calcola_importo.py -v`
Expected: FAIL su `test_tariffa_solo_al_minuto` e `test_tariffa_solo_al_km` con `TypeError: unsupported operand type(s) ... NoneType` (la riga 73 attuale moltiplica direttamente per `row.costo_al_km`/`row.costo_al_minuto` anche quando sono `None`).

- [ ] **Step 3: Aggiornare `calcola_importo`**

In `backend/bll/servizio_pricing.py`, sostituisci le righe 63-73:

```python
    def calcola_importo(self, tipo_mezzo: str, durata_min: float, distanza_km: float) -> Decimal:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT costo_al_minuto, costo_al_km FROM tariffe WHERE tipo_mezzo = :tipo"
                ),
                {"tipo": tipo_mezzo},
            ).fetchone()
        if not row:
            raise TariffaNonTrovata(f"Nessuna tariffa per {tipo_mezzo}")
        costo_al_minuto = row.costo_al_minuto if row.costo_al_minuto is not None else Decimal("0")
        costo_al_km = row.costo_al_km if row.costo_al_km is not None else Decimal("0")
        return Decimal(str(durata_min)) * costo_al_minuto + Decimal(str(distanza_km)) * costo_al_km
```

- [ ] **Step 4: Eseguire i test per verificare che passino**

Run: `cd backend && uv run pytest tests/test_calcola_importo.py -v`
Expected: PASS (3 test).

- [ ] **Step 5: Eseguire l'intera suite unitaria di pagamenti per la non-regressione**

Run: `cd backend && uv run pytest tests/test_pagamenti.py -v -m "not integration"`
Expected: PASS (questi test mockano `calcola_importo`, quindi non sono affetti dal cambio interno).

- [ ] **Step 6: Commit**

```bash
git add backend/bll/servizio_pricing.py backend/tests/test_calcola_importo.py
git commit -m "fix(pricing): calcola_importo gestisce costo_al_minuto/costo_al_km nullo"
```

---

### Task 6: Aggiornare i test di integrazione HTTP esistenti al nuovo payload

**Files:**
- Modify: `backend/tests/test_tariffa_http.py`

**Interfaces:**
- Consumes: endpoint `POST /operatore/tariffe`, `PUT /operatore/tariffe/{tipo_mezzo}` con `CreaTariffaRequest` da Task 2 (rifiuta payload con entrambi i costi popolati).

- [ ] **Step 1: Aggiornare i payload dei test esistenti**

In `backend/tests/test_tariffa_http.py`, sostituisci ogni occorrenza di payload/insert con entrambi i costi popolati con un solo campo. Sostituisci l'intero file con:

```python
import pytest
import uuid as _uuid
import httpx
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8000"


def _login_op(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _elimina_tariffa(db, tipo_mezzo: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM tariffe WHERE tipo_mezzo = :t"), {"t": tipo_mezzo})
        s.commit()


# [IF-OP.07] Definisce Tariffa / [IF-OP.08] Modifica Tariffa
class TestTariffaHTTP:

    @pytest.mark.integration
    def test_get_tariffe_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/tariffe", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @pytest.mark.integration
    def test_post_tariffa_201_costo_al_minuto(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["tipo_mezzo"] == tipo_mezzo
            assert r.json()["costo_al_km"] is None
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_201_costo_al_km(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": None, "costo_al_km": 0.10},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["costo_al_minuto"] is None
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_422_entrambi_i_costi(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": 0.10},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 422
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_409_duplicata(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "bicicletta"
        _elimina_tariffa(db, tipo_mezzo)
        with Session(db) as s:
            s.execute(
                text(
                    "INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) "
                    "VALUES (:t, 0.05, NULL)"
                ),
                {"t": tipo_mezzo},
            )
            s.commit()
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_put_tariffa_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "monopattino"
        _elimina_tariffa(db, tipo_mezzo)
        with Session(db) as s:
            s.execute(
                text(
                    "INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) "
                    "VALUES (:t, 0.05, NULL)"
                ),
                {"t": tipo_mezzo},
            )
            s.commit()
        try:
            r = httpx.put(
                f"{BASE}/operatore/tariffe/{tipo_mezzo}",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.07, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            assert Decimal(str(r.json()["costo_al_minuto"])) == Decimal("0.07")
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_put_tariffa_404_inesistente(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = f"inesistente-{_uuid.uuid4().hex[:6]}"
        r = httpx.put(
            f"{BASE}/operatore/tariffe/{tipo_mezzo}",
            json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.07, "costo_al_km": None},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404
```

- [ ] **Step 2: Eseguire i test di integrazione (richiede backend avviato e `DATABASE_URL` configurato)**

Run:
```bash
cd backend && uv run uvicorn main:app --reload &
uv run pytest tests/test_tariffa_http.py -v -m integration
```
Expected: PASS (8 test). Se il backend non è già avviato in un altro terminale, avvialo prima di lanciare i test (questi test fanno richieste HTTP reali a `localhost:8000`).

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_tariffa_http.py
git commit -m "test(tariffa): aggiorna i test HTTP al payload costo_al_minuto XOR costo_al_km"
```

---

### Task 7: `TariffaService.ts` — nuova firma con tipo di costo

**Files:**
- Modify: `frontend/src/services/TariffaService.ts`

**Interfaces:**
- Produces: `Tariffa { id, tipo_mezzo, costo_al_minuto: number | null, costo_al_km: number | null }`, `creaTariffa(tipoMezzo: string, tipoCosto: 'minuto' | 'km', valore: number): Promise<{ data: Tariffa }>`, `aggiornaTariffa(tipoMezzo: string, tipoCosto: 'minuto' | 'km', valore: number): Promise<{ data: Tariffa }>`. Usati da Task 8.

- [ ] **Step 1: Sostituire il file**

```typescript
import { api } from './ApiService'

export type TipoCostoTariffa = 'minuto' | 'km'

export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number | null
  costo_al_km: number | null
}

function buildPayload(tipo_mezzo: string, tipoCosto: TipoCostoTariffa, valore: number) {
  return {
    tipo_mezzo,
    costo_al_minuto: tipoCosto === 'minuto' ? valore : null,
    costo_al_km: tipoCosto === 'km' ? valore : null,
  }
}

// [IF-OP.07] Definisce Tariffa
export const getTariffe = (): Promise<{ data: Tariffa[] }> =>
  api.get('/operatore/tariffe')

export const creaTariffa = (
  tipo_mezzo: string,
  tipoCosto: TipoCostoTariffa,
  valore: number,
): Promise<{ data: Tariffa }> =>
  api.post('/operatore/tariffe', buildPayload(tipo_mezzo, tipoCosto, valore))

// [IF-OP.08] Modifica Tariffa
export const aggiornaTariffa = (
  tipo_mezzo: string,
  tipoCosto: TipoCostoTariffa,
  valore: number,
): Promise<{ data: Tariffa }> =>
  api.put(`/operatore/tariffe/${tipo_mezzo}`, buildPayload(tipo_mezzo, tipoCosto, valore))
```

- [ ] **Step 2: Verificare la compilazione TypeScript**

Run: `cd frontend && npx tsc --noEmit`
Expected: errori riportati in `VistaTariffe.tsx` (firma cambiata) — confermati e risolti nel Task 8. Nessun errore in `TariffaService.ts` stesso.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/TariffaService.ts
git commit -m "feat(tariffa-fe): TariffaService usa tipo di costo + valore singolo"
```

---

### Task 8: `VistaTariffe.tsx` — form con scelta minuto/km e validazione duplicato inline

**Files:**
- Modify: `frontend/src/views/operatore/VistaTariffe.tsx`
- Modify: `frontend/src/views/operatore/VistaTariffe.css`

**Interfaces:**
- Consumes: `creaTariffa(tipoMezzo, tipoCosto, valore)`, `aggiornaTariffa(tipoMezzo, tipoCosto, valore)`, `Tariffa { costo_al_minuto: number | null, costo_al_km: number | null }` da Task 7.

- [ ] **Step 1: Sostituire `VistaTariffe.tsx`**

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { getTariffe, creaTariffa, aggiornaTariffa, type Tariffa, type TipoCostoTariffa } from '../../services/TariffaService'
import './VistaTariffe.css'

const TIPI_MEZZO = ['monopattino', 'bicicletta', 'automobile'] as const

const TIPO_LABEL: Record<string, string> = {
  monopattino: 'Monopattino',
  bicicletta: 'Bicicletta',
  automobile: 'Automobile',
}

interface FormState {
  tipo_mezzo: string
  tipo_costo: TipoCostoTariffa
  valore: string
}

const FORM_VUOTO: FormState = {
  tipo_mezzo: TIPI_MEZZO[0],
  tipo_costo: 'minuto',
  valore: '',
}

function tariffaToForm(t: Tariffa): FormState {
  const tipo_costo: TipoCostoTariffa = t.costo_al_minuto !== null ? 'minuto' : 'km'
  const valore = tipo_costo === 'minuto' ? t.costo_al_minuto : t.costo_al_km
  return {
    tipo_mezzo: t.tipo_mezzo,
    tipo_costo,
    valore: valore !== null && valore !== undefined ? String(valore) : '',
  }
}

// [IF-OP.07] Definisce Tariffa / [IF-OP.08] Modifica Tariffa
export default function VistaTariffe() {
  const navigate = useNavigate()
  const [tariffe, setTariffe] = useState<Tariffa[]>([])
  const [mostraModal, setMostraModal] = useState(false)
  const [tariffaInModifica, setTariffaInModifica] = useState<Tariffa | null>(null)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricarica = useCallback(() => {
    getTariffe().then(r => setTariffe(r.data)).catch(() => {})
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriNuova = () => {
    setTariffaInModifica(null)
    setForm(FORM_VUOTO)
    setErrore('')
    setMostraModal(true)
  }

  const apriModifica = (t: Tariffa) => {
    setTariffaInModifica(t)
    setForm(tariffaToForm(t))
    setErrore('')
    setMostraModal(true)
  }

  const chiudiModal = () => {
    setMostraModal(false)
    setTariffaInModifica(null)
    setErrore('')
  }

  // [OP-05.1] tipo mezzo già tariffato: blocca la creazione e invita a modificare
  const tipoGiaEsistente =
    !tariffaInModifica && tariffe.some(t => t.tipo_mezzo === form.tipo_mezzo)

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    const valore = parseFloat(form.valore)
    try {
      if (tariffaInModifica) {
        await aggiornaTariffa(tariffaInModifica.tipo_mezzo, form.tipo_costo, valore)
      } else {
        await creaTariffa(form.tipo_mezzo, form.tipo_costo, valore)
      }
      chiudiModal()
      ricarica()
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const status = err.response?.status
        if (status === 409) setErrore('Tariffa già esistente per questa tipologia. Usa Modifica Tariffa.')
        else if (status === 404) setErrore('Tariffa non trovata.')
        else if (status === 422) setErrore('Dati non validi. Controlla i campi.')
        else setErrore('Errore durante il salvataggio. Riprova.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const datiValidi =
    !!form.tipo_mezzo &&
    !tipoGiaEsistente &&
    form.valore !== '' && parseFloat(form.valore) > 0

  const setTipoMezzo = (e: React.ChangeEvent<HTMLSelectElement>) =>
    setForm(prev => ({ ...prev, tipo_mezzo: e.target.value }))

  const setTipoCosto = (tipo_costo: TipoCostoTariffa) =>
    setForm(prev => ({ ...prev, tipo_costo }))

  const setValore = (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm(prev => ({ ...prev, valore: e.target.value }))

  return (
    <div className="vista-tariffe">
      <div className="tariffe-topbar">
        <h2>Tariffe</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="tariffe-body">
        <div className="tariffe-header-row">
          <h3>Tariffe per tipologia di mezzo</h3>
          <button className="btn-nuova-tariffa" onClick={apriNuova}>
            + Nuova tariffa
          </button>
        </div>

        <div className="tariffe-lista">
          {tariffe.length === 0 ? (
            <div className="tariffe-vuote">Nessuna tariffa definita. Crea la prima!</div>
          ) : (
            tariffe.map(t => (
              <div className="tariffa-card" key={t.id}>
                <div className="tariffa-tipo-badge">{TIPO_LABEL[t.tipo_mezzo] ?? t.tipo_mezzo}</div>
                <div className="tariffa-info">
                  <div className="tariffa-nome">{TIPO_LABEL[t.tipo_mezzo] ?? t.tipo_mezzo}</div>
                  <div className="tariffa-dettaglio">
                    {t.costo_al_minuto !== null ? `€${t.costo_al_minuto}/min` : `€${t.costo_al_km}/km`}
                  </div>
                </div>
                <button className="btn-modifica-tariffa" onClick={() => apriModifica(t)} title="Modifica">✏️</button>
              </div>
            ))
          )}
        </div>
      </div>

      {mostraModal && (
        <div className="modal-overlay-tariffa" onClick={chiudiModal}>
          <div className="modal-tariffa" onClick={e => e.stopPropagation()}>
            <h3>{tariffaInModifica ? 'Modifica tariffa' : 'Nuova tariffa'}</h3>

            <label>
              Tipologia mezzo *
              {tariffaInModifica ? (
                <input value={TIPO_LABEL[form.tipo_mezzo] ?? form.tipo_mezzo} disabled />
              ) : (
                <select value={form.tipo_mezzo} onChange={setTipoMezzo}>
                  {TIPI_MEZZO.map(t => (
                    <option key={t} value={t}>{TIPO_LABEL[t]}</option>
                  ))}
                </select>
              )}
            </label>

            {tipoGiaEsistente && (
              <p className="modal-errore-tariffa">
                Tariffa già esistente per questa tipologia. Usa Modifica Tariffa.
              </p>
            )}

            <label>
              Tipo di tariffa *
              <div className="tariffa-tipo-costo-radios">
                <label className="tariffa-radio">
                  <input
                    type="radio"
                    name="tipo_costo"
                    checked={form.tipo_costo === 'minuto'}
                    onChange={() => setTipoCosto('minuto')}
                  />
                  Costo al minuto
                </label>
                <label className="tariffa-radio">
                  <input
                    type="radio"
                    name="tipo_costo"
                    checked={form.tipo_costo === 'km'}
                    onChange={() => setTipoCosto('km')}
                  />
                  Costo al chilometro
                </label>
              </div>
            </label>

            <label>
              {form.tipo_costo === 'minuto' ? 'Costo al minuto (€) *' : 'Costo al km (€) *'}
              <input
                type="number"
                min="0"
                step="0.01"
                value={form.valore}
                onChange={setValore}
                placeholder={form.tipo_costo === 'minuto' ? 'es. 0.15' : 'es. 0.20'}
              />
            </label>

            {errore && <p className="modal-errore-tariffa">{errore}</p>}

            <div className="modal-azioni-tariffa">
              <button className="btn-annulla-tariffa" onClick={chiudiModal}>Annulla</button>
              <button className="btn-conferma-tariffa" onClick={handleConferma} disabled={caricamento || !datiValidi}>
                {caricamento ? '...' : tariffaInModifica ? 'Salva modifiche' : 'Salva tariffa'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Aggiungere lo stile per i radio button**

In `frontend/src/views/operatore/VistaTariffe.css`, dopo la regola `.modal-tariffa label { ... }` (riga 152-159), aggiungi:

```css
.tariffa-tipo-costo-radios {
  display: flex;
  gap: 16px;
  flex-direction: row !important;
}

.tariffa-radio {
  display: flex !important;
  flex-direction: row !important;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
}

.tariffa-radio input[type="radio"] {
  width: auto;
  padding: 0;
  cursor: pointer;
}
```

- [ ] **Step 3: Verificare la build TypeScript**

Run: `cd frontend && npx tsc --noEmit`
Expected: nessun errore.

- [ ] **Step 4: Avviare l'app e verificare manualmente il flusso**

Run: `cd backend && uv run uvicorn main:app --reload` (terminale 1), `cd frontend && npm run dev` (terminale 2). Apri `http://localhost:5173`, accedi come operatore, vai su Tariffe.

Verifica manualmente:
1. Click su "+ Nuova tariffa" → si apre sempre (anche se tutti i tipi hanno già una tariffa).
2. Seleziona un tipo mezzo già tariffato (es. monopattino, se presente) → appare il messaggio "Tariffa già esistente..." e "Salva tariffa" è disabilitato.
3. Seleziona un tipo mezzo libero, scegli "Costo al chilometro", inserisci un valore > 0 → "Salva tariffa" si abilita, il salvataggio crea la tariffa con solo `costo_al_km` popolato.
4. Apri "Modifica" su una tariffa esistente → il radio precompilato corrisponde al tipo di costo già impostato, il valore è precompilato; cambiare radio e valore e salvare aggiorna correttamente.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/operatore/VistaTariffe.tsx frontend/src/views/operatore/VistaTariffe.css
git commit -m "feat(tariffa-fe): scelta minuto/km nel form e validazione duplicato inline"
```

---

### Task 9: Documentazione sprint

**Files:**
- Modify: `docs/Sprintn3.md` (sezione caso d'uso OP-05, se presente con riferimenti a "costo al minuto e al km" come campi sempre entrambi obbligatori)

**Interfaces:** nessuna — solo documentazione.

- [ ] **Step 1: Cercare i riferimenti a OP-05 in Sprintn3.md**

Run: `grep -n "OP-05" docs/Sprintn3.md`

- [ ] **Step 2: Aggiornare la nota di implementazione**

Se la sezione OP-05 in `docs/Sprintn3.md` descrive il form con entrambi i costi sempre richiesti, aggiorna il testo per riflettere la scelta minuto/km esclusiva e il comportamento "tipo mezzo sempre selezionabile + errore inline se già tariffato" implementati in questo piano. Se la sezione è già coerente con questo comportamento, non modificare nulla.

- [ ] **Step 3: Commit (solo se è stata fatta una modifica)**

```bash
git add docs/Sprintn3.md
git commit -m "docs(sprint): aggiorna nota implementativa OP-05 Definisce Tariffa"
```
