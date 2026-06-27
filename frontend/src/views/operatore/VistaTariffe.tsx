import { useEffect, useState, useCallback } from 'react'
import axios from 'axios'
import { getTariffe, creaTariffa, aggiornaTariffa, type Tariffa, type TipoCostoTariffa } from '../../services/TariffaService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import '../../styles/primitives.css'
import './VistaTariffe.css'

const TIPI_MEZZO = ['monopattino', 'bicicletta', 'automobile'] as const

const TIPO_LABEL: Record<string, string> = {
  monopattino: 'Monopattino',
  bicicletta: 'Bicicletta',
  automobile: 'Automobile',
}

const TIPO_EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
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
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vtariffe__header">
          <h2 className="vtariffe__titolo">Tariffe</h2>
          <button
            className="sm-btn sm-btn--primary vtariffe__btn-nuova"
            onClick={apriNuova}
          >
            + Nuova tariffa
          </button>
        </div>

        <div className="vtariffe__body">
          <p className="vtariffe__sezione-label">Tariffe per tipologia di mezzo</p>

          <div className="vtariffe__lista">
            {tariffe.length === 0 ? (
              <div className="vtariffe__vuote">Nessuna tariffa definita. Crea la prima!</div>
            ) : (
              tariffe.map(t => (
                <div className="vtariffe__card sm-card" key={t.id}>
                  <div className="vtariffe__badge">
                    {TIPO_EMOJI[t.tipo_mezzo] ?? '🚗'}
                  </div>
                  <div className="vtariffe__info">
                    <div className="vtariffe__nome">{TIPO_LABEL[t.tipo_mezzo] ?? t.tipo_mezzo}</div>
                    <div className="vtariffe__prezzi sm-mono">
                      {t.costo_al_minuto !== null ? `€${t.costo_al_minuto}/min` : `€${t.costo_al_km}/km`}
                    </div>
                  </div>
                  <button
                    className="vtariffe__btn-modifica"
                    onClick={() => apriModifica(t)}
                    title="Modifica"
                  >
                    ✏️
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {mostraModal && (
          <div className="vtariffe__overlay" onClick={chiudiModal}>
            <div className="vtariffe__modal" onClick={e => e.stopPropagation()}>
              <h3 className="vtariffe__modal-titolo">
                {tariffaInModifica ? 'Modifica tariffa' : 'Nuova tariffa'}
              </h3>

              <label className="vtariffe__label">
                Tipologia mezzo *
                {tariffaInModifica ? (
                  <input
                    className="vtariffe__input"
                    value={TIPO_LABEL[form.tipo_mezzo] ?? form.tipo_mezzo}
                    disabled
                  />
                ) : (
                  <select
                    className="vtariffe__input"
                    value={form.tipo_mezzo}
                    onChange={setTipoMezzo}
                  >
                    {TIPI_MEZZO.map(t => (
                      <option key={t} value={t}>{TIPO_LABEL[t]}</option>
                    ))}
                  </select>
                )}
              </label>

              {tipoGiaEsistente && (
                <p className="vtariffe__errore">
                  Tariffa già esistente per questa tipologia. Usa Modifica Tariffa.
                </p>
              )}

              <label className="vtariffe__label">
                Tipo di tariffa *
                <div className="vtariffe__radios">
                  <label className="vtariffe__radio">
                    <input
                      type="radio"
                      name="tipo_costo"
                      checked={form.tipo_costo === 'minuto'}
                      onChange={() => setTipoCosto('minuto')}
                    />
                    Costo al minuto
                  </label>
                  <label className="vtariffe__radio">
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

              <label className="vtariffe__label">
                {form.tipo_costo === 'minuto' ? 'Costo al minuto (€) *' : 'Costo al km (€) *'}
                <input
                  className="vtariffe__input sm-mono"
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.valore}
                  onChange={setValore}
                  placeholder={form.tipo_costo === 'minuto' ? 'es. 0.15' : 'es. 0.20'}
                />
              </label>

              {errore && <p className="vtariffe__errore">{errore}</p>}

              <div className="vtariffe__modal-azioni">
                <button className="sm-btn sm-btn--ghost vtariffe__btn-modale" onClick={chiudiModal}>
                  Annulla
                </button>
                <button
                  className="sm-btn sm-btn--primary vtariffe__btn-modale"
                  onClick={handleConferma}
                  disabled={caricamento || !datiValidi}
                >
                  {caricamento ? '...' : tariffaInModifica ? 'Salva modifiche' : 'Salva tariffa'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
