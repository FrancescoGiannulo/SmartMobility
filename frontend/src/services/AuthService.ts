import { supabase } from '../supabaseClient'
import { api } from './ApiService'

export interface Profilo {
  id: string
  nome: string
  cognome?: string
  email: string
  sospeso?: boolean
}

export interface AuthResult {
  access_token: string
  ruolo: 'UT' | 'OP' | 'AP'
  profilo: Profilo
}

const salvaSessione = (result: AuthResult): void => {
  localStorage.setItem('token', result.access_token)
  localStorage.setItem('ruolo', result.ruolo)
  localStorage.setItem('profilo', JSON.stringify(result.profilo))
}

// [IF-UT.17] Registra Account
export const registra = async (dati: {
  email: string
  password: string
  nome: string
  cognome: string
}): Promise<AuthResult> => {
  const resp = await api.post<AuthResult>('/auth/registra', dati)
  salvaSessione(resp.data)
  return resp.data
}

// [IF-UT.18 / IF-OP.16 / IF-AP.07] Autentica Account
export const autentica = async (credenziali: {
  email: string
  password: string
}): Promise<AuthResult> => {
  const resp = await api.post<AuthResult>('/auth/login', credenziali)
  salvaSessione(resp.data)
  return resp.data
}

// Google OAuth — solo UT
export const autenticaGoogle = async (): Promise<void> => {
  await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo: `${window.location.origin}/auth/callback` },
  })
}

// Callback OAuth: salva token e recupera profilo dal backend
export const gestisciCallbackOAuth = async (): Promise<AuthResult | null> => {
  const { data } = await supabase.auth.getSession()
  if (!data.session) return null
  localStorage.setItem('token', data.session.access_token)
  const resp = await api.get<{ ruolo: string; profilo: Profilo }>('/auth/me')
  const result: AuthResult = {
    access_token: data.session.access_token,
    ruolo: resp.data.ruolo as 'UT' | 'OP' | 'AP',
    profilo: resp.data.profilo,
  }
  salvaSessione(result)
  return result
}

export const logout = async (): Promise<void> => {
  localStorage.removeItem('token')
  localStorage.removeItem('ruolo')
  localStorage.removeItem('profilo')
  await supabase.auth.signOut()
}

export const utenteCorrente = (): { ruolo: 'UT' | 'OP' | 'AP'; profilo: Profilo } | null => {
  const token = localStorage.getItem('token')
  const ruolo = localStorage.getItem('ruolo') as 'UT' | 'OP' | 'AP' | null
  const profiloStr = localStorage.getItem('profilo')
  if (!token || !ruolo || !profiloStr) return null
  try {
    return { ruolo, profilo: JSON.parse(profiloStr) }
  } catch {
    return null
  }
}
