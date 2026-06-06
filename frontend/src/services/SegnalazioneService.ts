import { api } from './ApiService'

export interface Segnalazione {
  id: string
  utente_id?: string
  tipologia: string
  descrizione: string
  stato: 'aperta' | 'in_carico'
  created_at: string
}

const TIPOLOGIE = [
  'Mezzo danneggiato',
  'Mezzo non funzionante',
  'Parcheggio non conforme',
  'Comportamento scorretto',
  'Altro',
] as const

export { TIPOLOGIE }

// [IF-UT.15] Invia Segnalazione
export const inviaSegnalazione = (
  tipologia: string,
  descrizione: string,
): Promise<{ data: Segnalazione }> =>
  api.post('/utente/segnalazioni', { tipologia, descrizione })

// [IF-OP.08] Gestisce Segnalazione
export const getSegnalazioni = (): Promise<{ data: Segnalazione[] }> =>
  api.get('/operatore/segnalazioni')

export const getDettaglioSegnalazione = (id: string): Promise<{ data: Segnalazione }> =>
  api.get(`/operatore/segnalazioni/${id}`)

export const prendiInCarico = (id: string): Promise<{ data: Segnalazione }> =>
  api.patch(`/operatore/segnalazioni/${id}/stato`, {})
