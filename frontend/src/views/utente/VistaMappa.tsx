import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map as GoogleMap,
  AdvancedMarker,
  InfoWindow,
} from '@vis.gl/react-google-maps'
import { getMezziUtente, getZoneUtente, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import TooltipZona from '../../components/TooltipZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import './VistaMappa.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, { c1: string; c2: string }> = {
  monopattino: { c1: '#4caf9a', c2: '#2a7a6a' },
  bicicletta:  { c1: '#3b82f6', c2: '#1d4ed8' },
  automobile:  { c1: '#ec4899', c2: '#be185d' },
}

const GLYPH_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

function PinMezzo({ tipo, dim }: { tipo: string; dim?: boolean }) {
  const c = COLORI_MEZZO[tipo] ?? { c1: '#64748b', c2: '#334155' }
  const glyph = GLYPH_MEZZO[tipo] ?? '●'
  return (
    <div
      className={`sm-pin${dim ? ' sm-pin--dim' : ''}`}
      style={{ ['--sm-c1' as string]: c.c1, ['--sm-c2' as string]: c.c2 }}
    >
      <div className="sm-pin__body">
        <span className="sm-pin__icon">{glyph}</span>
      </div>
    </div>
  )
}

interface ZonaHover {
  zona: ZonaMappa
  pos: google.maps.LatLngLiteral
}

const PRIORITA_TIPO: Record<string, number> = {
  operativa: 0, parcheggio: 1, limitata: 2, vietata: 3,
}

function zonaMiglioreDa(map: Map<string, ZonaHover>): ZonaHover | null {
  let best: ZonaHover | null = null
  for (const entry of map.values()) {
    if (!best || (PRIORITA_TIPO[entry.zona.tipo] ?? 1) > (PRIORITA_TIPO[best.zona.tipo] ?? 1)) {
      best = entry
    }
  }
  return best
}

export default function VistaMappa() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [centro, setCentro] = useState(CENTRO_DEFAULT)
  const [errore, setErrore] = useState('')
  const [zonaHover, setZonaHover] = useState<ZonaHover | null>(null)
  // [IF-UT.01] Priority queue: mantiene tutte le zone sotto il cursore, mostra quella più specifica
  const zoneAttive = useRef(new Map<string, ZonaHover>())

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      pos => setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => {}
    )
    Promise.all([getMezziUtente(), getZoneUtente()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => setErrore('Impossibile caricare la mappa. Riprova.'))
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  return (
    <div className="vista-mappa">
      <div className="mappa-topbar">
        <h2>Smart Mobility</h2>
        <button className="btn-logout-mappa" onClick={handleLogout}>Logout</button>
      </div>

      <GoogleMap
        className="mappa-container"
        defaultCenter={centro}
        defaultZoom={14}
        mapId="mappa-utente"
        gestureHandling="greedy"
        disableDefaultUI={false}
        style={{ paddingTop: 88 }}
      >
        {mezzi.map(m => (
          <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
            <PinMezzo tipo={m.tipo} />
          </AdvancedMarker>
        ))}

        {zone.map(z => {
          const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
          return (
            <ZonaPoligono
              key={z.id}
              zona={z}
              fillColor={colori.fill}
              strokeColor={colori.stroke}
              onHover={(zona, pos) => {
                zoneAttive.current.set(zona.id, { zona, pos })
                setZonaHover(zonaMiglioreDa(zoneAttive.current))
              }}
              onHoverEnd={() => {
                zoneAttive.current.delete(z.id)
                setZonaHover(zonaMiglioreDa(zoneAttive.current))
              }}
            />
          )
        })}

        {zonaHover && (
          <InfoWindow
            position={zonaHover.pos}
            onCloseClick={() => setZonaHover(null)}
          >
            <TooltipZona zona={zonaHover.zona} />
          </InfoWindow>
        )}
      </GoogleMap>

      {errore && <div className="mappa-errore">{errore}</div>}
      {!errore && mezzi.length === 0 && (
        <div className="mappa-nessun-mezzo">Nessun mezzo disponibile nelle vicinanze</div>
      )}
    </div>
  )
}

