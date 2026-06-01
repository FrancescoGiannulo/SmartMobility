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


class PrenotazioneRequest(BaseModel):
    mezzo_id: UUID


class TariffaOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    costo_al_minuto: str
    costo_al_km: str


class PromozioneOut(BaseModel):
    id: UUID
    titolo: str
    descrizione: str | None
    sconto_percentuale: str
    data_fine: str
