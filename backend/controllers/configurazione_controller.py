from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import ParametriSistemaRequest, ParametriSistemaOut
from bll.servizio_parametri import ServizioParametri, ParametriValidazioneException
from dal.attore_repository import AttoreRepository

router = APIRouter(prefix="/operatore", tags=["Operatore - Configurazione"])
_servizio = ServizioParametri()

router_sicurezza = APIRouter(prefix="/op/configurazione", tags=["Configurazione Sicurezza"])
_repo = AttoreRepository()


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
            operatore_id=UUID(str(_op["id"])),
        )
    except ParametriValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


class ConfigurazioneSicurezzaOut(BaseModel):
    lockout_window_min: int
    max_tentativi: int


class ConfigurazioneSicurezzaUpdate(BaseModel):
    lockout_window_min: int | None = Field(
        default=None,
        gt=0,
        le=1440,
        description="Finestra di lockout in minuti (1–1440). Null = non modificare.",
    )
    max_tentativi: int | None = Field(
        default=None,
        gt=0,
        le=20,
        description="Numero massimo di tentativi falliti (1–20). Null = non modificare.",
    )


@router_sicurezza.get("/sicurezza", response_model=ConfigurazioneSicurezzaOut)
def leggi_config_sicurezza(
    _=Depends(verify_token(["OP"])),
):
    """[IIN-2] Legge la configurazione di sicurezza corrente (finestra lockout, max tentativi)."""
    return _repo.leggi_config_sicurezza()


@router_sicurezza.patch("/sicurezza", response_model=ConfigurazioneSicurezzaOut)
def aggiorna_config_sicurezza(
    body: ConfigurazioneSicurezzaUpdate,
    _=Depends(verify_token(["OP"])),
):
    """[IIN-2] Aggiorna la configurazione di sicurezza."""
    if body.lockout_window_min is None and body.max_tentativi is None:
        raise HTTPException(
            status_code=422,
            detail="Specificare almeno uno dei campi: lockout_window_min, max_tentativi",
        )
    return _repo.aggiorna_config_sicurezza(body.lockout_window_min, body.max_tentativi)
