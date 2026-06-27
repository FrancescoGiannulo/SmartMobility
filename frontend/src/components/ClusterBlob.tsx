const COLORI: Record<string, { c1: string; c2: string }> = {
  monopattino: { c1: '#5FF0C4', c2: '#42A889' },
  bicicletta:  { c1: '#7fb4ff', c2: '#597EB2' },
  automobile:  { c1: '#FF8A7A', c2: '#B26155' },
}
const EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta:  '🚲',
  automobile:  '🚗',
}

function dim(count: number): number {
  if (count > 20) return 64
  if (count > 5)  return 52
  return 40
}

export default function ClusterBlob({
  count,
  tipoDominante,
}: {
  count: number
  tipoDominante: string
}) {
  const c = COLORI[tipoDominante] ?? { c1: '#64748b', c2: '#334155' }
  const emoji = EMOJI[tipoDominante] ?? '●'
  const size = dim(count)
  return (
    <div style={{ position: 'relative', width: size, height: size, cursor: 'pointer' }}>
      <div style={{
        width: size,
        height: size,
        borderRadius: '50%',
        background: `linear-gradient(135deg, ${c.c1}, ${c.c2})`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: size * 0.4,
        boxShadow: '0 2px 8px rgba(0,0,0,0.35)',
        border: '2px solid rgba(255,255,255,0.2)',
      }}>
        {emoji}
      </div>
      <div style={{
        position: 'absolute',
        top: -4,
        right: -4,
        background: 'white',
        color: '#0a2e26',
        borderRadius: '50%',
        minWidth: 20,
        height: 20,
        padding: '0 3px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 11,
        fontWeight: 700,
        boxShadow: '0 1px 4px rgba(0,0,0,0.3)',
        lineHeight: 1,
      }}>
        {count}
      </div>
    </div>
  )
}
