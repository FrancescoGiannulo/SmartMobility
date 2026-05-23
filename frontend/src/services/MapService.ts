import { api } from './ApiService'

export interface MezzoMappa {
  id: string
  codice: string
  tipo: 'monopattino' | 'bicicletta' | 'automobile'
  stato: string
  lat: number
  lng: number
  batteria: number | null
}

export interface ZonaMappa {
  id: string
  nome: string
  tipo: 'operativa' | 'parcheggio' | 'limitata' | 'vietata'
  perimetro: {
    type: 'Polygon'
    coordinates: number[][][]
  }
  limite_velocita: number | null
  attiva: boolean
}

export const getMezziUtente = async (): Promise<MezzoMappa[]> => {
  const r = await api.get<MezzoMappa[]>('/utente/mappa/mezzi')
  return r.data
}

export const getZoneUtente = async (): Promise<ZonaMappa[]> => {
  const r = await api.get<ZonaMappa[]>('/utente/mappa/zone')
  return r.data
}

export const getMezziOperatore = async (): Promise<MezzoMappa[]> => {
  const r = await api.get<MezzoMappa[]>('/operatore/mappa/mezzi')
  return r.data
}

export const getZoneOperatore = async (): Promise<ZonaMappa[]> => {
  const r = await api.get<ZonaMappa[]>('/operatore/zone')
  return r.data
}
