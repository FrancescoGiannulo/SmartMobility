import axios from 'axios'
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Map as GoogleMap,
  AdvancedMarker,
} from '@vis.gl/react-google-maps'
import { getMezziUtente, getZoneUtente, type MezzoMappa, type ZonaMappa } from '../../services/MapService'
import { getTariffe, getPromozioni, type Tariffa, type Promozione } from '../../services/PaymentService'
import { sbloccaMezzi } from '../../services/CorsaService'
import {
  creaPrenotazione,
  annullaPrenotazione,
  getPrenotazioniAttive,
  isRisultatiParziali,
  type Prenotazione,
} from '../../services/PrenotazioneService'
import { logout, utenteCorrente } from '../../services/AuthService'
import { getParametriUtente } from '../../services/ConfigurazioneService'
import { getSuggerimenti, generaSuggerimenti, segnaVisto, type Suggerimento } from '../../services/SuggerimentiService'
import ZonaPoligono from '../../components/ZonaPoligono'
import { COLORI_ZONA } from '../../utils/coloriZona'
import './VistaHomePageUtente.css'

const CENTRO_DEFAULT = { lat: 41.1087, lng: 16.8781 }

const COLORI_MEZZO: Record<string, { c1: string; c2: string }> = {
  monopattino: { c1: '#155e52', c2: '#2a7a6a' },
  bicicletta:  { c1: '#3b82f6', c2: '#1d4ed8' },
  automobile:  { c1: '#ec4899', c2: '#be185d' },
}

const GLYPH_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

function PinMezzo({ tipo, selected, dim }: { tipo: string; selected?: boolean; dim?: boolean }) {
  const c = COLORI_MEZZO[tipo] ?? { c1: '#64748b', c2: '#334155' }
  const glyph = GLYPH_MEZZO[tipo] ?? '●'
  return (
    <div
      className={`sm-pin${dim ? ' sm-pin--dim' : ''}${selected ? ' sm-pin--selected' : ''}`}
      style={{ ['--sm-c1' as string]: c.c1, ['--sm-c2' as string]: c.c2 }}
    >
      <div className="sm-pin__body">
        <span className="sm-pin__icon">{glyph}</span>
      </div>
      {selected && <span className="sm-pin__badge">✓</span>}
    </div>
  )
}

function Batteria({ valore }: { valore: number | null }) {
  if (valore == null) return <span className="batteria-nd">—</span>
  const barre = Math.min(4, Math.ceil(valore / 25))
  const colore = valore > 50 ? '#155e52' : valore > 20 ? '#f59e0b' : '#ef4444'
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



function formatTempoRimanente(sec: number): string {
  return `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, '0')}`
}

type SidebarSezione = 'menu' | 'prenotazioni' | 'tariffe' | 'promozioni'

export default function VistaHomePageUtente() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoMappa[]>([])
  const [zone, setZone] = useState<ZonaMappa[]>([])
  const [centro, setCentro] = useState(CENTRO_DEFAULT)
  const [posizioneReale, setPosizioneReale] = useState(false)
  const [errore, setErrore] = useState('')

  // Sidebar
  const [sidebarAperta, setSidebarAperta] = useState(false)
  const [sidebarSezione, setSidebarSezione] = useState<SidebarSezione>('menu')

  // Mezzo attivo, modalità panel e selezione
  const [mezzoAttivo, setMezzoAttivo] = useState<MezzoMappa | null>(null)
  const [modalita, setModalita] = useState<'prenota' | 'sblocca' | null>(null)
  const [selezione, setSelezione] = useState<MezzoMappa[]>([])

  // Prenotazioni
  const [prenotazioni, setPrenotazioni] = useState<Prenotazione[]>([])
  const [prenotazioniAttive, setPrenotazioniAttive] = useState<Prenotazione[]>([])
  const [mezziPrenotati, setMezziPrenotati] = useState<MezzoMappa[]>([])
  const [tempoRimanente, setTempoRimanente] = useState(0)
  const [nowMs, setNowMs] = useState(Date.now)

  // Stati azioni
  const [nonDisponibili, setNonDisponibili] = useState<string[]>([])
  const [sbloccoInCorso, setSbloccoInCorso] = useState(false)
  const [prenotaInCorso, setPrenotaInCorso] = useState(false)
  const [annullaInCorso, setAnnullaInCorso] = useState(false)
  const [errorePanel, setErrorePanel] = useState('')


  // [CS-15] Inizializzato a 1 (default DB); aggiornato subito dalla API
  const [nMax, setNMax] = useState(1)

  // [IF-UT.05] [IF-UT.13] Stato tariffe/promozioni (sidebar)
  const [tariffe, setTariffe] = useState<Tariffa[] | null>(null)
  const [promozioni, setPromozioni] = useState<Promozione[] | null>(null)
  const [loadingDrawer, setLoadingDrawer] = useState(false)
  const [erroreDrawer, setErroreDrawer] = useState('')

  // [IF-UT.14] Suggerimenti Intelligenti
  const [suggerimenti, setSuggerimenti] = useState<Suggerimento[] | null>(null)
  const [generaInCorso, setGeneraInCorso] = useState(false)
  const [erroreSuggerimenti, setErroreSuggerimenti] = useState('')

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      pos => {
        setCentro({ lat: pos.coords.latitude, lng: pos.coords.longitude })
        setPosizioneReale(true)
      },
      () => setPosizioneReale(false)
    )
    getZoneUtente().then(setZone).catch(() => {})

    const aggiornaMezzi = () =>
      getMezziUtente()
        .then(setMezzi)
        .catch(() => setErrore('Impossibile caricare la mappa. Riprova.'))

    // [CS-15] Ricarica i parametri con lo stesso intervallo dei mezzi
    const aggiornaParametri = () =>
      getParametriUtente().then(p => setNMax(p.max_mezzi_per_utente)).catch(() => {})

    aggiornaMezzi()
    aggiornaParametri()
    const t = setInterval(() => { aggiornaMezzi(); aggiornaParametri() }, 10_000)
    getPrenotazioniAttive().then(setPrenotazioniAttive).catch(() => {})
    return () => clearInterval(t)
  }, [])

  const handleLogout = useCallback(async () => {
    await logout()
    navigate('/', { replace: true })
  }, [navigate])

  // [IF-UT.05] — fetch lazy, apre drawer tariffe
  const apriTariffe = useCallback(async () => {
    setSidebarSezione('tariffe')
    if (tariffe !== null) return
    setLoadingDrawer(true)
    setErroreDrawer('')
    try {
      const r = await getTariffe()
      setTariffe(r.data)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 404) {
        setTariffe([])
      } else {
        setErroreDrawer('Impossibile caricare le tariffe.')
      }
    } finally {
      setLoadingDrawer(false)
    }
  }, [tariffe])

  // [IF-UT.13] — fetch lazy, apre drawer promozioni
  const apriPromozioni = useCallback(async () => {
    setSidebarSezione('promozioni')
    if (promozioni !== null) return
    setLoadingDrawer(true)
    setErroreDrawer('')
    try {
      const r = await getPromozioni()
      setPromozioni(r.data ?? [])
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 204) {
        setPromozioni([])
      } else {
        setErroreDrawer('Impossibile caricare le promozioni.')
      }
    } finally {
      setLoadingDrawer(false)
    }
  }, [promozioni])

  // [IF-UT.14] Suggerimenti — banner sulla mappa
  const [bannerAperto, setBannerAperto] = useState(false)

  useEffect(() => {
    getSuggerimenti()
      .then(r => { setSuggerimenti(r.data ?? []); if ((r.data ?? []).length > 0) setBannerAperto(true) })
      .catch(() => {})
  }, [])

  const handleGeneraSuggerimenti = useCallback(async () => {
    setGeneraInCorso(true)
    setErroreSuggerimenti('')
    try {
      const r = await generaSuggerimenti()
      setSuggerimenti(r.data ?? [])
      setBannerAperto(true)
    } catch {
      setErroreSuggerimenti('Errore nella generazione dei suggerimenti.')
    } finally {
      setGeneraInCorso(false)
    }
  }, [])

  const handleSegnaVisto = useCallback(async (id: string) => {
    try {
      await segnaVisto(id)
      setSuggerimenti(prev =>
        prev ? prev.map(s => s.id === id ? { ...s, stato: 'visto' as const } : s) : prev
      )
    } catch { /* ignore */ }
  }, [])

  useEffect(() => {
    const t = setInterval(() => setNowMs(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    if (prenotazioni.length === 0) return
    const prima = prenotazioni.reduce((a, b) =>
      new Date(a.scade_at) < new Date(b.scade_at) ? a : b
    )
    const aggiorna = () => {
      const diff = Math.max(0, Math.floor((new Date(prima.scade_at).getTime() - Date.now()) / 1000))
      setTempoRimanente(diff)
    }
    aggiorna()
    const t = setInterval(aggiorna, 1000)
    return () => clearInterval(t)
  }, [prenotazioni])

  const chiudiPanel = useCallback(() => {
    setMezzoAttivo(null)
    setModalita(null)
    setSelezione([])
    setErrorePanel('')
    setNonDisponibili([])
  }, [])

  const resettaSelezione = useCallback(() => {
    setSelezione([])
    setModalita(null)
    setMezzoAttivo(null)
    setErrorePanel('')
    setNonDisponibili([])
  }, [])

  const toggleSelezione = useCallback((mezzo: MezzoMappa) => {
    const giaPresente = selezione.some(m => m.id === mezzo.id)
    if (giaPresente) {
      setSelezione(prev => prev.filter(m => m.id !== mezzo.id))
    } else if (selezione.length >= nMax) {
      // limite raggiunto, ignorato silenziosamente
    } else if (selezione.length > 0 && selezione[0].tipo !== mezzo.tipo) {
      setErrorePanel(`Puoi selezionare solo mezzi dello stesso tipo (${selezione[0].tipo}).`)
      return
    } else {
      setSelezione(prev => [...prev, mezzo])
    }
    setNonDisponibili([])
    setErrorePanel('')
  }, [selezione])

  // [IF-UT.02] CS-04
  const handleConfermaPrenotazione = useCallback(async () => {
    if (selezione.length === 0) return
    setPrenotaInCorso(true)
    setErrorePanel('')
    setNonDisponibili([])
    try {
      const prens = await creaPrenotazione(selezione.map(m => m.id))
      setMezziPrenotati([...selezione])
      setPrenotazioni(prens)
      setSelezione([])
      setModalita(null)
      setMezzoAttivo(null)
      getPrenotazioniAttive().then(setPrenotazioniAttive).catch(() => {})
    } catch (err) {
      if (isRisultatiParziali(err)) {
        const ids = err.response.data.detail.non_disponibili
        setNonDisponibili(ids)
        setSelezione(prev => prev.filter(m => !ids.includes(m.id)))
        setErrorePanel(`${ids.length} mezzo/i non più disponibile/i. Puoi procedere con i restanti o aggiungere altri.`)
      } else {
        setErrorePanel('Errore durante la prenotazione. Riprova.')
      }
    } finally {
      setPrenotaInCorso(false)
    }
  }, [selezione])

  const handleAnnullaTutte = useCallback(async () => {
    if (prenotazioni.length === 0) return
    setAnnullaInCorso(true)
    setErrorePanel('')
    try {
      await Promise.all(prenotazioni.map(p => annullaPrenotazione(p.id)))
      setPrenotazioni([])
      setMezziPrenotati([])
      setPrenotazioniAttive([])
    } catch {
      setErrorePanel("Errore durante l'annullamento. Riprova.")
    } finally {
      setAnnullaInCorso(false)
    }
  }, [prenotazioni])

  // [IF-UT.04] CS-05 — sblocca uno o più mezzi (selezione, mezzo attivo, o targets espliciti)
  const handleSblocca = useCallback(async (explicitTargets?: MezzoMappa[]) => {
    const targets = explicitTargets ?? (selezione.length > 0
      ? selezione
      : mezzoAttivo ? [mezzoAttivo] : [])
    if (targets.length === 0) return
    setSbloccoInCorso(true)
    setErrorePanel('')
    try {
      const risultato = await sbloccaMezzi(
        targets.map(m => m.id),
        centro.lat,
        centro.lng,
      )
      if (risultato.sbloccati.length === 0) {
        // CS-05.01: tutti falliti
        setErrorePanel(`Sblocco non riuscito per ${risultato.falliti.length} mezzo/i. Riprova.`)
        return
      }
      if (risultato.falliti.length > 0) {
        // CS-05.01 parziale — avvisa ma procedi con i sbloccati
        setErrorePanel(`${risultato.falliti.length} mezzo/i non sbloccato/i. Gli altri sono pronti.`)
      }
      // naviga alla corsa — passa la lista completa per il multi-mezzo
      const primo = risultato.sbloccati[0]
      const inizio_at = new Date().toISOString()
      setSelezione([])
      setModalita(null)
      navigate(`/utente/corsa/${primo.mezzo_id}`, {
        state: {
          corse: risultato.sbloccati.map(s => ({
            corsa_id: s.corsa_id,
            mezzo: targets.find(m => m.id === s.mezzo_id) ?? targets[0],
            inizio_at,
            gruppo_corsa_id: s.gruppo_corsa_id ?? null,
          })),
        },
      })
    } catch {
      setErrorePanel('Errore durante lo sblocco. Riprova.')
    } finally {
      setSbloccoInCorso(false)
    }
  }, [mezzoAttivo, selezione, centro, navigate])

  const tipoLabel = (tipo: string) => tipo.charAt(0).toUpperCase() + tipo.slice(1)
  const isInSelezione = (m: MezzoMappa) => selezione.some(s => s.id === m.id)
  const isNonDisponibile = (m: MezzoMappa) => nonDisponibili.includes(m.id)
  const panelAperto = mezzoAttivo !== null || modalita !== null || selezione.length > 0 || prenotazioni.length > 0
  const utente = utenteCorrente()

  const apriSidebar = (sezione: SidebarSezione = 'menu') => {
    setSidebarSezione(sezione)
    setSidebarAperta(true)
  }

  return (
    <div className="vista-mappa">
      {/* ── Topbar ── */}
      <div className="mappa-topbar">
        <h2>Smart Mobility</h2>
        {selezione.length > 0 && (
          <span className="selezione-badge">{selezione.length}/{nMax}</span>
        )}
        <button
          type="button"
          className="btn-hamburger"
          onClick={() => apriSidebar('menu')}
          aria-label="Menu"
        >
          <span /><span /><span />
        </button>
      </div>

      {/* ── Mappa ── */}
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
            onClick={() => { setMezzoAttivo(m); setErrorePanel('') }}
          >
            <PinMezzo tipo={m.tipo} selected={isInSelezione(m)} dim={isNonDisponibile(m)} />
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
            />
          )
        })}

        {/* Marker posizione utente */}
        <AdvancedMarker position={centro}>
          <div
            className={posizioneReale ? 'pin-utente' : 'pin-default'}
            aria-label={posizioneReale ? 'La tua posizione' : 'Posizione predefinita'}
          >
            {posizioneReale && <div className="pin-utente__pulse" />}
            <div className={posizioneReale ? 'pin-utente__dot' : 'pin-default__dot'}>
              {posizioneReale ? '🧍' : '📍'}
            </div>
          </div>
        </AdvancedMarker>
      </GoogleMap>

      {/* ── [IF-UT.14] Banner suggerimenti ── */}
      <div className={`suggerimenti-banner${bannerAperto ? ' suggerimenti-banner--aperto' : ''}`}>
        <div className="suggerimenti-banner__header">
          <button
            className="suggerimenti-banner__toggle"
            onClick={() => setBannerAperto(prev => !prev)}
            aria-label={bannerAperto ? 'Chiudi suggerimenti' : 'Apri suggerimenti'}
            aria-expanded={bannerAperto}
          >
            <span className="suggerimenti-banner__toggle-icon">💡</span>
            <span className="suggerimenti-banner__toggle-label">Suggerimenti</span>
            <span className={`suggerimenti-banner__chevron${bannerAperto ? ' suggerimenti-banner__chevron--up' : ''}`}>
              ▾
            </span>
          </button>
          <button
            className="btn-genera-suggerimenti"
            onClick={(e) => { e.stopPropagation(); handleGeneraSuggerimenti() }}
            disabled={generaInCorso}
            aria-busy={generaInCorso}
          >
            {generaInCorso ? '...' : 'Genera'}
          </button>
        </div>

        {bannerAperto && (
          <div className="suggerimenti-banner__body" role="region" aria-label="Suggerimenti intelligenti">
            {erroreSuggerimenti && (
              <p className="suggerimenti-banner__errore" role="alert">{erroreSuggerimenti}</p>
            )}

            {generaInCorso && (
              <p className="suggerimenti-banner__vuoto">Generazione in corso...</p>
            )}

            {!generaInCorso && suggerimenti && suggerimenti.length > 0 ? (
              <ul className="suggerimenti-lista" role="list">
                {suggerimenti.map(s => (
                  <li
                    key={s.id}
                    className={`suggerimento-card${s.stato === 'nuovo' ? ' suggerimento-card--nuovo' : ''}`}
                    onClick={() => s.stato === 'nuovo' && handleSegnaVisto(s.id)}
                    role="listitem"
                    tabIndex={0}
                    onKeyDown={e => e.key === 'Enter' && s.stato === 'nuovo' && handleSegnaVisto(s.id)}
                  >
                    <span className="suggerimento-card__tipo">{
                      s.tipo === 'risparmio' ? '💰' :
                      s.tipo === 'percorso' ? '🗺️' :
                      s.tipo === 'abbonamento' ? '📅' :
                      s.tipo === 'orario' ? '🕐' :
                      s.tipo === 'mezzo' ? '🚲' : '💡'
                    } {s.tipo.charAt(0).toUpperCase() + s.tipo.slice(1)}</span>
                    <span className="suggerimento-card__testo">{s.testo}</span>
                    {s.stato === 'nuovo' && <span className="suggerimento-card__badge">Nuovo</span>}
                  </li>
                ))}
              </ul>
            ) : !generaInCorso && suggerimenti && suggerimenti.length === 0 && !erroreSuggerimenti ? (
              <p className="suggerimenti-banner__vuoto">Premi "Genera" per ottenere suggerimenti personalizzati.</p>
            ) : null}
          </div>
        )}
      </div>

      {/* ── Bottom sheet: prenota / selezione ── */}
      {panelAperto && (
        <div className="pannello-mezzo">
          <div className="pannello-header">
            <span className="pannello-titolo">
              {prenotazioni.length > 0 ? 'Prenotazioni attive' : 'Prenota mezzo'}
            </span>
            <button className="pannello-chiudi" onClick={() => {
              chiudiPanel()
              resettaSelezione()
              setPrenotazioni([])
              setMezziPrenotati([])
            }}>✕</button>
          </div>
          <div className="pannello-separatore" />

          {prenotazioni.length > 0 ? (
            <div className="pannello-prenotazioni">
              <p className="pannello-prenotati-titolo">
                ✅ {prenotazioni.length} mezzo/i prenotato/i
              </p>
              <p className="pannello-countdown-info">
                Tempo rimanente (prima scadenza):&nbsp;
                <strong>{formatTempoRimanente(tempoRimanente)}</strong>
              </p>
              <ul className="lista-prenotazioni">
                {prenotazioni.map(p => {
                  const mezzo = mezziPrenotati.find(m => m.id === p.mezzo_id) ?? mezzi.find(m => m.id === p.mezzo_id)
                  return (
                    <li key={p.id} className="item-prenotazione">
                      <span>{mezzo ? `${GLYPH_MEZZO[mezzo.tipo] ?? '●'} ${tipoLabel(mezzo.tipo)} · ${mezzo.codice}` : p.mezzo_id}</span>
                    </li>
                  )
                })}
              </ul>
              <div style={{ display: 'flex', gap: 8 }}>
                <button className="btn-prenota btn-annulla" onClick={handleAnnullaTutte} disabled={annullaInCorso} style={{ flex: 1 }}>
                  {annullaInCorso ? '...' : 'Annulla tutte'}
                </button>
                <button
                  className="btn-sblocca-panel"
                  onClick={() => {
                    const targets = mezziPrenotati.length > 0
                      ? mezziPrenotati
                      : prenotazioni.map(p => mezzi.find(m => m.id === p.mezzo_id)).filter(Boolean) as MezzoMappa[]
                    handleSblocca(targets)
                  }}
                  disabled={sbloccoInCorso}
                  style={{ flex: 1 }}
                >
                  {sbloccoInCorso ? '...' : `Sblocca (${prenotazioni.length})`}
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Info mezzo correntemente visualizzato */}
              {mezzoAttivo && (
                <>
                  <p className="pannello-tipo">{tipoLabel(mezzoAttivo.tipo)}:</p>
                  <div className="pannello-mezzo-row">
                    <span className="pannello-emoji">{GLYPH_MEZZO[mezzoAttivo.tipo] ?? '●'}</span>
                    <span className="pannello-codice">{mezzoAttivo.codice}</span>
                    <Batteria valore={mezzoAttivo.batteria} />
                  </div>
                </>
              )}

              {errorePanel && <p className="pannello-errore">{errorePanel}</p>}

              {/* Selezione — visibile solo quando si è già in una modalità */}
              {modalita !== null && selezione.length > 0 && (
                <div className="selezione-sezione">
                  <p className="selezione-label">
                    {modalita === 'prenota' ? 'Da prenotare' : 'Da sbloccare'} ({selezione.length}/{nMax}):
                  </p>
                  <div className="selezione-chips">
                    {selezione.map(m => (
                      <span key={m.id} className="chip-mezzo">
                        {GLYPH_MEZZO[m.tipo] ?? '●'} {m.codice}
                        <button className="chip-rimuovi" onClick={() => toggleSelezione(m)}>×</button>
                      </span>
                    ))}
                  </div>
                  {selezione.length < nMax && !errorePanel && (
                    <p className="selezione-hint">Tocca altri mezzi sulla mappa per aggiungerli.</p>
                  )}
                </div>
              )}

              <div className="pannello-azioni">
                {modalita === null ? (
                  /* ── Stato iniziale: scegli l'azione ── */
                  mezzoAttivo && (
                    <>
                      <button
                        className="btn-prenota"
                        onClick={() => {
                          setModalita('prenota')
                          toggleSelezione(mezzoAttivo)
                        }}
                      >
                        Prenota
                      </button>
                      <button
                        className="btn-sblocca-panel"
                        onClick={() => {
                          setModalita('sblocca')
                          toggleSelezione(mezzoAttivo)
                        }}
                        disabled={sbloccoInCorso}
                      >
                        Sblocca
                      </button>
                    </>
                  )
                ) : (
                  /* ── Modalità attiva: Aggiungi/Rimuovi + Conferma ── */
                  <>
                    {mezzoAttivo && (
                      isInSelezione(mezzoAttivo) ? (
                        <button className="btn-prenota btn-annulla" onClick={() => toggleSelezione(mezzoAttivo)}>
                          – Rimuovi
                        </button>
                      ) : (
                        <button
                          className="btn-prenota"
                          onClick={() => toggleSelezione(mezzoAttivo)}
                          disabled={selezione.length >= nMax}
                        >
                          + Aggiungi
                        </button>
                      )
                    )}
                    {modalita === 'prenota' ? (
                      <button
                        className="btn-sblocca-panel btn-conferma-prenota"
                        onClick={handleConfermaPrenotazione}
                        disabled={prenotaInCorso || selezione.length === 0}
                      >
                        {prenotaInCorso ? '...' : `Prenota (${selezione.length})`}
                      </button>
                    ) : (
                      <button
                        className="btn-sblocca-panel btn-conferma-prenota"
                        onClick={() => handleSblocca()}
                        disabled={sbloccoInCorso || selezione.length === 0}
                      >
                        {sbloccoInCorso ? '...' : `Sblocca (${selezione.length})`}
                      </button>
                    )}
                  </>
                )}
              </div>

              {!mezzoAttivo && modalita === null && (
                <p className="pannello-info">Seleziona un mezzo sulla mappa.</p>
              )}
            </>
          )}
        </div>
      )}

      {/* ── Sidebar overlay ── */}
      {sidebarAperta && (
        <div className="sidebar-overlay" onClick={() => setSidebarAperta(false)} />
      )}

      {/* ── Sidebar ── */}
      <div className={`sidebar${sidebarAperta ? ' sidebar--aperta' : ''}`}>
        {/* Header */}
        <div className="sidebar-header">
          <span className="sidebar-logo">SMART M<span className="sidebar-logo-accent">O</span>BILITY</span>
          <button className="sidebar-chiudi" onClick={() => setSidebarAperta(false)}>✕</button>
        </div>

        {sidebarSezione === 'menu' ? (
          <>
            {/* Profilo */}
            {utente && (
              <div className="sidebar-profilo">
                <div className="sidebar-avatar">
                  {(utente.profilo.nome?.[0] ?? '?').toUpperCase()}
                </div>
                <div>
                  <p className="sidebar-nome">{utente.profilo.nome}</p>
                  <p className="sidebar-email">{utente.profilo.email}</p>
                </div>
              </div>
            )}

            <div className="sidebar-divider" />

            {/* Voci menu */}
            <nav className="sidebar-voci">
              <button
                className="sidebar-voce"
                onClick={() => {
                  getPrenotazioniAttive().then(setPrenotazioniAttive).catch(() => {})
                  setSidebarSezione('prenotazioni')
                }}
              >
                <span className="sidebar-voce__testo">
                  Prenotazioni
                  {prenotazioniAttive.length > 0 && (
                    <span className="sidebar-badge">{prenotazioniAttive.length}</span>
                  )}
                </span>
                <span className="sidebar-voce__icona">🎫</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { apriTariffe(); setSidebarSezione('tariffe') }}
              >
                <span className="sidebar-voce__testo">Piano Tariffario</span>
                <span className="sidebar-voce__icona">€</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { apriPromozioni(); setSidebarSezione('promozioni') }}
              >
                <span className="sidebar-voce__testo">Bonus e Promozioni</span>
                <span className="sidebar-voce__icona">🎁</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/pagamenti') }}
              >
                <span className="sidebar-voce__testo">Portafoglio</span>
                <span className="sidebar-voce__icona">💳</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/abbonamenti') }}
              >
                <span className="sidebar-voce__testo">Abbonamenti</span>
                <span className="sidebar-voce__icona">📅</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/storico') }}
              >
                <span className="sidebar-voce__testo">Cronologia</span>
                <span className="sidebar-voce__icona">📋</span>
              </button>

              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/segnalazione') }}
              >
                <span className="sidebar-voce__testo">Invia segnalazione</span>
                <span className="sidebar-voce__icona">⚠️</span>
              </button>
            </nav>

            {/* Logout in fondo */}
            <div className="sidebar-footer">
              <button className="sidebar-voce sidebar-voce--logout" onClick={handleLogout}>
                <span className="sidebar-voce__testo">Esci</span>
                <span className="sidebar-voce__icona">🚪</span>
              </button>
            </div>
          </>
        ) : sidebarSezione === 'prenotazioni' ? (
          /* Sezione prenotazioni */
          <>
            <div className="sidebar-back-header">
              <button className="sidebar-back" onClick={() => setSidebarSezione('menu')}>← Indietro</button>
              <span className="sidebar-sezione-titolo">Le mie prenotazioni</span>
            </div>
            <div className="sidebar-divider" />
            {prenotazioniAttive.length === 0 ? (
              <p className="sidebar-empty">Nessuna prenotazione attiva.</p>
            ) : (
              <>
                <ul className="sidebar-prenotazioni">
                  {prenotazioniAttive.map(p => {
                    const secsLeft = Math.max(0, Math.floor((new Date(p.scade_at).getTime() - nowMs) / 1000))
                    return (
                      <li key={p.id} className="sidebar-pren-item">
                        <div className="sidebar-pren-row">
                          <span className="sidebar-pren-mezzo">
                            {GLYPH_MEZZO[p.tipo ?? ''] ?? '●'} {tipoLabel(p.tipo ?? '')} · {p.codice}
                          </span>
                          <span className="sidebar-pren-timer">⏱ {formatTempoRimanente(secsLeft)}</span>
                        </div>
                      </li>
                    )
                  })}
                </ul>
                <div className="sidebar-pren-azioni">
                  <button
                    className="btn-prenota btn-annulla"
                    disabled={annullaInCorso}
                    onClick={async () => {
                      setAnnullaInCorso(true)
                      try {
                        await Promise.all(prenotazioniAttive.map(p => annullaPrenotazione(p.id)))
                        setPrenotazioniAttive([])
                        setPrenotazioni([])
                        setMezziPrenotati([])
                      } catch { /* ignore */ }
                      finally { setAnnullaInCorso(false) }
                    }}
                  >
                    {annullaInCorso ? '...' : 'Annulla tutti'}
                  </button>
                  <button
                    className="btn-sblocca-panel"
                    disabled={sbloccoInCorso}
                    onClick={() => {
                      setSidebarAperta(false)
                      handleSblocca(prenotazioniAttive.map(p => ({
                        id: p.mezzo_id,
                        codice: p.codice ?? '',
                        tipo: (p.tipo ?? 'monopattino') as MezzoMappa['tipo'],
                        stato: 'Prenotato',
                        lat: 0,
                        lng: 0,
                        batteria: p.batteria ?? null,
                      })))
                    }}
                  >
                    {sbloccoInCorso ? '...' : `Sblocca (${prenotazioniAttive.length})`}
                  </button>
                </div>
              </>
            )}
          </>
        ) : (sidebarSezione === 'tariffe' || sidebarSezione === 'promozioni') ? (
          /* Sezione tariffe / promozioni */
          <>
            <div className="sidebar-back-header">
              <button className="sidebar-back" onClick={() => setSidebarSezione('menu')}>← Indietro</button>
              <span className="sidebar-sezione-titolo">
                {sidebarSezione === 'tariffe' ? 'Piano Tariffario' : 'Bonus e Promozioni'}
              </span>
            </div>
            <div className="sidebar-divider" />
            <div className="sidebar-pricing-body">
              {loadingDrawer && <p className="sidebar-empty">Caricamento...</p>}
              {erroreDrawer && <p className="sidebar-empty" style={{ color: '#e53935' }}>{erroreDrawer}</p>}
              {!loadingDrawer && !erroreDrawer && sidebarSezione === 'tariffe' && (
                tariffe && tariffe.length > 0 ? (
                  <ul className="pricing-lista">
                    {tariffe.map(t => (
                      <li key={t.id} className="pricing-card">
                        <span className="pricing-card__tipo">
                          {t.tipo_mezzo === 'monopattino' ? '🛴' : t.tipo_mezzo === 'bicicletta' ? '🚲' : '🚗'}{' '}
                          {t.tipo_mezzo.charAt(0).toUpperCase() + t.tipo_mezzo.slice(1)}
                        </span>
                        <span className="pricing-card__riga">{parseFloat(t.costo_al_minuto).toFixed(2)} €/min</span>
                        <span className="pricing-card__riga">{parseFloat(t.costo_al_km).toFixed(2)} €/km</span>
                      </li>
                    ))}
                  </ul>
                ) : <p className="sidebar-empty">Nessuna tariffa disponibile.</p>
              )}
              {!loadingDrawer && !erroreDrawer && sidebarSezione === 'promozioni' && (
                promozioni && promozioni.length > 0 ? (
                  <ul className="pricing-lista">
                    {promozioni.map(p => (
                      <li key={p.id} className="pricing-card pricing-card--promo">
                        <span className="pricing-card__tipo">{p.titolo}</span>
                        {p.descrizione && <span className="pricing-card__riga">{p.descrizione}</span>}
                        <span className="pricing-card__riga pricing-card__sconto">
                          -{parseFloat(p.sconto_percentuale).toFixed(0)}%
                        </span>
                        <span className="pricing-card__riga pricing-card__scadenza">
                          Fino al {new Date(p.data_fine).toLocaleDateString('it-IT')}
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : <p className="sidebar-empty">Nessuna promozione attiva al momento.</p>
              )}
            </div>
          </>
        ) : null}
      </div>



      {errore && <div className="mappa-errore">{errore}</div>}
    </div>
  )
}
