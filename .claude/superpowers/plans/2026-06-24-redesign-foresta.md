# Redesign "Foresta" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Applicare la direzione visiva "Foresta" (dark control-room, validata nel mockup `mockups-redesign/index.html`) a tutta l'app React reale — UT, OP, AP — senza modificare alcun comportamento applicativo.

**Architecture:** Si introduce un layer di **token centrali** (CSS custom properties) + un foglio di **primitivi condivisi** importati globalmente in `main.tsx`. Ogni vista mantiene il proprio file `.css` ma viene rifattorizzata per **consumare i token** invece dei colori hardcoded, e il markup viene ristrutturato per riprodurre il layout del mockup. Nessun cambiamento a logica, routing, servizi o API: il redesign è puramente visivo. Gli unici nuovi componenti React sono i gusci di navigazione condivisi (bottom-nav UT, sidebar OP/AP) per evitare duplicazione.

**Tech Stack:** React 19 + Vite + TypeScript · CSS per-vista (no Tailwind/CSS-modules) · Google Maps `@vis.gl/react-google-maps` · Recharts 3 · Font Google (Space Grotesk, Hanken Grotesk, Space Mono).

## Global Constraints

- **Zero cambi di comportamento.** Markup interattivo (handler, `value`/`onChange`, `aria-*`, `role`, `name`, routing, chiamate ai servizi) resta identico. Si toccano solo classi CSS, struttura di wrapping puramente presentazionale e il contenuto dei file `.css`.
- **Build sempre verde.** `npm run build` (= `tsc -b && vite build`) DEVE passare prima di ogni commit. Non si fa push su `main` (lavoriamo su `feature/redesign-foresta`).
- **Lint pulito.** `npm run lint` non deve introdurre nuovi errori.
- **Niente nuovi test runner.** Il frontend NON ha vitest/jest (solo eslint). La verifica per ogni task è: build verde + lint pulito + **review visiva** su `npm run dev`. Non inventare framework di test frontend.
- **Accessibilità preservata o migliorata (IIN-3 / WCAG 2.1 AA).** Mantenere `:focus-visible`, `.skip-to-content`, `aria-*`, contrasti testo ≥ 4.5:1. I token sono scelti per rispettare AA su sfondo `--bg`.
- **Token come unica fonte del colore.** Dopo la Fase 0, nessun nuovo colore hardcoded nei CSS delle viste: usare sempre `var(--token)`. Colori esadecimali letterali ammessi solo dentro `theme.css`.
- **Glossario di dominio invariato** (`Corsa`, `Mezzo`, `Zona`, `Abbonamento`, `Segnalazione`, ruoli UT/OP/AP). Il redesign non rinomina nulla.
- **Reference visiva:** `mockups-redesign/index.html` (palette Foresta = default). Ogni task di vista replica la sezione corrispondente di quel file.

---

## Metodologia di migrazione per-vista (la "ricetta")

Ogni task di Fase 1–3 segue **esattamente** questa procedura. È richiamata per riferimento da ogni task di vista (è un Global Constraint operativo, non un placeholder):

1. **Leggi** il `.tsx` e il `.css` correnti della vista.
2. **Inventario colori:** elenca ogni colore hardcoded (`#155e52`, `#fff`, `#e0e0e0`, inline `style`, ecc.).
3. **Sostituisci** ogni colore con il token equivalente (tabella in Task 1). Sposta gli inline-style cromatici dentro classi CSS che usano i token.
4. **Ristruttura il markup** per riprodurre il layout del mockup per quella vista (card sfumate, raggi morbidi, bottom-sheet/sidebar, KPI mono), **senza toccare** handler, stato, `aria-*`, routing.
5. **Applica i primitivi** condivisi (`.sm-btn`, `.sm-card`, `.sm-chip`, ecc., Task 2) dove sostituiscono CSS duplicato; rimuovi il CSS reso ridondante.
6. **Verifica:** `npm run build` verde → `npm run lint` pulito → `npm run dev`, apri la rotta, confronta con il mockup, controlla focus da tastiera e responsive (≤480px e desktop).
7. **Commit** con messaggio `redesign(<area>): <vista>`.

---

## File Structure

**Nuovi file:**
- `frontend/src/styles/theme.css` — token Foresta (colori, raggi, ombre, font, z-index). Unico luogo con esadecimali letterali.
- `frontend/src/styles/primitives.css` — classi riusabili: `.sm-btn`, `.sm-card`, `.sm-chip`, `.sm-kpi`, `.sm-sheet`, `.sm-bottom-nav`, `.sm-sidebar`, ecc.
- `frontend/src/styles/maps.ts` — array di stile Google Maps "Foresta" (`FORESTA_MAP_STYLE`) + helper colori per Recharts (`chartColors()`).
- `frontend/src/components/layout/BottomNavUtente.tsx` (+ `.css`) — bottom-nav condivisa UT.
- `frontend/src/components/layout/SidebarRuolo.tsx` (+ `.css`) — sidebar condivisa OP/AP.

**File globali modificati:**
- `frontend/index.html` — `<link>` ai font Google nel `<head>`.
- `frontend/src/main.tsx` — import di `theme.css` e `primitives.css` **prima** di `accessibilita.css`.
- `frontend/src/accessibilita.css` — colori hardcoded → token.
- `frontend/src/App.tsx` — `PlaceholderView` inline-style → token/primitivi.

**File di vista modificati** (un task ciascuno): tutte le viste in `src/views/{auth,utente,operatore,amministrazione}` + componenti mappa (`ZonaPoligono`, `TooltipZona`, `PopupStatsZona`, `ClusterLayerAP`, `HeatmapLayerAP`).

---

## FASE 0 — Fondamenta

### Task 1: Token Foresta (`theme.css`)

**Files:**
- Create: `frontend/src/styles/theme.css`
- Modify: `frontend/index.html` (head)
- Modify: `frontend/src/main.tsx`

**Interfaces:**
- Produces: token CSS globali su `:root` consumati da tutto il resto. Nomi esatti (gli altri task dipendono da questi): `--bg --bg-2 --surface --surface-2 --surface-3 --text --text-dim --text-mute --accent --accent-2 --accent-ink --border --border-2 --pin --warn --danger --glow --shadow --glass --r-lg --r-md --r-sm --r-pill --ff-display --ff-body --ff-mono --ease`.

- [ ] **Step 1: Crea `frontend/src/styles/theme.css`**

```css
/* theme.css — Token "Foresta" (redesign). Unico file con esadecimali letterali. */
:root {
  /* superfici */
  --bg:#051F20; --bg-2:rgba(7,38,36,.33);
  --surface:#0B2B26; --surface-2:#163832; --surface-3:#235347;
  /* testo */
  --text:#DAF1DE; --text-dim:#8EB69B; --text-mute:#5d7a6a;
  /* accento */
  --accent:#5FF0C4; --accent-2:#8EB69B; --accent-ink:#04201c;
  /* bordi / stati */
  --border:rgba(142,182,155,.16); --border-2:rgba(142,182,155,.28);
  --pin:#5FF0C4; --warn:#FFC971; --danger:#FF8A7A;
  /* effetti */
  --glow:rgba(95,240,196,.16);
  --shadow:0 24px 60px -28px rgba(0,0,0,.7);
  --glass:rgba(11,43,38,.55);
  /* forma */
  --r-lg:28px; --r-md:20px; --r-sm:14px; --r-pill:999px;
  /* tipografia */
  --ff-display:"Space Grotesk", system-ui, sans-serif;
  --ff-body:"Hanken Grotesk", system-ui, sans-serif;
  --ff-mono:"Space Mono", ui-monospace, monospace;
  /* motion / layer */
  --ease:cubic-bezier(.22,.61,.36,1);
}
html, body { background: var(--bg); color: var(--text); }
body { font-family: var(--ff-body); }
h1,h2,h3,h4 { font-family: var(--ff-display); letter-spacing:-.02em; }
@media (prefers-reduced-motion: reduce) {
  *{ animation:none !important; transition:none !important; }
}
```

- [ ] **Step 2: Aggiungi i font in `frontend/index.html`** dentro `<head>` (prima del tag che chiude head):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

- [ ] **Step 3: Importa i token in `frontend/src/main.tsx`** — aggiungere le due righe PRIMA di `import './accessibilita.css'`:

```tsx
import './styles/theme.css'
import './styles/primitives.css'
import './accessibilita.css'
```

(Nota: `primitives.css` viene creato nel Task 2; finché non esiste, Vite segnala errore — eseguire Task 2 subito dopo, oppure creare un `primitives.css` vuoto temporaneo. Per evitare build rotta, in questo task creare anche un `primitives.css` vuoto con un commento.)

- [ ] **Step 4: Crea `frontend/src/styles/primitives.css` segnaposto** (verrà riempito nel Task 2):

```css
/* primitives.css — riempito nel Task 2 */
```

- [ ] **Step 5: Verifica build**

Run: `cd frontend && npm run build`
Expected: PASS (nessun errore TypeScript/Vite). Lo sfondo dell'app è ora verde scuro.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/styles/theme.css frontend/src/styles/primitives.css frontend/index.html frontend/src/main.tsx
git commit -m "redesign(foundation): token Foresta + font + import globali"
```

---

### Task 2: Primitivi condivisi (`primitives.css`)

**Files:**
- Modify: `frontend/src/styles/primitives.css`

**Interfaces:**
- Consumes: token del Task 1.
- Produces: classi riusabili consumate da tutte le viste. Nomi esatti: `.sm-btn .sm-btn--primary .sm-btn--ghost .sm-btn--block .sm-card .sm-card--grad .sm-chip .sm-chip--ok .sm-kpi .sm-kpi--big .sm-label-xs .sm-sheet .sm-mono .sm-batt`.

- [ ] **Step 1: Scrivi i primitivi** in `frontend/src/styles/primitives.css` (sostituendo il segnaposto):

```css
/* primitives.css — componenti visivi riusabili (redesign Foresta) */
.sm-mono{ font-family:var(--ff-mono); }
.sm-label-xs{ font-family:var(--ff-mono); font-size:10px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--text-dim); }

/* bottoni */
.sm-btn{ font-family:var(--ff-body); font-weight:700; border:none; cursor:pointer;
  border-radius:var(--r-pill); padding:14px 20px; font-size:15px; display:inline-flex;
  align-items:center; justify-content:center; gap:9px; transition:.2s var(--ease); }
.sm-btn--primary{ background:var(--accent); color:var(--accent-ink);
  box-shadow:0 10px 30px -8px var(--glow); }
.sm-btn--primary:hover{ transform:translateY(-1px); }
.sm-btn--ghost{ background:var(--surface-2); color:var(--text); border:1px solid var(--border); }
.sm-btn--block{ width:100%; }
.sm-btn:disabled{ opacity:.5; cursor:not-allowed; transform:none; }

/* card */
.sm-card{ background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r-md); padding:16px; }
.sm-card--grad{ background:linear-gradient(160deg,var(--surface-2),var(--surface));
  position:relative; overflow:hidden; }

/* chip */
.sm-chip{ font-family:var(--ff-mono); font-size:11px; padding:5px 10px;
  border-radius:var(--r-pill); background:var(--surface-2); color:var(--text-dim);
  border:1px solid var(--border); display:inline-flex; gap:6px; align-items:center; }
.sm-chip--ok{ color:var(--accent); border-color:var(--border-2); }

/* kpi numerico */
.sm-kpi{ font-family:var(--ff-mono); font-weight:700; font-size:30px; line-height:1;
  letter-spacing:-.02em; }
.sm-kpi--big{ font-size:42px; }

/* bottom-sheet */
.sm-sheet{ background:var(--surface); border-radius:26px 26px 0 0;
  border-top:1px solid var(--border-2); padding:12px 16px 18px;
  box-shadow:0 -20px 50px -30px rgba(0,0,0,.6); }

/* indicatore batteria */
.sm-batt{ font-family:var(--ff-mono); font-size:12px; color:var(--accent);
  display:inline-flex; align-items:center; gap:6px; }
.sm-batt .bar{ width:30px; height:6px; border-radius:99px; background:var(--surface-3); overflow:hidden; }
.sm-batt .bar i{ display:block; height:100%; background:var(--accent); border-radius:99px; }
```

- [ ] **Step 2: Verifica build**

Run: `cd frontend && npm run build`
Expected: PASS.

- [ ] **Step 3: Review visiva rapida** — `npm run dev`, la pagina di login mostra già sfondo/testo a tema (anche se non ancora rifattorizzata).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/styles/primitives.css
git commit -m "redesign(foundation): primitivi condivisi (btn/card/chip/kpi/sheet)"
```

---

### Task 3: Accessibilità a token (`accessibilita.css`)

**Files:**
- Modify: `frontend/src/accessibilita.css`

**Interfaces:**
- Consumes: token del Task 1.

- [ ] **Step 1: Sostituisci i colori hardcoded con token.** In `accessibilita.css`:
  - `.skip-to-content` `background:#155e52` → `background:var(--surface-2)`; `color:#ffffff` → `color:var(--text)`.
  - `.skip-to-content:focus` `outline:3px solid #ffffff` → `outline:3px solid var(--accent)`.
  - `*:focus-visible` `outline:3px solid #155e52 !important` → `outline:3px solid var(--accent) !important`.
  - Ogni altro `#155e52`/`#fff`/grigio nel file → token equivalente (`--accent` per il verde brand, `--text`/`--text-dim` per i testi, `--border` per i bordi).

- [ ] **Step 2: Verifica contrasto e focus** — `npm run dev`, naviga con `Tab`: lo skip-link e l'anello di focus devono essere chiaramente visibili sul nuovo sfondo (anello menta `--accent` su `--bg`: ratio > 7:1, OK AA/AAA).

- [ ] **Step 3: Verifica build** — `cd frontend && npm run build` → PASS.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/accessibilita.css
git commit -m "redesign(foundation): accessibilita.css su token Foresta"
```

---

### Task 4: Stile mappe Google + tema Recharts (`maps.ts`)

**Files:**
- Create: `frontend/src/styles/maps.ts`

**Interfaces:**
- Produces: `export const FORESTA_MAP_STYLE: google.maps.MapTypeStyle[]` e `export function chartColors(): { accent: string; grid: string; text: string }`. Consumati dalle viste mappa (UT home, Corsa, OP dashboard) e dalle viste con Recharts (AP, Tariffe).

- [ ] **Step 1: Crea `frontend/src/styles/maps.ts`**

```ts
// maps.ts — stile mappa "Foresta" + colori grafici derivati dai token.

// Stile Google Maps coerente col dark control-room (verde profondo).
export const FORESTA_MAP_STYLE: google.maps.MapTypeStyle[] = [
  { elementType: 'geometry', stylers: [{ color: '#07221f' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#8EB69B' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#051F20' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#0B2B26' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#163832' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#04201c' }] },
  { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#0d322c' }] },
  { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: '#163832' }] },
  { featureType: 'transit', stylers: [{ visibility: 'off' }] },
  { featureType: 'administrative', elementType: 'geometry', stylers: [{ color: '#235347' }] },
]

// Helper colori per Recharts: legge i token correnti dal :root.
export function chartColors() {
  const s = getComputedStyle(document.documentElement)
  return {
    accent: s.getPropertyValue('--accent').trim() || '#5FF0C4',
    grid: s.getPropertyValue('--border').trim() || 'rgba(142,182,155,.16)',
    text: s.getPropertyValue('--text-dim').trim() || '#8EB69B',
  }
}
```

- [ ] **Step 2: Verifica build** — `cd frontend && npm run build` → PASS (il file è importato dalle viste nei task successivi; in questo task verifica solo che compili).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/styles/maps.ts
git commit -m "redesign(foundation): stile mappa Foresta + helper colori Recharts"
```

---

### Task 5: Gusci di navigazione condivisi (BottomNav UT + Sidebar OP/AP)

**Files:**
- Create: `frontend/src/components/layout/BottomNavUtente.tsx`, `BottomNavUtente.css`
- Create: `frontend/src/components/layout/SidebarRuolo.tsx`, `SidebarRuolo.css`

**Interfaces:**
- Produces:
  - `export default function BottomNavUtente(): JSX.Element` — usa `useNavigate`/`useLocation` (react-router già in uso) e marca `aria-current="page"` sull'attivo. Voci: Mappa `/utente/home`, Storico `/utente/storico`, FAB Sblocca (apre `/utente/home`), Abbonamenti `/utente/abbonamenti`, Profilo `/utente/profilo`.
  - `export default function SidebarRuolo({ ruolo }: { ruolo: 'OP' | 'AP' }): JSX.Element` — elenco voci derivato dal `ruolo`, attivo via `useLocation`, con `aria-current`.
- Consumes: token + primitivi.

- [ ] **Step 1: Scrivi `BottomNavUtente.tsx`** replicando la `.bnav` del mockup (4 voci + FAB centrale), con `NavLink`/`useLocation` per lo stato attivo e `aria-current="page"`. CSS in `BottomNavUtente.css` usando i token (`.sm-bottom-nav` come nel mockup: glass, `--glass`, `--accent` per l'attivo).

- [ ] **Step 2: Scrivi `SidebarRuolo.tsx`** con le voci per OP (Mappa flotta, Mezzi, Tariffe & Offerte, Regole & Zone, Segnalazioni, …) e AP (Dashboard, Report, Zone & Heatmap, Operatori), replicando `.side/.navi` del mockup. CSS in `SidebarRuolo.css` su token.

- [ ] **Step 3: Verifica build** — `cd frontend && npm run build` → PASS. (I componenti vengono montati nelle viste dei task di fase; qui basta che compilino e che un mount di prova in `VistaHomePageUtente` renderizzi senza errori — il cablaggio reale avviene nei rispettivi task di vista.)

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/layout/
git commit -m "redesign(foundation): gusci navigazione condivisi (BottomNav UT, Sidebar OP/AP)"
```

---

### Task 6: App shell — `PlaceholderView` a token

**Files:**
- Modify: `frontend/src/App.tsx` (componente `PlaceholderView`, ~righe 30-70)

- [ ] **Step 1: Sostituisci gli inline-style cromatici** di `PlaceholderView` con classi a token: il bottone LOGOUT usa `.sm-btn .sm-btn--ghost`; `color:#555` → `var(--text-dim)`; il padding/layout resta. Non toccare la logica di logout né le rotte.

- [ ] **Step 2: Verifica build** — `cd frontend && npm run build` → PASS.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "redesign(foundation): PlaceholderView su token/primitivi"
```

---

## FASE 1 — Utente (UT)

> Ogni task seguente applica la **ricetta di migrazione** (sezione "Metodologia") alla vista indicata, replicando la sezione corrispondente del mockup. Verifica = build verde + lint pulito + review visiva sulla rotta indicata.

### Task 7: VistaLogin (esempio completamente lavorato)

**Files:**
- Modify: `frontend/src/views/auth/VistaLogin.tsx`
- Modify: `frontend/src/views/auth/VistaLogin.css`

**Design (mockup → §02 "Login"):** card centrata su `--bg`; titolo display "Bentornato."; input dentro `.sm-card` con `.sm-label-xs`; CTA `.sm-btn--primary--block`; bottone Google `.sm-btn--ghost`; link "Registrati" in `--accent`. Le icone SVG `stroke="#155e52"` passano a `stroke="currentColor"` con `color:var(--accent)` sul contenitore.

- [ ] **Step 1: Rifattorizza `VistaLogin.css`** — sostituisci nel file: `background:#ffffff` (`.vista-login`) → `var(--bg)`; bordi/`#e0e0e0` → `var(--border)`; testo `#222`/`#555` → `var(--text)`/`var(--text-dim)`; ogni `#155e52` → `var(--accent)`; `border-radius` input/bottoni → `var(--r-pill)`/`var(--r-md)`; aggiungi `font-family:var(--ff-body)` ai campi e `var(--ff-display)` ai titoli. La `.login-input` su `--surface` con bordo `--border` e focus `--accent`.

- [ ] **Step 2: Aggiorna gli SVG inline in `VistaLogin.tsx`** — `stroke="#155e52"` → `stroke="currentColor"` (occhio mostra/nascondi password) e wrappa con `style={{color:'var(--accent)'}}` o classe; rimuovi gli inline-style cromatici del checkbox consenso (`accentColor:'#155e52'` → `var(--accent)`; `color:'#555'` → `var(--text-dim)`; link `#155e52` → `var(--accent)`). **Non toccare** `value/onChange/aria-label/handleSubmit/handleGoogle`.

- [ ] **Step 3: Build + lint** — `cd frontend && npm run build && npm run lint` → PASS.

- [ ] **Step 4: Review visiva** — `npm run dev`, apri `/`: confronta con §02 del mockup; verifica focus da tastiera su input e bottoni; verifica mobile (≤480px) e desktop.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/auth/VistaLogin.tsx frontend/src/views/auth/VistaLogin.css
git commit -m "redesign(ut): VistaLogin"
```

### Task 8: VistaHomePageUtente — `/utente/home`
**Files:** Modify `frontend/src/views/utente/VistaHomePageUtente.tsx` + `.css`.
**Design (mockup §02 "Home / mappa viva"):** mappa a tutto schermo con `FORESTA_MAP_STYLE` (Task 4) applicato alla `<Map>`; barra ricerca glass in alto; bottom-sheet `.sm-sheet` "Mezzi vicini" con righe mezzo (icona in `.sm-card` quadrata, `.sm-batt`); monta `<BottomNavUtente/>` (Task 5). Applica la ricetta. Verifica build+lint+visiva.
**Commit:** `redesign(ut): VistaHomePageUtente + map style`.

### Task 9: VistaCorsa — `/utente/corsa/:idMezzo`
**Files:** Modify `frontend/src/views/utente/VistaCorsa.tsx` + `.css`.
**Design (mockup §02 "Corsa attiva"):** mappa con polilinea `--accent`; chip "CORSA IN CORSO" con dot pulsante; bottom-sheet con readout mono a 3 celle (DURATA/KM·H/€) usando `.sm-kpi`; bottoni Pausa `.sm-btn--ghost` + Termina `.sm-btn--primary`. **Non toccare** la logica pausa/termina. Ricetta + verifica.
**Commit:** `redesign(ut): VistaCorsa`.

### Task 10: VistaPagamenti — `/utente/pagamenti`
**Files:** Modify `frontend/src/views/utente/VistaPagamenti.tsx` + `.css`.
**Design (mockup §02 "Riepilogo + pagamento"):** ring totale; ricevuta con `.rrow` (righe tratteggiate), badge promo/abbonamento (`.badge` → riusa `.sm-chip--ok` o nuovo `.sm-badge` se serve); card metodo di pagamento + CTA `.sm-btn--primary--block`. Ricetta + verifica.
**Commit:** `redesign(ut): VistaPagamenti`.

### Task 11: VistaAbbonamenti — `/utente/abbonamenti`
**Files:** Modify `frontend/src/views/utente/VistaAbbonamenti.tsx` + `.css`.
**Design (mockup §02 "Abbonamenti"):** piani in card; piano in evidenza con bordo `--accent` e gradiente; lista feature con check `--accent`. Mantenere la logica "un solo piano attivo" (nasconde piani se `corrente.data_fine > now()`). Ricetta + verifica.
**Commit:** `redesign(ut): VistaAbbonamenti`.

### Task 12: VistaStoricoCorse — `/utente/storico`
**Files:** Modify `frontend/src/views/utente/VistaStoricoCorse.tsx` + `.css`.
**Design (mockup §02 "Storico"):** card riepilogo mensile `.sm-card--grad` con 3 KPI mono; lista corse con icona mezzo, importo mono, badge abbonamento/promo; raggruppamento per `gruppo_corsa_id` invariato. Ricetta + verifica.
**Commit:** `redesign(ut): VistaStoricoCorse`.

### Task 13: VistaProfiloUtente — `/utente/profilo`
**Files:** Modify `frontend/src/views/utente/VistaProfiloUtente.tsx` + `.css`.
**Design:** intestazione profilo (avatar/iniziali su `--surface-2`), card dati in `.sm-card`, campi editabili a token, CTA salva `.sm-btn--primary`. Ricetta + verifica.
**Commit:** `redesign(ut): VistaProfiloUtente`.

### Task 14: VistaSegnalazione — `/utente/segnalazione`
**Files:** Modify `frontend/src/views/utente/VistaSegnalazione.tsx` + `.css`.
**Design:** form in `.sm-card`, select/textarea a token (`--surface`, bordo `--border`, focus `--accent`), CTA invio `.sm-btn--primary`. Ricetta + verifica.
**Commit:** `redesign(ut): VistaSegnalazione`.

### Task 15: VistaRecensione — `/utente/recensione`
**Files:** Modify `frontend/src/views/utente/VistaRecensione.tsx` + `.css`.
**Design:** stelle/rating in `--accent`, textarea a token, CTA `.sm-btn--primary`. Ricetta + verifica.
**Commit:** `redesign(ut): VistaRecensione`.

---

## FASE 2 — Operatore (OP)

### Task 16: VistaMappaOperatore — `/operatore/dashboard`
**Files:** Modify `frontend/src/views/operatore/VistaMappaOperatore.tsx` + `.css`.
**Design (mockup §03 "Plancia Operatore"):** layout plancia con `<SidebarRuolo ruolo="OP"/>` (Task 5); riga KPI (`.sm-card`/`.sm-card--grad`, KPI mono, "Batteria<20%" in `--warn`); mappa con `FORESTA_MAP_STYLE` + legenda zone; tabella flotta con `.state` (disp/uso/man). Precedenza zone `vietata>limitata>operativa` resta logica runtime invariata. Ricetta + verifica.
**Commit:** `redesign(op): VistaMappaOperatore`.

### Task 17: VistaMezziOperatore — `/operatore/mezzi`
**Files:** Modify `.tsx` + `.css`.
**Design:** tabella mezzi a tema (`.tbl`, `.state`, batteria mono), filtri in `.sm-chip`, azioni `.sm-btn--ghost`. Stati mezzo invariati (gestiti da ServizioMobilità). Ricetta + verifica.
**Commit:** `redesign(op): VistaMezziOperatore`.

### Task 18: VistaTariffe — `/operatore/tariffe`
**Files:** Modify `.tsx` + `.css`.
**Design:** card tariffe a token; eventuali grafici Recharts ricolorati con `chartColors()` (Task 4). Ricetta + verifica.
**Commit:** `redesign(op): VistaTariffe`.

### Task 19: VistaOfferte — `/operatore/offerte`
**Files:** Modify `.tsx` + `.css`.
**Design:** lista offerte/promozioni in card, badge sconto `--accent`, form a token. Ricetta + verifica.
**Commit:** `redesign(op): VistaOfferte`.

### Task 20: VistaImpostazioniRegole — `/operatore/impostazioni-regole`
**Files:** Modify `.tsx` + `.css`.
**Design:** pannelli regole fine-corsa in `.sm-card`, toggle/select a token, legenda zone. Ricetta + verifica.
**Commit:** `redesign(op): VistaImpostazioniRegole`.

### Task 21: VistaParametriSistema — `/operatore/parametri-sistema`
**Files:** Modify `.tsx` + `.css`.
**Design:** form parametri in `.sm-card`, valori numerici mono, CTA salva `.sm-btn--primary`. Ricetta + verifica.
**Commit:** `redesign(op): VistaParametriSistema`.

### Task 22: VistaSegnalazioniOperatore — `/operatore/segnalazioni`
**Files:** Modify `.tsx` + `.css`.
**Design:** lista segnalazioni con stato in `.sm-chip` (aperta/in lavorazione/chiusa → `--warn`/`--accent`), dettaglio in `.sm-card`. Ricetta + verifica.
**Commit:** `redesign(op): VistaSegnalazioniOperatore`.

### Task 23: VistaGestioneUtentiOperatore — `/operatore/utenti`
**Files:** Modify `.tsx` + `.css`.
**Design:** tabella utenti (`.tbl`), stato account in `.state`, azioni sospendi/riattiva `.sm-btn--ghost`. Logica invariata. Ricetta + verifica.
**Commit:** `redesign(op): VistaGestioneUtentiOperatore`.

### Task 24: VistaRecensioniOperatore — `/operatore/recensioni`
**Files:** Modify `.tsx` + `.css`.
**Design:** lista recensioni in card, rating `--accent`. Ricetta + verifica.
**Commit:** `redesign(op): VistaRecensioniOperatore`.

### Task 25: VistaStoricoModifiche — `/operatore/storico-modifiche`
**Files:** Modify `.tsx` + `.css`.
**Design:** timeline/tabella modifiche a token, timestamp mono. Ricetta + verifica.
**Commit:** `redesign(op): VistaStoricoModifiche`.

---

## FASE 3 — Amministrazione (AP)

### Task 26: VistaDashboardAP — `/ap/dashboard`
**Files:** Modify `frontend/src/views/amministrazione/VistaDashboardAP.tsx` + `.css`.
**Design (mockup §04 "Dashboard AP"):** `<SidebarRuolo ruolo="AP"/>`; riga 4 KPI; grafico domanda (Recharts ricolorato con `chartColors()`); heatmap densità zone. Logica cluster/heatmap invariata. Ricetta + verifica.
**Commit:** `redesign(ap): VistaDashboardAP`.

### Task 27: VistaReportAP — `/ap/report`
**Files:** Modify `frontend/src/views/amministrazione/VistaReportAP.tsx` + `.css`.
**Design:** report in card, grafici Recharts a tema, tabelle `.tbl`, export CTA `.sm-btn`. Ricetta + verifica.
**Commit:** `redesign(ap): VistaReportAP`.

### Task 28: Componenti mappa AP (cluster/heatmap/zona/tooltip/popup)
**Files:** Modify `frontend/src/components/ClusterLayerAP.tsx`, `HeatmapLayerAP.tsx`, `ZonaPoligono.tsx`, `TooltipZona.tsx`, `PopupStatsZona.tsx` (+ eventuali `.css`).
**Design:** colori poligoni/heatmap/tooltip allineati ai token (`--accent`, `--warn`, `--danger`, `--surface`, `--border`); il `PopupStatsZona` e `TooltipZona` come `.sm-card` glass. Mantenere invariata la logica di clustering e i gradienti heatmap (solo ricolorazione). Ricetta + verifica.
**Commit:** `redesign(ap): componenti mappa a token`.

### Task 29: Viste minori — PrivacyPolicy + CallbackOAuth
**Files:** Modify `frontend/src/views/PrivacyPolicy.tsx` + `.css`; `frontend/src/views/auth/CallbackOAuth.tsx`.
**Design:** PrivacyPolicy come documento leggibile su `--bg`/`--surface` con tipografia a token; CallbackOAuth: spinner/stato di caricamento a tema. Ricetta + verifica.
**Commit:** `redesign(misc): PrivacyPolicy + CallbackOAuth`.

---

## FASE 4 — Rifinitura finale

### Task 30: Pass globale di QA visivo + pulizia mockup
**Files:** eventuale `frontend/src/styles/primitives.css`/`theme.css` (ritocchi), `mockups-redesign/` (decisione).
- [ ] **Step 1:** Naviga tutte le rotte (UT/OP/AP) su `npm run dev`; annota incoerenze (spaziature, raggi, contrasti) e correggi nei token/primitivi (un solo punto).
- [ ] **Step 2:** Verifica accessibilità: `Tab` su ogni vista (focus visibile), `prefers-reduced-motion` (DevTools → Rendering), contrasti AA sui testi principali.
- [ ] **Step 3:** Responsive: 360px / 768px / 1280px su una vista per ruolo.
- [ ] **Step 4:** Build finale `cd frontend && npm run build && npm run lint` → PASS.
- [ ] **Step 5:** Decidi sorte di `mockups-redesign/`: spostare in `docs/` come riferimento o aggiungere a `.gitignore`. Documentare la scelta.
- [ ] **Step 6:** Aggiorna `docs/README.md`/`docs/Sprintn3.md` con una nota sul redesign (Definition of Done: documentazione).
- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "redesign(qa): pass finale accessibilità/responsive + note docs"
```

---

## Self-Review

**Spec coverage:** Tutte le 25 viste reali (da `App.tsx`) + componenti mappa + shell coperti: UT (Task 7–15: Login, Home, Corsa, Pagamenti, Abbonamenti, Storico, Profilo, Segnalazione, Recensione), OP (Task 16–25: Mappa, Mezzi, Tariffe, Offerte, ImpostazioniRegole, Parametri, Segnalazioni, Utenti, Recensioni, StoricoModifiche), AP (Task 26–28: Dashboard, Report, componenti mappa), minori (Task 29). Fondamenta (Task 1–6) + QA (Task 30). Nessuna rotta di `App.tsx` priva di task.

**Placeholder scan:** Le Fasi 1–3 usano deliberatamente la "ricetta" condivisa + design-note specifiche per vista invece di markup finale fabbricato: per un reskin CSS il markup definitivo si deriva dal codice attuale a tempo di esecuzione (leggerlo prima è parte dello Step 1 della ricetta). Foundation (Task 1–4) e l'esempio Login (Task 7) hanno codice completo. Nessun "TBD/TODO".

**Type consistency:** Nomi token (Task 1) e classi primitive (`.sm-*`, Task 2) usati coerentemente in tutti i task. `FORESTA_MAP_STYLE` e `chartColors()` (Task 4) referenziati con la stessa firma in Task 8/9/16/18/26/27. `BottomNavUtente`/`SidebarRuolo` (Task 5) con le props dichiarate.
