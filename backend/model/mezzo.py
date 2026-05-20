from pydantic import BaseModel
from enum import Enum

class StatoMezzo(str, Enum):
    disponibile = "Disponibile"
    prenotato = "Prenotato"
    in_uso = "In uso"
    in_pausa = "In pausa"
    in_manutenzione = "In manutenzione"
    fuori_servizio = "Fuori servizio"
    dismesso = "Dismesso"

class Mezzo(BaseModel):
    pass
