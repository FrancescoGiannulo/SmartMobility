from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class RegolaFineCorsaRepository:

    def __init__(self, db: Session | Engine) -> None:
        self._engine = db if isinstance(db, Engine) else None
        self._session = db if not isinstance(db, Engine) else None

    @contextmanager
    def _sessione(self):
        if self._session is not None:
            yield self._session
        else:
            with Session(self._engine) as s:
                yield s

    def trova_tutte(self) -> list[dict]:
        sql = text("""
            SELECT id, zona_parcheggio_id, batteria_minima,
                   penale_fuori_zona, tipo_vincolo
            FROM regole_fine_corsa
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql).fetchall()
        return [
            {
                "id": str(row.id),
                "zona_parcheggio_id": str(row.zona_parcheggio_id),
                "batteria_minima": row.batteria_minima,
                "penale_fuori_zona": float(row.penale_fuori_zona),
                "tipo_vincolo": row.tipo_vincolo,
            }
            for row in rows
        ]

    def elimina_tutto(self) -> None:
        sql = text("DELETE FROM regole_fine_corsa")
        with self._sessione() as s:
            s.execute(sql)
            s.commit()

    # [IF-OP.13] — crea una regola per una zona parcheggio
    def crea(
        self,
        zona_id: UUID,
        batteria_minima: int | None,
        penale_fuori_zona: float,
        tipo_vincolo: str,
    ) -> dict:
        sql = text("""
            INSERT INTO regole_fine_corsa
                (zona_parcheggio_id, batteria_minima, penale_fuori_zona, tipo_vincolo)
            VALUES (:zona_id, :batteria_minima, :penale_fuori_zona, :tipo_vincolo)
            RETURNING id, zona_parcheggio_id, batteria_minima, penale_fuori_zona, tipo_vincolo
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "zona_id": str(zona_id),
                "batteria_minima": batteria_minima,
                "penale_fuori_zona": penale_fuori_zona,
                "tipo_vincolo": tipo_vincolo,
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "zona_parcheggio_id": str(row.zona_parcheggio_id),
            "batteria_minima": row.batteria_minima,
            "penale_fuori_zona": float(row.penale_fuori_zona),
            "tipo_vincolo": row.tipo_vincolo,
        }
