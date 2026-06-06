import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session

from dal.abbonamento_repository import AbbonamentoRepository
from model.abbonamento_utente import AbbonamentoUtente
from model.offerta import Offerta


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
        # import lazy per evitare dipendenza circolare
        from bll.servizio_pricing import ServizioPricing, NessunMetodoPredefinito, PagamentoRifiutato as PRifiutato
        self._pricing = ServizioPricing()
        self._NessunMetodoPredefinito = NessunMetodoPredefinito
        self._PRifiutato = PRifiutato

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
        # [IF-UT.16] Impedisce la sottoscrizione multipla con abbonamento ancora attivo
        existing = self._repo.get_attivo(utente_id, db)
        if existing and existing.data_fine > datetime.now(timezone.utc):
            raise OffertaNonValida("Hai già un abbonamento attivo")

        offerta = db.query(Offerta).filter(Offerta.id == offerta_id).first()
        if offerta is None:
            raise OffertaNonValida(f"Offerta {offerta_id} non trovata")
        if offerta.tipo != "abbonamento":
            raise OffertaNonValida("L'offerta selezionata non è un piano abbonamento")
        if offerta.stato != "attiva":
            raise OffertaNonValida("Il piano abbonamento non è attualmente disponibile")
        if offerta.durata_giorni is None or offerta.prezzo is None:
            raise OffertaNonValida("Il piano abbonamento è incompleto")

        data_fine = datetime.now(timezone.utc) + timedelta(days=offerta.durata_giorni)
        abbonamento = self._repo.crea(
            utente_id=utente_id,
            offerta_id=offerta_id,
            data_fine=data_fine,
            db=db,
        )

        try:
            self._pricing.paga_importo(
                utente_id=utente_id,
                importo=offerta.prezzo,
                abbonamento_id=abbonamento.id,
            )
        except self._NessunMetodoPredefinito as e:
            # Rollback: il pagamento non è andato a buon fine, annulla l'abbonamento creato
            abbonamento.stato = "annullato"
            db.commit()
            raise NessunMetodoPagamento(str(e))
        except self._PRifiutato as e:
            abbonamento.stato = "annullato"
            db.commit()
            raise PagamentoRifiutato(str(e))

        return abbonamento
