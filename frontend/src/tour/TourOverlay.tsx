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
  const [targetTrovato, setTargetTrovato] = useState(false);
  const retryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const config = tourAttivo ? tours[tourAttivo] : null;
  const step = config?.steps[stepCorrente] ?? null;

  // Lock body scroll when tour is active
  useEffect(() => {
    if (!tourAttivo) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [tourAttivo]);

  const applicaSpotlight = useCallback((el: HTMLElement) => {
    el.setAttribute('data-tour-active', '');
    setTargetTrovato(true);
    requestAnimationFrame(() => {
      if (!tooltipRef.current) {
        setPronto(true);
        return;
      }
      const isMobile = window.innerWidth < 768;
      if (isMobile) {
        setPosizione(null);
      } else {
        const rect = el.getBoundingClientRect();
        const pos = calcolaPosizioneTooltip(rect, step?.tooltipPosition, tooltipRef.current);
        setPosizione(pos);
      }
      setPronto(true);
    });
  }, [step?.tooltipPosition]);

  // Position tooltip near spotlight target, with retry for targets
  // that appear after a state update (e.g. auto-selected mezzo panel)
  const posizionaSpotlight = useCallback((tentativo = 0) => {
    document.querySelectorAll('[data-tour-active]').forEach(el => {
      el.removeAttribute('data-tour-active');
    });

    if (!step || step.type === 'modal' || !step.target) {
      setTargetTrovato(false);
      setPronto(true);
      return;
    }

    const el = document.querySelector(`[data-tour="${step.target}"]`) as HTMLElement | null;
    if (!el) {
      if (tentativo < 3) {
        retryTimerRef.current = setTimeout(() => posizionaSpotlight(tentativo + 1), 200);
        return;
      }
      setTargetTrovato(false);
      setPronto(true);
      return;
    }

    applicaSpotlight(el);
  }, [step, applicaSpotlight]);

  useEffect(() => {
    if (retryTimerRef.current) clearTimeout(retryTimerRef.current);
    setPronto(false);
    setPosizione(null);
    setTargetTrovato(false);
    if (step) posizionaSpotlight(0);
    return () => { if (retryTimerRef.current) clearTimeout(retryTimerRef.current); };
  }, [step, posizionaSpotlight]);

  // Cleanup spotlight on unmount or tour end
  useEffect(() => {
    if (!tourAttivo) {
      document.querySelectorAll('[data-tour-active]').forEach(el => {
        el.removeAttribute('data-tour-active');
      });
    }
  }, [tourAttivo]);

  // Keyboard navigation + focus trap (IIN-3 WCAG)
  useEffect(() => {
    if (!tourAttivo) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { chiudiTour(); return; }
      if (e.key === 'ArrowRight') { prossimoStep(); return; }
      if (e.key === 'ArrowLeft') { stepPrecedente(); return; }

      // Focus trap: cycle Tab among focusable elements inside the dialog
      if (e.key === 'Tab' && tooltipRef.current) {
        const focusable = tooltipRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        );
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first || document.activeElement === tooltipRef.current) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [tourAttivo, chiudiTour, prossimoStep, stepPrecedente]);

  // Recalculate tooltip position on window resize
  useEffect(() => {
    if (!tourAttivo || !pronto) return;
    const handler = () => posizionaSpotlight();
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, [tourAttivo, pronto, posizionaSpotlight]);

  // Focus trap: focus the dialog on step change
  useEffect(() => {
    if (pronto && tooltipRef.current) {
      tooltipRef.current.focus();
    }
  }, [pronto, stepCorrente]);

  if (!tourAttivo || !step || !config) return null;

  const mostraComeModale = step.type === 'modal' || (step.type === 'spotlight' && !targetTrovato);

  // Modal step (or spotlight fallback when target not found)
  if (mostraComeModale) {
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

  // Spotlight step (target exists in DOM)
  const tooltipStyle: React.CSSProperties = posizione
    ? { top: posizione.top, left: posizione.left }
    : {};

  return createPortal(
    <>
      <div className="tour-spotlight-backdrop" onClick={(e) => e.stopPropagation()} />
      <div
        className={`tour-tooltip${step.tooltipPosition === 'top' ? ' tour-tooltip--top' : ''}`}
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
