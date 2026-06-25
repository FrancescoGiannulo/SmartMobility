from dataclasses import dataclass
from datetime import datetime
from .persona import Persona


@dataclass
class Utente(Persona):
    cognome: str = ""
    sospeso: bool = False
    motivazione_sospensione: str | None = None
    sospensione_fine: datetime | None = None
    contatore_parcheggi_corretti: int = 0
    credito_bonus: float = 0.0

    def ruolo_atteso(self) -> str:
        return "UT"
