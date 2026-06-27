// [IF-OP.01–IF-OP.11, IF-AP.01–IF-AP.03] Guscio navigazione operatore/AP
import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import './SidebarRuolo.css';

/* ── Icone decorative ── */
function IconMappa() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21" />
      <line x1="9" y1="3" x2="9" y2="18" />
      <line x1="15" y1="6" x2="15" y2="21" />
    </svg>
  );
}

function IconMezzi() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <circle cx="12" cy="12" r="9" />
      <line x1="12" y1="3" x2="12" y2="1" />
      <line x1="12" y1="23" x2="12" y2="21" />
      <line x1="3" y1="12" x2="1" y2="12" />
      <line x1="23" y1="12" x2="21" y2="12" />
    </svg>
  );
}

function IconTariffe() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="12" y1="1" x2="12" y2="23" />
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
    </svg>
  );
}

function IconOfferte() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" />
      <line x1="7" y1="7" x2="7.01" y2="7" />
    </svg>
  );
}

function IconRegole() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function IconSegnalazioni() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}

function IconUtenti() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function IconRecensioni() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

function IconParametri() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.07 4.93l-1.41 1.41M5.34 18.66l-1.41 1.41M20 12h2M2 12h2M19.07 19.07l-1.41-1.41M5.34 5.34 3.93 3.93" />
      <path d="M4.22 4.22a10 10 0 1 0 15.56 0" />
    </svg>
  );
}

function IconStorico() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="12 8 12 12 14 14" />
      <path d="M3.05 11a9 9 0 1 0 .5-3" />
      <polyline points="3 4 3 11 10 11" />
    </svg>
  );
}

function IconDashboard() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="3" width="7" height="7" />
      <rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" />
      <rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}

function IconReport() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  );
}

/* ── Definizioni voci per ruolo ── */
interface NavVoce {
  label: string;
  to: string;
  icon: React.ReactNode;
}

const VOCI_OP: NavVoce[] = [
  { label: 'Mappa flotta',      to: '/operatore/dashboard',          icon: <IconMappa /> },
  { label: 'Mezzi',             to: '/operatore/mezzi',              icon: <IconMezzi /> },
  { label: 'Tariffe',           to: '/operatore/tariffe',            icon: <IconTariffe /> },
  { label: 'Offerte',           to: '/operatore/offerte',            icon: <IconOfferte /> },
  { label: 'Regole & Zone',     to: '/operatore/impostazioni-regole',icon: <IconRegole /> },
  { label: 'Segnalazioni',      to: '/operatore/segnalazioni',       icon: <IconSegnalazioni /> },
  { label: 'Utenti',            to: '/operatore/utenti',             icon: <IconUtenti /> },
  { label: 'Recensioni',        to: '/operatore/recensioni',         icon: <IconRecensioni /> },
  { label: 'Parametri',         to: '/operatore/parametri-sistema',  icon: <IconParametri /> },
  { label: 'Storico modifiche', to: '/operatore/storico-modifiche',  icon: <IconStorico /> },
];

const VOCI_AP: NavVoce[] = [
  { label: 'Dashboard', to: '/ap/dashboard', icon: <IconDashboard /> },
  { label: 'Report',    to: '/ap/report',    icon: <IconReport /> },
];

/* ── Componente ── */
export default function SidebarRuolo({ ruolo }: { ruolo: 'OP' | 'AP' }): React.JSX.Element {
  const { pathname } = useLocation();
  const voci = ruolo === 'OP' ? VOCI_OP : VOCI_AP;

  return (
    <nav className="sm-sidebar" aria-label={ruolo === 'OP' ? 'Navigazione operatore' : 'Navigazione amministrazione'}>
      {voci.map(({ label, to, icon }) => {
        const isActive = pathname === to || pathname.startsWith(to + '/');
        return (
          <Link
            key={to}
            to={to}
            className={'sm-sidebar__item' + (isActive ? ' sm-sidebar__item--active' : '')}
            aria-current={isActive ? 'page' : undefined}
          >
            {icon}
            <span>{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
