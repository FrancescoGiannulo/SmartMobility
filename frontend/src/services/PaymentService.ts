import { api } from './ApiService'

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

// [IF-UT.12] Salva Metodi Pagamento
export const salvaMetodoPagamento = (metodo: object) => api.post('/pagamenti/metodi', metodo)

// [IF-UT.21] Imposta Metodo Predefinito
export const impostaPredefinito = (id: string) => api.put(`/pagamenti/metodi/${id}/predefinito`)

export const getMetodiPagamento = () => api.get('/pagamenti/metodi')

// [IF-UT.05] Consulta Tariffe
export const getTariffe = () => api.get<Tariffa[]>('/tariffe')

// [IF-UT.13] Visualizza Promozioni — 204 No Content se nessuna promozione attiva
export const getPromozioni = () => api.get<Promozione[]>('/promozioni')
