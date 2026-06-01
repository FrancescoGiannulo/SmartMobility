from sqlalchemy.orm import Session
from dal.tariffa_repository import TariffaRepository
from dal.promozione_repository import PromozioneRepository


class ServizioPricing:
    """Calcolo tariffe, promozioni e addebiti a fine corsa."""

    def __init__(self, db: Session) -> None:
        self._tariffa_repo = TariffaRepository(db)
        self._promozione_repo = PromozioneRepository(db)

    # [IF-UT.05]
    def getTariffe(self) -> list[dict]:
        return self._tariffa_repo.findAll()

    # [IF-UT.13]
    def getPromozioniAttive(self) -> list[dict]:
        return self._promozione_repo.getAttive()
