from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.prenotazione_repository import PrenotazioneRepository

N_MAX_DEFAULT = 3


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class PrenotazioneNonTrovataException(Exception):
    pass


# [IF-UT.02] CS-04.01 — alcuni mezzi della selezione non più disponibili
class AlcuniMezziNonDisponibiliException(Exception):
    def __init__(self, non_disponibili: list[str]) -> None:
        self.non_disponibili = non_disponibili
        super().__init__(f"Mezzi non disponibili: {non_disponibili}")


class LimiteMezziSuperatoException(Exception):
    pass


class ServizioPrenotazione:
    """Ciclo di vita delle prenotazioni: creazione, scadenza, cancellazione."""

    DURATA_MINUTI = 30

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._pren_repo = PrenotazioneRepository(db)

    # [IF-UT.02] CS-04 — prenotazioni attive dell'utente (per recupero dopo refresh)
    def get_prenotazioni_attive(self, utente_id: UUID) -> list[dict]:
        return self._pren_repo.trova_attive_per_utente(utente_id)

    # [IF-UT.02] CS-04 — caratteristiche mezzo (passo 3 del diagramma di sequenza)
    def get_caratteristiche(self, mezzo_id: UUID) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        return mezzo

    # [IF-UT.02] CS-04 — prenotazione di uno o più mezzi in batch
    def crea_prenotazioni(
        self,
        mezzo_ids: list[UUID],
        utente_id: UUID,
        n_max: int = N_MAX_DEFAULT,
    ) -> list[dict]:
        if not mezzo_ids:
            raise MezzoNonTrovatoException("Nessun mezzo specificato")
        if len(mezzo_ids) > n_max:
            raise LimiteMezziSuperatoException(
                f"Limite massimo {n_max} mezzi per prenotazione"
            )

        # msg18-20: verifica disponibilità di tutti i mezzi richiesti
        disponibili = self._mezzo_repo.trova_disponibili_da_lista(mezzo_ids)
        disponibili_ids = {m["id"] for m in disponibili}
        non_disponibili = [str(mid) for mid in mezzo_ids if str(mid) not in disponibili_ids]

        # msg alt[else] CS-04.01: se anche un solo mezzo non è disponibile, abort
        if non_disponibili:
            raise AlcuniMezziNonDisponibiliException(non_disponibili)

        # msg alt[tutti i mezzi disponibili] — loop per ogni mezzo
        prenotazioni = []
        for mezzo_id in mezzo_ids:
            # msg22-25: aggiorna stato mezzo → "Prenotato"
            self._mezzo_repo.aggiorna_stato(mezzo_id, "Prenotato")
            # msg26-29: crea prenotazione
            pren = self._pren_repo.crea(utente_id, mezzo_id, self.DURATA_MINUTI)
            prenotazioni.append(pren)

        return prenotazioni

    # [IF-UT.02] CS-XX — Annulla prenotazione attiva
    def annulla_prenotazione(self, prenotazione_id: UUID, utente_id: UUID) -> None:
        pren = self._pren_repo.trova_attiva_per_id_e_utente(prenotazione_id, utente_id)
        if pren is None:
            raise PrenotazioneNonTrovataException(f"Prenotazione {prenotazione_id} non trovata")
        self._pren_repo.aggiorna_stato(prenotazione_id, "annullata")
        self._mezzo_repo.aggiorna_stato(UUID(pren["mezzo_id"]), "Disponibile")