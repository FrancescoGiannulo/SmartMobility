import pytest
import uuid as _uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session


LAT_TEST = 41.11
LNG_TEST = 16.85


def _inserisci_mezzo(db, codice: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', 'Disponibile', :lat, :lng, 80)
        """), {"codice": codice, "lat": LAT_TEST, "lng": LNG_TEST})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _inserisci_corsa(db, utente_id, mezzo_id, stato="terminata",
                     gruppo_corsa_id=None, minuti_fa=0) -> str:
    now = datetime.now(timezone.utc) - timedelta(minutes=minuti_fa)
    fine = now + timedelta(minutes=30)
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, stato, inizio_at, fine_at,
                 distanza_km, gruppo_corsa_id)
            VALUES
                (:id, :uid, :mid, :stato, :inizio, :fine,
                 3.5, :gruppo)
        """), {
            "id": str(_uuid.uuid4()),
            "uid": str(utente_id),
            "mid": mezzo_id,
            "stato": stato,
            "inizio": now,
            "fine": fine,
            "gruppo": str(gruppo_corsa_id) if gruppo_corsa_id else None,
        })
        s.commit()
        row = s.execute(
            text("SELECT id FROM corse WHERE utente_id = :uid ORDER BY inizio_at DESC LIMIT 1"),
            {"uid": str(utente_id)}
        ).fetchone()
    return str(row.id)


def _cleanup(db, utente_id, mezzo_ids):
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE utente_id = :uid"),
                  {"uid": str(utente_id)})
        for mid in mezzo_ids:
            s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mid})
        s.commit()


class TestCorsaRepository:

    @pytest.mark.integration
    def test_crea_con_gruppo_corsa_id(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-GRP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        gruppo_id = _uuid.uuid4()
        try:
            repo = CorsaRepository(db)
            corsa = repo.crea(utente_test["id"], _uuid.UUID(mezzo_id),
                              None, gruppo_id)
            assert corsa["gruppo_corsa_id"] == str(gruppo_id)
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_find_by_utente_restituisce_solo_terminate(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-ST-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id, stato="terminata")
            _inserisci_corsa(db, utente_test["id"], mezzo_id, stato="in_uso")
            repo = CorsaRepository(db)
            risultato = repo.find_by_utente_order_by_data(utente_test["id"])
            assert len(risultato) == 1
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_find_by_utente_ordina_per_data_decrescente(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice1 = f"TEST-ORD1-{_uuid.uuid4().hex[:6]}"
        codice2 = f"TEST-ORD2-{_uuid.uuid4().hex[:6]}"
        mezzo1 = _inserisci_mezzo(db, codice1)
        mezzo2 = _inserisci_mezzo(db, codice2)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo1, minuti_fa=60)
            _inserisci_corsa(db, utente_test["id"], mezzo2, minuti_fa=10)
            repo = CorsaRepository(db)
            risultato = repo.find_by_utente_order_by_data(utente_test["id"])
            assert len(risultato) == 2
            assert risultato[0]["codice_mezzo"] == codice2
            assert risultato[1]["codice_mezzo"] == codice1
        finally:
            _cleanup(db, utente_test["id"], [mezzo1, mezzo2])
