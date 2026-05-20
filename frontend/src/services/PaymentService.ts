import { api } from './ApiService'

// [IF-UT.12] Salva Metodi Pagamento
export const salvaMetodoPagamento = (metodo: object) => api.post('/pagamenti/metodi', metodo)

// [IF-UT.21] Imposta Metodo Predefinito
export const impostaPredefinito = (id: string) => api.put(`/pagamenti/metodi/${id}/predefinito`)

export const getMetodiPagamento = () => api.get('/pagamenti/metodi')
