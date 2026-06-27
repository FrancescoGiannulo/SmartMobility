from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import RegolaFinecorsaRequest, RegolaFinecorsaOut
from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa, RegolaFinecorsaValidazioneException

router = APIRouter(prefix="/operatore", tags=["Operatore - Regole Fine Corsa"])
_servizio = ServizioRegolaFinecorsa()


# [IF-OP.06] — leggi config corrente
@router.get("/regole-fine-corsa", response_model=RegolaFinecorsaOut | None)
def get_regole(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.get_corrente(db)


# [IF-OP.06] — salva (upsert) config
@router.put("/regole-fine-corsa", response_model=RegolaFinecorsaOut)
def salva_regole(
    body: RegolaFinecorsaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.salva(
            tipo_vincolo=body.tipo_vincolo,
            penale_fuori_zona=body.penale_fuori_zona,
            bonus_parcheggi_corretti=body.bonus_parcheggi_corretti,
            bonus_valore=body.bonus_valore,
            db=db,
            operatore_id=UUID(str(_op["id"])),
        )
    except RegolaFinecorsaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))
