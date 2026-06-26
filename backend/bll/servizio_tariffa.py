from decimal import Decimal
from uuid import UUID
from dal.tariffa_repository import TariffaRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
    pass


def _a_decimal(valore: float | None) -> Decimal | None:
    return Decimal(str(valore)) if valore is not None else None


def _tariffa_a_dict(tariffa) -> dict:
    return {
        "id": str(tariffa.id),
        "tipo_mezzo": tariffa.tipo_mezzo,
        "costo_al_minuto": float(tariffa.costo_al_minuto) if tariffa.costo_al_minuto is not None else None,
        "costo_al_km": float(tariffa.costo_al_km) if tariffa.costo_al_km is not None else None,
    }


def _descrivi(tariffa) -> str:
    return (
        f"tipo_mezzo={tariffa.tipo_mezzo}, "
        f"costo_al_minuto={tariffa.costo_al_minuto}, "
        f"costo_al_km={tariffa.costo_al_km}"
    )


class ServizioTariffa:
    """[IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa."""

    def __init__(self, tariffa_repo: TariffaRepository | None = None):
        self._tariffa_repo = tariffa_repo or TariffaRepository()
        self._storico = ServizioStoricoModifiche()

    def get_tariffe(self) -> list[dict]:
        tariffe = self._tariffa_repo.find_all()
        return [_tariffa_a_dict(t) for t in tariffe]

    def crea_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None, operatore_id: UUID
    ) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            _a_decimal(costo_al_minuto),
            _a_decimal(costo_al_km),
        )
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_creata",
            descrizione=f"Creazione tariffa '{tipo_mezzo}'",
            valore_precedente=None,
            valore_nuovo=_descrivi(tariffa),
            operatore_id=operatore_id,
        )
        return _tariffa_a_dict(tariffa)

    def aggiorna_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float | None, costo_al_km: float | None, operatore_id: UUID
    ) -> dict:
        precedenti = [t for t in self._tariffa_repo.find_all() if t.tipo_mezzo == tipo_mezzo]
        precedente = precedenti[0] if precedenti else None
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            _a_decimal(costo_al_minuto),
            _a_decimal(costo_al_km),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_modificata",
            descrizione=f"Modifica tariffa '{tipo_mezzo}'",
            valore_precedente=_descrivi(precedente) if precedente is not None else None,
            valore_nuovo=_descrivi(tariffa),
            operatore_id=operatore_id,
        )
        return _tariffa_a_dict(tariffa)
