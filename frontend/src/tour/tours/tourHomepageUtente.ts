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
      target: 'mezzo-mappa',
      tooltipPosition: 'bottom',
      titolo: 'Seleziona un mezzo',
      testo: 'Tocca un\'icona sulla mappa per selezionare un mezzo. Si aprirà un pannello con i dettagli e le azioni disponibili.',
    },
    {
      type: 'spotlight',
      target: 'btn-prenota',
      tooltipPosition: 'top',
      titolo: 'Prenota',
      testo: 'Premi qui per prenotare il mezzo. Avrai un tempo limitato per raggiungere il mezzo e sbloccarlo.',
    },
    {
      type: 'spotlight',
      target: 'btn-sblocca',
      tooltipPosition: 'top',
      titolo: 'Sblocca',
      testo: 'Se sei già vicino al mezzo, puoi sbloccarlo direttamente senza prenotare. La corsa parte subito.',
    },
    {
      type: 'spotlight',
      target: 'btn-sidebar',
      tooltipPosition: 'bottom',
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
      testo: 'Ora sai come funziona. Seleziona un mezzo sulla mappa per iniziare! Se vorrai rivedere questo tour, premi il pulsante "?" in basso a sinistra.',
      ctaLabel: 'Inizia',
    },
  ],
};
