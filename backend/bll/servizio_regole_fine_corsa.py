from decimal import Decimal
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from dal.regola_fine_corsa_repository import RegoleFineCorsaRepository
from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa
from bll.servizio_storico_modifiche import ServizioStoricoModifiche

_VALORI_TIPO_VINCOLO = {v.value for v in TipoVincoloFinecorsa}


class RegolaFinecorsaValidazioneException(Exception):
    pass


class ServizioRegolaFinecorsa:
    """BLL per la gestione delle regole di fine corsa [IF-OP.06]."""

    def __init__(self):
        self._repo = RegoleFineCorsaRepository()
        self._storico = ServizioStoricoModifiche()

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
        operatore_id: UUID,
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
        if tipo_vincolo == "penale" and penale_fuori_zona <= Decimal("0"):
            raise RegolaFinecorsaValidazioneException(
                "penale_fuori_zona deve essere maggiore di 0 quando tipo_vincolo è 'penale'."
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
        has_bonus_count = bonus_parcheggi_corretti is not None
        has_bonus_value = bonus_valore is not None
        if has_bonus_count != has_bonus_value:
            raise RegolaFinecorsaValidazioneException(
                "bonus_parcheggi_corretti e bonus_valore devono essere forniti insieme."
            )

        precedente = self._repo.get_corrente(db)
        # Snapshot dei valori precedenti in stringhe semplici PRIMA di chiamare salva():
        # get_corrente() e salva() condividono la stessa Session, quindi per l'identity
        # map di SQLAlchemy restituiscono lo stesso oggetto Python — se teniamo solo il
        # riferimento all'oggetto, salva() lo muta e "precedente" finisce per coincidere
        # con il nuovo valore.
        valore_precedente_snapshot = (
            f"tipo_vincolo={precedente.tipo_vincolo.value}, "
            f"penale_fuori_zona={precedente.penale_fuori_zona}, "
            f"batteria_minima={precedente.batteria_minima}, "
            f"bonus_parcheggi_corretti={precedente.bonus_parcheggi_corretti}, "
            f"bonus_valore={precedente.bonus_valore}"
        ) if precedente is not None else None
        tipo_vincolo_enum = TipoVincoloFinecorsa(tipo_vincolo)
        aggiornata = self._repo.salva(
            tipo_vincolo=tipo_vincolo_enum,
            penale_fuori_zona=penale_fuori_zona,
            batteria_minima=batteria_minima,
            bonus_parcheggi_corretti=bonus_parcheggi_corretti,
            bonus_valore=bonus_valore,
            db=db,
        )
        self._storico.registra_modifica(
            tipo_configurazione="regole_fine_corsa_creata" if precedente is None else "regole_fine_corsa_modificata",
            descrizione="Definizione delle regole di fine corsa" if precedente is None else "Modifica delle regole di fine corsa",
            valore_precedente=valore_precedente_snapshot,
            valore_nuovo=(
                f"tipo_vincolo={aggiornata.tipo_vincolo.value}, "
                f"penale_fuori_zona={aggiornata.penale_fuori_zona}, "
                f"batteria_minima={aggiornata.batteria_minima}, "
                f"bonus_parcheggi_corretti={aggiornata.bonus_parcheggi_corretti}, "
                f"bonus_valore={aggiornata.bonus_valore}"
            ),
            operatore_id=operatore_id,
        )
        return aggiornata
