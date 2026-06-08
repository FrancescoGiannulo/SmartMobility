import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getOfferte,
  creaOfferta,
  modificaOfferta,
  eliminaOfferta,
  type Offerta,
  type CreaOffertaPayload,
  type TipoMezzo,
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
  tipo_mezzo: string
  stato: string
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
  tipo_mezzo: '',
  stato: 'attiva',
}

function offertaToForm(o: Offerta): FormState {
  const toLocal = (iso: string | null) => {
    if (!iso) return ''
    const d = new Date(iso)
    const pad = (n: number) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
  }
  return {
    nome: o.nome,
    tipo: o.tipo,
    descrizione: o.descrizione ?? '',
    sconto_percentuale: o.sconto_percentuale != null ? String(o.sconto_percentuale) : '',
    prezzo: o.prezzo != null ? String(o.prezzo) : '',
    durata_giorni: o.durata_giorni != null ? String(o.durata_giorni) : '',
    data_inizio: toLocal(o.data_inizio),
    data_scadenza: toLocal(o.data_scadenza),
    tipo_mezzo: o.tipo_mezzo ?? '',
    stato: o.stato,
  }
}

export default function VistaTariffePromozioni() {
  const navigate = useNavigate()
  const [offerte, setOfferte] = useState<Offerta[]>([])
  const [mostraModal, setMostraModal] = useState(false)
  const [offertaInModifica, setOffertaInModifica] = useState<Offerta | null>(null)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  const ricarica = useCallback(() => {
    getOfferte().then(setOfferte).catch(() => {})
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriNuova = () => {
    setOffertaInModifica(null)
    setForm(FORM_VUOTO)
    setErrore('')
    setMostraModal(true)
  }

  const apriModifica = (o: Offerta) => {
    setOffertaInModifica(o)
    setForm(offertaToForm(o))
    setErrore('')
    setMostraModal(true)
  }

  const chiudiModal = () => {
    setMostraModal(false)
    setOffertaInModifica(null)
    setErrore('')
  }

  const handleConferma = async () => {
    setErrore('')
    setCaricamento(true)
    try {
      if (offertaInModifica) {
        await modificaOfferta(offertaInModifica.id, {
          nome: form.nome.trim(),
          descrizione: form.descrizione.trim() || undefined,
          sconto_percentuale: form.sconto_percentuale ? parseFloat(form.sconto_percentuale) : undefined,
          prezzo: form.prezzo ? parseFloat(form.prezzo) : undefined,
          durata_giorni: form.durata_giorni ? parseInt(form.durata_giorni) : undefined,
          data_inizio: form.data_inizio || undefined,
          data_scadenza: form.data_scadenza || undefined,
          tipo_mezzo: form.tipo_mezzo ? (form.tipo_mezzo as TipoMezzo) : null,
          stato: form.stato || undefined,
        })
      } else {
        const payload: CreaOffertaPayload = {
          nome: form.nome.trim(),
          tipo: form.tipo,
          descrizione: form.descrizione.trim() || undefined,
          sconto_percentuale: form.sconto_percentuale ? parseFloat(form.sconto_percentuale) : undefined,
          prezzo: form.prezzo ? parseFloat(form.prezzo) : undefined,
          durata_giorni: form.durata_giorni ? parseInt(form.durata_giorni) : undefined,
          data_inizio: form.data_inizio || undefined,
          data_scadenza: form.data_scadenza || undefined,
          tipo_mezzo: form.tipo_mezzo ? (form.tipo_mezzo as CreaOffertaPayload['tipo_mezzo']) : undefined,
        }
        await creaOfferta(payload)
      }
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

  const dateErrate =
    !!form.data_inizio && !!form.data_scadenza && form.data_scadenza <= form.data_inizio

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
          <button className="btn-nuova-offerta" onClick={apriNuova}>
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
                    {o.tipo === 'abbonamento' && (
                      <span className="offerta-tipo-mezzo-badge">
                        {o.tipo_mezzo ? o.tipo_mezzo.charAt(0).toUpperCase() + o.tipo_mezzo.slice(1) : 'Tutti i mezzi'}
                      </span>
                    )}
                  </div>
                </div>
                <span className={`offerta-stato ${o.stato}`}>{STATO_LABEL[o.stato]}</span>
                <button className="btn-modifica-offerta" onClick={() => apriModifica(o)} title="Modifica">✏️</button>
                <button className="btn-elimina-offerta" onClick={() => handleElimina(o.id)} title="Elimina">🗑</button>
              </div>
            ))
          )}
        </div>
      </div>

      {mostraModal && (
        <div className="modal-overlay-offerta" onClick={chiudiModal}>
          <div className="modal-offerta" onClick={e => e.stopPropagation()}>
            <h3>{offertaInModifica ? 'Modifica offerta' : 'Nuova offerta'}</h3>

            <label>
              Nome *
              <input value={form.nome} onChange={set('nome')} placeholder="es. Estate 2026" />
            </label>

            {!offertaInModifica && (
              <label>
                Tipo *
                <select value={form.tipo} onChange={set('tipo')}>
                  <option value="promozione">Promozione</option>
                  <option value="abbonamento">Abbonamento</option>
                </select>
              </label>
            )}

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
                  Valido per
                  <select value={form.tipo_mezzo} onChange={set('tipo_mezzo')}>
                    <option value="">Tutti i mezzi</option>
                    <option value="bicicletta">Bicicletta</option>
                    <option value="monopattino">Monopattino</option>
                    <option value="automobile">Automobile</option>
                  </select>
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

            {offertaInModifica && (
              <label>
                Stato
                <select value={form.stato} onChange={set('stato')}>
                  <option value="attiva">Attiva</option>
                  <option value="bozza">Bozza</option>
                  <option value="scaduta">Scaduta</option>
                </select>
              </label>
            )}

            {dateErrate && (
              <p className="modal-errore-offerta">La data di scadenza deve essere successiva alla data di inizio.</p>
            )}
            {errore && <p className="modal-errore-offerta">{errore}</p>}

            <div className="modal-azioni-offerta">
              <button className="btn-annulla-offerta" onClick={chiudiModal}>Annulla</button>
              <button className="btn-conferma-offerta" onClick={handleConferma} disabled={caricamento || dateErrate}>
                {caricamento ? '...' : offertaInModifica ? 'Salva modifiche' : 'Salva offerta'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
