import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getMezziFlotta,
  aggiungiMezzo,
  verificaDismissione,
  dismetti,
  type MezzoFlotta,
  type AggiungiMezzoPayload,
} from '../../services/FlottaService'
import './VistaMezziOperatore.css'

const TIPO_EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

const STATO_PILL_CLASS: Record<string, string> = {
  'Disponibile':    'vmezzi__pill--disponibile',
  'Prenotato':      'vmezzi__pill--prenotato',
  'In uso':         'vmezzi__pill--in-uso',
  'In pausa':       'vmezzi__pill--in-pausa',
  'In manutenzione':'vmezzi__pill--manutenzione',
  'Fuori servizio': 'vmezzi__pill--fuori',
}

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

export default function VistaMezziOperatore() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoFlotta[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [toast, setToast] = useState<Toast | null>(null)
  const [mostraModal, setMostraModal] = useState(false)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [erroreForm, setErroreForm] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [confermaDismissione, setConfermaDismissione] = useState<MezzoFlotta | null>(null)
  const [controllando, setControllando] = useState(false)

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

  return (
    <div className="vmezzi">
      <header className="vmezzi__header">
        <div className="vmezzi__header-left">
          <button className="vmezzi__back" onClick={() => navigate('/operatore/dashboard')}>
            ←
          </button>
          <h1 className="vmezzi__titolo">Gestione Flotta</h1>
        </div>
        <button className="vmezzi__btn-aggiungi" onClick={apriModal}>
          + Aggiungi mezzo
        </button>
      </header>

      <main className="vmezzi__body">
        <div className="vmezzi__tabella-wrapper">
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
              ) : mezzi.length === 0 ? (
                <tr>
                  <td colSpan={6} className="vmezzi__empty">
                    Nessun mezzo in flotta
                  </td>
                </tr>
              ) : (
                mezzi.map(m => (
                  <tr key={m.id}>
                    <td>{TIPO_EMOJI[m.tipo] ?? '●'} {m.tipo}</td>
                    <td><strong>{m.codice}</strong></td>
                    <td>
                      <span className={`vmezzi__pill ${STATO_PILL_CLASS[m.stato] ?? ''}`}>
                        {m.stato}
                      </span>
                    </td>
                    <td>{m.batteria != null ? `${m.batteria}%` : '—'}</td>
                    <td>
                      {m.lat != null && m.lng != null
                        ? `${m.lat.toFixed(4)}, ${m.lng.toFixed(4)}`
                        : '—'}
                    </td>
                    <td>
                      <button
                        className="vmezzi__btn-dismetti"
                        disabled={controllando}
                        onClick={() => handleCliccaDismetti(m)}
                      >
                        Dismetti
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>

      {/* Modal aggiunta mezzo */}
      {mostraModal && (
        <div className="vmezzi__overlay" onClick={() => setMostraModal(false)}>
          <div className="vmezzi__modal" onClick={e => e.stopPropagation()}>
            <h2>Aggiungi nuovo mezzo</h2>

            <div className="vmezzi__campo">
              <label>Tipologia</label>
              <select value={form.tipo} onChange={e => handleCampo('tipo', e.target.value)}>
                <option value="monopattino">🛴 Monopattino</option>
                <option value="bicicletta">🚲 Bicicletta</option>
                <option value="automobile">🚗 Automobile</option>
              </select>
            </div>

            <div className="vmezzi__campo">
              <label>Codice identificativo</label>
              <input
                type="text"
                placeholder="es. MON-001"
                value={form.codice}
                onChange={e => handleCampo('codice', e.target.value)}
              />
            </div>

            <div className="vmezzi__campo">
              <label>Latitudine</label>
              <input
                type="number"
                step="0.0001"
                placeholder="es. 41.1177"
                value={form.lat}
                onChange={e => handleCampo('lat', e.target.value)}
              />
            </div>

            <div className="vmezzi__campo">
              <label>Longitudine</label>
              <input
                type="number"
                step="0.0001"
                placeholder="es. 16.8719"
                value={form.lng}
                onChange={e => handleCampo('lng', e.target.value)}
            />
            </div>

            <div className="vmezzi__campo">
              <label>Stato iniziale</label>
              <select value={form.stato} onChange={e => handleCampo('stato', e.target.value)}>
                <option value="Disponibile">Disponibile</option>
                <option value="In manutenzione">In manutenzione</option>
                <option value="Fuori servizio">Fuori servizio</option>
              </select>
            </div>

            {erroreForm && <p className="vmezzi__errore">{erroreForm}</p>}

            <div className="vmezzi__modal-footer">
              <button className="vmezzi__btn-annulla" onClick={() => setMostraModal(false)}>
                Annulla
              </button>
              <button
                className="vmezzi__btn-conferma"
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
          <div className="vmezzi__modal">
            <h2>Conferma dismissione</h2>
            <p style={{ color: '#475569', marginBottom: 24 }}>
              Vuoi dismettere il mezzo <strong>{confermaDismissione.codice}</strong>?
              L'operazione è irreversibile e il mezzo non sarà più disponibile per nuove corse.
            </p>
            <div className="vmezzi__modal-footer">
              <button
                className="vmezzi__btn-annulla"
                onClick={() => setConfermaDismissione(null)}
              >
                Annulla
              </button>
              <button
                className="vmezzi__btn-conferma vmezzi__btn-conferma--danger"
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
        <div className={`vmezzi__toast vmezzi__toast--${toast.tipo}`}>
          {toast.msg}
        </div>
      )}
    </div>
  )
}
