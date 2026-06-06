import { useEffect, useRef } from 'react'
import { useMap, useMapsLibrary } from '@vis.gl/react-google-maps'
import type { MezzoMappa } from '../services/MapService'

export default function HeatmapLayerAP({ mezzi }: { mezzi: MezzoMappa[] }) {
  const map = useMap()
  const visualization = useMapsLibrary('visualization')
  const layerRef = useRef<google.maps.visualization.HeatmapLayer | null>(null)

  useEffect(() => {
    if (!map || !visualization) return
    const layer = new google.maps.visualization.HeatmapLayer({
      data: [],
      map,
      radius: 35,
      opacity: 0.7,
    })
    layerRef.current = layer
    return () => {
      layer.setMap(null)
      layerRef.current = null
    }
  }, [map, visualization])

  useEffect(() => {
    if (!layerRef.current) return
    const points = mezzi.map(m => new google.maps.LatLng(m.lat, m.lng))
    layerRef.current.setData(points)
  }, [mezzi])

  return null
}
