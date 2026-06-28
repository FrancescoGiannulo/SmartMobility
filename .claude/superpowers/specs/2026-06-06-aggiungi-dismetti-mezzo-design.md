# Design Spec — Aggiunge Mezzo & Dismette Mezzo

**Data:** 2026-06-06  
**Item backlog:** IF-OP.11 (CS-11) — Aggiunge Mezzo, IF-OP.12 (CS-12) — Dismette Mezzo  
**Approccio scelto:** A — fedele ai diagrammi di sequenza  

---

## Contesto

L'Operatore deve poter censire nuovi mezzi nella flotta e dismettere quelli fuori uso. Entrambi i flussi sono specificati nei diagrammi di sequenza `sequence_aggiunge_mezzo.drawio` e `sequence_dismette_mezzo.drawio`. La `VistaMezziOperatore` non esiste ancora e va creata come pagina separata con route `/operatore/mezzi`.

---

## Backend

### DAL — `MezzoRepository` (nuovi metodi)

| Metodo | Firma | Note |
|---|---|---|
| `esiste_by_codice` | `(codice: str) -> bool` | Check unicità identificativo prima dell'inserimento |
| `crea` | `(tipo, codice, lat, lng, stato) -> dict` | INSERT mezzo, ritorna il record creato |
| `lista_tutti` | `() -> list[dict]` | Tutti i mezzi esclusi i dismessi, per la gestione operatore |
| `ha_corse_attive` | `(mezzo_id: UUID) -> bool` | Query corse non-terminate associate al mezzo |

`lista_tutti` esclude i mezzi dismessi e non filtra per presenza di coordinate (diversamente da `lista_per_mappa`).

### BLL — `ServizioMobilita` (nuovi metodi)

| Metodo | Eccezioni sollevate | Flusso |
|---|---|---|
| `get_mezzi_flotta() -> list[dict]` | — | Delega a `MezzoRepository.lista_tutti()` |
| `aggiungi_mezzo(tipo, codice, lat, lng, stato) -> dict` | `IdentificativoEsistenteException`, `PosizioneNonOperativaException` | 1. `esiste_by_codice` → 2. `ServizioGIS.verifica_posizione_in_zona_operativa` → 3. `crea` |
| `verifica_dismissione(mezzo_id) -> dict` | `MezzoNonTrovatoException`, `MezzoInMissioneException` | Controlla stato mezzo + corse attive nel DB |
| `dismetti_mezzo(mezzo_id) -> None` | `MezzoNonTrovatoException`, `MezzoInMissioneException` | Re-esegue i check + `aggiorna_stato("Dismesso")` |

`IdentificativoEsistenteException` e `PosizioneNonOperativaException` sono nuove eccezioni da definire in `servizio_mobilita.py`. `MezzoInMissioneException` è nuova; `MezzoNonTrovatoException` già esiste.

### BLL — `ServizioGIS` (nuovo metodo)

**`verifica_posizione_in_zona_operativa(lat: float, lng: float) -> bool`**

Aggiunge a `ZonaRepository` un metodo `punto_in_zona_operativa(lat, lng) -> bool` che esegue una query SQL con `ST_Within(ST_SetSRID(ST_MakePoint(:lng, :lat), 4326), perimetro)` filtrando su `tipo = 'operativa' AND attiva = true`. `ServizioGIS` chiama questo metodo e solleva `PosizioneNonOperativaException` se ritorna `False`.

### Controller — `MezzoOperatoreController` (nuove route)

Tutte le route richiedono token OP (`Depends(verify_token(["OP"]))`).

| Route | Metodo | Input | Output successo | Errori |
|---|---|---|---|---|
| `/operatore/mezzi` | GET | — | `200 list[MezzoFlottaOut]` | — |
| `/operatore/mezzi` | POST | `AggiungiMezzoRequest` | `201 MezzoFlottaOut` | `409` identificativo duplicato, `422` posizione fuori zona |
| `/operatore/mezzi/{id}/verifica` | POST | — | `200 {dismettibile: bool, mezzo: MezzoFlottaOut}` | `404` non trovato |
| `/operatore/mezzi/{id}` | DELETE | — | `200 {"status": "ok"}` | `404` non trovato, `409` mezzo in missione |

### Schemi Pydantic (in `schemas.py`)

```python
class AggiungiMezzoRequest(BaseModel):
    tipo: str          # "monopattino" | "bicicletta" | "automobile"
    codice: str
    lat: float
    lng: float
    stato: str = "Disponibile"

class MezzoFlottaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float | None
    lng: float | None
    batteria: int | None
```

---

## Frontend

### `FlottaService.ts` (modifiche)

I path `/flotta/mezzi` esistenti vengono corretti a `/operatore/mezzi`. Nuovi metodi aggiunti:

| Funzione | HTTP | Endpoint |
|---|---|---|
| `getMezziFlotta()` | GET | `/operatore/mezzi` |
| `aggiungiMezzo(data)` | POST | `/operatore/mezzi` |
| `verificaDismissione(id)` | POST | `/operatore/mezzi/{id}/verifica` |
| `dismetti(id)` | DELETE | `/operatore/mezzi/{id}` |

### `VistaMezziOperatore.tsx` — nuova pagina

**Route:** `/operatore/mezzi`  
**File:** `frontend/src/views/operatore/VistaMezziOperatore.tsx`

**Struttura UI:**
1. **Tabella flotta** — colonne: Codice, Tipo, Stato (pill colorata semanticamente), Batteria, Coordinate, Azioni
2. **Bottone "Aggiungi mezzo"** — apre modal con form: Tipo (select `monopattino|bicicletta|automobile`), Codice (text), Lat/Lng (number), Stato iniziale (select, default `Disponibile`)
3. **Bottone "Dismetti"** per riga — chiama `verificaDismissione(id)`:
   - Se `dismettibile: true` → mostra dialog di conferma
   - Se `dismettibile: false` → mostra toast errore con motivo

**Stati UI gestiti:**
- Loading skeleton durante il fetch iniziale
- Toast successo/errore dopo ogni operazione
- Modal form aggiungi (con validation inline)
- Dialog conferma dismissione (due step, da diagramma)

### Routing

Va aggiunta la route nel router principale e un link nella sidebar/navbar operatore, coerente con il pattern delle altre viste.

---

## Test

### `tests/test_aggiungi_mezzo.py`

| Test | Scenario | Atteso |
|---|---|---|
| `test_aggiunge_mezzo_ok` | Codice univoco, posizione in zona operativa | `201`, mezzo nel DB con stato `Disponibile` |
| `test_aggiunge_mezzo_codice_duplicato` | Stesso codice già esistente | `409 Conflict` |
| `test_aggiunge_mezzo_posizione_fuori_zona` | Lat/lng fuori da qualsiasi zona operativa | `422 Unprocessable` |

### `tests/test_dismetti_mezzo.py`

| Test | Scenario | Atteso |
|---|---|---|
| `test_verifica_dismissione_ok` | Mezzo `Disponibile`, nessuna corsa attiva | `{dismettibile: true}` |
| `test_verifica_dismissione_stato_bloccante` | Mezzo con stato `In uso` | `MezzoInMissioneException` → `409` |
| `test_verifica_dismissione_corsa_attiva` | Mezzo `Disponibile` ma corsa non terminata | `MezzoInMissioneException` → `409` |
| `test_dismetti_ok` | Scenario base | Stato aggiornato a `Dismesso`, `200 OK` |
| `test_dismetti_mezzo_non_trovato` | ID inesistente | `404 Not Found` |

Tutti i test sono unit test con mock dei repository. I test di integrazione vengono taggati `@pytest.mark.integration`.

---

## Tracciabilità

| Componente | ID backlog |
|---|---|
| `GET /operatore/mezzi` | IF-OP.11 |
| `POST /operatore/mezzi` | IF-OP.11 |
| `POST /operatore/mezzi/{id}/verifica` | IF-OP.12 |
| `DELETE /operatore/mezzi/{id}` | IF-OP.12 |
| `VistaMezziOperatore` | IF-OP.11, IF-OP.12 |
