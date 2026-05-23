from uuid import UUID
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from dal.zona_repository import ZonaRepository
from dal.mezzo_repository import MezzoRepository


class PoligonoNonValidoException(Exception):
    pass


class ServizioGIS:
    """Funzionalità geografiche: zone, posizioni, validazione perimetri."""

    def __init__(self, db: Session | Engine) -> None:
        self._zone_repo = ZonaRepository(db)
        self._mezzo_repo = MezzoRepository(db)

    def ottieni_zone(self) -> list[dict]:
        return self._zone_repo.lista_zone(solo_attive=True)

    def ottieni_mezzi_utente(self) -> list[dict]:
        return self._mezzo_repo.lista_per_mappa(solo_disponibili=True)

    def ottieni_mezzi_operatore(self) -> list[dict]:
        return self._mezzo_repo.lista_per_mappa(solo_disponibili=False)

    def crea_zona(
        self,
        nome: str,
        tipo: str,
        coordinate: list[list[float]],
        limite_velocita: int | None,
    ) -> dict:
        vertici_distinti = {tuple(c) for c in coordinate}
        if len(vertici_distinti) < 3:
            raise PoligonoNonValidoException("Il poligono deve avere almeno 3 vertici distinti")
        if coordinate[0] != coordinate[-1]:
            coordinate = coordinate + [coordinate[0]]
        zona = self._zone_repo.crea(nome, tipo, coordinate, limite_velocita)
        return self._zone_repo.trova_per_id(zona.id)

    def elimina_zona(self, zona_id: UUID) -> None:
        self._zone_repo.elimina(zona_id)
