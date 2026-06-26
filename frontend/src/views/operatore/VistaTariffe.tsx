import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { getTariffe, creaTariffa, aggiornaTariffa, type Tariffa, type TipoCostoTariffa } from '../../services/TariffaService'
import './VistaTariffe.css'

const TIPI_MEZZO = ['monopattino', 'bicicletta', 'automobile'] as const

const TIPO_LABEL: Record<string, string> = {
  monopattino: 'Monopattino',
  bicicletta: 'Bicicletta',
  automobile: 'Automobile',
}

interface FormState {
  tipo_mezzo: string
  tipo_costo: TipoCostoTariffa
  valore: string
}

const FORM_VUOTO: FormState = {
  tipo_mezzo: TIPI_MEZZO[0],
  tipo_costo: 'minuto',
  valore: '',
}

function tariffaToForm(t: Tariffa): FormState {
  const tipo_costo: TipoCostoTariffa = t.costo_al_minuto !== null ? 'minuto' : 'km'
  const valore = tipo_costo === 'minuto' ? t.costo_al_minuto : t.costo_al_km
  return {
    tipo_mezzo: t.tipo_mezzo,
    tipo_costo,
    valore: valore !== null && valore !== undefined ? String(valore) : '',
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

  const apriNuova = () => {
    setTariffaInModifica(null)
    setForm(FORM_VUOTO)
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

  // [OP-05.1] tipo mezzo già tariffato: blocca la creazione e invita a modificare
  const tipoGiaEsistente =
    !tariffaInModifica && tariffe.some(t => t.tipo_mezzo === form.tipo_mezzo)

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    const valore = parseFloat(form.valore)
    try {
      if (tariffaInModifica) {
        await aggiornaTariffa(tariffaInModifica.tipo_mezzo, form.tipo_costo, valore)
      } else {
        await creaTariffa(form.tipo_mezzo, form.tipo_costo, valore)
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
    !tipoGiaEsistente &&
    form.valore !== '' && parseFloat(form.valore) > 0

  const setTipoMezzo = (e: React.ChangeEvent<HTMLSelectElement>) =>
    setForm(prev => ({ ...prev, tipo_mezzo: e.target.value }))

  const setTipoCosto = (tipo_costo: TipoCostoTariffa) =>
    setForm(prev => ({ ...prev, tipo_costo }))

  const setValore = (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm(prev => ({ ...prev, valore: e.target.value }))

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
          <button className="btn-nuova-tariffa" onClick={apriNuova}>
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
                    {t.costo_al_minuto !== null ? `€${t.costo_al_minuto}/min` : `€${t.costo_al_km}/km`}
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
                <select value={form.tipo_mezzo} onChange={setTipoMezzo}>
                  {TIPI_MEZZO.map(t => (
                    <option key={t} value={t}>{TIPO_LABEL[t]}</option>
                  ))}
                </select>
              )}
            </label>

            {tipoGiaEsistente && (
              <p className="modal-errore-tariffa">
                Tariffa già esistente per questa tipologia. Usa Modifica Tariffa.
              </p>
            )}

            <label>
              Tipo di tariffa *
              <div className="tariffa-tipo-costo-radios">
                <label className="tariffa-radio">
                  <input
                    type="radio"
                    name="tipo_costo"
                    checked={form.tipo_costo === 'minuto'}
                    onChange={() => setTipoCosto('minuto')}
                  />
                  Costo al minuto
                </label>
                <label className="tariffa-radio">
                  <input
                    type="radio"
                    name="tipo_costo"
                    checked={form.tipo_costo === 'km'}
                    onChange={() => setTipoCosto('km')}
                  />
                  Costo al chilometro
                </label>
              </div>
            </label>

            <label>
              {form.tipo_costo === 'minuto' ? 'Costo al minuto (€) *' : 'Costo al km (€) *'}
              <input
                type="number"
                min="0"
                step="0.01"
                value={form.valore}
                onChange={setValore}
                placeholder={form.tipo_costo === 'minuto' ? 'es. 0.15' : 'es. 0.20'}
              />
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
