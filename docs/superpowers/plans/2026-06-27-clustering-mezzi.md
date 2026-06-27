# Clustering Mezzi su Mappa — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raggruppare i pin dei mezzi in blob cluster quando la mappa è a basso zoom, e mostrare pin individuali quando si zooma, su tutte e tre le viste mappa (UT, OP, AP).

**Architecture:** Hook `useMezziCluster(mezzi, map)` wrappa `supercluster` per calcolare cluster lato client al cambio di zoom/bounds. Ogni vista ha un componente inner (renderizzato dentro `<Map>`) che chiama il hook e mappa i risultati su `<ClusterBlob>` o `<PinMezzo>` via React `AdvancedMarker`. `ClusterLayerAP` viene eliminato e sostituito dallo stesso pattern.

**Tech Stack:** `supercluster` (npm), `@vis.gl/react-google-maps`, React 19 + TypeScript.

## Global Constraints

- Branch di lavoro: `feature/clustering-mezzi`
- Dominio: termini glossario (`Mezzo`, `MezzoMappa`, ecc.) — non usare Vehicle/Bike
- Colori mezzo: monopattino `#5FF0C4→#42A889`, bicicletta `#7fb4ff→#597EB2`, automobile `#FF8A7A→#B26155`
- Tipo dominante in caso di parità: priorità monopattino > bicicletta > automobile
- Cluster click → zoom in (`map.setZoom(expansionZoom)` + `map.panTo`)
- Dimensioni blob: ≤5 mezzi = 40px, ≤20 = 52px, >20 = 64px
- Verifica build dopo ogni task: `cd frontend && npm run build`

---

## File Map

| File | Azione | Responsabilità |
|---|---|---|
| `frontend/src/hooks/useMezziCluster.ts` | Crea | Hook: clustering logic con supercluster, ascolta eventi mappa |
| `frontend/src/components/ClusterBlob.tsx` | Crea | Componente visivo blob cluster |
| `frontend/src/views/utente/VistaHomePageUtente.tsx` | Modifica | Aggiunge `MezziClusterLayer` inner component, sostituisce loop marker |
| `frontend/src/views/operatore/VistaMappaOperatore.tsx` | Modifica | Stessa sostituzione, logica più semplice |
| `frontend/src/views/amministrazione/VistaDashboardAP.tsx` | Modifica | Modalità cluster: sostituisce `<ClusterLayerAP>` con hook + ClusterBlob |
| `frontend/src/components/ClusterLayerAP.tsx` | Elimina | Rimpiazzato dal pattern condiviso |

---

### Task 1: Installa supercluster e crea `useMezziCluster`

**Files:**
- Create: `frontend/src/hooks/useMezziCluster.ts`

**Interfaces:**
- Produces:
  ```ts
  export type MezzoPoint   = { type: 'mezzo';   mezzo: MezzoMappa }
  export type ClusterPoint = { type: 'cluster'; id: number; lat: number; lng: number; count: number; tipoDominante: string }
  export type ClusterItem  = MezzoPoint | ClusterPoint

  export function useMezziCluster(
    mezzi: MezzoMappa[],
    map: google.maps.Map | null
  ): { items: ClusterItem[]; getExpansionZoom: (clusterId: number) => number }
  ```

- [ ] **Step 1: Installa supercluster**

```bash
cd frontend && npm install supercluster
```

Output atteso: `added 1 package` (supercluster include i tipi TypeScript built-in dalla v8).

- [ ] **Step 2: Crea il file hook**

Crea `frontend/src/hooks/useMezziCluster.ts` con il contenuto seguente:

```ts
import { useEffect, useRef, useState, useCallback } from 'react'
import Supercluster from 'supercluster'
import type { MezzoMappa } from '../services/MapService'

export type MezzoPoint = { type: 'mezzo'; mezzo: MezzoMappa }
export type ClusterPoint = {
  type: 'cluster'
  id: number
  lat: number
  lng: number
  count: number
  tipoDominante: string
}
export type ClusterItem = MezzoPoint | ClusterPoint

type TipiMap = Record<string, number>
type PointProps = { id: string; tipo: string }
type ClusterProps = { tipi: TipiMap }

const TIPO_PRIORITY = ['monopattino', 'bicicletta', 'automobile']

function dominante(tipi: TipiMap): string {
  return TIPO_PRIORITY.reduce(
    (best, tipo) => ((tipi[tipo] ?? 0) > (tipi[best] ?? 0) ? tipo : best),
    TIPO_PRIORITY[0]
  )
}

export function useMezziCluster(
  mezzi: MezzoMappa[],
  map: google.maps.Map | null
): { items: ClusterItem[]; getExpansionZoom: (clusterId: number) => number } {
  const [items, setItems] = useState<ClusterItem[]>([])
  const scRef = useRef<Supercluster<PointProps, ClusterProps> | null>(null)

  useEffect(() => {
    if (!map) return
    if (mezzi.length === 0) { setItems([]); return }

    const sc = new Supercluster<PointProps, ClusterProps>({
      radius: 60,
      maxZoom: 16,
      map: props => ({ tipi: { [props.tipo]: 1 } }),
      reduce: (acc, props) => {
        Object.entries(props.tipi).forEach(([k, v]) => {
          acc.tipi[k] = (acc.tipi[k] ?? 0) + v
        })
      },
    })

    sc.load(
      mezzi.map(m => ({
        type: 'Feature' as const,
        geometry: { type: 'Point' as const, coordinates: [m.lng, m.lat] },
        properties: { id: m.id, tipo: m.tipo },
      }))
    )
    scRef.current = sc

    function calcola() {
      const bounds = map!.getBounds()
      const zoom = Math.round(map!.getZoom() ?? 14)
      if (!bounds) return

      const bbox: [number, number, number, number] = [
        bounds.getSouthWest().lng(),
        bounds.getSouthWest().lat(),
        bounds.getNorthEast().lng(),
        bounds.getNorthEast().lat(),
      ]

      const result: ClusterItem[] = sc.getClusters(bbox, zoom).map(f => {
        if (f.properties.cluster) {
          const p = f.properties as { cluster_id: number; point_count: number } & ClusterProps
          return {
            type: 'cluster' as const,
            id: p.cluster_id,
            lat: f.geometry.coordinates[1],
            lng: f.geometry.coordinates[0],
            count: p.point_count,
            tipoDominante: dominante(p.tipi ?? {}),
          }
        }
        const p = f.properties as PointProps
        return {
          type: 'mezzo' as const,
          mezzo: mezzi.find(m => m.id === p.id)!,
        }
      })
      setItems(result)
    }

    calcola()
    const zl = map.addListener('zoom_changed', calcola)
    const bl = map.addListener('bounds_changed', calcola)

    return () => {
      zl.remove()
      bl.remove()
      scRef.current = null
    }
  }, [map, mezzi])

  const getExpansionZoom = useCallback(
    (clusterId: number) => scRef.current?.getClusterExpansionZoom(clusterId) ?? 18,
    []
  )

  return { items, getExpansionZoom }
}
```

- [ ] **Step 3: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit
```

Output atteso: nessun errore.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/hooks/useMezziCluster.ts frontend/package.json frontend/package-lock.json
git commit -m "feat: add useMezziCluster hook with supercluster"
```

---

### Task 2: Crea `ClusterBlob`

**Files:**
- Create: `frontend/src/components/ClusterBlob.tsx`

**Interfaces:**
- Consumes: `ClusterPoint` (da Task 1, ma non importato — riceve `count` e `tipoDominante` come props dirette)
- Produces:
  ```ts
  export default function ClusterBlob(props: { count: number; tipoDominante: string }): JSX.Element
  ```

- [ ] **Step 1: Crea il componente**

Crea `frontend/src/components/ClusterBlob.tsx`:

```tsx
const COLORI: Record<string, { c1: string; c2: string }> = {
  monopattino: { c1: '#5FF0C4', c2: '#42A889' },
  bicicletta:  { c1: '#7fb4ff', c2: '#597EB2' },
  automobile:  { c1: '#FF8A7A', c2: '#B26155' },
}
const EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta:  '🚲',
  automobile:  '🚗',
}

function dim(count: number): number {
  if (count > 20) return 64
  if (count > 5)  return 52
  return 40
}

export default function ClusterBlob({
  count,
  tipoDominante,
}: {
  count: number
  tipoDominante: string
}) {
  const c = COLORI[tipoDominante] ?? { c1: '#64748b', c2: '#334155' }
  const emoji = EMOJI[tipoDominante] ?? '●'
  const size = dim(count)
  return (
    <div style={{ position: 'relative', width: size, height: size, cursor: 'pointer' }}>
      <div style={{
        width: size,
        height: size,
        borderRadius: '50%',
        background: `linear-gradient(135deg, ${c.c1}, ${c.c2})`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: size * 0.4,
        boxShadow: '0 2px 8px rgba(0,0,0,0.35)',
        border: '2px solid rgba(255,255,255,0.2)',
      }}>
        {emoji}
      </div>
      <div style={{
        position: 'absolute',
        top: -4,
        right: -4,
        background: 'white',
        color: '#0a2e26',
        borderRadius: '50%',
        minWidth: 20,
        height: 20,
        padding: '0 3px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 11,
        fontWeight: 700,
        boxShadow: '0 1px 4px rgba(0,0,0,0.3)',
        lineHeight: 1,
      }}>
        {count}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit
```

Output atteso: nessun errore.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/ClusterBlob.tsx
git commit -m "feat: add ClusterBlob component"
```

---

### Task 3: Integra clustering in VistaHomePageUtente (UT)

**Files:**
- Modify: `frontend/src/views/utente/VistaHomePageUtente.tsx` (righe 1-8, 464-478)

**Interfaces:**
- Consumes:
  - `useMezziCluster(mezzi: MezzoMappa[], map: google.maps.Map | null)` → `{ items, getExpansionZoom }` (Task 1)
  - `ClusterBlob({ count, tipoDominante })` (Task 2)
  - `useMap()` da `@vis.gl/react-google-maps`

- [ ] **Step 1: Aggiungi import `useMap` e i nuovi moduli**

In `VistaHomePageUtente.tsx`, la riga 4 importa da `@vis.gl/react-google-maps`. Sostituisci quella sezione:

```tsx
// Prima:
import {
  Map as GoogleMap,
  AdvancedMarker,
} from '@vis.gl/react-google-maps'

// Dopo:
import {
  Map as GoogleMap,
  AdvancedMarker,
  useMap,
} from '@vis.gl/react-google-maps'
import { useMezziCluster } from '../../hooks/useMezziCluster'
import ClusterBlob from '../../components/ClusterBlob'
```

- [ ] **Step 2: Aggiungi il componente inner `MezziClusterLayer`**

Dopo la funzione `formatTempoRimanente` (riga ~83) e prima di `export default function VistaHomePageUtente()`, aggiungi:

```tsx
function MezziClusterLayer({
  mezzi,
  onMezzoClick,
  isSelected,
  isDim,
}: {
  mezzi: MezzoMappa[]
  onMezzoClick: (m: MezzoMappa) => void
  isSelected: (m: MezzoMappa) => boolean
  isDim: (m: MezzoMappa) => boolean
}) {
  const map = useMap()
  const { items, getExpansionZoom } = useMezziCluster(mezzi, map)
  const primoDisponibileId = mezzi.find(m => m.stato === 'Disponibile')?.id

  return (
    <>
      {items.map(item => {
        if (item.type === 'cluster') {
          return (
            <AdvancedMarker
              key={`cluster-${item.id}`}
              position={{ lat: item.lat, lng: item.lng }}
              onClick={() => {
                if (!map) return
                map.setZoom(getExpansionZoom(item.id))
                map.panTo({ lat: item.lat, lng: item.lng })
              }}
            >
              <ClusterBlob count={item.count} tipoDominante={item.tipoDominante} />
            </AdvancedMarker>
          )
        }
        const m = item.mezzo
        return (
          <AdvancedMarker
            key={m.id}
            position={{ lat: m.lat, lng: m.lng }}
            onClick={() => onMezzoClick(m)}
          >
            <div data-tour={m.id === primoDisponibileId ? 'mezzo-mappa' : undefined}>
              <PinMezzo tipo={m.tipo} selected={isSelected(m)} dim={isDim(m)} />
            </div>
          </AdvancedMarker>
        )
      })}
    </>
  )
}
```

- [ ] **Step 3: Sostituisci il loop marker nella JSX della mappa**

Trova il blocco (righe 464-478):
```tsx
        {mezzi.map((m, i) => {
          const primoDisponibile = mezzi.findIndex(x => x.stato === 'Disponibile')
          const isTourTarget = i === (primoDisponibile >= 0 ? primoDisponibile : 0)
          return (
            <AdvancedMarker
              key={m.id}
              position={{ lat: m.lat, lng: m.lng }}
              onClick={() => { setMezzoAttivo(m); setErrorePanel('') }}
            >
              <div data-tour={isTourTarget ? 'mezzo-mappa' : undefined}>
                <PinMezzo tipo={m.tipo} selected={isInSelezione(m)} dim={isNonDisponibile(m)} />
              </div>
            </AdvancedMarker>
          )
        })}
```

Sostituisci con:
```tsx
        <MezziClusterLayer
          mezzi={mezzi}
          onMezzoClick={m => { setMezzoAttivo(m); setErrorePanel('') }}
          isSelected={isInSelezione}
          isDim={isNonDisponibile}
        />
```

- [ ] **Step 4: Verifica build TypeScript**

```bash
cd frontend && npm run build
```

Output atteso: build completata senza errori.

- [ ] **Step 5: Verifica visiva in browser**

Apri http://localhost:5173, accedi come utente. Con zoom basso devono comparire blob cluster; zoomando i pin si separano. Click su un blob → la mappa zooma fino a separare i pin.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/views/utente/VistaHomePageUtente.tsx
git commit -m "feat(ut): add vehicle clustering on user map"
```

---

### Task 4: Integra clustering in VistaMappaOperatore (OP)

**Files:**
- Modify: `frontend/src/views/operatore/VistaMappaOperatore.tsx` (righe 1-14, 276-284)

**Interfaces:**
- Consumes: stesse di Task 3 (hook + ClusterBlob)

- [ ] **Step 1: Aggiungi import `useMap` e i nuovi moduli**

In `VistaMappaOperatore.tsx`, sostituisci la sezione import:

```tsx
// Prima:
import {
  Map as GoogleMap,
  AdvancedMarker,
  useMap,
} from '@vis.gl/react-google-maps'

// Dopo (useMap già presente, aggiunge hook e blob):
import {
  Map as GoogleMap,
  AdvancedMarker,
  useMap,
} from '@vis.gl/react-google-maps'
import { useMezziCluster } from '../../hooks/useMezziCluster'
import ClusterBlob from '../../components/ClusterBlob'
```

- [ ] **Step 2: Aggiungi il componente inner `MezziClusterLayer`**

Dopo la funzione `PinMezzo` (riga ~44) e prima di `type TipoZona`, aggiungi:

```tsx
function MezziClusterLayer({
  mezzi,
  onMezzoClick,
}: {
  mezzi: MezzoMappa[]
  onMezzoClick: (m: MezzoMappa) => void
}) {
  const map = useMap()
  const { items, getExpansionZoom } = useMezziCluster(mezzi, map)

  return (
    <>
      {items.map(item => {
        if (item.type === 'cluster') {
          return (
            <AdvancedMarker
              key={`cluster-${item.id}`}
              position={{ lat: item.lat, lng: item.lng }}
              onClick={e => {
                e.stop()
                if (!map) return
                map.setZoom(getExpansionZoom(item.id))
                map.panTo({ lat: item.lat, lng: item.lng })
              }}
            >
              <ClusterBlob count={item.count} tipoDominante={item.tipoDominante} />
            </AdvancedMarker>
          )
        }
        const m = item.mezzo
        return (
          <AdvancedMarker
            key={m.id}
            position={{ lat: m.lat, lng: m.lng }}
            onClick={e => { e.stop(); onMezzoClick(m) }}
          >
            <PinMezzo tipo={m.tipo} stato={m.stato} />
          </AdvancedMarker>
        )
      })}
    </>
  )
}
```

- [ ] **Step 3: Sostituisci il loop marker nella JSX**

Trova il blocco (righe 276-284):
```tsx
              {mezzi.map(m => (
                <AdvancedMarker
                  key={m.id}
                  position={{ lat: m.lat, lng: m.lng }}
                  onClick={e => { e.stop(); setMezzoSelezionato(m); setZonaSelezionata(null) }}
                >
                  <PinMezzo tipo={m.tipo} stato={m.stato} />
                </AdvancedMarker>
              ))}
```

Sostituisci con:
```tsx
              <MezziClusterLayer
                mezzi={mezzi}
                onMezzoClick={m => { setMezzoSelezionato(m); setZonaSelezionata(null) }}
              />
```

- [ ] **Step 4: Verifica build TypeScript**

```bash
cd frontend && npm run build
```

Output atteso: build completata senza errori.

- [ ] **Step 5: Verifica visiva in browser**

Accedi come operatore → mappa. Zoom basso → blob cluster. Zoom alto → pin individuali. Click pin → pannello dettaglio mezzo si apre come prima.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/views/operatore/VistaMappaOperatore.tsx
git commit -m "feat(op): add vehicle clustering on operator map"
```

---

### Task 5: Migra AP e rimuovi ClusterLayerAP

**Files:**
- Modify: `frontend/src/views/amministrazione/VistaDashboardAP.tsx` (righe 10, 248-255)
- Delete: `frontend/src/components/ClusterLayerAP.tsx`

**Interfaces:**
- Consumes: stesse di Task 3/4
- La modalità `cluster` di AP mostra pin circolari (stile AP `PinMezzo`) per i singoli veicoli, non sm-pin teardrop

- [ ] **Step 1: Aggiungi import hook e ClusterBlob, rimuovi ClusterLayerAP**

In `VistaDashboardAP.tsx`, sostituisci:
```tsx
// Prima:
import { Map, AdvancedMarker } from '@vis.gl/react-google-maps'
...
import ClusterLayerAP from '../../components/ClusterLayerAP'

// Dopo:
import { Map, AdvancedMarker, useMap } from '@vis.gl/react-google-maps'
...
import { useMezziCluster } from '../../hooks/useMezziCluster'
import ClusterBlob from '../../components/ClusterBlob'
// (riga import ClusterLayerAP rimossa)
```

- [ ] **Step 2: Aggiungi il componente inner `MezziClusterLayerAP`**

Dopo la funzione `PinMezzo` (riga ~83) e prima di `export default function VistaDashboardAP()`, aggiungi:

```tsx
function MezziClusterLayerAP({ mezzi }: { mezzi: MezzoMappa[] }) {
  const map = useMap()
  const { items, getExpansionZoom } = useMezziCluster(mezzi, map)

  return (
    <>
      {items.map(item => {
        if (item.type === 'cluster') {
          return (
            <AdvancedMarker
              key={`cluster-${item.id}`}
              position={{ lat: item.lat, lng: item.lng }}
              onClick={() => {
                if (!map) return
                map.setZoom(getExpansionZoom(item.id))
                map.panTo({ lat: item.lat, lng: item.lng })
              }}
            >
              <ClusterBlob count={item.count} tipoDominante={item.tipoDominante} />
            </AdvancedMarker>
          )
        }
        const m = item.mezzo
        return (
          <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
            <PinMezzo tipo={m.tipo} stato={m.stato} />
          </AdvancedMarker>
        )
      })}
    </>
  )
}
```

- [ ] **Step 3: Sostituisci `<ClusterLayerAP>` nel JSX**

Trova (riga ~255):
```tsx
                {vistaMode === 'cluster' && <ClusterLayerAP mezzi={mezziVisibili} />}
```

Sostituisci con:
```tsx
                {vistaMode === 'cluster' && <MezziClusterLayerAP mezzi={mezziVisibili} />}
```

- [ ] **Step 4: Elimina ClusterLayerAP**

```bash
rm frontend/src/components/ClusterLayerAP.tsx
```

- [ ] **Step 5: Verifica build TypeScript**

```bash
cd frontend && npm run build
```

Output atteso: build completata senza errori. Nessun riferimento rimasto a `ClusterLayerAP`.

- [ ] **Step 6: Verifica visiva in browser**

Accedi come AP → modalità cluster. Zoom basso → blob. Zoom alto → pin circolari. Click blob → zoom in. Modalità pin e heatmap: invariate.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/views/amministrazione/VistaDashboardAP.tsx
git rm frontend/src/components/ClusterLayerAP.tsx
git commit -m "feat(ap): migrate cluster mode to shared hook, remove ClusterLayerAP"
```
