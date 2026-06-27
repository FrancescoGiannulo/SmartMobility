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
        // ClusterFeature has `cluster: true` in its properties
        const props = f.properties as Record<string, unknown>
        if (props['cluster'] === true) {
          const p = f.properties as { cluster_id: number; point_count: number; tipi?: TipiMap }
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
