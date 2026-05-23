import type { ZonaMappa } from '../services/MapService'

const COLORI_ZONA: Record<string, { stroke: string }> = {
  vietata:    { stroke: '#f44336' },
  limitata:   { stroke: '#ff9800' },
  parcheggio: { stroke: '#4caf50' },
  operativa:  { stroke: '#2196f3' },
}

export default function TooltipZona({ zona }: { zona: ZonaMappa }) {
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
    </div>
  )
}
