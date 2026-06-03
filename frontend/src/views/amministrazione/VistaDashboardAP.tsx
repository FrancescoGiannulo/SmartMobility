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
import './VistaDashboardAP.css'

const CENTRO_DEFAULT = { lat: 41.1177, lng: 16.8719 }

const COLORI_MEZZO: Record<string, string> = {
  monopattino: '#4caf9a',
  bicicletta: '#2196f3',
  automobile: '#e91e8c',
}
const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

type VistaMode = 'pin' | 'cluster' | 'heatmap'

function KpiCard({ label, valore, colore }: { label: string; valore: number | string; colore: string }) {
  return (
    <div className="kpi-card">
      <span className="kpi-valore" style={{ color: colore }}>{valore}</span>
      <span className="kpi-label">{label}</span>
    </div>
  )
}

const RAGGIO = 38
const STROKE = 8
const CIRCONFERENZA = 2 * Math.PI * RAGGIO

function GaugeMezzi({ perc }: { perc: number }) {
  const offset = CIRCONFERENZA - (perc / 100) * CIRCONFERENZA
  const colore = perc >= 60 ? '#4caf9a' : perc >= 30 ? '#ff9800' : '#f44336'
  return (
    <div className="gauge-container">
      <svg width={96} height={96} viewBox="0 0 96 96">
        <circle cx={48} cy={48} r={RAGGIO} fill="none" stroke="#e8ecef" strokeWidth={STROKE} />
        <circle
          cx={48} cy={48} r={RAGGIO} fill="none"
          stroke={colore} strokeWidth={STROKE}
          strokeDasharray={CIRCONFERENZA}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          style={{ transition: 'stroke-dashoffset 0.5s ease, stroke 0.5s ease' }}
        />
        <text x={48} y={45} textAnchor="middle" fontSize={15} fontWeight={800} fill="#0f172a">{perc}%</text>
        <text x={48} y={61} textAnchor="middle" fontSize={8} fontWeight={600} fill="#94a3b8">DISPONIBILI</text>
      </svg>
    </div>
  )
}

function PinMezzo({ tipo, stato }: { tipo: string; stato: string }) {
  const colore = COLORI_MEZZO[tipo] ?? '#888'
  const emoji = EMOJI_MEZZO[tipo] ?? '●'
  return (
    <div style={{
      background: colore,
      opacity: stato === 'Disponibile' ? 1 : 0.45,
      borderRadius: '50%',
      width: 32, height: 32,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
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
  const [vistaMode, setVistaMode] = useState<VistaMode>('pin')
  const [layerAttivi, setLayerAttivi] = useState<Set<string>>(
    new Set(['monopattino', 'bicicletta', 'automobile'])
  )
  const [zonaSelezionata, setZonaSelezionata] = useState<ZonaMappa | null>(null)
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
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
    totale: mezzi.length,
    disponibili: mezzi.filter(m => m.stato === 'Disponibile').length,
    inUso: mezzi.filter(m => m.stato === 'In uso').length,
    manutenzione: mezzi.filter(
      m => ['In manutenzione', 'Fuori servizio', 'In pausa'].includes(m.stato)
    ).length,
  }), [mezzi])

  const percDisponibili = kpi.totale > 0
    ? Math.round((kpi.disponibili / kpi.totale) * 100)
    : 0

  const conteggiPerTipo = useMemo(() => ({
    monopattino: mezzi.filter(m => m.tipo === 'monopattino').length,
    bicicletta: mezzi.filter(m => m.tipo === 'bicicletta').length,
    automobile: mezzi.filter(m => m.tipo === 'automobile').length,
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

  if (vista === 'report') {
    return <VistaReportAP onIndietro={() => setVista('mappa')} />
  }

  const errVal = errore ? '—' : undefined

  return (
    <div className="vista-dashboard-ap">
      <div className="dashboard-ap-topbar">
        <h2>🚲 SMART MOBILITY: Amministrazione Pubblica</h2>
        <button type="button" className="btn-logout-ap" onClick={handleLogout}>LOGOUT</button>
      </div>

      <div className="dashboard-ap-kpi">
        <KpiCard label="Totale" valore={errVal ?? kpi.totale} colore="#64748b" />
        <KpiCard label="Disponibili" valore={errVal ?? kpi.disponibili} colore="#4caf9a" />
        <KpiCard label="In uso" valore={errVal ?? kpi.inUso} colore="#2196f3" />
        <KpiCard label="Non disponibili" valore={errVal ?? kpi.manutenzione} colore="#ff9800" />
      </div>

      <div className="dashboard-ap-body">
        {errore && <div className="dashboard-ap-errore">{errore}</div>}

        <div className="dashboard-ap-mappa">
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

        <div className="dashboard-ap-pannello">
          <div className="logo">SMART MOBILITY</div>

          <GaugeMezzi perc={percDisponibili} />

          <div className="pannello-sezione">
            <div className="pannello-sezione-titolo">Vista mappa</div>
            <div className="vista-toggle">
              {(['pin', 'cluster', 'heatmap'] as VistaMode[]).map(mode => (
                <button
                  key={mode}
                  type="button"
                  className={`btn-vista${vistaMode === mode ? ' attivo' : ''}`}
                  onClick={() => setVistaMode(mode)}
                >
                  {mode === 'pin' ? '📍 Pin' : mode === 'cluster' ? '⬤ Cluster' : '🔥 Heatmap'}
                </button>
              ))}
            </div>
          </div>

          <div className="pannello-sezione">
            <div className="pannello-sezione-titolo">Filtra tipo mezzo</div>
            <div className="chips-tipo">
              {[
                { tipo: 'monopattino', emoji: '🛴', colore: '#4caf9a' },
                { tipo: 'bicicletta', emoji: '🚲', colore: '#2196f3' },
                { tipo: 'automobile', emoji: '🚗', colore: '#e91e8c' },
              ].map(({ tipo, emoji, colore }) => {
                const attivo = layerAttivi.has(tipo)
                return (
                  <button
                    key={tipo}
                    type="button"
                    className={`chip-tipo${attivo ? ' attivo' : ''}`}
                    style={attivo ? { background: colore, borderColor: colore } : undefined}
                    onClick={() => toggleLayer(tipo)}
                  >
                    <span className="chip-emoji">{emoji}</span>
                    <span className="chip-label">{tipo}</span>
                    <span className="chip-badge">
                      {conteggiPerTipo[tipo as keyof typeof conteggiPerTipo]}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          <button type="button" className="btn-pannello-ap" onClick={() => setVista('report')}>
            📊 VISUALIZZA REPORT
          </button>
        </div>
      </div>
    </div>
  )
}
