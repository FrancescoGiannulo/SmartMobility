import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map as GoogleMap,
  AdvancedMarker,
  useMap,
} from '@vis.gl/react-google-maps'
import { getMezziOperatore, getZoneOperatore, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { creaZona, eliminaZona } from '../../services/ZonaService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import { COLORI_ZONA } from '../../utils/coloriZona'
import './VistaMappaOperatore.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, { c1: string; c2: string }> = {
  monopattino: { c1: '#5FF0C4', c2: '#42A889' },
  bicicletta:  { c1: '#7fb4ff', c2: '#597EB2' },
  automobile:  { c1: '#FF8A7A', c2: '#B26155' },
}

const GLYPH_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const c = COLORI_MEZZO[tipo] ?? { c1: '#155e52', c2: '#2a7a6a' }
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

/* derive a CSS class suffix from stato string */
function statoChipClass(stato: string): string {
  const s = stato.toLowerCase().replace(/\s+/g, '-')
  if (s === 'disponibile') return 'state-chip--disp'
  if (s === 'in-uso') return 'state-chip--uso'
  if (s === 'in-pausa') return 'state-chip--pausa'
  if (s === 'in-manutenzione') return 'state-chip--man'
  if (s === 'prenotato') return 'state-chip--pren'
  if (s === 'fuori-servizio') return 'state-chip--fs'
  return ''
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
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const [eliminazione, setEliminazione] = useState(false)
  const [erroreEliminazione, setErroreEliminazione] = useState('')
  const [mezzoSelezionato, setMezzoSelezionato] = useState<MezzoMappa | null>(null)

  const ricaricaDati = useCallback(() => {
    Promise.all([getMezziOperatore(), getZoneOperatore()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => {})
  }, [])

  useEffect(() => {
    ricaricaDati()
    const t = setInterval(ricaricaDati, 2000)  // [IF-OP.01] aggiornamento posizioni mezzi in tempo reale
    return () => clearInterval(t)
  }, [ricaricaDati])

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

  /* ── KPI derivati dai dati reali ── */
  const totale   = mezzi.length
  const inUso    = mezzi.filter(m => m.stato === 'In uso').length
  const battBassa = mezzi.filter(m => m.batteria != null && m.batteria < 20).length
  const inManutenzione = mezzi.filter(m => m.stato === 'In manutenzione').length

  return (
    <div className="vista-mappa-op">
      {/* ── Left sidebar: logo + nav ── */}
      <div className="mappa-op-sidebar">
        <div className="mappa-op-sidebar-logo">
          <img src="/logo.png" alt="Smart Mobility" />
          <span className="role-tag">OP</span>
        </div>
        <SidebarRuolo ruolo="OP" />
      </div>

      {/* ── Right content column ── */}
      <div className="mappa-op-content">

        {/* Topbar */}
        <div className="mappa-op-topbar">
          <h2>
            <img src="/logo.png" alt="Smart Mobility" className="topbar-logo" />
            <span className="role-tag">Operatore</span>
          </h2>
          <button type="button" className="btn-logout-mappa" onClick={handleLogout}>Logout</button>
        </div>

        {/* KPI row */}
        <div className="mappa-op-kpis">
          <div className="mappa-op-kpi mappa-op-kpi--grad">
            <div className="kpi-label">Mezzi totali</div>
            <div className="kpi-value sm-mono">{totale}</div>
            <div className="kpi-sub">in flotta</div>
          </div>
          <div className="mappa-op-kpi">
            <div className="kpi-label">In uso ora</div>
            <div className="kpi-value sm-mono">{inUso}</div>
            <div className="kpi-sub">{totale > 0 ? `${Math.round(inUso / totale * 100)}% flotta` : '—'}</div>
          </div>
          <div className="mappa-op-kpi">
            <div className="kpi-label">Batteria &lt; 20%</div>
            <div className={`kpi-value sm-mono${battBassa > 0 ? ' kpi-value--warn' : ''}`}>{battBassa}</div>
            <div className="kpi-sub">da raccogliere</div>
          </div>
          <div className="mappa-op-kpi">
            <div className="kpi-label">In manutenzione</div>
            <div className="kpi-value sm-mono">{inManutenzione}</div>
            <div className="kpi-sub">fuori servizio</div>
          </div>
        </div>

        {/* Map + Fleet split */}
        <div className="mappa-op-body">

          {/* Map */}
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
                <AdvancedMarker
                  key={m.id}
                  position={{ lat: m.lat, lng: m.lng }}
                  onClick={e => { e.stop(); setMezzoSelezionato(m); setZonaSelezionata(null) }}
                >
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
                    onClick={tipoDisegno ? undefined : zona => {
                      setZonaSelezionata(zona)
                      setMezzoSelezionato(null)
                    }}
                  />
                )
              })}
            </GoogleMap>

            {/* Zone legend */}
            <div className="mappa-op-legenda" aria-label="Legenda zone">
              <span className="leg-item">
                <i className="leg-dot" style={{ background: COLORI_ZONA.parcheggio.stroke, opacity: .8 }} />
                Parcheggio
              </span>
              <span className="leg-item">
                <i className="leg-dot" style={{ border: '1px dashed rgba(142,182,155,.5)', background: 'transparent' }} />
                Operativa
              </span>
              <span className="leg-item">
                <i className="leg-dot" style={{ background: COLORI_ZONA.vietata.stroke, opacity: .8 }} />
                Vietata
              </span>
              <span className="leg-item">
                <i className="leg-dot" style={{ background: COLORI_ZONA.limitata.stroke, opacity: .8 }} />
                Limitata
              </span>
            </div>

            {/* Zone draw tools + info cards overlay */}
            <div className="mappa-op-zone-tools">
              {/* Mezzo info card */}
              {mezzoSelezionato && (
                <div className="mezzo-info-card">
                  <div className="mezzo-info-header">
                    <span className="mezzo-info-titolo">
                      {mezzoSelezionato.tipo === 'monopattino' ? '🛴'
                        : mezzoSelezionato.tipo === 'bicicletta' ? '🚲' : '🚗'}{' '}
                      {mezzoSelezionato.codice}
                    </span>
                    <button className="mezzo-info-chiudi" onClick={() => setMezzoSelezionato(null)} aria-label="Chiudi">✕</button>
                  </div>
                  <div className="mezzo-info-riga">
                    <span className="mezzo-info-label">Tipo</span>
                    <span>{mezzoSelezionato.tipo.charAt(0).toUpperCase() + mezzoSelezionato.tipo.slice(1)}</span>
                  </div>
                  <div className="mezzo-info-riga">
                    <span className="mezzo-info-label">Stato</span>
                    <span className={`mezzo-stato mezzo-stato--${mezzoSelezionato.stato.toLowerCase().replace(' ', '-')}`}>
                      {mezzoSelezionato.stato}
                    </span>
                  </div>
                  <div className="mezzo-info-riga">
                    <span className="mezzo-info-label">Batteria</span>
                    <span>{mezzoSelezionato.batteria != null ? `${mezzoSelezionato.batteria}%` : '—'}</span>
                  </div>
                  <div className="mezzo-info-riga">
                    <span className="mezzo-info-label">Pos.</span>
                    <span style={{ fontFamily: 'var(--ff-mono)', fontSize: 10 }}>
                      {mezzoSelezionato.lat.toFixed(4)}, {mezzoSelezionato.lng.toFixed(4)}
                    </span>
                  </div>
                </div>
              )}

              {/* Zona info card */}
              {zonaSelezionata && (
                <div className="mezzo-info-card">
                  <div className="mezzo-info-header">
                    <span className="mezzo-info-titolo">
                      {zonaSelezionata.tipo === 'vietata' ? '🚫'
                        : zonaSelezionata.tipo === 'limitata' ? '⚠️'
                        : zonaSelezionata.tipo === 'parcheggio' ? 'P'
                        : '◉'}{' '}
                      {zonaSelezionata.nome}
                    </span>
                    <button className="mezzo-info-chiudi" onClick={() => { setZonaSelezionata(null); setErroreEliminazione('') }} aria-label="Chiudi">✕</button>
                  </div>
                  <div className="mezzo-info-riga">
                    <span className="mezzo-info-label">Tipo</span>
                    <span>{zonaSelezionata.tipo.charAt(0).toUpperCase() + zonaSelezionata.tipo.slice(1)}</span>
                  </div>
                  {zonaSelezionata.limite_velocita && (
                    <div className="mezzo-info-riga">
                      <span className="mezzo-info-label">Limite</span>
                      <span>{zonaSelezionata.limite_velocita} km/h</span>
                    </div>
                  )}
                  {erroreEliminazione && <p className="info-card-error">{erroreEliminazione}</p>}
                  <button
                    className="btn-zona btn-zona--danger"
                    style={{ marginTop: 2 }}
                    onClick={handleEliminaZona}
                    disabled={eliminazione}
                  >
                    {eliminazione ? 'Eliminazione…' : 'Elimina zona'}
                  </button>
                </div>
              )}

              {/* Draw zone buttons */}
              <button type="button" className="btn-zona btn-zona--danger" onClick={() => avviaDisegno('vietata')}>
                + Zona vietata
              </button>
              <button type="button" className="btn-zona btn-zona--warn" onClick={() => avviaDisegno('limitata')}>
                + Zona limitata
              </button>
              <button type="button" className="btn-zona btn-zona--accent" onClick={() => avviaDisegno('parcheggio')}>
                + Parcheggio
              </button>
              <button type="button" className="btn-zona btn-zona--info" onClick={() => avviaDisegno('operativa')}>
                + Confine operativo
              </button>
            </div>
          </div>

          {/* Fleet table */}
          <div className="mappa-op-flotta">
            <div className="mappa-op-flotta-header">
              <span className="mappa-op-flotta-title">Stato flotta</span>
              <span className="mappa-op-flotta-count">{mezzi.length} mezzi</span>
            </div>
            <div className="mappa-op-flotta-table-wrap">
              <table className="tbl-flotta" aria-label="Lista mezzi della flotta">
                <thead>
                  <tr>
                    <th>Mezzo</th>
                    <th>Tipo</th>
                    <th>Batt.</th>
                    <th>Stato</th>
                  </tr>
                </thead>
                <tbody>
                  {mezzi.length === 0 && (
                    <tr>
                      <td colSpan={4} style={{ textAlign: 'center', color: 'var(--text-mute)', padding: '24px 12px', fontFamily: 'var(--ff-mono)', fontSize: 12 }}>
                        Nessun mezzo disponibile
                      </td>
                    </tr>
                  )}
                  {mezzi.map(m => (
                    <tr
                      key={m.id}
                      onClick={() => { setMezzoSelezionato(m); setZonaSelezionata(null) }}
                      style={{ cursor: 'pointer' }}
                      aria-label={`Mezzo ${m.codice}`}
                    >
                      <td className="mono">{m.codice}</td>
                      <td>{m.tipo.charAt(0).toUpperCase() + m.tipo.slice(1)}</td>
                      <td className={m.batteria != null && m.batteria < 20 ? 'batt-warn' : 'mono'}>
                        {m.batteria != null ? `${m.batteria}%` : '—'}
                      </td>
                      <td>
                        <span className={`state-chip ${statoChipClass(m.stato)}`}>
                          {m.stato}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Drawing hint banner */}
      {tipoDisegno && (
        <div className="mappa-op-hint">
          <span>Disegna il poligono sulla mappa: doppio click per chiudere</span>
          <button type="button" onClick={() => setTipoDisegno(null)}>Annulla</button>
        </div>
      )}

      {/* Modal: nuova zona */}
      {modalZona && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Nuova zona {modalZona.tipo}</h3>
            <input
              aria-label="Nome zona"
              placeholder="Nome zona"
              value={nomeZona}
              onChange={e => setNomeZona(e.target.value)}
            />
            {modalZona.tipo === 'limitata' && (
              <input
                type="number"
                aria-label="Limite velocità (km/h)"
                placeholder="Limite velocità (km/h)"
                value={limiteVelocita}
                onChange={e => setLimiteVelocita(e.target.value)}
                min={1}
              />
            )}
            {erroreModal && <p className="modal-errore">{erroreModal}</p>}
            <button type="button" className="sm-btn sm-btn--primary" onClick={handleConfermaZona} disabled={caricamento}>
              {caricamento ? 'Salvataggio…' : 'Salva zona'}
            </button>
            <button type="button" className="sm-btn sm-btn--ghost" onClick={() => setModalZona(null)}>
              Annulla
            </button>
          </div>
        </div>
      )}

      {/* Modal: conferma eliminazione zona */}
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
              className="sm-btn sm-btn--primary"
              style={{ background: 'var(--danger)', color: 'var(--bg)', boxShadow: 'none' }}
              onClick={handleEliminaZona}
              disabled={eliminazione}
            >
              {eliminazione ? 'Eliminazione…' : 'Elimina'}
            </button>
            <button
              type="button"
              className="sm-btn sm-btn--ghost"
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
