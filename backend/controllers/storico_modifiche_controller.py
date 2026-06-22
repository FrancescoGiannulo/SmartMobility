from fastapi import APIRouter, Depends
from bll.servizio_storico_modifiche import ServizioStoricoModifiche
from middleware.auth_middleware import verify_token
from controllers.schemas import StoricoModificaOut

# [IF-OP.13] StoricoModificheController
router = APIRouter(prefix="/operatore", tags=["Storico Modifiche"])
_servizio = ServizioStoricoModifiche()


@router.get("/storico-modifiche", response_model=list[StoricoModificaOut])
def get_storico(_op: dict = Depends(verify_token(["OP"]))):
    """[IF-OP.13] Mostra Storico Modifiche."""
    return _servizio.get_storico()
