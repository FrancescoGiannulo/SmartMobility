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
