from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from bll.servizio_segnalazione import ServizioSegnalazione
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import InviaSegnalazioneRequest, SegnalazioneOut

# [IF-UT.12] SegnalazioneUtenteController
router = APIRouter(prefix="/utente", tags=["Segnalazioni Utente"])


@router.get("/segnalazioni", response_model=list[SegnalazioneOut])
def mie_segnalazioni(
    utente: dict = Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[IF-UT.12] Le mie segnalazioni."""
    return ServizioSegnalazione(db).get_mie_segnalazioni(UUID(str(utente["id"])))


@router.post("/segnalazioni", response_model=SegnalazioneOut, status_code=201)
def invia_segnalazione(
    body: InviaSegnalazioneRequest,
    utente: dict = Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[IF-UT.12] Invia Segnalazione."""
    return ServizioSegnalazione(db).registra_segnalazione(
        UUID(str(utente["id"])), body.tipologia, body.descrizione
    )
