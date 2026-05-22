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
