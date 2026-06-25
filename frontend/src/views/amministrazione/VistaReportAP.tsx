import { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts'
import { recuperaReport, type Report, type DatoTorta } from '../../services/ReportService'
import './VistaReportAP.css'

function LabelTorta({ cx, cy, midAngle, outerRadius, name, value }: {
  cx: number; cy: number; midAngle: number; outerRadius: number; name: string; value: number
}) {
  const RAD = Math.PI / 180
  const r = outerRadius + 24
  const x = cx + r * Math.cos(-midAngle * RAD)
  const y = cy + r * Math.sin(-midAngle * RAD)
  return (
    <text x={x} y={y} textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={12} fill="#8EB69B">
      {name} {value}%
    </text>
  )
}

export default function VistaReportAP() {
  const [report, setReport] = useState<Report | null>(null)
  const [errore, setErrore] = useState('')

  useEffect(() => {
    recuperaReport()
      .then(setReport)
      .catch(() => setErrore('Statistiche non disponibili, riprovare'))
  }, [])

  if (errore) {
    return <div className="vista-report-ap"><div className="ap-errore">{errore}</div></div>
  }
  if (!report) {
    return <div className="vista-report-ap"><div className="report-body">Caricamento…</div></div>
  }

  const quotaDominante = report.dati_torta.reduce(
    (max, d) => d.value > max.value ? d : max,
    report.dati_torta[0] ?? { name: '—', value: 0, colore: '#999' }
  )

  return (
    <div className="vista-report-ap">
      <div className="report-body">

        <div className="report-kpi-row">
          <div className="report-kpi-card">
            <span className="report-kpi-valore report-kpi-valore--1">{report.corse_totali}</span>
            <span className="report-kpi-label">Corse totali</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore report-kpi-valore--2">{report.durata_media_h}h</span>
            <span className="report-kpi-label">Durata media</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore report-kpi-valore--3">{report.distanza_totale_km} km</span>
            <span className="report-kpi-label">Distanza totale</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore report-kpi-valore--4">{quotaDominante.value}%</span>
            <span className="report-kpi-label">{quotaDominante.name}</span>
          </div>
        </div>

        <div className="report-charts-row">
          <div className="report-chart-card grande">
            <div className="report-chart-titolo">Corse settimanali per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={report.dati_settimanali} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(142,182,155,.16)" />
                <XAxis dataKey="giorno" tick={{ fontSize: 12, fill: '#8EB69B' }} />
                <YAxis tick={{ fontSize: 12, fill: '#8EB69B' }} />
                <Tooltip />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12, color: '#8EB69B' }} />
                <Bar dataKey="monopattino" name="Monopattino" stackId="a" fill="#5FF0C4" />
                <Bar dataKey="bicicletta"  name="Bicicletta"  stackId="a" fill="#7fb4ff" />
                <Bar dataKey="automobile"  name="Automobile"  stackId="a" fill="#FF8A7A" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="report-chart-card piccola">
            <div className="report-chart-titolo">Quota per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={report.dati_torta}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  labelLine={false}
                  label={(props) => <LabelTorta {...(props as Parameters<typeof LabelTorta>[0])} />}
                >
                  {report.dati_torta.map((d: DatoTorta) => (
                    <Cell key={d.name} fill={d.colore} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  )
}
