from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from bll.servizio_mobilita import ServizioMobilita, SegnalazioneNonTrovata
from controllers.schemas import MezzoMappaOut, SegnalazioneOut

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


# [IF-OP.08] Gestisce Segnalazione
@router.get("/segnalazioni", response_model=list[SegnalazioneOut])
def lista_segnalazioni(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    return ServizioMobilita(db).get_segnalazioni()


@router.get("/segnalazioni/{segnalazione_id}", response_model=SegnalazioneOut)
def dettaglio_segnalazione(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    try:
        return ServizioMobilita(db).get_dettaglio_segnalazione(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/segnalazioni/{segnalazione_id}/stato", response_model=SegnalazioneOut)
def prendi_in_carico(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    try:
        return ServizioMobilita(db).prendi_in_carico(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
