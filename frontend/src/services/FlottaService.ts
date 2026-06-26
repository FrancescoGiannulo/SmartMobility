import { api } from './ApiService'

export interface MezzoFlotta {
  id: string
  codice: string
  tipo: string
  stato: string
  lat: number | null
  lng: number | null
  batteria: number | null
}

export interface AggiungiMezzoPayload {
  tipo: string
  codice: string
  lat: number
  lng: number
  stato: string
}

export interface ZonaParcheggio {
  id: string
  nome: string
}

export interface ConfigurazioneFinecorsa {
  durata_max_prenotazione_min: number
  durata_periodo_grazia_min: number
  max_mezzi_per_utente: number
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  penale_fuori_zona: number
  zone_parcheggio: ZonaParcheggio[]
}

// [IF-OP.11] Lista flotta operatore
export const getMezziFlotta = (): Promise<{ data: MezzoFlotta[] }> =>
  api.get('/operatore/mezzi')

// [IF-OP.11] Aggiunge nuovo mezzo
export const aggiungiMezzo = (mezzo: AggiungiMezzoPayload): Promise<{ data: MezzoFlotta }> =>
  api.post('/operatore/mezzi', mezzo)

// [IF-OP.12] Verifica se il mezzo può essere dismesso
export const verificaDismissione = (
  id: string
): Promise<{ data: { dismettibile: boolean; motivo: string | null; mezzo: MezzoFlotta } }> =>
  api.post(`/operatore/mezzi/${id}/verifica`, {})

// [IF-OP.12] Dismette il mezzo
export const dismetti = (id: string): Promise<{ data: { status: string } }> =>
  api.delete(`/operatore/mezzi/${id}`)

// [IF-OP.04] Modifica Stato Mezzo (implementato separatamente)
export const modificaStato = (id: string, stato: string) =>
  api.put(`/operatore/mezzi/${id}/stato`, { stato })

// [IF-OP.13] Configurazione regole fine corsa
export const getConfigurazioneFinecorsa = async (): Promise<ConfigurazioneFinecorsa> => {
  const r = await api.get<ConfigurazioneFinecorsa>('/operatore/configurazione/fine-corsa')
  return r.data
}

export const salvaConfigurazioneFinecorsa = async (
  config: Omit<ConfigurazioneFinecorsa, 'zone_parcheggio'>
): Promise<void> => {
  await api.post('/operatore/configurazione/fine-corsa', config)
}
