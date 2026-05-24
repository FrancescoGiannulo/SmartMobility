from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from controllers.schemas import MezzoMappaOut, ZonaOut

router = APIRouter(prefix="/ap", tags=["Mappa AP"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Tutti i mezzi con posizione per la Mappa AP."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


@router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Zone attive per la Mappa AP."""
    return ServizioGIS(db).ottieni_zone()
