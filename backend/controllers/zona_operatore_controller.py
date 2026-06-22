from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_mappa import ServizioMappa, PoligonoNonValidoException, PoligonoFuoriZonaOperativaException
from dal.zona_repository import ZonaNonTrovataException
from controllers.schemas import ZonaOut, ZonaCreate

router = APIRouter(prefix="/operatore/zone", tags=["Zone Operatore"])


@router.get("", response_model=list[ZonaOut])
def lista_zone(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Lista zone attive."""
    return ServizioMappa(db).ottieni_zone()


@router.post("", response_model=ZonaOut, status_code=201)
def crea_zona(
    body: ZonaCreate,
    _op=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03 / OP.03 / OP.15 / OP.16] Crea una nuova zona."""
    try:
        return ServizioMappa(db).crea_zona(
            body.nome, body.tipo, body.coordinate, body.limite_velocita,
            operatore_id=UUID(str(_op["id"])),
        )
    except (PoligonoNonValidoException, PoligonoFuoriZonaOperativaException) as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{zona_id}", status_code=204)
def elimina_zona(
    zona_id: UUID,
    _op=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-03] Elimina zona."""
    try:
        ServizioMappa(db).elimina_zona(zona_id, operatore_id=UUID(str(_op["id"])))
    except ZonaNonTrovataException as e:
        raise HTTPException(status_code=404, detail=str(e))
