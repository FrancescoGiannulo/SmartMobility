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


class TestServizioMobilita:

    @pytest.mark.integration
    def test_sblocca_gruppo_assegna_gruppo_corsa_id(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        from sqlalchemy.orm import Session as OrmSession
        codice1 = f"TEST-SG1-{_uuid.uuid4().hex[:6]}"
        codice2 = f"TEST-SG2-{_uuid.uuid4().hex[:6]}"
        mezzo1 = _inserisci_mezzo(db, codice1)
        mezzo2 = _inserisci_mezzo(db, codice2)
        try:
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                ris = svc.sblocca_mezzi(
                    [_uuid.UUID(mezzo1), _uuid.UUID(mezzo2)],
                    utente_test["id"]
                )
            assert len(ris["sbloccati"]) == 2
            with Session(db) as s:
                corse = s.execute(
                    text("SELECT gruppo_corsa_id FROM corse WHERE utente_id = :uid"),
                    {"uid": str(utente_test["id"])}
                ).fetchall()
            gruppi = [str(c.gruppo_corsa_id) for c in corse if c.gruppo_corsa_id]
            assert len(gruppi) == 2
            assert gruppi[0] == gruppi[1]
        finally:
            _cleanup(db, utente_test["id"], [mezzo1, mezzo2])

    @pytest.mark.integration
    def test_sblocca_singolo_nessun_gruppo_corsa_id(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        from sqlalchemy.orm import Session as OrmSession
        codice = f"TEST-SS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                svc.sblocca_mezzi([_uuid.UUID(mezzo_id)], utente_test["id"])
            with Session(db) as s:
                row = s.execute(
                    text("SELECT gruppo_corsa_id FROM corse WHERE utente_id = :uid"),
                    {"uid": str(utente_test["id"])}
                ).fetchone()
            assert row.gruppo_corsa_id is None
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_get_storico_restituisce_corse(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        from sqlalchemy.orm import Session as OrmSession
        codice = f"TEST-GS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id)
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                storico = svc.get_storico(utente_test["id"])
            assert len(storico) == 1
            assert storico[0]["codice_mezzo"] == codice
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])


class TestStoricoEndpoint:

    def _token(self, email: str, password: str) -> str:
        import httpx
        r = httpx.post("http://localhost:8000/auth/login",
                       json={"email": email, "password": password})
        assert r.status_code == 200
        return r.json()["access_token"]

    @pytest.mark.integration
    def test_storico_vuoto(self, utente_test):
        import httpx
        token = self._token(utente_test["email"], utente_test["password"])
        r = httpx.get("http://localhost:8000/utente/corse/storico",
                      headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json() == []

    @pytest.mark.integration
    def test_storico_con_corse(self, db, utente_test):
        import httpx
        codice = f"TEST-EP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id)
            token = self._token(utente_test["email"], utente_test["password"])
            r = httpx.get("http://localhost:8000/utente/corse/storico",
                          headers={"Authorization": f"Bearer {token}"})
            assert r.status_code == 200
            data = r.json()
            assert len(data) == 1
            assert data[0]["codice_mezzo"] == codice
            assert data[0]["tipo_mezzo"] == "monopattino"
            assert "inizio_at" in data[0]
            assert "gruppo_corsa_id" in data[0]
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_storico_richiede_autenticazione(self):
        import httpx
        r = httpx.get("http://localhost:8000/utente/corse/storico")
        assert r.status_code == 401
