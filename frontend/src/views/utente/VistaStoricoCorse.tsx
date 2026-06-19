import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStoricoCorsa, type Corsa } from '../../services/CorsaService'
import './VistaCorse.css'

const GLYPH: Record<string, string> = {
  monopattino: '🛴', bicicletta: '🚲', automobile: '🚗',
}

function formatDataOra(iso: string): string {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function formatOra(iso: string): string {
  return new Date(iso).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' })
}

function formatDurata(min: number | null): string {
  if (min == null) return '—'
  const totalSec = Math.round(min * 60)
  if (totalSec < 60) return `${totalSec} sec`
  const m = Math.floor(totalSec / 60)
  return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m} min`
}

function renderSaldo(c: Corsa): React.ReactNode {
  if (c.costo_totale === 0) return <span className="corse-tag-abbonamento">Abbonamento</span>
  if (c.nome_offerta_applicata && c.importo_pieno != null)
    return (
      <span className="corse-saldo-promo">
        <s className="corse-saldo-pieno">€{c.importo_pieno.toFixed(2)}</s>
        {' '}€{c.costo_totale?.toFixed(2)}
        <span className="corse-tag-promo">{c.nome_offerta_applicata}</span>
      </span>
    )
  if (c.costo_totale != null) return <span>€{c.costo_totale.toFixed(2)}</span>
  return null
}

type VoceStorico =
  | { tipo: 'singola'; corsa: Corsa }
  | { tipo: 'gruppo'; gruppo_id: string; corse: Corsa[] }

function raggruppa(corse: Corsa[]): VoceStorico[] {
  const voci: VoceStorico[] = []
  const gruppiVisti = new Map<string, Corsa[]>()
  for (const c of corse) {
    if (!c.gruppo_corsa_id) {
      voci.push({ tipo: 'singola', corsa: c })
    } else {
      if (!gruppiVisti.has(c.gruppo_corsa_id)) {
        const gruppo: Corsa[] = []
        gruppiVisti.set(c.gruppo_corsa_id, gruppo)
        voci.push({ tipo: 'gruppo', gruppo_id: c.gruppo_corsa_id, corse: gruppo })
      }
      gruppiVisti.get(c.gruppo_corsa_id)!.push(c)
    }
  }
  return voci
}

// [IF-UT.14] CS-11 — Visualizza Storico Corse
export default function VistaCorse() {
  const navigate = useNavigate()
  const [voci, setVoci] = useState<VoceStorico[]>([])
  const [stato, setStato] = useState<'loading' | 'ok' | 'errore'>('loading')
  const [popupGruppo, setPopupGruppo] = useState<Corsa[] | null>(null)

  const carica = () => {
    setStato('loading')
    getStoricoCorsa()
      .then(corse => {
        setVoci(raggruppa(corse))
        setStato('ok')
      })
      .catch(() => setStato('errore'))
  }

  useEffect(() => { carica() }, [])

  return (
    <div className="vista-corse-wrap">
      <header className="corse-header">
        <button type="button" className="btn-back-corse" onClick={() => navigate(-1)}>
          ← Indietro
        </button>
        <h1 className="corse-titolo-header">Cronologia Corse</h1>
      </header>

      <div className="corse-body">
        {stato === 'loading' && (
          <p className="corse-loading">Caricamento...</p>
        )}

        {/* [CS-11.1] DatiNonDisponibili */}
        {stato === 'errore' && (
          <div className="corse-errore-banner">
            <p className="corse-errore-testo">
              Storico delle corse non disponibile al momento. Riprova più tardi.
            </p>
            <button type="button" className="btn-riprova" onClick={carica}>
              Riprova
            </button>
          </div>
        )}

        {stato === 'ok' && voci.length === 0 && (
          <p className="corse-vuoto">Nessuna corsa effettuata.</p>
        )}

        {stato === 'ok' && voci.length > 0 && (
          <ul className="corse-lista">
            {voci.map((v) =>
              v.tipo === 'singola' ? (
                <li key={v.corsa.id} className="corse-item">
                  <div className="corse-item-riga">
                    <span className="corse-item-icona">{GLYPH[v.corsa.tipo_mezzo ?? ''] ?? '●'}</span>
                    <div className="corse-item-info">
                      <span className="corse-item-codice">{v.corsa.codice_mezzo}</span>
                      <span className="corse-item-dettagli">
                        {formatDurata(v.corsa.durata_min)}
                        {' · '}{v.corsa.distanza_km != null ? `${v.corsa.distanza_km.toFixed(1)} km` : '— km'}
                        {renderSaldo(v.corsa) && <> · {renderSaldo(v.corsa)}</>}
                      </span>
                      <span className="corse-item-orari">
                        {formatDataOra(v.corsa.inizio_at)}
                        {v.corsa.fine_at && ` → ${formatOra(v.corsa.fine_at)}`}
                      </span>
                    </div>
                  </div>
                </li>
              ) : (
                <li key={v.gruppo_id} className="corse-item">
                  <div className="corse-gruppo-header">
                    <span className="corse-gruppo-icone">
                      {v.corse.map(c => GLYPH[c.tipo_mezzo ?? ''] ?? '●').join('')}
                    </span>
                    <div className="corse-gruppo-info">
                      <span className="corse-gruppo-badge">Gruppo ({v.corse.length} mezzi)</span>
                      <span className="corse-gruppo-data">{formatDataOra(v.corse[0].inizio_at)}</span>
                      {v.corse.some(c => c.costo_totale != null) && (
                        <span className="corse-gruppo-totale">
                          Totale: €{v.corse.reduce((s, c) => s + (c.costo_totale ?? 0), 0).toFixed(2)}
                        </span>
                      )}
                    </div>
                    <button
                      type="button"
                      className="btn-dettagli-gruppo"
                      onClick={() => setPopupGruppo(v.corse)}
                    >
                      Dettagli
                    </button>
                  </div>
                </li>
              )
            )}
          </ul>
        )}
      </div>

      {/* Popup dettaglio gruppo */}
      {popupGruppo && (
        <div className="popup-overlay" onClick={() => setPopupGruppo(null)}>
          <div className="popup-card" onClick={e => e.stopPropagation()}>
            <div className="popup-header">
              <h2 className="popup-titolo">Dettaglio corsa di gruppo</h2>
              <button
                type="button"
                className="btn-chiudi-popup"
                onClick={() => setPopupGruppo(null)}
                aria-label="Chiudi"
              >
                ✕
              </button>
            </div>
            <ul className="popup-lista">
              {popupGruppo.map(c => (
                <li key={c.id} className="popup-item">
                  <span className="popup-item-icona">{GLYPH[c.tipo_mezzo ?? ''] ?? '●'}</span>
                  <div className="popup-item-info">
                    <span className="popup-item-codice">{c.codice_mezzo}</span>
                    <span className="popup-item-dettagli">
                      {formatDurata(c.durata_min)}
                      {' · '}{c.distanza_km != null ? `${c.distanza_km.toFixed(1)} km` : '— km'}
                      {renderSaldo(c) && <> · {renderSaldo(c)}</>}
                    </span>
                    <span className="popup-item-orari">
                      {formatDataOra(c.inizio_at)}
                      {c.fine_at && ` → ${formatOra(c.fine_at)}`}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
