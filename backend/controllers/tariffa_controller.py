from fastapi import APIRouter, Depends, HTTPException, status
from middleware.auth_middleware import verify_token
from bll.servizio_tariffa import ServizioTariffa, TariffaGiaEsistente, TariffaNonTrovata
from controllers.schemas import CreaTariffaRequest, TariffaResponse

router = APIRouter(prefix="/operatore", tags=["Tariffe"])
_servizio = ServizioTariffa()


# [IF-OP.07] Definisce Tariffa
@router.get("/tariffe", response_model=list[TariffaResponse])
def lista_tariffe(_=Depends(verify_token(["OP"]))):
    return _servizio.get_tariffe()


@router.post("/tariffe", response_model=TariffaResponse, status_code=status.HTTP_201_CREATED)
def crea_tariffa(
    body: CreaTariffaRequest,
    _=Depends(verify_token(["OP"])),
):
    try:
        return _servizio.crea_tariffa(body.tipo_mezzo, body.costo_al_minuto, body.costo_al_km)
    except TariffaGiaEsistente as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-OP.08] Modifica Tariffa
@router.put("/tariffe/{tipo_mezzo}", response_model=TariffaResponse)
def aggiorna_tariffa(
    tipo_mezzo: str,
    body: CreaTariffaRequest,
    _=Depends(verify_token(["OP"])),
):
    try:
        return _servizio.aggiorna_tariffa(tipo_mezzo, body.costo_al_minuto, body.costo_al_km)
    except TariffaNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
