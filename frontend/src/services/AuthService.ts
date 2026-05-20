import { api } from './ApiService'

// [IF-UT.17] Registra Account
export const registra = (dati: { email: string; password: string; nome: string }) =>
  api.post('/auth/registra', dati)

// [IF-UT.18] Autentica Account
export const autentica = (credenziali: { email: string; password: string }) =>
  api.post('/auth/login', credenziali)

export const logout = () => {
  localStorage.removeItem('token')
}
