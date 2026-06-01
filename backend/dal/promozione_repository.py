from sqlalchemy import func
from sqlalchemy.orm import Session
from model.promozione import Promozione


class PromozioneRepository:

    def __init__(self, db: Session | None = None) -> None:
        self._db = db

    # [IF-UT.13] — promozioni con attiva=True e data_fine >= adesso
    def getAttive(self) -> list[dict]:
        if self._db is None:
            raise RuntimeError("PromozioneRepository.getAttive richiede db iniettato")
        rows = (
            self._db.query(Promozione)
            .filter(
                Promozione.attiva.is_(True),
                Promozione.data_fine >= func.now(),
            )
            .all()
        )
        return [
            {
                "id": str(r.id),
                "titolo": r.titolo,
                "descrizione": r.descrizione,
                "sconto_percentuale": f"{r.sconto_percentuale:.2f}",
                "data_fine": r.data_fine.isoformat(),
            }
            for r in rows
        ]
