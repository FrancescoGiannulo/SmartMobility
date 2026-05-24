export interface DatoSettimanale {
  giorno: string
  monopattino: number
  bicicletta: number
  automobile: number
}

export interface DatoTorta {
  name: string
  value: number
  colore: string
}

export const DATI_SETTIMANALI: DatoSettimanale[] = [
  { giorno: 'Lun', monopattino: 42, bicicletta: 18, automobile: 12 },
  { giorno: 'Mar', monopattino: 38, bicicletta: 22, automobile: 10 },
  { giorno: 'Mer', monopattino: 35, bicicletta: 20, automobile: 14 },
  { giorno: 'Gio', monopattino: 28, bicicletta: 15, automobile: 8  },
  { giorno: 'Ven', monopattino: 20, bicicletta: 12, automobile: 6  },
  { giorno: 'Sab', monopattino: 15, bicicletta: 10, automobile: 5  },
  { giorno: 'Dom', monopattino: 10, bicicletta: 8,  automobile: 4  },
]

export const DATI_TORTA: DatoTorta[] = [
  { name: 'Monopattino', value: 70.9, colore: '#4caf9a' },
  { name: 'Bicicletta',  value: 13.3, colore: '#2196f3' },
  { name: 'Automobile',  value: 15.8, colore: '#e91e8c' },
]
