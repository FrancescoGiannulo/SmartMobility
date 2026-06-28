# AP Section Redesign — Design Spec

> **For agentic workers:** This is a pure frontend redesign. No backend changes required. All data already available via existing services (`getMezziAP`, `getZoneAP`). Mock data in `datiReportMock.ts` stays as-is.

**Goal:** Modernise the AP (Amministrazione Pubblica) dashboard and report views with a Clean SaaS B2 layout — left icon navigation sidebar, inline KPI topbar, and a proper analytics report page — while keeping the platform's existing `#4caf9a` teal accent and light colour palette.

**Architecture:** Pure CSS/TSX changes to `VistaDashboardAP.tsx`, `VistaDashboardAP.css`, `VistaReportAP.tsx`, `VistaReportAP.css`. No new routes, no new services, no backend work. The two "pages" (Mappa and Report) remain rendered inside the same component via a `vista` state switch, exactly as today.

**Tech Stack:** React 19 + TypeScript, inline CSS via class names, existing Recharts for charts.

---

## Layout Structure

Both pages (Mappa and Report) share the same shell:

```
┌──────┬──────────────────────────────────────────────────┐
│ 52px │  Topbar (36px)                                   │
│ nav  ├──────────────────────────────────────────────────┤
│ side │  Content area (fills remaining height)           │
│ bar  │                                                  │
└──────┴──────────────────────────────────────────────────┘
```

### Left Navigation Sidebar (52px, always visible)

- Background: `#ffffff`, right border: `1px solid #f1f5f9`, box-shadow: `2px 0 8px rgba(0,0,0,0.04)`
- **Top:** Logo tile — 28×28px, `background: #4caf9a`, `border-radius: 8px`, emoji `🚲`, `font-size: 18px`
- **Nav items (2):**
  - `🗺️` label "Mappa" — when active: `background: #ecfdf5`, `border: 1.5px solid #4caf9a`, label colour `#4caf9a`; when inactive: `background: #f8fafc`, label colour `#94a3b8`
  - `📊` label "Report" — same active/inactive rules
  - Each tile: 36×36px, `border-radius: 8px`, centred column flex, icon `font-size: 14px`, label `font-size: 9px font-weight: 700`
  - Click switches `vista` state between `'mappa'` and `'report'`
- **Bottom:** Badge "AP", `font-size: 10px`, `color: #94a3b8`, `font-weight: 700`; then Logout — text "Esci", `font-size: 9px color: #94a3b8 font-weight: 600`, click calls `handleLogout`

### Topbar (36px, inside main area)

- Background: `#ffffff`, `border-bottom: 1px solid #f1f5f9`
- **Left:** Page title, `font-size: 13px font-weight: 700 color: #0f172a`
  - Mappa page: "Dashboard Mappa"
  - Report page: "Report Settimanale"
- **Right (Mappa page):** Three KPI pills inline — `89 disp | 34 uso | 19 man`
  - Each pill: value + label, separated by `|` divider in `#e2e8f0`
  - Colours: disponibili `#4caf9a`, in uso `#3b82f6`, manutenzione `#f59e0b`
  - `font-size: 11px font-weight: 800`
- **Right (Report page):** Two export buttons — `CSV` (background `#4caf9a`, text white) and `PDF` (background `#3b82f6`, text white), `font-size: 10px`, `border-radius: 8px`, `padding: 3px 10px font-weight: 700`

---

## Mappa Page — Content Area

Content area = `display: flex; flex-direction: row` — same as today but without the old topbar.

### Map (flex: 1)

No changes. Same `<Map>` component, same layers (pin/cluster/heatmap), same zone polygons, same popup stats.

### Right Controls Panel (180px fixed width)

- Background: `#ffffff`, `border-left: 1px solid #f1f5f9`, `box-shadow: -2px 0 8px rgba(0,0,0,0.04)`
- Padding: `12px 10px`, `gap: 10px`, `overflow-y: auto`
- Sections (each with an uppercase label `font-size: 9px color: #94a3b8 font-weight: 700 letter-spacing: 0.5px`):

  **Gauge disponibilità:**
  - SVG circle gauge (keep existing `GaugeMezzi` component, same dimensions)
  - Centre it with `display: flex; justify-content: center`

  **Vista mappa:**
  - Label: "Vista"
  - Toggle buttons: Pin / Cluster / Heatmap
  - Active: `background: #4caf9a color: #fff`; inactive: `background: #f1f5f9 color: #64748b`
  - `border-radius: 6px`, `font-size: 10px font-weight: 700`, `padding: 4px`
  - Layout: vertical stack (3 buttons stacked), each `width: 100%`

  **Filtra tipo mezzo:**
  - Label: "Mezzi"
  - 3 chip buttons (🛴 monopattino, 🚲 bicicletta, 🚗 automobile)
  - Active: coloured border + background tint; inactive: `#f1f5f9` with 0.55 opacity
  - Each shows count badge, e.g. `🛴 68`
  - `border-radius: 8px`, `font-size: 10px font-weight: 700`, `padding: 5px 8px`

---

## Report Page — Content Area

Content area = `display: flex; flex-direction: column; gap: 12px; padding: 14px 16px; background: #f8fafc; overflow-y: auto`

### KPI Summary Row (4 cards)

`display: flex; gap: 10px`

Each card:
- Background: `#ffffff`, `border-radius: 12px`, `padding: 12px 16px`, `box-shadow: 0 1px 4px rgba(0,0,0,0.08)`
- Large number: `font-size: 24px font-weight: 900`
- Label below: `font-size: 9px font-weight: 600 color: #94a3b8 text-transform: uppercase letter-spacing: 0.5px`

The 4 cards (values from mock data):
1. **Corse totali** — sum of all `DatoSettimanale` entries, colour `#4caf9a`
2. **Durata media** — hardcoded mock `26.4h`, colour `#3b82f6`
3. **Distanza totale** — hardcoded mock `142 km`, colour `#8b5cf6`
4. **Quota dominante** — computed from `DATI_TORTA` (max value entry name + %), colour `#f59e0b`

### Charts Row

`display: flex; gap: 12px; flex: 1`

**Bar chart card (flex: 2):**
- Background: `#ffffff`, `border-radius: 12px`, `padding: 16px 16px 8px`, `box-shadow: 0 1px 4px rgba(0,0,0,0.08)`
- Title: "Corse settimanali per tipologia", `font-size: 11px font-weight: 700 color: #64748b text-transform: uppercase`
- `<ResponsiveContainer width="100%" height={220}>`
- Existing `<BarChart>` — keep same data, same stacked bars, same colours
- Remove hardcoded `width={480}` — use 100% via ResponsiveContainer

**Pie chart card (flex: 1):**
- Background: `#ffffff`, `border-radius: 12px`, `padding: 16px`, `box-shadow: 0 1px 4px rgba(0,0,0,0.08)`
- Title: "Quota per tipologia"
- `<ResponsiveContainer width="100%" height={220}>`
- Existing `<PieChart>` — keep same data and colours
- Remove hardcoded `width={340}` — use 100%

---

## CSS Files

### `VistaDashboardAP.css` — rewrite

Replace current file entirely. Key new classes:

```
.vista-dashboard-ap         — full viewport, flex row (sidebar + main)
.ap-sidebar                 — 52px, flex column, white, border-right
.ap-sidebar-logo            — 28×28 teal tile
.ap-nav-item                — 36×36 tile, border-radius 8px
.ap-nav-item.attivo         — teal border + ecfdf5 bg
.ap-main                    — flex:1, flex column
.ap-topbar                  — 36px height, white, flex row
.ap-kpi-pill                — inline KPI value+label pair
.ap-kpi-divider             — "|" separator in #e2e8f0
.ap-body                    — flex:1, flex row (map + panel)
.ap-mappa                   — flex:1
.ap-pannello                — 180px, white, border-left, flex column
.ap-pannello-sezione        — section wrapper
.ap-pannello-label          — uppercase small label
.ap-vista-btn               — vista toggle button
.ap-vista-btn.attivo        — teal active state
.ap-chip-mezzo              — vehicle filter chip
.ap-chip-mezzo.attivo       — coloured active state
```

### `VistaReportAP.css` — rewrite

Replace current file entirely. Key new classes:

```
.vista-report-ap            — flex:1, flex column (fills ap-main)
.report-topbar              — 36px, white, flex row (title + export buttons)
.btn-export-csv             — teal bg, white text
.btn-export-pdf             — blue bg, white text
.report-body                — flex:1, flex column, gap 12px, padding 14px 16px, bg #f8fafc, overflow-y auto
.report-kpi-row             — flex row, gap 10px
.report-kpi-card            — white card with shadow, border-radius 12px
.report-kpi-valore          — large number, font-weight 900
.report-kpi-label           — small uppercase label
.report-charts-row          — flex row, gap 12px, flex:1
.report-chart-card          — white card with shadow, flex:2 or flex:1
.report-chart-titolo        — uppercase small chart title
```

---

## Component Changes

### `VistaDashboardAP.tsx`

- Remove old topbar `<div className="dashboard-ap-topbar">` — replace with shared shell: `ap-sidebar` + `ap-main`
- Remove old `dashboard-ap-kpi` strip — move KPI values inline into `ap-topbar` as pills
- Logout button moves into sidebar bottom
- `VistaReportAP` no longer receives `onIndietro` prop — navigation is handled by the sidebar nav item click
- `vista` state and toggle stay in `VistaDashboardAP` — the sidebar renders in both views

### `VistaReportAP.tsx`

- Remove `onIndietro` prop and the "← Indietro" button entirely (navigation via sidebar now)
- Add 4 KPI summary cards computed from existing mock data
- Switch `ResponsiveContainer` to `width="100%"` on both charts (remove hardcoded pixel widths)
- `VistaReportAP` renders only the topbar + body — the sidebar is rendered by the parent

---

## What Does NOT Change

- Map logic, layers, zone polygons, popup stats — unchanged
- `HeatmapLayerAP`, `ClusterLayerAP`, `PopupStatsZona`, `ZonaPoligono` — unchanged
- `GaugeMezzi` component — unchanged, just repositioned in the panel
- `datiReportMock.ts` — unchanged
- All services (`getMezziAP`, `getZoneAP`) — unchanged
- No new routes, no React Router changes
- No backend changes
- `@media print` in `VistaReportAP.css` — preserve: hide topbar and show only charts for PDF print
