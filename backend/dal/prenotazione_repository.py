from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class PrenotazioneRepository:

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

    # [IF-UT.04] CS-10 — verifica prenotazione attiva per sblocco da prenotazione
    def trova_attiva_per_utente_e_mezzo(
        self, utente_id: UUID, mezzo_id: UUID
    ) -> dict | None:
        sql = text("""
            SELECT id, utente_id, mezzo_id, stato
            FROM prenotazioni
            WHERE utente_id = :utente_id
              AND mezzo_id = :mezzo_id
              AND stato = 'attiva'
              AND scade_at > now()
            LIMIT 1
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
            }).fetchone()
        if row is None:
            return None
        return {
            "id": row.id,
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
        }

    def aggiorna_stato(self, prenotazione_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE prenotazioni SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {
                "stato": nuovo_stato,
                "id": str(prenotazione_id),
            })
            s.commit()
