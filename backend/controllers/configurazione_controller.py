from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import ParametriSistemaRequest, ParametriSistemaOut
from bll.servizio_parametri import ServizioParametri, ParametriValidazioneException

router = APIRouter(prefix="/operatore", tags=["Operatore - Configurazione"])
_servizio = ServizioParametri()


# [CS-15 / IF-OP.08/09/10/14] — leggi parametri correnti
@router.get("/configurazione/parametri", response_model=ParametriSistemaOut)
def get_parametri(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.get_parametri(db)


# [CS-15 / IF-OP.08/09/10/14] — aggiorna parametri
@router.put("/configurazione/parametri", response_model=ParametriSistemaOut)
def aggiorna_parametri(
    body: ParametriSistemaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.aggiorna_parametri(
            durata_max_prenotazione_min=body.durata_max_prenotazione_min,
            durata_periodo_grazia_min=body.durata_periodo_grazia_min,
            max_mezzi_per_utente=body.max_mezzi_per_utente,
            addebito_pausa_min=body.addebito_pausa_min,
            db=db,
        )
    except ParametriValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))
