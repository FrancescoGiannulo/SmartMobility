from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.storico_modifiche import StoricoModifiche


class StoricoModificheRepository:
    """[IF-OP.12] Persistenza dello storico delle modifiche alle configurazioni del servizio."""

    def crea(
        self,
        tipo_configurazione: str,
        descrizione: str,
        valore_precedente: str | None,
        valore_nuovo: str | None,
        operatore_id: UUID,
    ) -> StoricoModifiche:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "INSERT INTO storico_modifiche "
                    "(tipo_configurazione, descrizione, valore_precedente, valore_nuovo, operatore_id) "
                    "VALUES (:tipo, :descrizione, :precedente, :nuovo, :operatore_id) "
                    "RETURNING id, tipo_configurazione, descrizione, valore_precedente, valore_nuovo, "
                    "operatore_id, created_at"
                ),
                {
                    "tipo": tipo_configurazione,
                    "descrizione": descrizione,
                    "precedente": valore_precedente,
                    "nuovo": valore_nuovo,
                    "operatore_id": str(operatore_id),
                },
            ).fetchone()
            session.commit()
            return StoricoModifiche(
                id=row.id,
                tipo_configurazione=row.tipo_configurazione,
                descrizione=row.descrizione,
                valore_precedente=row.valore_precedente,
                valore_nuovo=row.valore_nuovo,
                operatore_id=row.operatore_id,
                created_at=row.created_at,
            )

    def find_all(self) -> list[StoricoModifiche]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, tipo_configurazione, descrizione, valore_precedente, valore_nuovo, "
                    "operatore_id, created_at "
                    "FROM storico_modifiche ORDER BY created_at DESC"
                )
            ).fetchall()
            return [
                StoricoModifiche(
                    id=row.id,
                    tipo_configurazione=row.tipo_configurazione,
                    descrizione=row.descrizione,
                    valore_precedente=row.valore_precedente,
                    valore_nuovo=row.valore_nuovo,
                    operatore_id=row.operatore_id,
                    created_at=row.created_at,
                )
                for row in rows
            ]
