from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()
