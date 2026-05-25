from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class OperatoreRepository:

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

    def trova_impostazioni(self, operatore_id: UUID) -> dict | None:
        sql = text("""
            SELECT durata_max_prenotazione_min, durata_periodo_grazia_min,
                   max_mezzi_per_utente
            FROM operatori WHERE id = :id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(operatore_id)}).fetchone()
        if row is None:
            return None
        return {
            "durata_max_prenotazione_min": row.durata_max_prenotazione_min,
            "durata_periodo_grazia_min": row.durata_periodo_grazia_min,
            "max_mezzi_per_utente": row.max_mezzi_per_utente,
        }

    def aggiorna_impostazioni(
        self,
        operatore_id: UUID,
        durata_max_prenotazione_min: int,
        durata_periodo_grazia_min: int,
        max_mezzi_per_utente: int,
    ) -> None:
        sql = text("""
            UPDATE operatori
            SET durata_max_prenotazione_min = :durata_pren,
                durata_periodo_grazia_min   = :durata_grazia,
                max_mezzi_per_utente        = :max_mezzi
            WHERE id = :id
        """)
        with self._sessione() as s:
            s.execute(sql, {
                "durata_pren": durata_max_prenotazione_min,
                "durata_grazia": durata_periodo_grazia_min,
                "max_mezzi": max_mezzi_per_utente,
                "id": str(operatore_id),
            })
            s.commit()
