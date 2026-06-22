import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.recensione import Recensione


class RecensioneRepository:

    # [IF-UT.15] Scrive Recensione
    def save(self, utente_id: uuid.UUID, voto: int, commento: str | None) -> Recensione:
        with Session(engine) as session:
            recensione = Recensione(utente_id=utente_id, voto=voto, commento=commento)
            session.add(recensione)
            session.commit()
            session.refresh(recensione)
            return recensione

    def find_by_utente_id(self, utente_id: uuid.UUID) -> list[Recensione]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, voto, commento, created_at "
                    "FROM recensioni WHERE utente_id = :uid ORDER BY created_at DESC"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
        return [
            Recensione(
                id=r.id, utente_id=r.utente_id, voto=r.voto,
                commento=r.commento, created_at=r.created_at,
            )
            for r in rows
        ]

    def find_all(self) -> list[Recensione]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, voto, commento, created_at "
                    "FROM recensioni ORDER BY created_at DESC"
                )
            ).fetchall()
        return [
            Recensione(
                id=r.id, utente_id=r.utente_id, voto=r.voto,
                commento=r.commento, created_at=r.created_at,
            )
            for r in rows
        ]
