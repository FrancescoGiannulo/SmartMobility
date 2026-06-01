import type { ZonaMappa } from '../services/MapService'
import { COLORI_ZONA } from '../utils/coloriZona'

interface TooltipZonaProps {
  zona: ZonaMappa
  onElimina?: () => void
}

const ICONA_TIPO: Record<string, string> = {
  operativa: '◉',
  parcheggio: 'P',
  limitata: '!',
  vietata: '×',
}

const LABEL_TIPO: Record<string, string> = {
  operativa: 'Operativa',
  parcheggio: 'Parcheggio',
  limitata: 'Limitata',
  vietata: 'Vietata',
}

export default function TooltipZona({ zona, onElimina }: TooltipZonaProps) {
  const colori = COLORI_ZONA[zona.tipo] ?? COLORI_ZONA.operativa
  const accent = colori.stroke
  const icona = ICONA_TIPO[zona.tipo] ?? '●'
  const label = LABEL_TIPO[zona.tipo] ?? zona.tipo

  return (
    <div
      style={{
        fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif",
        padding: '14px 16px',
        minWidth: 220,
        maxWidth: 280,
        color: '#0f172a',
      }}
    >
      {/* Header: icon + name + type badge */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
        <div
          style={{
            width: 38,
            height: 38,
            borderRadius: 11,
            background: `linear-gradient(135deg, ${accent}, ${accent}cc)`,
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 18,
            fontWeight: 800,
            flexShrink: 0,
            boxShadow: `0 4px 12px ${accent}66`,
          }}
        >
          {icona}
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 12,
              fontWeight: 700,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: accent,
              marginBottom: 2,
            }}
          >
            {label}
          </div>
          <div
            style={{
              fontSize: 15,
              fontWeight: 800,
              letterSpacing: '-0.01em',
              color: '#0f172a',
              lineHeight: 1.25,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {zona.nome}
          </div>
        </div>
      </div>

      {/* Optional speed-limit row */}
      {zona.limite_velocita && (
        <div
          style={{
            marginTop: 12,
            padding: '8px 10px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: 10,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 8,
          }}
        >
          <span
            style={{
              fontSize: 12,
              fontWeight: 700,
              color: '#64748b',
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
            }}
          >
            Limite
          </span>
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 14,
              fontWeight: 700,
              color: '#0f172a',
            }}
          >
            {zona.limite_velocita} <span style={{ color: '#94a3b8', fontSize: 12 }}>km/h</span>
          </span>
        </div>
      )}

      {/* Delete action (operator only) */}
      {onElimina && (
        <button
          type="button"
          onClick={e => {
            e.stopPropagation()
            onElimina()
          }}
          style={{
            marginTop: 12,
            width: '100%',
            padding: '9px 12px',
            background: 'rgba(244, 63, 94, 0.08)',
            color: '#f43f5e',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            borderRadius: 10,
            fontSize: 12.5,
            fontWeight: 700,
            letterSpacing: '0.02em',
            cursor: 'pointer',
            fontFamily: 'inherit',
            transition: 'background 160ms ease, color 160ms ease, border-color 160ms ease',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = '#f43f5e'
            e.currentTarget.style.color = '#fff'
            e.currentTarget.style.borderColor = 'transparent'
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = 'rgba(244, 63, 94, 0.08)'
            e.currentTarget.style.color = '#f43f5e'
            e.currentTarget.style.borderColor = 'rgba(244, 63, 94, 0.3)'
          }}
        >
          Elimina zona
        </button>
      )}
    </div>
  )
}
