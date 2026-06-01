import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from model.offerta import Offerta


class NomeDuplicatoException(Exception):
    pass


class OffertaNonTrovataException(Exception):
    pass


class OffertaRepository:

    def lista(self, db: Session) -> list[Offerta]:
        return db.query(Offerta).order_by(Offerta.created_at.desc()).all()

    def trova_per_id(self, offerta_id: uuid.UUID, db: Session) -> Offerta:
        offerta = db.query(Offerta).filter(Offerta.id == offerta_id).first()
        if not offerta:
            raise OffertaNonTrovataException(f"Offerta {offerta_id} non trovata")
        return offerta

    def nome_esiste(self, nome: str, db: Session) -> bool:
        return db.query(Offerta).filter(Offerta.nome == nome).first() is not None

    def crea(
        self,
        nome: str,
        tipo: str,
        descrizione: Optional[str],
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_inizio: Optional[datetime],
        data_scadenza: Optional[datetime],
        db: Session,
    ) -> Offerta:
        if self.nome_esiste(nome, db):
            raise NomeDuplicatoException(f"Offerta con nome '{nome}' già esistente")
        offerta = Offerta(
            nome=nome,
            tipo=tipo,
            stato="attiva",
            descrizione=descrizione,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_inizio=data_inizio,
            data_scadenza=data_scadenza,
        )
        db.add(offerta)
        db.commit()
        db.refresh(offerta)
        return offerta

    def elimina(self, offerta_id: uuid.UUID, db: Session) -> None:
        offerta = self.trova_per_id(offerta_id, db)
        db.delete(offerta)
        db.commit()
