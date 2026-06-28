# Tour Guidato Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a zero-dependency guided tour system that auto-starts on first access and is replayable via a "?" button, with WCAG accessibility (IIN-3).

**Architecture:** Declarative step arrays define each tour. A React context provider manages state (active tour, current step, seen-status via localStorage). A single overlay component rendered via `createPortal` handles both full-screen modal steps and CSS-spotlight steps (box-shadow trick). Elements are targeted by `data-tour` attributes, not CSS selectors.

**Tech Stack:** React 19, TypeScript, CSS (no external dependencies)

## Global Constraints

- Zero external dependencies — no tour libraries
- WCAG IIN-3: focus trap, aria-live, keyboard nav (Escape, arrows), contrast ≥ 4.5:1, `prefers-reduced-motion`
- All Italian UI text
- `data-tour` attributes for DOM targeting — no CSS selector coupling
- localStorage key format: `tour_visto_{tourId}_{userId}`
- Mobile breakpoint: `< 768px` → tooltip becomes bottom-sheet
- CSS custom properties from `VistaHomePageUtente.css` (e.g. `--sm-primary: #155e52`) are reused
- The `utenteCorrente()` function from `AuthService.ts` provides the current user's `profilo.id`

---

### Task 1: Types and Tour Step Data

**Files:**
- Create: `frontend/src/tour/types.ts`
- Create: `frontend/src/tour/tours/tourHomepageUtente.ts`

**Interfaces:**
- Consumes: nothing
- Produces: `TourStep`, `TourConfig`, `TourContextValue` types; `tourHomepageUtente` constant of type `TourConfig`

- [ ] **Step 1: Create `frontend/src/tour/types.ts`**

```typescript
export type TourStepType = 'modal' | 'spotlight';
export type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

export interface TourStep {
  type: TourStepType;
  target?: string;
  tooltipPosition?: TooltipPosition;
  titolo: string;
  testo: string;
  ctaLabel?: string;
  ctaAction?: () => void;
}

export interface TourConfig {
  id: string;
  pathname: string;
  steps: TourStep[];
}

export interface TourContextValue {
  tourAttivo: string | null;
  stepCorrente: number;
  totalStep: number;
  tourDisponibile: boolean;
  avviaTour: (tourId: string) => void;
  prossimoStep: () => void;
  stepPrecedente: () => void;
  chiudiTour: () => void;
}
```

- [ ] **Step 2: Create `frontend/src/tour/tours/tourHomepageUtente.ts`**

```typescript
import type { TourConfig } from '../types';

export const tourHomepageUtente: TourConfig = {
  id: 'homepage-ut',
  pathname: '/utente/home',
  steps: [
    {
      type: 'modal',
      titolo: 'Benvenuto in Smart Mobility!',
      testo: 'Scopri come muoverti a Zootropolis con bici, monopattini e auto condivise. Questo tour ti mostrerà le funzionalità principali. Puoi saltarlo in qualsiasi momento.',
    },
    {
      type: 'spotlight',
      target: 'mappa',
      tooltipPosition: 'bottom',
      titolo: 'La mappa della città',
      testo: 'Qui vedi tutti i mezzi disponibili vicino a te. Ogni icona rappresenta un mezzo: toccala per vederne i dettagli.',
    },
    {
      type: 'spotlight',
      target: 'filtro-mezzi',
      tooltipPosition: 'bottom',
      titolo: 'Filtra per tipo di mezzo',
      testo: 'Usa questi filtri per visualizzare solo bici, monopattini o auto.',
    },
    {
      type: 'spotlight',
      target: 'selezione-mezzi',
      tooltipPosition: 'top',
      titolo: 'Seleziona i mezzi',
      testo: 'Tocca un mezzo sulla mappa per aggiungerlo alla tua selezione. Puoi selezionarne più di uno per prenotarli insieme.',
    },
    {
      type: 'spotlight',
      target: 'btn-prenota',
      tooltipPosition: 'top',
      titolo: 'Prenota',
      testo: 'Quando hai scelto, premi qui per prenotare. Avrai un tempo limitato per raggiungere il mezzo e sbloccarlo.',
    },
    {
      type: 'spotlight',
      target: 'pannello-prenotazioni',
      tooltipPosition: 'top',
      titolo: 'Le tue prenotazioni',
      testo: 'Qui trovi le prenotazioni attive con il countdown. Premi "Sblocca" quando sei vicino al mezzo per iniziare la corsa.',
    },
    {
      type: 'spotlight',
      target: 'btn-sidebar',
      tooltipPosition: 'right',
      titolo: 'Il menu',
      testo: 'Da qui accedi a tutto il resto: cronologia corse, pagamenti, abbonamenti, promozioni e segnalazioni.',
    },
    {
      type: 'spotlight',
      target: 'banner-suggerimenti',
      tooltipPosition: 'top',
      titolo: 'Suggerimenti intelligenti',
      testo: 'Smart Mobility ti propone mezzi e percorsi in base alle tue abitudini e alla situazione del traffico.',
    },
    {
      type: 'modal',
      titolo: 'Tutto pronto!',
      testo: 'Ora sai come funziona. Seleziona un mezzo sulla mappa per iniziare! Se vorrai rivedere questo tour, premi il pulsante "?" in basso a destra.',
      ctaLabel: 'Inizia',
    },
  ],
};
```

- [ ] **Step 3: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit --pretty 2>&1 | head -20`

Expected: no errors related to `tour/` files

- [ ] **Step 4: Commit**

```bash
git add frontend/src/tour/types.ts frontend/src/tour/tours/tourHomepageUtente.ts
git commit -m "feat(tour): add types and homepage tour step data (IIN-3)"
```

---

### Task 2: TourProvider (context + state logic)

**Files:**
- Create: `frontend/src/tour/useTour.ts`
- Create: `frontend/src/tour/TourProvider.tsx`

**Interfaces:**
- Consumes: `TourConfig`, `TourContextValue` from `tour/types.ts`; `utenteCorrente()` from `services/AuthService.ts`
- Produces: `TourProvider` component (props: `tours: Record<string, TourConfig>`, `children: React.ReactNode`); `useTour()` hook returning `TourContextValue`

- [ ] **Step 1: Create `frontend/src/tour/useTour.ts`**

```typescript
import { useContext } from 'react';
import { TourContext } from './TourProvider';
import type { TourContextValue } from './types';

export function useTour(): TourContextValue {
  const ctx = useContext(TourContext);
  if (!ctx) throw new Error('useTour must be used within TourProvider');
  return ctx;
}
```

- [ ] **Step 2: Create `frontend/src/tour/TourProvider.tsx`**

```tsx
import { createContext, useState, useCallback, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { utenteCorrente } from '../services/AuthService';
import type { TourConfig, TourContextValue } from './types';

export const TourContext = createContext<TourContextValue | null>(null);

function lsKey(tourId: string, userId: string): string {
  return `tour_visto_${tourId}_${userId}`;
}

function trovaStepValido(
  steps: TourConfig['steps'],
  indice: number,
  direzione: 1 | -1,
): number {
  let i = indice;
  while (i >= 0 && i < steps.length) {
    const step = steps[i];
    if (step.type === 'modal' || !step.target) return i;
    if (document.querySelector(`[data-tour="${step.target}"]`)) return i;
    i += direzione;
  }
  return -1;
}

interface TourProviderProps {
  tours: Record<string, TourConfig>;
  children: React.ReactNode;
}

export function TourProvider({ tours, children }: TourProviderProps) {
  const location = useLocation();
  const [tourAttivo, setTourAttivo] = useState<string | null>(null);
  const [stepCorrente, setStepCorrente] = useState(0);
  const focusPrecedenteRef = useRef<HTMLElement | null>(null);
  const autoStartFatto = useRef(false);

  const configCorrente = tourAttivo ? tours[tourAttivo] : null;
  const totalStep = configCorrente?.steps.length ?? 0;

  const tourDisponibile = Object.values(tours).some(
    t => t.pathname === location.pathname,
  );

  const chiudiTour = useCallback(() => {
    if (!tourAttivo) return;
    const utente = utenteCorrente();
    if (utente) {
      localStorage.setItem(lsKey(tourAttivo, utente.profilo.id), 'true');
    }
    setTourAttivo(null);
    setStepCorrente(0);
    focusPrecedenteRef.current?.focus();
    focusPrecedenteRef.current = null;
  }, [tourAttivo]);

  const avviaTour = useCallback(
    (tourId: string) => {
      const config = tours[tourId];
      if (!config) return;
      focusPrecedenteRef.current = document.activeElement as HTMLElement;
      setTourAttivo(tourId);
      setStepCorrente(0);
    },
    [tours],
  );

  const prossimoStep = useCallback(() => {
    if (!configCorrente) return;
    const prossimo = trovaStepValido(configCorrente.steps, stepCorrente + 1, 1);
    if (prossimo === -1) {
      chiudiTour();
    } else {
      setStepCorrente(prossimo);
    }
  }, [configCorrente, stepCorrente, chiudiTour]);

  const stepPrecedente = useCallback(() => {
    if (!configCorrente) return;
    const precedente = trovaStepValido(configCorrente.steps, stepCorrente - 1, -1);
    if (precedente !== -1) {
      setStepCorrente(precedente);
    }
  }, [configCorrente, stepCorrente]);

  // Auto-start: first visit on matching pathname
  useEffect(() => {
    if (tourAttivo || autoStartFatto.current) return;
    const utente = utenteCorrente();
    if (!utente) return;

    const tourDaAvviare = Object.values(tours).find(
      t => t.pathname === location.pathname && !localStorage.getItem(lsKey(t.id, utente.profilo.id)),
    );
    if (!tourDaAvviare) return;

    autoStartFatto.current = true;
    const timer = setTimeout(() => avviaTour(tourDaAvviare.id), 800);
    return () => clearTimeout(timer);
  }, [location.pathname, tours, tourAttivo, avviaTour]);

  // Auto-close on route change
  useEffect(() => {
    if (!tourAttivo || !configCorrente) return;
    if (location.pathname !== configCorrente.pathname) {
      chiudiTour();
    }
  }, [location.pathname, tourAttivo, configCorrente, chiudiTour]);

  const valore: TourContextValue = {
    tourAttivo,
    stepCorrente,
    totalStep,
    tourDisponibile,
    avviaTour,
    prossimoStep,
    stepPrecedente,
    chiudiTour,
  };

  return (
    <TourContext.Provider value={valore}>
      {children}
    </TourContext.Provider>
  );
}
```

- [ ] **Step 3: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit --pretty 2>&1 | head -20`

Expected: no errors related to `tour/` files

- [ ] **Step 4: Commit**

```bash
git add frontend/src/tour/useTour.ts frontend/src/tour/TourProvider.tsx
git commit -m "feat(tour): add TourProvider context with auto-start and auto-close (IIN-3)"
```

---

### Task 3: TourOverlay (portal + spotlight CSS + tooltip + modal)

**Files:**
- Create: `frontend/src/tour/TourOverlay.tsx`
- Create: `frontend/src/tour/TourOverlay.css`

**Interfaces:**
- Consumes: `useTour()` hook; `TourStep` from `types.ts`; reads `tours` prop from a `tours` prop passed directly (or reads config from context — see note below)
- Produces: `<TourOverlay tours={tours} />` component rendered in App.tsx; renders overlay via `createPortal(document.body)`

Note: `TourOverlay` needs access to the step data. The cleanest way: it receives `tours` as a prop (same object passed to `TourProvider`), and uses `useTour().tourAttivo` + `useTour().stepCorrente` to index into it.

- [ ] **Step 1: Create `frontend/src/tour/TourOverlay.css`**

```css
/* ============================================================
   Tour Guidato — Overlay, Spotlight, Tooltip
   ============================================================ */

/* Spotlight: applied to target element via data-tour-active attribute */
[data-tour-active] {
  position: relative !important;
  z-index: 10001 !important;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7) !important;
  border-radius: 8px;
  pointer-events: auto;
}

/* Modal overlay backdrop */
.tour-overlay-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: tour-fadeIn 200ms ease;
}

@keyframes tour-fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Modal card (for modal-type steps) */
.tour-modal {
  background: #fff;
  border-radius: 20px;
  padding: 36px 32px 28px;
  max-width: 420px;
  width: calc(100vw - 48px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: tour-scaleIn 250ms cubic-bezier(0.34, 1.56, 0.64, 1);
  outline: none;
}

@keyframes tour-scaleIn {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}

.tour-modal__titolo {
  font-size: 22px;
  font-weight: 800;
  color: #155e52;
  margin: 0 0 12px;
  letter-spacing: -0.01em;
}

.tour-modal__testo {
  font-size: 15px;
  line-height: 1.6;
  color: #334155;
  margin: 0 0 28px;
}

/* Tooltip (for spotlight-type steps) */
.tour-tooltip {
  position: fixed;
  z-index: 10002;
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  max-width: 340px;
  width: calc(100vw - 48px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  animation: tour-tooltipIn 200ms ease;
  outline: none;
}

@keyframes tour-tooltipIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.tour-tooltip__titolo {
  font-size: 16px;
  font-weight: 700;
  color: #155e52;
  margin: 0 0 6px;
}

.tour-tooltip__testo {
  font-size: 14px;
  line-height: 1.55;
  color: #475569;
  margin: 0 0 16px;
}

/* Close button (top-right of tooltip) */
.tour-tooltip__chiudi {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 18px;
  color: #94a3b8;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 6px;
  line-height: 1;
  transition: color 150ms, background 150ms;
}

.tour-tooltip__chiudi:hover {
  color: #334155;
  background: rgba(0, 0, 0, 0.05);
}

.tour-tooltip__chiudi:focus-visible {
  outline: 2px solid #155e52;
  outline-offset: 2px;
}

/* Progress dots */
.tour-dots {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}

.tour-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e2e8f0;
  transition: background 200ms;
}

.tour-dot--attivo {
  background: #155e52;
}

/* Navigation buttons (shared by modal and tooltip) */
.tour-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.tour-btn {
  padding: 10px 22px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 150ms, transform 100ms;
  border: none;
}

.tour-btn:active { transform: scale(0.97); }

.tour-btn:focus-visible {
  outline: 2px solid #155e52;
  outline-offset: 2px;
}

.tour-btn--primario {
  background: #155e52;
  color: #fff;
}

.tour-btn--primario:hover { opacity: 0.88; }

.tour-btn--secondario {
  background: #e0f2ee;
  color: #155e52;
}

.tour-btn--secondario:hover { opacity: 0.8; }

.tour-btn--salta {
  background: none;
  color: #94a3b8;
  padding: 10px 12px;
  font-size: 13px;
}

.tour-btn--salta:hover { color: #64748b; }

/* Mobile bottom-sheet for tooltip */
@media (max-width: 767px) {
  .tour-tooltip {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    top: auto;
    max-width: none;
    width: 100%;
    border-radius: 20px 20px 0 0;
    padding: 24px 20px calc(env(safe-area-inset-bottom, 0px) + 20px);
    animation: tour-slideUp 250ms ease;
  }

  @keyframes tour-slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .tour-overlay-backdrop,
  .tour-modal,
  .tour-tooltip,
  [data-tour-active] {
    animation: none !important;
    transition: none !important;
  }
}
```

- [ ] **Step 2: Create `frontend/src/tour/TourOverlay.tsx`**

```tsx
import { useEffect, useRef, useState, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { useTour } from './useTour';
import type { TourConfig, TourStep } from './types';
import './TourOverlay.css';

interface TourOverlayProps {
  tours: Record<string, TourConfig>;
}

const TOOLTIP_GAP = 12;

function calcolaPosizioneTooltip(
  rect: DOMRect,
  posizione: TourStep['tooltipPosition'],
  tooltipEl: HTMLElement,
): { top: number; left: number } {
  const tt = tooltipEl.getBoundingClientRect();
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  let top = 0;
  let left = 0;

  switch (posizione) {
    case 'bottom':
      top = rect.bottom + TOOLTIP_GAP;
      left = rect.left + rect.width / 2 - tt.width / 2;
      break;
    case 'top':
      top = rect.top - tt.height - TOOLTIP_GAP;
      left = rect.left + rect.width / 2 - tt.width / 2;
      break;
    case 'left':
      top = rect.top + rect.height / 2 - tt.height / 2;
      left = rect.left - tt.width - TOOLTIP_GAP;
      break;
    case 'right':
      top = rect.top + rect.height / 2 - tt.height / 2;
      left = rect.right + TOOLTIP_GAP;
      break;
    default:
      top = rect.bottom + TOOLTIP_GAP;
      left = rect.left + rect.width / 2 - tt.width / 2;
  }

  // Clamp to viewport
  left = Math.max(8, Math.min(left, vw - tt.width - 8));
  top = Math.max(8, Math.min(top, vh - tt.height - 8));

  return { top, left };
}

function Dots({ totale, corrente }: { totale: number; corrente: number }) {
  return (
    <div className="tour-dots" aria-hidden="true">
      {Array.from({ length: totale }, (_, i) => (
        <span key={i} className={`tour-dot${i === corrente ? ' tour-dot--attivo' : ''}`} />
      ))}
    </div>
  );
}

function NavButtons({
  stepCorrente,
  totalStep,
  onIndietro,
  onAvanti,
  onSalta,
  ctaLabel,
}: {
  stepCorrente: number;
  totalStep: number;
  onIndietro: () => void;
  onAvanti: () => void;
  onSalta: () => void;
  ctaLabel?: string;
}) {
  const isUltimo = stepCorrente === totalStep - 1;
  const isPrimo = stepCorrente === 0;

  return (
    <div className="tour-nav">
      {isPrimo ? (
        <button type="button" className="tour-btn tour-btn--salta" onClick={onSalta}>
          Salta
        </button>
      ) : (
        <button type="button" className="tour-btn tour-btn--secondario" onClick={onIndietro}>
          Indietro
        </button>
      )}
      <button type="button" className="tour-btn tour-btn--primario" onClick={onAvanti}>
        {isUltimo ? (ctaLabel ?? 'Fine') : `Avanti ${stepCorrente + 1}/${totalStep}`}
      </button>
    </div>
  );
}

export function TourOverlay({ tours }: TourOverlayProps) {
  const { tourAttivo, stepCorrente, totalStep, prossimoStep, stepPrecedente, chiudiTour } = useTour();
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [posizione, setPosizione] = useState<{ top: number; left: number } | null>(null);
  const [pronto, setPronto] = useState(false);

  const config = tourAttivo ? tours[tourAttivo] : null;
  const step = config?.steps[stepCorrente] ?? null;

  // Scroll to target + position tooltip
  const posizionaSpotlight = useCallback(() => {
    if (!step || step.type === 'modal' || !step.target) {
      setPronto(true);
      return;
    }

    // Remove previous spotlight
    document.querySelectorAll('[data-tour-active]').forEach(el => {
      el.removeAttribute('data-tour-active');
    });

    const el = document.querySelector(`[data-tour="${step.target}"]`) as HTMLElement | null;
    if (!el) {
      prossimoStep();
      return;
    }

    el.setAttribute('data-tour-active', '');

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    el.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', block: 'center' });

    setTimeout(() => {
      if (!tooltipRef.current) {
        setPronto(true);
        return;
      }
      const isMobile = window.innerWidth < 768;
      if (isMobile) {
        setPosizione(null);
      } else {
        const rect = el.getBoundingClientRect();
        const pos = calcolaPosizioneTooltip(rect, step.tooltipPosition, tooltipRef.current);
        setPosizione(pos);
      }
      setPronto(true);
    }, 400);
  }, [step, prossimoStep]);

  useEffect(() => {
    setPronto(false);
    setPosizione(null);
    if (step) posizionaSpotlight();
  }, [step, posizionaSpotlight]);

  // Cleanup spotlight on unmount or tour end
  useEffect(() => {
    if (!tourAttivo) {
      document.querySelectorAll('[data-tour-active]').forEach(el => {
        el.removeAttribute('data-tour-active');
      });
    }
  }, [tourAttivo]);

  // Keyboard navigation
  useEffect(() => {
    if (!tourAttivo) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { chiudiTour(); return; }
      if (e.key === 'ArrowRight') { prossimoStep(); return; }
      if (e.key === 'ArrowLeft') { stepPrecedente(); return; }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [tourAttivo, chiudiTour, prossimoStep, stepPrecedente]);

  // Focus trap: focus the dialog on step change
  useEffect(() => {
    if (pronto && tooltipRef.current) {
      tooltipRef.current.focus();
    }
  }, [pronto, stepCorrente]);

  if (!tourAttivo || !step || !config) return null;

  // Modal step
  if (step.type === 'modal') {
    return createPortal(
      <div className="tour-overlay-backdrop" role="dialog" aria-modal="true" aria-label="Tour guidato">
        <div className="tour-modal" ref={tooltipRef} tabIndex={-1}>
          <div aria-live="polite">
            <h2 className="tour-modal__titolo">{step.titolo}</h2>
            <p className="tour-modal__testo">{step.testo}</p>
          </div>
          <Dots totale={totalStep} corrente={stepCorrente} />
          <NavButtons
            stepCorrente={stepCorrente}
            totalStep={totalStep}
            onIndietro={stepPrecedente}
            onAvanti={() => {
              step.ctaAction?.();
              prossimoStep();
            }}
            onSalta={chiudiTour}
            ctaLabel={step.ctaLabel}
          />
        </div>
      </div>,
      document.body,
    );
  }

  // Spotlight step
  const tooltipStyle: React.CSSProperties = posizione
    ? { top: posizione.top, left: posizione.left }
    : {};

  return createPortal(
    <>
      <div
        className="tour-tooltip"
        ref={tooltipRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-label="Tour guidato"
        style={{
          ...tooltipStyle,
          visibility: pronto ? 'visible' : 'hidden',
        }}
      >
        <button
          type="button"
          className="tour-tooltip__chiudi"
          onClick={chiudiTour}
          aria-label="Chiudi tour"
        >
          ✕
        </button>
        <div aria-live="polite">
          <h3 className="tour-tooltip__titolo">{step.titolo}</h3>
          <p className="tour-tooltip__testo">{step.testo}</p>
        </div>
        <Dots totale={totalStep} corrente={stepCorrente} />
        <NavButtons
          stepCorrente={stepCorrente}
          totalStep={totalStep}
          onIndietro={stepPrecedente}
          onAvanti={prossimoStep}
          onSalta={chiudiTour}
          ctaLabel={step.ctaLabel}
        />
      </div>
    </>,
    document.body,
  );
}
```

- [ ] **Step 3: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit --pretty 2>&1 | head -20`

Expected: no errors related to `tour/` files

- [ ] **Step 4: Commit**

```bash
git add frontend/src/tour/TourOverlay.tsx frontend/src/tour/TourOverlay.css
git commit -m "feat(tour): add TourOverlay with spotlight CSS and tooltip positioning (IIN-3)"
```

---

### Task 4: TourTrigger + wire up in App.tsx and VistaHomePageUtente

**Files:**
- Create: `frontend/src/tour/TourTrigger.tsx`
- Create: `frontend/src/tour/TourTrigger.css`
- Modify: `frontend/src/App.tsx` — wrap routes with TourProvider, add TourOverlay
- Modify: `frontend/src/views/utente/VistaHomePageUtente.tsx` — add `data-tour` attributes and TourTrigger

**Interfaces:**
- Consumes: `useTour()` hook; `TourProvider` and `TourOverlay` components; `tourHomepageUtente` config
- Produces: Complete wired-up tour system

- [ ] **Step 1: Create `frontend/src/tour/TourTrigger.css`**

```css
.tour-trigger {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #155e52;
  color: #fff;
  border: none;
  font-size: 22px;
  font-weight: 700;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 0 4px 16px rgba(21, 94, 82, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 200ms, box-shadow 200ms;
}

.tour-trigger:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(21, 94, 82, 0.5);
}

.tour-trigger:active {
  transform: scale(0.96);
}

.tour-trigger:focus-visible {
  outline: 2px solid #06d6a0;
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  .tour-trigger {
    transition: none;
  }
}
```

- [ ] **Step 2: Create `frontend/src/tour/TourTrigger.tsx`**

```tsx
import { useTour } from './useTour';
import './TourTrigger.css';

interface TourTriggerProps {
  tourId: string;
}

export function TourTrigger({ tourId }: TourTriggerProps) {
  const { tourAttivo, tourDisponibile, avviaTour } = useTour();

  if (!tourDisponibile || tourAttivo) return null;

  return (
    <button
      type="button"
      className="tour-trigger"
      onClick={() => avviaTour(tourId)}
      aria-label="Riavvia tour guidato"
    >
      ?
    </button>
  );
}
```

- [ ] **Step 3: Modify `frontend/src/App.tsx` — wrap with TourProvider + add TourOverlay**

Add imports at the top of the file:
```typescript
import { TourProvider } from './tour/TourProvider'
import { TourOverlay } from './tour/TourOverlay'
import { tourHomepageUtente } from './tour/tours/tourHomepageUtente'
```

Add the tours constant above the `App` function:
```typescript
const TOURS = {
  [tourHomepageUtente.id]: tourHomepageUtente,
}
```

Wrap the existing `<main>` and `<Routes>` inside TourProvider, and add TourOverlay as a sibling.

The relevant section of the `App` function return becomes (only showing changed structure):
```tsx
<BrowserRouter>
  <TourProvider tours={TOURS}>
    <main id="main-content" tabIndex={-1} style={{ outline: 'none' }}>
      <Routes>
        {/* ... all existing routes unchanged ... */}
      </Routes>
    </main>
    <TourOverlay tours={TOURS} />
  </TourProvider>
</BrowserRouter>
```

- [ ] **Step 4: Modify `frontend/src/views/utente/VistaHomePageUtente.tsx` — add `data-tour` attributes and TourTrigger**

4a. Add import at the top:
```typescript
import { TourTrigger } from '../../tour/TourTrigger'
```

4b. Add `data-tour="mappa"` to the map container. Find the `<GoogleMap` element (line ~398) and wrap it or add to its parent. The map is already inside `.vista-mappa`. Add `data-tour` to the `<GoogleMap>` element by wrapping it in a div:

Change:
```tsx
<GoogleMap
  className="mappa-container"
```
To:
```tsx
<div data-tour="mappa" style={{ width: '100%', height: '100%' }}>
<GoogleMap
  className="mappa-container"
```
And close the div after `</GoogleMap>` (after line ~442).

4c. Add `data-tour="btn-sidebar"` to the hamburger button. Find the button with `className="btn-hamburger"` (line ~388):

Change:
```tsx
<button
  type="button"
  className="btn-hamburger"
  onClick={() => apriSidebar('menu')}
  aria-label="Menu"
>
```
To:
```tsx
<button
  type="button"
  className="btn-hamburger"
  data-tour="btn-sidebar"
  onClick={() => apriSidebar('menu')}
  aria-label="Menu"
>
```

4d. Add `data-tour="banner-suggerimenti"` to the suggestions banner. Find the banner div (line ~445):

Change:
```tsx
<div className={`suggerimenti-banner${bannerAperto ? ' suggerimenti-banner--aperto' : ''}`}>
```
To:
```tsx
<div data-tour="banner-suggerimenti" className={`suggerimenti-banner${bannerAperto ? ' suggerimenti-banner--aperto' : ''}`}>
```

4e. Add `data-tour` attributes inside the bottom sheet panel. The panel div is at line ~511.

Add `data-tour="pannello-prenotazioni"` to the prenotazioni section (line ~526):
Change:
```tsx
<div className="pannello-prenotazioni">
```
To:
```tsx
<div className="pannello-prenotazioni" data-tour="pannello-prenotazioni">
```

Add `data-tour="selezione-mezzi"` to the selezione section (line ~581):
Change:
```tsx
<div className="selezione-sezione">
```
To:
```tsx
<div className="selezione-sezione" data-tour="selezione-mezzi">
```

Add `data-tour="btn-prenota"` to the Prenota button (line ~605):
Change:
```tsx
<button
  className="btn-prenota"
  onClick={() => {
    setModalita('prenota')
    toggleSelezione(mezzoAttivo)
  }}
>
  Prenota
</button>
```
To:
```tsx
<button
  className="btn-prenota"
  data-tour="btn-prenota"
  onClick={() => {
    setModalita('prenota')
    toggleSelezione(mezzoAttivo)
  }}
>
  Prenota
</button>
```

Add `data-tour="filtro-mezzi"` to the selezione badge in the topbar (line ~384). The selezione badge is the closest thing to a "filter" indicator:
Change:
```tsx
{selezione.length > 0 && (
  <span className="selezione-badge">{selezione.length}/{nMax}</span>
)}
```
To:
```tsx
{selezione.length > 0 && (
  <span className="selezione-badge" data-tour="filtro-mezzi">{selezione.length}/{nMax}</span>
)}
```

Note: if the badge is not visible (selezione is empty), the "filtro-mezzi" step will be auto-skipped — this is correct behavior per spec.

4f. Add `<TourTrigger>` at the end of the component, just before the closing `</div>` of `.vista-mappa` (before line ~907):

Add before `{errore && ...}`:
```tsx
<TourTrigger tourId="homepage-ut" />
```

- [ ] **Step 5: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit --pretty 2>&1 | head -20`

Expected: no errors

- [ ] **Step 6: Verify dev server starts and tour renders**

Run: `cd frontend && npm run dev`

Open http://localhost:5173 in a browser. After logging in as a UT user:
- The tour should auto-start after ~800ms with the welcome modal
- Clicking "Avanti" should progress through steps
- Spotlight should highlight elements with dark overlay around them
- Clicking "?" button should replay the tour
- Pressing Escape should close the tour
- Arrow keys should navigate steps

- [ ] **Step 7: Commit**

```bash
git add frontend/src/tour/TourTrigger.tsx frontend/src/tour/TourTrigger.css frontend/src/App.tsx frontend/src/views/utente/VistaHomePageUtente.tsx
git commit -m "feat(tour): wire up TourProvider, TourOverlay, TourTrigger and data-tour attributes (IIN-3)"
```

---

### Task 5: Visual polish and edge case fixes

**Files:**
- Modify: `frontend/src/tour/TourOverlay.css` — adjust z-index interactions with existing UI
- Modify: `frontend/src/tour/TourOverlay.tsx` — handle window resize during spotlight

**Interfaces:**
- Consumes: all tour components from previous tasks
- Produces: production-ready tour behavior

- [ ] **Step 1: Add resize handler in TourOverlay.tsx**

Inside the `TourOverlay` component, add a resize listener that recalculates tooltip position when the window is resized during a spotlight step. Add this `useEffect` after the existing keyboard navigation effect:

```tsx
useEffect(() => {
  if (!tourAttivo || !pronto) return;
  const handler = () => posizionaSpotlight();
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, [tourAttivo, pronto, posizionaSpotlight]);
```

- [ ] **Step 2: Add click-outside-tooltip to advance**

In `TourOverlay.tsx`, for spotlight steps, add click handler on the spotlight area. When the user clicks outside the tooltip but on the spotlighted element, it should not close the tour. When clicking the dark area (which doesn't exist as a div), nothing happens — this is correct because the box-shadow is not a clickable element.

No code change needed — this is already handled correctly by the current architecture.

- [ ] **Step 3: Ensure suggerimenti-banner z-index doesn't clash**

The suggestions banner has `z-index: 10` in `VistaHomePageUtente.css`. The tour overlay uses `z-index: 10000+`. No clash — no changes needed.

- [ ] **Step 4: Test mobile bottom-sheet behavior**

Open browser dev tools, toggle responsive mode to < 768px width. Verify:
- Spotlight tooltip appears as bottom-sheet (full-width, fixed to bottom)
- Modal steps remain centered
- Navigation buttons are reachable

- [ ] **Step 5: Test prefers-reduced-motion**

In browser dev tools → Rendering → Emulate CSS media feature `prefers-reduced-motion: reduce`. Verify:
- No animations on overlay, modal, tooltip, or spotlight
- `scrollIntoView` uses `behavior: 'auto'`

- [ ] **Step 6: Test keyboard accessibility**

With screen reader off:
- Tab: focus should stay within tooltip/modal
- Escape: closes tour
- Arrow Left/Right: navigate steps
- After closing: focus returns to previously focused element

- [ ] **Step 7: Commit if any changes were made**

```bash
git add -u frontend/src/tour/
git commit -m "feat(tour): add resize handling and polish edge cases (IIN-3)"
```
