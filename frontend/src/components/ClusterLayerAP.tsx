import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import { MarkerClusterer } from '@googlemaps/markerclusterer'
import type { MezzoMappa } from '../services/MapService'

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#155e52',
  bicicletta: '#2196f3',
  automobile: '#e91e8c',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

export default function ClusterLayerAP({ mezzi }: { mezzi: MezzoMappa[] }) {
  const map = useMap()
  const clustererRef = useRef<MarkerClusterer | null>(null)
  const markersRef = useRef<google.maps.marker.AdvancedMarkerElement[]>([])

  useEffect(() => {
    if (!map) return
    clustererRef.current = new MarkerClusterer({ map })
    return () => {
      clustererRef.current?.clearMarkers()
      clustererRef.current = null
    }
  }, [map])

  useEffect(() => {
    if (!clustererRef.current || !window.google) return
    clustererRef.current.clearMarkers()
    markersRef.current.forEach(m => { m.map = null })
    markersRef.current = []

    const nuoviMarker = mezzi.map(m => {
      const el = document.createElement('div')
      el.style.cssText = [
        `background:${COLORI_MEZZO[m.tipo] ?? '#888'}`,
        'border-radius:50%',
        'width:32px',
        'height:32px',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'font-size:16px',
        'box-shadow:0 2px 6px rgba(0,0,0,0.3)',
        'border:2px solid #fff',
        `opacity:${m.stato === 'Disponibile' ? 1 : 0.45}`,
      ].join(';')
      el.textContent = EMOJI_MEZZO[m.tipo] ?? '●'
      return new google.maps.marker.AdvancedMarkerElement({
        position: { lat: m.lat, lng: m.lng },
        content: el,
      })
    })
    markersRef.current = nuoviMarker
    clustererRef.current.addMarkers(nuoviMarker)
  }, [mezzi])

  return null
}
