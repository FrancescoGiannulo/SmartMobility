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


class TestServizioMobilitaDismetti:

    @pytest.mark.integration
    def test_verifica_dismissione_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VD-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is True
            assert ris["motivo"] is None
            assert ris["mezzo"]["id"] == mezzo_id
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_verifica_dismissione_stato_bloccante(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VB-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is False
            assert ris["motivo"] is not None
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_verifica_dismissione_corsa_attiva(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        corsa_id = str(_uuid.uuid4())
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at)
                VALUES (:id, :uid, :mid, 'in_uso', now())
            """), {"id": corsa_id, "uid": str(utente_test["id"]), "mid": mezzo_id})
            s.commit()
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is False
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM corse WHERE id = :id"), {"id": corsa_id})
                s.commit()
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_dismetti_mezzo_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-DM-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            with Session(db) as s:
                ServizioMobilita(s).dismetti_mezzo(_uuid.UUID(mezzo_id))
            assert MezzoRepository(db).trova_per_id(_uuid.UUID(mezzo_id))["stato"] == "Dismesso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_dismetti_mezzo_non_trovato(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonTrovatoException
        with Session(db) as s:
            with pytest.raises(MezzoNonTrovatoException):
                ServizioMobilita(s).dismetti_mezzo(_uuid.uuid4())

    @pytest.mark.integration
    def test_dismetti_mezzo_in_missione(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoInMissioneException
        codice = f"TEST-DI-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            with Session(db) as s:
                with pytest.raises(MezzoInMissioneException):
                    ServizioMobilita(s).dismetti_mezzo(_uuid.UUID(mezzo_id))
        finally:
            _elimina_mezzo(db, mezzo_id)
