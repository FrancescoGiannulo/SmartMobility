from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_gis import ServizioGIS
from bll.servizio_mobilita import ServizioMobilita, SegnalazioneNonTrovata
from bll.servizio_pricing import ServizioPricing, TariffaGiaEsistente, TariffaNonTrovata
from controllers.schemas import MezzoMappaOut, SegnalazioneOut, ConfigurazioneFineCorsaRequest, CreaTariffaRequest, TariffaResponse

router = APIRouter(prefix="/operatore", tags=["Flotta Operatore"])
_pricing = ServizioPricing()

TIPI_VINCOLO_VALIDI = {"penale", "divieto", "avviso"}


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_operatore(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[CS-02 / OP.01] Tutti i mezzi con posizione per la Mappa Operatore."""
    return ServizioGIS(db).ottieni_mezzi_operatore()


# [IF-OP.08] Gestisce Segnalazione
@router.get("/segnalazioni", response_model=list[SegnalazioneOut])
def lista_segnalazioni(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    return ServizioMobilita(db).get_segnalazioni()


@router.get("/segnalazioni/{segnalazione_id}", response_model=SegnalazioneOut)
def dettaglio_segnalazione(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    try:
        return ServizioMobilita(db).get_dettaglio_segnalazione(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/segnalazioni/{segnalazione_id}/stato", response_model=SegnalazioneOut)
def prendi_in_carico(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    try:
        return ServizioMobilita(db).prendi_in_carico(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))


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


@router.put("/tariffe/{tipo_mezzo}", response_model=TariffaResponse)
def aggiorna_tariffa(
    tipo_mezzo: str,
    body: CreaTariffaRequest,
    _=Depends(verify_token(["OP"])),
):
    try:
        return _pricing.aggiorna_tariffa(tipo_mezzo, body.costo_al_minuto, body.costo_al_km)
    except TariffaNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
