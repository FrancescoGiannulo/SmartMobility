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


from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut, ZonaOut

mappa_router = APIRouter(prefix="/utente", tags=["Mappa Utente"])


@mappa_router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Mezzi disponibili per la Mappa Utente."""
    return ServizioGIS(db).ottieni_mezzi_utente()


@mappa_router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Zone attive per la Mappa Utente."""
    return ServizioGIS(db).ottieni_zone()
