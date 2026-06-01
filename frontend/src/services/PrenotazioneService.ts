import axios from 'axios'
import { api } from './ApiService'
import type { MezzoMappa } from './MapService'

export interface Prenotazione {
  id: string
  utente_id: string
  mezzo_id: string
  stato: 'attiva'
  scade_at: string
  created_at: string
}

// [IF-UT.02] CS-04.01 — risposta parziale quando alcuni mezzi non sono disponibili
export interface ErroreParziale {
  messaggio: string
  non_disponibili: string[]
}

export function isErroreParziale(err: unknown): err is { response: { data: { detail: ErroreParziale } } } {
  return (
    axios.isAxiosError(err) &&
    err.response?.status === 409 &&
    typeof err.response?.data?.detail === 'object' &&
    Array.isArray(err.response?.data?.detail?.non_disponibili)
  )
}

// [IF-UT.02] CS-04 — Prenotazione arricchita con info mezzo (per recupero dopo refresh)
export interface PrenotazioneAttiva extends Prenotazione {
  codice: string
  tipo: string
  batteria: number | null
}

export const getPrenotazioniAttive = async (): Promise<PrenotazioneAttiva[]> => {
  const r = await api.get<PrenotazioneAttiva[]>('/utente/prenotazioni/attive')
  return r.data
}

// [IF-UT.02] CS-04 — Caratteristiche mezzo (msg2-3 del diagramma di sequenza)
export const getMezzoCaratteristiche = async (mezzoId: string): Promise<MezzoMappa> => {
  const r = await api.get<MezzoMappa>(`/utente/mezzi/${mezzoId}`)
  return r.data
}

// [IF-UT.02] CS-04 — Prenota uno o più mezzi
export const prenotaMezzi = async (mezzoIds: string[]): Promise<Prenotazione[]> => {
  const r = await api.post<{ prenotazioni: Prenotazione[] }>(
    '/utente/prenotazioni',
    { mezzo_ids: mezzoIds }
  )
  return r.data.prenotazioni
}

// [IF-UT.02] CS-XX — Annulla prenotazione
export const annullaPrenotazione = async (prenotazioneId: string): Promise<void> => {
  await api.delete(`/utente/prenotazioni/${prenotazioneId}`)
}