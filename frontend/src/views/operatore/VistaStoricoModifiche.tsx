import { useEffect, useState, useCallback } from 'react'
import { getStoricoModifiche, type StoricoModifica } from '../../services/StoricoModificheService'
import SidebarRuolo from '../../components/layout/SidebarRuolo'
import './VistaStoricoModifiche.css'

interface CampoConfig {
  label: string
  formatta?: (v: string) => string
  valori?: Record<string, string>
}

interface CategoriaConfig {
  label: string
  tipi: string[]
  campi: Record<string, CampoConfig>
}

const EURO = (v: string) => `${Number(v).toFixed(2)}€`
const PERCENTO = (v: string) => `${v}%`
const MINUTI = (v: string) => `${v} min`
const DATA = (v: string) => {
  const d = new Date(v)
  return Number.isNaN(d.getTime()) ? v : formatData(v)
}

const CATEGORIE: CategoriaConfig[] = [
  {
    label: 'Parametri di sistema',
    tipi: ['parametri_sistema'],
    campi: {
      durata_max_prenotazione_min: { label: 'Durata massima prenotazione', formatta: MINUTI },
      durata_periodo_grazia_min: { label: 'Durata periodo di grazia', formatta: MINUTI },
      max_mezzi_per_utente: { label: 'Numero massimo mezzi per utente' },
      addebito_pausa_min: { label: 'Addebito pausa al minuto', formatta: EURO },
    },
  },
  {
    label: 'Regole di fine corsa',
    tipi: ['regole_fine_corsa_creata', 'regole_fine_corsa_modificata'],
    campi: {
      tipo_vincolo: {
        label: 'Vincolo rilascio fuori zona parcheggio',
        valori: { penale: 'Penale (addebito importo)', divieto: 'Blocco fine corsa', avviso: 'Avviso (nessun addebito)' },
      },
      penale_fuori_zona: { label: 'Importo penale', formatta: EURO },
      batteria_minima: { label: 'Batteria minima richiesta', formatta: PERCENTO },
      bonus_parcheggi_corretti: { label: 'Numero parcheggi corretti necessari' },
      bonus_valore: { label: 'Valore bonus', formatta: EURO },
    },
  },
  {
    label: 'Zone',
    tipi: ['zona_creata', 'zona_eliminata'],
    campi: {
      nome: { label: 'Nome zona' },
      tipo: {
        label: 'Tipo zona',
        valori: { operativa: 'Operativa', parcheggio: 'Parcheggio', limitata: 'Limitata', vietata: 'Vietata' },
      },
      limite_velocita: { label: 'Limite di velocità' },
    },
  },
  {
    label: 'Tariffe',
    tipi: ['tariffa_creata', 'tariffa_modificata'],
    campi: {
      tipo_mezzo: { label: 'Tipo mezzo' },
      costo_al_minuto: { label: 'Costo al minuto', formatta: EURO },
      costo_al_km: { label: 'Costo al km', formatta: EURO },
    },
  },
  {
    label: 'Offerte',
    tipi: ['offerta_creata', 'offerta_modificata', 'offerta_eliminata'],
    campi: {
      nome: { label: 'Nome offerta' },
      tipo: { label: 'Tipo', valori: { promozione: 'Promozione', abbonamento: 'Abbonamento' } },
      stato: { label: 'Stato', valori: { attiva: 'Attiva', bozza: 'Bozza', scaduta: 'Scaduta' } },
      descrizione: { label: 'Descrizione' },
      sconto_percentuale: { label: 'Sconto', formatta: PERCENTO },
      prezzo: { label: 'Prezzo', formatta: EURO },
      durata_giorni: { label: 'Durata', formatta: v => `${v} giorni` },
      data_inizio: { label: 'Data inizio', formatta: DATA },
      data_scadenza: { label: 'Data scadenza', formatta: DATA },
      tipo_mezzo: {
        label: 'Valido per',
        valori: { monopattino: 'Monopattino', bicicletta: 'Bicicletta', automobile: 'Automobile' },
      },
    },
  },
]

// "a=1, b=2, c=None" -> { a: "1", b: "2", c: "None" }
// split solo prima di un token "parola=" per non rompersi su virgole nei valori liberi (es. descrizione)
function parseValori(s: string | null): Record<string, string> {
  if (!s) return {}
  const risultato: Record<string, string> = {}
  for (const coppia of s.split(/,\s*(?=[a-zA-Z_][a-zA-Z0-9_]*=)/)) {
    const idx = coppia.indexOf('=')
    if (idx === -1) continue
    risultato[coppia.slice(0, idx).trim()] = coppia.slice(idx + 1).trim()
  }
  return risultato
}

interface RigaDiff {
  campo: string
  prima?: string
  dopo?: string
}

function calcolaDiff(precedente: string | null, nuovo: string | null): RigaDiff[] {
  const prec = parseValori(precedente)
  const dopo = parseValori(nuovo)
  const righe: RigaDiff[] = []
  if (precedente && nuovo) {
    for (const campo of Object.keys(dopo)) {
      if (prec[campo] !== dopo[campo]) {
        righe.push({ campo, prima: prec[campo], dopo: dopo[campo] })
      }
    }
  } else if (nuovo) {
    for (const campo of Object.keys(dopo)) {
      if (dopo[campo] !== 'None') righe.push({ campo, dopo: dopo[campo] })
    }
  } else if (precedente) {
    for (const campo of Object.keys(prec)) {
      if (prec[campo] !== 'None') righe.push({ campo, prima: prec[campo] })
    }
  }
  return righe
}

function formattaValore(categoria: CategoriaConfig | undefined, campo: string, valore: string): string {
  if (valore === 'None') return '—'
  const config = categoria?.campi[campo]
  if (!config) return valore
  if (config.valori) return config.valori[valore] ?? valore
  if (config.formatta) return config.formatta(valore)
  return valore
}

function etichettaCampo(categoria: CategoriaConfig | undefined, campo: string): string {
  return categoria?.campi[campo]?.label ?? campo
}

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

// [IF-OP.13] Mostra Storico Modifiche
export default function VistaStoricoModifiche() {
  const [storico, setStorico] = useState<StoricoModifica[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [categoriaAperta, setCategoriaAperta] = useState<string | null>(null)

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

  const sezioni = CATEGORIE
    .map(categoria => ({
      categoria,
      voci: storico.filter(v => categoria.tipi.includes(v.tipo_configurazione)),
    }))
    .filter(s => s.voci.length > 0)

  return (
    <div className="sm-op-shell">
      <SidebarRuolo ruolo="OP" />
      <div className="sm-op-main">
        <div className="vstorico__body">
          <h1 className="vstorico__titolo">Storico Modifiche</h1>

          {errore && <p className="vstorico__errore">{errore}</p>}

          {caricamento ? (
            <p className="vstorico__vuoto">Caricamento...</p>
          ) : sezioni.length === 0 ? (
            <p className="vstorico__vuoto">Nessuna modifica registrata.</p>
          ) : (
            <div className="vstorico__sezioni">
              {sezioni.map(({ categoria, voci }) => {
                const aperta = categoriaAperta === categoria.label
                return (
                  <div key={categoria.label} className="vstorico__sezione">
                    <button
                      type="button"
                      className="vstorico__sezione-header"
                      onClick={() => setCategoriaAperta(aperta ? null : categoria.label)}
                    >
                      <span className="vstorico__sezione-titolo">
                        {categoria.label}
                        <span className="vstorico__sezione-badge">{voci.length}</span>
                      </span>
                      <span className={`vstorico__chevron${aperta ? ' vstorico__chevron--aperta' : ''}`}>▾</span>
                    </button>
                    {aperta && (
                      <div className="vstorico__lista">
                        {voci.map(v => (
                          <div key={v.id} className="vstorico__card">
                            <div className="vstorico__card-header">
                              <span className="vstorico__data">{formatData(v.created_at)}</span>
                              <span className="vstorico__operatore">
                                Modificato da: {v.operatore_nome ?? 'Operatore non disponibile'}
                              </span>
                            </div>
                            <p className="vstorico__descrizione">{v.descrizione}</p>
                            <div className="vstorico__valori">
                              {calcolaDiff(v.valore_precedente, v.valore_nuovo).map(riga => (
                                <div key={riga.campo} className="vstorico__riga-diff">
                                  <span className="vstorico__riga-etichetta">{etichettaCampo(categoria, riga.campo)}:</span>
                                  {riga.prima !== undefined && (
                                    <span className="vstorico__valore-precedente">
                                      {formattaValore(categoria, riga.campo, riga.prima)}
                                    </span>
                                  )}
                                  {riga.prima !== undefined && riga.dopo !== undefined && (
                                    <span className="vstorico__freccia">→</span>
                                  )}
                                  {riga.dopo !== undefined && (
                                    <span className="vstorico__valore-nuovo">
                                      {formattaValore(categoria, riga.campo, riga.dopo)}
                                    </span>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
