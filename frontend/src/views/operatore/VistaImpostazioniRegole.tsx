import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  getRegolaFinecorsa,
  salvaRegolaFinecorsa,
  type SalvaRegolaPayload,
} from '../../services/RegolaFinecorsaService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import './VistaImpostazioniRegole.css'

const LABEL_VINCOLO: Record<string, string> = {
  penale: 'Penale (addebito importo)',
  divieto: 'Blocco fine corsa',
  avviso: 'Avviso (nessun addebito)',
}

export default function VistaImpostazioniRegole() {
  const [tipoVincolo, setTipoVincolo] = useState<'penale' | 'divieto' | 'avviso'>('avviso')
  const [penale, setPenale] = useState('')
  const [batteria, setBatteria] = useState('')
  const [bonusAttivo, setBonusAttivo] = useState(false)
  const [bonusParcheggi, setBonusParcheggi] = useState('')
  const [bonusValore, setBonusValore] = useState('')
  const [errore, setErrore] = useState('')
  const [conferma, setConferma] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  useEffect(() => {
    getRegolaFinecorsa().then(regola => {
      if (!regola) return
      setTipoVincolo(regola.tipo_vincolo)
      setPenale(regola.penale_fuori_zona > 0 ? String(regola.penale_fuori_zona) : '')
      setBatteria(regola.batteria_minima != null ? String(regola.batteria_minima) : '')
      if (regola.bonus_parcheggi_corretti != null) {
        setBonusAttivo(true)
        setBonusParcheggi(String(regola.bonus_parcheggi_corretti))
        setBonusValore(regola.bonus_valore != null ? String(regola.bonus_valore) : '')
      }
    }).catch(() => {})
  }, [])

  const handleSalva = async () => {
    setErrore('')
    setConferma('')
    setCaricamento(true)
    try {
      const payload: SalvaRegolaPayload = {
        tipo_vincolo: tipoVincolo,
        penale_fuori_zona: penale ? parseFloat(penale) : 0,
        batteria_minima: batteria ? parseInt(batteria) : undefined,
        bonus_parcheggi_corretti: bonusAttivo && bonusParcheggi ? parseInt(bonusParcheggi) : undefined,
        bonus_valore: bonusAttivo && bonusValore ? parseFloat(bonusValore) : undefined,
      }
      await salvaRegolaFinecorsa(payload)
      setConferma('✅ Regole di fine corsa salvate correttamente.')
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail
        setErrore(typeof detail === 'string' ? detail : 'Dati non validi. Controlla i campi.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  return (
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vregole__header">
          <h2>Impostazioni Regole Fine Corsa</h2>
        </div>

        <div className="vregole__body">
          <div className="vregole__card sm-card">
            <h3>Politica sanzionatoria</h3>
            <div className="vregole__campo">
              <label>Vincolo rilascio fuori zona parcheggio</label>
              <select value={tipoVincolo} onChange={e => setTipoVincolo(e.target.value as typeof tipoVincolo)}>
                {Object.entries(LABEL_VINCOLO).map(([val, label]) => (
                  <option key={val} value={val}>{label}</option>
                ))}
              </select>
            </div>
            {tipoVincolo === 'penale' && (
              <div className="vregole__campo">
                <label>Importo penale (€)</label>
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={penale}
                  onChange={e => setPenale(e.target.value)}
                  placeholder="es. 5.00"
                />
              </div>
            )}
          </div>

          <div className="vregole__card sm-card">
            <h3>Vincoli aggiuntivi</h3>
            <div className="vregole__campo">
              <label>Batteria minima richiesta (%)</label>
              <input
                type="number"
                min="0"
                max="100"
                value={batteria}
                onChange={e => setBatteria(e.target.value)}
                placeholder="Lascia vuoto per nessun vincolo"
              />
            </div>
          </div>

          <div className="vregole__card sm-card">
            <h3>Incentivo parcheggio corretto</h3>
            <label className="vregole__bonus-toggle">
              <input type="checkbox" checked={bonusAttivo} onChange={e => setBonusAttivo(e.target.checked)} />
              Attiva bonus per parcheggi corretti
            </label>
            {bonusAttivo && (
              <>
                <div className="vregole__campo">
                  <label>Numero parcheggi corretti necessari</label>
                  <input
                    type="number"
                    min="1"
                    value={bonusParcheggi}
                    onChange={e => setBonusParcheggi(e.target.value)}
                    placeholder="es. 5"
                  />
                </div>
                <div className="vregole__campo">
                  <label>Valore bonus (€)</label>
                  <input
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={bonusValore}
                    onChange={e => setBonusValore(e.target.value)}
                    placeholder="es. 2.50"
                  />
                </div>
              </>
            )}
          </div>

          {errore && <p className="vregole__errore">{errore}</p>}
          {conferma && <p className="vregole__conferma">{conferma}</p>}

          <button className="vregole__btn-salva sm-btn sm-btn--primary" onClick={handleSalva} disabled={caricamento}>
            {caricamento ? '...' : 'Salva regole'}
          </button>
        </div>
      </div>
    </div>
  )
}
