from pydantic import BaseModel, EmailStr
from typing import Any
from uuid import UUID


class RegistrazioneRequest(BaseModel):
    email: EmailStr
    password: str
    nome: str
    cognome: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    ruolo: str
    profilo: dict


class AggiungiMetodoRequest(BaseModel):
    tipo: str
    last_four: str | None = None


class EffettuaPagamentoRequest(BaseModel):
    corsa_id: str
    tipo_mezzo: str
    durata_min: float
    distanza_km: float


class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool


class MezzoMappaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float
    lng: float
    batteria: int | None


class ZonaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    perimetro: dict[str, Any]
    limite_velocita: int | None
    attiva: bool


class ZonaCreate(BaseModel):
    nome: str
    tipo: str
    coordinate: list[list[float]]
    limite_velocita: int | None = None


class CreaTariffaRequest(BaseModel):
    tipo_mezzo: str
    costo_al_minuto: float
    costo_al_km: float


class TariffaResponse(BaseModel):
    id: str
    tipo_mezzo: str
    costo_al_minuto: float
    costo_al_km: float


class PrenotazioneRequest(BaseModel):
    mezzo_id: UUID
