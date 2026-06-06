import pytest
import uuid as _uuid
import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8000"
LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _login_op(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _elimina_mezzo(db, codice: str) -> None:
    with Session(db) as s:
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
        if row:
            s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": str(row.id)})
            s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": str(row.id)})
            s.commit()


def _inserisci_zona_operativa(db) -> str:
    with Session(db) as s:
        row = s.execute(text("""
            INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
            VALUES ('ZonaTestHTTP', 'operativa',
                ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.8,41.0],[16.95,41.0],[16.95,41.2],[16.8,41.2],[16.8,41.0]]]}'),
                NULL)
            RETURNING id
        """)).fetchone()
        s.commit()
        assert row is not None
        return str(row.id)


def _elimina_zona(db, zona_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
        s.commit()


class TestAggiungiMezzoHTTP:

    @pytest.mark.integration
    def test_get_mezzi_flotta_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/mezzi", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @pytest.mark.integration
    def test_post_mezzo_201(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        zona_id = _inserisci_zona_operativa(db)
        codice = f"HTTP-OK-{_uuid.uuid4().hex[:6]}"
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi",
                json={"tipo": "monopattino", "codice": codice, "lat": LAT_BARI, "lng": LNG_BARI},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["codice"] == codice
        finally:
            _elimina_mezzo(db, codice)
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_post_mezzo_409_duplicato(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        zona_id = _inserisci_zona_operativa(db)
        codice = f"HTTP-DUP-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi",
                json={"tipo": "monopattino", "codice": codice, "lat": LAT_BARI, "lng": LNG_BARI},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, codice)
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_verifica_dismissione_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        codice = f"HTTP-VD-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
            row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
            assert row is not None
            mezzo_id = str(row.id)
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi/{mezzo_id}/verifica",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200
            assert r.json()["dismettibile"] is True
        finally:
            _elimina_mezzo(db, codice)

    @pytest.mark.integration
    def test_delete_mezzo_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        codice = f"HTTP-DEL-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
            row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
            assert row is not None
            mezzo_id = str(row.id)
        try:
            r = httpx.delete(
                f"{BASE}/operatore/mezzi/{mezzo_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200
        finally:
            _elimina_mezzo(db, codice)
