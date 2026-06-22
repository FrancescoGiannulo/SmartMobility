import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStoricoModifiche, type StoricoModifica } from '../../services/StoricoModificheService'
import './VistaStoricoModifiche.css'

const LABEL_TIPO: Record<string, string> = {
  parametri_sistema: 'Parametri di sistema',
  regole_fine_corsa: 'Regole di fine corsa',
  zona_creata: 'Zona creata',
  zona_eliminata: 'Zona eliminata',
}

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

// [IF-OP.12] Mostra Storico Modifiche
export default function VistaStoricoModifiche() {
  const navigate = useNavigate()
  const [storico, setStorico] = useState<StoricoModifica[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')

  const caricaStorico = useCallback(async () => {
    try {
      const modifiche = await getStoricoModifiche()
      setStorico(modifiche)
    } catch {
      setErrore('Impossibile caricare lo storico delle modifiche.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaStorico() }, [caricaStorico])

  return (
    <div className="vista-storico-mod-wrap">
      <button type="button" className="btn-back-storico-mod" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="storico-mod-titolo">Storico Modifiche</h1>

      {errore && <p className="storico-mod-errore">{errore}</p>}

      {caricamento ? (
        <p className="storico-mod-vuoto">Caricamento...</p>
      ) : storico.length === 0 ? (
        <p className="storico-mod-vuoto">Nessuna modifica registrata.</p>
      ) : (
        <div className="storico-mod-lista">
          {storico.map(v => (
            <div key={v.id} className="storico-mod-card">
              <div className="storico-mod-card-header">
                <span className="storico-mod-tipo">{LABEL_TIPO[v.tipo_configurazione] ?? v.tipo_configurazione}</span>
                <span className="storico-mod-data">{formatData(v.created_at)}</span>
              </div>
              <p className="storico-mod-descrizione">{v.descrizione}</p>
              {(v.valore_precedente || v.valore_nuovo) && (
                <div className="storico-mod-valori">
                  {v.valore_precedente && (
                    <span className="storico-mod-valore-precedente">Prima: {v.valore_precedente}</span>
                  )}
                  {v.valore_nuovo && (
                    <span className="storico-mod-valore-nuovo">Dopo: {v.valore_nuovo}</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
