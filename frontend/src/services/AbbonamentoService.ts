import { api } from './ApiService'

export interface PianoAbbonamento {
  id: string
  nome: string
  descrizione: string | null
  prezzo: number
  durata_giorni: number
  stato: string
}

export interface AbbonamentoAttivo {
  id: string
  utente_id: string
  offerta_id: string
  data_inizio: string
  data_fine: string
  stato: string
}

export const getPianiAbbonamento = async (): Promise<PianoAbbonamento[]> => {
  const r = await api.get<PianoAbbonamento[]>('/utente/abbonamenti/piani')
  return r.data
}

export const getAbbonamentoCorrente = async (): Promise<AbbonamentoAttivo | null> => {
  const r = await api.get<AbbonamentoAttivo | null>('/utente/abbonamenti/corrente')
  return r.data
}

export const sottoscriviAbbonamento = async (offertaId: string): Promise<AbbonamentoAttivo> => {
  const r = await api.post<AbbonamentoAttivo>(`/utente/abbonamenti/${offertaId}`)
  return r.data
}
