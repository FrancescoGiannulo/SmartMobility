# Schema Logico DB — Smart Mobility Sprint 1

**Data:** 2026-05-21  
**Sprint:** Sprint 1  
**Ambito:** Solo item Sprint 1 (23 item)  
**DB:** Supabase (PostgreSQL) con PostGIS e Row Level Security

---

## Decisioni architetturali

| Decisione | Scelta | Motivazione |
|-----------|--------|-------------|
| Ruoli utente | 3 tabelle separate (`utenti`, `operatori`, `amministratori`) collegate a `auth.users` | Strutture dati diverse per ogni ruolo; nessuna colonna inutilizzata |
| Geometria zone | PostGIS `GEOMETRY(POLYGON, 4326)` | Query spaziali native (`ST_Contains`, `ST_Intersects`) necessarie per ServizioGIS; già disponibile su Supabase free |
| Operatori | Singolo operatore | Zootropolis ha un unico gestore del servizio |
| Prenotazione ↔ Corsa | Tabelle separate con FK nullable su `corse.prenotazione_id` | CS-10 permette sblocco diretto senza prenotazione attiva |
| Scope | Solo Sprint 1 | Evita over-engineering; schema si estende sprint per sprint |

---

## Enum PostgreSQL

```sql
CREATE TYPE tipo_mezzo AS ENUM ('monopattino', 'bicicletta', 'automobile');

CREATE TYPE stato_mezzo AS ENUM (
    'Disponibile', 'Prenotato', 'In uso', 'In pausa',
    'In manutenzione', 'Fuori servizio', 'Dismesso'
);

CREATE TYPE tipo_zona AS ENUM ('operativa', 'parcheggio', 'limitata', 'vietata');

CREATE TYPE stato_prenotazione AS ENUM ('attiva', 'scaduta', 'annullata', 'convertita');

CREATE TYPE stato_corsa AS ENUM ('in_uso', 'in_pausa', 'terminata');

CREATE TYPE stato_pagamento AS ENUM ('completato', 'rifiutato', 'in_attesa');

CREATE TYPE tipo_metodo_pagamento AS ENUM ('google_pay', 'apple_pay', 'paypal', 'carta');

CREATE TYPE tipo_vincolo_fine_corsa AS ENUM ('penale', 'divieto', 'avviso');
```

---

## Tabelle

### 1. `utenti` — IF-UT.17/18/19

Profilo dell'utente finale, collegato a `auth.users`.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, FK → auth.users.id | Stesso ID di Supabase Auth |
| `nome` | TEXT | NOT NULL | |
| `cognome` | TEXT | NOT NULL | |
| `telefono` | TEXT | nullable | |
| `sospeso` | BOOLEAN | DEFAULT false | IF-OP.05 — sospensione account |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 2. `operatori` — IF-OP.16

Profilo dell'operatore del servizio. Include i parametri di configurazione del servizio (IUI-19).

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, FK → auth.users.id | |
| `nome` | TEXT | NOT NULL | |
| `durata_max_prenotazione_min` | INTEGER | DEFAULT 15 | IF-OP.09 |
| `durata_periodo_grazia_min` | INTEGER | DEFAULT 5 | IF-OP.10 |
| `max_mezzi_per_utente` | INTEGER | DEFAULT 1 | IF-OP.11 |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 3. `amministratori` — IF-AP.07

Profilo dell'amministrazione pubblica.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, FK → auth.users.id | |
| `nome` | TEXT | NOT NULL | |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 4. `mezzi` — IF-OP.04/12/13

Flotta dei mezzi di sharing.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `codice` | TEXT | UNIQUE NOT NULL | Identificativo fisico del mezzo |
| `tipo` | tipo_mezzo | NOT NULL | |
| `stato` | stato_mezzo | DEFAULT 'Disponibile' | Modificabile solo via ServizioMobilità |
| `lat` | DOUBLE PRECISION | nullable | Posizione corrente |
| `lng` | DOUBLE PRECISION | nullable | Posizione corrente |
| `batteria` | INTEGER | nullable, CHECK 0–100 | Nullable per bici meccanica senza batteria |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 5. `zone` — IF-AP.02/03/04, IF-OP.03

Zone geografiche. AP crea `vietata`, `limitata`, `parcheggio`; OP crea `operativa`.

**Ownership zone (Sprint 1):** tutte le zone (`operativa`, `vietata`, `parcheggio`, `limitata`) sono create dall'Operatore tramite `IF-OP.02`. La precedenza tra tipi è applicata in `ServizioGIS`, non tramite vincoli DB.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `nome` | TEXT | NOT NULL | |
| `tipo` | tipo_zona | NOT NULL | Tipo di zona: operativa / parcheggio / limitata / vietata |
| `perimetro` | GEOMETRY(POLYGON, 4326) | NOT NULL | PostGIS — WGS84 |
| `limite_velocita` | INTEGER | nullable | Solo per tipo='limitata' (IF-AP.04) |
| `attiva` | BOOLEAN | DEFAULT true | Per modifica/disattivazione zona |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 6. `tariffe` — IF-OP.07/08

Una riga per tipologia di mezzo. `UNIQUE` su `tipo_mezzo` rispetta la precondizione di CS-14.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `tipo_mezzo` | tipo_mezzo | UNIQUE NOT NULL | CS-14: NON può esistere già una tariffa per questo tipo |
| `costo_al_minuto` | NUMERIC(10,4) | NOT NULL, CHECK > 0 | |
| `costo_al_km` | NUMERIC(10,4) | NOT NULL, CHECK > 0 | |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |
| `aggiornata_at` | TIMESTAMPTZ | DEFAULT now() | Aggiornato da trigger o dalla BLL |

---

### 7. `prenotazioni` — IF-UT.02/03

Riserva temporanea di un mezzo. Lifecycle indipendente dalla corsa.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `utente_id` | UUID | NOT NULL, FK → utenti(id) | |
| `mezzo_id` | UUID | NOT NULL, FK → mezzi(id) | |
| `stato` | stato_prenotazione | DEFAULT 'attiva' | `convertita` quando genera una corsa |
| `scade_at` | TIMESTAMPTZ | NOT NULL | Calcolato da `durata_max_prenotazione_min` dell'operatore |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 8. `corse` — IF-UT.04/06/07

Sessione di utilizzo attivo di un mezzo. `prenotazione_id` è nullable: CS-10 permette sblocco diretto.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `utente_id` | UUID | NOT NULL, FK → utenti(id) | |
| `mezzo_id` | UUID | NOT NULL, FK → mezzi(id) | |
| `prenotazione_id` | UUID | nullable, FK → prenotazioni(id) | Approccio A: FK opzionale |
| `stato` | stato_corsa | DEFAULT 'in_uso' | |
| `inizio_at` | TIMESTAMPTZ | NOT NULL | Momento sblocco |
| `fine_at` | TIMESTAMPTZ | nullable | Popolato al termine (CS-11) |
| `distanza_km` | NUMERIC(10,3) | nullable | Popolato al termine |
| `inizio_lat` | DOUBLE PRECISION | nullable | Posizione sblocco |
| `inizio_lng` | DOUBLE PRECISION | nullable | Posizione sblocco |
| `fine_lat` | DOUBLE PRECISION | nullable | Posizione chiusura |
| `fine_lng` | DOUBLE PRECISION | nullable | Posizione chiusura |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 9. `metodi_pagamento` — IF-UT.12/21

Metodi di pagamento salvati dall'utente. Nessun dato sensibile in chiaro: solo token del ProviderPagamenti.

**Invariante:** al massimo un metodo per utente ha `predefinito=true`. Applicato nella BLL (`ServizioPricing`), non tramite UNIQUE parziale.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `utente_id` | UUID | NOT NULL, FK → utenti(id) | |
| `tipo` | tipo_metodo_pagamento | NOT NULL | |
| `token_esterno` | TEXT | NOT NULL | Token mock del ProviderPagamenti |
| `last_four` | TEXT | nullable | Solo per tipo='carta' |
| `predefinito` | BOOLEAN | DEFAULT false | IF-UT.21 |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 10. `pagamenti` — IF-UT.20

Transazione di pagamento generata al termine di ogni corsa (CS-12).

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `corsa_id` | UUID | NOT NULL, FK → corse(id) | |
| `utente_id` | UUID | NOT NULL, FK → utenti(id) | Denormalizzato per query RLS |
| `metodo_pagamento_id` | UUID | nullable, FK → metodi_pagamento(id) | Nullable: CS-12.1 (pagamento rifiutato) |
| `importo` | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | |
| `stato` | stato_pagamento | DEFAULT 'in_attesa' | |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

### 11. `regole_fine_corsa` — IF-OP.14

Configurazione delle regole sanzionatorie per la chiusura corsa fuori dalle zone di parcheggio. Una riga per zona di parcheggio.

| Colonna | Tipo | Vincoli | Note |
|---------|------|---------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `zona_parcheggio_id` | UUID | NOT NULL, FK → zone(id) | La zona referenziata deve avere tipo='parcheggio' |
| `batteria_minima` | INTEGER | nullable, CHECK 0–100 | Soglia batteria per chiusura valida |
| `penale_fuori_zona` | NUMERIC(10,2) | DEFAULT 0.00 | Importo penale aggiuntivo |
| `tipo_vincolo` | tipo_vincolo_fine_corsa | DEFAULT 'avviso' | Da IUI-19: penale / divieto / avviso |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

---

## Diagramma relazioni (testuale)

```
auth.users ──< utenti
auth.users ──< operatori
auth.users ──< amministratori

utenti >── prenotazioni ──< mezzi
utenti >── corse ──< mezzi
corse >──o prenotazioni          (nullable — Approccio A)

utenti >── metodi_pagamento
corse >── pagamenti ──< metodi_pagamento (nullable)
utenti >── pagamenti

zone >── regole_fine_corsa       (solo zone tipo='parcheggio')
```

---

## Note implementative

- **PostGIS:** attivare con `CREATE EXTENSION IF NOT EXISTS postgis;` prima delle migrazioni.
- **Indice spaziale:** creare `CREATE INDEX ON zone USING GIST (perimetro);` per rendere efficienti le query `ST_Contains`/`ST_Intersects` usate da `ServizioGIS`.
- **RLS Supabase:** ogni tabella deve avere policy che limita l'accesso al ruolo corretto (UT/OP/AP) usando `auth.uid()` e join sulle tabelle di profilo.
- **Stato mezzo:** qualsiasi UPDATE su `mezzi.stato` deve passare per `ServizioMobilità` — mai aggiornare direttamente da Controller o DAL.
- **Priorità zone AP:** `ServizioGIS` applica la precedenza `vietata > limitata > operativa` a runtime, non tramite vincoli DB.
- **Predefinito pagamento:** CS-13 specifica che se è il primo metodo salvato viene impostato automaticamente come predefinito — logica in `ServizioPricing`.
- **Vincolo zona parcheggio:** `regole_fine_corsa.zona_parcheggio_id` deve referenziare solo zone con `tipo='parcheggio'`. Non applicato tramite CHECK DB (richiederebbe una funzione SQL); applicato nella BLL (`ServizioMobilità`) prima del salvataggio.
