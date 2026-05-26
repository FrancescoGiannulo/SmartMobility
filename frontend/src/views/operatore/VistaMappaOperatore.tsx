import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map as GoogleMap,
  AdvancedMarker,
  InfoWindow,
  useMap,
} from '@vis.gl/react-google-maps'
import { getMezziOperatore, getZoneOperatore, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { creaZona, eliminaZona } from '../../services/ZonaService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import TooltipZona from '../../components/TooltipZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import './VistaMappaOperatore.css'

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

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const c = COLORI_MEZZO[tipo] ?? { c1: '#64748b', c2: '#334155' }
  const glyph = GLYPH_MEZZO[tipo] ?? '●'
  const dim = stato !== 'Disponibile'
  return (
    <div
      className={`sm-pin${dim ? ' sm-pin--dim' : ''}`}
      style={{ ['--sm-c1' as string]: c.c1, ['--sm-c2' as string]: c.c2 }}
      title={`${tipo} — ${stato}`}
    >
      <div className="sm-pin__body">
        <span className="sm-pin__icon">{glyph}</span>
      </div>
    </div>
  )
}


type TipoZona = 'vietata' | 'limitata' | 'parcheggio' | 'operativa'

interface ModalZona {
  tipo: TipoZona
  coordinate: google.maps.LatLngLiteral[]
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
      window.google.maps.event.clearInstanceListeners(dm)
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
  const [zonaHover, setZonaHover] = useState<ZonaHover | null>(null)
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const zoneAttive = useRef(new Map<string, ZonaHover>())
  const [eliminazione, setEliminazione] = useState(false)
  const [erroreEliminazione, setErroreEliminazione] = useState('')

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
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number } })?.response?.status
      if (status === 422) {
        setErroreModal("La zona deve essere disegnata all'interno del confine operativo.")
      } else {
        setErroreModal('Errore durante il salvataggio. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const handleEliminaZona = async () => {
    if (!zonaSelezionata) return
    setEliminazione(true)
    setErroreEliminazione('')
    try {
      await eliminaZona(zonaSelezionata.id)
      setZonaSelezionata(null)
      ricaricaDati()
    } catch {
      setErroreEliminazione('Impossibile eliminare la zona. Riprova.')
    } finally {
      setEliminazione(false)
    }
  }

  return (
    <div className="vista-mappa-op">
      <div className="mappa-op-topbar">
        <h2>
          Smart Mobility
          <span className="role-tag">Operatore</span>
        </h2>
        <button type="button" className="btn-logout-mappa" onClick={handleLogout}>Logout</button>
      </div>

      <div className="mappa-op-body">
        <div className="mappa-op-mappa">
          <GoogleMap
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
                <TooltipZona
                  zona={zonaHover.zona}
                  onElimina={() => {
                    setZonaSelezionata(zonaHover.zona)
                    setZonaHover(null)
                  }}
                />
              </InfoWindow>
            )}
          </GoogleMap>
        </div>

        <div className="mappa-op-pannello">
          <div className="logo">Control Center</div>

          <div className="section-label">Definisci zone</div>

          <button type="button" className="btn-pannello danger" onClick={() => avviaDisegno('vietata')}>
            Zona vietata
          </button>
          <button type="button" className="btn-pannello warning" onClick={() => avviaDisegno('limitata')}>
            Zona limitata
          </button>
          <button type="button" className="btn-pannello success" onClick={() => avviaDisegno('parcheggio')}>
            Zona parcheggio
          </button>
          <button type="button" className="btn-pannello info" onClick={() => avviaDisegno('operativa')}>
            Confine operativo
          </button>

          <div className="section-label">Gestione</div>

          <button type="button" className="btn-pannello secondario">Gestisci segnalazioni</button>
          <button type="button" className="btn-pannello secondario">Gestisci utenti</button>
          <button type="button" className="btn-pannello secondario">Impostazioni regole</button>
          <button type="button" className="btn-pannello secondario">Tariffe e promozioni</button>
          <button type="button" className="btn-pannello secondario">Visualizza report</button>
          <button type="button" className="btn-pannello secondario">Gestisci mezzi</button>
        </div>
      </div>

      {tipoDisegno && (
        <div className="mappa-op-hint">
          <span>Disegna il poligono sulla mappa — doppio click per chiudere</span>
          <button type="button" onClick={() => setTipoDisegno(null)}>Annulla</button>
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
            <button type="button" className="btn-pannello" onClick={handleConfermaZona} disabled={caricamento}>
              {caricamento ? 'Salvataggio…' : 'Salva zona'}
            </button>
            <button type="button" className="btn-pannello secondario" onClick={() => setModalZona(null)}>
              Annulla
            </button>
          </div>
        </div>
      )}

      {zonaSelezionata && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Elimina zona</h3>
            <p style={{ marginBottom: 16 }}>
              Vuoi eliminare la zona <strong>{zonaSelezionata.nome}</strong>?
            </p>
            {erroreEliminazione && <p className="modal-errore">{erroreEliminazione}</p>}
            <button
              type="button"
              className="btn-pannello danger"
              onClick={handleEliminaZona}
              disabled={eliminazione}
            >
              {eliminazione ? 'Eliminazione…' : 'Elimina'}
            </button>
            <button
              type="button"
              className="btn-pannello secondario"
              onClick={() => { setZonaSelezionata(null); setErroreEliminazione('') }}
            >
              Annulla
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
