# Design — Backend Pagamenti (feature/pagamenti)

**Data**: 2026-05-23 (aggiornato 2026-05-24)
**Item backlog**: IF-UT.12, IF-UT.20, IF-UT.21
**Branch**: `feature/pagamenti`
**Riferimenti**: `docs/Diagrammi/Diagramma di sequenza/sequence_salva_metodi_pagamento.drawio.xml`, `sequence_effettua_pagamento.drawio.xml`

---

## Scope

Implementazione del layer pagamenti lato backend. Non include CorsaRepository, MezzoRepository, ServizioGIS o ServizioMobilita — appartengono a `feature/corsa` e `feature/mappa-zone`. Il punto di integrazione con `feature/corsa` è `ServizioPricing.effettua_pagamento()`.

---

## File coinvolti

| File | Azione |
|------|--------|
| `backend/providers/provider_pagamenti.py` | nuovo |
| `backend/dal/pagamento_repository.py` | riempire |
| `backend/bll/servizio_pricing.py` | riempire |
| `backend/controllers/pagamenti_controller.py` | riempire |
| `backend/controllers/schemas.py` | estendere |
| `backend/tests/test_pagamenti.py` | nuovo |

---

## URL

Tutti gli endpoint vivono sotto `/utente/pagamenti` (come da diagramma di sequenza):

```
GET    /utente/pagamenti/metodi
POST   /utente/pagamenti/metodi
PUT    /utente/pagamenti/metodi/{id}/predefinito
DELETE /utente/pagamenti/metodi/{id}
POST   /utente/pagamenti
```

---

## Architettura

### Provider

`backend/providers/provider_pagamenti.py` — stub configurabile:

```python
class RispostaPagamento:
    autorizzato: bool
    transazione_id: str

class DatiNonValidiException(Exception): pass

class ProviderPagamentiStub:
    def __init__(self, deve_fallire: bool = False): ...

    def valida_dati_pagamento(self, tipo: str, dati: dict) -> str:
        # restituisce tokenMetodo; se deve_fallire → DatiNonValidiException

    def autorizza(self, token_metodo: str, importo: Decimal) -> RispostaPagamento:
        # se deve_fallire → RispostaPagamento(autorizzato=False)
```

`deve_fallire=True` simula entrambi i casi di errore:
- validazione dati → `DatiNonValidiException` → 422
- pagamento rifiutato → `RispostaPagamento(autorizzato=False)` → 402

### DAL — PagamentoRepository

| Metodo | Descrizione |
|--------|-------------|
| `aggiungi_metodo(utente_id, tipo, token_esterno, last_four) -> MetodoPagamento` | Salva metodo. Se primo → `predefinito=True`. |
| `lista_metodi(utente_id) -> list[MetodoPagamento]` | Lista metodi dell'utente. |
| `trova_metodo(metodo_id, utente_id) -> MetodoPagamento` | Trova per id (verifica appartenenza). |
| `exists_by_token(token_esterno: str) -> bool` | Verifica duplicato per token (da diagramma: `existsByToken`). |
| `imposta_predefinito(metodo_id, utente_id) -> None` | Reset tutti a false, set id a true. |
| `rimuovi_metodo(metodo_id, utente_id) -> None` | Elimina metodo. |
| `trova_predefinito(utente_id) -> MetodoPagamento \| None` | Metodo predefinito per effettua_pagamento. |
| `crea_pagamento(corsa_id, utente_id, metodo_id, importo, stato) -> Pagamento` | Crea record pagamento. |

### BLL — ServizioPricing

```python
class MetodoNonTrovato(Exception): pass
class MetodoDuplicato(Exception): pass
class DatiNonValidi(Exception): pass
class NessunMetodoPredefinito(Exception): pass
class PagamentoRifiutato(Exception): pass
class TariffaNonTrovata(Exception): pass
```

| Metodo | Item | Descrizione |
|--------|------|-------------|
| `aggiungi_metodo(utente_id, tipo, dati) -> dict` | IF-UT.12 | Chiama provider.valida_dati_pagamento → ottiene token → verifica duplicato → salva |
| `lista_metodi(utente_id) -> list[dict]` | IF-UT.12 | Delega al DAL |
| `imposta_predefinito(metodo_id, utente_id) -> dict` | IF-UT.21 | Verifica appartenenza → delega al DAL |
| `rimuovi_metodo(metodo_id, utente_id) -> None` | IF-UT.12 | Verifica appartenenza → delega al DAL |
| `calcola_importo(tipo_mezzo, durata_min, distanza_km) -> Decimal` | IF-UT.20 | Legge Tariffa dal DB |
| `effettua_pagamento(corsa_id, utente_id, tipo_mezzo, durata_min, distanza_km) -> dict` | IF-UT.20 | Punto di integrazione con `feature/corsa` |

**Flusso `aggiungi_metodo` (da diagramma):**
1. `provider.valida_dati_pagamento(tipo, dati)` → `token_esterno`
2. `repo.exists_by_token(token_esterno)` → se True → `MetodoDuplicato`
3. Crea e salva `MetodoPagamento`
4. Se primo metodo → già predefinito (gestito nel DAL)

**Flusso `effettua_pagamento` (da diagramma):**
1. `calcola_importo(tipo_mezzo, durata_min, distanza_km)`
2. `repo.trova_predefinito(utente_id)` — se None → `NessunMetodoPredefinito`
3. `provider.autorizza(metodo.token_esterno, importo)`
4. Se non autorizzato → salva `Pagamento(stato=rifiutato)` → `PagamentoRifiutato`
5. Salva `Pagamento(stato=completato)`
6. Restituisce `{pagamento_id, importo, stato, transazione_id}`

**Nota:** l'aggiornamento di `Corsa.stato = "Completata"` è responsabilità di `ServizioMobilita` in `feature/corsa`.

### Controller

Router prefix: `/utente/pagamenti`. Tutti i metodi richiedono `verify_token(required_roles=["UT"])`.

| Endpoint | Status | Errori |
|----------|--------|--------|
| `GET /metodi` | 200 | — |
| `POST /metodi` | 201 | 409 duplicato, 422 dati non validi |
| `PUT /metodi/{id}/predefinito` | 200 | 404 non trovato |
| `DELETE /metodi/{id}` | 204 | 404 non trovato |
| `POST /` | 201 | 402 pagamento rifiutato, 400 no metodo predefinito |

### Schemi Pydantic

```python
class AggiungiMetodoRequest(BaseModel):
    tipo: str           # "google_pay" | "apple_pay" | "paypal" | "carta"
    last_four: str | None = None   # solo per "carta"

class EffettuaPagamentoRequest(BaseModel):
    corsa_id: str
    tipo_mezzo: str     # "bicicletta" | "monopattino" | "automobile"
    durata_min: float
    distanza_km: float

class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool
```

---

## Test

| Test | Scenario |
|------|----------|
| `test_provider_autorizza_ok` | stub OK |
| `test_provider_rifiuta` | stub KO |
| `test_aggiungi_metodo_carta` | CS-13 base |
| `test_aggiungi_metodo_duplicato` | CS-13 — token già presente → 409 |
| `test_dati_non_validi` | CS-13 — provider rifiuta dati → 422 |
| `test_primo_metodo_diventa_predefinito` | CS-13 passo 9 |
| `test_imposta_predefinito` | IF-UT.21 base |
| `test_effettua_pagamento_ok` | CS-12 base |
| `test_pagamento_rifiutato` | CS-12.1 — stato rifiutato salvato |
| `test_pagamento_senza_metodo_predefinito` | CS-12 — no metodo → 400 |

---

## Integrazione con feature/corsa

`ServizioMobilita.termina_corsa()` chiamerà:

```python
from bll.servizio_pricing import ServizioPricing

riepilogo = ServizioPricing().effettua_pagamento(
    corsa_id=corsa.id,
    utente_id=utente_id,
    tipo_mezzo=corsa.tipo_mezzo,
    durata_min=durata_calcolata,
    distanza_km=corsa.distanza_km,
)
# poi aggiorna corsa.stato = "Completata" e mezzo.stato = "Disponibile"
```