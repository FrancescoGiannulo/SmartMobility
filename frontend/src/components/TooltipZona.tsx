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
        fontFamily: 'var(--ff-body)',
        padding: '14px 16px',
        minWidth: 220,
        maxWidth: 280,
        color: 'var(--text)',
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
            color: 'var(--accent-ink)',
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
              color: 'var(--text)',
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
            background: 'var(--surface-2)',
            border: '1px solid var(--border)',
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
              color: 'var(--text-mute)',
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
            }}
          >
            Limite
          </span>
          <span
            style={{
              fontFamily: 'var(--ff-mono)',
              fontSize: 14,
              fontWeight: 700,
              color: 'var(--text)',
            }}
          >
            {zona.limite_velocita} <span style={{ color: 'var(--text-mute)', fontSize: 12 }}>km/h</span>
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
            background: 'color-mix(in srgb, var(--danger) 8%, var(--surface))',
            color: 'var(--danger)',
            border: '1px solid color-mix(in srgb, var(--danger) 30%, var(--surface))',
            borderRadius: 10,
            fontSize: 12.5,
            fontWeight: 700,
            letterSpacing: '0.02em',
            cursor: 'pointer',
            fontFamily: 'inherit',
            transition: 'background 160ms ease, color 160ms ease, border-color 160ms ease',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = 'var(--danger)'
            e.currentTarget.style.color = 'var(--accent-ink)'
            e.currentTarget.style.borderColor = 'transparent'
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = 'color-mix(in srgb, var(--danger) 8%, var(--surface))'
            e.currentTarget.style.color = 'var(--danger)'
            e.currentTarget.style.borderColor = 'color-mix(in srgb, var(--danger) 30%, var(--surface))'
          }}
        >
          Elimina zona
        </button>
      )}
    </div>
  )
}
