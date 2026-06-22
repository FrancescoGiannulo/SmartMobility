from uuid import UUID
from config import engine
from dal.recensione_repository import RecensioneRepository
from dal.corsa_repository import CorsaRepository


class VotoNonValidoException(Exception):
    pass


class CorsaNonConclusaException(Exception):
    pass


class ServizioRecensione:
    """[IF-UT.15] BLL per la scrittura di recensioni utente.
    [IF-OP.12] BLL per la consultazione recensioni lato Operatore."""

    def __init__(self) -> None:
        self._repo = RecensioneRepository()
        self._corsa_repo = CorsaRepository(engine)

    # [IF-UT.15] Scrive Recensione
    def valida_voto(self, voto: int) -> bool:
        return 1 <= voto <= 5

    # [IF-UT.15] Scrive Recensione — precondizione 2 dello use case UT-15
    def ha_corsa_conclusa(self, utente_id: UUID) -> bool:
        return self._corsa_repo.ha_corsa_conclusa(utente_id)

    # [IF-UT.15] Scrive Recensione
    def scrivi_recensione(self, utente_id: UUID, voto: int, commento: str | None) -> dict:
        if not self.valida_voto(voto):
            raise VotoNonValidoException("Il voto deve essere compreso tra 1 e 5")
        if not self.ha_corsa_conclusa(utente_id):
            raise CorsaNonConclusaException(
                "Devi aver concluso almeno una corsa per lasciare una recensione"
            )
        recensione = self._repo.save(utente_id, voto, commento)
        return {
            "id": str(recensione.id),
            "voto": recensione.voto,
            "commento": recensione.commento,
            "created_at": recensione.created_at.isoformat(),
        }

    # [IF-UT.15] Le mie recensioni
    def get_mie_recensioni(self, utente_id: UUID) -> list[dict]:
        return [
            {
                "id": str(r.id),
                "voto": r.voto,
                "commento": r.commento,
                "created_at": r.created_at.isoformat(),
            }
            for r in self._repo.find_by_utente_id(utente_id)
        ]

    # [IF-OP.12] Visualizza Recensioni — calcolo voto medio (self-call del SD)
    def _calcola_voto_medio(self, recensioni: list) -> float:
        if not recensioni:
            return 0.0
        return round(sum(r.voto for r in recensioni) / len(recensioni), 1)

    # [IF-OP.12] Visualizza Recensioni — elenco recensioni + voto medio aggregato
    def get_recensioni(self) -> dict:
        recensioni = self._repo.find_all()
        return {
            "recensioni": [
                {
                    "id": str(r.id),
                    "voto": r.voto,
                    "commento": r.commento,
                    "created_at": r.created_at.isoformat(),
                }
                for r in recensioni
            ],
            "voto_medio": self._calcola_voto_medio(recensioni),
        }
