import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session

from dal.abbonamento_repository import AbbonamentoRepository
from dal.pagamento_repository import PagamentoRepository
from model.abbonamento_utente import AbbonamentoUtente
from model.offerta import Offerta
from providers.provider_pagamenti import ProviderPagamentiStub


class AbbonamentoException(Exception):
    pass


class OffertaNonValida(Exception):
    pass


class NessunMetodoPagamento(Exception):
    pass


class PagamentoRifiutato(Exception):
    pass


class ServizioAbbonamento:
    """[IF-UT.16] BLL per la sottoscrizione di abbonamenti."""

    def __init__(self) -> None:
        self._repo = AbbonamentoRepository()
        self._pagamento_repo = PagamentoRepository()
        self._provider = ProviderPagamentiStub()

    def get_piani_disponibili(self, db: Session) -> list[Offerta]:
        """Restituisce solo le offerte di tipo abbonamento con stato attiva."""
        return (
            db.query(Offerta)
            .filter(Offerta.tipo == "abbonamento", Offerta.stato == "attiva")
            .order_by(Offerta.created_at.desc())
            .all()
        )

    def get_abbonamento_attivo(self, utente_id: uuid.UUID, db: Session) -> Optional[AbbonamentoUtente]:
        return self._repo.get_attivo(utente_id, db)

    def sottoscrivi(
        self,
        utente_id: uuid.UUID,
        offerta_id: uuid.UUID,
        db: Session,
    ) -> AbbonamentoUtente:
        offerta = db.query(Offerta).filter(Offerta.id == offerta_id).first()
        if offerta is None:
            raise OffertaNonValida(f"Offerta {offerta_id} non trovata")
        if offerta.tipo != "abbonamento":
            raise OffertaNonValida("L'offerta selezionata non è un piano abbonamento")
        if offerta.stato != "attiva":
            raise OffertaNonValida("Il piano abbonamento non è attualmente disponibile")
        if offerta.durata_giorni is None or offerta.prezzo is None:
            raise OffertaNonValida("Il piano abbonamento è incompleto")

        metodi = self._pagamento_repo.lista_metodi(utente_id)
        if not metodi:
            raise NessunMetodoPagamento("Aggiungi un metodo di pagamento prima di sottoscrivere")

        metodo = next((m for m in metodi if m.predefinito), metodi[0])
        risposta = self._provider.autorizza(metodo.token_esterno, offerta.prezzo)
        if not risposta.autorizzato:
            raise PagamentoRifiutato("Il pagamento è stato rifiutato dal provider")

        data_fine = datetime.now(timezone.utc) + timedelta(days=offerta.durata_giorni)
        return self._repo.crea(
            utente_id=utente_id,
            offerta_id=offerta_id,
            data_fine=data_fine,
            db=db,
        )
