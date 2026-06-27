import { api } from './ApiService'

export interface RegolaFinecorsa {
  id: string
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  penale_fuori_zona: number
  bonus_parcheggi_corretti: number | null
  bonus_valore: number | null
  created_at: string
}

export interface SalvaRegolaPayload {
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  penale_fuori_zona: number
  bonus_parcheggi_corretti?: number
  bonus_valore?: number
}

export const getRegolaFinecorsa = async (): Promise<RegolaFinecorsa | null> => {
  const r = await api.get<RegolaFinecorsa | null>('/operatore/regole-fine-corsa')
  return r.data
}

export const salvaRegolaFinecorsa = async (payload: SalvaRegolaPayload): Promise<RegolaFinecorsa> => {
  const r = await api.put<RegolaFinecorsa>('/operatore/regole-fine-corsa', payload)
  return r.data
}
