import { api } from './ApiService'

export interface Recensione {
  id: string
  voto: number
  commento: string | null
  created_at: string
}

// [IF-UT.15] Scrive Recensione
export const scriviRecensione = (
  voto: number,
  commento?: string,
): Promise<{ data: Recensione }> =>
  api.post('/utente/recensioni', { voto, commento: commento || null })
