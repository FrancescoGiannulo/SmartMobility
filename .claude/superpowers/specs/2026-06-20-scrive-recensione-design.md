# Design — UT-15 Scrive Recensione

## Caso d'uso (fonte: Sprint3_SMART_Mobility.md, confermato dall'utente)

| Campo | Valore |
|---|---|
| ID | UT-15 |
| Attori | Utente |
| Precondizioni | 1. Utente autenticato. 2. Utente ha effettuato e concluso almeno una corsa. |
| Scenario base | 1. Utente apre "Lascia Recensione" dal menu. 2. Sistema mostra form (voto 1-5, commento facoltativo). 3-4. Utente compila. 5. Utente conferma. 6. Sistema salva recensione associata all'utente. 7. Sistema mostra conferma. |
| Post-condizioni | Recensione salvata e associata all'Utente. |
| Scenari alternativi | Nessuno (documentato così nello use case). |

Regola di dominio (glossario): un Utente può lasciare più recensioni nel tempo; la recensione non è vincolata a una singola corsa.

## Diagrammi di riferimento

- `docs/Diagrammi/Diagrammi di Sequenza/camilla/sprint2/sequence_scrive_recensione.drawio`
- `docs/Diagrammi/Diagramma Classi.drawio` (export in `docs/Diagrammi/DiagrammaClassi.md`)

Flusso (dal diagramma di sequenza): `VistaRecensione.confermaScrivi(voto, commento)` → `RecensioneService.scriviRecensione(voto, commento)` → `ApiService.inviaRichiesta` → `POST /utente/recensioni` (HTTPS+JWT) → `FrontController.validaAutenticazione()` → `RecensioneController.scriviRecensione(idUtente, voto, commento)` → `ServizioRecensione.scriviRecensione(idUtente, voto, commento)` → `validaVoto(voto)` → `RecensioneRepository.save(recensione)` → risposta 201 con `:recensione` a ritroso fino a `mostraConfermaRecensione()`.

## Classi coinvolte (nomi esatti dal diagramma — vincolanti)

- **Model**: `Recensione` (id, idUtente, voto:int, commento:String, dataCreazione:DateTime)
- **DAL**: `RecensioneRepository` — `save(r)`, `findByUtenteId(idUtente)`, `findAll()`
- **BLL**: `IServizioRecensione` / `ServizioRecensione` — `scriviRecensione(idUtente, voto, commento): Recensione`, `validaVoto(voto): boolean`
- **Controller**: `RecensioneController` — `scriviRecensione(idUtente, voto, commento): Response`
- **Client Service**: `RecensioneService` — `scriviRecensione(voto, commento): void`
- **View**: `VistaRecensione` — `apriFormRecensione()`, `mostraFormRecensione()`, `confermaScrivi(voto, commento)`, `mostraConfermaRecensione()`, `mostraErrore(msg)`

## Implementazione

### Backend (segue il pattern di `Segnalazione`, l'analogo più vicino)

- `backend/migrations/014_recensioni.sql`: tabella `recensioni` (id uuid PK, utente_id uuid FK→utenti, voto int CHECK 1-5, commento text NULL, created_at timestamptz default now())
- `backend/model/recensione.py`: ORM `Recensione` (stile identico a `model/segnalazione.py`)
- `backend/dal/recensione_repository.py`: `RecensioneRepository` (pattern engine-based come `SegnalazioneRepository`) con `save`, `find_by_utente_id`, `find_all`
- `backend/dal/corsa_repository.py`: aggiunto `ha_corsa_conclusa(utente_id) -> bool` (query `EXISTS` su `stato='terminata'`)
- `backend/bll/servizio_recensione.py`: `ServizioRecensione.scrivi_recensione(utente_id, voto, commento)` — valida voto (1-5, altrimenti 422), verifica precondizione 2 dello use case tramite `ha_corsa_conclusa(utente_id)` (altrimenti 422 `CorsaNonConclusaException`), poi salva. `valida_voto(voto)` e `ha_corsa_conclusa(idUtente)` esposti come metodi separati per rispettare il diagramma.

**Aggiornamento (decisione utente, 2026-06-20)**: la precondizione 2 dello use case ("ha effettuato e concluso almeno una corsa") è stata inizialmente esclusa dall'implementazione perché non modellata nei diagrammi originali (`ServizioRecensione` aveva solo `recensioneRepo: IRecensioneRepository`). Su richiesta esplicita dell'utente è stata successivamente aggiunta sia al codice che ai diagrammi: `Diagramma Classi.drawio` ora include `- corsaRepo: ICorsaRepository` e `+ haCorsaConclusa(idUtente: String): boolean` su `ServizioRecensione`/`IServizioRecensione`; `sequence_scrive_recensione.drawio` include il passo `10b: haCorsaConclusa(idUtente)` con il ramo alternativo (precondizione non soddisfatta → 422) prima di `save(recensione)`. Diagrammi e codice sono quindi nuovamente allineati.
- `backend/controllers/recensione_controller.py`: router `prefix="/utente"`, `POST /recensioni` con `verify_token(["UT"])`, `status_code=201`
- `backend/controllers/schemas.py`: `ScriviRecensioneRequest{voto:int, commento:str|None}`, `RecensioneOut{id,voto,commento,created_at}`
- `backend/main.py`: registrazione router

### Frontend

- `frontend/src/services/RecensioneService.ts`: `scriviRecensione(voto, commento)` → `POST /utente/recensioni`
- `frontend/src/views/utente/VistaRecensione.tsx`: form voto a stelle (1-5) + textarea commento facoltativo + stato conferma/errore (ricalca `VistaSegnalazione.tsx`)
- `App.tsx`: route `/utente/recensione` protetta da `RoutaProtetta ruoloRichiesto="UT"`
- `VistaHomePageUtente.tsx`: voce sidebar "Lascia recensione" nel menu

### Test

- `backend/tests/test_recensione.py` (integration): scenario base con fixture `utente_con_corsa_conclusa` (salvataggio riuscito, recensione associata all'utente) + voto valido senza commento + voto fuori range → 422 + utente senza corsa conclusa → 422 + non autenticato → 401

## Note di scope

- Nessuna modifica/cancellazione recensione: non richiesta dallo use case né dal diagramma.
- Nessun endpoint di lettura per l'AP/operatore in questo slice (IF-OP.12 "Visualizza Recensioni" è fuori scope, non specificato nel diagramma fornito).
