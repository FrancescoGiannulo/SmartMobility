import { api } from './ApiService'

export interface StoricoModifica {
  id: string
  tipo_configurazione: string
  descrizione: string
  valore_precedente: string | null
  valore_nuovo: string | null
  operatore_id: string
  created_at: string
  operatore_nome: string | null
}

export const getStoricoModifiche = async (): Promise<StoricoModifica[]> => {
  const r = await api.get<StoricoModifica[]>('/operatore/storico-modifiche')
  return r.data
}
