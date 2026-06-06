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
        tipo_mezzo: Optional[str] = None,
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
            tipo_mezzo=tipo_mezzo,
        )
        db.add(offerta)
        db.commit()
        db.refresh(offerta)
        return offerta

    def aggiorna(
        self,
        offerta_id: uuid.UUID,
        db: Session,
        nome: Optional[str] = None,
        descrizione: Optional[str] = None,
        sconto_percentuale: Optional[Decimal] = None,
        prezzo: Optional[Decimal] = None,
        durata_giorni: Optional[int] = None,
        data_inizio: Optional[datetime] = None,
        data_scadenza: Optional[datetime] = None,
        stato: Optional[str] = None,
        tipo_mezzo: Optional[str] = None,
    ) -> Offerta:
        offerta = self.trova_per_id(offerta_id, db)
        if nome is not None and nome != offerta.nome:
            if self.nome_esiste(nome, db):
                raise NomeDuplicatoException(f"Offerta con nome '{nome}' già esistente")
            offerta.nome = nome
        if descrizione is not None:
            offerta.descrizione = descrizione
        if sconto_percentuale is not None:
            offerta.sconto_percentuale = sconto_percentuale
        if prezzo is not None:
            offerta.prezzo = prezzo
        if durata_giorni is not None:
            offerta.durata_giorni = durata_giorni
        if data_inizio is not None:
            offerta.data_inizio = data_inizio
        if data_scadenza is not None:
            offerta.data_scadenza = data_scadenza
        if stato is not None:
            offerta.stato = stato
        if tipo_mezzo is not None:
            offerta.tipo_mezzo = tipo_mezzo
        db.commit()
        db.refresh(offerta)
        return offerta

    def elimina(self, offerta_id: uuid.UUID, db: Session) -> None:
        offerta = self.trova_per_id(offerta_id, db)
        db.delete(offerta)
        db.commit()
