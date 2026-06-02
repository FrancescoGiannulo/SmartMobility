import pytest
import uuid as _uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_TEST = 41.11
LNG_TEST = 16.85


# ── Helpers ────────────────────────────────────────────────────────────────

def _login(email: str, password: str) -> str:
    import httpx
    r = httpx.post("http://localhost:8000/auth/login",
                   json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _inserisci_mezzo(db, codice: str, stato: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_TEST, "lng": LNG_TEST})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM prenotazioni WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


# ── TestMezzoRepository ────────────────────────────────────────────────────

class TestMezzoRepository:

    @pytest.mark.integration
    def test_trova_per_id_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-TR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            mezzo = repo.trova_per_id(_uuid.UUID(mezzo_id))
            assert mezzo is not None
            assert mezzo["stato"] == "Disponibile"
            assert mezzo["codice"] == codice
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_per_id_non_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        assert MezzoRepository(db).trova_per_id(_uuid.uuid4()) is None

    @pytest.mark.integration
    def test_aggiorna_stato(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-AS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            repo.aggiorna_stato(_uuid.UUID(mezzo_id), "In uso")
            assert repo.trova_per_id(_uuid.UUID(mezzo_id))["stato"] == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_sbloccabili_disponibili_vicini(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-SB-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            risultato = repo.trova_sbloccabili(utente_test["id"], LAT_TEST, LNG_TEST)
            ids = [r["id"] for r in risultato]
            assert mezzo_id in ids
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_sbloccabili_prenotati_dall_utente(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-SBP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]), "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            repo = MezzoRepository(db)
            risultato = repo.trova_sbloccabili(utente_test["id"], LAT_TEST, LNG_TEST)
            item = next((r for r in risultato if r["id"] == mezzo_id), None)
            assert item is not None
            assert item["prenotato"] is True
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_sbloccabili_esclude_lontani(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-SBL-{_uuid.uuid4().hex[:6]}"
        # Mezzo a Roma (~900 km di distanza da Bari)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
                VALUES (:codice, 'monopattino', 'Disponibile', 41.90, 12.49, 80)
            """), {"codice": codice})
            s.commit()
            row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
            mezzo_id = str(row.id)
        try:
            repo = MezzoRepository(db)
            risultato = repo.trova_sbloccabili(utente_test["id"], LAT_TEST, LNG_TEST, raggio_km=0.5)
            ids = [r["id"] for r in risultato]
            assert mezzo_id not in ids
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestCorsaRepository ────────────────────────────────────────────────────

class TestCorsaRepository:

    @pytest.mark.integration
    def test_crea_corsa_diretta(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-CR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            corsa = CorsaRepository(db).crea(utente_test["id"], _uuid.UUID(mezzo_id), None)
            assert corsa["stato"] == "in_uso"
            assert corsa["prenotazione_id"] is None
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestServizioMobilita ───────────────────────────────────────────────────

class TestServizioMobilita:

    @pytest.mark.integration
    def test_sblocca_singolo_disponibile(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SM-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            svc = ServizioMobilita(db)
            risultato = svc.sblocca_mezzi([_uuid.UUID(mezzo_id)], utente_test["id"])
            assert len(risultato["sbloccati"]) == 1
            assert len(risultato["falliti"]) == 0
            assert risultato["sbloccati"][0]["mezzo_id"] == mezzo_id
            with Session(db) as s:
                row = s.execute(text("SELECT stato FROM mezzi WHERE id = :id"), {"id": mezzo_id}).fetchone()
            assert row.stato == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_da_prenotazione(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SMP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]), "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            svc = ServizioMobilita(db)
            risultato = svc.sblocca_mezzi([_uuid.UUID(mezzo_id)], utente_test["id"])
            assert len(risultato["sbloccati"]) == 1
            corsa_id = risultato["sbloccati"][0]["corsa_id"]
            with Session(db) as s:
                corsa = s.execute(text("SELECT prenotazione_id FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert corsa.prenotazione_id is not None
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_batch_parziale_cs05_01(self, db, utente_test):
        """CS-05.01: un mezzo non disponibile → finisce nei falliti, l'altro viene sbloccato."""
        from bll.servizio_mobilita import ServizioMobilita
        c1 = f"TEST-BP1-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-BP2-{_uuid.uuid4().hex[:6]}"
        id_ok = _inserisci_mezzo(db, c1, "Disponibile")
        id_ko = _inserisci_mezzo(db, c2, "In uso")
        try:
            svc = ServizioMobilita(db)
            risultato = svc.sblocca_mezzi(
                [_uuid.UUID(id_ok), _uuid.UUID(id_ko)], utente_test["id"]
            )
            assert len(risultato["sbloccati"]) == 1
            assert len(risultato["falliti"]) == 1
            assert risultato["sbloccati"][0]["mezzo_id"] == id_ok
            assert id_ko in risultato["falliti"]
        finally:
            _elimina_mezzo(db, id_ok)
            _elimina_mezzo(db, id_ko)

    @pytest.mark.integration
    def test_sblocca_mezzo_non_trovato_nel_batch(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        risultato = ServizioMobilita(db).sblocca_mezzi([_uuid.uuid4()], utente_test["id"])
        assert len(risultato["falliti"]) == 1
        assert len(risultato["sbloccati"]) == 0


# ── TestSbloccaMezzoHTTP ───────────────────────────────────────────────────

class TestSbloccaMezzoHTTP:

    @pytest.mark.integration
    def test_sblocca_singolo_200(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/mezzi/sblocca",
                json={"mezzo_ids": [mezzo_id], "lat": LAT_TEST, "lng": LNG_TEST},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            data = r.json()
            assert len(data["sbloccati"]) == 1
            assert len(data["falliti"]) == 0
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_non_autenticato_401(self, db):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            r = httpx.post(
                "http://localhost:8000/utente/mezzi/sblocca",
                json={"mezzo_ids": [mezzo_id]},
            )
            assert r.status_code == 401
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_get_mezzi_sbloccabili_200(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.get(
                f"http://localhost:8000/utente/mezzi/sbloccabili?lat={LAT_TEST}&lng={LNG_TEST}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            ids = [m["id"] for m in r.json()]
            assert mezzo_id in ids
        finally:
            _elimina_mezzo(db, mezzo_id)