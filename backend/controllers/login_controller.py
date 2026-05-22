from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from bll.servizio_utenti import (
    ServizioUtenti,
    CredenzialNonValideException,
    AccountBloccatoException,
    AccountSospesoException,
    ServizioAuthException,
)
from middleware.auth_middleware import verify_token
from controllers.schemas import LoginRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])
_servizio = ServizioUtenti()


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest):
    """[IF-UT.18 / IF-OP.16 / IF-AP.07]"""
    try:
        return _servizio.autentica_account(body.email, body.password)
    except AccountBloccatoException as e:
        raise HTTPException(status_code=423, detail=str(e))
    except AccountSospesoException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except CredenzialNonValideException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ServizioAuthException as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/me")
def me(utente_corrente: dict = Depends(verify_token())):
    """Restituisce profilo e ruolo dell'utente autenticato."""
    return _servizio.profilo_corrente(
        UUID(str(utente_corrente["id"])),
        utente_corrente["email"],
    )
