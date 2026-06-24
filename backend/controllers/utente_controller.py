from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from bll.servizio_utenti import (
    ServizioUtenti,
    EmailGiaRegistrataException,
    ServizioAuthException,
)
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import RegistrazioneRequest, AuthResponse, ModificaProfiloRequest

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

# ── GDPR ─────────────────────────────────────────────────────────────────────

gdpr_router = APIRouter(prefix="/utente", tags=["GDPR"])


@gdpr_router.put("/profilo")
def modifica_profilo(
    body: ModificaProfiloRequest,
    utente_corrente: dict = Depends(verify_token(["UT"])),
):
    try:
        aggiornato = _servizio.modifica_dati_account(
            utente_corrente["id"], body.nome, body.cognome
        )
        return aggiornato
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@gdpr_router.get("/dati-personali")
def esporta_dati_personali(
    utente_corrente: dict = Depends(verify_token(["UT"])),
):
    """[IIN-2 / GDPR art. 20] Esporta i dati personali dell'utente autenticato in formato JSON."""
    try:
        return _servizio.esporta_dati(utente_corrente["id"], utente_corrente["email"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@gdpr_router.delete("/account", status_code=204)
def cancella_account(
    utente_corrente: dict = Depends(verify_token(["UT"])),
):
    """[IIN-2 / GDPR art. 17] Cancella definitivamente l'account (diritto all'oblio)."""
    try:
        _servizio.cancella_account(utente_corrente["id"])
    except ServizioAuthException as e:
        raise HTTPException(status_code=502, detail=str(e))
    return Response(status_code=204)
