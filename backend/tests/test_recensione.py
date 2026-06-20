"""[IF-UT.15] Test Scrive Recensione — scenari base e alternativi."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _elimina_recensione(db, recensione_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM recensioni WHERE id = :id"), {"id": recensione_id})
        s.commit()


# ── Scenario base: voto + commento ───────────────────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_scenario_base(utente_test, db):
    """[IF-UT.15] Utente autenticato scrive recensione con voto e commento → 201."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 5, "commento": "Servizio ottimo"},
        headers=_auth(token),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["voto"] == 5
    assert body["commento"] == "Servizio ottimo"
    assert "id" in body
    assert "created_at" in body
    # cleanup
    _elimina_recensione(db, body["id"])


# ── Scenario alternativo: voto valido senza commento ─────────────────────────

@pytest.mark.integration
def test_scrive_recensione_senza_commento(utente_test, db):
    """[IF-UT.15] Voto valido senza commento → 201, commento null."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 3},
        headers=_auth(token),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["commento"] is None
    # cleanup
    _elimina_recensione(db, body["id"])


# ── Scenario alternativo: voto fuori range → 422 ─────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_voto_fuori_range(utente_test):
    """[IF-UT.15] Voto fuori dall'intervallo [1,5] → 422."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 6, "commento": "x"},
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ── Scenario alternativo: non autenticato → 401 ──────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.post("/utente/recensioni", json={"voto": 4})
    assert resp.status_code == 401
