from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.tariffa import Tariffa


class TariffaRepository:

    # [IF-OP.07] Definisce Tariffa
    def find_all(self) -> list[Tariffa]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, tipo_mezzo, costo_al_minuto, costo_al_km "
                    "FROM tariffe ORDER BY tipo_mezzo"
                )
            ).fetchall()
            return [
                Tariffa(
                    id=r.id,
                    tipo_mezzo=r.tipo_mezzo,
                    costo_al_minuto=r.costo_al_minuto,
                    costo_al_km=r.costo_al_km,
                )
                for r in rows
            ]

    def exists_by_tipologia(self, tipo_mezzo: str) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text("SELECT 1 FROM tariffe WHERE tipo_mezzo = :tipo LIMIT 1"),
                {"tipo": tipo_mezzo},
            ).fetchone()
        return result is not None

    def aggiorna(self, tipo_mezzo: str, costo_al_minuto: Decimal, costo_al_km: Decimal) -> Tariffa | None:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "UPDATE tariffe SET costo_al_minuto = :minuto, costo_al_km = :km "
                    "WHERE tipo_mezzo = :tipo "
                    "RETURNING id, tipo_mezzo, costo_al_minuto, costo_al_km"
                ),
                {"minuto": str(costo_al_minuto), "km": str(costo_al_km), "tipo": tipo_mezzo},
            ).fetchone()
            session.commit()
        if not row:
            return None
        return Tariffa(id=row.id, tipo_mezzo=row.tipo_mezzo, costo_al_minuto=row.costo_al_minuto, costo_al_km=row.costo_al_km)

    def crea(self, tipo_mezzo: str, costo_al_minuto: Decimal, costo_al_km: Decimal) -> Tariffa:
        with Session(engine) as session:
            tariffa = Tariffa(
                tipo_mezzo=tipo_mezzo,
                costo_al_minuto=costo_al_minuto,
                costo_al_km=costo_al_km,
            )
            session.add(tariffa)
            session.commit()
            session.refresh(tariffa)
            return tariffa
