import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { getTariffe, creaTariffa, aggiornaTariffa, type Tariffa } from '../../services/FlottaService'
import './VistaTariffePromozioni.css'

const TIPI_MEZZO = ['monopattino', 'bicicletta', 'automobile'] as const

const EMOJI_MEZZO: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

// [IF-OP.07] Definisce Tariffa
export default function VistaTariffePromozioni() {
  const navigate = useNavigate()

  const [tariffe, setTariffe] = useState<Tariffa[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [messaggio, setMessaggio] = useState('')

  const [mostraForm, setMostraForm] = useState(false)
  const [tipoMezzo, setTipoMezzo] = useState<string>('monopattino')
  const [costoMinuto, setCostoMinuto] = useState('')
  const [costoKm, setCostoKm] = useState('')
  const [invioInCorso, setInvioInCorso] = useState(false)
  const [erroreForm, setErroreForm] = useState('')

  const [modificaId, setModificaId] = useState<string | null>(null)
  const [modMinuto, setModMinuto] = useState('')
  const [modKm, setModKm] = useState('')
  const [modInCorso, setModInCorso] = useState(false)
  const [erroreModifica, setErroreModifica] = useState('')

  const caricaTariffe = useCallback(async () => {
    try {
      const res = await getTariffe()
      setTariffe(res.data)
    } catch {
      setErrore('Impossibile caricare le tariffe.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaTariffe() }, [caricaTariffe])

  const apriModifica = (t: Tariffa) => {
    setModificaId(t.tipo_mezzo)
    setModMinuto(t.costo_al_minuto.toFixed(4))
    setModKm(t.costo_al_km.toFixed(4))
    setErroreModifica('')
  }

  const handleModifica = async (e: React.FormEvent, tipo_mezzo: string) => {
    e.preventDefault()
    const minuto = parseFloat(modMinuto)
    const km = parseFloat(modKm)
    if (isNaN(minuto) || minuto <= 0 || isNaN(km) || km <= 0) {
      setErroreModifica('I costi devono essere numeri maggiori di zero.')
      return
    }
    setModInCorso(true)
    setErroreModifica('')
    try {
      await aggiornaTariffa(tipo_mezzo, minuto, km)
      setModificaId(null)
      setMessaggio('Tariffa aggiornata.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaTariffe()
    } catch {
      setErroreModifica('Errore durante l\'aggiornamento. Riprova.')
    } finally {
      setModInCorso(false)
    }
  }

  const tipiDisponibili = TIPI_MEZZO.filter(
    t => !tariffe.some(ta => ta.tipo_mezzo === t)
  )

  const handleCrea = async (e: React.FormEvent) => {
    e.preventDefault()
    const minuto = parseFloat(costoMinuto)
    const km = parseFloat(costoKm)
    if (isNaN(minuto) || minuto <= 0 || isNaN(km) || km <= 0) {
      setErroreForm('I costi devono essere numeri maggiori di zero.')
      return
    }
    setInvioInCorso(true)
    setErroreForm('')
    try {
      await creaTariffa(tipoMezzo, minuto, km)
      setMostraForm(false)
      setCostoMinuto('')
      setCostoKm('')
      setMessaggio('Tariffa creata con successo.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaTariffe()
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErroreForm('Tariffa già esistente. Usa Modifica Tariffa (IF-OP.08).')
      } else {
        setErroreForm('Errore durante la creazione. Riprova.')
      }
    } finally {
      setInvioInCorso(false)
    }
  }

  return (
    <div className="vista-tariffe-wrap">
      <button type="button" className="btn-back-tariffe" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="tariffe-titolo">Tariffe</h1>

      {messaggio && <div className="tariffe-messaggio">{messaggio}</div>}
      {errore && <p className="tariffe-errore">{errore}</p>}

      {caricamento ? (
        <p className="tariffe-caricamento">Caricamento...</p>
      ) : tariffe.length === 0 ? (
        <p className="tariffe-vuoto">Nessuna tariffa definita.</p>
      ) : (
        <div className="tariffe-lista">
          {tariffe.map(t => (
            <div key={t.id} className="tariffa-card">
              <div className="tariffa-card-header">
                <span className="tariffa-emoji">{EMOJI_MEZZO[t.tipo_mezzo] ?? '🚌'}</span>
                <div className="tariffa-info">
                  <span className="tariffa-tipo">{t.tipo_mezzo.charAt(0).toUpperCase() + t.tipo_mezzo.slice(1)}</span>
                  <span className="tariffa-costi">
                    €{t.costo_al_minuto.toFixed(4)}/min · €{t.costo_al_km.toFixed(4)}/km
                  </span>
                </div>
                <button
                  type="button"
                  className="btn-modifica-tariffa"
                  onClick={() => modificaId === t.tipo_mezzo ? setModificaId(null) : apriModifica(t)}
                >
                  {modificaId === t.tipo_mezzo ? 'Annulla' : 'Modifica'}
                </button>
              </div>
              {modificaId === t.tipo_mezzo && (
                <form className="modifica-form" onSubmit={e => handleModifica(e, t.tipo_mezzo)}>
                  <div className="modifica-row">
                    <div className="modifica-campo">
                      <label className="tariffe-label" htmlFor={`min-${t.tipo_mezzo}`}>€/min</label>
                      <input
                        id={`min-${t.tipo_mezzo}`}
                        type="number"
                        className="tariffe-input"
                        step="0.0001"
                        min="0.0001"
                        value={modMinuto}
                        onChange={e => setModMinuto(e.target.value)}
                        required
                      />
                    </div>
                    <div className="modifica-campo">
                      <label className="tariffe-label" htmlFor={`km-${t.tipo_mezzo}`}>€/km</label>
                      <input
                        id={`km-${t.tipo_mezzo}`}
                        type="number"
                        className="tariffe-input"
                        step="0.0001"
                        min="0.0001"
                        value={modKm}
                        onChange={e => setModKm(e.target.value)}
                        required
                      />
                    </div>
                  </div>
                  {erroreModifica && <p className="tariffe-errore">{erroreModifica}</p>}
                  <button type="submit" className="btn-tariffe-primario" disabled={modInCorso}>
                    {modInCorso ? 'Salvataggio...' : 'SALVA'}
                  </button>
                </form>
              )}
            </div>
          ))}
        </div>
      )}

      {!mostraForm ? (
        tipiDisponibili.length > 0 ? (
          <button
            type="button"
            className="btn-tariffe-primario"
            onClick={() => {
              setTipoMezzo(tipiDisponibili[0])
              setMostraForm(true)
              setErroreForm('')
            }}
          >
            + Aggiungi tariffa
          </button>
        ) : (
          <p className="tariffe-completo">Tutte le tipologie di mezzo hanno una tariffa definita.</p>
        )
      ) : (
        <form className="tariffe-form" onSubmit={handleCrea}>
          <h2 className="tariffe-form-titolo">Nuova tariffa</h2>

          <label className="tariffe-label" htmlFor="tipo-mezzo">Tipologia mezzo</label>
          <select
            id="tipo-mezzo"
            className="tariffe-select"
            value={tipoMezzo}
            onChange={e => setTipoMezzo(e.target.value)}
          >
            {tipiDisponibili.map(t => (
              <option key={t} value={t}>{EMOJI_MEZZO[t]} {t.charAt(0).toUpperCase() + t.slice(1)}</option>
            ))}
          </select>

          <label className="tariffe-label" htmlFor="costo-minuto">Costo al minuto (€)</label>
          <input
            id="costo-minuto"
            type="number"
            className="tariffe-input"
            placeholder="es. 0.05"
            step="0.0001"
            min="0.0001"
            value={costoMinuto}
            onChange={e => setCostoMinuto(e.target.value)}
            required
          />

          <label className="tariffe-label" htmlFor="costo-km">Costo al km (€)</label>
          <input
            id="costo-km"
            type="number"
            className="tariffe-input"
            placeholder="es. 0.10"
            step="0.0001"
            min="0.0001"
            value={costoKm}
            onChange={e => setCostoKm(e.target.value)}
            required
          />

          {erroreForm && <p className="tariffe-errore">{erroreForm}</p>}

          <div className="tariffe-form-azioni">
            <button type="submit" className="btn-tariffe-primario" disabled={invioInCorso}>
              {invioInCorso ? 'Salvataggio...' : 'SALVA'}
            </button>
            <button
              type="button"
              className="btn-tariffe-annulla"
              onClick={() => { setMostraForm(false); setErroreForm('') }}
              disabled={invioInCorso}
            >
              Annulla
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
