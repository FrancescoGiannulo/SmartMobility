# Design: feature/mappa-zone

**Data:** 2026-05-23
**Sprint:** 1
**Branch:** feature/mappa-zone
**Riferimento:** Sprint1_definitivo.md

---

## Scope

Item del Sprint 1 backlog coperti da questo branch:

| ID | Caso d'uso | Descrizione |
|---|---|---|
| UT.01 | CS-01 | Visualizza Mappa Utente |
| OP.01 | CS-02 | Visualizza Mappa Operatore |
| OP.03 | CS-03 | Definisce Confine Operativo |
| OP.15 | CS-03 | Definisce Zone Vietate |
| OP.16 | CS-03 | Definisce Zone Parcheggio |

Non in scope: AP.03 (non nel backlog Sprint 1), prenotazione, sblocco, stato mezzo, tariffe, pagamenti (altri branch).

---

## Tecnologie

- **Mappa:** Google Maps via `@vis.gl/react-google-maps`
- **Disegno zone:** Google Maps Drawing Manager (nativo, nessuna dipendenza extra)
- **Geometrie DB:** PostGIS / GeoAlchemy2 (`POLYGON`, SRID 4326)
- **API Key:** `VITE_GOOGLE_MAPS_API_KEY` in `frontend/.env.local`

---

## Backend

### Endpoint

| Metodo | Path | Controller | Auth | Descrizione |
|---|---|---|---|---|
| GET | `/utente/mappa/mezzi` | `utente_controller.py` | UT | Solo mezzi Disponibili con lat/lng/tipo/batteria |
| GET | `/utente/mappa/zone` | `utente_controller.py` | UT | Zone attive serializzate in GeoJSON |
| GET | `/operatore/mappa/mezzi` | `mezzo_operatore_controller.py` | OP | Tutti i mezzi con stato/lat/lng/tipo/batteria |
| GET | `/operatore/zone` | `zona_operatore_controller.py` | OP | Lista zone esistenti |
| POST | `/operatore/zone` | `zona_operatore_controller.py` | OP | Crea zona (tipo + GeoJSON + nome + limite_velocita?) |
| DELETE | `/operatore/zone/{id}` | `zona_operatore_controller.py` | OP | Elimina zona |

Nessun controller nuovo — tutti gli endpoint vanno nei controller esistenti (approccio B).

### Layer

**DAL — `ZonaRepository`:**
- `lista_zone(solo_attive: bool)` → lista `Zona`
- `trova_per_id(id)` → `Zona`
- `crea(nome, tipo, coordinate, limite_velocita)` → `Zona`
- `elimina(id)` → None

**BLL — `ServizioGIS`:**
- `ottieni_zone_per_mappa()` → lista zone serializzate GeoJSON
- `crea_zona(nome, tipo, coordinate, limite_velocita)` → valida poligono (≥3 vertici, no auto-intersezioni), chiama repository
- `elimina_zona(id)` → chiama repository
- `punto_in_zona(lat, lng, tipo)` → bool (usato da altri branch per fine corsa)

**Serializzazione perimetro:** `geoalchemy2.functions.ST_AsGeoJSON` → stringa JSON → `json.loads()`.

### Schemi Pydantic (schemas.py)

```python
class ZonaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str  # "operativa" | "parcheggio" | "limitata" | "vietata"
    perimetro: dict  # GeoJSON Polygon
    limite_velocita: int | None
    attiva: bool

class ZonaCreate(BaseModel):
    nome: str
    tipo: str
    coordinate: list[list[float]]  # [[lng, lat], ...]
    limite_velocita: int | None = None

class MezzoMappaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float | None
    lng: float | None
    batteria: int | None
```

---

## Frontend

### Servizi

**`MapService.ts`** — letture:
- `getMezziUtente()` → `GET /utente/mappa/mezzi`
- `getMezziOperatore()` → `GET /operatore/mappa/mezzi`
- `getZone()` → `GET /utente/mappa/zone` (usato da UT e OP)
- `getZoneOperatore()` → `GET /operatore/zone`

**`ZonaService.ts`** — scritture:
- `creaZona(dati: ZonaCreate)` → `POST /operatore/zone`
- `eliminaZona(id: string)` → `DELETE /operatore/zone/{id}`

### Viste

**`views/utente/VistaMappa.tsx`** (CS-01 / IUI-2):
- Mappa fullscreen con `APIProvider` + `Map`
- Pin per ogni mezzo disponibile: colore per tipo (monopattino verde, bici blu, auto magenta)
- Poligoni zone sovrapposti: vietata rosso, limitata arancione, parcheggio verde, operativa blu
- Marker posizione utente (geolocation API)
- Bottom sheet al click su pin mezzo (placeholder — implementato in feature/corsa)

**`views/operatore/VistaMappaOperatore.tsx`** (CS-02 + CS-03 / IUI-16):
- Layout split 70/30: mappa a sinistra, pannello controlli a destra
- Mappa: tutti i mezzi con stato, zone esistenti
- Pannello destra: 6 bottoni pill (GESTISCI SEGNALAZIONI, GESTISCI UTENTI, IMPOSTAZIONI REGOLE, TARIFFE E PROMOZIONI, VISUALIZZA REPORT, GESTISCI MEZZI) — i bottoni non-mappa sono placeholder per altri branch
- Bottoni "DEFINISCI ZONA" aprono modal con selezione tipo → attiva DrawingManager
- Al completamento del poligono: modal conferma con nome zona → `creaZona()`
- Zone disegnate appaiono sulla mappa con il colore semantico

### Colori zona

| Tipo | Colore fill | Colore bordo |
|---|---|---|
| vietata | `#f44336` (rosso, 30% opacity) | `#f44336` |
| limitata | `#ff9800` (arancione, 30% opacity) | `#ff9800` |
| parcheggio | `#4caf50` (verde, 30% opacity) | `#4caf50` |
| operativa | `#2196f3` (blu, 30% opacity) | `#2196f3` |

---

## Gestione errori

| Scenario | Comportamento |
|---|---|
| Mezzo senza lat/lng | Escluso dalla risposta backend (WHERE lat IS NOT NULL) |
| Poligono < 3 vertici | Backend 422, frontend messaggio "Disegna almeno 3 vertici" |
| Utente nega geolocalizzazione | Mappa centrata su coordinate fisse Zootropolis, nessun marker |
| Nessun mezzo disponibile | Mappa vuota con testo "Nessun mezzo disponibile" |
| Errore di rete | Toast errore, mappa visibile con dati precedenti |

---

## Test backend

| Test | Input | Atteso |
|---|---|---|
| `test_visualizza_mappa_utente` | GET `/utente/mappa/mezzi` autenticato UT | Solo mezzi Disponibili |
| `test_visualizza_mappa_operatore` | GET `/operatore/mappa/mezzi` autenticato OP | Tutti i mezzi |
| `test_crea_zona_valida` | POST zona con 4 vertici | 201 + zona in DB |
| `test_crea_zona_vertici_insufficienti` | POST zona con 2 vertici | 422 |
| `test_lista_zone` | GET `/operatore/zone` | Lista zone attive |
| `test_elimina_zona` | DELETE `/operatore/zone/{id}` | 204 |

---

## Utenti di test

| Ruolo | Email | Password |
|---|---|---|
| OP | `operatore@smartmobility.test` | `Operatore123!` |
| AP | `admin@smartmobility.test` | `Admin123!` |

Script di seed: `backend/scripts/seed_test_users.py`
