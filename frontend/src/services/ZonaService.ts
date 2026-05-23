import { api } from './ApiService'
import type { ZonaMappa } from './MapService'

export interface ZonaCreate {
  nome: string
  tipo: string
  coordinate: number[][]
  limite_velocita: number | null
}

export const creaZona = async (dati: ZonaCreate): Promise<ZonaMappa> => {
  const r = await api.post<ZonaMappa>('/operatore/zone', dati)
  return r.data
}

export const eliminaZona = async (id: string): Promise<void> => {
  await api.delete(`/operatore/zone/${id}`)
}
