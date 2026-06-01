from sqlalchemy.orm import Session
from model.tariffa import Tariffa


class TariffaRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    # [IF-UT.05]
    def findAll(self) -> list[dict]:
        rows = self._db.query(Tariffa).all()
        return [
            {
                "id": str(r.id),
                "tipo_mezzo": r.tipo_mezzo.value,
                "costo_al_minuto": f"{r.costo_al_minuto:.4f}",
                "costo_al_km": f"{r.costo_al_km:.4f}",
            }
            for r in rows
        ]
