from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.notifica import Notifica


class NotificaRepository:
    """[IF-OP.09] Persistenza delle notifiche utente."""

    def crea(self, id_utente: UUID, messaggio: str) -> Notifica:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "INSERT INTO notifiche (utente_id, messaggio) "
                    "VALUES (:utente_id, :messaggio) "
                    "RETURNING id, utente_id, messaggio, letta, created_at"
                ),
                {"utente_id": str(id_utente), "messaggio": messaggio},
            ).fetchone()
            session.commit()
            return Notifica(
                id=row.id,
                id_utente=row.utente_id,
                messaggio=row.messaggio,
                letta=row.letta,
                data=row.created_at,
            )

    def find_by_utente(self, id_utente: UUID) -> list[Notifica]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, messaggio, letta, created_at "
                    "FROM notifiche WHERE utente_id = :id ORDER BY created_at DESC"
                ),
                {"id": str(id_utente)},
            ).fetchall()
            return [
                Notifica(
                    id=row.id,
                    id_utente=row.utente_id,
                    messaggio=row.messaggio,
                    letta=row.letta,
                    data=row.created_at,
                )
                for row in rows
            ]
