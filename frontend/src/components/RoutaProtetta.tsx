import React from 'react'
import { Navigate } from 'react-router-dom'
import { utenteCorrente } from '../services/AuthService'

interface Props {
  ruoloRichiesto: 'UT' | 'OP' | 'AP'
  children: React.ReactNode
}

export default function RoutaProtetta({ ruoloRichiesto, children }: Props) {
  const utente = utenteCorrente()
  if (!utente) return <Navigate to="/" replace />
  if (utente.ruolo !== ruoloRichiesto) return <Navigate to="/non-autorizzato" replace />
  return <>{children}</>
}
