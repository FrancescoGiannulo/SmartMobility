from fastapi import APIRouter, HTTPException, Depends, Response
from bll.servizio_utenti import (
    ServizioUtenti,
    EmailGiaRegistrataException,
    ServizioAuthException,
)
from controllers.schemas import RegistrazioneRequest, AuthResponse
from middleware.auth_middleware import verify_token

router = APIRouter(prefix="/auth", tags=["auth"])
_servizio = ServizioUtenti()


@router.post("/registra", response_model=AuthResponse, status_code=201)
def registra(body: RegistrazioneRequest):
    """[IF-UT.17]"""
    if len(body.password) < 8:
        raise HTTPException(status_code=422, detail="Password minimo 8 caratteri")
    if not body.nome.strip() or not body.cognome.strip():
        raise HTTPException(status_code=422, detail="Nome e cognome obbligatori")
    # [IIN-2 / GDPR art. 7] Il consenso esplicito al trattamento dati è obbligatorio
    if not body.consenso_privacy:
        raise HTTPException(
            status_code=422,
            detail="Il consenso al trattamento dei dati personali è obbligatorio per la registrazione",
        )
    try:
        return _servizio.registra_account(body.email, body.password, body.nome, body.cognome)
    except EmailGiaRegistrataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ServizioAuthException as e:
        raise HTTPException(status_code=502, detail=str(e))


from sqlalchemy.orm import Session
from database import get_db
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


# ── GDPR ─────────────────────────────────────────────────────────────────────

gdpr_router = APIRouter(prefix="/utente", tags=["GDPR"])


@gdpr_router.get("/dati-personali")
def esporta_dati_personali(
    utente_corrente: dict = Depends(verify_token(["UT"])),
):
    """[IIN-2 / GDPR art. 20] Esporta i dati personali dell'utente autenticato in formato JSON
    (portabilità dei dati).
    """
    try:
        return _servizio.esporta_dati(utente_corrente["id"], utente_corrente["email"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@gdpr_router.delete("/account", status_code=204)
def cancella_account(
    utente_corrente: dict = Depends(verify_token(["UT"])),
):
    """[IIN-2 / GDPR art. 17] Cancella definitivamente l'account e tutti i dati personali
    dell'utente autenticato (diritto all'oblio).
    """
    try:
        _servizio.cancella_account(utente_corrente["id"])
    except ServizioAuthException as e:
        raise HTTPException(status_code=502, detail=str(e))
    return Response(status_code=204)
