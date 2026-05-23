from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS, PoligonoNonValidoException
from dal.zona_repository import ZonaNonTrovataException
from controllers.schemas import ZonaOut, ZonaCreate

router = APIRouter(prefix="/operatore/zone", tags=["Zone Operatore"])


@router.get("", response_model=list[ZonaOut])
def lista_zone(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Lista zone attive."""
    return ServizioGIS(db).ottieni_zone()


@router.post("", response_model=ZonaOut, status_code=201)
def crea_zona(
    body: ZonaCreate,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Crea una nuova zona."""
    try:
        return ServizioGIS(db).crea_zona(
            body.nome, body.tipo, body.coordinate, body.limite_velocita
        )
    except PoligonoNonValidoException as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{zona_id}", status_code=204)
def elimina_zona(
    zona_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03] Elimina zona."""
    try:
        ServizioGIS(db).elimina_zona(zona_id)
    except ZonaNonTrovataException as e:
        raise HTTPException(status_code=404, detail=str(e))
