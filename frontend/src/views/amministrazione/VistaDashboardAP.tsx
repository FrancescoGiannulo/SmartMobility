// frontend/src/views/amministrazione/VistaDashboardAP.tsx
// [IF-AP.03] Dashboard mappa Amministrazione Pubblica
import { useEffect, useState, useCallback, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { Map, AdvancedMarker } from '@vis.gl/react-google-maps'
import { getMezziAP, getZoneAP, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { logout } from '../../services/AuthService'
import ZonaPoligono from '../../components/ZonaPoligono'
import HeatmapLayerAP from '../../components/HeatmapLayerAP'
import ClusterLayerAP from '../../components/ClusterLayerAP'
import PopupStatsZona from '../../components/PopupStatsZona'
import { COLORI_ZONA } from '../../utils/coloriZona'
import VistaReportAP from './VistaReportAP'
import { esportaCSV } from '../../services/ReportService'
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#5FF0C4',
  bicicletta:  '#7fb4ff',
  automobile:  '#FF8A7A',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta:  '🚲',
  automobile:  '🚗',
}

type VistaMode = 'pin' | 'cluster' | 'heatmap'

const CHIP_CONFIG = [
  { tipo: 'monopattino', emoji: '🛴' },
  { tipo: 'bicicletta',  emoji: '🚲' },
  { tipo: 'automobile',  emoji: '🚗' },
] as const

const RAGGIO = 38
const STROKE = 8
const CIRCONFERENZA = 2 * Math.PI * RAGGIO

function GaugeMezzi({ perc }: { perc: number }) {
  const offset = CIRCONFERENZA - (perc / 100) * CIRCONFERENZA
  // Remap: green >= 60, orange >= 30, red < 30
  const colore = perc >= 60 ? '#5FF0C4' : perc >= 30 ? '#FFC971' : '#FF8A7A'
  return (
    <div className="ap-gauge-container">
      <svg width={140} height={140} viewBox="0 0 96 96">
        <circle cx={48} cy={48} r={RAGGIO} fill="none" stroke="#163832" strokeWidth={STROKE} />
        <circle
          cx={48} cy={48} r={RAGGIO} fill="none"
          stroke={colore} strokeWidth={STROKE}
          strokeDasharray={CIRCONFERENZA}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          style={{ transition: 'stroke-dashoffset 0.5s ease, stroke 0.5s ease' }}
        />
        <text x={48} y={45} textAnchor="middle" fontSize={15} fontWeight={800} fill="#DAF1DE">{perc}%</text>
        <text x={48} y={61} textAnchor="middle" fontSize={8} fontWeight={600} fill="#5d7a6a">DISPONIBILI</text>
      </svg>
    </div>
  )
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#8EB69B'
  const emoji  = EMOJI_MEZZO[tipo]  ?? '●'
  return (
    <div style={{
      background: colore,
      opacity: stato === 'Disponibile' ? 1 : 0.45,
      borderRadius: '50%',
      width: 32, height: 32,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 16,
      boxShadow: '0 2px 6px rgba(0,0,0,0.5)',
      border: '2px solid rgba(11,43,38,0.4)',
    }}>
      {emoji}
    </div>
  )
}

export default function VistaDashboardAP() {
  const navigate = useNavigate()
  const [vista, setVista] = useState<'mappa' | 'report'>('mappa')
  const [vistaMode, setVistaMode] = useState<VistaMode>('pin')
  const [layerAttivi, setLayerAttivi] = useState<Set<string>>(
    new Set(['monopattino', 'bicicletta', 'automobile'])
  )
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const [mezzi, setMezzi]   = useState<MezzoMappa[]>([])
  const [zone, setZone]     = useState<ZonaMappa[]>([])
  const [errore, setErrore] = useState('')

  useEffect(() => {
    Promise.all([getMezziAP(), getZoneAP()])
      .then(([m, z]) => { setMezzi(m); setZone(z) })
      .catch(() => setErrore('Impossibile caricare i dati della mappa. Riprova.'))
  }, [])

  const mezziVisibili = useMemo(
    () => mezzi.filter(m => layerAttivi.has(m.tipo)),
    [mezzi, layerAttivi]
  )

  const kpi = useMemo(() => ({
    disponibili:  mezzi.filter(m => m.stato === 'Disponibile').length,
    inUso:        mezzi.filter(m => m.stato === 'In uso').length,
    manutenzione: mezzi.filter(
      m => ['In manutenzione', 'Fuori servizio', 'In pausa'].includes(m.stato)
    ).length,
  }), [mezzi])

  const percDisponibili = mezzi.length > 0
    ? Math.round((kpi.disponibili / mezzi.length) * 100)
    : 0

  const conteggiPerTipo = useMemo(() => ({
    monopattino: mezzi.filter(m => m.tipo === 'monopattino').length,
    bicicletta:  mezzi.filter(m => m.tipo === 'bicicletta').length,
    automobile:  mezzi.filter(m => m.tipo === 'automobile').length,
  }), [mezzi])

  const toggleLayer = useCallback((tipo: string) => {
    setLayerAttivi(prev => {
      const next = new Set(prev)
      next.has(tipo) ? next.delete(tipo) : next.add(tipo)
      return next
    })
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  const errVal = errore ? '—' : undefined

  return (
    <div className="vista-dashboard-ap">

      {/* ── Left sidebar ── */}
      <div className="ap-sidebar">
        <div className="ap-sidebar-logo"><img src="/logo.png" alt="Smart Mobility" style={{ width: 52, height: 'auto' }} /></div>

        <div
          className={`ap-nav-item${vista === 'mappa' ? ' attivo' : ''}`}
          role="button"
          tabIndex={0}
          onClick={() => setVista('mappa')}
          onKeyDown={e => e.key === 'Enter' && setVista('mappa')}
        >
          <span className="ap-nav-icon">🗺️</span>
          <span className="ap-nav-label">Mappa</span>
        </div>

        <div
          className={`ap-nav-item${vista === 'report' ? ' attivo' : ''}`}
          role="button"
          tabIndex={0}
          onClick={() => setVista('report')}
          onKeyDown={e => e.key === 'Enter' && setVista('report')}
        >
          <span className="ap-nav-icon">📊</span>
          <span className="ap-nav-label">Report</span>
        </div>

        <div className="ap-nav-bottom">
          <span className="ap-nav-badge">AP</span>
          <button type="button" className="ap-nav-logout" onClick={handleLogout}>Esci</button>
        </div>
      </div>

      {/* ── Main area ── */}
      <div className="ap-main">

        {/* Topbar */}
        <div className="ap-topbar">
          <span className="ap-topbar-title">
            {vista === 'mappa' ? 'Dashboard Mappa' : 'Report Settimanale'}
          </span>

          {vista === 'mappa' && (
            <div className="ap-kpi-pills">
              <span className="ap-kpi-pill ap-kpi-pill--dispo">
                <strong>{errVal ?? kpi.disponibili}</strong>{' '}
                <span>disp</span>
              </span>
              <span className="ap-kpi-divider">|</span>
              <span className="ap-kpi-pill ap-kpi-pill--uso">
                <strong>{errVal ?? kpi.inUso}</strong>{' '}
                <span>uso</span>
              </span>
              <span className="ap-kpi-divider">|</span>
              <span className="ap-kpi-pill ap-kpi-pill--man">
                <strong>{errVal ?? kpi.manutenzione}</strong>{' '}
                <span>man</span>
              </span>
            </div>
          )}

          {vista === 'report' && (
            <div className="ap-topbar-actions">
              <button type="button" className="btn-export-csv" onClick={() => esportaCSV()}>CSV</button>
              <button type="button" className="btn-export-pdf" onClick={() => window.print()}>PDF</button>
            </div>
          )}
        </div>

        {/* Content: Mappa or Report */}
        {vista === 'mappa' ? (
          <div className="ap-body">
            {errore && <div className="ap-errore">{errore}</div>}

            <div className="ap-mappa">
              <Map
                style={{ width: '100%', height: '100%' }}
                defaultCenter={CENTRO_DEFAULT}
                defaultZoom={14}
                mapId="mappa-ap"
                gestureHandling="greedy"
              >
                {zone.map(z => {
                  const colori = COLORI_ZONA[z.tipo] ?? COLORI_ZONA.operativa
                  return (
                    <ZonaPoligono
                      key={z.id}
                      zona={z}
                      fillColor={colori.fill}
                      strokeColor={colori.stroke}
                      onClick={zona => setZonaSelezionata(
                        prev => prev?.id === zona.id ? null : zona
                      )}
                    />
                  )
                })}

                {zonaSelezionata && (
                  <PopupStatsZona
                    zona={zonaSelezionata}
                    mezziVisibili={mezziVisibili}
                    onChiudi={() => setZonaSelezionata(null)}
                  />
                )}

                {vistaMode === 'pin' && mezziVisibili.map(m => (
                  <AdvancedMarker key={m.id} position={{ lat: m.lat, lng: m.lng }}>
                    <PinMezzo tipo={m.tipo} stato={m.stato} />
                  </AdvancedMarker>
                ))}

                {vistaMode === 'heatmap' && <HeatmapLayerAP mezzi={mezziVisibili} />}
                {vistaMode === 'cluster' && <ClusterLayerAP mezzi={mezziVisibili} />}
              </Map>
            </div>

            <div className="ap-pannello">
              <GaugeMezzi perc={percDisponibili} />

              <div className="ap-pannello-sezione">
                <div className="ap-pannello-label">Vista</div>
                {(['pin', 'cluster', 'heatmap'] as VistaMode[]).map(mode => (
                  <button
                    key={mode}
                    type="button"
                    className={`ap-vista-btn${vistaMode === mode ? ' attivo' : ''}`}
                    onClick={() => setVistaMode(mode)}
                  >
                    {mode === 'pin' ? '📍 Pin' : mode === 'cluster' ? '⬤ Cluster' : '🔥 Heatmap'}
                  </button>
                ))}
              </div>

              <div className="ap-pannello-sezione">
                <div className="ap-pannello-label">Mezzi</div>
                {CHIP_CONFIG.map(({ tipo, emoji }) => {
                  const attivo = layerAttivi.has(tipo)
                  return (
                    <button
                      key={tipo}
                      type="button"
                      className={`ap-chip-mezzo ap-chip-mezzo--${tipo}${attivo ? ' attivo' : ''}`}
                      onClick={() => toggleLayer(tipo)}
                    >
                      <span>{emoji}</span>
                      <span style={{ flex: 1, textTransform: 'capitalize' }}>{tipo}</span>
                      <span className="ap-chip-mezzo-count">
                        {conteggiPerTipo[tipo as keyof typeof conteggiPerTipo]}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        ) : (
          <VistaReportAP />
        )}
      </div>
    </div>
  )
}
