import { api } from './ApiService'

export type TipoCostoTariffa = 'minuto' | 'km'

export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number | null
  costo_al_km: number | null
}

function buildPayload(tipo_mezzo: string, tipoCosto: TipoCostoTariffa, valore: number) {
  return {
    tipo_mezzo,
    costo_al_minuto: tipoCosto === 'minuto' ? valore : null,
    costo_al_km: tipoCosto === 'km' ? valore : null,
  }
}

// [IF-OP.07] Definisce Tariffa
export const getTariffe = (): Promise<{ data: Tariffa[] }> =>
  api.get('/operatore/tariffe')

export const creaTariffa = (
  tipo_mezzo: string,
  tipoCosto: TipoCostoTariffa,
  valore: number,
): Promise<{ data: Tariffa }> =>
  api.post('/operatore/tariffe', buildPayload(tipo_mezzo, tipoCosto, valore))

// [IF-OP.08] Modifica Tariffa
export const aggiornaTariffa = (
  tipo_mezzo: string,
  tipoCosto: TipoCostoTariffa,
  valore: number,
): Promise<{ data: Tariffa }> =>
  api.put(`/operatore/tariffe/${tipo_mezzo}`, buildPayload(tipo_mezzo, tipoCosto, valore))
