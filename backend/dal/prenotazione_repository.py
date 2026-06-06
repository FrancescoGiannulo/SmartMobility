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
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
        }

    # [IF-UT.02] CS-XX — crea prenotazione con scadenza configurabile
    def crea(self, utente_id: UUID, mezzo_id: UUID, durata_minuti: int = 30) -> dict:
        sql = text("""
            INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
            VALUES (:utente_id, :mezzo_id, 'attiva',
                    now() + :durata * interval '1 minute')
            RETURNING id, utente_id, mezzo_id, stato, scade_at, created_at
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
                "durata": durata_minuti,
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
            "scade_at": row.scade_at.isoformat(),
            "created_at": row.created_at.isoformat(),
        }

    def aggiorna_stato(self, prenotazione_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE prenotazioni SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {
                "stato": nuovo_stato,
                "id": str(prenotazione_id),
            })
            s.commit()

    # [IF-UT.02] CS-04 — lista prenotazioni attive dell'utente
    def trova_attive_per_utente(self, utente_id: UUID) -> list[dict]:
        sql = text("""
            SELECT p.id, p.mezzo_id, p.stato, p.scade_at, p.created_at,
                   m.codice, m.tipo, m.batteria
            FROM prenotazioni p
            JOIN mezzi m ON m.id = p.mezzo_id
            WHERE p.utente_id = :utente_id
              AND p.stato = 'attiva'
              AND p.scade_at > now()
            ORDER BY p.created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"utente_id": str(utente_id)}).fetchall()
        return [
            {
                "id": str(row.id),
                "mezzo_id": str(row.mezzo_id),
                "stato": row.stato,
                "scade_at": row.scade_at.isoformat(),
                "created_at": row.created_at.isoformat(),
                "codice": row.codice,
                "tipo": row.tipo,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    # [IF-UT.04] CS-05 — trova se esiste qualsiasi prenotazione attiva per il mezzo (da qualsiasi utente)
    def trova_qualsiasi_attiva_per_mezzo(self, mezzo_id: UUID) -> dict | None:
        sql = text("""
            SELECT id FROM prenotazioni
            WHERE mezzo_id = :mezzo_id
              AND stato = 'attiva'
              AND scade_at > now()
            LIMIT 1
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"mezzo_id": str(mezzo_id)}).fetchone()
        if row is None:
            return None
        return {"id": str(row.id)}

    # [IF-UT.02] CS-XX — trova prenotazione attiva per id e utente
    def trova_attiva_per_id_e_utente(
        self, prenotazione_id: UUID, utente_id: UUID
    ) -> dict | None:
        sql = text("""
            SELECT id, mezzo_id, stato
            FROM prenotazioni
            WHERE id = :id AND utente_id = :utente_id AND stato = 'attiva'
            LIMIT 1
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "id": str(prenotazione_id),
                "utente_id": str(utente_id),
            }).fetchone()
        if row is None:
            return None
        return {"id": str(row.id), "mezzo_id": str(row.mezzo_id), "stato": row.stato}
