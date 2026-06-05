from decimal import Decimal
from sqlalchemy.orm import Session

from dal.parametri_sistema_repository import ParametriSistemaRepository
from model.parametri_sistema import ParametriSistema


class ParametriValidazioneException(Exception):
    pass


class ServizioParametri:
    """[CS-15] BLL per la gestione dei parametri numerici di sistema (IF-OP.08/09/10/14)."""

    def __init__(self):
        self._repo = ParametriSistemaRepository()

    def get_parametri(self, db: Session) -> ParametriSistema:
        return self._repo.get(db)

    def aggiorna_parametri(
        self,
        durata_max_prenotazione_min: int,
        durata_periodo_grazia_min: int,
        max_mezzi_per_utente: int,
        addebito_pausa_min: Decimal,
        db: Session,
    ) -> ParametriSistema:
        if durata_max_prenotazione_min < 0:
            raise ParametriValidazioneException(
                "durata_max_prenotazione_min non può essere negativa."
            )
        if durata_periodo_grazia_min < 0:
            raise ParametriValidazioneException(
                "durata_periodo_grazia_min non può essere negativa."
            )
        if max_mezzi_per_utente < 1:
            raise ParametriValidazioneException(
                "max_mezzi_per_utente deve essere un intero positivo (>= 1)."
            )
        if addebito_pausa_min < Decimal("0"):
            raise ParametriValidazioneException(
                "addebito_pausa_min non può essere negativo."
            )
        return self._repo.save(
            durata_max_prenotazione_min=durata_max_prenotazione_min,
            durata_periodo_grazia_min=durata_periodo_grazia_min,
            max_mezzi_per_utente=max_mezzi_per_utente,
            addebito_pausa_min=addebito_pausa_min,
            db=db,
        )
