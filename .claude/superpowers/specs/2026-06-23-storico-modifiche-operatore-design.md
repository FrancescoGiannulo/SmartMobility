# Storico Modifiche — mostrare l'operatore che ha effettuato la modifica [IF-OP.13]

## Contesto e problema

La vista "Storico Modifiche" (`VistaStoricoModifiche.tsx`) registra per ogni voce l'`operatore_id` che ha effettuato la modifica (colonna già presente in `storico_modifiche`, popolata da tutti i servizi che scrivono nello storico), ma non lo mostra mai all'operatore che consulta la vista. Le card mostrano solo data, descrizione e diff dei valori.

## Obiettivo

Mostrare il nome dell'operatore autore della modifica in ogni voce dello storico, risolvendo `operatore_id` → `nome` tramite la tabella `operatori`.

## Backend

### `backend/dal/storico_modifiche_repository.py`

`find_all()`: la query passa da `SELECT ... FROM storico_modifiche` a un `LEFT JOIN operatori o ON o.id = sm.operatore_id`, aggiungendo `o.nome AS operatore_nome` alla SELECT. `LEFT JOIN` (non `INNER`) per non perdere righe storiche il cui operatore è stato successivamente rimosso — in quel caso `operatore_nome` torna `NULL`.

`crea()` non viene modificato: l'INSERT...RETURNING non ha bisogno del nome (il valore appena creato non passa dalla vista storico in quel momento); l'oggetto restituito avrà `operatore_nome=None`.

### `backend/model/storico_modifiche.py`

Nuovo campo sul dataclass: `operatore_nome: str | None = None`.

### `backend/bll/servizio_storico_modifiche.py`

`get_storico()`: il dict di output aggiunge `"operatore_nome": v.operatore_nome`.

### `backend/controllers/schemas.py`

`StoricoModificaOut`: nuovo campo `operatore_nome: str | None = None`.

## Frontend

### `frontend/src/services/StoricoModificheService.ts`

L'interfaccia `StoricoModifica` aggiunge `operatore_nome: string | null`.

### `frontend/src/views/operatore/VistaStoricoModifiche.tsx`

Nell'header della card (`storico-mod-card-header`, accanto alla data), si aggiunge una riga con il nome dell'operatore: `Modificato da: {operatore_nome}`. Se `operatore_nome` è `null` (operatore cancellato), si mostra `Operatore non disponibile`.

## Test

`backend/tests/test_storico_modifiche.py`:
- I test esistenti che usano `uuid.uuid4()` senza inserire una riga in `operatori` restano verdi: con `LEFT JOIN`, `operatore_nome` è semplicemente `None`, nessuna asserzione esistente lo controlla.
- Nuovo test in `TestStoricoModificheRepository`: inserisce un operatore reale (via `INSERT INTO operatori` o fixture esistente se disponibile), crea una voce di storico con quel `operatore_id`, e verifica che `find_all()` restituisca `operatore_nome` popolato correttamente. Cleanup della riga operatore in `finally`.

## Non in scope

- Nessuna migrazione DB (`operatore_id` esiste già).
- Nessuna modifica alla logica di registrazione delle modifiche (`registra_modifica`) — riguarda solo la lettura/visualizzazione.
- Nessun nuovo campo "email" o altro identificativo — solo `nome`, come da approvazione utente.
