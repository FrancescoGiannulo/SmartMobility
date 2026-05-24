# Dashboard Amministrazione Pubblica — Design Spec

**Data:** 2026-05-24
**Items:** IF-AP.03 (Visualizza Mappa AP), IF-AP.01 (Accede Report)
**Branch:** feature/mappa-zone

---

## 1. Obiettivo

Implementare la dashboard dell'Amministrazione Pubblica con due schermate:
1. **Mappa AP** — read-only, mostra tutti i mezzi della flotta e le zone attive
2. **Report AP** — grafico a barre settimanale + torta per tipologia di mezzo + export CSV/PDF

---

## 2. Architettura

### Backend

Nuovo file `backend/controllers/ap_controller.py` con due endpoint read-only:

| Metodo | Path | Ruolo | BLL |
|---|---|---|---|
| GET | `/ap/mappa/mezzi` | AP | `ServizioGIS.ottieni_mezzi_operatore()` |
| GET | `/ap/mappa/zone` | AP | `ServizioGIS.ottieni_zone()` |

- Gli schemi di risposta riusano `MezzoMappaOut` e `ZonaOut` già definiti in `controllers/schemas.py`
- `main.py` registra il nuovo router `ap_router`
- Nessuna modifica a BLL o DAL — la logica esiste già in `ServizioGIS`

### Frontend

```
frontend/src/views/amministrazione/
├── VistaDashboardAP.tsx     — schermata mappa (default) + navigazione a report
├── VistaDashboardAP.css
├── VistaReportAP.tsx        — schermata report intera
├── VistaReportAP.css
└── datiReportMock.ts        — dati mock sostituibili con API call in futuro
```

`MapService.ts` — aggiunge `getMezziAP()` e `getZoneAP()`

`App.tsx` — sostituisce `PlaceholderView` con `VistaDashboardAP` alla route `/ap/dashboard`

---

## 3. Comportamento

### VistaDashboardAP

- Layout split 70/30 identico a `VistaMappaOperatore`
- Sinistra (70%): mappa Google Maps read-only, pin mezzi con opacità per stato, poligoni zone colorati per tipo
- Destra (30%): logo SMART MOBILITY + un solo pulsante "VISUALIZZA REPORT" → setta stato interno `vista = 'report'`
- Nessun Drawing Manager, nessun pulsante di modifica zona
- I dati mappa vengono caricati da `GET /ap/mappa/mezzi` e `GET /ap/mappa/zone`

### VistaReportAP

- Schermata intera (sostituisce la mappa quando `vista === 'report'`)
- Pulsante "← Indietro" in alto → setta `vista = 'mappa'`
- **Grafico a barre** (Recharts `BarChart`): corse per giorno della settimana (Lun–Dom), barre impilate per tipologia (monopattino verde, bicicletta blu, automobile magenta)
- **Grafico a torta** (Recharts `PieChart`): quota percentuale per tipologia con etichette
- **ESPORTA CSV**: genera e scarica un file `.csv` con i dati mock
- **ESPORTA PDF**: `window.print()` con CSS `@media print` che nasconde la topbar e mostra solo i grafici

### Dati mock (`datiReportMock.ts`)

```typescript
export const DATI_SETTIMANALI = [
  { giorno: 'Lun', monopattino: 42, bicicletta: 18, automobile: 12 },
  { giorno: 'Mar', monopattino: 38, bicicletta: 22, automobile: 10 },
  { giorno: 'Mer', monopattino: 35, bicicletta: 20, automobile: 14 },
  { giorno: 'Gio', monopattino: 28, bicicletta: 15, automobile: 8  },
  { giorno: 'Ven', monopattino: 20, bicicletta: 12, automobile: 6  },
  { giorno: 'Sab', monopattino: 15, bicicletta: 10, automobile: 5  },
  { giorno: 'Dom', monopattino: 10, bicicletta: 8,  automobile: 4  },
]

export const DATI_TORTA = [
  { name: 'Monopattino', value: 70.9 },
  { name: 'Bicicletta',  value: 13.3 },
  { name: 'Automobile',  value: 15.8 },
]
```

---

## 4. Testing

Nuovo file `backend/tests/test_ap.py` con 3 test (unit, no integration):

| Test | Atteso |
|---|---|
| `GET /ap/mappa/mezzi` con token AP valido | 200 + lista |
| `GET /ap/mappa/mezzi` senza token | 401 |
| `GET /ap/mappa/mezzi` con token UT | 403 |

---

## 5. File coinvolti

| File | Azione |
|---|---|
| `backend/controllers/ap_controller.py` | Crea |
| `backend/main.py` | Modifica — aggiunge `ap_router` |
| `backend/tests/test_ap.py` | Crea |
| `frontend/src/services/MapService.ts` | Modifica — aggiunge `getMezziAP`, `getZoneAP` |
| `frontend/src/views/amministrazione/VistaDashboardAP.tsx` | Crea |
| `frontend/src/views/amministrazione/VistaDashboardAP.css` | Crea |
| `frontend/src/views/amministrazione/VistaReportAP.tsx` | Crea |
| `frontend/src/views/amministrazione/VistaReportAP.css` | Crea |
| `frontend/src/views/amministrazione/datiReportMock.ts` | Crea |
| `frontend/src/App.tsx` | Modifica — collega `/ap/dashboard` |

---

## 6. Vincoli

- AP non definisce zone (rimosso in questo sprint)
- Dati report sono mock per Sprint 1; il contratto del componente `VistaReportAP` è disegnato per accettare i dati come props, così la sostituzione con dati reali richiede solo di cambiare il chiamante
- Nessuna nuova libreria backend
- Recharts è l'unica nuova dipendenza frontend
