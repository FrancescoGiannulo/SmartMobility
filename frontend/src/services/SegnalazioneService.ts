import { api } from './ApiService'

export interface Segnalazione {
  id: string
  utente_id?: string
  tipologia: string
  descrizione: string
  stato: 'aperta' | 'in_carico'
  created_at: string
  nome_utente?: string
}

const TIPOLOGIE = [
  'Mezzo danneggiato',
  'Mezzo non funzionante',
  'Parcheggio non conforme',
  'Comportamento scorretto',
  'Altro',
] as const

export { TIPOLOGIE }

// [IF-UT.12] Invia Segnalazione
export const salvaSegnalazione = (
  tipologia: string,
  descrizione: string,
): Promise<{ data: Segnalazione }> =>
  api.post('/utente/segnalazioni', { tipologia, descrizione })

export const getMieSegnalazioni = (): Promise<{ data: Segnalazione[] }> =>
  api.get('/utente/segnalazioni')

// [IF-OP.08] Gestisce Segnalazione
export const getSegnalazioni = (): Promise<{ data: Segnalazione[] }> =>
  api.get('/operatore/segnalazioni')

export const getDettaglioSegnalazione = (id: string): Promise<{ data: Segnalazione }> =>
  api.get(`/operatore/segnalazioni/${id}`)

export const aggiornaStatoSegnalazione = (id: string): Promise<{ data: Segnalazione }> =>
  api.patch(`/operatore/segnalazioni/${id}/prendi-in-carico`, {})
