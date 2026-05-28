from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from bll.servizio_pricing import ServizioPricing, TariffaGiaEsistente
from controllers.schemas import MezzoMappaOut, CreaTariffaRequest, TariffaResponse

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])
_pricing = ServizioPricing()


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


# [IF-OP.07] Definisce Tariffa
@router.get("/tariffe", response_model=list[TariffaResponse])
def lista_tariffe(_=Depends(verify_token(["OP"]))):
    return _pricing.get_tariffe()


@router.post("/tariffe", response_model=TariffaResponse, status_code=status.HTTP_201_CREATED)
def crea_tariffa(
    body: CreaTariffaRequest,
    _=Depends(verify_token(["OP"])),
):
    try:
        return _pricing.crea_tariffa(body.tipo_mezzo, body.costo_al_minuto, body.costo_al_km)
    except TariffaGiaEsistente as e:
        raise HTTPException(status_code=409, detail=str(e))
