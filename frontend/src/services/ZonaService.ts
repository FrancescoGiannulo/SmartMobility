import { api } from './ApiService'

// [IF-AP.02] Definisce Zone Vietate / [IF-AP.03] Zone Parcheggio / [IF-OP.03] Zone Operative
export const creaZona = (zona: object) => api.post('/zone', zona)

export const getZone = () => api.get('/zone')

export const modificaZona = (id: string, dati: object) => api.put(`/zone/${id}`, dati)
