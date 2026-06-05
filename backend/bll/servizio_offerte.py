import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from dal.offerta_repository import OffertaRepository, NomeDuplicatoException, OffertaNonTrovataException
from model.offerta import Offerta


class OffertaValidazioneException(Exception):
    pass


class OffertaDuplicataException(Exception):
    pass


class ServizioOfferte:

    def __init__(self) -> None:
        self._repo = OffertaRepository()

    def lista_offerte(self, db: Session) -> list[Offerta]:
        return self._repo.lista(db)

    def crea_offerta(
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
        self._valida(
            nome=nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_scadenza=data_scadenza,
        )
        try:
            return self._repo.crea(
                nome=nome,
                tipo=tipo,
                descrizione=descrizione,
                sconto_percentuale=sconto_percentuale,
                prezzo=prezzo,
                durata_giorni=durata_giorni,
                data_inizio=data_inizio,
                data_scadenza=data_scadenza,
                db=db,
            )
        except NomeDuplicatoException:
            raise OffertaDuplicataException(f"Esiste già un'offerta con nome '{nome}'")

    def elimina_offerta(self, offerta_id: uuid.UUID, db: Session) -> None:
        try:
            self._repo.elimina(offerta_id, db)
        except OffertaNonTrovataException:
            raise OffertaValidazioneException(f"Offerta {offerta_id} non trovata")

    def _valida(
        self,
        nome: str,
        tipo: str,
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_scadenza: Optional[datetime],
    ) -> None:
        if not nome or not nome.strip():
            raise OffertaValidazioneException("Il nome è obbligatorio")
        if tipo not in ("promozione", "abbonamento"):
            raise OffertaValidazioneException("Tipo non valido: usa 'promozione' o 'abbonamento'")
        if tipo == "promozione":
            if sconto_percentuale is None:
                raise OffertaValidazioneException("Lo sconto percentuale è obbligatorio per una promozione")
            if sconto_percentuale <= 0 or sconto_percentuale > 100:
                raise OffertaValidazioneException("Lo sconto deve essere compreso tra 1 e 100")
            if data_scadenza is None:
                raise OffertaValidazioneException("La data di scadenza è obbligatoria per una promozione")
            ds = data_scadenza if data_scadenza.tzinfo else data_scadenza.replace(tzinfo=timezone.utc)
            if ds <= datetime.now(timezone.utc):
                raise OffertaValidazioneException("La data di scadenza deve essere nel futuro")
        if tipo == "abbonamento":
            if prezzo is None:
                raise OffertaValidazioneException("Il prezzo è obbligatorio per un abbonamento")
            if prezzo <= 0:
                raise OffertaValidazioneException("Il prezzo deve essere maggiore di zero")
            if durata_giorni is None:
                raise OffertaValidazioneException("La durata in giorni è obbligatoria per un abbonamento")
            if durata_giorni <= 0:
                raise OffertaValidazioneException("La durata deve essere maggiore di zero")
