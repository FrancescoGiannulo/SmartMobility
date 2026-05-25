import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getConfigurazioneFinecorsa,
  salvaConfigurazioneFinecorsa,
  type ConfigurazioneFinecorsa,
} from '../../services/FlottaService'
import './VistaImpostazioniRegole.css'

type TipoVincolo = 'penale' | 'divieto' | 'avviso'

const LABEL_VINCOLO: Record<TipoVincolo, string> = {
  penale: 'Penale',
  divieto: 'Divieto di parcheggio',
  avviso: 'Semplice avviso',
}

// [IF-OP.13] CS-XX — Schermata impostazioni regole fine corsa
export default function VistaImpostazioniRegole() {
  const navigate = useNavigate()

  const [durataPren, setDurataPren] = useState(30)
  const [durataGrazia, setDurataGrazia] = useState(10)
  const [maxMezzi, setMaxMezzi] = useState(1)
  const [tipoVincolo, setTipoVincolo] = useState<TipoVincolo>('avviso')
  const [batteriaMinima, setBatteriaMinima] = useState<string>('')
  const [penaleFuoriZona, setPenaleFuoriZona] = useState(0)
  const [dropdownAperto, setDropdownAperto] = useState(false)

  const [caricamento, setCaricamento] = useState(true)
  const [salvataggio, setSalvataggio] = useState(false)
  const [errore, setErrore] = useState('')
  const [successo, setSuccesso] = useState(false)

  useEffect(() => {
    getConfigurazioneFinecorsa()
      .then((cfg: ConfigurazioneFinecorsa) => {
        setDurataPren(cfg.durata_max_prenotazione_min)
        setDurataGrazia(cfg.durata_periodo_grazia_min)
        setMaxMezzi(cfg.max_mezzi_per_utente)
        setTipoVincolo(cfg.tipo_vincolo)
        setBatteriaMinima(cfg.batteria_minima != null ? String(cfg.batteria_minima) : '')
        setPenaleFuoriZona(cfg.penale_fuori_zona)
      })
      .catch(() => setErrore('Impossibile caricare la configurazione.'))
      .finally(() => setCaricamento(false))
  }, [])

  const handleSalva = useCallback(async () => {
    setErrore('')
    setSuccesso(false)
    setSalvataggio(true)
    try {
      await salvaConfigurazioneFinecorsa({
        durata_max_prenotazione_min: durataPren,
        durata_periodo_grazia_min: durataGrazia,
        max_mezzi_per_utente: maxMezzi,
        tipo_vincolo: tipoVincolo,
        batteria_minima: batteriaMinima !== '' ? Number(batteriaMinima) : null,
        penale_fuori_zona: penaleFuoriZona,
      })
      setSuccesso(true)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore(err.response.data?.detail ?? 'Parametri fuori dai valori ammessi.')
      } else {
        setErrore('Errore durante il salvataggio. Riprova.')
      }
    } finally {
      setSalvataggio(false)
    }
  }, [durataPren, durataGrazia, maxMezzi, tipoVincolo, batteriaMinima, penaleFuoriZona])

  if (caricamento) {
    return <div className="regole-wrap"><p className="regole-loading">Caricamento...</p></div>
  }

  return (
    <div className="regole-wrap">
      <button className="regole-chiudi" onClick={() => navigate(-1)}>✕</button>
      <h1 className="regole-titolo">IMPOSTAZIONI REGOLE</h1>

      <div className="regole-card">
        <div className="regole-riga">
          <span className="regole-label">Durata massima prenotazione:</span>
          <div className="regole-input-unit">
            <input
              className="regole-input"
              type="number"
              min={1}
              value={durataPren}
              onChange={e => setDurataPren(Number(e.target.value))}
            />
            <span className="regole-unit">min</span>
          </div>
        </div>
        <div className="regole-separatore" />

        <div className="regole-riga">
          <span className="regole-label">Durata del periodo di grazia per la pausa corsa:</span>
          <div className="regole-input-unit">
            <input
              className="regole-input"
              type="number"
              min={0}
              value={durataGrazia}
              onChange={e => setDurataGrazia(Number(e.target.value))}
            />
            <span className="regole-unit">min</span>
          </div>
        </div>
        <div className="regole-separatore" />

        <div className="regole-riga">
          <span className="regole-label">Numero massimo di prenotazioni contemporanee per singolo utente:</span>
          <div className="regole-input-unit">
            <input
              className="regole-input"
              type="number"
              min={1}
              value={maxMezzi}
              onChange={e => setMaxMezzi(Number(e.target.value))}
            />
          </div>
        </div>
        <div className="regole-separatore" />

        <div className="regole-riga">
          <span className="regole-label">Batteria minima per fine corsa:</span>
          <div className="regole-input-unit">
            <input
              className="regole-input"
              type="number"
              min={0}
              max={100}
              placeholder="—"
              value={batteriaMinima}
              onChange={e => setBatteriaMinima(e.target.value)}
            />
            <span className="regole-unit">%</span>
          </div>
        </div>
        <div className="regole-separatore" />

        <div className="regole-riga">
          <span className="regole-label">Penale fuori zona (€):</span>
          <div className="regole-input-unit">
            <input
              className="regole-input"
              type="number"
              min={0}
              step={0.5}
              value={penaleFuoriZona}
              onChange={e => setPenaleFuoriZona(Number(e.target.value))}
            />
            <span className="regole-unit">€</span>
          </div>
        </div>
        <div className="regole-separatore" />

        <div className="regole-riga regole-riga-vincolo">
          <span className="regole-label">Regola di business al termine corsa fuori da una zona di parcheggio:</span>
          <div className="regole-dropdown-wrap">
            <button
              className="regole-dropdown-btn"
              onClick={() => setDropdownAperto(v => !v)}
            >
              <span>{LABEL_VINCOLO[tipoVincolo]}</span>
              <span className="regole-dropdown-arrow">▾</span>
            </button>
            {dropdownAperto && (
              <div className="regole-dropdown-menu">
                {(Object.keys(LABEL_VINCOLO) as TipoVincolo[]).map(k => (
                  <button
                    key={k}
                    className={`regole-dropdown-item${tipoVincolo === k ? ' attivo' : ''}`}
                    onClick={() => { setTipoVincolo(k); setDropdownAperto(false) }}
                  >
                    {LABEL_VINCOLO[k]}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {errore && <p className="regole-errore">{errore}</p>}
      {successo && <p className="regole-successo">Regole salvate con successo.</p>}

      <button className="regole-btn-salva" onClick={handleSalva} disabled={salvataggio}>
        {salvataggio ? 'Salvataggio...' : 'SALVA'}
      </button>
    </div>
  )
}
