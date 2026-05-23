import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  APIProvider,
  Map,
  AdvancedMarker,
  Polygon,
  useMap,
} from '@vis.gl/react-google-maps'
import { getMezziOperatore, getZoneOperatore, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { creaZona } from '../../services/ZonaService'
import { logout } from '../../services/AuthService'
import './VistaMappaOperatore.css'

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string
const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_ZONA: Record<string, { fill: string; stroke: string }> = {
  vietata:    { fill: 'rgba(244,67,54,0.25)',  stroke: '#f44336' },
  limitata:   { fill: 'rgba(255,152,0,0.25)',  stroke: '#ff9800' },
  parcheggio: { fill: 'rgba(76,175,80,0.25)',  stroke: '#4caf50' },
  operativa:  { fill: 'rgba(33,150,243,0.25)', stroke: '#2196f3' },
}

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

type TipoZona = 'vietata' | 'limitata' | 'parcheggio' | 'operativa'

interface ModalZona {
  tipo: TipoZona
  coordinate: google.maps.LatLngLiteral[]
}

function DrawingManager({
  tipoAttivo,
  onCompletato,
}: {
  tipoAttivo: TipoZona | null
  onCompletato: (coords: google.maps.LatLngLiteral[]) => void
}) {
  const mappa = useMap()
  const managerRef = useRef<google.maps.drawing.DrawingManager | null>(null)

  useEffect(() => {
    if (!mappa || !window.google) return
    if (managerRef.current) {
      managerRef.current.setMap(null)
      managerRef.current = null
    }
    if (!tipoAttivo) return

    const colori = COLORI_ZONA[tipoAttivo]
    const dm = new window.google.maps.drawing.DrawingManager({
      drawingMode: window.google.maps.drawing.OverlayType.POLYGON,
      drawingControl: false,
      polygonOptions: {
        fillColor: colori.fill,
        strokeColor: colori.stroke,
        strokeWeight: 2,
        editable: false,
      },
    })
    dm.setMap(mappa)

    window.google.maps.event.addListener(dm, 'polygoncomplete', (polygon: google.maps.Polygon) => {
      const coords = polygon.getPath().getArray().map(p => ({ lat: p.lat(), lng: p.lng() }))
      polygon.setMap(null)
      dm.setMap(null)
      managerRef.current = null
      onCompletato(coords)
    })

    managerRef.current = dm
    return () => {
      dm.setMap(null)
    }
  }, [mappa, tipoAttivo, onCompletato])

  return null
}

export default function VistaMappaOperatore() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [tipoDisegno, setTipoDisegno] = useState<TipoZona | null>(null)
  const [modalZona, setModalZona] = useState<ModalZona | null>(null)
  const [nomeZona, setNomeZona] = useState('')
  const [limiteVelocita, setLimiteVelocita] = useState('')
  const [erroreModal, setErroreModal] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricaricaDati = useCallback(() => {
    Promise.all([getMezziOperatore(), getZoneOperatore()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => {})
  }, [])

  useEffect(() => { ricaricaDati() }, [ricaricaDati])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  const avviaDisegno = (tipo: TipoZona) => {
    setTipoDisegno(tipo)
    setModalZona(null)
  }

  const handlePoligonoCompletato = useCallback((coords: google.maps.LatLngLiteral[]) => {
    if (!tipoDisegno) return
    setModalZona({ tipo: tipoDisegno, coordinate: coords })
    setTipoDisegno(null)
    setNomeZona('')
    setLimiteVelocita('')
    setErroreModal('')
  }, [tipoDisegno])

  const handleConfermaZona = async () => {
    if (!modalZona) return
    if (!nomeZona.trim()) { setErroreModal('Inserisci un nome per la zona'); return }
    setCaricamento(true)
    setErroreModal('')
    try {
      const coordinate = modalZona.coordinate.map(p => [p.lng, p.lat])
      await creaZona({
        nome: nomeZona.trim(),
        tipo: modalZona.tipo,
        coordinate,
        limite_velocita: limiteVelocita ? parseInt(limiteVelocita) : null,
      })
      setModalZona(null)
      ricaricaDati()
    } catch {
      setErroreModal('Errore durante il salvataggio. Riprova.')
    } finally {
      setCaricamento(false)
    }
  }

  return (
    <div className="vista-mappa-op">
      <div className="mappa-op-topbar">
        <h2>🚲 SMART MOBILITY — Operatore</h2>
        <button className="btn-logout-mappa" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="mappa-op-body">
        <div className="mappa-op-mappa">
          <APIProvider
            apiKey={API_KEY}
            libraries={['drawing']}
          >
            <Map
              style={{ width: '100%', height: '100%' }}
              defaultCenter={CENTRO_DEFAULT}
              defaultZoom={14}
              mapId="mappa-operatore"
              gestureHandling="greedy"
            >
              <DrawingManager
                tipoAttivo={tipoDisegno}
                onCompletato={handlePoligonoCompletato}
              />

              {mezzi.map(m => (
                <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
                  <PinMezzo tipo={m.tipo} stato={m.stato} />
                </AdvancedMarker>
              ))}

              {zone.map(z => {
                const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
                const paths = z.perimetro.coordinates[0].map(([lng, lat]) => ({ lat, lng }))
                return (
                  <Polygon
                    key={z.id}
                    paths={paths}
                    strokeColor={colori.stroke}
                    strokeOpacity={1}
                    strokeWeight={2}
                    fillColor={colori.fill}
                    fillOpacity={1}
                  />
                )
              })}
            </Map>
          </APIProvider>
        </div>

        <div className="mappa-op-pannello">
          <div className="logo">SMART MOBILITY</div>

          <button className="btn-pannello" onClick={() => avviaDisegno('vietata')}>
            DEFINISCI ZONA VIETATA
          </button>
          <button className="btn-pannello" style={{ background: '#ff9800' }} onClick={() => avviaDisegno('limitata')}>
            DEFINISCI ZONA LIMITATA
          </button>
          <button className="btn-pannello" style={{ background: '#4caf50' }} onClick={() => avviaDisegno('parcheggio')}>
            DEFINISCI ZONA PARCHEGGIO
          </button>
          <button className="btn-pannello" style={{ background: '#2196f3' }} onClick={() => avviaDisegno('operativa')}>
            DEFINISCI CONFINE OPERATIVO
          </button>

          <hr style={{ border: 'none', borderTop: '1px solid #e0e0e0', margin: '4px 0' }} />

          <button className="btn-pannello secondario">GESTISCI SEGNALAZIONI</button>
          <button className="btn-pannello secondario">GESTISCI UTENTI</button>
          <button className="btn-pannello secondario">IMPOSTAZIONI REGOLE</button>
          <button className="btn-pannello secondario">TARIFFE E PROMOZIONI</button>
          <button className="btn-pannello secondario">VISUALIZZA REPORT</button>
          <button className="btn-pannello secondario">GESTISCI MEZZI</button>
        </div>
      </div>

      {tipoDisegno && (
        <div style={{
          position: 'fixed', bottom: 24, left: '35%', transform: 'translateX(-50%)',
          background: '#333', color: '#fff', borderRadius: 12, padding: '12px 20px',
          fontSize: 14, zIndex: 50, boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
        }}>
          Disegna il poligono sulla mappa — doppio click per chiudere
          <button
            onClick={() => setTipoDisegno(null)}
            style={{ marginLeft: 12, background: 'transparent', border: '1px solid #fff', color: '#fff', borderRadius: 8, padding: '2px 10px', cursor: 'pointer' }}
          >
            Annulla
          </button>
        </div>
      )}

      {modalZona && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Nuova zona {modalZona.tipo}</h3>
            <input
              placeholder="Nome zona"
              value={nomeZona}
              onChange={e => setNomeZona(e.target.value)}
              autoFocus
            />
            {modalZona.tipo === 'limitata' && (
              <input
                type="number"
                placeholder="Limite velocità (km/h)"
                value={limiteVelocita}
                onChange={e => setLimiteVelocita(e.target.value)}
                min={1}
              />
            )}
            {erroreModal && <p className="modal-errore">{erroreModal}</p>}
            <button className="btn-pannello" onClick={handleConfermaZona} disabled={caricamento}>
              {caricamento ? '...' : 'SALVA ZONA'}
            </button>
            <button className="btn-pannello secondario" onClick={() => setModalZona(null)}>
              Annulla
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
