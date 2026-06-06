import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getOfferte,
  creaOfferta,
  eliminaOfferta,
  type Offerta,
  type CreaOffertaPayload,
} from '../../services/OffertaService'
import './VistaTariffePromozioni.css'

const STATO_LABEL: Record<string, string> = {
  attiva: 'Attiva',
  scaduta: 'Scaduta',
  bozza: 'Bozza',
}

const TIPO_EMOJI: Record<string, string> = {
  promozione: '🏷️',
  abbonamento: '📅',
}

interface FormState {
  nome: string
  tipo: 'promozione' | 'abbonamento'
  descrizione: string
  sconto_percentuale: string
  prezzo: string
  durata_giorni: string
  data_inizio: string
  data_scadenza: string
}

const FORM_VUOTO: FormState = {
  nome: '',
  tipo: 'promozione',
  descrizione: '',
  sconto_percentuale: '',
  prezzo: '',
  durata_giorni: '',
  data_inizio: '',
  data_scadenza: '',
}

export default function VistaTariffePromozioni() {
  const navigate = useNavigate()
  const [offerte, setOfferte] = useState<Offerta[]>([])
  const [mostraModal, setMostraModal] = useState(false)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricarica = useCallback(() => {
    getOfferte().then(setOfferte).catch(() => {})
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriModal = () => {
    setForm(FORM_VUOTO)
    setErrore('')
    setMostraModal(true)
  }

  const chiudiModal = () => {
    setMostraModal(false)
    setErrore('')
  }

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    try {
      const payload: CreaOffertaPayload = {
        nome: form.nome.trim(),
        tipo: form.tipo,
        descrizione: form.descrizione.trim() || undefined,
        sconto_percentuale: form.sconto_percentuale ? parseFloat(form.sconto_percentuale) : undefined,
        prezzo: form.prezzo ? parseFloat(form.prezzo) : undefined,
        durata_giorni: form.durata_giorni ? parseInt(form.durata_giorni) : undefined,
        data_inizio: form.data_inizio || undefined,
        data_scadenza: form.data_scadenza || undefined,
      }
      await creaOfferta(payload)
      chiudiModal()
      ricarica()
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const status = err.response?.status
        const detail = err.response?.data?.detail
        if (status === 409) setErrore("Esiste già un'offerta con questo nome.")
        else if (status === 422) setErrore(typeof detail === 'string' ? detail : 'Dati non validi. Controlla i campi.')
        else setErrore('Errore durante il salvataggio. Riprova.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const handleElimina = async (id: string) => {
    if (!confirm('Eliminare questa offerta?')) return
    await eliminaOfferta(id).catch(() => {})
    ricarica()
  }

  const set = (field: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(prev => ({ ...prev, [field]: e.target.value }))

  return (
    <div className="vista-tariffe">
      <div className="tariffe-topbar">
        <h2>Tariffe e Promozioni</h2>
        <button className="btn-indietro" onClick={() => navigate('/operatore/dashboard')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="tariffe-body">
        <div className="tariffe-header-row">
          <h3>Offerte commerciali</h3>
          <button className="btn-nuova-offerta" onClick={apriModal}>
            + Nuova offerta
          </button>
        </div>

        <div className="offerte-lista">
          {offerte.length === 0 ? (
            <div className="offerte-vuote">Nessuna offerta definita. Crea la prima!</div>
          ) : (
            offerte.map(o => (
              <div className="offerta-card" key={o.id}>
                <div className={`offerta-tipo-badge ${o.tipo}`}>
                  {TIPO_EMOJI[o.tipo]}
                </div>
                <div className="offerta-info">
                  <div className="offerta-nome">{o.nome}</div>
                  <div className="offerta-dettaglio">
                    {o.tipo === 'promozione'
                      ? `Sconto ${o.sconto_percentuale}% — scade ${o.data_scadenza ? new Date(o.data_scadenza).toLocaleDateString('it-IT') : '—'}`
                      : `€${o.prezzo} · ${o.durata_giorni} giorni`}
                  </div>
                </div>
                <span className={`offerta-stato ${o.stato}`}>{STATO_LABEL[o.stato]}</span>
                <button className="btn-elimina-offerta" onClick={() => handleElimina(o.id)} title="Elimina">🗑</button>
              </div>
            ))
          )}
        </div>
      </div>

      {mostraModal && (
        <div className="modal-overlay-offerta" onClick={chiudiModal}>
          <div className="modal-offerta" onClick={e => e.stopPropagation()}>
            <h3>Nuova offerta</h3>

            <label>
              Nome *
              <input value={form.nome} onChange={set('nome')} placeholder="es. Estate 2026" />
            </label>

            <label>
              Tipo *
              <select value={form.tipo} onChange={set('tipo')}>
                <option value="promozione">Promozione</option>
                <option value="abbonamento">Abbonamento</option>
              </select>
            </label>

            <label>
              Descrizione
              <input value={form.descrizione} onChange={set('descrizione')} placeholder="Descrizione opzionale" />
            </label>

            {form.tipo === 'promozione' && (
              <>
                <label>
                  Sconto (%) *
                  <input type="number" min="1" max="100" value={form.sconto_percentuale} onChange={set('sconto_percentuale')} placeholder="es. 20" />
                </label>
                <label>
                  Data scadenza *
                  <input type="datetime-local" value={form.data_scadenza} onChange={set('data_scadenza')} />
                </label>
              </>
            )}

            {form.tipo === 'abbonamento' && (
              <>
                <label>
                  Prezzo (€) *
                  <input type="number" min="0.01" step="0.01" value={form.prezzo} onChange={set('prezzo')} placeholder="es. 29.99" />
                </label>
                <label>
                  Durata (giorni) *
                  <input type="number" min="1" value={form.durata_giorni} onChange={set('durata_giorni')} placeholder="es. 30" />
                </label>
                <label>
                  Data inizio
                  <input type="datetime-local" value={form.data_inizio} onChange={set('data_inizio')} />
                </label>
                <label>
                  Data scadenza
                  <input type="datetime-local" value={form.data_scadenza} onChange={set('data_scadenza')} />
                </label>
              </>
            )}

            {errore && <p className="modal-errore-offerta">{errore}</p>}

            <div className="modal-azioni-offerta">
              <button className="btn-annulla-offerta" onClick={chiudiModal}>Annulla</button>
              <button className="btn-conferma-offerta" onClick={handleConferma} disabled={caricamento}>
                {caricamento ? '...' : 'Salva offerta'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
