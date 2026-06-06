import uuid
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import CreaOffertaRequest, ModificaOffertaRequest, OffertaOut
from bll.servizio_offerte import ServizioOfferta, OffertaValidazioneException, OffertaDuplicataException

router = APIRouter(prefix="/operatore", tags=["Operatore - Offerte"])
_servizio = ServizioOfferta()


# [IF-OP.06] — lista offerte
@router.get("/offerte", response_model=list[OffertaOut])
def lista_offerte(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.lista_offerte(db)


# [IF-OP.06] — crea offerta
@router.post("/offerte", response_model=OffertaOut, status_code=201)
def crea_offerta(
    body: CreaOffertaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.crea_offerta(
            nome=body.nome,
            tipo=body.tipo,
            descrizione=body.descrizione,
            sconto_percentuale=body.sconto_percentuale,
            prezzo=body.prezzo,
            durata_giorni=body.durata_giorni,
            data_inizio=body.data_inizio,
            data_scadenza=body.data_scadenza,
            db=db,
            tipo_mezzo=body.tipo_mezzo,
        )
    except OffertaDuplicataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.06] — modifica offerta
@router.patch("/offerte/{offerta_id}", response_model=OffertaOut)
def modifica_offerta(
    offerta_id: uuid.UUID,
    body: ModificaOffertaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.modifica_offerta(
            offerta_id=offerta_id,
            db=db,
            nome=body.nome,
            descrizione=body.descrizione,
            sconto_percentuale=body.sconto_percentuale,
            prezzo=body.prezzo,
            durata_giorni=body.durata_giorni,
            data_inizio=body.data_inizio,
            data_scadenza=body.data_scadenza,
            stato=body.stato,
            tipo_mezzo=body.tipo_mezzo,
        )
    except OffertaDuplicataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.06] — elimina offerta
@router.delete("/offerte/{offerta_id}", status_code=204)
def elimina_offerta(
    offerta_id: uuid.UUID,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        _servizio.elimina_offerta(offerta_id, db)
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=404, detail=str(e))
