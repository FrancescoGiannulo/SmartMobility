from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.corsa_repository import CorsaRepository
from dal.prenotazione_repository import PrenotazioneRepository


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class CorsaNonTrovataException(Exception):
    pass


class ServizioMobilita:

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._corsa_repo = CorsaRepository(db)
        self._pren_repo = PrenotazioneRepository(db)

    # [IF-UT.04] CS-10 — Sblocca Mezzo
    def sblocca_mezzo(self, mezzo_id: UUID, utente_id: UUID) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")

        stato = mezzo["stato"]
        prenotazione_id = None

        if stato == "Disponibile":
            pass  # sblocco diretto — CS-10 scenario base
        elif stato == "Prenotato":
            pren = self._pren_repo.trova_attiva_per_utente_e_mezzo(
                utente_id, mezzo_id
            )
            if pren is None:
                raise MezzoNonDisponibileException(
                    "Mezzo prenotato da un altro utente"
                )
            prenotazione_id = pren["id"]
        else:
            raise MezzoNonDisponibileException(
                f"Mezzo non disponibile (stato: {stato})"
            )

        corsa = self._corsa_repo.crea(utente_id, mezzo_id, prenotazione_id)

        if prenotazione_id:
            self._pren_repo.aggiorna_stato(UUID(prenotazione_id), "convertita")

        self._mezzo_repo.aggiorna_stato(mezzo_id, "In uso")

        return corsa

    # [IF-UT.06] CS-11 — Termina Corsa (minimale: aggiorna stati)
    def termina_corsa(self, corsa_id: UUID, utente_id: UUID) -> None:
        corsa = self._corsa_repo.trova_per_id(corsa_id)
        if corsa is None:
            raise CorsaNonTrovataException(f"Corsa {corsa_id} non trovata")
        self._corsa_repo.aggiorna_stato(corsa_id, "terminata")
        self._mezzo_repo.aggiorna_stato(UUID(corsa["mezzo_id"]), "Disponibile")
