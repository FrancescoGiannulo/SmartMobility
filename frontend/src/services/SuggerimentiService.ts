import { api } from './ApiService'

export interface Suggerimento {
  id: string
  tipo: 'risparmio' | 'percorso' | 'abbonamento' | 'orario' | 'mezzo' | 'generale'
  testo: string
  dati_contesto: Record<string, unknown>
  stato: 'nuovo' | 'visto'
  creato_at: string | null
}

// [IF-UT.14] Visualizza Suggerimenti Intelligenti
export const getSuggerimenti = (): Promise<{ data: Suggerimento[] }> =>
  api.get('/utente/suggerimenti')

export const generaSuggerimenti = (): Promise<{ data: Suggerimento[] }> =>
  api.post('/utente/suggerimenti/genera')

export const segnaVisto = (id: string): Promise<void> =>
  api.patch(`/utente/suggerimenti/${id}/visto`)
