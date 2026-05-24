from pydantic import BaseModel, EmailStr


class RegistrazioneRequest(BaseModel):
    email: EmailStr
    password: str
    nome: str
    cognome: str


class LoginRequest(BaseModel):
    email: EmailStr
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
