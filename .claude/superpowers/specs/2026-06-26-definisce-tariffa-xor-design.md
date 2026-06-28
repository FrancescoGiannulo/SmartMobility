# Design: OP-05 Definisce Tariffa — scelta minuto/km e validazione duplicato

Data: 2026-06-26

## Contesto

Caso d'uso `OP-05` ("Definisce Tariffa"): l'operatore deve poter scegliere, per ogni
tipologia di mezzo, **se** la tariffa è a costo al minuto **oppure** a costo al
chilometro (non entrambi), e inserire un solo valore. Se la tipologia ha già una
tariffa attiva, il sistema deve rifiutare la creazione e invitare l'operatore a usare
la modifica (scenario alternativo `OP-05.1`).

Il diagramma delle classi (`docs/Diagrammi/DiagrammaClassi.md`, fonte di verità) per
`Tariffa` specifica già:

```
- costoPerMinuto: float?
- costoPerKm: float?
Vincolo: esattamente uno tra costoPerMinuto e costoPerKm è non-null
```

L'implementazione attuale diverge da questo vincolo: `model/tariffa.py` ha entrambi i
campi `NOT NULL` e il form frontend richiede sempre entrambi i valori. Inoltre il
dropdown "tipo mezzo" nel form di creazione filtra via i tipi già tariffati, invece di
mostrarli sempre e far emergere l'errore OP-05.1 alla validazione.

## Modifiche Backend

### Migrazione `backend/migrations/021_tariffa_xor_costo.sql`
- `ALTER COLUMN costo_al_minuto DROP NOT NULL`, `ALTER COLUMN costo_al_km DROP NOT NULL`.
- `UPDATE tariffe SET costo_al_km = NULL` (le righe esistenti mantengono solo
  `costo_al_minuto`, dato che non c'è traffico di produzione da preservare su entrambi
  i valori).
- Drop dei due `CHECK` esistenti (`tariffa_costo_minuto_positivo`,
  `tariffa_costo_km_positivo`), creazione di un unico `CHECK` XOR:
  `(costo_al_minuto IS NOT NULL AND costo_al_km IS NULL AND costo_al_minuto > 0)
   OR (costo_al_km IS NOT NULL AND costo_al_minuto IS NULL AND costo_al_km > 0)`.

### `backend/model/tariffa.py`
- `costo_al_minuto`, `costo_al_km`: `Mapped[Decimal | None]`, nullable.
- `__table_args__`: sostituire i due check positivi con il check XOR sopra.

### `backend/controllers/schemas.py`
- `CreaTariffaRequest`: `costo_al_minuto: float | None = None`,
  `costo_al_km: float | None = None`. Validator Pydantic (`model_validator`) che
  impone: esattamente uno dei due è non-None ed è `> 0`, l'altro è `None` (o assente).
  Se violato → `422`.
- `TariffaResponse`: stessi campi opzionali.

### `backend/dal/tariffa_repository.py`
- `crea`, `aggiorna`, `findAll`, `find_all`: propagare `None` invece di forzare
  `Decimal` su entrambi i campi.

### `backend/bll/servizio_tariffa.py`
- Nessuna modifica alla logica di `exists_by_tipologia` (il check duplicato OP-05.1 è
  già corretto: una riga per `tipo_mezzo`, vincolo `UNIQUE` già presente).
- `crea_tariffa`/`aggiorna_tariffa`: passare `None` quando il campo non è impostato,
  aggiornare i dict di ritorno e i messaggi di storico modifiche per non assumere
  entrambi i valori popolati.

### `backend/bll/servizio_pricing.py`
- `calcola_importo`: cambiare
  `durata_min * costo_al_minuto + distanza_km * costo_al_km`
  in
  `durata_min * (costo_al_minuto or 0) + distanza_km * (costo_al_km or 0)`
  per gestire il campo nullo senza eccezioni.

### Non toccare
- `backend/migrations/003_seed_tariffe.sql` resta storica e invariata; la 021 corregge
  i dati a runtime (non si riscrive la storia delle migrazioni già applicate).

## Modifiche Frontend (`frontend/src/views/operatore/VistaTariffe.tsx`)

1. **Form di creazione/modifica**:
   - Nuovo campo "Tipo di tariffa" — due radio button: *Costo al minuto* / *Costo al
     km*.
   - Un solo input numerico per il valore, con label/placeholder che cambia in base
     al tipo selezionato (es. "es. 0.15" per minuto, "es. 0.20" per km).
   - Rimuovere i due input sempre visibili (`costo_al_minuto` + `costo_al_km`
     contemporaneamente).
2. **Tipo mezzo**: il dropdown nel form di creazione mostra sempre tutte le 3
   tipologie (`TIPI_MEZZO`), non più filtrato da `tipiDisponibili`. Il pulsante
   "+ Nuova tariffa" è sempre abilitato (rimuovere `disabled={tipiDisponibili.length
   === 0}`).
3. **Validazione duplicato lato client**: quando l'operatore seleziona, nel form di
   creazione, un tipo mezzo già presente in `tariffe`, mostrare subito il messaggio
   inline "Tariffa già esistente per questa tipologia. Usa Modifica tariffa." e
   disabilitare "Salva tariffa". Il controllo sull'esito HTTP `409` resta come
   fallback di sicurezza (race condition con un altro operatore).
4. **Modifica esistente**: precompilare il radio in base a quale dei due campi è
   popolato nella tariffa (`costo_al_minuto != null` → minuto, altrimenti km) e il
   valore nel campo unico. L'operatore può cambiare il tipo di costo anche in
   modifica (passare da minuto a km o viceversa).
5. **Lista tariffe**: la card mostra solo il valore impostato — `€0.05/min` oppure
   `€0.15/km` — non più sempre entrambi.

### `frontend/src/services/TariffaService.ts`
- `creaTariffa`/`aggiornaTariffa`: firma aggiornata per accettare un solo valore di
  costo più il tipo (es. `creaTariffa(tipoMezzo, tipoTariffa: 'minuto' | 'km', valore:
  number)`), che internamente costruisce il payload con l'altro campo a `undefined`.

## Test

- Backend (pytest):
  - `crea_tariffa` con solo `costo_al_minuto` → successo, `costo_al_km` è `None` nella
    risposta.
  - `crea_tariffa` con entrambi i campi popolati → `422`.
  - `crea_tariffa` con nessun campo popolato → `422`.
  - `crea_tariffa` su tipo mezzo già tariffato → `TariffaGiaEsistente` / `409`
    (scenario OP-05.1, test già esistente da verificare).
  - `calcola_importo` con tariffa solo a minuto e tariffa solo a km → importo corretto
    in entrambi i casi.
- Aggiornare i test esistenti su `servizio_tariffa`/`servizio_pricing` che assumevano
  entrambi i campi sempre popolati.

## Documentazione
- Aggiornare `docs/Sprintn3.md` (caso d'uso OP-05) se necessario per riflettere il
  flusso form aggiornato (probabilmente già coerente, da verificare in fase di
  implementazione).
