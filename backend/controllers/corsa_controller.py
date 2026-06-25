from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import (
    PrenotazioneRequest,
    MezzoMappaOut,
    SbloccoRequest,
    MezzoSbloccabileOut,
    RisultatoSblocco,
    Corsa,
    PosizioneDemoRequest,
)
from bll.servizio_mobilita import (
    ServizioMobilita,
    CorsaNonTrovataException,
    CorsaNonInUsaException,
    CorsaNonInPausaException,
)
from bll.servizio_prenotazione import (
    ServizioPrenotazione,
    MezzoNonTrovatoException as PrenMezzoNonTrovato,
    AlcuniMezziNonDisponibiliException,
    MezziFuoriRaggioGruppoException,
    LimiteMezziSuperatoException,
    PrenotazioneNonTrovataException,
)
from dal.parametri_sistema_repository import ParametriSistemaRepository
from controllers.schemas import ParametriSistemaOut
import config
from dal.corsa_repository import CorsaRepository
from bll.servizio_mappa import ServizioMappa

router = APIRouter(prefix="/utente", tags=["Utente - Corsa"])
_parametri_repo = ParametriSistemaRepository()


# [IF-UT.02 / CS-15] — Parametri di sistema visibili all'utente
@router.get("/parametri", response_model=ParametriSistemaOut)
def get_parametri_utente(
    _=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return _parametri_repo.get(db)


# [IF-UT.02] CS-04 — Prenotazioni attive utente (recupero dopo refresh)
@router.get("/prenotazioni/attive")
def get_prenotazioni_attive(
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return ServizioPrenotazione(db).get_prenotazioni_attive(utente["id"])


# [IF-UT.04] CS-05 — Lista mezzi sbloccabili (msg3 diagramma di sequenza)
@router.get("/mezzi/sbloccabili", response_model=list[MezzoSbloccabileOut])
def get_mezzi_sbloccabili(
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return ServizioMobilita(db).get_mezzi_sbloccabili(utente["id"], lat, lng)


# [IF-UT.02] CS-04 — Caratteristiche mezzo (msg3 del diagramma di sequenza)
@router.get("/mezzi/{mezzo_id}", response_model=MezzoMappaOut)
def get_caratteristiche_mezzo(
    mezzo_id: UUID,
    _=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        return ServizioPrenotazione(db).get_caratteristiche(mezzo_id)
    except PrenMezzoNonTrovato:
        raise HTTPException(status_code=404, detail="Mezzo non trovato")


# [IF-UT.02] CS-04 — Prenota uno o più mezzi
@router.post("/prenotazioni", status_code=201)
def prenota_mezzi(
    body: PrenotazioneRequest,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        prenotazioni = ServizioPrenotazione(db).crea_prenotazioni(
            body.mezzo_ids, utente["id"]
        )
        return {"prenotazioni": prenotazioni}
    except PrenMezzoNonTrovato:
        raise HTTPException(status_code=404, detail="Mezzo non trovato")
    except LimiteMezziSuperatoException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AlcuniMezziNonDisponibiliException as e:
        raise HTTPException(
            status_code=409,
            detail={
                "messaggio": "Alcuni mezzi non sono più disponibili",
                "non_disponibili": e.non_disponibili,
            },
        )
    except MezziFuoriRaggioGruppoException as e:
        raise HTTPException(
            status_code=422,
            detail={
                "messaggio": "Alcuni mezzi sono troppo lontani dal primo selezionato",
                "fuori_raggio": e.fuori_raggio,
            },
        )


# [IF-UT.02] CS-XX — Annulla prenotazione
@router.delete("/prenotazioni/{prenotazione_id}", status_code=204)
def annulla_prenotazione(
    prenotazione_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        ServizioPrenotazione(db).annulla_prenotazione(prenotazione_id, utente["id"])
    except PrenotazioneNonTrovataException:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")


# [IF-UT.04] CS-05 — Sblocca uno o più mezzi in batch (msg15 diagramma di sequenza)
@router.post("/mezzi/sblocca", status_code=200, response_model=RisultatoSblocco)
def sblocca_mezzi(
    body: SbloccoRequest,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    return ServizioMobilita(db).sblocca_mezzi(
        body.mezzo_ids, utente["id"], body.lat, body.lng
    )


# [IF-UT.10] SD SospendeCorsa — msg3: PUT /utente/corse/{idCorsa}/pausa
@router.put("/corse/{corsa_id}/pausa", status_code=200)
def sospendi_corsa(
    corsa_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        return ServizioMobilita(db).sospendiCorsa(corsa_id, UUID(str(utente["id"])))
    except CorsaNonTrovataException:
        raise HTTPException(status_code=404, detail="Corsa non trovata")
    except CorsaNonInUsaException as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-UT.05] — Riprende la corsa dalla pausa
@router.post("/corse/{corsa_id}/riprendi", status_code=200)
def riprendi_corsa(
    corsa_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        ServizioMobilita(db).riprendi_corsa(corsa_id, UUID(str(utente["id"])))
        return {"status": "in_uso"}
    except CorsaNonTrovataException:
        raise HTTPException(status_code=404, detail="Corsa non trovata")
    except CorsaNonInPausaException as e:
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


# [IF-UT.14] UT-11 — Storico corse dell'utente (statica prima della dinamica)
@router.get("/corse/storico", response_model=list[Corsa])
def get_storico_corse(
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    """[IF-UT.14 / UT-11] Restituisce la cronologia delle corse terminate dell'utente."""
    from sqlalchemy.exc import SQLAlchemyError
    try:
        return ServizioMobilita(db).get_storico(utente["id"])
    except SQLAlchemyError:
        # [UT-11.1] DatiNonDisponibili — errore di accesso ai dati
        raise HTTPException(
            status_code=503,
            detail="Storico non disponibile al momento. Riprova più tardi.",
        )


# [IF-UT.07] UT-08 — Riepilogo corsa terminata
@router.get("/corse/{corsa_id}/riepilogo", response_model=Corsa)
def get_riepilogo_corsa(
    corsa_id: UUID,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    try:
        return ServizioMobilita(db).calcolaRiepilogoSessione(corsa_id, UUID(str(utente["id"])))
    except CorsaNonTrovataException:
        raise HTTPException(status_code=404, detail="Corsa non trovata")


# [IF-OP.01 / IF-UT.08] Helper demo di presentazione (gated all'account demo):
# aggiorna la posizione del mezzo della corsa per simularne il movimento sulla mappa.
@router.patch("/corse/{corsa_id}/demo/posizione", status_code=204)
def aggiorna_posizione_demo(
    corsa_id: UUID,
    body: PosizioneDemoRequest,
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    if not config.DEMO_ACCOUNT_EMAIL or utente["email"] != config.DEMO_ACCOUNT_EMAIL:
        raise HTTPException(status_code=403, detail="Funzione demo non disponibile per questo account")
    corsa = CorsaRepository(db).trova_per_id(corsa_id)
    if corsa is None or corsa["utente_id"] != str(utente["id"]):
        raise HTTPException(status_code=403, detail="Corsa non appartenente all'utente")
    ServizioMappa(db).aggiorna_posizione_mezzo(UUID(corsa["mezzo_id"]), body.lat, body.lng)