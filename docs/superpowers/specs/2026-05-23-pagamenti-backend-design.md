# Design — Backend Pagamenti (feature/pagamenti)

**Data**: 2026-05-23  
**Item backlog**: IF-UT.12, IF-UT.20, IF-UT.21  
**Branch**: `feature/pagamenti`

---

## Scope

Implementazione del layer pagamenti lato backend. Non include termina-corsa, CorsaRepository, MezzoRepository o ServizioGIS — quei layer appartengono a `feature/corsa` e `feature/mappa-zone`. Il punto di integrazione con `feature/corsa` è `ServizioPricing.effettua_pagamento()`.

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

## Architettura

### Provider (nuovo layer)

`backend/providers/provider_pagamenti.py` — stub configurabile OK/KO:

```python
class RispostaPagamento:
    autorizzato: bool
    transazione_id: str

class ProviderPagamentiStub:
    def __init__(self, deve_fallire: bool = False): ...
    def autorizza(self, token: str, importo: Decimal) -> RispostaPagamento: ...
```

`deve_fallire=True` simula il flusso CS-12.1 (PagamentoRifiutato → 402).  
Il costruttore accetta il flag per facilitare i test senza monkey-patching.

### DAL — PagamentoRepository

Metodi:

| Metodo | Descrizione |
|--------|-------------|
| `aggiungi_metodo(utente_id, tipo, last_four) -> MetodoPagamento` | CS-13 passo 8. Genera token_esterno come UUID. Se è il primo metodo, lo imposta predefinito. |
| `lista_metodi(utente_id) -> list[MetodoPagamento]` | CS-13 passo 2 |
| `trova_metodo(metodo_id, utente_id) -> MetodoPagamento` | usato da imposta_predefinito e rimuovi |
| `metodo_gia_presente(utente_id, tipo, last_four) -> bool` | CS-13 passo 7 — verifica duplicati |
| `imposta_predefinito(metodo_id, utente_id) -> None` | IF-UT.21. Usa UPDATE con WHERE per atomicità. |
| `rimuovi_metodo(metodo_id, utente_id) -> None` | rimuove il metodo; se era predefinito, nessun nuovo predefinito automatico |
| `trova_predefinito(utente_id) -> MetodoPagamento \| None` | usato da effettua_pagamento |
| `crea_pagamento(corsa_id, utente_id, metodo_id, importo, stato, transazione_id) -> Pagamento` | CS-12 passo 14 |

Pattern: ogni metodo apre una `Session(engine)` autonoma, stessa convenzione di `AttoreRepository`.

### BLL — ServizioPricing

```python
class MetodoNonTrovatoException(Exception): pass
class MetodoDuplicatoException(Exception): pass
class NessunMetodoPredefinito(Exception): pass
class PagamentoRifiutatoException(Exception): pass
```

Metodi pubblici:

| Metodo | Item | Descrizione |
|--------|------|-------------|
| `aggiungi_metodo(utente_id, tipo, last_four) -> dict` | IF-UT.12 | Valida tipo, verifica duplicato, delega al DAL |
| `lista_metodi(utente_id) -> list[dict]` | IF-UT.12 | Delega al DAL, serializza |
| `imposta_predefinito(metodo_id, utente_id) -> dict` | IF-UT.21 | Verifica che il metodo esista e appartenga all'utente |
| `rimuovi_metodo(metodo_id, utente_id) -> None` | IF-UT.12 | Verifica appartenenza prima di rimuovere |
| `calcola_importo(tipo_mezzo, durata_min, distanza_km) -> Decimal` | IF-UT.20 | Recupera Tariffa dal DB; importo = durata×costo_al_minuto + distanza×costo_al_km |
| `effettua_pagamento(corsa_id, utente_id, tipo_mezzo, durata_min, distanza_km) -> dict` | IF-UT.20 | Punto di integrazione con `feature/corsa` |

**Flusso `effettua_pagamento`:**
1. `calcola_importo(tipo_mezzo, durata_min, distanza_km)`
2. `PagamentoRepository.trova_predefinito(utente_id)` — se None → `NessunMetodoPredefinitException`
3. `ProviderPagamentiStub.autorizza(token, importo)`
4. Se non autorizzato → salva Pagamento con `stato=rifiutato` → raise `PagamentoRifiutatoException`
5. Salva Pagamento con `stato=completato`
6. Restituisce `{pagamento_id, importo, stato, transazione_id}`

### Controller — /pagamenti/metodi

Tutti gli endpoint richiedono `verify_token(required_roles=["UT"])`.

| Metodo | Path | Item | Comportamento errore |
|--------|------|------|----------------------|
| `GET` | `/pagamenti/metodi` | IF-UT.12 | — |
| `POST` | `/pagamenti/metodi` | IF-UT.12 | 409 se duplicato |
| `PUT` | `/pagamenti/metodi/{id}/predefinito` | IF-UT.21 | 404 se non trovato |
| `DELETE` | `/pagamenti/metodi/{id}` | IF-UT.12 | 404 se non trovato |

### Schemi Pydantic (schemas.py)

```python
class AggiungiMetodoRequest(BaseModel):
    tipo: str          # "google_pay" | "apple_pay" | "paypal" | "carta"
    last_four: str | None  # solo per tipo "carta"

class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool
```

---

## Test (test_pagamenti.py)

| Test | Scenario | Marker |
|------|----------|--------|
| `test_aggiungi_metodo_carta` | CS-13 scenario base | unit |
| `test_aggiungi_metodo_duplicato` | CS-13 — metodo già presente → 409 | unit |
| `test_primo_metodo_diventa_predefinito` | CS-13 passo 9 | unit |
| `test_imposta_predefinito` | IF-UT.21 scenario base | unit |
| `test_effettua_pagamento_ok` | CS-12 scenario base | unit |
| `test_pagamento_rifiutato` | CS-12.1 — stub deve_fallire=True | unit |
| `test_pagamento_senza_metodo_predefinito` | CS-12 — utente senza metodo | unit |

I test mockano `PagamentoRepository` e `ProviderPagamentiStub` — nessun DB richiesto.

---

## Integrazione con feature/corsa

`ServizioMobilita.termina_corsa()` (in `feature/corsa`) chiamerà:

```python
from bll.servizio_pricing import ServizioPricing

riepilogo_pagamento = ServizioPricing().effettua_pagamento(
    corsa_id=corsa.id,
    utente_id=utente_id,
    tipo_mezzo=corsa.tipo_mezzo,
    durata_min=durata_calcolata,
    distanza_km=corsa.distanza_km,
)
```
