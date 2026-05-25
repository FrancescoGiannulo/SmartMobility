import { api } from './ApiService'

export interface CorsaAttiva {
  id: string
  mezzo_id: string
  utente_id: string
  prenotazione_id: string | null
  stato: 'in_uso'
  inizio_at: string
}

// [IF-UT.04] CS-10 Sblocca Mezzo
export const sbloccaMezzo = async (mezzoId: string): Promise<CorsaAttiva> => {
  const r = await api.post<CorsaAttiva>(`/utente/mezzi/${mezzoId}/sblocca`)
  return r.data
}
