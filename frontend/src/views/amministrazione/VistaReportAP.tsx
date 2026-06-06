import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts'
import { DATI_SETTIMANALI, DATI_TORTA, type DatoTorta } from './datiReportMock'
import './VistaReportAP.css'

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

const corseTotali = DATI_SETTIMANALI.reduce(
  (acc, d) => acc + d.monopattino + d.bicicletta + d.automobile,
  0
)

const quotaDominante = DATI_TORTA.reduce(
  (max, d) => d.value > max.value ? d : max,
  DATI_TORTA[0]
)

export default function VistaReportAP() {
  return (
    <div className="vista-report-ap">
      <div className="report-body">

        <div className="report-kpi-row">
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#155e52' }}>{corseTotali}</span>
            <span className="report-kpi-label">Corse totali</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#3b82f6' }}>26.4h</span>
            <span className="report-kpi-label">Durata media</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#8b5cf6' }}>142 km</span>
            <span className="report-kpi-label">Distanza totale</span>
          </div>
          <div className="report-kpi-card">
            <span className="report-kpi-valore" style={{ color: '#f59e0b' }}>{quotaDominante.value}%</span>
            <span className="report-kpi-label">{quotaDominante.name}</span>
          </div>
        </div>

        <div className="report-charts-row">
          <div className="report-chart-card grande">
            <div className="report-chart-titolo">Corse settimanali per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={DATI_SETTIMANALI} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="giorno" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="monopattino" name="Monopattino" stackId="a" fill="#155e52" />
                <Bar dataKey="bicicletta"  name="Bicicletta"  stackId="a" fill="#2196f3" />
                <Bar dataKey="automobile"  name="Automobile"  stackId="a" fill="#e91e8c" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="report-chart-card piccola">
            <div className="report-chart-titolo">Quota per tipologia</div>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={DATI_TORTA}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
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

      </div>
    </div>
  )
}
