# Visualizza Storico Corse — Design Spec

**Use case:** IF-UT.14 / CS-11  
**Branch:** feature/corsa  

---

## Goal

Consentire all'utente autenticato di visualizzare l'elenco cronologico (più recente prima) di tutte le corse effettuate. Le corse di gruppo (più mezzi sbloccati insieme) sono raggruppate visivamente con un badge e un popup di dettaglio per ciascun mezzo.

---

## Architettura

Segue il diagramma di sequenza `sequence_storico_corsa.drawio`:

```
VistaCorse → CorsaService → GET /utente/corse/storico
  → CorsaController → ServizioMobilità.get_storico()
    → CorsaRepository.find_by_utente_order_by_data()
```

Lo scenario alternativo **DatiNonDisponibili** (CS-11.1): qualsiasi eccezione nel repository viene propagata come 503, la vista mostra un banner con il messaggio "Storico non disponibile, riprovare" e un bottone "Riprova".

---

## Modifiche DB

### Migrazione `010_gruppo_corsa_id.sql`

```sql
ALTER TABLE corse ADD COLUMN gruppo_corsa_id UUID;
CREATE INDEX idx_corse_gruppo ON corse (gruppo_corsa_id)
    WHERE gruppo_corsa_id IS NOT NULL;
```

`gruppo_corsa_id` è nullable. Corse singole: `NULL`. Corse di gruppo: tutte condividono l'`id` della prima corsa creata nel batch di sblocco.

---

## Backend

### `CorsaRepository` — 2 modifiche

**`crea()` aggiornato:**
```python
def crea(self, utente_id, mezzo_id, prenotazione_id, gruppo_corsa_id=None) -> dict:
    # INSERT INTO corse (..., gruppo_corsa_id) VALUES (..., :gruppo_corsa_id)
```

**Nuovo metodo `find_by_utente_order_by_data()`:**
```python
def find_by_utente_order_by_data(self, utente_id: UUID) -> list[dict]:
    # SELECT c.id, c.inizio_at, c.fine_at, c.gruppo_corsa_id,
    #        m.tipo, m.codice
    # FROM corse c JOIN mezzi m ON c.mezzo_id = m.id
    # WHERE c.utente_id = :uid AND c.stato = 'terminata'
    # ORDER BY c.inizio_at DESC
```

Restituisce per ogni corsa: `id`, `tipo_mezzo`, `codice_mezzo`, `inizio_at`, `fine_at`, `durata_min` (calcolato in SQL come `EXTRACT(EPOCH FROM (fine_at - inizio_at))/60`, `NULL` se corsa ancora aperta), `distanza_km`, `gruppo_corsa_id`.

### `ServizioMobilità` — 2 modifiche

**`sblocca_mezzi()` aggiornato:**
- Se `len(mezzo_ids) > 1`: genera `gruppo_corsa_id = id della prima corsa creata`
- Passa `gruppo_corsa_id` a `CorsaRepository.crea()` per ogni mezzo

**Nuovo metodo `get_storico()`:**
```python
def get_storico(self, utente_id: UUID) -> list[dict]:
    return self._corsa_repo.find_by_utente_order_by_data(utente_id)
    # Eccezioni non catchate → propagate al controller → 503
```

### `prenotazione_utente_controller` — nuovo endpoint

```
GET /utente/corse/storico
Auth: verify_token(["UT"])
200 OK → List<CorsaStoricoOut>
503 → {"detail": "Storico non disponibile"}
```

**Schema risposta `CorsaStoricoOut`:**
```python
class CorsaStoricoOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    codice_mezzo: str
    inizio_at: datetime
    fine_at: datetime | None
    durata_min: float | None
    distanza_km: float | None
    gruppo_corsa_id: UUID | None
```

---

## Frontend

### `CorsaService.ts` — nuovo metodo

```typescript
export const getStoricoCorsa = () =>
  api.get<CorsaStorico[]>('/utente/corse/storico')

export interface CorsaStorico {
  id: string
  tipo_mezzo: string
  codice_mezzo: string
  inizio_at: string
  fine_at: string | null
  durata_min: number | null
  distanza_km: number | null
  gruppo_corsa_id: string | null
}
```

### `VistaCorse.tsx`

**Stati:** `loading` | `errore` | `vuoto` | `lista`

**Logica di raggruppamento (client-side):**
Le corse con lo stesso `gruppo_corsa_id` vengono aggregate in un'unica riga "gruppo". Ogni riga gruppo mostra:
- Badge "Gruppo (N mezzi)"
- Icone di tutti i mezzi coinvolti
- Data e durata della sessione (dalla prima corsa del gruppo)
- Cliccando → popup/modal con tabella dettagliata per ogni mezzo (codice, tipo, durata individuale, km)

**Corse singole** (`gruppo_corsa_id = null`): riga standard con icona mezzo, codice, durata, km, data.

**Scenario DatiNonDisponibili:** banner rosso con testo "Storico delle corse non disponibile al momento. Riprova più tardi." + bottone "Riprova" che richiama il fetch.

**Layout (IUI-9):** lista lineare con divisori orizzontali, header con bottone "← Indietro", icona mezzo a sinistra, dati a destra.

### `VistaCorse.css`

Stili per: lista con divisori, riga corsa, riga gruppo con badge, popup dettaglio gruppo, stati loading/errore/vuoto.

### `App.tsx`

```tsx
<Route path="/utente/storico" element={
  <RoutaProtetta ruoloRichiesto="UT">
    <VistaCorse />
  </RoutaProtetta>
} />
```

### `VistaMappa.tsx` — sidebar

Aggiunge voce "Cronologia" nel menu laterale che naviga a `/utente/storico`.

---

## Testing

- `GET /utente/corse/storico` con utente senza corse → `[]`
- `GET /utente/corse/storico` con corse singole → lista ordinata per data decrescente
- Sblocco di gruppo → le corse risultanti hanno lo stesso `gruppo_corsa_id`
- Errore DB → 503

---

## Out of scope

- Paginazione (non richiesta dalla specifica)
- Filtri per data o tipo mezzo
- Esportazione storico
