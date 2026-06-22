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
): number {
  if (indice < 0 || indice >= steps.length) return -1;
  return indice;
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
    const prossimo = trovaStepValido(configCorrente.steps, stepCorrente + 1);
    if (prossimo === -1) {
      chiudiTour();
    } else {
      setStepCorrente(prossimo);
    }
  }, [configCorrente, stepCorrente, chiudiTour]);

  const stepPrecedente = useCallback(() => {
    if (!configCorrente) return;
    const precedente = trovaStepValido(configCorrente.steps, stepCorrente - 1);
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
