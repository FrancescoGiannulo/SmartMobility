// maps.ts — stile mappa "Foresta" + colori grafici derivati dai token.

// Stile Google Maps coerente col dark control-room (verde profondo).
export const FORESTA_MAP_STYLE: google.maps.MapTypeStyle[] = [
  { elementType: 'geometry', stylers: [{ color: '#07221f' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#8EB69B' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#051F20' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#0B2B26' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#163832' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#04201c' }] },
  { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#0d322c' }] },
  { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: '#163832' }] },
  { featureType: 'transit', stylers: [{ visibility: 'off' }] },
  { featureType: 'administrative', elementType: 'geometry', stylers: [{ color: '#235347' }] },
]

// Helper colori per Recharts: legge i token correnti dal :root.
export function chartColors() {
  const s = getComputedStyle(document.documentElement)
  return {
    accent: s.getPropertyValue('--accent').trim() || '#5FF0C4',
    grid: s.getPropertyValue('--border').trim() || 'rgba(142,182,155,.16)',
    text: s.getPropertyValue('--text-dim').trim() || '#8EB69B',
  }
}
