import { api } from './ApiService'

export interface MetodoPagamento {
  id: string
  tipo: 'google_pay' | 'apple_pay' | 'paypal' | 'carta'
  last_four: string | null
  predefinito: boolean
}

// [IF-UT.05]
export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: string
  costo_al_km: string
}

// [IF-UT.13]
export interface Promozione {
  id: string
  titolo: string
  descrizione: string | null
  sconto_percentuale: string
  data_fine: string
}

export interface RispostaPagamento {
  id: string
  importo: number
  stato: 'completato' | 'rifiutato' | 'in_attesa'
  transazione_id: string
}

// [IF-UT.12] Lista metodi di pagamento salvati
export const getMetodiPagamento = async (): Promise<MetodoPagamento[]> => {
  const r = await api.get<MetodoPagamento[]>('/utente/pagamenti/metodi')
  return r.data
}

// [IF-UT.12] Aggiungi metodo di pagamento
export const aggiungiMetodo = async (
  tipo: string,
  last_four?: string,
): Promise<MetodoPagamento> => {
  const body: { tipo: string; last_four?: string } = { tipo }
  if (last_four) body.last_four = last_four
  const r = await api.post<MetodoPagamento>('/utente/pagamenti/metodi', body)
  return r.data
}

// [IF-UT.21] Imposta metodo di pagamento predefinito
export const impostaPredefinito = async (id: string): Promise<void> => {
  await api.put(`/utente/pagamenti/metodi/${id}/predefinito`)
}

// [IF-UT.12] Rimuovi metodo di pagamento
export const rimuoviMetodo = async (id: string): Promise<void> => {
  await api.delete(`/utente/pagamenti/metodi/${id}`)
}

// [IF-UT.20] Effettua pagamento a fine corsa
export const effettuaPagamento = async (
  corsa_id: string,
  tipo_mezzo: string,
  durata_min: number,
  distanza_km: number,
): Promise<RispostaPagamento> => {
  const r = await api.post<RispostaPagamento>('/utente/pagamenti/', {
    corsa_id,
    tipo_mezzo,
    durata_min,
    distanza_km,
  })
  return r.data
}

// [IF-UT.05] Consulta Tariffe
export const getTariffe = () => api.get<Tariffa[]>('/tariffe')

// [IF-UT.13] Visualizza Promozioni — 204 No Content se nessuna promozione attiva
export const getPromozioni = () => api.get<Promozione[]>('/promozioni')
