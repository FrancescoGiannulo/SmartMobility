import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { getTariffe, creaTariffa, aggiornaTariffa, type Tariffa } from '../../services/TariffaService'
import './VistaTariffe.css'

const TIPI_MEZZO = ['monopattino', 'bicicletta', 'automobile'] as const

const TIPO_LABEL: Record<string, string> = {
  monopattino: 'Monopattino',
  bicicletta: 'Bicicletta',
  automobile: 'Automobile',
}

interface FormState {
  tipo_mezzo: string
  costo_al_minuto: string
  costo_al_km: string
}

const FORM_VUOTO: FormState = {
  tipo_mezzo: '',
  costo_al_minuto: '',
  costo_al_km: '',
}

function tariffaToForm(t: Tariffa): FormState {
  return {
    tipo_mezzo: t.tipo_mezzo,
    costo_al_minuto: String(t.costo_al_minuto),
    costo_al_km: String(t.costo_al_km),
  }
}

// [IF-OP.07] Definisce Tariffa / [IF-OP.08] Modifica Tariffa
export default function VistaTariffe() {
  const navigate = useNavigate()
  const [tariffe, setTariffe] = useState<Tariffa[]>([])
  const [mostraModal, setMostraModal] = useState(false)
  const [tariffaInModifica, setTariffaInModifica] = useState<Tariffa | null>(null)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricarica = useCallback(() => {
    getTariffe().then(r => setTariffe(r.data)).catch(() => {})
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const tipiDisponibili = TIPI_MEZZO.filter(
    t => !tariffe.some(tariffa => tariffa.tipo_mezzo === t)
  )

  const apriNuova = () => {
    setTariffaInModifica(null)
    setForm({ ...FORM_VUOTO, tipo_mezzo: tipiDisponibili[0] ?? '' })
    setErrore('')
    setMostraModal(true)
  }

  const apriModifica = (t: Tariffa) => {
    setTariffaInModifica(t)
    setForm(tariffaToForm(t))
    setErrore('')
    setMostraModal(true)
  }

  const chiudiModal = () => {
    setMostraModal(false)
    setTariffaInModifica(null)
    setErrore('')
  }

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    const costoMinuto = parseFloat(form.costo_al_minuto)
    const costoKm = parseFloat(form.costo_al_km)
    try {
      if (tariffaInModifica) {
        await aggiornaTariffa(tariffaInModifica.tipo_mezzo, costoMinuto, costoKm)
      } else {
        await creaTariffa(form.tipo_mezzo, costoMinuto, costoKm)
      }
      chiudiModal()
      ricarica()
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const status = err.response?.status
        if (status === 409) setErrore('Tariffa già esistente per questa tipologia. Usa Modifica Tariffa.')
        else if (status === 404) setErrore('Tariffa non trovata.')
        else if (status === 422) setErrore('Dati non validi. Controlla i campi.')
        else setErrore('Errore durante il salvataggio. Riprova.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const datiValidi =
    !!form.tipo_mezzo &&
    form.costo_al_minuto !== '' && parseFloat(form.costo_al_minuto) >= 0 &&
    form.costo_al_km !== '' && parseFloat(form.costo_al_km) >= 0

  const set = (field: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(prev => ({ ...prev, [field]: e.target.value }))

  return (
    <div className="vista-tariffe">
      <div className="tariffe-topbar">
        <h2>Tariffe</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="tariffe-body">
        <div className="tariffe-header-row">
          <h3>Tariffe per tipologia di mezzo</h3>
          <button className="btn-nuova-tariffa" onClick={apriNuova} disabled={tipiDisponibili.length === 0}>
            + Nuova tariffa
          </button>
        </div>

        <div className="tariffe-lista">
          {tariffe.length === 0 ? (
            <div className="tariffe-vuote">Nessuna tariffa definita. Crea la prima!</div>
          ) : (
            tariffe.map(t => (
              <div className="tariffa-card" key={t.id}>
                <div className="tariffa-tipo-badge">{TIPO_LABEL[t.tipo_mezzo] ?? t.tipo_mezzo}</div>
                <div className="tariffa-info">
                  <div className="tariffa-nome">{TIPO_LABEL[t.tipo_mezzo] ?? t.tipo_mezzo}</div>
                  <div className="tariffa-dettaglio">
                    €{t.costo_al_minuto}/min · €{t.costo_al_km}/km
                  </div>
                </div>
                <button className="btn-modifica-tariffa" onClick={() => apriModifica(t)} title="Modifica">✏️</button>
              </div>
            ))
          )}
        </div>
      </div>

      {mostraModal && (
        <div className="modal-overlay-tariffa" onClick={chiudiModal}>
          <div className="modal-tariffa" onClick={e => e.stopPropagation()}>
            <h3>{tariffaInModifica ? 'Modifica tariffa' : 'Nuova tariffa'}</h3>

            <label>
              Tipologia mezzo *
              {tariffaInModifica ? (
                <input value={TIPO_LABEL[form.tipo_mezzo] ?? form.tipo_mezzo} disabled />
              ) : (
                <select value={form.tipo_mezzo} onChange={set('tipo_mezzo')}>
                  {tipiDisponibili.map(t => (
                    <option key={t} value={t}>{TIPO_LABEL[t]}</option>
                  ))}
                </select>
              )}
            </label>

            <label>
              Costo al minuto (€) *
              <input type="number" min="0" step="0.01" value={form.costo_al_minuto} onChange={set('costo_al_minuto')} placeholder="es. 0.15" />
            </label>

            <label>
              Costo al km (€) *
              <input type="number" min="0" step="0.01" value={form.costo_al_km} onChange={set('costo_al_km')} placeholder="es. 0.20" />
            </label>

            {errore && <p className="modal-errore-tariffa">{errore}</p>}

            <div className="modal-azioni-tariffa">
              <button className="btn-annulla-tariffa" onClick={chiudiModal}>Annulla</button>
              <button className="btn-conferma-tariffa" onClick={handleConferma} disabled={caricamento || !datiValidi}>
                {caricamento ? '...' : tariffaInModifica ? 'Salva modifiche' : 'Salva tariffa'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
