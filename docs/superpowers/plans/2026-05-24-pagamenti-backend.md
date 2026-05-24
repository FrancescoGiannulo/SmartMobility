# Pagamenti Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare IF-UT.12, IF-UT.20, IF-UT.21 — CRUD metodi di pagamento e pagamento a fine corsa.

**Architecture:** Layer Provider (stub OK/KO) → DAL (PagamentoRepository) → BLL (ServizioPricing) → Controller REST. ServizioPricing.effettua_pagamento() è il punto di integrazione con feature/corsa.

**Tech Stack:** FastAPI, SQLAlchemy 2.0 (raw SQL con text()), Pydantic, pytest + unittest.mock

---

## File Map

| File | Azione |
|------|--------|
| `backend/providers/__init__.py` | nuovo (vuoto) |
| `backend/providers/provider_pagamenti.py` | nuovo — stub OK/KO |
| `backend/dal/pagamento_repository.py` | riempire — CRUD metodi + crea_pagamento |
| `backend/bll/servizio_pricing.py` | riempire — logica metodi + calcola_importo + effettua_pagamento |
| `backend/controllers/schemas.py` | estendere — AggiungiMetodoRequest, MetodoPagamentoResponse |
| `backend/controllers/pagamenti_controller.py` | riempire — 4 endpoint |
| `backend/main.py` | modificare — registrare pagamenti_router |
| `backend/tests/test_pagamenti.py` | nuovo — 7 test unit |

---

## Task 1: ProviderPagamentiStub

**Files:**
- Create: `backend/providers/__init__.py`
- Create: `backend/providers/provider_pagamenti.py`
- Test: `backend/tests/test_pagamenti.py`

- [ ] **Step 1: Scrivi il test per il provider**

Crea `backend/tests/test_pagamenti.py`:

```python
from decimal import Decimal
from providers.provider_pagamenti import ProviderPagamentiStub, RispostaPagamento


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
```

- [ ] **Step 2: Esegui per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v
```
Atteso: `ModuleNotFoundError: No module named 'providers'`

- [ ] **Step 3: Crea i file del provider**

`backend/providers/__init__.py` — vuoto.

`backend/providers/provider_pagamenti.py`:

```python
import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RispostaPagamento:
    autorizzato: bool
    transazione_id: str


class ProviderPagamentiStub:

    def __init__(self, deve_fallire: bool = False):
        self.deve_fallire = deve_fallire

    def autorizza(self, token: str, importo: Decimal) -> RispostaPagamento:
        if self.deve_fallire:
            return RispostaPagamento(autorizzato=False, transazione_id="")
        return RispostaPagamento(autorizzato=True, transazione_id=str(uuid.uuid4()))
```

- [ ] **Step 4: Esegui per verificare che passi**

```bash
cd backend && uv run pytest tests/test_pagamenti.py -v
```
Atteso: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/providers/__init__.py backend/providers/provider_pagamenti.py backend/tests/test_pagamenti.py
git commit -m "feat(pagamenti): ProviderPagamentiStub configurabile OK/KO"
```

---

## Task 2: Schemi Pydantic

**Files:**
- Modify: `backend/controllers/schemas.py`

- [ ] **Step 1: Aggiungi i nuovi schemi**

Apri `backend/controllers/schemas.py` e aggiungi in fondo:

```python
class AggiungiMetodoRequest(BaseModel):
    tipo: str          # "google_pay" | "apple_pay" | "paypal" | "carta"
    last_four: str | None = None   # obbligatorio solo per tipo "carta"


class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool
```

- [ ] **Step 2: Verifica importabilità**

```bash
cd backend && uv run python -c "from controllers.schemas import AggiungiMetodoRequest, MetodoPagamentoResponse; print('ok')"
```
Atteso: `ok`

- [ ] **Step 3: Commit**

```bash
git add backend/controllers/schemas.py
git commit -m "feat(pagamenti): aggiungi schemi Pydantic metodi pagamento"
```

---

## Task 3: PagamentoRepository

**Files:**
- Modify: `backend/dal/pagamento_repository.py`

Il repository usa raw SQL con `text()` e `Session(engine)` — stesso pattern di `AttoreRepository`.

- [ ] **Step 1: Scrivi il file completo**

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
        self, utente_id: UUID, tipo: TipoMetodoPagamento, last_four: str | None
    ) -> MetodoPagamento:
        with Session(engine) as session:
            count = session.execute(
                text("SELECT COUNT(*) FROM metodi_pagamento WHERE utente_id = :uid"),
                {"uid": str(utente_id)},
            ).scalar()
            predefinito = int(count) == 0
            token = str(uuid.uuid4())
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
                    "token": token,
                    "lf": last_four,
                    "pred": predefinito,
                },
            )
            session.commit()
        m = MetodoPagamento()
        m.id = metodo_id
        m.utente_id = utente_id
        m.tipo = tipo
        m.token_esterno = token
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

    def metodo_gia_presente(
        self, utente_id: UUID, tipo: TipoMetodoPagamento, last_four: str | None
    ) -> bool:
        with Session(engine) as session:
            if last_four:
                row = session.execute(
                    text(
                        "SELECT 1 FROM metodi_pagamento "
                        "WHERE utente_id = :uid AND tipo = :tipo AND last_four = :lf"
                    ),
                    {"uid": str(utente_id), "tipo": tipo.value, "lf": last_four},
                ).fetchone()
            else:
                row = session.execute(
                    text(
                        "SELECT 1 FROM metodi_pagamento "
                        "WHERE utente_id = :uid AND tipo = :tipo"
                    ),
                    {"uid": str(utente_id), "tipo": tipo.value},
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

- [ ] **Step 2: Verifica importabilità (nessun DB richiesto)**

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

- [ ] **Step 1: Aggiungi i test unit a test_pagamenti.py**

Aggiungi in fondo a `backend/tests/test_pagamenti.py`:

```python
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest

from bll.servizio_pricing import (
    ServizioPricing,
    MetodoDuplicato,
    MetodoNonTrovato,
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
    m.token_esterno = "tok-fake"
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
    """CS-13 scenario base."""
    s = _servizio()
    s._repo.metodo_gia_presente.return_value = False
    s._repo.aggiungi_metodo.return_value = _metodo_fake(predefinito=True, last_four="4242")

    result = s.aggiungi_metodo(UTENTE_ID, "carta", "4242")

    assert result["tipo"] == "carta"
    assert result["last_four"] == "4242"
    s._repo.aggiungi_metodo.assert_called_once_with(UTENTE_ID, TipoMetodoPagamento.carta, "4242")


def test_aggiungi_metodo_duplicato():
    """CS-13 — metodo già presente → MetodoDuplicato."""
    s = _servizio()
    s._repo.metodo_gia_presente.return_value = True

    with pytest.raises(MetodoDuplicato):
        s.aggiungi_metodo(UTENTE_ID, "paypal", None)


def test_primo_metodo_diventa_predefinito():
    """CS-13 passo 9 — il DAL imposta predefinito=True se primo metodo."""
    s = _servizio()
    s._repo.metodo_gia_presente.return_value = False
    s._repo.aggiungi_metodo.return_value = _metodo_fake(predefinito=True)

    result = s.aggiungi_metodo(UTENTE_ID, "carta", "1234")

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
    """CS-12.1 — provider rifiuta → PagamentoRifiutato, stato rifiutato salvato nel DB."""
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
Atteso: `ImportError` o `ModuleNotFoundError` su `bll.servizio_pricing`

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
from providers.provider_pagamenti import ProviderPagamentiStub


class MetodoNonTrovato(Exception):
    pass


class MetodoDuplicato(Exception):
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
    def aggiungi_metodo(self, utente_id: UUID, tipo: str, last_four: str | None) -> dict:
        try:
            tipo_enum = TipoMetodoPagamento(tipo)
        except ValueError:
            raise MetodoNonTrovato(f"Tipo metodo non valido: {tipo}")
        if self._repo.metodo_gia_presente(utente_id, tipo_enum, last_four):
            raise MetodoDuplicato("Metodo già associato all'account")
        metodo = self._repo.aggiungi_metodo(utente_id, tipo_enum, last_four)
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

    # [IF-UT.20] — chiamato da ServizioMobilita.termina_corsa() in feature/corsa
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
Atteso: `9 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_pricing.py backend/tests/test_pagamenti.py
git commit -m "feat(pagamenti): ServizioPricing + test unit IF-UT.12, IF-UT.20, IF-UT.21"
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
from bll.servizio_pricing import ServizioPricing, MetodoNonTrovato, MetodoDuplicato
from controllers.schemas import AggiungiMetodoRequest, MetodoPagamentoResponse

router = APIRouter(prefix="/pagamenti", tags=["Pagamenti"])
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
    try:
        return _servizio.aggiungi_metodo(utente["id"], body.tipo, body.last_four)
    except MetodoDuplicato as e:
        raise HTTPException(status_code=409, detail=str(e))
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
```

- [ ] **Step 2: Registra il router in main.py**

Modifica `backend/main.py` aggiungendo:

```python
from controllers.pagamenti_controller import router as pagamenti_router
```

e nella sezione `include_router`:

```python
app.include_router(pagamenti_router)
```

Il file finale deve contenere:

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

- [ ] **Step 3: Verifica che il server si avvii e gli endpoint compaiano**

```bash
cd backend && uv run uvicorn main:app --reload
```

Apri [http://localhost:8000/docs](http://localhost:8000/docs) e verifica che esistano:
- `GET /pagamenti/metodi`
- `POST /pagamenti/metodi`
- `PUT /pagamenti/metodi/{metodo_id}/predefinito`
- `DELETE /pagamenti/metodi/{metodo_id}`

- [ ] **Step 4: Esegui tutti i test per regressione**

```bash
cd backend && uv run pytest tests/ -v -m "not integration"
```
Atteso: tutti i test passano.

- [ ] **Step 5: Commit**

```bash
git add backend/controllers/pagamenti_controller.py backend/main.py
git commit -m "feat(pagamenti): controller REST e registrazione router [IF-UT.12, IF-UT.21]"
```

---

## Task 6: Push e PR

- [ ] **Step 1: Push del branch**

```bash
git push origin feature/pagamenti
```

- [ ] **Step 2: Apri la Pull Request su GitHub**

Vai su [github.com/FrancescoGiannulo/SmartMobility](https://github.com/FrancescoGiannulo/SmartMobility), clicca **"Compare & pull request"** su `feature/pagamenti` e compila:

- **Titolo**: `[IF-UT.12, IF-UT.20, IF-UT.21] Backend pagamenti — metodi e ServizioPricing`
- **Descrizione**:
  - Implementati: PagamentoRepository, ServizioPricing, ProviderPagamentiStub, Controller REST
  - Punto di integrazione: `ServizioPricing.effettua_pagamento()` — da chiamare in `ServizioMobilita.termina_corsa()` (feature/corsa)
  - Test: 9 unit test, nessun DB richiesto
