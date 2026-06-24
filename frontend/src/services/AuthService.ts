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
  localStorage.setItem('profilo:v1', JSON.stringify(result.profilo))
}

// [IF-UT.17] Registra Account
export const registra = async (dati: {
  email: string
  password: string
  nome: string
  cognome: string
  consenso_privacy: boolean  // [IIN-2 / GDPR art. 7]
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

// [IF-UT.18 — variante OAuth] Callback OAuth: find-or-create sul backend, poi salva sessione
export const gestisciCallbackOAuth = async (accessToken: string, consensoPrivacy: boolean): Promise<AuthResult> => {
  localStorage.setItem('token', accessToken)
  const resp = await api.post<AuthResult>('/auth/oauth-accedi', { consenso_privacy: consensoPrivacy })
  salvaSessione(resp.data)
  return resp.data
}

export const modificaDatiAccount = async (dati: {
  nome: string
  cognome: string
}): Promise<{ nome: string; cognome: string }> => {
  const resp = await api.put<{ nome: string; cognome: string }>('/utente/profilo', dati)
  const profiloStr = localStorage.getItem('profilo:v1')
  if (profiloStr) {
    const profilo = JSON.parse(profiloStr)
    profilo.nome = resp.data.nome
    profilo.cognome = resp.data.cognome
    localStorage.setItem('profilo:v1', JSON.stringify(profilo))
  }
  return resp.data
}

export const logout = async (): Promise<void> => {
  localStorage.removeItem('token')
  localStorage.removeItem('ruolo')
  localStorage.removeItem('profilo:v1')
  await supabase.auth.signOut()
}

export const utenteCorrente = (): { ruolo: 'UT' | 'OP' | 'AP'; profilo: Profilo } | null => {
  const token = localStorage.getItem('token')
  const ruolo = localStorage.getItem('ruolo') as 'UT' | 'OP' | 'AP' | null
  const profiloStr = localStorage.getItem('profilo:v1')
  if (!token || !ruolo || !profiloStr) return null
  try {
    // Decode JWT exp without verification (client-side only)
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (Date.now() / 1000 > payload.exp) {
      localStorage.removeItem('token')
      localStorage.removeItem('ruolo')
      localStorage.removeItem('profilo:v1')
      return null
    }
    return { ruolo, profilo: JSON.parse(profiloStr) }
  } catch {
    return null
  }
}
