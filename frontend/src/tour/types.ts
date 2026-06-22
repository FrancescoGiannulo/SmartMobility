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
