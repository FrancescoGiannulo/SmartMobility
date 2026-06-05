from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from middleware.auth_middleware import verify_token
from dal.attore_repository import AttoreRepository

router = APIRouter(prefix="/op/configurazione", tags=["Configurazione Sicurezza"])
_repo = AttoreRepository()


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


@router.get("/sicurezza", response_model=ConfigurazioneSicurezzaOut)
def leggi_config_sicurezza(
    _=Depends(verify_token(["OP"])),
):
    """[IIN-2] Legge la configurazione di sicurezza corrente (finestra lockout, max tentativi)."""
    return _repo.leggi_config_sicurezza()


@router.patch("/sicurezza", response_model=ConfigurazioneSicurezzaOut)
def aggiorna_config_sicurezza(
    body: ConfigurazioneSicurezzaUpdate,
    _=Depends(verify_token(["OP"])),
):
    """[IIN-2] Aggiorna la configurazione di sicurezza (finestra lockout e/o max tentativi).

    - **lockout_window_min**: minuti entro cui vengono contati i tentativi falliti consecutivi.
    - **max_tentativi**: numero di tentativi falliti che scatena il blocco dell'account.
    """
    if body.lockout_window_min is None and body.max_tentativi is None:
        raise HTTPException(
            status_code=422,
            detail="Specificare almeno uno dei campi: lockout_window_min, max_tentativi",
        )
    return _repo.aggiorna_config_sicurezza(body.lockout_window_min, body.max_tentativi)
