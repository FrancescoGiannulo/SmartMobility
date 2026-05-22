from pydantic import BaseModel


class RegistrazioneRequest(BaseModel):
    email: str
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
