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

const IconaCarta = () => (
  <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#155e52" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="1" y="4" width="22" height="16" rx="3" />
    <line x1="1" y1="10" x2="23" y2="10" />
  </svg>
)

const IconaGoogle = () => (
  <svg viewBox="0 0 24 24" width="28" height="28">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 0 0 1 12c0 1.77.42 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
  </svg>
)

const IconaApple = () => (
  <svg viewBox="0 0 24 24" width="28" height="28" fill="#000">
    <path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.32 2.32-1.55 4.16-3.74 4.25z"/>
  </svg>
)

const IconaPaypal = () => (
  <svg viewBox="0 0 24 24" width="28" height="28">
    <path d="M7.02 21.5l.4-2.48h-.93L9.5 3.5h5.09c1.69 0 2.87.35 3.52 1.05.63.67.83 1.63.6 2.86-.06.33-.15.68-.27 1.04-.13.36-.29.71-.49 1.04a5.1 5.1 0 0 1-1.65 1.86c-.72.5-1.57.83-2.55.98l-.37.04H11.5l-.63 3.98-.05.24H7.02z" fill="#003087"/>
    <path d="M18.14 7.1c-.02.11-.04.22-.06.34-.74 3.8-3.28 5.12-6.52 5.12H10.1l-.8 5.09-.23 1.44h2.72l.38-2.38.02-.13.46-2.88.03-.15h.3c2.65 0 4.72-1.07 5.33-4.18.25-1.3.12-2.38-.47-3.14a2.7 2.7 0 0 0-.65-.53l-.05.4z" fill="#0070E0"/>
  </svg>
)

const ICONA_TIPO: Record<string, () => React.ReactNode> = {
  carta:      IconaCarta,
  paypal:     IconaPaypal,
  google_pay: IconaGoogle,
  apple_pay:  IconaApple,
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
                  <span className="pag-card-icona">{ICONA_TIPO[m.tipo]?.() ?? '💰'}</span>
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
              <option key={t} value={t}>{LABEL_TIPO[t]}</option>
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
