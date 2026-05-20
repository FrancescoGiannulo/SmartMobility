import { api } from './ApiService'

// [IF-UT.01] Visualizza Mappa Utente
export const getMezziDisponibili = () => api.get('/mappa/mezzi')

// [IF-AP.08] Visualizza Mappa AP / [IF-OP.01] Visualizza Mappa Operatore
export const getMezziFlotta = () => api.get('/mappa/flotta')

export const getZone = () => api.get('/mappa/zone')
