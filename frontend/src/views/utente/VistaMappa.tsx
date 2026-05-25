import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  Map,
  AdvancedMarker,
  InfoWindow,
} from '@vis.gl/react-google-maps'
import { getMezziUtente, getZoneUtente, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { sbloccaMezzo } from '../../services/CorsaService'
import { prenotaMezzo, type Prenotazione } from '../../services/PrenotazioneService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import TooltipZona from '../../components/TooltipZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import './VistaMappa.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const MEZZI_MOCK: MezzoMappa[] = [
  { id: 'aaaaaaaa-0001-0001-0001-000000000001', codice: 'SM-001', tipo: 'monopattino', stato: 'Disponibile', lat: 41.1180, lng: 16.8720, batteria: 85 },
  { id: 'aaaaaaaa-0002-0002-0002-000000000002', codice: 'BK-002', tipo: 'bicicletta',  stato: 'Disponibile', lat: 41.1165, lng: 16.8710, batteria: 60 },
  { id: 'aaaaaaaa-0003-0003-0003-000000000003', codice: 'CAR-003', tipo: 'automobile', stato: 'Disponibile', lat: 41.1190, lng: 16.8740, batteria: 90 },
  { id: 'aaaaaaaa-0004-0004-0004-000000000004', codice: 'SM-004', tipo: 'monopattino', stato: 'Disponibile', lat: 41.1155, lng: 16.8730, batteria: 30 },
]

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
      width: 40,
      height: 40,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 20,
      boxShadow: '0 2px 8px rgba(0,0,0,0.35)',
      border: '3px solid #fff',
      cursor: 'pointer',
    }}>
      {emoji}
    </div>
  )
}

function Batteria({ valore }: { valore: number | null }) {
  if (valore == null) return <span className="batteria-nd">—</span>
  const barre = Math.min(4, Math.ceil(valore / 25))
  const colore = valore > 50 ? '#4caf9a' : valore > 20 ? '#f59e0b' : '#ef4444'
  return (
    <span className="batteria-barre">
      {[1, 2, 3, 4].map(i => (
        <span key={i} className="batteria-barra" style={{
          height: 6 + i * 4,
          background: i <= barre ? colore : '#e0e0e0',
        }} />
      ))}
    </span>
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
  const [mezzoSelezionato, setMezzoSelezionato] = useState<MezzoMappa | null>(null)
  const [sbloccoInCorso, setSbloccoInCorso] = useState(false)
  const [prenotaInCorso, setPrenotaInCorso] = useState(false)
  const [prenotazione, setPrenotazione] = useState<Prenotazione | null>(null)
  const [tempoRimanente, setTempoRimanente] = useState(0)
  const [errorePanel, setErrorePanel] = useState('')

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      pos => setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => {}
    )
    getZoneUtente().then(setZone).catch(() => {})

    const aggiornaMezzi = () =>
      getMezziUtente()
        .then(m => setMezzi(m.length > 0 ? m : MEZZI_MOCK))
        .catch(() => setErrore('Impossibile caricare la mappa. Riprova.'))

    aggiornaMezzi()
    const t = setInterval(aggiornaMezzi, 10_000)
    return () => clearInterval(t)
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  useEffect(() => {
    if (!prenotazione) return
    const aggiorna = () => {
      const diff = Math.max(0, Math.floor((new Date(prenotazione.scade_at).getTime() - Date.now()) / 1000))
      setTempoRimanente(diff)
    }
    aggiorna()
    const t = setInterval(aggiorna, 1000)
    return () => clearInterval(t)
  }, [prenotazione])

  const chiudiPanel = useCallback(() => {
    setMezzoSelezionato(null)
    setPrenotazione(null)
    setErrorePanel('')
  }, [])

  const handlePrenota = useCallback(async () => {
    if (!mezzoSelezionato) return
    setPrenotaInCorso(true)
    setErrorePanel('')
    try {
      const pren = await prenotaMezzo(mezzoSelezionato.id)
      setPrenotazione(pren)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErrorePanel('Mezzo non più disponibile.')
      } else if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrorePanel('Mezzo non trovato.')
      } else {
        setErrorePanel('Errore durante la prenotazione. Riprova.')
      }
    } finally {
      setPrenotaInCorso(false)
    }
  }, [mezzoSelezionato])

  const handleSblocca = useCallback(async () => {
    if (!mezzoSelezionato) return
    setSbloccoInCorso(true)
    setErrorePanel('')
    try {
      const corsa = await sbloccaMezzo(mezzoSelezionato.id)
      navigate(`/utente/corsa/${mezzoSelezionato.id}`, { state: { mezzo: mezzoSelezionato, corsa } })
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErrorePanel('Mezzo non più disponibile.')
      } else if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrorePanel('Mezzo non trovato.')
      } else {
        setErrorePanel('Errore durante lo sblocco. Riprova.')
      }
    } finally {
      setSbloccoInCorso(false)
    }
  }, [mezzoSelezionato, navigate])

  const tipoLabel = (tipo: string) =>
    tipo.charAt(0).toUpperCase() + tipo.slice(1)

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
        onClick={chiudiPanel}
      >
        {mezzi.map(m => (
          <AdvancedMarker
            key={m.id}
            position={{ lat: m.lat, lng: m.lng }}
            onClick={() => { setMezzoSelezionato(m); setErrorePanel('') }}
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

      {/* Pannello mezzo — stile mockup 5 */}
      {mezzoSelezionato && (
        <div className="pannello-mezzo">
          <div className="pannello-header">
            <span className="pannello-titolo">Sblocca/Prenota mezzo</span>
            <button className="pannello-chiudi" onClick={chiudiPanel}>✕</button>
          </div>
          <div className="pannello-separatore" />

          <p className="pannello-tipo">{tipoLabel(mezzoSelezionato.tipo)}:</p>
          <div className="pannello-mezzo-row">
            <span className="pannello-emoji">
              {mezzoSelezionato.tipo === 'monopattino' ? '🛴'
               : mezzoSelezionato.tipo === 'bicicletta' ? '🚲' : '🚗'}
            </span>
            <span className="pannello-codice">{mezzoSelezionato.codice}</span>
            <Batteria valore={mezzoSelezionato.batteria} />
          </div>

          {errorePanel ? (
            <p className="pannello-errore">{errorePanel}</p>
          ) : prenotazione ? (
            <p className="pannello-info pannello-prenotato">
              ✅ Prenotato! Hai <strong>{Math.floor(tempoRimanente / 60)}:{String(tempoRimanente % 60).padStart(2, '0')}</strong> per raggiungere il mezzo.
            </p>
          ) : (
            <p className="pannello-info">Premi <em>Sblocca</em> per iniziare subito, oppure <em>Prenota</em> per riservarlo.</p>
          )}

          <div className="pannello-azioni">
            <button
              className="btn-prenota"
              onClick={handlePrenota}
              disabled={prenotaInCorso || !!prenotazione}
            >
              {prenotaInCorso ? '...' : prenotazione ? 'Prenotato' : 'Prenota'}
            </button>
            <button className="btn-sblocca-panel" onClick={handleSblocca} disabled={sbloccoInCorso}>
              {sbloccoInCorso ? '...' : 'Sblocca'}
            </button>
          </div>
        </div>
      )}

      {errore && <div className="mappa-errore">{errore}</div>}
    </div>
  )
}
