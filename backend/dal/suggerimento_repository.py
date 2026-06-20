import uuid
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.suggerimento import Suggerimento, StatoSuggerimento, TipoSuggerimento


class SuggerimentoRepository:

    # [IF-UT.14] Visualizza Suggerimenti Intelligenti
    def find_by_utente(self, utente_id: uuid.UUID) -> list[Suggerimento]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, tipo, testo, dati_contesto, stato, creato_at "
                    "FROM suggerimenti WHERE utente_id = :uid "
                    "ORDER BY creato_at DESC"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
        return [
            Suggerimento(
                id=r.id, utente_id=r.utente_id, tipo=r.tipo,
                testo=r.testo, dati_contesto=r.dati_contesto,
                stato=r.stato, creato_at=r.creato_at,
            )
            for r in rows
        ]

    def find_recenti(self, utente_id: uuid.UUID, da: datetime) -> list[Suggerimento]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, tipo, testo, dati_contesto, stato, creato_at "
                    "FROM suggerimenti WHERE utente_id = :uid AND creato_at >= :da "
                    "ORDER BY creato_at DESC"
                ),
                {"uid": str(utente_id), "da": da},
            ).fetchall()
        return [
            Suggerimento(
                id=r.id, utente_id=r.utente_id, tipo=r.tipo,
                testo=r.testo, dati_contesto=r.dati_contesto,
                stato=r.stato, creato_at=r.creato_at,
            )
            for r in rows
        ]

    def save(self, s: Suggerimento) -> Suggerimento:
        with Session(engine) as session:
            session.add(s)
            session.commit()
            session.refresh(s)
            return s

    def save_batch(self, suggerimenti: list[Suggerimento]) -> list[Suggerimento]:
        with Session(engine) as session:
            session.add_all(suggerimenti)
            session.commit()
            for s in suggerimenti:
                session.refresh(s)
            return suggerimenti

    def aggiorna_stato(self, id: uuid.UUID, stato: StatoSuggerimento) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text(
                    "UPDATE suggerimenti SET stato = :stato "
                    "WHERE id = :sid RETURNING id"
                ),
                {"stato": stato.value, "sid": str(id)},
            ).fetchone()
            session.commit()
        return result is not None

    def elimina_per_utente(self, utente_id: uuid.UUID) -> int:
        with Session(engine) as session:
            result = session.execute(
                text("DELETE FROM suggerimenti WHERE utente_id = :uid"),
                {"uid": str(utente_id)},
            )
            session.commit()
            return result.rowcount
