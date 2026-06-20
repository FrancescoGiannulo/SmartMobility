from decimal import Decimal
from dal.tariffa_repository import TariffaRepository


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
    pass


class ServizioTariffa:
    """[IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa."""

    def __init__(self, tariffa_repo: TariffaRepository | None = None):
        self._tariffa_repo = tariffa_repo or TariffaRepository()

    def get_tariffe(self) -> list[dict]:
        tariffe = self._tariffa_repo.find_all()
        return [
            {
                "id": str(t.id),
                "tipo_mezzo": t.tipo_mezzo,
                "costo_al_minuto": float(t.costo_al_minuto),
                "costo_al_km": float(t.costo_al_km),
            }
            for t in tariffe
        ]

    def crea_tariffa(self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }

    def aggiorna_tariffa(self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float) -> dict:
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }
