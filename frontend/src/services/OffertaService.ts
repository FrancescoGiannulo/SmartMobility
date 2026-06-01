import { api } from './ApiService'

export interface Offerta {
  id: string
  nome: string
  tipo: 'promozione' | 'abbonamento'
  stato: 'bozza' | 'attiva' | 'scaduta'
  descrizione: string | null
  sconto_percentuale: number | null
  prezzo: number | null
  durata_giorni: number | null
  data_inizio: string | null
  data_scadenza: string | null
  created_at: string
}

export interface CreaOffertaPayload {
  nome: string
  tipo: 'promozione' | 'abbonamento'
  descrizione?: string
  sconto_percentuale?: number
  prezzo?: number
  durata_giorni?: number
  data_inizio?: string
  data_scadenza?: string
}

export const getOfferte = async (): Promise<Offerta[]> => {
  const r = await api.get<Offerta[]>('/operatore/offerte')
  return r.data
}

export const creaOfferta = async (payload: CreaOffertaPayload): Promise<Offerta> => {
  const r = await api.post<Offerta>('/operatore/offerte', payload)
  return r.data
}

export const eliminaOfferta = async (id: string): Promise<void> => {
  await api.delete(`/operatore/offerte/${id}`)
}
