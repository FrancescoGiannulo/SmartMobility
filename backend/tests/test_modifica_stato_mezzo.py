import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _inserisci_mezzo(db, codice: str, stato: str = "Disponibile") -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_BARI, "lng": LNG_BARI})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


class TestServizioMobilitaModificaStato:

    # OP-04 — sequenza principale
    @pytest.mark.integration
    def test_modifica_stato_mezzo_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-MS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            with Session(db) as s:
                ServizioMobilita(s).modifica_stato_mezzo(_uuid.UUID(mezzo_id), "In manutenzione")
            assert MezzoRepository(db).trova_per_id(_uuid.UUID(mezzo_id))["stato"] == "In manutenzione"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_modifica_stato_mezzo_non_trovato(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonTrovatoException
        with Session(db) as s:
            with pytest.raises(MezzoNonTrovatoException):
                ServizioMobilita(s).modifica_stato_mezzo(_uuid.uuid4(), "Disponibile")

    # OP-04.1 — sequenza alternativa: mezzo in uso/prenotato
    @pytest.mark.integration
    def test_modifica_stato_mezzo_in_missione(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoInMissioneException
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-MI-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            with Session(db) as s:
                with pytest.raises(MezzoInMissioneException):
                    ServizioMobilita(s).modifica_stato_mezzo(_uuid.UUID(mezzo_id), "Disponibile")
            assert MezzoRepository(db).trova_per_id(_uuid.UUID(mezzo_id))["stato"] == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)
