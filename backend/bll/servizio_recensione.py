from uuid import UUID
from dal.recensione_repository import RecensioneRepository


class VotoNonValidoException(Exception):
    pass


class ServizioRecensione:
    """[IF-UT.15] BLL per la scrittura di recensioni utente."""

    def __init__(self) -> None:
        self._repo = RecensioneRepository()

    # [IF-UT.15] Scrive Recensione
    def valida_voto(self, voto: int) -> bool:
        return 1 <= voto <= 5

    # [IF-UT.15] Scrive Recensione
    def scrivi_recensione(self, utente_id: UUID, voto: int, commento: str | None) -> dict:
        if not self.valida_voto(voto):
            raise VotoNonValidoException("Il voto deve essere compreso tra 1 e 5")
        recensione = self._repo.save(utente_id, voto, commento)
        return {
            "id": str(recensione.id),
            "voto": recensione.voto,
            "commento": recensione.commento,
            "created_at": recensione.created_at.isoformat(),
        }
