from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from middleware.auth_middleware import verify_token
from bll.servizio_pricing import (
    ServizioPricing,
    MetodoNonTrovato,
    MetodoDuplicato,
    DatiNonValidi,
    NessunMetodoPredefinito,
    PagamentoRifiutato,
    TariffaNonTrovata,
)
from controllers.schemas import (
    AggiungiMetodoRequest,
    EffettuaPagamentoRequest,
    MetodoPagamentoResponse,
)

router = APIRouter(prefix="/utente/pagamenti", tags=["Pagamenti"])
_servizio = ServizioPricing()


# [IF-UT.12] Lista metodi di pagamento salvati
@router.get("/metodi", response_model=list[MetodoPagamentoResponse])
def lista_metodi(utente: dict = Depends(verify_token(required_roles=["UT"]))):
    return _servizio.lista_metodi(UUID(str(utente["id"])))


# [IF-UT.12] Aggiungi metodo di pagamento
@router.post("/metodi", response_model=MetodoPagamentoResponse, status_code=status.HTTP_201_CREATED)
def aggiungi_metodo(
    body: AggiungiMetodoRequest,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    dati = {}
    if body.last_four:
        dati["last_four"] = body.last_four
    try:
        return _servizio.aggiungi_metodo(UUID(str(utente["id"])), body.tipo, dati)
    except DatiNonValidi as e:
        raise HTTPException(status_code=422, detail=str(e))
    except MetodoDuplicato as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-UT.21] Imposta metodo di pagamento predefinito
@router.put("/metodi/{metodo_id}/predefinito", status_code=status.HTTP_200_OK)
def imposta_predefinito(
    metodo_id: UUID,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    try:
        _servizio.imposta_predefinito(metodo_id, UUID(str(utente["id"])))
    except MetodoNonTrovato as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"detail": "Metodo impostato come predefinito"}


# [IF-UT.12] Rimuovi metodo di pagamento
@router.delete("/metodi/{metodo_id}", status_code=status.HTTP_204_NO_CONTENT)
def rimuovi_metodo(
    metodo_id: UUID,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    try:
        _servizio.rimuovi_metodo(metodo_id, UUID(str(utente["id"])))
    except MetodoNonTrovato as e:
        raise HTTPException(status_code=404, detail=str(e))


# [IF-UT.20] Effettua pagamento a fine corsa
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def effettua_pagamento(
    body: EffettuaPagamentoRequest,
    utente: dict = Depends(verify_token(required_roles=["UT"])),
):
    try:
        return _servizio.effettua_pagamento(
            corsa_id=UUID(body.corsa_id),
            utente_id=UUID(str(utente["id"])),
            tipo_mezzo=body.tipo_mezzo,
            durata_min=body.durata_min,
            distanza_km=body.distanza_km,
            offerta_id=UUID(body.offerta_id) if body.offerta_id else None,
        )
    except NessunMetodoPredefinito as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TariffaNonTrovata as e:
        raise HTTPException(status_code=500, detail=str(e))
    except PagamentoRifiutato as e:
        raise HTTPException(status_code=402, detail=str(e))
