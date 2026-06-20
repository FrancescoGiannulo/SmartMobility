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
- `backend/bll/servizio_recensione.py`: `ServizioRecensione.scrivi_recensione(utente_id, voto, commento)` — valida voto (1-5, altrimenti 422) poi salva. `valida_voto(voto)` esposto come metodo separato per rispettare il diagramma.

**Nota di fedeltà ai diagrammi**: la precondizione 2 dello use case ("ha effettuato e concluso almeno una corsa") non è enforced lato codice. Il diagramma delle classi assegna a `ServizioRecensione` solo `recensioneRepo: IRecensioneRepository` (nessuna dipendenza da `CorsaRepository`), e il diagramma di sequenza non mostra alcun passo di verifica — passa direttamente da `scriviRecensione` a `validaVoto` a `save`. Diagramma classi e diagramma di sequenza sono entrambi vincolanti per CLAUDE.md: in caso di conflitto con la prosa dello use case, prevalgono i diagrammi. Non aggiungo quindi una dipendenza da `CorsaRepository` non modellata.
- `backend/controllers/recensione_controller.py`: router `prefix="/utente"`, `POST /recensioni` con `verify_token(["UT"])`, `status_code=201`
- `backend/controllers/schemas.py`: `ScriviRecensioneRequest{voto:int, commento:str|None}`, `RecensioneOut{id,voto,commento,created_at}`
- `backend/main.py`: registrazione router

### Frontend

- `frontend/src/services/RecensioneService.ts`: `scriviRecensione(voto, commento)` → `POST /utente/recensioni`
- `frontend/src/views/utente/VistaRecensione.tsx`: form voto a stelle (1-5) + textarea commento facoltativo + stato conferma/errore (ricalca `VistaSegnalazione.tsx`)
- `App.tsx`: route `/utente/recensione` protetta da `RoutaProtetta ruoloRichiesto="UT"`
- `VistaHomePageUtente.tsx`: voce sidebar "Lascia recensione" nel menu

### Test

- `backend/tests/test_recensione.py` (integration, fixture `utente_test`): scenario base (salvataggio riuscito, recensione associata all'utente) + validazione voto fuori range (0 o 6 → 422) + voto valido senza commento (campo facoltativo)

## Note di scope

- Nessuna modifica/cancellazione recensione: non richiesta dallo use case né dal diagramma.
- Nessun endpoint di lettura per l'AP/operatore in questo slice (IF-OP.13 "Visualizza Recensioni" è fuori scope, non specificato nel diagramma fornito).
