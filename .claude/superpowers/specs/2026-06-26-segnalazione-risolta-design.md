# Gestisci segnalazione — stato "risolta" [IF-OP.08]

## Problema
`StatoSegnalazione` (model/segnalazione.py) supporta solo `aperta` → `in_carico`. Non esiste modo per l'operatore di chiudere una segnalazione, né per l'utente di vedere che è stata risolta. `VistaSegnalazioniOperatore.tsx` mostra solo "PRENDI IN CARICO"; `VistaSegnalazione.tsx` (storico utente) mappa solo i due stati esistenti nei badge.

## Decisioni
- Nuovo stato `risolta`, transizione valida solo da `in_carico` (non da `aperta` — l'operatore deve prima prendere in carico).
- Tentativo di risolvere una segnalazione non in `in_carico` → errore esplicito, mappato a HTTP 422 (stesso pattern di `OffertaNonValida` in `servizio_abbonamento.py`).
- Nessuna notifica push all'utente: lo stato "risolta" appare semplicemente nel badge dello storico (`VistaSegnalazione.tsx`), già ricaricato via `caricaStorico()`.
- Stato terminale: nessuna transizione fuori da `risolta`.

## Modifiche

**Migrazione** (`backend/migrations/020_segnalazione_risolta.sql`): `ALTER TYPE stato_segnalazione ADD VALUE 'risolta';`

**Model** (`backend/model/segnalazione.py`): aggiungere `risolta = "risolta"` a `StatoSegnalazione`.

**BLL** (`backend/bll/servizio_segnalazione.py`):
- Nuova eccezione `TransizioneNonValida(Exception)`.
- Nuovo metodo `risolvi(segnalazione_id)`: legge stato corrente via `get_dettaglio_segnalazione`, se non è `in_carico` solleva `TransizioneNonValida`, altrimenti chiama `self._repo.aggiorna_stato(segnalazione_id, StatoSegnalazione.risolta)` (riusa il metodo generico esistente) e ritorna il dettaglio aggiornato.

**Controller** (`backend/controllers/segnalazione_op_controller.py`):
- Nuovo endpoint `PATCH /operatore/segnalazioni/{segnalazione_id}/risolvi` → `ServizioSegnalazione(db).risolvi(...)`.
- Cattura `SegnalazioneNonTrovata` → 404, `TransizioneNonValida` → 422.

**Frontend**
- `SegnalazioneService.ts`: tipo `Segnalazione.stato` → `'aperta' | 'in_carico' | 'risolta'`; nuova funzione `risolviSegnalazione(id)` → `PATCH /operatore/segnalazioni/{id}/risolvi`.
- `VistaSegnalazioniOperatore.tsx`: aggiungere `risolta: 'Risolta'` / `badge-risolta` a `STATO_LABEL`/`STATO_CLASS`; bottone "SEGNA COME RISOLTA" visibile quando `selezionata.stato === 'in_carico'` (sostituisce/affianca il messaggio "Già presa in carico"); messaggio di conferma analogo a `prendiInCarico`.
- `VistaSegnalazione.tsx`: aggiungere `risolta: 'Risolta'` / classe badge a `STATO_LABEL`/`STATO_CLASS` per lo storico utente. Nessun'altra modifica — il polling esistente (`caricaStorico` al mount) basta, l'utente vede lo stato aggiornato quando ricarica/rivisita la pagina.

## Test
- Backend: scenario base (`in_carico` → `risolvi` → stato `risolta`, visibile in `find_by_utente`); scenario alternativo (`risolvi` su segnalazione `aperta` → `TransizioneNonValida`/422); scenario alternativo (`risolvi` su id inesistente → 404).
- Frontend: nessun test automatico nuovo (pattern esistente per questa vista non ha test); verifica manuale del badge e del bottone nei due ruoli.
