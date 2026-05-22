from dataclasses import dataclass
from .persona import Persona


@dataclass
class AmministrazionePubblica(Persona):

    def ruolo_atteso(self) -> str:
        return "AP"
