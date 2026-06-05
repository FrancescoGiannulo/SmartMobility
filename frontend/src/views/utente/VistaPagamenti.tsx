import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getMetodiPagamento,
  aggiungiMetodo,
  impostaPredefinito,
  rimuoviMetodo,
  type MetodoPagamento,
} from '../../services/PaymentService'
import './VistaPagamenti.css'

const EMOJI_TIPO: Record<string, string> = {
  carta:      '💳',
  paypal:     '💜',
  google_pay: '📱',
  apple_pay:  '🍎',
}

const LABEL_TIPO: Record<string, string> = {
  carta:      'Carta di credito',
  paypal:     'PayPal',
  google_pay: 'Google Pay',
  apple_pay:  'Apple Pay',
}

const TIPI_DISPONIBILI = ['carta', 'paypal', 'google_pay', 'apple_pay'] as const

// [IF-UT.12] Salva Metodi di Pagamento / [IF-UT.21] Imposta Metodo Predefinito
export default function VistaPagamenti() {
  const navigate = useNavigate()

  const [metodi, setMetodi] = useState<MetodoPagamento[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [messaggio, setMessaggio] = useState('')

  const [mostraForm, setMostraForm] = useState(false)
  const [nuovoTipo, setNuovoTipo] = useState<string>('carta')
  const [nuovoLastFour, setNuovoLastFour] = useState('')
  const [aggiungiInCorso, setAggiungiInCorso] = useState(false)
  const [erroreForm, setErroreForm] = useState('')

  const [azioneInCorso, setAzioneInCorso] = useState<string | null>(null)

  const caricaMetodi = useCallback(async () => {
    try {
      const lista = await getMetodiPagamento()
      setMetodi(lista)
    } catch {
      setErrore('Impossibile caricare i metodi di pagamento.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaMetodi() }, [caricaMetodi])

  const handleAggiungi = async (e: React.FormEvent) => {
    e.preventDefault()
    setAggiungiInCorso(true)
    setErroreForm('')
    try {
      const lastFour = nuovoTipo === 'carta' ? nuovoLastFour.trim() || undefined : undefined
      await aggiungiMetodo(nuovoTipo, lastFour)
      setMostraForm(false)
      setNuovoTipo('carta')
      setNuovoLastFour('')
      setMessaggio('Metodo aggiunto.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaMetodi()
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErroreForm('Metodo già presente.')
      } else if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErroreForm('Dati non validi. Verifica le informazioni inserite.')
      } else {
        setErroreForm('Errore durante l\'aggiunta. Riprova.')
      }
    } finally {
      setAggiungiInCorso(false)
    }
  }

  const handlePredefinito = async (id: string) => {
    setAzioneInCorso(id + '-pred')
    setErrore('')
    try {
      await impostaPredefinito(id)
      setMessaggio('Metodo impostato come predefinito.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaMetodi()
    } catch {
      setErrore('Errore durante l\'operazione. Riprova.')
    } finally {
      setAzioneInCorso(null)
    }
  }

  const handleRimuovi = async (id: string) => {
    setAzioneInCorso(id + '-del')
    setErrore('')
    try {
      await rimuoviMetodo(id)
      setMessaggio('Metodo rimosso.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaMetodi()
    } catch {
      setErrore('Errore durante la rimozione. Riprova.')
    } finally {
      setAzioneInCorso(null)
    }
  }

  return (
    <div className="vista-pagamenti-wrap">
      <button type="button" className="btn-back-pag" onClick={() => navigate(-1)}>
        ← Torna indietro
      </button>

      <h1 className="pag-titolo">Metodi di pagamento</h1>

      {messaggio && <div className="pag-messaggio">{messaggio}</div>}
      {errore && <p className="pag-errore">{errore}</p>}

      {caricamento ? (
        <p className="pag-caricamento">Caricamento...</p>
      ) : metodi.length === 0 ? (
        <p className="pag-vuoto">Nessun metodo salvato. Aggiungi il tuo primo metodo di pagamento.</p>
      ) : (
        <>
          {metodi.length > 1 && !metodi.some(m => m.predefinito) && (
            <p className="pag-avviso">
              Hai più metodi di pagamento. Impostane uno come predefinito per procedere al pagamento.
            </p>
          )}
          <div className="pag-lista">
            {metodi.map(m => (
              <div key={m.id} className={`pag-card${m.predefinito ? ' pag-card--predefinito' : ''}`}>
                <div className="pag-card-info">
                  <span className="pag-card-emoji">{EMOJI_TIPO[m.tipo] ?? '💰'}</span>
                  <div className="pag-card-dettagli">
                    <span className="pag-card-tipo">{LABEL_TIPO[m.tipo] ?? m.tipo}</span>
                    {m.last_four && (
                      <span className="pag-card-last-four">•••• {m.last_four}</span>
                    )}
                  </div>
                  {m.predefinito && (
                    <span className="pag-badge-predefinito">★ Predefinito</span>
                  )}
                </div>
                <div className="pag-card-azioni">
                  {metodi.length > 1 && !m.predefinito && (
                    <button
                      type="button"
                      className="btn-pag-secondario"
                      onClick={() => handlePredefinito(m.id)}
                      disabled={azioneInCorso !== null}
                    >
                      {azioneInCorso === m.id + '-pred' ? '...' : 'Imposta predefinito'}
                    </button>
                  )}
                  <button
                    type="button"
                    className="btn-pag-rimuovi"
                    onClick={() => handleRimuovi(m.id)}
                    disabled={azioneInCorso !== null}
                    aria-label="Rimuovi metodo"
                  >
                    {azioneInCorso === m.id + '-del' ? '...' : '✕'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {!mostraForm ? (
        <button
          type="button"
          className="btn-pag-primario"
          onClick={() => { setMostraForm(true); setErroreForm('') }}
        >
          + Aggiungi metodo
        </button>
      ) : (
        <form className="pag-form" onSubmit={handleAggiungi}>
          <h2 className="pag-form-titolo">Nuovo metodo</h2>

          <label className="pag-label" htmlFor="tipo-metodo">Tipo</label>
          <select
            id="tipo-metodo"
            className="pag-select"
            value={nuovoTipo}
            onChange={e => setNuovoTipo(e.target.value)}
          >
            {TIPI_DISPONIBILI.map(t => (
              <option key={t} value={t}>{EMOJI_TIPO[t]} {LABEL_TIPO[t]}</option>
            ))}
          </select>

          {nuovoTipo === 'carta' && (
            <>
              <label className="pag-label" htmlFor="last-four">Ultime 4 cifre</label>
              <input
                id="last-four"
                type="text"
                className="pag-input"
                placeholder="es. 1234"
                maxLength={4}
                pattern="\d{4}"
                value={nuovoLastFour}
                onChange={e => setNuovoLastFour(e.target.value.replace(/\D/g, ''))}
              />
            </>
          )}

          {erroreForm && <p className="pag-errore">{erroreForm}</p>}

          <div className="pag-form-azioni">
            <button type="submit" className="btn-pag-primario" disabled={aggiungiInCorso}>
              {aggiungiInCorso ? 'Aggiunta...' : 'AGGIUNGI'}
            </button>
            <button
              type="button"
              className="btn-pag-annulla"
              onClick={() => { setMostraForm(false); setErroreForm('') }}
              disabled={aggiungiInCorso}
            >
              Annulla
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
