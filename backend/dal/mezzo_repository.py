from contextlib import contextmanager
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
