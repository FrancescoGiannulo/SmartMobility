import { api } from './ApiService'

export interface ZonaParcheggio {
  id: string
  nome: string
}

export interface ConfigurazioneFinecorsa {
  durata_max_prenotazione_min: number
  durata_periodo_grazia_min: number
  max_mezzi_per_utente: number
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  batteria_minima: number | null
  penale_fuori_zona: number
  zone_parcheggio: ZonaParcheggio[]
}

// [IF-OP.12] Aggiunge Mezzo
export const aggiungiMezzo = (mezzo: object) => api.post('/flotta/mezzi', mezzo)

// [IF-OP.13] Dismette Mezzo
export const dismetti = (id: string) => api.delete(`/flotta/mezzi/${id}`)

// [IF-OP.04] Modifica Stato Mezzo
export const modificaStato = (id: string, stato: string) =>
  api.put(`/flotta/mezzi/${id}/stato`, { stato })

// [IF-OP.13] CS-XX — Configurazione regole fine corsa
export const getConfigurazioneFinecorsa = async (): Promise<ConfigurazioneFinecorsa> => {
  const r = await api.get<ConfigurazioneFinecorsa>('/operatore/configurazione/fine-corsa')
  return r.data
}

export const salvaConfigurazioneFinecorsa = async (
  config: Omit<ConfigurazioneFinecorsa, 'zone_parcheggio'>
): Promise<void> => {
  await api.post('/operatore/configurazione/fine-corsa', config)
}
