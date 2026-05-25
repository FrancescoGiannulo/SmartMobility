from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from bll.servizio_mobilita import ServizioMobilita
from controllers.schemas import MezzoMappaOut, ConfigurazioneFineCorsaRequest

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])

TIPI_VINCOLO_VALIDI = {"penale", "divieto", "avviso"}


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


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
