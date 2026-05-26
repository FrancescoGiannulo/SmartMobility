import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts'
import { DATI_SETTIMANALI, DATI_TORTA, type DatoSettimanale, type DatoTorta } from './datiReportMock'
import './VistaReportAP.css'

interface VistaReportAPProps {
  onIndietro: () => void
}

function esportaCsv(dati: DatoSettimanale[]): void {
  const intestazione = 'Giorno,Monopattino,Bicicletta,Automobile'
  const righe = dati.map(d => `${d.giorno},${d.monopattino},${d.bicicletta},${d.automobile}`)
  const contenuto = [intestazione, ...righe].join('\n')
  const blob = new Blob(['﻿' + contenuto], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report_smartmobility.csv'
  a.click()
  URL.revokeObjectURL(url)
}

function LabelTorta({ cx, cy, midAngle, outerRadius, name, value }: {
  cx: number; cy: number; midAngle: number; outerRadius: number; name: string; value: number
}) {
  const RAD = Math.PI / 180
  const r = outerRadius + 24
  const x = cx + r * Math.cos(-midAngle * RAD)
  const y = cy + r * Math.sin(-midAngle * RAD)
  return (
    <text x={x} y={y} textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={12} fill="#444">
      {name} {value}%
    </text>
  )
}

export default function VistaReportAP({ onIndietro }: VistaReportAPProps) {
  return (
    <div className="vista-report-ap">
      <div className="report-topbar">
        <button className="btn-indietro" onClick={onIndietro}>← Indietro</button>
        <h2>REPORT</h2>
      </div>

      <div className="report-body">
        <div className="report-grafici">
          <div className="report-card">
            <h3>Corse settimanali per tipologia</h3>
            <ResponsiveContainer width={480} height={260}>
              <BarChart data={DATI_SETTIMANALI} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="giorno" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="monopattino" name="Monopattino" stackId="a" fill="#4caf9a" />
                <Bar dataKey="bicicletta"  name="Bicicletta"  stackId="a" fill="#2196f3" />
                <Bar dataKey="automobile"  name="Automobile"  stackId="a" fill="#e91e8c" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="report-card">
            <h3>Quota per tipologia</h3>
            <ResponsiveContainer width={340} height={260}>
              <PieChart>
                <Pie
                  data={DATI_TORTA}
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  dataKey="value"
                  labelLine={false}
                  label={(props) => <LabelTorta {...(props as Parameters<typeof LabelTorta>[0])} />}
                >
                  {DATI_TORTA.map((d: DatoTorta) => (
                    <Cell key={d.name} fill={d.colore} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="report-azioni">
          <button className="btn-export csv" onClick={() => esportaCsv(DATI_SETTIMANALI)}>
            ESPORTA CSV
          </button>
          <button className="btn-export pdf" onClick={() => window.print()}>
            ESPORTA PDF
          </button>
        </div>
      </div>
    </div>
  )
}
