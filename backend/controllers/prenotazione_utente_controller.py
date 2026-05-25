from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import PrenotazioneRequest
from bll.servizio_mobilita import (
    ServizioMobilita,
    MezzoNonTrovatoException,
    MezzoNonDisponibileException,
    CorsaNonTrovataException,
)
from bll.servizio_prenotazione import (
    ServizioPrenotazione,
    MezzoNonTrovatoException as PrenMezzoNonTrovato,
    MezzoNonDisponibileException as PrenMezzoNonDisponibile,
)

router = APIRouter(prefix="/utente", tags=["Utente - Corsa"])

# [IF-UT.02] CS-XX — Prenota Mezzo
@router.post("/prenotazioni", status_code=201)
def prenota_mezzo(
    body: PrenotazioneRequest,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        pren = ServizioPrenotazione(db).crea_prenotazione(body.mezzo_id, utente["id"])
        return pren
    except PrenMezzoNonTrovato:
        raise HTTPException(status_code=404, detail="Mezzo non trovato")
    except PrenMezzoNonDisponibile as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-UT.04] CS-10 Sblocca Mezzo
@router.post("/mezzi/{mezzo_id}/sblocca", status_code=201)
def sblocca_mezzo(
    mezzo_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        corsa = ServizioMobilita(db).sblocca_mezzo(mezzo_id, utente["id"])
        return corsa
    except MezzoNonTrovatoException:
        raise HTTPException(status_code=404, detail="Mezzo non trovato")
    except MezzoNonDisponibileException as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-UT.06] CS-11 Termina Corsa (minimale)
@router.post("/corse/{corsa_id}/termina", status_code=200)
def termina_corsa(
    corsa_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        ServizioMobilita(db).termina_corsa(corsa_id, utente["id"])
        return {"status": "ok"}
    except CorsaNonTrovataException:
        raise HTTPException(status_code=404, detail="Corsa non trovata")
