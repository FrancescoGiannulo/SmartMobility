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
      <div style={{ fontFamily: 'var(--ff-body)', minWidth: 200, color: 'var(--text)', padding: '2px 4px', background: 'var(--bg)' }}>
        {/* Header zona */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: accent, color: 'var(--accent-ink)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 800, fontSize: 16, flexShrink: 0,
          }}>
            {ICONA_TIPO[zona.tipo] ?? '●'}
          </div>
          <div>
            <div style={{ fontSize: 10, fontWeight: 700, color: accent, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              {LABEL_TIPO[zona.tipo]}
            </div>
            <div style={{ fontSize: 14, fontWeight: 800, color: 'var(--text)' }}>{zona.nome}</div>
          </div>
        </div>

        {/* Totale mezzi */}
        <div style={{ background: 'var(--surface-2)', borderRadius: 8, padding: '7px 10px', marginBottom: 8 }}>
          <div style={{ fontSize: 11, color: 'var(--text-mute)', fontWeight: 600, marginBottom: 2 }}>Mezzi nella zona</div>
          <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--text)' }}>{mezziInterni.length}</div>
        </div>

        {/* Breakdown per tipo */}
        <div style={{ display: 'flex', gap: 5, marginBottom: 8 }}>
          {[
            { emoji: '🛴', count: perTipo.monopattino, colore: '#5FF0C4' },
            { emoji: '🚲', count: perTipo.bicicletta, colore: '#7fb4ff' },
            { emoji: '🚗', count: perTipo.automobile, colore: '#FF8A7A' },
          ].map(({ emoji, count, colore }) => (
            <div key={emoji} style={{
              flex: 1, textAlign: 'center', background: 'var(--surface-2)',
              borderRadius: 8, padding: '5px 4px',
              borderTop: `3px solid ${colore}`,
            }}>
              <div style={{ fontSize: 15 }}>{emoji}</div>
              <div style={{ fontWeight: 800, fontSize: 13, color: 'var(--text)' }}>{count}</div>
            </div>
          ))}
        </div>

        {/* Stato */}
        <div style={{ fontSize: 11, color: 'var(--text-mute)' }}>
          <span style={{ color: 'var(--accent)', fontWeight: 700 }}>{disponibili} disponibili</span>
          {' · '}
          <span>{mezziInterni.length - disponibili} non disponibili</span>
        </div>
      </div>
    </InfoWindow>
  )
}
