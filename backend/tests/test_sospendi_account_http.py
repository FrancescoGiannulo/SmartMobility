import pytest
import httpx
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8010"


def _login(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _pulisci_notifiche(db, utente_id) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM notifiche WHERE utente_id = :id"), {"id": str(utente_id)})
        s.commit()


@pytest.mark.integration
class TestUtentiOPControllerHTTP:

    def test_get_utenti_200(self, db, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/utenti", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert any(u["id"] == str(utente_test["id"]) for u in r.json())

    def test_get_utenti_403_per_ruolo_ut(self, utente_test):
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.get(f"{BASE}/operatore/utenti", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 403

    def test_get_dettaglio_utente_200(self, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(
            f"{BASE}/operatore/utenti/{utente_test['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        assert r.json()["email"] == utente_test["email"]

    def test_get_dettaglio_utente_404(self, operatore_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(
            f"{BASE}/operatore/utenti/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    def test_sospendi_account_200(self, db, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        try:
            r = httpx.patch(
                f"{BASE}/operatore/utenti/{utente_test['id']}/stato",
                json={"motivazione": "Comportamento scorretto"},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            assert r.json()["sospeso"] is True
        finally:
            _pulisci_notifiche(db, utente_test["id"])

    def test_sospendi_account_422_motivazione_vuota(self, operatore_test, utente_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{utente_test['id']}/stato",
            json={"motivazione": "   "},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 422

    def test_sospendi_account_409_gia_sospeso(self, operatore_test, utente_sospeso):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{utente_sospeso['id']}/stato",
            json={"motivazione": "Motivo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 409

    def test_sospendi_account_404_non_trovato(self, operatore_test):
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.patch(
            f"{BASE}/operatore/utenti/{uuid4()}/stato",
            json={"motivazione": "Motivo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404
