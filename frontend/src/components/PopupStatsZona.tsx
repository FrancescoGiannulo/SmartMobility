import { InfoWindow } from '@vis.gl/react-google-maps'
import { puntoInPoligono } from '../utils/geoUtils'
import { COLORI_ZONA } from '../utils/coloriZona'
import type { ZonaMappa, MezzoMappa } from '../services/MapService'

const LABEL_TIPO: Record<string, string> = {
  operativa: 'Operativa',
  parcheggio: 'Parcheggio',
  limitata: 'Limitata',
  vietata: 'Vietata',
}
const ICONA_TIPO: Record<string, string> = {
  operativa: '◉',
  parcheggio: 'P',
  limitata: '!',
  vietata: '×',
}

function calcolaCentroide(zona: ZonaMappa): google.maps.LatLngLiteral {
  const ring = zona.perimetro.coordinates[0]
  // GeoJSON: [lng, lat]
  const lat = ring.reduce((s, c) => s + c[1], 0) / ring.length
  const lng = ring.reduce((s, c) => s + c[0], 0) / ring.length
  return { lat, lng }
}

interface Props {
  zona: ZonaMappa
  mezziVisibili: MezzoMappa[]
  onChiudi: () => void
}

export default function PopupStatsZona({ zona, mezziVisibili, onChiudi }: Props) {
  const centroide = calcolaCentroide(zona)
  const mezziInterni = mezziVisibili.filter(m =>
    puntoInPoligono(m.lat, m.lng, zona.perimetro)
  )
  const perTipo = {
    monopattino: mezziInterni.filter(m => m.tipo === 'monopattino').length,
    bicicletta: mezziInterni.filter(m => m.tipo === 'bicicletta').length,
    automobile: mezziInterni.filter(m => m.tipo === 'automobile').length,
  }
  const disponibili = mezziInterni.filter(m => m.stato === 'Disponibile').length
  const accent = COLORI_ZONA[zona.tipo]?.stroke ?? '#2196f3'

  return (
    <InfoWindow position={centroide} onCloseClick={onChiudi}>
      <div style={{ fontFamily: 'system-ui, sans-serif', minWidth: 200, color: '#0f172a', padding: '2px 4px' }}>
        {/* Header zona */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: accent, color: '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 800, fontSize: 16, flexShrink: 0,
          }}>
            {ICONA_TIPO[zona.tipo] ?? '●'}
          </div>
          <div>
            <div style={{ fontSize: 10, fontWeight: 700, color: accent, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              {LABEL_TIPO[zona.tipo]}
            </div>
            <div style={{ fontSize: 14, fontWeight: 800 }}>{zona.nome}</div>
          </div>
        </div>

        {/* Totale mezzi */}
        <div style={{ background: '#f8fafc', borderRadius: 8, padding: '7px 10px', marginBottom: 8 }}>
          <div style={{ fontSize: 11, color: '#64748b', fontWeight: 600, marginBottom: 2 }}>Mezzi nella zona</div>
          <div style={{ fontSize: 22, fontWeight: 800 }}>{mezziInterni.length}</div>
        </div>

        {/* Breakdown per tipo */}
        <div style={{ display: 'flex', gap: 5, marginBottom: 8 }}>
          {[
            { emoji: '🛴', count: perTipo.monopattino, colore: '#4caf9a' },
            { emoji: '🚲', count: perTipo.bicicletta, colore: '#2196f3' },
            { emoji: '🚗', count: perTipo.automobile, colore: '#e91e8c' },
          ].map(({ emoji, count, colore }) => (
            <div key={emoji} style={{
              flex: 1, textAlign: 'center', background: '#f8fafc',
              borderRadius: 8, padding: '5px 4px',
              borderTop: `3px solid ${colore}`,
            }}>
              <div style={{ fontSize: 15 }}>{emoji}</div>
              <div style={{ fontWeight: 800, fontSize: 13 }}>{count}</div>
            </div>
          ))}
        </div>

        {/* Stato */}
        <div style={{ fontSize: 11, color: '#64748b' }}>
          <span style={{ color: '#4caf9a', fontWeight: 700 }}>{disponibili} disponibili</span>
          {' · '}
          <span>{mezziInterni.length - disponibili} non disponibili</span>
        </div>
      </div>
    </InfoWindow>
  )
}
