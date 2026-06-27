import pytest
import uuid as _uuid
import httpx
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8000"


def _login_op(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _elimina_tariffa(db, tipo_mezzo: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM tariffe WHERE tipo_mezzo = :t"), {"t": tipo_mezzo})
        s.commit()


# [IF-OP.07] Definisce Tariffa / [IF-OP.08] Modifica Tariffa
class TestTariffaHTTP:

    @pytest.mark.integration
    def test_get_tariffe_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/tariffe", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @pytest.mark.integration
    def test_post_tariffa_201_costo_al_minuto(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["tipo_mezzo"] == tipo_mezzo
            assert r.json()["costo_al_km"] is None
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_201_costo_al_km(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": None, "costo_al_km": 0.10},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["costo_al_minuto"] is None
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_422_entrambi_i_costi(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "automobile"
        _elimina_tariffa(db, tipo_mezzo)
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": 0.10},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 422
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_post_tariffa_409_duplicata(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "bicicletta"
        _elimina_tariffa(db, tipo_mezzo)
        with Session(db) as s:
            s.execute(
                text(
                    "INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) "
                    "VALUES (:t, 0.05, NULL)"
                ),
                {"t": tipo_mezzo},
            )
            s.commit()
        try:
            r = httpx.post(
                f"{BASE}/operatore/tariffe",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.05, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_put_tariffa_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = "monopattino"
        _elimina_tariffa(db, tipo_mezzo)
        with Session(db) as s:
            s.execute(
                text(
                    "INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) "
                    "VALUES (:t, 0.05, NULL)"
                ),
                {"t": tipo_mezzo},
            )
            s.commit()
        try:
            r = httpx.put(
                f"{BASE}/operatore/tariffe/{tipo_mezzo}",
                json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.07, "costo_al_km": None},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            assert Decimal(str(r.json()["costo_al_minuto"])) == Decimal("0.07")
        finally:
            _elimina_tariffa(db, tipo_mezzo)

    @pytest.mark.integration
    def test_put_tariffa_404_inesistente(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        tipo_mezzo = f"inesistente-{_uuid.uuid4().hex[:6]}"
        r = httpx.put(
            f"{BASE}/operatore/tariffe/{tipo_mezzo}",
            json={"tipo_mezzo": tipo_mezzo, "costo_al_minuto": 0.07, "costo_al_km": None},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404
