import uuid
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import AbbonamentoOut, OffertaOut
from bll.servizio_abbonamento import (
    ServizioAbbonamento,
    OffertaNonValida,
    NessunMetodoPagamento,
    PagamentoRifiutato,
)

router = APIRouter(prefix="/utente", tags=["Utente - Abbonamenti"])
_servizio = ServizioAbbonamento()


# [IF-UT.16] — piani abbonamento disponibili
@router.get("/abbonamenti/piani", response_model=list[OffertaOut])
def get_piani(
    _ut=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return _servizio.get_piani_disponibili(db)


# [IF-UT.16] — abbonamento attivo dell'utente
@router.get("/abbonamenti/corrente", response_model=AbbonamentoOut | None)
def get_corrente(
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return _servizio.get_abbonamento_attivo(utente["sub"], db)


# [IF-UT.16] — sottoscrivi piano
@router.post("/abbonamenti/{offerta_id}", response_model=AbbonamentoOut, status_code=201)
def sottoscrivi(
    offerta_id: uuid.UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        return _servizio.sottoscrivi(
            utente_id=uuid.UUID(utente["sub"]),
            offerta_id=offerta_id,
            db=db,
        )
    except OffertaNonValida as e:
        detail = str(e)
        status = 404 if "non trovata" in detail else 422
        raise HTTPException(status_code=status, detail=detail)
    except NessunMetodoPagamento as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PagamentoRifiutato as e:
        raise HTTPException(status_code=402, detail=str(e))
