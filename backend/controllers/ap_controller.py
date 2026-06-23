from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import verify_token
from bll.servizio_mappa import ServizioMappa
from bll.servizio_report import ServizioReport
from controllers.schemas import MezzoMappaOut, ZonaOut, ReportOut

router = APIRouter(prefix="/ap", tags=["Mappa AP"])


@router.get("/mappa/mezzi", response_model=list[MezzoMappaOut])
def mappa_mezzi_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Tutti i mezzi con posizione per la Mappa AP."""
    return ServizioMappa(db).ottieni_mezzi_operatore()


@router.get("/mappa/zone", response_model=list[ZonaOut])
def mappa_zone_ap(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.03] Zone attive per la Mappa AP."""
    return ServizioMappa(db).ottieni_zone()


# [IF-AP.01] Accede Report — AmministrazionePubblicaController.visualizzaReport
@router.get("/report", response_model=ReportOut)
def visualizza_report(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.01] Report aggregato (corse, distanza, durata media, quote per tipologia)."""
    return ServizioReport(db).genera_report()


# [IF-AP.02] Esporta Report — AmministrazionePubblicaController.esportaCSV
@router.get("/report/export", response_class=PlainTextResponse)
def esporta_report(
    _=Depends(verify_token(["AP"])),
    db: Session = Depends(get_db),
):
    """[IF-AP.02] Esporta il report settimanale in formato CSV."""
    csv = ServizioReport(db).esporta_csv()
    return PlainTextResponse(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report_smartmobility.csv"},
    )
