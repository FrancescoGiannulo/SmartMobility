import { api } from './ApiService'

export interface Prenotazione {
  id: string
  utente_id: string
  mezzo_id: string
  stato: 'attiva'
  scade_at: string
  created_at: string
}

// [IF-UT.02] CS-XX — Prenota Mezzo
export const prenotaMezzo = async (mezzoId: string): Promise<Prenotazione> => {
  const r = await api.post<Prenotazione>('/utente/prenotazioni', { mezzo_id: mezzoId })
  return r.data
}

// [IF-UT.02] CS-XX — Annulla prenotazione
export const annullaPrenotazione = async (prenotazioneId: string): Promise<void> => {
  await api.delete(`/utente/prenotazioni/${prenotazioneId}`)
}
