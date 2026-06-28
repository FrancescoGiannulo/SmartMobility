# Spec: Clustering Mezzi su Mappa

**Data:** 2026-06-27
**Branch:** feature/clustering-mezzi
**Viste coinvolte:** VistaHomePageUtente (UT), VistaMappaOperatore (OP), VistaDashboardAP (AP)

---

## Problema

Con molti mezzi vicini tra loro, i pin si sovrappongono rendendo la mappa illeggibile (vedi screenshot). La soluzione è raggruppare i pin vicini in un blob cluster quando la mappa è a zoom basso, e mostrarli individualmente quando si zooma.

---

## Approccio scelto: `supercluster` + React AdvancedMarker

**Libreria:** `supercluster` (5 kB, zero dipendenze).
**Motivo:** l'unico approccio che preserva intatta la logica di selezione multipla React di UT (stato `isInSelezione`, `isNonDisponibile`, click handler sul drawer), senza richiedere sync imperativo tra DOM e stato React.

---

## Architettura

```
supercluster (lib)
     ↑
useMezziCluster(mezzi, map)        ← hook condiviso
  - ascolta zoom_changed + bounds_changed
  - ricalcola cluster ad ogni evento
  - restituisce ClusterItem[] | MezzoItem[]
     ↓
AdvancedMarker (React)
  ├── ClusterBlob     →  blob circolare cluster
  └── PinMezzo        →  sm-pin teardrop esistente (invariato)
```

### File nuovi

| File | Contenuto |
|---|---|
| `frontend/src/hooks/useMezziCluster.ts` | Hook che wrappa supercluster, ascolta eventi mappa, restituisce array di punti |
| `frontend/src/components/ClusterBlob.tsx` | Componente React blob cluster (cerchio, colore tipo dominante, badge conteggio) |

### File modificati

| File | Modifica |
|---|---|
| `VistaHomePageUtente.tsx` | Sostituisce `mezzi.map(→ AdvancedMarker)` con output di `useMezziCluster` |
| `VistaMappaOperatore.tsx` | Stessa sostituzione |
| `VistaDashboardAP.tsx` | Modalità `cluster`: sostituisce `<ClusterLayerAP>` con hook + `ClusterBlob` |
| `ClusterLayerAP.tsx` | Rimosso a migrazione AP completata |

---

## `useMezziCluster` — interfaccia

```ts
type MezzoPoint  = { type: 'mezzo';   mezzo: MezzoMappa }
type ClusterPoint = { type: 'cluster'; id: number; lat: number; lng: number;
                      count: number; tipoDominante: string }

function useMezziCluster(
  mezzi: MezzoMappa[],
  map: google.maps.Map | null
): Array<MezzoPoint | ClusterPoint>
```

- Raggio clustering: **60 px** (default supercluster)
- Zoom min cluster: si forma a zoom ≤ 15 (configurabile via costante)
- Al cambio di `mezzi` o della mappa, ricalcola immediatamente

---

## `ClusterBlob` — design visivo

- **Forma:** cerchio (distinguibile dal teardrop dei pin individuali)
- **Colore:** gradiente tipo dominante (stesso palette pin: cyan scooter, blue bici, salmon auto)
- **Contenuto centro:** emoji tipo dominante (🛴 / 🚲 / 🚗)
- **Badge:** cerchietto bianco in alto a destra con numero totale mezzi nel cluster
- **Dimensione:** 3 taglie in base al count
  - S (≤5 mezzi): 40px
  - M (≤20 mezzi): 52px
  - L (>20 mezzi): 64px
- **Click:** zoom automatico sulla mappa (`map.fitBounds` del bounding box del cluster)

**Tipo dominante:** il tipo con il maggior numero di mezzi nel cluster. In caso di parità, priorità: monopattino > bicicletta > automobile.

---

## Integrazione per vista

### UT (VistaHomePageUtente)

- `useMezziCluster(mezzi, map)` restituisce i punti
- Per ogni `MezzoPoint`: `<AdvancedMarker>` con `<PinMezzo>` esattamente come ora
  - `isInSelezione`, `isNonDisponibile`, `onClick` → nessuna modifica
- Per ogni `ClusterPoint`: `<AdvancedMarker>` con `<ClusterBlob>`
  - Click → `map.fitBounds` del cluster (non apre sidebar)
- Pin posizione utente: invariato

### OP (VistaMappaOperatore)

- Stessa sostituzione, senza logica di selezione
- Click su pin individuale → apre pannello dettaglio mezzo (comportamento attuale)

### AP (VistaDashboardAP)

- Solo la modalità `cluster` cambia: da `<ClusterLayerAP>` a hook + `ClusterBlob`
- Modalità `pin` e `heatmap`: invariate
- `ClusterLayerAP.tsx` eliminato dopo la migrazione

---

## Comportamento zoom

- Zoom out → i pin vicini collassano in cluster blob
- Click su cluster → `map.fitBounds` → la mappa zooma fino a separare i punti
- Zoom in manuale → i cluster si sciolgono progressivamente in pin individuali

---

## Non in scope

- Filtro per tipo mezzo nel cluster
- Animazioni di espansione/collasso
- Click su cluster → lista mezzi in popup (scelta esplicita: zoom in)
- Stato `dim` (non disponibile) sui cluster (applicato solo ai pin individuali)
