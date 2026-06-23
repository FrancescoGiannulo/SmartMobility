from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dal.corsa_repository import CorsaRepository


class ServizioReport:
    """[IF-AP.01] Generazione report aggregati e statistiche per AP."""

    # Allineato ai colori usati dal frontend (VistaReportAP / VistaDashboardAP)
    _COLORI = {
        "monopattino": "#155e52",
        "bicicletta": "#2196f3",
        "automobile": "#e91e8c",
    }
    _ETICHETTE = {
        "monopattino": "Monopattino",
        "bicicletta": "Bicicletta",
        "automobile": "Automobile",
    }
    _GIORNI = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

    def __init__(self, db: Session) -> None:
        self._corsa_repo = CorsaRepository(db)

    # [IF-AP.01] Accede Report — genera il report aggregato per il periodo indicato
    def genera_report(self, da: datetime | None = None, a: datetime | None = None) -> dict:
        da, a = self._intervallo(da, a)
        corse = self._corsa_repo.find_by_periodo(da, a)
        return self._aggrega_statistiche(corse)

    # [IF-AP.02] Esporta Report — serializza il report in formato CSV
    def esporta_csv(self, da: datetime | None = None, a: datetime | None = None) -> str:
        report = self.genera_report(da, a)
        return self._serializza_csv(report)

    # [IF-AP.01] Consulta lo storico delle corse nel periodo
    def consulta_storico(self, da: datetime | None = None, a: datetime | None = None) -> list[dict]:
        da, a = self._intervallo(da, a)
        return self._corsa_repo.find_by_periodo(da, a)

    # ── helper privati ────────────────────────────────────────────────────────

    def _intervallo(self, da: datetime | None, a: datetime | None) -> tuple[datetime, datetime]:
        """Default: settimana corrente (lunedì 00:00 → lunedì successivo)."""
        if da is not None and a is not None:
            return da, a
        oggi = datetime.now(timezone.utc)
        lunedi = (oggi - timedelta(days=oggi.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return lunedi, lunedi + timedelta(days=7)

    def _aggrega_statistiche(self, corse: list[dict]) -> dict:
        corse_totali = len(corse)
        distanza_totale = sum(c["distanza_km"] for c in corse)
        durata_totale_min = sum(c["durata_min"] for c in corse)
        durata_media_h = (durata_totale_min / corse_totali / 60) if corse_totali else 0.0

        # Conteggi per giorno della settimana e tipologia
        settimana = {
            g: {"monopattino": 0, "bicicletta": 0, "automobile": 0} for g in self._GIORNI
        }
        per_tipo = {"monopattino": 0, "bicicletta": 0, "automobile": 0}
        for c in corse:
            tipo = c["tipo_mezzo"]
            if tipo not in per_tipo:
                continue
            per_tipo[tipo] += 1
            giorno = self._GIORNI[c["inizio_at"].weekday()]
            settimana[giorno][tipo] += 1

        dati_settimanali = [
            {"giorno": g, **settimana[g]} for g in self._GIORNI
        ]
        dati_torta = [
            {
                "name": self._ETICHETTE[tipo],
                "value": round(per_tipo[tipo] / corse_totali * 100, 1) if corse_totali else 0.0,
                "colore": self._COLORI[tipo],
            }
            for tipo in ("monopattino", "bicicletta", "automobile")
        ]

        return {
            "corse_totali": corse_totali,
            "durata_media_h": round(durata_media_h, 1),
            "distanza_totale_km": round(distanza_totale, 1),
            "dati_settimanali": dati_settimanali,
            "dati_torta": dati_torta,
        }

    def _serializza_csv(self, report: dict) -> str:
        intestazione = "Giorno,Monopattino,Bicicletta,Automobile"
        righe = [
            f"{d['giorno']},{d['monopattino']},{d['bicicletta']},{d['automobile']}"
            for d in report["dati_settimanali"]
        ]
        return "\n".join([intestazione, *righe])
