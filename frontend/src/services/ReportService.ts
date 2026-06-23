// [IF-AP.01 / IF-AP.02] ReportService — report aggregati per l'Amministrazione Pubblica
import { api } from './ApiService'

export interface DatoSettimanale {
  giorno: string
  monopattino: number
  bicicletta: number
  automobile: number
}

export interface DatoTorta {
  name: string
  value: number
  colore: string
}

export interface Report {
  corse_totali: number
  durata_media_h: number
  distanza_totale_km: number
  dati_settimanali: DatoSettimanale[]
  dati_torta: DatoTorta[]
}

// [IF-AP.01] recuperaReport(periodo): Report
export const recuperaReport = async (): Promise<Report> => {
  const r = await api.get<Report>('/ap/report')
  return r.data
}

// [IF-AP.02] esportaCSV(idReport): File — scarica il CSV generato dal backend
export const esportaCSV = async (): Promise<void> => {
  const r = await api.get('/ap/report/export', { responseType: 'blob' })
  const url = URL.createObjectURL(r.data as Blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report_smartmobility.csv'
  a.click()
  URL.revokeObjectURL(url)
}
