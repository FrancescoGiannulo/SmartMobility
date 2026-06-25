from uuid import UUID
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from dal.zona_repository import ZonaRepository
from dal.mezzo_repository import MezzoRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class PoligonoNonValidoException(Exception):
    pass


class PoligonoFuoriZonaOperativaException(Exception):
    pass


class ServizioMappa:
    """Funzionalità geografiche: zone, posizioni, validazione perimetri."""

    def __init__(self, db: Session | Engine) -> None:
        self._zone_repo = ZonaRepository(db)
        self._mezzo_repo = MezzoRepository(db)
        self._storico = ServizioStoricoModifiche()

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
        operatore_id: UUID,
    ) -> dict:
        vertici_distinti = {tuple(c) for c in coordinate}
        if len(vertici_distinti) < 3:
            raise PoligonoNonValidoException("Il poligono deve avere almeno 3 vertici distinti")
        if coordinate[0] != coordinate[-1]:
            coordinate = coordinate + [coordinate[0]]
        # [IF-OP.02] Zone non-operative devono essere contenute in una zona operativa
        if tipo != "operativa":
            if not self._zone_repo.esiste_zona_operativa_contenente(coordinate):
                raise PoligonoFuoriZonaOperativaException(
                    "La zona deve essere disegnata all'interno del confine operativo"
                )
        zona = self._zone_repo.crea(nome, tipo, coordinate, limite_velocita)
        creata = self._zone_repo.trova_per_id(zona.id)
        self._storico.registra_modifica(
            tipo_configurazione="zona_creata",
            descrizione=f"Creazione zona '{nome}' (tipo: {tipo})",
            valore_precedente=None,
            valore_nuovo=f"nome={nome}, tipo={tipo}, limite_velocita={limite_velocita}",
            operatore_id=operatore_id,
        )
        return creata

    def elimina_zona(self, zona_id: UUID, operatore_id: UUID) -> None:
        zona = self._zone_repo.trova_per_id(zona_id)
        self._zone_repo.elimina(zona_id)
        self._storico.registra_modifica(
            tipo_configurazione="zona_eliminata",
            descrizione=f"Eliminazione zona '{zona['nome']}'",
            valore_precedente=f"nome={zona['nome']}, tipo={zona['tipo']}",
            valore_nuovo=None,
            operatore_id=operatore_id,
        )

    # [IF-OP.11] Verifica che la posizione ricada in una zona operativa attiva
    def verifica_posizione_in_zona_operativa(self, lat: float, lng: float) -> bool:
        return self._zone_repo.punto_in_zona_operativa(lat, lng)

    # [IF-OP.01] Helper demo di presentazione: aggiorna la posizione di un mezzo.
    # La posizione non è uno stato del mezzo: resta in ServizioMappa (servizio geografico).
    def aggiorna_posizione_mezzo(self, id_mezzo: UUID, lat: float, lng: float) -> None:
        self._mezzo_repo.aggiorna_posizione(id_mezzo, lat, lng)
