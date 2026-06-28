# Tour Guidato — Design Spec

**Data:** 2026-06-22
**Item correlato:** IIN-3 (Usabilità / WCAG)
**Scope:** Tour guidato per utente (UT) sulla homepage. Architettura estendibile a OP/AP.

---

## Obiettivo

Fornire un tour guidato non bloccante e facoltativo che si avvia automaticamente al primo accesso dell'utente sulla homepage. L'utente può skipparlo in qualsiasi momento e rigiocarlo tramite un pulsante "?".

## Decisioni architetturali

- **Zero dipendenze esterne**: spotlight CSS (box-shadow trick), portal nativo React, localStorage per persistenza
- **Approccio dichiarativo**: i tour sono array di step definiti come dati, non come codice
- **Disaccoppiamento dal DOM**: gli step puntano ad attributi `data-tour="nome"`, non a selettori CSS
- **Accessibilità WCAG (IIN-3)**: focus trap, aria-live, navigazione tastiera, contrasto ≥ 4.5:1, prefers-reduced-motion

---

## Struttura file

```
frontend/src/
├── tour/
│   ├── TourProvider.tsx           — Context + provider: stato tour, navigazione step
│   ├── TourOverlay.tsx            — Overlay via portal: spotlight CSS + tooltip + modal
│   ├── TourTrigger.tsx            — Pulsante "?" floating per rilanciare il tour
│   ├── useTour.ts                 — Hook custom per consumare il context
│   ├── tours/
│   │   └── tourHomepageUtente.ts  — Array step per homepage UT
│   └── types.ts                   — Tipi TypeScript
```

---

## Tipi TypeScript

```typescript
type TourStepType = 'modal' | 'spotlight';
type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

interface TourStep {
  type: TourStepType;
  target?: string;                // valore di data-tour (assente per modal)
  tooltipPosition?: TooltipPosition; // ignorato per modal e per mobile (<768px → bottom-sheet)
  titolo: string;
  testo: string;
  ctaLabel?: string;              // label custom per il bottone "Avanti" sull'ultimo step
  ctaAction?: () => void;         // azione CTA opzionale sull'ultimo step
}

interface TourConfig {
  id: string;
  pathname: string;               // pagina su cui il tour è attivo (es. "/utente/home")
  steps: TourStep[];
}

interface TourContextValue {
  tourAttivo: string | null;
  stepCorrente: number;
  totalStep: number;
  tourDisponibile: boolean;       // true se la pagina corrente ha un tour registrato
  avviaTour: (tourId: string) => void;
  prossimoStep: () => void;
  stepPrecedente: () => void;
  chiudiTour: () => void;
}
```

---

## Step del tour homepage utente

| # | Tipo | Target (`data-tour`) | Titolo | Testo | Tooltip pos. |
|---|------|----------------------|--------|-------|-------------|
| 0 | modal | — | Benvenuto in Smart Mobility! | Scopri come muoverti a Zootropolis con bici, monopattini e auto condivise. Questo tour ti mostrerà le funzionalità principali. Puoi saltarlo in qualsiasi momento. | centro |
| 1 | spotlight | `mappa` | La mappa della città | Qui vedi tutti i mezzi disponibili vicino a te. Ogni icona rappresenta un mezzo: toccala per vederne i dettagli. | bottom |
| 2 | spotlight | `filtro-mezzi` | Filtra per tipo di mezzo | Usa questi filtri per visualizzare solo bici, monopattini o auto. | bottom |
| 3 | spotlight | `selezione-mezzi` | Seleziona i mezzi | Tocca un mezzo sulla mappa per aggiungerlo alla tua selezione. Puoi selezionarne più di uno per prenotarli insieme. | top |
| 4 | spotlight | `btn-prenota` | Prenota | Quando hai scelto, premi qui per prenotare. Avrai un tempo limitato per raggiungere il mezzo e sbloccarlo. | top |
| 5 | spotlight | `pannello-prenotazioni` | Le tue prenotazioni | Qui trovi le prenotazioni attive con il countdown. Premi "Sblocca" quando sei vicino al mezzo per iniziare la corsa. | top |
| 6 | spotlight | `btn-sidebar` | Il menu | Da qui accedi a tutto il resto: cronologia corse, pagamenti, abbonamenti, promozioni e segnalazioni. | right |
| 7 | spotlight | `banner-suggerimenti` | Suggerimenti intelligenti | Smart Mobility ti propone mezzi e percorsi in base alle tue abitudini e alla situazione del traffico. | top |
| 8 | modal | — | Tutto pronto! | Ora sai come funziona. Seleziona un mezzo sulla mappa per iniziare! Se vorrai rivedere questo tour, premi il pulsante "?" in basso a destra. | centro |

Se un elemento target non è presente nel DOM, lo step viene auto-skippato.

---

## Overlay e spotlight CSS

### Step modal (tipo `modal`)

Card centrata su sfondo scuro (`position: fixed; inset: 0; background: rgba(0,0,0,0.7)`). Card bianca con titolo, testo, bottoni navigazione.

### Step spotlight (tipo `spotlight`)

Nessun div overlay separato. L'elemento target riceve una classe temporanea:

```css
[data-tour-active] {
  position: relative;
  z-index: 10001;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7);
  border-radius: 8px;
}
```

Il box-shadow con spread 9999px crea l'effetto "buio intorno, illuminato solo questo".

### Tooltip

Posizionato con `getBoundingClientRect()` del target + offset. Clamping ai bordi viewport.

Su mobile (viewport < 768px): bottom-sheet fisso (`position: fixed; bottom: 0; left: 0; right: 0`).

Layout tooltip:

```
┌──────────────────────────────┐
│  Titolo step          [X]    │
│                              │
│  Testo descrittivo           │
│                              │
│  ● ● ○ ○ ○ ○ ○ ○ ○         │
│                              │
│  [Indietro]    [Avanti 2/9]  │
└──────────────────────────────┘
```

### Scroll + delay

Prima di illuminare: `element.scrollIntoView({ behavior: 'smooth', block: 'center' })` + `setTimeout(400ms)`.

---

## TourProvider — logica

### Auto-start

1. Al mount, legge `utenteCorrente()` per ottenere `userId`
2. Controlla `localStorage.getItem(`tour_visto_${tourId}_${userId}`)`
3. Se `null` e `location.pathname` matcha il tour → avvia dopo 800ms di delay (tempo per rendering DOM)

### Navigazione

- **prossimoStep**: incrementa indice. Auto-skip se target assente nel DOM. Se ultimo → `chiudiTour`
- **stepPrecedente**: decrementa con stessa logica auto-skip
- **chiudiTour**: `tourAttivo = null`, scrive `tour_visto_${tourId}_${userId} = "true"` in localStorage, restituisce focus all'elemento precedente

### Auto-close su navigazione

`useEffect` su `location.pathname`: se cambia durante un tour attivo → `chiudiTour()`.

### Rigioca on demand

`avviaTour(tourId)` funziona sempre indipendentemente dallo stato "visto".

---

## Pulsante "?" (TourTrigger)

- `position: fixed; bottom: 24px; right: 24px; z-index: 9999`
- 48x48px, border-radius 50%, sfondo colore primario
- `aria-label="Riavvia tour guidato"`
- Visibile solo sulle pagine con un tour registrato (`tourDisponibile`)
- Nascosto durante un tour attivo
- Click → `avviaTour('homepage-ut')`

---

## Integrazione in App.tsx

```tsx
<BrowserRouter>
  <TourProvider tours={tours}>
    <main id="main-content">
      <Routes>...</Routes>
    </main>
    <TourOverlay />
  </TourProvider>
</BrowserRouter>
```

`TourTrigger` va dentro `VistaHomePageUtente.tsx`, non in App.tsx.

---

## Attributi data-tour da aggiungere in VistaHomePageUtente

| Elemento | Attributo |
|----------|-----------|
| Wrapper mappa Google | `data-tour="mappa"` |
| Filtri tipo mezzo | `data-tour="filtro-mezzi"` |
| Pannello selezione mezzi | `data-tour="selezione-mezzi"` |
| Bottone Prenota | `data-tour="btn-prenota"` |
| Pannello prenotazioni attive | `data-tour="pannello-prenotazioni"` |
| Bottone hamburger sidebar | `data-tour="btn-sidebar"` |
| Banner suggerimenti AI | `data-tour="banner-suggerimenti"` |

---

## Accessibilità (IIN-3 / WCAG)

| Requisito | Implementazione |
|-----------|-----------------|
| Focus trap | Focus ciclico dentro tooltip/modal. Al close, focus torna all'elemento precedente |
| `role="dialog"` + `aria-modal="true"` | Sul contenitore overlay |
| `aria-live="polite"` | Sul contenuto tooltip per annuncio cambio step |
| `aria-describedby` | Collega target all'ID tooltip |
| Escape | Chiude tour |
| Frecce ← → | Navigazione step |
| Contrasto | Testo su card: rapporto ≥ 4.5:1 |
| `prefers-reduced-motion` | Disabilita scroll smooth e transizioni CSS |

---

## Estendibilità

Per aggiungere un tour OP/AP in futuro:

1. Creare `tour/tours/tourDashboardOperatore.ts` con l'array di step
2. Aggiungere attributi `data-tour` nella vista OP
3. Registrare il tour nell'oggetto `tours` in App.tsx
4. Inserire `TourTrigger` nella vista OP

Zero modifiche al motore (TourProvider, TourOverlay).
