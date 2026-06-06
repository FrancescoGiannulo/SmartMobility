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


class ServizioOfferta:

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
        tipo_mezzo: Optional[str] = None,
    ) -> Offerta:
        self._valida(
            nome=nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_scadenza=data_scadenza,
            tipo_mezzo=tipo_mezzo,
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
                tipo_mezzo=tipo_mezzo,
            )
        except NomeDuplicatoException:
            raise OffertaDuplicataException(f"Esiste già un'offerta con nome '{nome}'")

    def modifica_offerta(
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
        try:
            offerta_corrente = self._repo.trova_per_id(offerta_id, db)
        except OffertaNonTrovataException:
            raise OffertaValidazioneException(f"Offerta {offerta_id} non trovata")
        tipo = offerta_corrente.tipo
        self._valida(
            nome=nome or offerta_corrente.nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale if sconto_percentuale is not None else offerta_corrente.sconto_percentuale,
            prezzo=prezzo if prezzo is not None else offerta_corrente.prezzo,
            durata_giorni=durata_giorni if durata_giorni is not None else offerta_corrente.durata_giorni,
            data_scadenza=data_scadenza if data_scadenza is not None else offerta_corrente.data_scadenza,
            tipo_mezzo=tipo_mezzo if tipo_mezzo is not None else offerta_corrente.tipo_mezzo,
        )
        try:
            return self._repo.aggiorna(
                offerta_id=offerta_id,
                db=db,
                nome=nome,
                descrizione=descrizione,
                sconto_percentuale=sconto_percentuale,
                prezzo=prezzo,
                durata_giorni=durata_giorni,
                data_inizio=data_inizio,
                data_scadenza=data_scadenza,
                stato=stato,
                tipo_mezzo=tipo_mezzo,
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
        tipo_mezzo: Optional[str] = None,
    ) -> None:
        if not nome or not nome.strip():
            raise OffertaValidazioneException("Il nome è obbligatorio")
        if tipo not in ("promozione", "abbonamento"):
            raise OffertaValidazioneException("Tipo non valido: usa 'promozione' o 'abbonamento'")
        if tipo_mezzo is not None and tipo_mezzo not in ("monopattino", "bicicletta", "automobile"):
            raise OffertaValidazioneException("tipo_mezzo non valido: usa 'monopattino', 'bicicletta' o 'automobile'")
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
