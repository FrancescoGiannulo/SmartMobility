from dataclasses import dataclass
from .persona import Persona


@dataclass
class Operatore(Persona):
    durata_max_prenotazione_min: int = 15
    durata_periodo_grazia_min: int = 5
    max_mezzi_per_utente: int = 1

    def ruolo_atteso(self) -> str:
        return "OP"
