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

// [IF-UT.06] Salva Metodi di Pagamento / [IF-UT.21] Imposta Metodo Predefinito
export default function VistaPagamenti() {
  const navigate = useNavigate()

  const [metodi, setMetodi] = useState<MetodoPagamento[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [messaggio, setMessaggio] = useState('')

  const [mostraForm, setMostraForm] = useState(false)
  const [nuovoTipo, setNuovoTipo] = useState<string>('carta')
  const [cartaNomeTitolare, setCartaNomeTitolare] = useState('')
  const [cartaCognomeTitolare, setCartaCognomeTitolare] = useState('')
  const [cartaNumero, setCartaNumero] = useState('')
  const [cartaCvc, setCartaCvc] = useState('')
  const [cartaScadenza, setCartaScadenza] = useState('')
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

  const resetFormCarta = () => {
    setCartaNomeTitolare('')
    setCartaCognomeTitolare('')
    setCartaNumero('')
    setCartaCvc('')
    setCartaScadenza('')
  }

  const handleAggiungi = async (e: React.FormEvent) => {
    e.preventDefault()
    setAggiungiInCorso(true)
    setErroreForm('')
    try {
      let dati: Record<string, string> | undefined
      if (nuovoTipo === 'carta') {
        dati = {
          nome_titolare: cartaNomeTitolare.trim(),
          cognome_titolare: cartaCognomeTitolare.trim(),
          numero: cartaNumero.replace(/\s/g, ''),
          cvc: cartaCvc.trim(),
          scadenza: cartaScadenza.trim(),
        }
      }
      await aggiungiMetodo(nuovoTipo, dati)
      setMostraForm(false)
      setNuovoTipo('carta')
      resetFormCarta()
      setMessaggio('Metodo aggiunto.')
      setTimeout(() => setMessaggio(''), 3000)
      await caricaMetodi()
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        setErroreForm('Metodo già presente.')
      } else if (axios.isAxiosError(err) && err.response?.status === 422) {
        const detail = err.response?.data?.detail
        setErroreForm(typeof detail === 'string' ? detail : 'Dati non validi. Verifica le informazioni inserite.')
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
          onClick={() => { setMostraForm(true); setErroreForm(''); resetFormCarta() }}
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
            <div className="pag-carta-fields">
              <label className="pag-label" htmlFor="carta-nome">Nome titolare</label>
              <input
                id="carta-nome"
                type="text"
                className="pag-input"
                placeholder="Mario"
                value={cartaNomeTitolare}
                onChange={e => setCartaNomeTitolare(e.target.value)}
                required
              />

              <label className="pag-label" htmlFor="carta-cognome">Cognome titolare</label>
              <input
                id="carta-cognome"
                type="text"
                className="pag-input"
                placeholder="Rossi"
                value={cartaCognomeTitolare}
                onChange={e => setCartaCognomeTitolare(e.target.value)}
                required
              />

              <label className="pag-label" htmlFor="carta-numero">Numero carta</label>
              <input
                id="carta-numero"
                type="text"
                className="pag-input"
                placeholder="1234 5678 9012 3456"
                maxLength={19}
                value={cartaNumero}
                onChange={e => {
                  const solo = e.target.value.replace(/\D/g, '').slice(0, 16)
                  const formattato = solo.replace(/(\d{4})(?=\d)/g, '$1 ')
                  setCartaNumero(formattato)
                }}
                required
              />

              <div className="pag-carta-row">
                <div className="pag-carta-col">
                  <label className="pag-label" htmlFor="carta-scadenza">Scadenza</label>
                  <input
                    id="carta-scadenza"
                    type="text"
                    className="pag-input"
                    placeholder="MM/AA"
                    maxLength={5}
                    value={cartaScadenza}
                    onChange={e => {
                      let v = e.target.value.replace(/[^\d/]/g, '')
                      if (v.length === 2 && !v.includes('/') && cartaScadenza.length < v.length) {
                        v = v + '/'
                      }
                      setCartaScadenza(v.slice(0, 5))
                    }}
                    required
                  />
                </div>
                <div className="pag-carta-col">
                  <label className="pag-label" htmlFor="carta-cvc">CVC</label>
                  <input
                    id="carta-cvc"
                    type="password"
                    className="pag-input"
                    placeholder="•••"
                    maxLength={4}
                    value={cartaCvc}
                    onChange={e => setCartaCvc(e.target.value.replace(/\D/g, ''))}
                    required
                  />
                </div>
              </div>
            </div>
          )}

          {erroreForm && <p className="pag-errore">{erroreForm}</p>}

          <div className="pag-form-azioni">
            <button type="submit" className="btn-pag-primario" disabled={aggiungiInCorso}>
              {aggiungiInCorso ? 'Aggiunta...' : 'AGGIUNGI'}
            </button>
            <button
              type="button"
              className="btn-pag-annulla"
              onClick={() => { setMostraForm(false); setErroreForm(''); resetFormCarta() }}
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
