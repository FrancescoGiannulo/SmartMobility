import uuid as _uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class CorsaRepository:

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

    def trova_per_id(self, corsa_id: UUID) -> dict | None:
        sql = text("SELECT id, utente_id, mezzo_id, stato FROM corse WHERE id = :id")
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(corsa_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
        }

    def aggiorna_stato(self, corsa_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE corse SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"stato": nuovo_stato, "id": str(corsa_id)})
            s.commit()

    # [IF-UT.04] CS-10 — crea corsa all'avvio del mezzo
    def crea(
        self,
        utente_id: UUID,
        mezzo_id: UUID,
        prenotazione_id: UUID | None,
    ) -> dict:
        sql = text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, prenotazione_id, stato, inizio_at)
            VALUES
                (:id, :utente_id, :mezzo_id, :prenotazione_id, 'in_uso', :inizio_at)
            RETURNING id, utente_id, mezzo_id, prenotazione_id, stato, inizio_at
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "id": str(_uuid.uuid4()),
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
                "prenotazione_id": str(prenotazione_id) if prenotazione_id else None,
                "inizio_at": datetime.now(timezone.utc),
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "prenotazione_id": str(row.prenotazione_id) if row.prenotazione_id else None,
            "stato": row.stato,
            "inizio_at": row.inizio_at.isoformat(),
        }
