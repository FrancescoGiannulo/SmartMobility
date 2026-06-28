# IF-OP.09 — Sospende Account Utente — Design

**Data:** 2026-06-21
**Backlog item:** `IF-OP.09` / caso d'uso `OP-09` (`docs/Sprintn3.md` § 2.4.3.25, § 2.2.2.19, § 1.4.25)

## Contesto

Il caso d'uso OP-09 ("Sospende Account Utente") è già completamente modellato nel diagramma delle classi (`docs/Diagrammi/Diagramma Classi.drawio` / export `DiagrammaClassi.md`) e nel diagramma di sequenza (`docs/Diagrammi/Diagrammi di Sequenza/Flavio/sprint2/sequence_sospende_account_utente.drawio`), ma non è mai stato implementato (annotato come "pianificato, non implementato" in `docs/CoerenzaDiagrammaClassi.md`).

Parte della base esiste già:
- `Utente.sospeso: bool` (colonna DB, ORM, dataclass) — già presente.
- `ServizioUtenti.autentica_account` blocca già il login se `profilo.sospeso` è `True`, lanciando `AccountSospesoException` → HTTP 403 (`docs/...`, `backend/bll/servizio_utenti.py:111`).
- Un bottone placeholder "Gestisci utenti" esiste già in `VistaMappaOperatore.tsx:327` senza `onClick`.

Quello che manca: la motivazione della sospensione, l'elenco/dettaglio utenti per l'Operatore, l'endpoint di sospensione, la notifica persistita, e la UI lato Operatore.

## Scope

**Incluso:**
- Operatore consulta elenco utenti, apre dettaglio, inserisce motivazione, sospende l'account con conferma.
- Notifica persistita in DB per l'Utente sospeso (no UI di lettura — vedi "Fuori scope").
- Login bloccato per utenti sospesi (già esistente, verificato/testato in questo lavoro).

**Fuori scope (decisioni esplicite):**
- **Riattivazione account**: non presente nel caso d'uso OP-09 né nel diagramma di sequenza. Non implementata in questo lavoro — eventuale item futuro separato.
- **Invalidazione sessione attiva**: la sospensione blocca solo i login futuri, coerente con il pattern già esistente per `AccountBloccatoException`. Nessuna chiamata a `supabase.auth.admin` per revocare sessioni JWT già emesse.
- **UI notifiche/centro notifiche**: `Notifica`/`NotificaService`/`NotificaRepository` vengono creati e usati (come richiesto dal diagramma), ma solo per persistenza. L'Utente è già informato del blocco tramite il 403 al login; un'eventuale UI di notifica è lavoro futuro.

## Backend

### Migrazione `backend/migrations/015_sospensione_account.sql`
```sql
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

### Model
- `backend/model/notifica.py` — dataclass `Notifica(id, idUtente, messaggio, letta, data)`, allineata al diagramma classi.
- `backend/model/orm.py` — entità ORM `Notifica` (tabella `notifiche`), per coerenza con il pattern esistente (`Utente`, `Operatore`, ...).

### DAL
- `backend/dal/notifica_repository.py` — `NotificaRepository`:
  - `crea(idUtente: UUID, messaggio: str) -> Notifica`
  - `findByUtente(idUtente: UUID) -> list[Notifica]`
- `backend/dal/attore_repository.py` — aggiunte a `AttoreRepository`:
  - `lista_utenti() -> list[dict]` — join `utenti` + `auth.users` per recuperare l'email (pattern già usato in `trova_per_email`).
  - `trova_utente_per_id(id: UUID) -> dict` — dettaglio singolo utente (stesso join); lancia `AttoreNonTrovatoException` se assente.
  - `sospendi(id: UUID, motivazione: str) -> None` — `UPDATE utenti SET sospeso=true, motivazione_sospensione=:m, sospeso_at=NOW() WHERE id=:id`; lancia `AttoreNonTrovatoException` se l'utente non esiste, `AccountGiaSospesoException` se `sospeso` è già `true` (precondizione 2 del caso d'uso: "l'account è attivo").

### BLL
- `backend/bll/notifica_service.py` — `NotificaService.notifica(idUtente: UUID, messaggio: str) -> None`, delega a `NotificaRepository.crea`.
- `backend/bll/servizio_utenti.py` — nuova eccezione `AccountGiaSospesoException`; nuovi metodi su `ServizioUtenti`:
  - `get_utenti() -> list[dict]`
  - `get_dettaglio_utente(id: UUID) -> dict`
  - `sospendi_account(id: UUID, motivazione: str) -> None` — valida `motivazione` non vuota (`ValueError` se vuota/whitespace), chiama `self._repo.sospendi(id, motivazione)`, poi `NotificaService().notifica(id, f"Il tuo account è stato sospeso. Motivo: {motivazione}")`.

### Controller
- `backend/controllers/utenti_op_controller.py` (nuovo, `UtentiOPController` del diagramma):
  - `GET /operatore/utenti` → `ServizioUtenti().get_utenti()`
  - `GET /operatore/utenti/{utente_id}` → `get_dettaglio_utente`, 404 se non trovato
  - `PATCH /operatore/utenti/{utente_id}/stato` body `SospensioneRequest{motivazione: str}` → `sospendi_account`; 404 se non trovato, 409 se già sospeso, 422 se motivazione vuota
  - Tutte le route con `Depends(verify_token(["OP"]))`
- `backend/controllers/schemas.py` — `UtenteListItemOut`, `UtenteDettaglioOut`, `SospensioneRequest`
- `backend/main.py` — registra il nuovo router

### Test (`backend/tests/test_sospendi_account.py`)
- Scenario base: OP sospende UT attivo con motivazione → 200, `sospeso=true`, notifica creata.
- Motivazione vuota → 422.
- Utente già sospeso → 409 (`AccountGiaSospesoException`).
- Utente inesistente → 404.
- Ruolo non-OP che chiama l'endpoint → 403.
- Login dell'utente sospeso dopo la sospensione → 403 `AccountSospesoException` (riusa/estende pattern `test_auth.py::test_login_account_sospeso`).

## Frontend

- `frontend/src/services/GestioneUtentiService.ts` (nome esatto del diagramma di sequenza, lifeline `:GestioneUtentiService`):
  - `interface UtenteListItem { id, nome, cognome, email, sospeso }`
  - `getUtenti(): Promise<{data: UtenteListItem[]}>`
  - `getDettaglioUtente(id): Promise<{data: UtenteListItem}>`
  - `sospendiAccount(id, motivazione): Promise<{data: UtenteListItem}>`
- `frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx` + `.css` — stesso pattern strutturale di `VistaSegnalazioniOperatore.tsx`: lista a sinistra, dettaglio a destra, textarea motivazione obbligatoria, dialogo di conferma, badge "Sospeso" e azione disabilitata se già sospeso.
- `frontend/src/App.tsx` — rotta `/operatore/utenti`, `ruoloRichiesto="OP"`.
- `frontend/src/views/operatore/VistaMappaOperatore.tsx:327` — collega il bottone placeholder "Gestisci utenti" a `navigate('/operatore/utenti')`.

## Documentazione

- `docs/Sprintn3.md` § OP-09: correggere le post-condizioni (attualmente testo copiato dal caso d'uso "Gestisce Segnalazione") in qualcosa come: "L'account dell'Utente è sospeso; l'Utente non può più accedere alla piattaforma; l'Utente è stato notificato dell'avvenuta sospensione."
- `docs/CoerenzaDiagrammaClassi.md`: aggiornare a ✅ le righe `VistaGestioneUtentiOperatore`, `UtentiOPController`, `NotificaService`, `Notifica`, `NotificaRepository`, `AttoreRepository.sospendi`; rimuovere dal riepilogo "Critiche" i punti relativi (`VistaGestioneUtentiOperatore mancante`, `UtentiOPController mancante`); aggiungere una riga in "Cronologia fix".

## Vincoli architetturali rispettati

- Controller solo validazione/smistamento HTTP, nessuna logica.
- Logica di sospensione in `ServizioUtenti` (BLL), nessun accesso diretto al DB.
- `AttoreRepository` (DAL) gestisce solo l'accesso ai dati.
- Nomi delle classi/metodi coerenti con il diagramma delle classi (`sospendiAccount`, `sospendi`, `notifica`, `Notifica`, `GestioneUtentiService`).
