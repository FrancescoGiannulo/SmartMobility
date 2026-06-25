import { useState, useEffect, useCallback } from 'react'
import { getRecensioni, type Recensione } from '../../services/RecensioneService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
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
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vrec__body">
          <h1 className="vrec__titolo">Recensioni</h1>

          {errore && <p className="vrec__errore">{errore}</p>}

          {caricamento ? (
            <p className="vrec__vuoto">Caricamento...</p>
          ) : recensioni.length === 0 ? (
            // [IF-OP.12.01] NessunaRecensione
            <p className="vrec__vuoto">Nessuna recensione presente.</p>
          ) : (
            <>
              <div className="vrec__media">
                <span className="vrec__media-valore">{votoMedio.toFixed(1)}</span>
                <span className="vrec__media-stelle">{stelle(Math.round(votoMedio))}</span>
                <span className="vrec__media-label">
                  Voto medio su {recensioni.length} recension{recensioni.length === 1 ? 'e' : 'i'}
                </span>
              </div>

              <div className="vrec__lista">
                {recensioni.map(r => (
                  <div key={r.id} className="vrec__card">
                    <div className="vrec__card-header">
                      <span className="vrec__stelle">{stelle(r.voto)}</span>
                      <span className="vrec__data">{formatData(r.created_at)}</span>
                    </div>
                    {r.commento && <p className="vrec__commento">{r.commento}</p>}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
