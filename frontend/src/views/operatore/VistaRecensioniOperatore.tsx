import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getRecensioni, type Recensione } from '../../services/RecensioneService'
import './VistaRecensioniOperatore.css'

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function stelle(voto: number) {
  return '★'.repeat(voto) + '☆'.repeat(5 - voto)
}

// [IF-OP.12] Visualizza Recensioni
export default function VistaRecensioniOperatore() {
  const navigate = useNavigate()

  const [recensioni, setRecensioni] = useState<Recensione[]>([])
  const [votoMedio, setVotoMedio] = useState(0)
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')

  // [IF-OP.12] apriRecensioni()
  const apriRecensioni = useCallback(async () => {
    try {
      const res = await getRecensioni()
      setRecensioni(res.data.recensioni)
      setVotoMedio(res.data.voto_medio)
    } catch {
      setErrore('Impossibile caricare le recensioni.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { apriRecensioni() }, [apriRecensioni])

  // [IF-OP.12] mostraRecensioni(recensioni, votoMedio)
  return (
    <div className="vista-rec-op-wrap">
      <button type="button" className="btn-back-rec-op" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="rec-op-titolo">Recensioni</h1>

      {errore && <p className="rec-op-errore">{errore}</p>}

      {caricamento ? (
        <p className="rec-op-vuoto">Caricamento...</p>
      ) : recensioni.length === 0 ? (
        // [IF-OP.12.01] NessunaRecensione
        <p className="rec-op-vuoto">Nessuna recensione presente.</p>
      ) : (
        <>
          <div className="rec-op-media">
            <span className="rec-op-media-valore">{votoMedio.toFixed(1)}</span>
            <span className="rec-op-media-stelle">{stelle(Math.round(votoMedio))}</span>
            <span className="rec-op-media-label">
              Voto medio su {recensioni.length} recension{recensioni.length === 1 ? 'e' : 'i'}
            </span>
          </div>

          <div className="rec-op-lista">
            {recensioni.map(r => (
              <div key={r.id} className="rec-op-card">
                <div className="rec-op-card-header">
                  <span className="rec-op-stelle">{stelle(r.voto)}</span>
                  <span className="rec-op-data">{formatData(r.created_at)}</span>
                </div>
                {r.commento && <p className="rec-op-commento">{r.commento}</p>}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
