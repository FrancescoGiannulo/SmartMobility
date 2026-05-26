from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.prenotazione_repository import PrenotazioneRepository


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class PrenotazioneNonTrovataException(Exception):
    pass


class ServizioPrenotazione:
    """Ciclo di vita delle prenotazioni: creazione, scadenza, cancellazione."""

    DURATA_MINUTI = 30

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._pren_repo = PrenotazioneRepository(db)

    # [IF-UT.02] CS-XX — Annulla prenotazione attiva
    def annulla_prenotazione(self, prenotazione_id: UUID, utente_id: UUID) -> None:
        pren = self._pren_repo.trova_attiva_per_id_e_utente(prenotazione_id, utente_id)
        if pren is None:
            raise PrenotazioneNonTrovataException(f"Prenotazione {prenotazione_id} non trovata")
        self._pren_repo.aggiorna_stato(prenotazione_id, "annullata")
        self._mezzo_repo.aggiorna_stato(UUID(pren["mezzo_id"]), "Disponibile")

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
