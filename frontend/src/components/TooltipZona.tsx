import type { ZonaMappa } from '../services/MapService'
import { COLORI_ZONA } from '../utils/coloriZona'

interface TooltipZonaProps {
  zona: ZonaMappa
  onElimina?: () => void
}

export default function TooltipZona({ zona, onElimina }: TooltipZonaProps) {
  const colori = COLORI_ZONA[zona.tipo] ?? COLORI_ZONA.operativa
  return (
    <div style={{ padding: '4px 2px', minWidth: 120 }}>
      <strong style={{ display: 'block', marginBottom: 4 }}>{zona.nome}</strong>
      <span style={{
        display: 'inline-block', padding: '2px 8px', borderRadius: 12, fontSize: 12,
        background: colori.stroke, color: '#fff',
      }}>
        {zona.tipo}
      </span>
      {zona.limite_velocita && (
        <span style={{ display: 'block', marginTop: 4, fontSize: 12 }}>
          Max {zona.limite_velocita} km/h
        </span>
      )}
      {onElimina && (
        <button
          onClick={e => { e.stopPropagation(); onElimina() }}
          style={{
            display: 'block', marginTop: 8, width: '100%',
            padding: '4px 0', background: '#f44336', color: '#fff',
            border: 'none', borderRadius: 6, fontSize: 12,
            cursor: 'pointer', fontWeight: 600,
          }}
        >
          🗑 Elimina
        </button>
      )}
    </div>
  )
}
