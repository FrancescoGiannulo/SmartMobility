from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from bll.servizio_suggerimenti import ServizioSuggerimenti
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import SuggerimentoOut

# [IF-UT.14] SuggerimentoController
router = APIRouter(prefix="/utente/suggerimenti", tags=["Suggerimenti"])


@router.get("", response_model=list[SuggerimentoOut])
def get_suggerimenti(
    utente: dict = Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[IF-UT.14] Restituisce i suggerimenti salvati per l'utente."""
    return ServizioSuggerimenti(db).get_suggerimenti(UUID(str(utente["id"])))


@router.post("/genera", response_model=list[SuggerimentoOut])
def genera_suggerimenti(
    utente: dict = Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[IF-UT.14] Genera nuovi suggerimenti intelligenti basati sui dati utente."""
    return ServizioSuggerimenti(db).genera_suggerimenti(UUID(str(utente["id"])))


@router.patch("/{suggerimento_id}/visto", status_code=204)
def segna_visto(
    suggerimento_id: UUID,
    utente: dict = Depends(verify_token(["UT"])),
    db: Session = Depends(get_db),
):
    """[IF-UT.14] Segna un suggerimento come visto."""
    ServizioSuggerimenti(db).segna_visto(suggerimento_id, UUID(str(utente["id"])))
