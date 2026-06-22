import { useContext } from 'react';
import { TourContext } from './TourProvider';
import type { TourContextValue } from './types';

export function useTour(): TourContextValue {
  const ctx = useContext(TourContext);
  if (!ctx) throw new Error('useTour must be used within TourProvider');
  return ctx;
}
