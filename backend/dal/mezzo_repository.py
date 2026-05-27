from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class MezzoRepository:

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

    def lista_per_mappa(self, solo_disponibili: bool) -> list[dict]:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE lat IS NOT NULL AND lng IS NOT NULL
              AND (:solo_disponibili = false OR stato = 'Disponibile')
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"solo_disponibili": solo_disponibili}).fetchall()
        return [
            {
                "id": row.id,
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    def trova_per_id(self, mezzo_id: UUID) -> dict | None:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi WHERE id = :id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(mezzo_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "codice": row.codice,
            "tipo": row.tipo,
            "stato": row.stato,
            "lat": row.lat,
            "lng": row.lng,
            "batteria": row.batteria,
        }

    def aggiorna_stato(self, mezzo_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE mezzi SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"stato": nuovo_stato, "id": str(mezzo_id)})
            s.commit()
