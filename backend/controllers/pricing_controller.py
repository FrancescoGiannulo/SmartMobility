from fastapi import APIRouter, Depends, HTTPException, Response
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_pricing import ServizioPricing
from controllers.schemas import TariffaOut, PromozioneOut

router = APIRouter(tags=["Pricing"])

# Variabile a livello modulo: permette dependency_overrides nei test
_auth_utente = verify_token(["UT"])


# [IF-UT.05] Consulta Tariffe
@router.get("/tariffe", response_model=list[TariffaOut])
def get_tariffe(
    utente=Depends(_auth_utente),
    db=Depends(get_db),
):
    tariffe = ServizioPricing(db).getTariffe()
    if not tariffe:
        raise HTTPException(status_code=404, detail="Nessuna tariffa disponibile.")
    return tariffe


# [IF-UT.13] Visualizza Promozioni
@router.get("/promozioni", status_code=200)
def get_promozioni(
    response: Response,
    utente=Depends(_auth_utente),
    db=Depends(get_db),
):
    promozioni = ServizioPricing(db).getPromozioniAttive()
    if not promozioni:
        response.status_code = 204
        return None
    return promozioni
