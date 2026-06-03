import { api } from './ApiService'

export interface CorsaAttiva {
  id: string
  mezzo_id: string
  utente_id: string
  prenotazione_id: string | null
  stato: 'in_uso'
  inizio_at: string
}

export interface MezzoSbloccabile {
  id: string
  codice: string
  tipo: 'monopattino' | 'bicicletta' | 'automobile'
  stato: string
  lat: number
  lng: number
  batteria: number | null
  prenotato: boolean
  prenotazione_id: string | null
}

export interface RisultatoSbloccoItem {
  mezzo_id: string
  corsa_id: string
}

export interface RisultatoSblocco {
  sbloccati: RisultatoSbloccoItem[]
  falliti: string[]
}

// [IF-UT.04] CS-05 — lista mezzi sbloccabili (prenotati + disponibili vicini)
export const getMezziSbloccabili = async (
  lat?: number,
  lng?: number,
): Promise<MezzoSbloccabile[]> => {
  const params = lat != null && lng != null ? `?lat=${lat}&lng=${lng}` : ''
  const r = await api.get<MezzoSbloccabile[]>(`/utente/mezzi/sbloccabili${params}`)
  return r.data
}

// [IF-UT.04] CS-05 — sblocca uno o più mezzi in batch
export const sbloccaMezzi = async (
  mezzoIds: string[],
  lat?: number,
  lng?: number,
): Promise<RisultatoSblocco> => {
  const r = await api.post<RisultatoSblocco>('/utente/mezzi/sblocca', {
    mezzo_ids: mezzoIds,
    lat: lat ?? null,
    lng: lng ?? null,
  })
  return r.data
}

// [IF-UT.06] CS-11 Termina Corsa
export const terminaCorsa = async (corsaId: string): Promise<void> => {
  await api.post(`/utente/corse/${corsaId}/termina`)
}