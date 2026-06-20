// frontend/src/views/utente/VistaRecensione.tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { scriviRecensione, type Recensione } from '../../services/RecensioneService'
import './VistaRecensione.css'

function formatData(iso: string) {
  return new Date(iso).toLocaleDateString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  })
}

// [IF-UT.15] Scrive Recensione
export default function VistaRecensione() {
  const navigate = useNavigate()

  const [voto, setVoto] = useState(0)
  const [commento, setCommento] = useState('')
  const [invioInCorso, setInvioInCorso] = useState(false)
  const [recensioneInviata, setRecensioneInviata] = useState<Recensione | null>(null)
  const [errore, setErrore] = useState('')

  const confermaScrivi = async (e: React.FormEvent) => {
    e.preventDefault()
    if (voto < 1 || voto > 5) {
      setErrore('Seleziona un voto da 1 a 5 stelle.')
      return
    }
    setInvioInCorso(true)
    setErrore('')
    try {
      const res = await scriviRecensione(voto, commento.trim() || undefined)
      setRecensioneInviata(res.data)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        const dettaglio = err.response.data?.detail
        setErrore(typeof dettaglio === 'string' ? dettaglio : 'Dati non validi. Controlla il voto e riprova.')
      } else {
        setErrore("Errore durante l'invio. Riprova.")
      }
    } finally {
      setInvioInCorso(false)
    }
  }

  return (
    <div className="vista-recensione-wrap">
      <button type="button" className="btn-back-rec" onClick={() => navigate(-1)}>
        ← Torna indietro
      </button>

      {recensioneInviata ? (
        <div className="rec-conferma">
          <span className="rec-conferma-icona">✅</span>
          <h2 className="rec-conferma-titolo">Recensione inviata</h2>
          <p className="rec-conferma-testo">
            Grazie per il tuo feedback, ci aiuta a migliorare il servizio.
          </p>

          <div className="rec-storico">
            <div className="rec-storico-card">
              <div className="rec-storico-stelle">
                {[1, 2, 3, 4, 5].map(n => (
                  <span
                    key={n}
                    className={`rec-stella-statica${n <= recensioneInviata.voto ? ' rec-stella-statica--attiva' : ''}`}
                  >
                    ★
                  </span>
                ))}
              </div>
              {recensioneInviata.commento && (
                <p className="rec-storico-commento">{recensioneInviata.commento}</p>
              )}
              <span className="rec-storico-data">{formatData(recensioneInviata.created_at)}</span>
            </div>
          </div>

          <button
            type="button"
            className="btn-rec-secondario"
            onClick={() => navigate('/utente/home')}
          >
            Torna alla mappa
          </button>
        </div>
      ) : (
        <>
          <h1 className="rec-titolo">Lascia una recensione</h1>
          <p className="rec-sottotitolo">Aiutaci a migliorare il servizio.</p>

          <form onSubmit={confermaScrivi}>
            <span className="rec-label">Voto</span>
            <div className="rec-stelle">
              {[1, 2, 3, 4, 5].map(n => (
                <button
                  key={n}
                  type="button"
                  className={`rec-stella${n <= voto ? ' rec-stella--attiva' : ''}`}
                  onClick={() => setVoto(n)}
                  aria-label={`${n} stelle`}
                >
                  ★
                </button>
              ))}
            </div>

            <label className="rec-label" htmlFor="commento">Commento (facoltativo)</label>
            <textarea
              id="commento"
              className="rec-textarea"
              placeholder="Racconta la tua esperienza..."
              rows={5}
              maxLength={500}
              value={commento}
              onChange={e => setCommento(e.target.value)}
            />
            <span className="rec-contatore">{commento.length}/500</span>

            {errore && <p className="rec-errore">{errore}</p>}

            <button type="submit" className="btn-rec-primario" disabled={invioInCorso}>
              {invioInCorso ? 'Invio in corso...' : 'INVIA RECENSIONE'}
            </button>
          </form>
        </>
      )}
    </div>
  )
}
