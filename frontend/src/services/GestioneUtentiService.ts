import { api } from './ApiService'

export interface UtenteListItem {
  id: string
  nome: string
  cognome: string
  email: string
  sospeso: boolean
}

// [IF-OP.09] Sospende Account Utente
export const getUtenti = (): Promise<{ data: UtenteListItem[] }> =>
  api.get('/operatore/utenti')

export const getDettaglioUtente = (id: string): Promise<{ data: UtenteListItem }> =>
  api.get(`/operatore/utenti/${id}`)

export const sospendiAccount = (
  id: string,
  motivazione: string,
): Promise<{ data: UtenteListItem }> =>
  api.patch(`/operatore/utenti/${id}/stato`, { motivazione })
