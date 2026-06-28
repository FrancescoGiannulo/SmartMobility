# Storico Modifiche — sezioni per categoria e diff leggibile [IF-OP.13]

## Contesto e problema

La vista "Storico Modifiche" (`VistaStoricoModifiche.tsx`) mostra oggi tutte le voci in un'unica lista cronologica, senza raggruppamento per tipo di configurazione. Inoltre per ogni voce mostra l'intero dump di "Prima"/"Dopo" con tutti i campi del record, anche quelli non cambiati (es. `addebito_pausa_min=0.0000` → `addebito_pausa_min=0.0000`), rendendo difficile capire cosa è realmente cambiato.

Inoltre, oggi il backend registra nello storico solo: `parametri_sistema`, `regole_fine_corsa`, `zona_creata`, `zona_eliminata`. Le modifiche a **Tariffe** e **Offerte** non vengono registrate.

## Obiettivo

1. Estendere il backend per registrare anche le modifiche a Tariffe e Offerte nello storico.
2. Riorganizzare la UI in sezioni per categoria (accordion), con diff leggibile che mostra solo i campi effettivamente cambiati, con etichette in italiano e unità di misura.

## Backend

### Convenzione esistente da riusare

`valore_precedente` e `valore_nuovo` sono colonne `TEXT` in `storico_modifiche`, già popolate con il formato `"campo1=valore1, campo2=valore2, ..."` (vedi `servizio_parametri.py`, `servizio_regole_fine_corsa.py`, `servizio_mappa.py`). Questa convenzione viene **riusata** per le nuove categorie — nessuna modifica di schema, nessuna migrazione necessaria, e le righe storiche già presenti restano leggibili con lo stesso parser frontend.

### Nuovi tipi di configurazione

| `tipo_configurazione` | Quando | Campi loggati |
|---|---|---|
| `tariffa_creata` | `ServizioTariffa.crea_tariffa` | `tipo_mezzo`, `costo_al_minuto`, `costo_al_km` |
| `tariffa_modificata` | `ServizioTariffa.aggiorna_tariffa` | `tipo_mezzo`, `costo_al_minuto`, `costo_al_km` |
| `offerta_creata` | `ServizioOfferta.crea_offerta` | `nome`, `tipo`, `descrizione`, `sconto_percentuale`, `prezzo`, `durata_giorni`, `data_inizio`, `data_scadenza`, `tipo_mezzo` |
| `offerta_modificata` | `ServizioOfferta.modifica_offerta` | stessi campi sopra + `stato` |
| `offerta_eliminata` | `ServizioOfferta.elimina_offerta` | stessi campi dell'offerta eliminata |

### Modifiche puntuali

- **`backend/bll/servizio_tariffa.py`**: inietta `ServizioStoricoModifiche` nel costruttore. `crea_tariffa` e `aggiorna_tariffa` accettano un nuovo parametro obbligatorio `operatore_id: UUID`. Dopo la persistenza, chiamano `registra_modifica` con `valore_precedente=None` (per la creazione) o i valori del record letto prima dell'update (per la modifica), e `valore_nuovo` con i valori aggiornati, nel formato `key=value` esistente.
- **`backend/controllers/tariffa_controller.py`**: le route `crea_tariffa` e `aggiorna_tariffa` cambiano la dipendenza da `_=Depends(verify_token(["OP"]))` a `_op=Depends(verify_token(["OP"]))` e passano `operatore_id=UUID(str(_op["id"]))` al service.
- **`backend/bll/servizio_offerte.py`**: inietta `ServizioStoricoModifiche` nel costruttore. `crea_offerta`, `modifica_offerta`, `elimina_offerta` accettano `operatore_id: UUID`. `modifica_offerta` ha già `offerta_corrente` disponibile (già letta per la validazione) da usare come `valore_precedente`. `elimina_offerta` deve leggere l'offerta prima di eliminarla per poter loggare `valore_precedente`.
- **`backend/controllers/offerta_controller.py`**: il dependency `_op` è già presente su tutte le route; basta passare `operatore_id=UUID(str(_op["id"]))` alle tre chiamate al service.

### Non in scope

- Nessuna modifica a `parametri_sistema`, `regole_fine_corsa`, `zona_*` — restano come sono (stesso formato, già corretto).
- Nessuna modifica allo schema DB o a `StoricoModificheRepository`.

## Frontend

### `VistaStoricoModifiche.tsx`

**Parsing generico:**
```ts
function parseValori(s: string | null): Record<string, string> {
  // "a=1, b=2" -> { a: "1", b: "2" }
}
```

**Calcolo diff:**
```ts
function calcolaDiff(prec: string | null, nuovo: string | null): Array<{campo: string, prima?: string, dopo?: string}> {
  // - se entrambi presenti: solo le chiavi con valore diverso
  // - se solo nuovo presente (creazione): tutte le chiavi di nuovo
  // - se solo prec presente (eliminazione): tutte le chiavi di prec
}
```

**Configurazione categorie** — mappa ogni `tipo_configurazione` a una categoria e una tabella di etichette/formattatori per campo:

| Categoria | `tipo_configurazione` incluse |
|---|---|
| Parametri di sistema | `parametri_sistema` |
| Regole di fine corsa | `regole_fine_corsa` |
| Zone | `zona_creata`, `zona_eliminata` |
| Tariffe | `tariffa_creata`, `tariffa_modificata` |
| Offerte | `offerta_creata`, `offerta_modificata`, `offerta_eliminata` |

Ogni campo ha un'etichetta leggibile e un formattatore (es. `penale_fuori_zona` → "Penale fuori zona" formattato in `€`; `sconto_percentuale` → "Sconto" formattato in `%`; `costo_al_minuto` → "Costo al minuto" in `€/min`). Campi non mappati vengono mostrati con il nome originale come fallback, non bloccano il rendering.

**Layout — accordion:**
- Una card per categoria, con titolo e contatore (es. "Tariffe (3)"); le categorie senza voci non vengono mostrate.
- Click sull'header espande/collassa; solo una categoria aperta alla volta (stato `categoriaAperta: string | null`).
- Dentro la categoria espansa: lista delle voci (già ordinate newest-first dal backend) con data, descrizione, e righe diff nel formato `Etichetta: prima → dopo` (per creazione/eliminazione si omette la freccia, mostrando solo il valore presente).

**CSS (`VistaStoricoModifiche.css`):** nuove classi per l'header di sezione (cursor pointer, chevron), il contatore badge, e le righe diff (`<etichetta>: <prima> → <dopo>` con "prima" in rosso e "dopo" in verde, mantenendo la palette esistente).

### `StoricoModificheService.ts`

Nessuna modifica: l'interfaccia `StoricoModifica` resta identica.

## Testing

- Backend: test in `backend/tests/test_storico_modifiche.py` (o nuovo file) che verificano la registrazione per `crea_tariffa`, `aggiorna_tariffa`, `crea_offerta`, `modifica_offerta`, `elimina_offerta` — scenario base per ciascuno.
- Frontend: nessun test automatico esistente per questa vista; verifica manuale nel browser con dati di test (creare/modificare una tariffa e un'offerta, controllare che compaiano nella sezione corretta con diff corretto).
