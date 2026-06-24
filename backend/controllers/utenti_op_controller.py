from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from bll.servizio_utenti import ServizioUtenti
from dal.attore_repository import AttoreNonTrovatoException, AccountGiaSospesoException
from middleware.auth_middleware import verify_token
from controllers.schemas import UtenteListItemOut, UtenteDettaglioOut, SospensioneRequest

# [IF-OP.09] UtentiOPController
router = APIRouter(prefix="/operatore", tags=["Gestione Utenti Operatore"])
_servizio = ServizioUtenti()


@router.get("/utenti", response_model=list[UtenteListItemOut])
def lista_utenti(_=Depends(verify_token(["OP"]))):
    """[IF-OP.09] Elenco di tutti gli Utenti registrati."""
    return _servizio.get_utenti()


@router.get("/utenti/{utente_id}", response_model=UtenteDettaglioOut)
def dettaglio_utente(utente_id: UUID, _=Depends(verify_token(["OP"]))):
    """[IF-OP.09] Dettaglio del profilo di un Utente."""
    try:
        return _servizio.get_dettaglio_utente(utente_id)
    except AttoreNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/utenti/{utente_id}/stato", response_model=UtenteDettaglioOut)
def sospendi_account(
    utente_id: UUID,
    body: SospensioneRequest,
    _=Depends(verify_token(["OP"])),
):
    """[IF-OP.09] Sospende l'account di un Utente, con motivazione."""
    try:
        _servizio.sospendi_account(utente_id, body.motivazione, body.durata_giorni)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AccountGiaSospesoException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except AttoreNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _servizio.get_dettaglio_utente(utente_id)
