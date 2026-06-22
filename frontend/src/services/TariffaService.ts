import { api } from './ApiService'

export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number
  costo_al_km: number
}

// [IF-OP.07] Definisce Tariffa
export const getTariffe = (): Promise<{ data: Tariffa[] }> =>
  api.get('/operatore/tariffe')

export const creaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.post('/operatore/tariffe', { tipo_mezzo, costo_al_minuto, costo_al_km })

// [IF-OP.08] Modifica Tariffa
export const aggiornaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.put(`/operatore/tariffe/${tipo_mezzo}`, { tipo_mezzo, costo_al_minuto, costo_al_km })
