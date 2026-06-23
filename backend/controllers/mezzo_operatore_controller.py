from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_mappa import ServizioMappa
from bll.servizio_mobilita import ServizioMobilita

from controllers.schemas import (
    MezzoMappaOut,
    ConfigurazioneFineCorsaRequest,
    AggiungiMezzoRequest,
    ModificaStatoMezzoRequest,
    MezzoFlottaOut,
)

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])

TIPI_VINCOLO_VALIDI = {"penale", "divieto", "avviso"}


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioMappa(db).ottieni_mezzi_operatore()



# [IF-OP.11] CS-11 — Lista flotta operatore (tutti i mezzi non dismessi)
@router.get("/mezzi", response_model=list[MezzoFlottaOut])
def lista_mezzi_flotta(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    return ServizioMobilita(db).get_mezzi_flotta()


# [IF-OP.11] CS-11 — Aggiunge nuovo mezzo alla flotta
@router.post("/mezzi", response_model=MezzoFlottaOut, status_code=201)
def aggiungi_mezzo(
    body: AggiungiMezzoRequest,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import IdentificativoEsistenteException, PosizioneNonOperativaException
    tipi_validi = {"monopattino", "bicicletta", "automobile"}
    if body.tipo not in tipi_validi:
        raise HTTPException(status_code=422, detail=f"tipo non valido: {body.tipo}")
    if not body.codice.strip():
        raise HTTPException(status_code=422, detail="codice non può essere vuoto")
    try:
        return ServizioMobilita(db).aggiungi_mezzo(
            body.tipo, body.codice.strip(), body.lat, body.lng, body.stato
        )
    except IdentificativoEsistenteException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PosizioneNonOperativaException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.04] Modifica Stato Mezzo — cambio stato manuale dell'operatore
@router.put("/mezzi/{mezzo_id}/stato", response_model=MezzoFlottaOut)
def modifica_stato_mezzo(
    mezzo_id: UUID,
    body: ModificaStatoMezzoRequest,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import MezzoNonTrovatoException, MezzoInMissioneException
    try:
        return ServizioMobilita(db).modifica_stato_mezzo(mezzo_id, body.stato)
    except MezzoNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MezzoInMissioneException as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-OP.12] CS-12 — Verifica se un mezzo può essere dismesso (no side-effects)
@router.post("/mezzi/{mezzo_id}/verifica")
def verifica_dismissione(
    mezzo_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import MezzoNonTrovatoException
    try:
        return ServizioMobilita(db).verifica_dismissione(mezzo_id)
    except MezzoNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))


# [IF-OP.12] CS-12 — Dismette il mezzo (imposta stato "Dismesso")
@router.delete("/mezzi/{mezzo_id}")
def dismetti_mezzo(
    mezzo_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import MezzoNonTrovatoException, MezzoInMissioneException
    try:
        ServizioMobilita(db).dismetti_mezzo(mezzo_id)
        return {"status": "ok"}
    except MezzoNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MezzoInMissioneException as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-OP.13] CS-XX — Leggi configurazione regole fine corsa
@router.get("/configurazione/fine-corsa")
def get_configurazione_fine_corsa(
    operatore=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    return ServizioMobilita(db).get_zona_parcheggio_e_regole(UUID(operatore["id"]))


# [IF-OP.13] CS-XX — Salva configurazione regole fine corsa
@router.post("/configurazione/fine-corsa", status_code=201)
def salva_configurazione_fine_corsa(
    body: ConfigurazioneFineCorsaRequest,
    operatore=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    if body.tipo_vincolo not in TIPI_VINCOLO_VALIDI:
        raise HTTPException(status_code=422, detail="tipo_vincolo non valido")
    if body.batteria_minima is not None and not (0 <= body.batteria_minima <= 100):
        raise HTTPException(status_code=422, detail="batteria_minima deve essere tra 0 e 100")
    if body.durata_max_prenotazione_min <= 0:
        raise HTTPException(status_code=422, detail="durata_max_prenotazione_min deve essere > 0")
    if body.durata_periodo_grazia_min < 0:
        raise HTTPException(status_code=422, detail="durata_periodo_grazia_min deve essere >= 0")
    if body.max_mezzi_per_utente <= 0:
        raise HTTPException(status_code=422, detail="max_mezzi_per_utente deve essere > 0")
    ServizioMobilita(db).salva_regole_fine_corsa(
        UUID(operatore["id"]),
        body.durata_max_prenotazione_min,
        body.durata_periodo_grazia_min,
        body.max_mezzi_per_utente,
        body.tipo_vincolo,
        body.batteria_minima,
        body.penale_fuori_zona,
    )
    return {"status": "ok"}
