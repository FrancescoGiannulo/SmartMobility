import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map,
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

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta:  '#2196f3',
  automobile:  '#e91e8c',
}

function PinMezzo({ tipo }: { tipo: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = tipo === 'monopattino' ? '🛴' : tipo === 'bicicletta' ? '🚲' : '🚗'
  return (
    <div style={{
      background: colore,
      borderRadius: '50%',
      width: 36,
      height: 36,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 18,
      boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
      border: '2px solid #fff',
    }}>
      {emoji}
    </div>
  )
}

interface ZonaHover {
  zona: ZonaMappa
  pos: google.maps.LatLngLiteral
}

export default function VistaMappa() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [centro, setCentro] = useState(CENTRO_DEFAULT)
  const [errore, setErrore] = useState('')
  const [zonaHover, setZonaHover] = useState<ZonaHover | null>(null)

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
        <h2>🚲 SMART MOBILITY</h2>
        <button className="btn-logout-mappa" onClick={handleLogout}>LOGOUT</button>
      </div>

      <Map
        className="mappa-container"
        defaultCenter={centro}
        defaultZoom={14}
        mapId="mappa-utente"
        gestureHandling="greedy"
        disableDefaultUI={false}
        style={{ paddingTop: 56 }}
      >
        {mezzi.map(m => (
          <AdvancedMarker
            key={m.id}
            position={{ lat: m.lat, lng: m.lng }}
            onClick={() => navigate(`/utente/corsa/${m.id}`, { state: { mezzo: m } })}
          >
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
              onHover={(zona, pos) => setZonaHover({ zona, pos })}
              onHoverEnd={() => setZonaHover(null)}
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
      </Map>

      {errore && <div className="mappa-errore">{errore}</div>}
      {!errore && mezzi.length === 0 && (
        <div className="mappa-nessun-mezzo">Nessun mezzo disponibile nelle vicinanze</div>
      )}
    </div>
  )
}

