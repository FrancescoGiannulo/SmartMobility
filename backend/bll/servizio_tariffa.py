from decimal import Decimal
from uuid import UUID
from dal.tariffa_repository import TariffaRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
    pass


class ServizioTariffa:
    """[IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa."""

    def __init__(self, tariffa_repo: TariffaRepository | None = None):
        self._tariffa_repo = tariffa_repo or TariffaRepository()
        self._storico = ServizioStoricoModifiche()

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

    def crea_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID
    ) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_creata",
            descrizione=f"Creazione tariffa '{tipo_mezzo}'",
            valore_precedente=None,
            valore_nuovo=(
                f"tipo_mezzo={tariffa.tipo_mezzo}, "
                f"costo_al_minuto={tariffa.costo_al_minuto}, "
                f"costo_al_km={tariffa.costo_al_km}"
            ),
            operatore_id=operatore_id,
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }

    def aggiorna_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID
    ) -> dict:
        precedenti = [t for t in self._tariffa_repo.find_all() if t.tipo_mezzo == tipo_mezzo]
        precedente = precedenti[0] if precedenti else None
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_modificata",
            descrizione=f"Modifica tariffa '{tipo_mezzo}'",
            valore_precedente=(
                f"tipo_mezzo={precedente.tipo_mezzo}, "
                f"costo_al_minuto={precedente.costo_al_minuto}, "
                f"costo_al_km={precedente.costo_al_km}"
            ) if precedente is not None else None,
            valore_nuovo=(
                f"tipo_mezzo={tariffa.tipo_mezzo}, "
                f"costo_al_minuto={tariffa.costo_al_minuto}, "
                f"costo_al_km={tariffa.costo_al_km}"
            ),
            operatore_id=operatore_id,
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }
