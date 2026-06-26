from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from bll.servizio_segnalazione import ServizioSegnalazione, SegnalazioneNonTrovata, TransizioneNonValida
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import SegnalazioneOut

# [IF-OP.08] SegnalazioneOPController
router = APIRouter(prefix="/operatore", tags=["Segnalazioni Operatore"])


@router.get("/segnalazioni", response_model=list[SegnalazioneOut])
def lista_segnalazioni(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[IF-OP.08] Lista di tutte le segnalazioni."""
    return ServizioSegnalazione(db).get_segnalazioni()


@router.get("/segnalazioni/{segnalazione_id}", response_model=SegnalazioneOut)
def dettaglio_segnalazione(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[IF-OP.08] Dettaglio di una segnalazione."""
    try:
        return ServizioSegnalazione(db).get_dettaglio_segnalazione(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/segnalazioni/{segnalazione_id}/prendi-in-carico", response_model=SegnalazioneOut)
def prendi_in_carico(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[IF-OP.08] Prendi in carico una segnalazione."""
    try:
        return ServizioSegnalazione(db).prendi_in_carico(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/segnalazioni/{segnalazione_id}/risolvi", response_model=SegnalazioneOut)
def risolvi_segnalazione(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[IF-OP.08] Segna una segnalazione come risolta."""
    try:
        return ServizioSegnalazione(db).risolvi(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TransizioneNonValida as e:
        raise HTTPException(status_code=422, detail=str(e))
