import { api } from './ApiService'

export interface ParametriSistema {
  durata_max_prenotazione_min: number
  durata_periodo_grazia_min: number
  max_mezzi_per_utente: number
  addebito_pausa_min: number
}

export const getParametriSistema = async (): Promise<ParametriSistema> => {
  const r = await api.get<ParametriSistema>('/operatore/configurazione/parametri')
  return r.data
}

export const aggiornaParametriSistema = async (payload: ParametriSistema): Promise<ParametriSistema> => {
  const r = await api.put<ParametriSistema>('/operatore/configurazione/parametri', payload)
  return r.data
}

export const getParametriUtente = async (): Promise<ParametriSistema> => {
  const r = await api.get<ParametriSistema>('/utente/parametri')
  return r.data
}
