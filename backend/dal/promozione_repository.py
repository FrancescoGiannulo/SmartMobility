from sqlalchemy import func
from sqlalchemy.orm import Session
from model.offerta import Promozione


class PromozioneRepository:

    def __init__(self, db: Session | None = None) -> None:
        self._db = db

    # [IF-UT.13] — promozioni attive dalla tabella offerte
    def getAttive(self) -> list[dict]:
        if self._db is None:
            raise RuntimeError("PromozioneRepository.getAttive richiede db iniettato")
        rows = (
            self._db.query(Promozione)
            .filter(
                Promozione.stato == "attiva",
                Promozione.data_scadenza >= func.now(),
            )
            .all()
        )
        return [
            {
                "id": str(r.id),
                "titolo": r.nome,
                "descrizione": r.descrizione,
                "sconto_percentuale": f"{r.sconto_percentuale:.2f}",
                "data_fine": r.data_scadenza.isoformat(),
            }
            for r in rows
        ]
