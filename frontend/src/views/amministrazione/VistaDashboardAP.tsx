import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Map, AdvancedMarker } from '@vis.gl/react-google-maps'
import { getMezziAP, getZoneAP, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import TooltipZona from '../../components/TooltipZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import VistaReportAP from './VistaReportAP'
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta:  '#2196f3',
  automobile:  '#e91e8c',
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = tipo === 'monopattino' ? '🛴' : tipo === 'bicicletta' ? '🚲' : '🚗'
  const opacita = stato === 'Disponibile' ? 1 : 0.45
  return (
    <div style={{
      background: colore,
      opacity: opacita,
      borderRadius: '50%',
      width: 32,
      height: 32,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 16,
      boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
      border: '2px solid #fff',
    }}>
      {emoji}
    </div>
  )
}

export default function VistaDashboardAP() {
  const navigate = useNavigate()
  const [vista, setVista] = useState<'mappa' | 'report'>('mappa')
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [tooltipZona, setTooltipZona] = useState<{ zona: ZonaMappa; pos: google.maps.LatLngLiteral } | null>(null)
  const [errore, setErrore] = useState('')

  useEffect(() => {
    Promise.all([getMezziAP(), getZoneAP()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => setErrore('Impossibile caricare i dati della mappa. Riprova.'))
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  if (vista === 'report') {
    return <VistaReportAP onIndietro={() => setVista('mappa')} />
  }

  return (
    <div className="vista-dashboard-ap">
      <div className="dashboard-ap-topbar">
        <h2>🚲 SMART MOBILITY — Amministrazione Pubblica</h2>
        <button className="btn-logout-ap" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="dashboard-ap-body">
        {errore && (
          <div style={{
            position: 'absolute',
            top: 72,
            left: '35%',
            transform: 'translateX(-50%)',
            background: '#fff',
            borderRadius: 12,
            padding: '12px 20px',
            boxShadow: '0 2px 12px rgba(0,0,0,0.15)',
            fontSize: 14,
            color: '#d32f2f',
            zIndex: 20,
          }}>
            {errore}
          </div>
        )}
        <div className="dashboard-ap-mappa">
          <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={CENTRO_DEFAULT}
            defaultZoom={14}
            mapId="mappa-ap"
            gestureHandling="greedy"
          >
            {mezzi.map(m => (
              <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
                <PinMezzo tipo={m.tipo} stato={m.stato} />
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
                  onHover={(zona, pos) => setTooltipZona({ zona, pos })}
                  onHoverEnd={() => setTooltipZona(null)}
                />
              )
            })}

            {tooltipZona && (
              <TooltipZona zona={tooltipZona.zona} />
            )}
          </Map>
        </div>

        <div className="dashboard-ap-pannello">
          <div className="logo">SMART MOBILITY</div>
          <button className="btn-pannello-ap" onClick={() => setVista('report')}>
            📊 VISUALIZZA REPORT
          </button>
        </div>
      </div>
    </div>
  )
}
