from uuid import UUID
from sqlalchemy.orm import Session
from dal.segnalazione_repository import SegnalazioneRepository, SegnalazioneNonTrovataException
from model.segnalazione import StatoSegnalazione


class SegnalazioneNonTrovata(Exception):
    pass


class TransizioneNonValida(Exception):
    pass


class ServizioSegnalazione:
    """[IF-UT.12 / IF-OP.08] BLL per la gestione delle segnalazioni utente."""

    def __init__(self, db: Session) -> None:
        self._repo = SegnalazioneRepository()

    # [IF-UT.12] Le mie segnalazioni
    def get_mie_segnalazioni(self, utente_id: UUID) -> list[dict]:
        return [
            {
                "id": str(s.id),
                "tipologia": s.tipologia,
                "descrizione": s.descrizione,
                "stato": s.stato,
                "created_at": s.created_at.isoformat(),
            }
            for s in self._repo.find_by_utente(utente_id)
        ]

    # [IF-UT.12] Invia Segnalazione
    def registra_segnalazione(self, utente_id: UUID, tipologia: str, descrizione: str) -> dict:
        segnalazione = self._repo.crea(utente_id, tipologia, descrizione)
        return {
            "id": str(segnalazione.id),
            "tipologia": segnalazione.tipologia,
            "descrizione": segnalazione.descrizione,
            "stato": segnalazione.stato,
            "created_at": segnalazione.created_at.isoformat(),
        }

    # [IF-OP.08] Lista segnalazioni (operatore)
    def get_segnalazioni(self) -> list[dict]:
        return [
            {
                "id": str(s["id"]),
                "utente_id": str(s["utente_id"]),
                "tipologia": s["tipologia"],
                "descrizione": s["descrizione"],
                "stato": s["stato"],
                "created_at": s["created_at"].isoformat(),
                "nome_utente": s["nome_utente"],
            }
            for s in self._repo.find_all()
        ]

    # [IF-OP.08] Dettaglio segnalazione
    def get_dettaglio_segnalazione(self, segnalazione_id: UUID) -> dict:
        s = self._repo.find_by_id(segnalazione_id)
        if not s:
            raise SegnalazioneNonTrovata(f"Segnalazione {segnalazione_id} non trovata")
        return {
            "id": str(s["id"]),
            "utente_id": str(s["utente_id"]),
            "tipologia": s["tipologia"],
            "descrizione": s["descrizione"],
            "stato": s["stato"],
            "created_at": s["created_at"].isoformat(),
            "nome_utente": s["nome_utente"],
        }

    # [IF-OP.08] Prendi in carico
    def prendi_in_carico(self, segnalazione_id: UUID) -> dict:
        aggiornato = self._repo.aggiorna_stato(segnalazione_id, StatoSegnalazione.in_carico)
        if not aggiornato:
            raise SegnalazioneNonTrovata(f"Segnalazione {segnalazione_id} non trovata")
        return self.get_dettaglio_segnalazione(segnalazione_id)

    # [IF-OP.08] Segna come risolta
    def risolvi(self, segnalazione_id: UUID) -> dict:
        dettaglio = self.get_dettaglio_segnalazione(segnalazione_id)
        if dettaglio["stato"] != StatoSegnalazione.in_carico.value:
            raise TransizioneNonValida(
                f"Impossibile risolvere una segnalazione con stato '{dettaglio['stato']}'"
            )
        self._repo.aggiorna_stato(segnalazione_id, StatoSegnalazione.risolta)
        return self.get_dettaglio_segnalazione(segnalazione_id)
