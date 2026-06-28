# Pagamenti Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare IF-UT.12, IF-UT.20, IF-UT.21 — CRUD metodi di pagamento e pagamento a fine corsa.

**Architecture:** Provider stub (valida + autorizza) → DAL (PagamentoRepository) → BLL (ServizioPricing) → Controller REST sotto `/utente/pagamenti`. CorsaRepository non viene toccato — l'aggiornamento stato corsa è in `feature/corsa`.

**Tech Stack:** FastAPI, SQLAlchemy 2.0 (raw SQL con `text()`), Pydantic, pytest + unittest.mock

---

## File Map

| File | Azione |
|------|--------|
| `backend/providers/__init__.py` | nuovo (vuoto) |
| `backend/providers/provider_pagamenti.py` | nuovo — stub con `valida_dati_pagamento` e `autorizza` |
| `backend/dal/pagamento_repository.py` | riempire |
| `backend/bll/servizio_pricing.py` | riempire |
| `backend/controllers/schemas.py` | estendere |
| `backend/controllers/pagamenti_controller.py` | riempire |
| `backend/main.py` | aggiungere import e `include_router` |
| `backend/tests/test_pagamenti.py` | nuovo — 10 test unit |

---

## Task 1: ProviderPagamentiStub

**Files:**
- Create: `backend/providers/__init__.py`
- Create: `backend/providers/provider_pagamenti.py`
- Create: `backend/tests/test_pagamenti.py`

- [ ] **Step 1: Scrivi i test del provider**

Crea `backend/tests/test_pagamenti.py`:

```python
from decimal import Decimal
from providers.provider_pagamenti import ProviderPagamentiStub, RispostaPagamento, DatiNonValidiException


def test_provider_autorizza_ok():
    provider = ProviderPagamentiStub(deve_fallire=False)
    risposta = provider.autorizza("tok-abc", Decimal("5.00"))
    assert risposta.autorizzato is True
    assert risposta.transazione_id != ""


def test_provider_rifiuta():
    provider = ProviderPagamentiStub(deve_fallire=True)
    risposta = provider.autorizza("tok-abc", Decimal("5.00"))
    assert risposta.autorizzato is False
    assert risposta.transazione_id == ""


def test_provider_valida_dati_ok():
    provider = ProviderPagamentiStub(deve_fallire=False)
    token = provider.valida_dati_pagamento("carta", {"last_four": "1234"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_provider_valida_dati_non_validi():
    provider = ProviderPagamentiStub(deve_fallire=True)
    import pytest
    with pytest.raises(DatiNonValidiException):
        provider.valida_dati_pagamento("carta", {"last_four": "9999"})
```

- [ ] **Step 2: Esegui per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v
```
Atteso: `ModuleNotFoundError: No module named 'providers'`

- [ ] **Step 3: Crea i file**

`backend/providers/__init__.py` — vuoto.

`backend/providers/provider_pagamenti.py`:

```python
import uuid
from dataclasses import dataclass
from decimal import Decimal


class DatiNonValidiException(Exception):
    pass


@dataclass
class RispostaPagamento:
    autorizzato: bool
    transazione_id: str


class ProviderPagamentiStub:

    def __init__(self, deve_fallire: bool = False):
        self.deve_fallire = deve_fallire

    def valida_dati_pagamento(self, tipo: str, dati: dict) -> str:
        """Valida i dati del metodo e restituisce un token. CS-13 passo 15-16."""
        if self.deve_fallire:
            raise DatiNonValidiException("Dati di pagamento non validi")
        return f"{tipo}-{uuid.uuid4()}"

    def autorizza(self, token_metodo: str, importo: Decimal) -> RispostaPagamento:
        """Autorizza un addebito. CS-12 passo 9-10."""
        if self.deve_fallire:
            return RispostaPagamento(autorizzato=False, transazione_id="")
        return RispostaPagamento(autorizzato=True, transazione_id=str(uuid.uuid4()))
```

- [ ] **Step 4: Esegui per verificare che passi**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v
```
Atteso: `4 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/providers/__init__.py backend/providers/provider_pagamenti.py backend/tests/test_pagamenti.py
git commit -m "feat(pagamenti): ProviderPagamentiStub con valida_dati_pagamento e autorizza"
```

---

## Task 2: Schemi Pydantic

**Files:**
- Modify: `backend/controllers/schemas.py`

- [ ] **Step 1: Aggiungi i nuovi schemi in fondo a schemas.py**

```python
class AggiungiMetodoRequest(BaseModel):
    tipo: str
    last_four: str | None = None


class EffettuaPagamentoRequest(BaseModel):
    corsa_id: str
    tipo_mezzo: str
    durata_min: float
    distanza_km: float


class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool
```

- [ ] **Step 2: Verifica importabilità**

```bash
cd backend && uv run python -c "from controllers.schemas import AggiungiMetodoRequest, EffettuaPagamentoRequest, MetodoPagamentoResponse; print('ok')"
```
Atteso: `ok`

- [ ] **Step 3: Commit**

```bash
git add backend/controllers/schemas.py
git commit -m "feat(pagamenti): schemi Pydantic AggiungiMetodoRequest, EffettuaPagamentoRequest, MetodoPagamentoResponse"
```

---

## Task 3: PagamentoRepository

**Files:**
- Modify: `backend/dal/pagamento_repository.py`

Stesso pattern di `AttoreRepository`: raw SQL con `text()`, `Session(engine)` aperta e chiusa per metodo.

- [ ] **Step 1: Implementa il repository**

`backend/dal/pagamento_repository.py`:

```python
import uuid
from uuid import UUID
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.pagamento import MetodoPagamento, Pagamento, TipoMetodoPagamento, StatoPagamento


class MetodoNonTrovatoException(Exception):
    pass


class PagamentoRepository:

    def aggiungi_metodo(
        self,
        utente_id: UUID,
        tipo: TipoMetodoPagamento,
        token_esterno: str,
        last_four: str | None,
    ) -> MetodoPagamento:
        with Session(engine) as session:
            count = session.execute(
                text("SELECT COUNT(*) FROM metodi_pagamento WHERE utente_id = :uid"),
                {"uid": str(utente_id)},
            ).scalar()
            predefinito = int(count) == 0
            metodo_id = uuid.uuid4()
            session.execute(
                text(
                    "INSERT INTO metodi_pagamento "
                    "(id, utente_id, tipo, token_esterno, last_four, predefinito) "
                    "VALUES (:id, :uid, :tipo, :token, :lf, :pred)"
                ),
                {
                    "id": str(metodo_id),
                    "uid": str(utente_id),
                    "tipo": tipo.value,
                    "token": token_esterno,
                    "lf": last_four,
                    "pred": predefinito,
                },
            )
            session.commit()
        m = MetodoPagamento()
        m.id = metodo_id
        m.utente_id = utente_id
        m.tipo = tipo
        m.token_esterno = token_esterno
        m.last_four = last_four
        m.predefinito = predefinito
        return m

    def lista_metodi(self, utente_id: UUID) -> list[MetodoPagamento]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, tipo, token_esterno, last_four, predefinito "
                    "FROM metodi_pagamento WHERE utente_id = :uid ORDER BY created_at"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
        result = []
        for row in rows:
            m = MetodoPagamento()
            m.id = UUID(str(row.id))
            m.utente_id = utente_id
            m.tipo = TipoMetodoPagamento(row.tipo)
            m.token_esterno = row.token_esterno
            m.last_four = row.last_four
            m.predefinito = row.predefinito
            result.append(m)
        return result

    def trova_metodo(self, metodo_id: UUID, utente_id: UUID) -> MetodoPagamento:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT id, tipo, token_esterno, last_four, predefinito "
                    "FROM metodi_pagamento WHERE id = :id AND utente_id = :uid"
                ),
                {"id": str(metodo_id), "uid": str(utente_id)},
            ).fetchone()
        if not row:
            raise MetodoNonTrovatoException(f"Metodo {metodo_id} non trovato")
        m = MetodoPagamento()
        m.id = UUID(str(row.id))
        m.utente_id = utente_id
        m.tipo = TipoMetodoPagamento(row.tipo)
        m.token_esterno = row.token_esterno
        m.last_four = row.last_four
        m.predefinito = row.predefinito
        return m

    def exists_by_token(self, token_esterno: str) -> bool:
        with Session(engine) as session:
            row = session.execute(
                text("SELECT 1 FROM metodi_pagamento WHERE token_esterno = :token"),
                {"token": token_esterno},
            ).fetchone()
        return row is not None

    def imposta_predefinito(self, metodo_id: UUID, utente_id: UUID) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "UPDATE metodi_pagamento SET predefinito = false WHERE utente_id = :uid"
                ),
                {"uid": str(utente_id)},
            )
            session.execute(
                text(
                    "UPDATE metodi_pagamento SET predefinito = true "
                    "WHERE id = :id AND utente_id = :uid"
                ),
                {"id": str(metodo_id), "uid": str(utente_id)},
            )
            session.commit()

    def rimuovi_metodo(self, metodo_id: UUID, utente_id: UUID) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "DELETE FROM metodi_pagamento WHERE id = :id AND utente_id = :uid"
                ),
                {"id": str(metodo_id), "uid": str(utente_id)},
            )
            session.commit()

    def trova_predefinito(self, utente_id: UUID) -> MetodoPagamento | None:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT id, tipo, token_esterno, last_four "
                    "FROM metodi_pagamento WHERE utente_id = :uid AND predefinito = true"
                ),
                {"uid": str(utente_id)},
            ).fetchone()
        if not row:
            return None
        m = MetodoPagamento()
        m.id = UUID(str(row.id))
        m.utente_id = utente_id
        m.tipo = TipoMetodoPagamento(row.tipo)
        m.token_esterno = row.token_esterno
        m.last_four = row.last_four
        m.predefinito = True
        return m

    def crea_pagamento(
        self,
        corsa_id: UUID,
        utente_id: UUID,
        metodo_id: UUID | None,
        importo: Decimal,
        stato: StatoPagamento,
    ) -> Pagamento:
        with Session(engine) as session:
            pagamento_id = uuid.uuid4()
            session.execute(
                text(
                    "INSERT INTO pagamenti "
                    "(id, corsa_id, utente_id, metodo_pagamento_id, importo, stato) "
                    "VALUES (:id, :corsa_id, :uid, :metodo_id, :importo, :stato)"
                ),
                {
                    "id": str(pagamento_id),
                    "corsa_id": str(corsa_id),
                    "uid": str(utente_id),
                    "metodo_id": str(metodo_id) if metodo_id else None,
                    "importo": str(importo),
                    "stato": stato.value,
                },
            )
            session.commit()
        p = Pagamento()
        p.id = pagamento_id
        p.corsa_id = corsa_id
        p.utente_id = utente_id
        p.metodo_pagamento_id = metodo_id
        p.importo = importo
        p.stato = stato
        return p
```

- [ ] **Step 2: Verifica importabilità**

```bash
cd backend && uv run python -c "from dal.pagamento_repository import PagamentoRepository; print('ok')"
```
Atteso: `ok`

- [ ] **Step 3: Commit**

```bash
git add backend/dal/pagamento_repository.py
git commit -m "feat(pagamenti): PagamentoRepository — CRUD metodi e crea_pagamento [IF-UT.12, IF-UT.20]"
```

---

## Task 4: ServizioPricing + test unit

**Files:**
- Modify: `backend/bll/servizio_pricing.py`
- Modify: `backend/tests/test_pagamenti.py`

- [ ] **Step 1: Aggiungi i test in fondo a test_pagamenti.py**

```python
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest

from bll.servizio_pricing import (
    ServizioPricing,
    MetodoDuplicato,
    MetodoNonTrovato,
    DatiNonValidi,
    NessunMetodoPredefinito,
    PagamentoRifiutato,
)
from dal.pagamento_repository import MetodoNonTrovatoException
from model.pagamento import MetodoPagamento, TipoMetodoPagamento, Pagamento, StatoPagamento

UTENTE_ID = uuid4()
CORSA_ID = uuid4()
METODO_ID = uuid4()


def _metodo_fake(predefinito=False, last_four="1234"):
    m = MagicMock(spec=MetodoPagamento)
    m.id = METODO_ID
    m.utente_id = UTENTE_ID
    m.tipo = TipoMetodoPagamento.carta
    m.token_esterno = "carta-tok-fake"
    m.last_four = last_four
    m.predefinito = predefinito
    return m


def _pagamento_fake(stato=StatoPagamento.completato):
    p = MagicMock(spec=Pagamento)
    p.id = uuid4()
    p.stato = stato
    return p


def _servizio(deve_fallire=False):
    from providers.provider_pagamenti import ProviderPagamentiStub
    s = ServizioPricing(provider=ProviderPagamentiStub(deve_fallire=deve_fallire))
    s._repo = MagicMock()
    return s


# --- IF-UT.12: aggiungi metodo ---

def test_aggiungi_metodo_carta():
    """CS-13 scenario base — provider valida dati e restituisce token."""
    s = _servizio()
    s._repo.exists_by_token.return_value = False
    s._repo.aggiungi_metodo.return_value = _metodo_fake(predefinito=True, last_four="4242")

    result = s.aggiungi_metodo(UTENTE_ID, "carta", {"last_four": "4242"})

    assert result["tipo"] == "carta"
    assert result["last_four"] == "4242"
    s._repo.exists_by_token.assert_called_once()
    s._repo.aggiungi_metodo.assert_called_once()


def test_aggiungi_metodo_duplicato():
    """CS-13 — token già presente → MetodoDuplicato."""
    s = _servizio()
    s._repo.exists_by_token.return_value = True

    with pytest.raises(MetodoDuplicato):
        s.aggiungi_metodo(UTENTE_ID, "paypal", {})


def test_dati_non_validi():
    """CS-13 — provider rifiuta i dati → DatiNonValidi."""
    s = _servizio(deve_fallire=True)

    with pytest.raises(DatiNonValidi):
        s.aggiungi_metodo(UTENTE_ID, "carta", {"last_four": "0000"})


def test_primo_metodo_diventa_predefinito():
    """CS-13 passo 9 — il DAL imposta predefinito=True se primo metodo."""
    s = _servizio()
    s._repo.exists_by_token.return_value = False
    s._repo.aggiungi_metodo.return_value = _metodo_fake(predefinito=True)

    result = s.aggiungi_metodo(UTENTE_ID, "carta", {"last_four": "1234"})

    assert result["predefinito"] is True


# --- IF-UT.21: imposta predefinito ---

def test_imposta_predefinito():
    """IF-UT.21 scenario base."""
    s = _servizio()
    s._repo.trova_metodo.return_value = _metodo_fake(predefinito=False)

    result = s.imposta_predefinito(METODO_ID, UTENTE_ID)

    s._repo.imposta_predefinito.assert_called_once_with(METODO_ID, UTENTE_ID)
    assert result["predefinito"] is True


# --- IF-UT.20: effettua pagamento ---

def test_effettua_pagamento_ok():
    """CS-12 scenario base — provider autorizza."""
    s = _servizio(deve_fallire=False)
    s._repo.trova_predefinito.return_value = _metodo_fake(predefinito=True)
    s._repo.crea_pagamento.return_value = _pagamento_fake(StatoPagamento.completato)

    with patch.object(s, "calcola_importo", return_value=Decimal("3.50")):
        result = s.effettua_pagamento(CORSA_ID, UTENTE_ID, "bicicletta", 10.0, 2.5)

    assert result["stato"] == "completato"
    assert result["importo"] == 3.50


def test_pagamento_rifiutato():
    """CS-12.1 — provider rifiuta → PagamentoRifiutato, record salvato con stato rifiutato."""
    s = _servizio(deve_fallire=True)
    s._repo.trova_predefinito.return_value = _metodo_fake(predefinito=True)
    s._repo.crea_pagamento.return_value = _pagamento_fake(StatoPagamento.rifiutato)

    with patch.object(s, "calcola_importo", return_value=Decimal("3.50")):
        with pytest.raises(PagamentoRifiutato):
            s.effettua_pagamento(CORSA_ID, UTENTE_ID, "bicicletta", 10.0, 2.5)

    _, kwargs = s._repo.crea_pagamento.call_args
    assert kwargs["stato"] == StatoPagamento.rifiutato


def test_pagamento_senza_metodo_predefinito():
    """CS-12 — utente senza metodo predefinito → NessunMetodoPredefinito."""
    s = _servizio()
    s._repo.trova_predefinito.return_value = None

    with patch.object(s, "calcola_importo", return_value=Decimal("3.50")):
        with pytest.raises(NessunMetodoPredefinito):
            s.effettua_pagamento(CORSA_ID, UTENTE_ID, "bicicletta", 10.0, 2.5)
```

- [ ] **Step 2: Esegui per verificare che i nuovi test falliscano**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v -k "not test_provider"
```
Atteso: `ImportError` su `bll.servizio_pricing`

- [ ] **Step 3: Implementa ServizioPricing**

`backend/bll/servizio_pricing.py`:

```python
from uuid import UUID
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.pagamento import TipoMetodoPagamento, StatoPagamento
from dal.pagamento_repository import PagamentoRepository, MetodoNonTrovatoException
from providers.provider_pagamenti import ProviderPagamentiStub, DatiNonValidiException


class MetodoNonTrovato(Exception):
    pass


class MetodoDuplicato(Exception):
    pass


class DatiNonValidi(Exception):
    pass


class NessunMetodoPredefinito(Exception):
    pass


class PagamentoRifiutato(Exception):
    pass


class TariffaNonTrovata(Exception):
    pass


class ServizioPricing:

    def __init__(self, provider=None):
        self._repo = PagamentoRepository()
        self._provider = provider or ProviderPagamentiStub()

    # [IF-UT.12] CS-13
    def aggiungi_metodo(self, utente_id: UUID, tipo: str, dati: dict) -> dict:
        try:
            tipo_enum = TipoMetodoPagamento(tipo)
        except ValueError:
            raise MetodoNonTrovato(f"Tipo metodo non valido: {tipo}")
        try:
            token = self._provider.valida_dati_pagamento(tipo, dati)
        except DatiNonValidiException as e:
            raise DatiNonValidi(str(e))
        if self._repo.exists_by_token(token):
            raise MetodoDuplicato("Metodo già associato all'account")
        last_four = dati.get("last_four") if tipo == "carta" else None
        metodo = self._repo.aggiungi_metodo(utente_id, tipo_enum, token, last_four)
        return self._serializza(metodo)

    # [IF-UT.12]
    def lista_metodi(self, utente_id: UUID) -> list[dict]:
        return [self._serializza(m) for m in self._repo.lista_metodi(utente_id)]

    # [IF-UT.21]
    def imposta_predefinito(self, metodo_id: UUID, utente_id: UUID) -> dict:
        try:
            metodo = self._repo.trova_metodo(metodo_id, utente_id)
        except MetodoNonTrovatoException:
            raise MetodoNonTrovato("Metodo non trovato")
        self._repo.imposta_predefinito(metodo_id, utente_id)
        metodo.predefinito = True
        return self._serializza(metodo)

    # [IF-UT.12]
    def rimuovi_metodo(self, metodo_id: UUID, utente_id: UUID) -> None:
        try:
            self._repo.trova_metodo(metodo_id, utente_id)
        except MetodoNonTrovatoException:
            raise MetodoNonTrovato("Metodo non trovato")
        self._repo.rimuovi_metodo(metodo_id, utente_id)

    # [IF-UT.20]
    def calcola_importo(self, tipo_mezzo: str, durata_min: float, distanza_km: float) -> Decimal:
        with Session(engine) as session:
            row = session.execute(
                text("SELECT costo_al_minuto, costo_al_km FROM tariffe WHERE tipo_mezzo = :tipo"),
                {"tipo": tipo_mezzo},
            ).fetchone()
        if not row:
            raise TariffaNonTrovata(f"Nessuna tariffa per tipo mezzo: {tipo_mezzo}")
        return (
            Decimal(str(durata_min)) * row.costo_al_minuto
            + Decimal(str(distanza_km)) * row.costo_al_km
        )

    # [IF-UT.20] — punto di integrazione con feature/corsa
    def effettua_pagamento(
        self,
        corsa_id: UUID,
        utente_id: UUID,
        tipo_mezzo: str,
        durata_min: float,
        distanza_km: float,
    ) -> dict:
        importo = self.calcola_importo(tipo_mezzo, durata_min, distanza_km)
        metodo = self._repo.trova_predefinito(utente_id)
        if metodo is None:
            raise NessunMetodoPredefinito("Nessun metodo di pagamento predefinito")
        risposta = self._provider.autorizza(metodo.token_esterno, importo)
        if not risposta.autorizzato:
            self._repo.crea_pagamento(
                corsa_id=corsa_id,
                utente_id=utente_id,
                metodo_id=metodo.id,
                importo=importo,
                stato=StatoPagamento.rifiutato,
            )
            raise PagamentoRifiutato("Pagamento rifiutato dal provider")
        pagamento = self._repo.crea_pagamento(
            corsa_id=corsa_id,
            utente_id=utente_id,
            metodo_id=metodo.id,
            importo=importo,
            stato=StatoPagamento.completato,
        )
        return {
            "pagamento_id": str(pagamento.id),
            "importo": float(importo),
            "stato": "completato",
            "transazione_id": risposta.transazione_id,
        }

    def _serializza(self, metodo) -> dict:
        return {
            "id": str(metodo.id),
            "tipo": metodo.tipo.value,
            "last_four": metodo.last_four,
            "predefinito": metodo.predefinito,
        }
```

- [ ] **Step 4: Esegui tutti i test**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v
```
Atteso: `14 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_pricing.py backend/tests/test_pagamenti.py
git commit -m "feat(pagamenti): ServizioPricing + 10 test unit [IF-UT.12, IF-UT.20, IF-UT.21]"
```

---

## Task 5: Controller e registrazione router

**Files:**
- Modify: `backend/controllers/pagamenti_controller.py`
- Modify: `backend/main.py`

- [ ] **Step 1: Implementa il controller**

`backend/controllers/pagamenti_controller.py`:

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from middleware.auth_middleware import verify_token
from bll.servizio_pricing import (
    ServizioPricing,
    MetodoNonTrovato,
    MetodoDuplicato,
    DatiNonValidi,
    NessunMetodoPredefinito,
    PagamentoRifiutato,
)
from controllers.schemas import (
    AggiungiMetodoRequest,
    EffettuaPagamentoRequest,
    MetodoPagamentoResponse,
)

router = APIRouter(prefix="/utente/pagamenti", tags=["Pagamenti"])
_servizio = ServizioPricing()


@router.get("/metodi", response_model=list[MetodoPagamentoResponse])
def lista_metodi(utente: dict = Depends(verify_token(required_roles=["UT"]))):
    """[IF-UT.12] Lista metodi di pagamento dell'utente."""
    return _servizio.lista_metodi(utente["id"])


@router.post("/metodi", response_model=MetodoPagamentoResponse, status_code=201)
def aggiungi_metodo(
    body: AggiungiMetodoRequest,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    """[IF-UT.12] CS-13 — Aggiunge un metodo di pagamento."""
    dati = {"last_four": body.last_four} if body.last_four else {}
    try:
        return _servizio.aggiungi_metodo(utente["id"], body.tipo, dati)
    except MetodoDuplicato as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DatiNonValidi as e:
        raise HTTPException(status_code=422, detail=str(e))
    except MetodoNonTrovato as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/metodi/{metodo_id}/predefinito", response_model=MetodoPagamentoResponse)
def imposta_predefinito(
    metodo_id: UUID,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    """[IF-UT.21] Imposta un metodo come predefinito."""
    try:
        return _servizio.imposta_predefinito(metodo_id, utente["id"])
    except MetodoNonTrovato as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/metodi/{metodo_id}", status_code=204)
def rimuovi_metodo(
    metodo_id: UUID,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    """[IF-UT.12] Rimuove un metodo di pagamento."""
    try:
        _servizio.rimuovi_metodo(metodo_id, utente["id"])
    except MetodoNonTrovato as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", status_code=201)
def effettua_pagamento(
    body: EffettuaPagamentoRequest,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    """[IF-UT.20] CS-12 — Effettua il pagamento di una corsa."""
    try:
        return _servizio.effettua_pagamento(
            corsa_id=UUID(body.corsa_id),
            utente_id=utente["id"],
            tipo_mezzo=body.tipo_mezzo,
            durata_min=body.durata_min,
            distanza_km=body.distanza_km,
        )
    except NessunMetodoPredefinito as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PagamentoRifiutato as e:
        raise HTTPException(status_code=402, detail=str(e))
```

- [ ] **Step 2: Registra il router in main.py**

`backend/main.py`:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as utente_router
from controllers.pagamenti_controller import router as pagamenti_router

app = FastAPI(title="SmartMobility API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(utente_router)
app.include_router(pagamenti_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
```

- [ ] **Step 3: Verifica avvio e endpoint**

```bash
cd backend && uv run uvicorn main:app --reload
```

Apri [http://localhost:8000/docs](http://localhost:8000/docs) e verifica che esistano:
- `GET /utente/pagamenti/metodi`
- `POST /utente/pagamenti/metodi`
- `PUT /utente/pagamenti/metodi/{metodo_id}/predefinito`
- `DELETE /utente/pagamenti/metodi/{metodo_id}`
- `POST /utente/pagamenti`

- [ ] **Step 4: Esegui tutti i test per regressione**

```bash
cd backend && uv run pytest tests/ -v -m "not integration"
```
Atteso: tutti i test passano.

- [ ] **Step 5: Commit**

```bash
git add backend/controllers/pagamenti_controller.py backend/main.py
git commit -m "feat(pagamenti): controller REST /utente/pagamenti [IF-UT.12, IF-UT.20, IF-UT.21]"
```

---

## Task 6: Push e PR

- [ ] **Step 1: Push**

```bash
git push origin feature/pagamenti
```

- [ ] **Step 2: Apri la Pull Request**

Titolo: `[IF-UT.12, IF-UT.20, IF-UT.21] Backend pagamenti — metodi e ServizioPricing`

Descrizione:
- `ProviderPagamentiStub` configurabile OK/KO
- `PagamentoRepository` — CRUD metodi + crea_pagamento
- `ServizioPricing` — aggiungi/lista/imposta/rimuovi metodi + effettua_pagamento
- Endpoint: `GET/POST/PUT/DELETE /utente/pagamenti/metodi`, `POST /utente/pagamenti`
- Punto integrazione: `ServizioPricing.effettua_pagamento()` — chiamare da `ServizioMobilita.termina_corsa()` in `feature/corsa`
- 14 unit test, nessun DB richiesto