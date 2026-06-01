from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session

from dal.regola_fine_corsa_repository import RegolaFinecorsaRepository
from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa

_VALORI_TIPO_VINCOLO = {v.value for v in TipoVincoloFinecorsa}


class RegolaFinecorsaValidazioneException(Exception):
    pass


class ServizioRegolaFinecorsa:
    """BLL per la gestione delle regole di fine corsa [IF-OP.13]."""

    def __init__(self):
        self._repo = RegolaFinecorsaRepository()

    def get_corrente(self, db: Session) -> Optional[RegolaFinecorsa]:
        """Restituisce la configurazione globale corrente, o None se non ancora impostata."""
        return self._repo.get_corrente(db)

    def salva(
        self,
        tipo_vincolo: str,
        penale_fuori_zona: Decimal,
        batteria_minima: Optional[int],
        bonus_parcheggi_corretti: Optional[int],
        bonus_valore: Optional[Decimal],
        db: Session,
    ) -> RegolaFinecorsa:
        """Valida e persiste (upsert) la configurazione globale delle regole di fine corsa."""
        if tipo_vincolo not in _VALORI_TIPO_VINCOLO:
            raise RegolaFinecorsaValidazioneException(
                f"tipo_vincolo non valido: '{tipo_vincolo}'. "
                f"Valori ammessi: {sorted(_VALORI_TIPO_VINCOLO)}"
            )
        if penale_fuori_zona < Decimal("0"):
            raise RegolaFinecorsaValidazioneException(
                "penale_fuori_zona non può essere negativa."
            )
        if batteria_minima is not None and not (0 <= batteria_minima <= 100):
            raise RegolaFinecorsaValidazioneException(
                "batteria_minima deve essere compresa tra 0 e 100."
            )
        if bonus_parcheggi_corretti is not None and bonus_parcheggi_corretti <= 0:
            raise RegolaFinecorsaValidazioneException(
                "bonus_parcheggi_corretti deve essere maggiore di 0."
            )
        if bonus_valore is not None and bonus_valore <= Decimal("0"):
            raise RegolaFinecorsaValidazioneException(
                "bonus_valore deve essere maggiore di 0."
            )

        tipo_vincolo_enum = TipoVincoloFinecorsa(tipo_vincolo)
        return self._repo.salva(
            tipo_vincolo=tipo_vincolo_enum,
            penale_fuori_zona=penale_fuori_zona,
            batteria_minima=batteria_minima,
            bonus_parcheggi_corretti=bonus_parcheggi_corretti,
            bonus_valore=bonus_valore,
            db=db,
        )
