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
