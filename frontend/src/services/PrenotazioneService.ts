import axios from 'axios'
import { api } from './ApiService'
import type { MezzoMappa } from './MapService'

// [IF-UT.02] Prenotazione (classe del diagramma delle classi)
export interface Prenotazione {
  id: string
  utente_id: string
  mezzo_id: string
  stato: 'attiva'
  scade_at: string
  created_at: string
  // Campi opzionali presenti nel recupero prenotazioni attive (join con Mezzo)
  codice?: string
  tipo?: string
  batteria?: number | null
}

// [IF-UT.02] CS-04.01 — risposta parziale quando alcuni mezzi non sono disponibili (risultatiParziali nel diagramma di sequenza)
export interface RisultatiParziali {
  messaggio: string
  non_disponibili: string[]
}

export function isRisultatiParziali(err: unknown): err is { response: { data: { detail: RisultatiParziali } } } {
  return (
    axios.isAxiosError(err) &&
    err.response?.status === 409 &&
    typeof err.response?.data?.detail === 'object' &&
    Array.isArray(err.response?.data?.detail?.non_disponibili)
  )
}

// [IF-UT.02] CS-04 — risposta 422 quando alcuni mezzi del gruppo sono troppo lontani
// dal primo selezionato (fuoriRaggio nel diagramma di sequenza, msg 37/38)
export interface MezziFuoriRaggio {
  messaggio: string
  fuori_raggio: string[]
}

export function isMezziFuoriRaggio(err: unknown): err is { response: { data: { detail: MezziFuoriRaggio } } } {
  return (
    axios.isAxiosError(err) &&
    err.response?.status === 422 &&
    typeof err.response?.data?.detail === 'object' &&
    Array.isArray(err.response?.data?.detail?.fuori_raggio)
  )
}

// [IF-UT.02] CS-04 — Recupera prenotazioni attive dopo refresh (getPrenotazioniAttive nel diagramma)
export const getPrenotazioniAttive = async (): Promise<Prenotazione[]> => {
  const r = await api.get<Prenotazione[]>('/utente/prenotazioni/attive')
  return r.data
}

// [IF-UT.02] CS-04 — Caratteristiche mezzo (getCaratteristiche nel diagramma)
export const getCaratteristiche = async (mezzoId: string): Promise<MezzoMappa> => {
  const r = await api.get<MezzoMappa>(`/utente/mezzi/${mezzoId}`)
  return r.data
}

// [IF-UT.02] CS-04 — Crea la prenotazione di uno o più mezzi (creaPrenotazione nel diagramma)
export const creaPrenotazione = async (mezzoIds: string[]): Promise<Prenotazione[]> => {
  const r = await api.post<{ prenotazioni: Prenotazione[] }>('/utente/prenotazioni', { mezzo_ids: mezzoIds })
  return r.data.prenotazioni
}

// [IF-UT.02] CS-XX — Annulla prenotazione (annullaPrenotazione nel diagramma)
export const annullaPrenotazione = async (prenotazioneId: string): Promise<void> => {
  await api.delete(`/utente/prenotazioni/${prenotazioneId}`)
}
