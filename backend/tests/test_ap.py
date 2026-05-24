import pytest
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def test_ap_mappa_mezzi_autenticato(ap_test):
    """[IF-AP.03] AP autenticata riceve lista mezzi."""
    token = _login(ap_test["email"], ap_test["password"])
    resp = http.get(
        "/ap/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_ap_mappa_mezzi_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/ap/mappa/mezzi")
    assert resp.status_code == 401


def test_ap_mappa_mezzi_ruolo_errato(utente_test):
    """[IIN-2] Token UT su endpoint AP → 403."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.get(
        "/ap/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_ap_mappa_zone_autenticato(ap_test):
    """[IF-AP.03] AP autenticata riceve lista zone."""
    token = _login(ap_test["email"], ap_test["password"])
    resp = http.get(
        "/ap/mappa/zone",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
