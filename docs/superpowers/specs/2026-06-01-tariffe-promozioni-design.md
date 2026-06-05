# Design Spec: IF-UT.05 Consulta Tariffe + IF-UT.13 Visualizza Promozioni

**Data**: 2026-06-01  
**Sprint**: Sprint 1  
**Autore**: Francesco Giannulo  
**Item backlog**: IF-UT.05, IF-UT.13  
**Diagrammi di sequenza**: `TestDrawIOClaude/output/francesco/sequence_consulta_tariffe.drawio`, `sequence_visualizza_promozioni.drawio`

---

## 1. Contesto

Due user story dello Sprint 1 richiedono che l'utente finale (UT) possa consultare le tariffe del servizio e le promozioni attive direttamente dalla homepage (VistaMappa). Entrambe le funzionalità sono read-only lato utente: i dati vengono creati dall'operatore tramite IF-OP.06/07 (non ancora implementati).

---

## 2. Diagrammi di sequenza — riepilogo

### IF-UT.05 Consulta Tariffe

```
UT → VistaHomepageUtente: consultaTariffe()
VistaHomepageUtente → ApiService: getTariffe()
ApiService → PagamentoController: GET /tariffe
  alt [tariffe definite]
    PagamentoController → ServizioPricing: getTariffe()
    ServizioPricing → TariffaRepository: findAll()
    TariffaRepository → ServizioPricing: :Tariffa[]
    ServizioPricing → PagamentoController: :tariffe
    PagamentoController → ApiService: 200 OK {tariffe[]}
    ApiService → VistaHomepageUtente: renderTariffe(tariffe[])
    VistaHomepageUtente → UT: mostraTariffe()
  alt [TariffeNonDefinite]
    PagamentoController → ApiService: 404 Not Found
    ApiService → VistaHomepageUtente: :errore
    VistaHomepageUtente → UT: mostraErrore("Nessuna tariffa disponibile.")
```

### IF-UT.13 Visualizza Promozioni

```
UT → VistaHomepageUtente: consultaPromozioni()
VistaHomepageUtente → ApiService: getPromozioni()
ApiService → PagamentoController: GET /promozioni
  alt [promozioni attive]
    PagamentoController → ServizioPricing: getPromozioniAttive()
    ServizioPricing → VistaHomepageUtente (via chain): :promozioni[]
    PagamentoController → ApiService: 200 OK {promozioni[]}
    ApiService → VistaHomepageUtente: renderPromozioni(promozioni[])
    VistaHomepageUtente → UT: mostraPromozioni()
  alt [NessunPromozioneAttiva]
    PagamentoController → ApiService: 204 No Content
    ApiService → VistaHomepageUtente: :empty
    VistaHomepageUtente → UT: mostraMessaggio("Nessuna promozione attiva al momento.")
```

---

## 3. Architettura — layer per layer

### 3.1 Database

**Tabella `tariffe`** — già presente in `001_init_schema.sql`. Nessuna modifica.

**Nuova tabella `promozioni`** — da aggiungere in una nuova migrazione `002_promozioni.sql`:

```sql
CREATE TABLE promozioni (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titolo              TEXT NOT NULL,
    descrizione         TEXT,
    sconto_percentuale  NUMERIC(5,2) NOT NULL CHECK (sconto_percentuale > 0 AND sconto_percentuale <= 100),
    data_inizio         TIMESTAMPTZ NOT NULL DEFAULT now(),
    data_fine           TIMESTAMPTZ NOT NULL,
    attiva              BOOLEAN NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3.2 Model (ORM SQLAlchemy 2.0)

**File**: `backend/model/promozione.py`

```python
class Promozione(Base):
    __tablename__ = "promozioni"
    __table_args__ = (
        CheckConstraint("sconto_percentuale > 0 AND sconto_percentuale <= 100", ...),
        CheckConstraint("data_fine > data_inizio", ...),
    )
    id: Mapped[UUID]
    titolo: Mapped[str]
    descrizione: Mapped[str | None]
    sconto_percentuale: Mapped[Decimal]
    data_inizio: Mapped[datetime]
    data_fine: Mapped[datetime]
    attiva: Mapped[bool]
    created_at: Mapped[datetime]
```

`backend/model/tariffa.py` — già presente, nessuna modifica.

### 3.3 DAL

**File**: `backend/dal/tariffa_repository.py` (nuovo)

```python
class TariffaRepository:
    def findAll(self, db: Session) -> list[Tariffa]: ...
```

**File**: `backend/dal/promozione_repository.py` (nuovo)

```python
class PromozioneRepository:
    def getAttive(self, db: Session) -> list[Promozione]:
        # WHERE attiva = true AND data_fine >= now()
```

### 3.4 BLL

**File**: `backend/bll/servizio_pricing.py` (attualmente vuoto — da completare)

```python
class ServizioPricing:
    def getTariffe(self, db: Session) -> list[Tariffa]: ...
    def getPromozioniAttive(self, db: Session) -> list[Promozione]: ...
```

### 3.5 Controller

**File**: `backend/controllers/pricing_controller.py` (nuovo)  
**Prefix**: nessuno (per rispettare i path `/tariffe` e `/promozioni` del diagramma)

```python
GET /tariffe
  → ServizioPricing.getTariffe()
  → 200 OK [TariffaOut] se lista non vuota
  → 404 se lista vuota

GET /promozioni
  → ServizioPricing.getPromozioniAttive()
  → 200 OK [PromozioneOut] se lista non vuota
  → 204 No Content se lista vuota
```

**Auth**: endpoint pubblici — l'utente deve essere autenticato ma non serve controllo ruolo specifico (l'auth middleware JWT già in place protegge le route).

### 3.6 Schemas Pydantic

Da aggiungere in `backend/controllers/schemas.py`:

```python
class TariffaOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    costo_al_minuto: Decimal
    costo_al_km: Decimal

class PromozioneOut(BaseModel):
    id: UUID
    titolo: str
    descrizione: str | None
    sconto_percentuale: Decimal
    data_fine: datetime
```

### 3.7 Registrazione router

`backend/main.py`: aggiungere `app.include_router(pricing_router)`.

---

## 4. Frontend

### 4.1 Service

**File**: `frontend/src/services/PaymentService.ts` — aggiungere:

```ts
export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number
  costo_al_km: number
}

export interface Promozione {
  id: string
  titolo: string
  descrizione: string | null
  sconto_percentuale: number
  data_fine: string
}

// [IF-UT.05] Consulta Tariffe
export const getTariffe = () => api.get<Tariffa[]>('/tariffe')

// [IF-UT.13] Visualizza Promozioni
export const getPromozioni = () => api.get<Promozione[]>('/promozioni')
```

### 4.2 VistaMappa — integrazione drawer

**File**: `frontend/src/views/utente/VistaMappa.tsx`

Aggiunte:
1. Stato: `drawerAperto: 'tariffe' | 'promozioni' | null`
2. Stato dati (lazy): `tariffe: Tariffa[] | null`, `promozioni: Promozione[] | null`, `loadingDrawer: boolean`
3. Due bottoni flottanti in bottom-left (sopra i controlli mappa esistenti)
4. Al primo click su "Tariffe": fetch `getTariffe()` → popola `tariffe`, apre drawer
5. Al primo click su "Promo": fetch `getPromozioni()` → popola `promozioni`, apre drawer
6. Re-fetch solo se il dato non è già in cache locale (evita chiamate ripetute)

**Componente drawer** (inline nel file o in `frontend/src/components/DrawerPricing.tsx`):
- Overlay semitrasparente sul lato sinistro della mappa
- Header con titolo + pulsante chiudi (×)
- Contenuto: lista card per ogni tariffa/promozione
- Per tariffe vuote: testo "Nessuna tariffa disponibile."
- Per promozioni vuote: testo "Nessuna promozione attiva al momento."

**CSS**: stile coerente con VistaMappa.css (colore brand `#4caf9a`, border-radius 12px, sfondo `rgba(255,255,255,0.97)`)

---

## 5. Test

**File**: `backend/tests/test_pricing.py` (nuovo)

| Test | Scenario | Atteso |
|------|----------|--------|
| `test_get_tariffe_con_dati` | DB con 1+ righe in `tariffe` | 200, lista non vuota |
| `test_get_tariffe_vuote` | DB senza righe in `tariffe` | 404 |
| `test_get_promozioni_attive` | Promozione con `attiva=True`, `data_fine` futura | 200, lista |
| `test_get_promozioni_nessuna_attiva` | Nessuna promozione attiva | 204 |
| `test_get_promozioni_scaduta_esclusa` | Promozione con `data_fine` passata | 204 (non inclusa) |

Tutti i test sono unit test (nessun DB reale): `ServizioPricing` mockato nel controller test; `TariffaRepository` e `PromozioneRepository` mockati nel BLL test.

---

## 6. File da creare/modificare

### Nuovi file
- `backend/migrations/002_promozioni.sql`
- `backend/model/promozione.py`
- `backend/dal/tariffa_repository.py`
- `backend/dal/promozione_repository.py`
- `backend/controllers/pricing_controller.py`
- `backend/tests/test_pricing.py`
- (opzionale) `frontend/src/components/DrawerPricing.tsx`

### File modificati
- `backend/bll/servizio_pricing.py` — implementazione metodi
- `backend/controllers/schemas.py` — aggiunta TariffaOut, PromozioneOut
- `backend/main.py` — registrazione pricing_router
- `frontend/src/services/PaymentService.ts` — aggiunta getTariffe, getPromozioni
- `frontend/src/views/utente/VistaMappa.tsx` — drawer tariffe/promozioni
- `frontend/src/views/utente/VistaMappa.css` — stile drawer

---

## 7. Decisioni di design

- **`GET /tariffe` restituisce 404 (non 200 con lista vuota)**: il diagramma di sequenza specifica esplicitamente `404 Not Found` per il caso `[TariffeNonDefinite]`.
- **`GET /promozioni` restituisce 204 (non 404)**: il diagramma specifica `204 No Content` per il caso `[NessunPromozioneAttiva]` — semanticamente corretto perché la risorsa esiste ma è vuota.
- **Fetch lazy nel frontend**: i dati di tariffe/promozioni non vengono caricati al mount della mappa per non rallentare il rendering iniziale.
- **`VistaHomepageUtente` nel diagramma = `VistaMappa`**: confermato dall'utente — nessuna nuova route.
- **Promozioni senza FK a operatore**: IF-OP.06 non è ancora implementato; la tabella è autosufficiente, l'FK `operatore_id` verrà aggiunta quando IF-OP.06 sarà in scope.
