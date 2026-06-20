from math import radians, cos, sin, asin, sqrt
from uuid import UUID
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.prenotazione_repository import PrenotazioneRepository
from dal.parametri_sistema_repository import ParametriSistemaRepository


# [IF-UT.02] CS-04 — raggio massimo (km) entro cui i mezzi aggiunti al gruppo
# devono trovarsi rispetto al primo mezzo selezionato. Il primo mezzo non ha
# vincolo di distanza; gli altri devono essere "nelle vicinanze" (step 4 del caso d'uso).
RAGGIO_GRUPPO_KM = 0.5


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * asin(sqrt(a))


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


# [IF-UT.02] CS-04 — uno o più mezzi aggiunti sono troppo lontani dal primo del gruppo
class MezziFuoriRaggioGruppoException(Exception):
    def __init__(self, fuori_raggio: list[str]) -> None:
        self.fuori_raggio = fuori_raggio
        super().__init__(f"Mezzi fuori dal raggio di selezione gruppo: {fuori_raggio}")


class LimiteMezziSuperatoException(Exception):
    pass


class ServizioPrenotazione:
    """Ciclo di vita delle prenotazioni: creazione, scadenza, cancellazione."""

    def __init__(self, db: Session) -> None:
        self._mezzo_repo = MezzoRepository(db)
        self._pren_repo = PrenotazioneRepository(db)
        self._parametri_repo = ParametriSistemaRepository()
        self._db = db

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
    ) -> list[dict]:
        parametri = self._parametri_repo.get(self._db)
        durata_minuti = parametri.durata_max_prenotazione_min
        n_max = parametri.max_mezzi_per_utente

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

        # [IF-UT.02] CS-04 — verifica raggio gruppo: il primo mezzo selezionato è il
        # riferimento (nessun vincolo di distanza); gli altri devono trovarsi entro
        # RAGGIO_GRUPPO_KM dal primo (step 4 del caso d'uso "nelle vicinanze")
        if len(mezzo_ids) > 1:
            posizioni = {m["id"]: (m["lat"], m["lng"]) for m in disponibili}
            rif_lat, rif_lng = posizioni[str(mezzo_ids[0])]
            fuori_raggio = []
            if rif_lat is not None and rif_lng is not None:
                for mid in mezzo_ids[1:]:
                    lat, lng = posizioni[str(mid)]
                    if lat is None or lng is None:
                        continue
                    if _haversine_km(rif_lat, rif_lng, lat, lng) > RAGGIO_GRUPPO_KM:
                        fuori_raggio.append(str(mid))
            if fuori_raggio:
                raise MezziFuoriRaggioGruppoException(fuori_raggio)

        # msg alt[tutti i mezzi disponibili] — loop per ogni mezzo
        prenotazioni = []
        for mezzo_id in mezzo_ids:
            # msg22-25: aggiorna stato mezzo → "Prenotato"
            self._mezzo_repo.aggiorna_stato(mezzo_id, "Prenotato")
            # msg26-29: crea prenotazione
            pren = self._pren_repo.crea(utente_id, mezzo_id, durata_minuti)
            prenotazioni.append(pren)

        return prenotazioni

    # [IF-UT.02] CS-XX — Annulla prenotazione attiva
    def annulla_prenotazione(self, prenotazione_id: UUID, utente_id: UUID) -> None:
        pren = self._pren_repo.trova_attiva_per_id_e_utente(prenotazione_id, utente_id)
        if pren is None:
            raise PrenotazioneNonTrovataException(f"Prenotazione {prenotazione_id} non trovata")
        self._pren_repo.aggiorna_stato(prenotazione_id, "annullata")
        self._mezzo_repo.aggiorna_stato(UUID(pren["mezzo_id"]), "Disponibile")
