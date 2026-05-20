from pydantic import BaseModel
from enum import Enum

class TipoZona(str, Enum):
    operativa = "ZonaOperativa"
    parcheggio = "ZonaParcheggio"
    limitata = "ZonaLimitata"
    vietata = "ZonaVietata"

class Zona(BaseModel):
    pass
