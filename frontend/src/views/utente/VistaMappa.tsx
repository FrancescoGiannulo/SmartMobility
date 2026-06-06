import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  Map as GoogleMap,
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

function Batteria({ valore }: { valore: number | null }) {
  if (valore == null) return <span className="batteria-nd">N/D</span>
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
  const [mezzoSelezionato, setMezzoSelezionato] = useState<MezzoMappa | null>(null)
  const [sbloccoInCorso, setSbloccoInCorso] = useState(false)
  const [prenotaInCorso, setPrenotaInCorso] = useState(false)
  const [prenotazione, setPrenotazione] = useState<Prenotazione | null>(null)
  const [tempoRimanente, setTempoRimanente] = useState(0)
  const [errorePanel, setErrorePanel] = useState('')
  // [IF-UT.01] Priority queue: mantiene tutte le zone sotto il cursore, mostra quella più specifica
  const zoneAttive = useRef(new Map<string, ZonaHover>())

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      pos => setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => {}
    )
    getZoneUtente().then(setZone).catch(() => {})

    const aggiornaMezzi = () =>
      getMezziUtente()
        .then(setMezzi)
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
        <h2>Smart Mobility</h2>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button type="button" className="btn-logout-mappa" style={{ fontSize: 13 }} onClick={() => navigate('/utente/segnalazione')}>Segnala</button>
          <button type="button" className="btn-logout-mappa" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <GoogleMap
        className="mappa-container"
        defaultCenter={centro}
        defaultZoom={14}
        mapId="mappa-utente"
        gestureHandling="greedy"
        disableDefaultUI={false}
        style={{ paddingTop: 88 }}
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

      {/* Pannello mezzo — stile mockup 5 */}
      {mezzoSelezionato && (
        <div className="pannello-mezzo">
          <div className="pannello-header">
            <span className="pannello-titolo">Sblocca/Prenota mezzo</span>
            <button type="button" className="pannello-chiudi" onClick={chiudiPanel}>✕</button>
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
              type="button"
              className="btn-prenota"
              onClick={handlePrenota}
              disabled={prenotaInCorso || !!prenotazione}
            >
              {prenotaInCorso ? '...' : prenotazione ? 'Prenotato' : 'Prenota'}
            </button>
            <button type="button" className="btn-sblocca-panel" onClick={handleSblocca} disabled={sbloccoInCorso}>
              {sbloccoInCorso ? '...' : 'Sblocca'}
            </button>
          </div>
        </div>
      )}

      {errore && <div className="mappa-errore">{errore}</div>}
    </div>
  )
}
