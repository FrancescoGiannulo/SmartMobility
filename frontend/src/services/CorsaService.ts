import { api } from './ApiService'

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
  gruppo_corsa_id: string | null
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

// [IF-UT.10] SD SospendeCorsa — msg2: sospendiCorsa(idCorsa)
export interface RispostaSospensione {
  stato: string
  tempo_gratuito_residuo_sec: number
  addebito_pausa_min: number
  periodo_grazia_scaduto: boolean
}

export const sospendiCorsa = async (corsaId: string): Promise<RispostaSospensione> => {
  const r = await api.put<RispostaSospensione>(`/utente/corse/${corsaId}/pausa`)
  return r.data
}

// [IF-UT.05] Riprende la corsa dalla pausa
export const riprendiCorsa = async (corsaId: string): Promise<void> => {
  await api.post(`/utente/corse/${corsaId}/riprendi`)
}

// [IF-UT.07/IF-UT.14] Corsa (classe del diagramma delle classi)
export interface Corsa {
  id: string
  inizio_at: string
  fine_at: string | null
  costo_totale: number | null    // costoTotale nel diagramma
  stato: string | null
  distanza_km: number | null     // distanzaPercorsa nel diagramma
  gruppo_corsa_id: string | null // gruppoCorsaID nel diagramma
  importo_pieno: number | null   // da pagamenti, per badge abbonamento/promo
  // Campi aggiuntivi per lo storico (join con Mezzo)
  tipo_mezzo: string | null
  codice_mezzo: string | null
  durata_min: number | null
  nome_offerta_applicata: string | null
}

export const getStoricoCorsa = async (): Promise<Corsa[]> => {
  const r = await api.get<Corsa[]>('/utente/corse/storico')
  return r.data
}

// [IF-UT.07] CS-06 — Riepilogo corsa terminata
export const getRiepilogoCorsa = async (corsaId: string): Promise<Corsa> => {
  const r = await api.get<Corsa>(`/utente/corse/${corsaId}/riepilogo`)
  return r.data
}
