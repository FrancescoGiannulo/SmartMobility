from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from bll.servizio_recensione import (
    ServizioRecensione,
    VotoNonValidoException,
    CorsaNonConclusaException,
)
from middleware.auth_middleware import verify_token
from controllers.schemas import (
    ScriviRecensioneRequest,
    RecensioneOut,
    RecensioniOperatoreOut,
)

# [IF-UT.15] RecensioneController
router = APIRouter(prefix="/utente", tags=["Recensioni"])
# [IF-OP.13] RecensioneController — lato Operatore
router_operatore = APIRouter(prefix="/operatore", tags=["Recensioni"])
_servizio = ServizioRecensione()


@router.get("/recensioni", response_model=list[RecensioneOut])
def mie_recensioni(
    utente: dict = Depends(verify_token(["UT"])),
):
    """[IF-UT.15] Le mie recensioni."""
    return _servizio.get_mie_recensioni(UUID(str(utente["id"])))


@router.post("/recensioni", response_model=RecensioneOut, status_code=201)
def scrivi_recensione(
    body: ScriviRecensioneRequest,
    utente: dict = Depends(verify_token(["UT"])),
):
    """[IF-UT.15] Scrive Recensione."""
    try:
        return _servizio.scrivi_recensione(UUID(str(utente["id"])), body.voto, body.commento)
    except VotoNonValidoException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except CorsaNonConclusaException as e:
        raise HTTPException(status_code=422, detail=str(e))


@router_operatore.get("/recensioni", response_model=RecensioniOperatoreOut)
def get_recensioni(
    _: dict = Depends(verify_token(["OP"])),
):
    """[IF-OP.13] Visualizza Recensioni — elenco recensioni + voto medio."""
    return _servizio.get_recensioni()
