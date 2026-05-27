from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.prenotazione_repository import PrenotazioneRepository


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class ServizioPrenotazione:
    """Ciclo di vita delle prenotazioni: creazione, scadenza, cancellazione."""

    DURATA_MINUTI = 30

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._pren_repo = PrenotazioneRepository(db)

    # [IF-UT.02] CS-XX — Prenota Mezzo
    def crea_prenotazione(self, mezzo_id: UUID, utente_id: UUID) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        if mezzo["stato"] != "Disponibile":
            raise MezzoNonDisponibileException(
                f"Mezzo non disponibile (stato: {mezzo['stato']})"
            )
        prenotazione = self._pren_repo.crea(utente_id, mezzo_id, self.DURATA_MINUTI)
        self._mezzo_repo.aggiorna_stato(mezzo_id, "Prenotato")
        return prenotazione
