import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from model.abbonamento_utente import AbbonamentoUtente


class AbbonamentoRepository:

    def crea(
        self,
        utente_id: uuid.UUID,
        offerta_id: uuid.UUID,
        data_fine: datetime,
        db: Session,
    ) -> AbbonamentoUtente:
        abbonamento = AbbonamentoUtente(
            utente_id=utente_id,
            offerta_id=offerta_id,
            data_fine=data_fine,
            stato="attivo",
        )
        db.add(abbonamento)
        db.commit()
        db.refresh(abbonamento)
        return abbonamento

    def get_attivo(self, utente_id: uuid.UUID, db: Session) -> Optional[AbbonamentoUtente]:
        return (
            db.query(AbbonamentoUtente)
            .filter(
                AbbonamentoUtente.utente_id == utente_id,
                AbbonamentoUtente.stato == "attivo",
            )
            .order_by(AbbonamentoUtente.data_fine.desc())
            .first()
        )
