import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getPianiAbbonamento,
  getAbbonamentoCorrente,
  sottoscriviAbbonamento,
  type PianoAbbonamento,
  type AbbonamentoAttivo,
} from '../../services/AbbonamentoService'
import './VistaAbbonamenti.css'

export default function VistaAbbonamenti() {
  const navigate = useNavigate()
  const [piani, setPiani] = useState<PianoAbbonamento[]>([])
  const [corrente, setCorrente] = useState<AbbonamentoAttivo | null>(null)
  const [pianoSelezionato, setPianoSelezionato] = useState<PianoAbbonamento | null>(null)
  const [conferma, setConferma] = useState('')
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)

  useEffect(() => {
    getPianiAbbonamento().then(setPiani).catch(() => {})
    getAbbonamentoCorrente().then(setCorrente).catch(() => {})
  }, [])

  const handleSottoscrivi = async () => {
    if (!pianoSelezionato) return
    setErrore('')
    setConferma('')
    setCaricamento(true)
    try {
      const abb = await sottoscriviAbbonamento(pianoSelezionato.id)
      setCorrente(abb)
      setPianoSelezionato(null)
      setConferma(`Abbonamento "${pianoSelezionato.nome}" attivato con successo!`)
    } catch (err) {
      // Aggiorna corrente anche in caso di errore: l'abbonamento potrebbe essere stato creato
      // ma la risposta persa (es. errore di rete post-commit)
      getAbbonamentoCorrente().then(setCorrente).catch(() => {})
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail
        setErrore(typeof detail === 'string' ? detail : 'Impossibile completare la sottoscrizione.')
      } else {
        setErrore('Errore di rete. Riprova.')
      }
    } finally {
      setCaricamento(false)
    }
  }

  const formatData = (iso: string) =>
    new Date(iso).toLocaleDateString('it-IT', { day: '2-digit', month: 'long', year: 'numeric' })

  return (
    <div className="vista-abb">
      <div className="abb-topbar">
        <h2>Abbonamenti</h2>
        <button className="btn-indietro-abb" onClick={() => navigate('/utente/home')}>
          ← Torna alla mappa
        </button>
      </div>

      <div className="abb-body">

        {corrente && (
          <div className="abb-corrente">
            <div className="abb-corrente-label">Abbonamento attivo</div>
            <div className="abb-corrente-info">
              Valido fino al <strong>{formatData(corrente.data_fine)}</strong>
            </div>
          </div>
        )}

        {corrente && new Date(corrente.data_fine) > new Date() ? (
          <div className="abb-vuoti">
            Hai già un abbonamento attivo. Potrai sottoscriverne uno nuovo alla scadenza.
          </div>
        ) : (
          <>
            <h3 className="abb-sezione-titolo">Piani disponibili</h3>

            {piani.length === 0 ? (
              <div className="abb-vuoti">Nessun piano abbonamento disponibile al momento.</div>
            ) : (
              <div className="abb-piani">
                {piani.map(piano => (
                  <div
                    key={piano.id}
                    className={`abb-piano-card ${pianoSelezionato?.id === piano.id ? 'selezionato' : ''}`}
                    onClick={() => { setPianoSelezionato(piano); setErrore(''); setConferma('') }}
                  >
                    <div className="abb-piano-nome">{piano.nome}</div>
                    {piano.descrizione && <div className="abb-piano-desc">{piano.descrizione}</div>}
                    <div className="abb-piano-dettagli">
                      <span className="abb-piano-prezzo">€{Number(piano.prezzo).toFixed(2)}</span>
                      <span className="abb-piano-durata">{piano.durata_giorni} giorni</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {pianoSelezionato && (
          <div className="abb-riepilogo">
            <h4>Riepilogo sottoscrizione</h4>
            <p><strong>Piano:</strong> {pianoSelezionato.nome}</p>
            <p><strong>Durata:</strong> {pianoSelezionato.durata_giorni} giorni</p>
            <p><strong>Importo:</strong> €{Number(pianoSelezionato.prezzo).toFixed(2)}</p>
            <p className="abb-riepilogo-nota">Il pagamento verrà addebitato sul tuo metodo predefinito.</p>
            <div className="abb-riepilogo-azioni">
              <button className="btn-annulla-abb" onClick={() => setPianoSelezionato(null)}>Annulla</button>
              <button className="btn-conferma-abb" onClick={handleSottoscrivi} disabled={caricamento}>
                {caricamento ? '...' : 'Conferma e paga'}
              </button>
            </div>
          </div>
        )}

        {errore && <p className="abb-errore">{errore}</p>}
        {conferma && <p className="abb-conferma">{conferma}</p>}
      </div>
    </div>
  )
}
