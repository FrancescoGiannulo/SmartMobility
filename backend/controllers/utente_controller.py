from fastapi import APIRouter, HTTPException
from bll.servizio_utenti import (
    ServizioUtenti,
    EmailGiaRegistrataException,
    ServizioAuthException,
)
from controllers.schemas import RegistrazioneRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])
_servizio = ServizioUtenti()


@router.post("/registra", response_model=AuthResponse, status_code=201)
def registra(body: RegistrazioneRequest):
    """[IF-UT.17]"""
    if len(body.password) < 8:
        raise HTTPException(status_code=422, detail="Password minimo 8 caratteri")
    if not body.nome.strip() or not body.cognome.strip():
        raise HTTPException(status_code=422, detail="Nome e cognome obbligatori")
    try:
        return _servizio.registra_account(body.email, body.password, body.nome, body.cognome)
    except EmailGiaRegistrataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ServizioAuthException as e:
        raise HTTPException(status_code=502, detail=str(e))
