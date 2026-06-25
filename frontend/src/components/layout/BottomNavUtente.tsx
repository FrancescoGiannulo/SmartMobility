// [IF-UT.01, IF-UT.03, IF-UT.09, IF-UT.11, IF-UT.13] Guscio navigazione utente
import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import './BottomNavUtente.css';

function IconMappa() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21" />
      <line x1="9" y1="3" x2="9" y2="18" />
      <line x1="15" y1="6" x2="15" y2="21" />
    </svg>
  );
}

function IconStorico() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function IconAbbonamenti() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
      <line x1="1" y1="10" x2="23" y2="10" />
    </svg>
  );
}

function IconProfilo() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}

interface NavItemProps {
  to: string;
  label: string;
  icon: React.ReactNode;
  exact?: boolean;
  currentPath: string;
}

function NavItem({ to, label, icon, exact = false, currentPath }: NavItemProps) {
  const isActive = exact ? currentPath === to : currentPath.startsWith(to);
  return (
    <Link
      to={to}
      className={'sm-bottom-nav__item' + (isActive ? ' sm-bottom-nav__item--active' : '')}
      aria-current={isActive ? 'page' : undefined}
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}

export default function BottomNavUtente(): React.JSX.Element {
  const { pathname } = useLocation();

  return (
    <nav className="sm-bottom-nav" aria-label="Navigazione principale">
      <NavItem
        to="/utente/home"
        label="Mappa"
        icon={<IconMappa />}
        exact
        currentPath={pathname}
      />
      <NavItem
        to="/utente/storico"
        label="Storico"
        icon={<IconStorico />}
        currentPath={pathname}
      />
      <NavItem
        to="/utente/abbonamenti"
        label="Abbonamenti"
        icon={<IconAbbonamenti />}
        currentPath={pathname}
      />
      <NavItem
        to="/utente/profilo"
        label="Profilo"
        icon={<IconProfilo />}
        currentPath={pathname}
      />
    </nav>
  );
}
