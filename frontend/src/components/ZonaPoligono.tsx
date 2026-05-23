import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { ZonaMappa } from '../services/MapService'

interface ZonaPoligonoProps {
  zona: ZonaMappa
  fillColor: string
  strokeColor: string
  onHover?: (zona: ZonaMappa, pos: google.maps.LatLngLiteral) => void
  onHoverEnd?: () => void
  onClick?: (zona: ZonaMappa) => void
}

export default function ZonaPoligono({
  zona, fillColor, strokeColor, onHover, onHoverEnd, onClick,
}: ZonaPoligonoProps) {
  const mappa = useMap()

  // Ref pattern: i callback e i dati della zona vengono aggiornati ad ogni render
  // senza ricaricare l'effect e ricreare il poligono
  const zonaRef = useRef(zona)
  zonaRef.current = zona
  const onHoverRef = useRef(onHover)
  onHoverRef.current = onHover
  const onHoverEndRef = useRef(onHoverEnd)
  onHoverEndRef.current = onHoverEnd
  const onClickRef = useRef(onClick)
  onClickRef.current = onClick

  useEffect(() => {
    if (!mappa || !window.google) return
    const paths = zonaRef.current.perimetro.coordinates[0].map(
      ([lng, lat]) => ({ lat, lng })
    )
    const poly = new window.google.maps.Polygon({
      paths,
      strokeColor,
      strokeOpacity: 1,
      strokeWeight: 2,
      fillColor,
      fillOpacity: 1,
      map: mappa,
    })
    window.google.maps.event.addListener(
      poly,
      'mouseover',
      (e: google.maps.MapMouseEvent) => {
        if (e.latLng) {
          onHoverRef.current?.(zonaRef.current, {
            lat: e.latLng.lat(),
            lng: e.latLng.lng(),
          })
        }
      }
    )
    window.google.maps.event.addListener(poly, 'mouseout', () => {
      onHoverEndRef.current?.()
    })
    window.google.maps.event.addListener(poly, 'click', () => {
      onClickRef.current?.(zonaRef.current)
    })
    return () => {
      window.google.maps.event.clearInstanceListeners(poly)
      poly.setMap(null)
    }
  }, [mappa, zona.id, fillColor, strokeColor]) // eslint-disable-line react-hooks/exhaustive-deps

  return null
}
