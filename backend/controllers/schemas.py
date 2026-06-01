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


class PrenotazioneRequest(BaseModel):
    mezzo_id: UUID


from datetime import datetime
from decimal import Decimal


class CreaOffertaRequest(BaseModel):
    nome: str
    tipo: str  # 'promozione' | 'abbonamento'
    descrizione: str | None = None
    sconto_percentuale: Decimal | None = None
    prezzo: Decimal | None = None
    durata_giorni: int | None = None
    data_inizio: datetime | None = None
    data_scadenza: datetime | None = None


class OffertaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    stato: str
    descrizione: str | None
    sconto_percentuale: Decimal | None
    prezzo: Decimal | None
    durata_giorni: int | None
    data_inizio: datetime | None
    data_scadenza: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
