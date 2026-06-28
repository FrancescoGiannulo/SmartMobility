# Design: IF-AP.03 – Visualizza Mappa Amministrazione Pubblica

**Data:** 2026-06-03  
**ID backlog:** IF-AP.03  
**Sprint:** 1  
**Ruolo:** AP (Amministrazione Pubblica)

---

## Contesto

La dashboard dell'Amministrazione Pubblica (IUI-11) permette di monitorare il servizio di mobilità sul territorio. Il backend (`/ap/mappa/mezzi`, `/ap/mappa/zone`) è già implementato e testato (6/6 test verdi). Il frontend ha una base (`VistaDashboardAP.tsx`) con mappa, overlay zone e navigazione al report.

Questo design aggiunge:
1. **Layer filtering** — toggle per tipo mezzo con conteggio
2. **Vista mappa** — modalità Pin / Cluster / Heatmap
3. **KPI bar** — 4 counter live calcolati dai mezzi caricati
4. **Gauge disponibilità** — indicatore circolare % flotta disponibile
5. **Popup stats per zona** — click su zona → stats mezzi interni

---

## Architettura componenti

```
VistaDashboardAP (modificato)
├── KpiBar (inline, nuovo)
├── Map
│   ├── ZonaPoligono[]  (+ onClick per stats)
│   ├── HeatmapLayerAP  (nuovo, vistaMode='heatmap')
│   ├── ClusterLayerAP  (nuovo, vistaMode='cluster')
│   ├── AdvancedMarker[] (filtrato per layerAttivi, vistaMode='pin')
│   └── PopupStatsZona  (nuovo, on click zona)
└── Pannello destra
    ├── Logo SMART MOBILITY
    ├── GaugeMezzi (SVG, nuovo)
    ├── Toggle vista: Pin | Cluster | Heatmap
    ├── Chips tipo mezzo: 🛴 N | 🚲 N | 🚗 N
    └── [VISUALIZZA REPORT]
```

---

## Stato locale

| State | Tipo | Default |
|---|---|---|
| `vistaMode` | `'pin' \| 'cluster' \| 'heatmap'` | `'pin'` |
| `layerAttivi` | `Set<string>` | `new Set(['monopattino','bicicletta','automobile'])` |
| `zonaSelezionata` | `ZonaMappa \| null` | `null` |
| `mezzi` | `MezzoMappa[]` | `[]` |
| `zone` | `ZonaMappa[]` | `[]` |
| `errore` | `string` | `''` |

Computed (non in state):
- `mezziVisibili = mezzi.filter(m => layerAttivi.has(m.tipo))`
- `kpi = { totale, disponibili, inUso, manutenzione }` calcolato da `mezzi`
- `percDisponibili = (kpi.disponibili / kpi.totale) * 100`

---

## Componenti nuovi

### HeatmapLayerAP
- **File:** `frontend/src/components/HeatmapLayerAP.tsx`
- Usa `useMapsLibrary('visualization')` per caricare la libreria Google Maps
- `useEffect` istanzia `google.maps.visualization.HeatmapLayer` con i punti `mezziVisibili`
- Aggiorna i punti al cambiare di `mezziVisibili`
- Cleanup: `heatmap.setMap(null)` on unmount
- Proprietà heatmap: `radius: 35`, `opacity: 0.7`

### ClusterLayerAP
- **File:** `frontend/src/components/ClusterLayerAP.tsx`
- Dipendenza: `@googlemaps/markerclusterer`
- Usa `useMap()` + `useEffect` per istanziare `MarkerClusterer`
- Crea `google.maps.marker.AdvancedMarkerElement` per ogni mezzo visibile
- Renderer personalizzato: cluster bubble con colore basato sul tipo predominante
- Cleanup: `clusterer.clearMarkers()` on unmount o cambio `mezziVisibili`

### PopupStatsZona
- **File:** `frontend/src/components/PopupStatsZona.tsx`
- Usa `InfoWindow` di `@vis.gl/react-google-maps` (o native `google.maps.InfoWindow`)
- Posizione: centroide del poligono zona (media lat/lng dei vertici)
- Contenuto:
  - Icona + nome + tipo zona (come TooltipZona)
  - Conteggio mezzi interni (point-in-polygon ray casting su `mezziVisibili`)
  - Breakdown per tipo: `🛴 X | 🚲 Y | 🚗 Z`
  - Breakdown per stato: `Disponibili X | In uso Y`
- Chiusura: click sulla ×, click fuori, o apertura altra zona

### Utility: `puntoInPoligono`
- **File:** `frontend/src/utils/geoUtils.ts`
- Algoritmo ray casting standard
- Firma: `puntoInPoligono(lat: number, lng: number, perimetro: GeoJSON.Polygon): boolean`
- Usata da `PopupStatsZona` per filtrare `mezziVisibili`

### KPI bar (inline in VistaDashboardAP)
- Fascia orizzontale sotto la topbar (altezza ~48px)
- 4 card: **Totale** (grigio) | **Disponibili** (verde) | **In uso** (blu) | **Manutenzione** (arancio)
- Background bianco, ombra leggera, separata dalla mappa

### GaugeMezzi (inline nel pannello)
- SVG circle progress con `stroke-dasharray` / `stroke-dashoffset`
- Mostra `percDisponibili%` al centro
- Colore arco: verde → arancio → rosso in base alla percentuale
- Raggio 40px, stroke 8px

### Layer chips (inline nel pannello)
- 3 pill per tipo mezzo con emoji + etichetta + badge conteggio
- Colori: monopattino `#4caf9a`, bicicletta `#2196f3`, automobile `#e91e8c`
- Quando inattivo: `opacity: 0.35`, background grigio

### Vista toggle (inline nel pannello)
- 3 pulsanti segmentati: `Pin | Cluster | Heatmap`
- Stile "segmented control" (bordo condiviso, fill sul selezionato)

---

## Flusso interazione (scenari)

### Scenario base (vistaMode='pin')
1. AP accede a `/ap/dashboard`
2. Caricamento mezzi + zone via `Promise.all([getMezziAP(), getZoneAP()])`
3. KPI bar si popola con i conteggi
4. Gauge mostra % disponibilità
5. Mappa mostra pin filtrati (tutti attivi per default)
6. AP può:
   - Toggle chip tipo → nasconde/mostra i pin di quel tipo
   - Click zona → `PopupStatsZona` con stats mezzi interni
   - Cambiare vista → Cluster o Heatmap

### Scenario alternativo: vistaMode='heatmap'
- I pin individuali spariscono
- `HeatmapLayerAP` mostra il gradiente di densità
- Layer chips rimangono attivi (filtrano anche la heatmap)
- Click zona rimane attivo → stats popup

### Scenario alternativo: vistaMode='cluster'
- I pin individuali spariscono
- `ClusterLayerAP` mostra cluster colorati
- Zoom in → cluster si espandono fino ai pin
- Click zona rimane attivo

### Scenario alternativo: errore caricamento
- `errore` viene impostato al fallimento della chiamata API
- Banner rosso sopra la mappa: "Impossibile caricare i dati della mappa. Riprova."
- KPI bar mostra `---`, gauge vuota

---

## Documentazione da aggiornare

### Sprint1_definitivo.md — Sprint Backlog
Aggiungere riga: `| AP.03 | Sprint 1 | Visualizza Mappa AP |`

### Sprint1_definitivo.md — Use case
Aggiungere tabella CS-XX (IF-AP.03) con:
- Scenario base (caricamento + filtro layer + cambio vista)
- Scenario alternativo: errore GIS (`mostraErrore("Dati GIS non disponibili. Riprovare.")`)

---

## Dipendenze

| Package | Motivo |
|---|---|
| `@googlemaps/markerclusterer` | ClusterLayerAP — clustering nativo Google Maps |

Nessuna altra dipendenza nuova. Heatmap usa `useMapsLibrary('visualization')` già disponibile tramite `@vis.gl/react-google-maps`.

---

## Test

I 6 test backend esistenti (`test_ap.py`) continuano a passare invariati.

Nessun nuovo test backend (logica già coperta).

Frontend: nessun test automatizzato richiesto dalla methodology (la UI viene verificata manualmente post-implementazione come da `docs/GitWorkflow.md`).
