import { api } from './ApiService'

// [IF-OP.12] Aggiunge Mezzo
export const aggiungiMezzo = (mezzo: object) => api.post('/flotta/mezzi', mezzo)

// [IF-OP.13] Dismette Mezzo
export const dismetti = (id: string) => api.delete(`/flotta/mezzi/${id}`)

// [IF-OP.04] Modifica Stato Mezzo
export const modificaStato = (id: string, stato: string) =>
  api.put(`/flotta/mezzi/${id}/stato`, { stato })

// [IF-OP.07] Definisce Tariffa
export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number
  costo_al_km: number
}

export const getTariffe = (): Promise<{ data: Tariffa[] }> =>
  api.get('/operatore/tariffe')

export const creaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.post('/operatore/tariffe', { tipo_mezzo, costo_al_minuto, costo_al_km })

export const aggiornaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.put(`/operatore/tariffe/${tipo_mezzo}`, { tipo_mezzo, costo_al_minuto, costo_al_km })
