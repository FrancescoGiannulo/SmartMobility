import { useEffect, useState, useCallback } from 'react'
import axios from 'axios'
import {
  getMezziFlotta,
  aggiungiMezzo,
  verificaDismissione,
  dismetti,
  modificaStato,
  type MezzoFlotta,
  type AggiungiMezzoPayload,
} from '../../services/FlottaService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import '../../styles/primitives.css'
import './VistaMezziOperatore.css'

const TIPO_EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

const STATO_CHIP_CLASS: Record<string, string> = {
  'Disponibile':    'vmezzi__state--disponibile',
  'Prenotato':      'vmezzi__state--prenotato',
  'In uso':         'vmezzi__state--in-uso',
  'In pausa':       'vmezzi__state--in-pausa',
  'In manutenzione':'vmezzi__state--manutenzione',
  'Fuori servizio': 'vmezzi__state--fuori',
}

const STATI_MODIFICABILI = ['Disponibile', 'In manutenzione', 'Fuori servizio']
const STATI_BLOCCATI = new Set(['In uso', 'In pausa'])

interface FormState {
  tipo: string
  codice: string
  lat: string
  lng: string
  stato: string
}

const FORM_VUOTO: FormState = {
  tipo: 'monopattino',
  codice: '',
  lat: '',
  lng: '',
  stato: 'Disponibile',
}

interface Toast { msg: string; tipo: 'ok' | 'err' }

const TUTTI_STATI = ['Tutti', 'Disponibile', 'Prenotato', 'In uso', 'In pausa', 'In manutenzione', 'Fuori servizio']

export default function VistaMezziOperatore() {
  const [mezzi, setMezzi] = useState<MezzoFlotta[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [toast, setToast] = useState<Toast | null>(null)
  const [mostraModal, setMostraModal] = useState(false)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [erroreForm, setErroreForm] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [confermaDismissione, setConfermaDismissione] = useState<MezzoFlotta | null>(null)
  const [controllando, setControllando] = useState(false)
  const [aggiornandoStato, setAggiornandoStato] = useState<string | null>(null)
  const [filtroStato, setFiltroStato] = useState('Tutti')

  const mostraToast = (msg: string, tipo: 'ok' | 'err') => {
    setToast({ msg, tipo })
    setTimeout(() => setToast(null), 3500)
  }

  const ricarica = useCallback(() => {
    setCaricamento(true)
    getMezziFlotta()
      .then(r => setMezzi(r.data))
      .catch(() => mostraToast('Errore nel caricamento della flotta', 'err'))
      .finally(() => setCaricamento(false))
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriModal = () => {
    setForm(FORM_VUOTO)
    setErroreForm('')
    setMostraModal(true)
  }

  const handleCampo = (k: keyof FormState, v: string) =>
    setForm(f => ({ ...f, [k]: v }))

  const handleSubmitAggiungi = async () => {
    if (!form.codice.trim()) {
      setErroreForm('Il codice è obbligatorio')
      return
    }
    const lat = parseFloat(form.lat)
    const lng = parseFloat(form.lng)
    if (isNaN(lat) || isNaN(lng)) {
      setErroreForm('Latitudine e longitudine devono essere numeri validi')
      return
    }
    const payload: AggiungiMezzoPayload = {
      tipo: form.tipo,
      codice: form.codice.trim(),
      lat,
      lng,
      stato: form.stato,
    }
    setSubmitting(true)
    setErroreForm('')
    try {
      await aggiungiMezzo(payload)
      setMostraModal(false)
      ricarica()
      mostraToast('Mezzo aggiunto con successo', 'ok')
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail ?? 'Errore durante l\'aggiunta'
        if (err.response?.status === 409) {
          setErroreForm('Identificativo già in uso. Scegli un codice diverso.')
        } else {
          setErroreForm(String(detail))
        }
      } else {
        setErroreForm('Errore imprevisto')
      }
    } finally {
      setSubmitting(false)
    }
  }

  const handleCliccaDismetti = async (mezzo: MezzoFlotta) => {
    setControllando(true)
    try {
      const r = await verificaDismissione(mezzo.id)
      if (r.data.dismettibile) {
        setConfermaDismissione(mezzo)
      } else {
        mostraToast(r.data.motivo ?? 'Impossibile dismettere il mezzo', 'err')
      }
    } catch {
      mostraToast('Errore durante la verifica', 'err')
    } finally {
      setControllando(false)
    }
  }

  // [IF-OP.04] Modifica stato mezzo dall'operatore
  const handleCambiaStato = async (mezzo: MezzoFlotta, nuovoStato: string) => {
    if (nuovoStato === mezzo.stato) return
    setAggiornandoStato(mezzo.id)
    try {
      await modificaStato(mezzo.id, nuovoStato)
      ricarica()
      mostraToast('Stato del mezzo aggiornato', 'ok')
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        mostraToast(String(err.response.data?.detail ?? 'Mezzo attualmente in uso o prenotato'), 'err')
      } else {
        mostraToast('Errore durante l\'aggiornamento dello stato', 'err')
      }
    } finally {
      setAggiornandoStato(null)
    }
  }

  const handleConfermaDismissione = async () => {
    if (!confermaDismissione) return
    try {
      await dismetti(confermaDismissione.id)
      setConfermaDismissione(null)
      ricarica()
      mostraToast('Mezzo dismesso con successo', 'ok')
    } catch {
      mostraToast('Errore durante la dismissione', 'err')
    }
  }

  const mezziFiltrati = filtroStato === 'Tutti'
    ? mezzi
    : mezzi.filter(m => m.stato === filtroStato)

  return (
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />

      <div className="sm-op-main">
        <header className="vmezzi__header">
          <h1 className="vmezzi__titolo">Gestione Flotta</h1>
          <button className="sm-btn sm-btn--primary vmezzi__btn-aggiungi" onClick={apriModal}>
            + Aggiungi mezzo
          </button>
        </header>

        <main className="vmezzi__body">
          {/* Filtri stato come chip */}
          <div className="vmezzi__filtri" role="group" aria-label="Filtra per stato">
            {TUTTI_STATI.map(s => (
              <button
                key={s}
                className={`sm-chip vmezzi__filtro-chip${filtroStato === s ? ' vmezzi__filtro-chip--attivo' : ''}`}
                onClick={() => setFiltroStato(s)}
                aria-pressed={filtroStato === s}
              >
                {s}
              </button>
            ))}
          </div>

          <div className="vmezzi__tabella-wrapper sm-card">
            <table className="vmezzi__tabella">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Codice</th>
                  <th>Stato</th>
                  <th>Batteria</th>
                  <th>Coordinate</th>
                  <th>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {caricamento ? (
                  Array.from({ length: 4 }).map((_, i) => (
                    <tr key={i} className="vmezzi__skeleton">
                      {Array.from({ length: 6 }).map((_, j) => <td key={j}>&nbsp;</td>)}
                    </tr>
                  ))
                ) : mezziFiltrati.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="vmezzi__empty">
                      Nessun mezzo{filtroStato !== 'Tutti' ? ` con stato "${filtroStato}"` : ' in flotta'}
                    </td>
                  </tr>
                ) : (
                  mezziFiltrati.map(m => {
                    const battPct = m.batteria ?? null
                    const battClass = battPct !== null && battPct === 0
                      ? 'vmezzi__batt--critica'
                      : battPct !== null && battPct < 20
                      ? 'vmezzi__batt--bassa'
                      : ''
                    return (
                      <tr key={m.id}>
                        <td>{TIPO_EMOJI[m.tipo] ?? '●'} {m.tipo}</td>
                        <td><span className="sm-mono vmezzi__codice">{m.codice}</span></td>
                        <td>
                          {STATI_BLOCCATI.has(m.stato) ? (
                            <span className={`sm-chip vmezzi__state ${STATO_CHIP_CLASS[m.stato] ?? ''}`}>
                              {m.stato}
                            </span>
                          ) : (
                            <select
                              className={`sm-chip vmezzi__state vmezzi__state--select ${STATO_CHIP_CLASS[m.stato] ?? ''}`}
                              value={m.stato}
                              disabled={aggiornandoStato === m.id}
                              onChange={e => handleCambiaStato(m, e.target.value)}
                              aria-label={`Stato del mezzo ${m.codice}`}
                            >
                              {m.stato === 'Prenotato' && (
                                <option value="Prenotato" disabled>Prenotato</option>
                              )}
                              {STATI_MODIFICABILI.map(s => (
                                <option key={s} value={s}>{s}</option>
                              ))}
                            </select>
                          )}
                        </td>
                        <td>
                          {battPct != null
                            ? <span className={`sm-mono vmezzi__batt ${battClass}`}>{battPct}%</span>
                            : <span className="vmezzi__dash">—</span>}
                        </td>
                        <td>
                          {m.lat != null && m.lng != null
                            ? <span className="sm-mono vmezzi__coords">{m.lat.toFixed(4)}, {m.lng.toFixed(4)}</span>
                            : <span className="vmezzi__dash">—</span>}
                        </td>
                        <td>
                          <button
                            className="sm-btn sm-btn--ghost vmezzi__btn-dismetti"
                            disabled={controllando}
                            onClick={() => handleCliccaDismetti(m)}
                          >
                            Dismetti
                          </button>
                        </td>
                      </tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>
        </main>

        {/* Modal aggiunta mezzo */}
        {mostraModal && (
          <div className="vmezzi__overlay" onClick={() => setMostraModal(false)}>
            <div className="vmezzi__modal" onClick={e => e.stopPropagation()} role="dialog" aria-modal="true" aria-labelledby="modal-aggiungi-titolo">
              <h2 id="modal-aggiungi-titolo">Aggiungi nuovo mezzo</h2>

              <div className="vmezzi__campo">
                <label htmlFor="vm-tipo">Tipologia</label>
                <select id="vm-tipo" value={form.tipo} onChange={e => handleCampo('tipo', e.target.value)}>
                  <option value="monopattino">🛴 Monopattino</option>
                  <option value="bicicletta">🚲 Bicicletta</option>
                  <option value="automobile">🚗 Automobile</option>
                </select>
              </div>

              <div className="vmezzi__campo">
                <label htmlFor="vm-codice">Codice identificativo</label>
                <input
                  id="vm-codice"
                  type="text"
                  placeholder="es. MON-001"
                  value={form.codice}
                  onChange={e => handleCampo('codice', e.target.value)}
                />
              </div>

              <div className="vmezzi__campo">
                <label htmlFor="vm-lat">Latitudine</label>
                <input
                  id="vm-lat"
                  type="number"
                  step="0.0001"
                  placeholder="es. 41.1177"
                  value={form.lat}
                  onChange={e => handleCampo('lat', e.target.value)}
                />
              </div>

              <div className="vmezzi__campo">
                <label htmlFor="vm-lng">Longitudine</label>
                <input
                  id="vm-lng"
                  type="number"
                  step="0.0001"
                  placeholder="es. 16.8719"
                  value={form.lng}
                  onChange={e => handleCampo('lng', e.target.value)}
                />
              </div>

              <div className="vmezzi__campo">
                <label htmlFor="vm-stato">Stato iniziale</label>
                <select id="vm-stato" value={form.stato} onChange={e => handleCampo('stato', e.target.value)}>
                  <option value="Disponibile">Disponibile</option>
                  <option value="In manutenzione">In manutenzione</option>
                  <option value="Fuori servizio">Fuori servizio</option>
                </select>
              </div>

              {erroreForm && <p className="vmezzi__errore" role="alert">{erroreForm}</p>}

              <div className="vmezzi__modal-footer">
                <button className="sm-btn sm-btn--ghost" onClick={() => setMostraModal(false)}>
                  Annulla
                </button>
                <button
                  className="sm-btn sm-btn--primary"
                  onClick={handleSubmitAggiungi}
                  disabled={submitting}
                >
                  {submitting ? 'Salvataggio…' : 'Aggiungi'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Dialog conferma dismissione */}
        {confermaDismissione && (
          <div className="vmezzi__overlay">
            <div className="vmezzi__modal" role="dialog" aria-modal="true" aria-labelledby="modal-dismetti-titolo">
              <h2 id="modal-dismetti-titolo">Conferma dismissione</h2>
              <p className="vmezzi__modal-desc">
                Vuoi dismettere il mezzo <strong>{confermaDismissione.codice}</strong>?
                L'operazione è irreversibile e il mezzo non sarà più disponibile per nuove corse.
              </p>
              <div className="vmezzi__modal-footer">
                <button
                  className="sm-btn sm-btn--ghost"
                  onClick={() => setConfermaDismissione(null)}
                >
                  Annulla
                </button>
                <button
                  className="sm-btn sm-btn--primary vmezzi__btn--danger"
                  onClick={handleConfermaDismissione}
                >
                  Dismetti
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Toast */}
        {toast && (
          <div className={`vmezzi__toast vmezzi__toast--${toast.tipo}`} role="status" aria-live="polite">
            {toast.msg}
          </div>
        )}
      </div>
    </div>
  )
}
