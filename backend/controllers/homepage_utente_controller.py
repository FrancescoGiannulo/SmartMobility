from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from bll.servizio_gis import ServizioGIS
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import MezzoMappaOut, ZonaOut

router = APIRouter(prefix="/utente", tags=["Homepage Utente"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Mezzi disponibili per la Mappa Utente."""
    return ServizioGIS(db).ottieni_mezzi_utente()


@router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_utente(
    _=Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[CS-01 / UT.01] Zone attive per la Mappa Utente."""
    return ServizioGIS(db).ottieni_zone()
