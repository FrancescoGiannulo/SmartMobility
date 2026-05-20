import { api } from './ApiService'

// [IF-OP.12] Aggiunge Mezzo
export const aggiungiMezzo = (mezzo: object) => api.post('/flotta/mezzi', mezzo)

// [IF-OP.13] Dismette Mezzo
export const dismetti = (id: string) => api.delete(`/flotta/mezzi/${id}`)

// [IF-OP.04] Modifica Stato Mezzo
export const modificaStato = (id: string, stato: string) =>
  api.put(`/flotta/mezzi/${id}/stato`, { stato })
